#!/usr/bin/env python3
"""corpus_lint.py - documentation consistency linter for the P vs NP corpus.

Stdlib only (python3, no dependencies). Validates the whole corpus in one run and
lives at the corpus root. The corpus layout it expects:

  ./                    GOAL.md, README.md, LOG.md, bibliography.md, this checker
  docs/                 route maps, theory, forensics, theorem map
  docs/monitors/        dated monitoring screens
  experiments/          all python scripts (mutual imports stay same-dir)
  paper/                the LaTeX write-up and its change log
  lean_channel/         the Lean 4 formalization project (excluded from scans)

Checks:
  1. compile      - every *.py under experiments/ compiles (py_compile).
  2. references   - every backtick `file.md` / `file.py` reference in any *.md
                    document resolves by basename somewhere in the corpus tree.
  3. retractions  - the exact retraction-marker strings (the ">>"-prefixed lines of
                    LOG.md) appear ONLY in LOG.md; no other document uses the
                    ">>" marker style or quotes a marker line.
  4. key claims   - required substrings (proved-result names, verdicts, taxonomic
                    definitions) are present in the document that owns them.
  5. log structure- LOG.md headings parse, entry timestamps are monotone
                    non-decreasing, and no heading line is duplicated.
  6. orphan script- every *.py filename is mentioned somewhere in the corpus
                    documentation (*.md plus paper/*.tex).
  7. numbers      - measured constants quoted in README.md appear in the
                    corresponding detail documents (whitespace-normalized
                    matching), including the arithmetic identity behind
                    q = 10/38 at (32,2).
  8. proved registry - every entry in proved_registry.py (one tuple per PROVED
                    claim in docs/current_results.md) has its proof anchor
                    substring present in the named proof document and a
                    corresponding line in current_results.md; conversely the
                    section-2 entry headers of current_results.md are exactly
                    the registry's REQUIRED_CLAIMS mirror, each backed by a
                    registry claim.
  9. label hygiene- HEURISTIC TRIPWIRE, not a proof of anything: a PROVED
                    marker in docs/*.md (statement position; correction and
                    retraction lines excluded) must be accompanied by
                    proof-kind vocabulary (proof/enumerated/machine-checked/
                    Theorem/Lemma) somewhere in its enclosing section, or
                    cite a registry claim_id.

The checker never writes to the corpus: compilation artifacts go to a temp dir.
Exit status: 0 if the corpus is clean, 1 otherwise.
"""

from __future__ import annotations

import py_compile
import re
import sys
import tempfile
from collections import Counter
from pathlib import Path

# The PROVED registry is the data half of check 8 and lives beside this file
# at the corpus root (script-dir import; the stdlib-only constraint is
# unchanged for the lint's own logic).
import proved_registry

CORPUS = Path(__file__).resolve().parent

# This checker is tooling, not a corpus artifact: exclude it from the corpus
# script set (it is trivially self-compiled by running, and not documented in
# the corpus documents).
LINT_NAME = Path(__file__).resolve().name

# Scripts registered by agents still writing their owning documents: skipped
# until the document lands (then remove the entry; the lint will enforce it).
PENDING_SCRIPTS: dict[str, str] = {}

# ---------------------------------------------------------------------------
# Whitelists and needle tables (keep documented; extend only with a reason).
# ---------------------------------------------------------------------------

# (source document, backtick target) -> reason the target is allowed to be absent.
# Empty today: every backticked *.md / *.py reference in the corpus resolves.
REFERENCE_WHITELIST: dict[tuple[str, str], str] = {
    # GUIDANCE.md is a verbatim external review; it may cite the checker's old name.
    ("GUIDANCE.md", "verify_corpus.py"): "quoted external review text",
    # odd-p deliverable landed; keep the wildcard mechanism for future in-flight files.
    ("__any__", "chi_odd_p_check.py"): "document landed 2026-10-04",
}

# (document, required substring), matched after collapsing whitespace runs to a
# single space, so strings that wrap across source lines still match.
KEY_CLAIMS: list[tuple[str, str, str]] = [
    # (file, needle, why it must be there)
    ("proof_complexity.md", "Theorem B (adaptive single-variable cap, PROVED)",
     "session's adaptive single-variable theorem, proved"),
    ("proof_complexity.md", "Lemma B.1 (mild coupling; statement and PROOF COMPLETE; quantifier REPAIRED",
     "Lemma B.1 with complete proof"),
    ("proof_complexity.md", "Proposition A (fixed-label exactness, proved)",
     "Prop A present"),
    ("proof_complexity.md", "Proposition C (non-adaptive single-variable cap, PROVED)",
     "Prop C present"),
    ("proof_complexity.md", "Proposition D (non-adaptive cap at ALL query degrees, p = 2, PROVED)",
     "Prop D present"),
    ("proof_complexity.md", "Open Problem O1 (formal)",
     "O1 formal statement"),
    ("proof_complexity.md", "RESOLUTION OF O1 (definitive",
     "single definitive O1 resolution"),
    ("two_phase_tree.md", "Theorem T (exact error law of the two-phase tree, PROVED)",
     "Theorem T, proved"),
    ("two_phase_tree.md", "SIMULATOR ARTIFACT",
     "major correction block present"),
    ("two_phase_tree.md", "2^{-Theta(d^2)}",
     "Theorem F floor exponent (correction)"),
    ("two_phase_tree.md", "The chi-hypothesis of Theorem 6.1 SURVIVES",
     "corrected chi-hypothesis status"),
    ("two_phase_tree.md", "fired 0 times in 816,000 tree simulations",
     "phase-2-fail empirical confirmation"),
    ("two_phase_tree.md", "beats the cap by 4x",
     "4x advantage over Theorem B's cap"),
    ("edwards_audit.md", "Verdict: the proof fails.",
     "Edwards audit verdict"),
    ("edwards_audit.md", "Verdict and taxonomy mapping",
     "taxonomy mapping section"),
    ("edwards_audit.md", "Proposed new mode F7",
     "F7 proposal"),
    ("goertzel_audit.md", "Verdict: the proof fails.",
     "Goertzel audit verdict"),
    ("goertzel_audit.md", "Proposition 1 (the trilemma, formal",
     "formalized trilemma"),
    ("goertzel_audit.md", "Lemma 2.12",
     "Finding 1 anchor"),
    ("failure_modes.md", "F7 (PROPOSED, 2026-10-03, first instantiation Edwards)",
     "F7 defined in the taxonomy"),
    ("failure_modes.md", "Protean surrogate / definition drift",
     "F7 name and mechanism"),
    ("failure_modes.md", "F1. Redefinition of the target.",
     "F1 defined"),
    ("failure_modes.md", "F6. Formalization mismatch.",
     "F6 defined"),
    ("failure_modes.md", "one-line field guide",
     "triage procedure"),
    ("note_to_author.md", "Reading-check question",
     "note is a question draft per GUIDANCE, not a claim"),
    ("cert_floor.md", "Theorem F (exact certification floor) - PROVED",
     "Theorem F present"),
    ("p_family.md", "characteristic-uniform",
     "chi-task p-uniformity verified"),
    ("proof_complexity.md", "Proposition D: FALSE AS STATED",
     "Prop D retraction"),
    ("thmT_verify.md", "Theorem T and both per-hit posterior caps: independent replication",
     "replication title"),
    ("thmT_verify.md", "Points: (16,1), (24,3), (48,4), (96,6), (128,8)",
     "the five replication points"),
    ("thmT_verify.md", "816000 two-phase simulations",
     "aggregate simulation count"),
    ("clues.md", "6. Evidence balance sheet",
     "evidence balance section"),
    ("clues.md", "Position statement DOWNGRADED per GUIDANCE.md 2026-10-04",
     "evidence balance removed per guidance (no confidence claims)"),
    ("williams_ladder.md", "n^{2.5-eps}-size THR o THR circuits",
     "2026 frontier record"),
    ("williams_ladder.md", "OR-closure",
     "documented blocker"),
    ("magnification_gap.md", "2*eps - delta",
     "known exponent"),
    ("magnification_gap.md", "2*eps + o(1)",
     "needed exponent"),
    ("algebraic_rung.md", "GCT occurrence obstructions are impossible in the padded det-vs-perm orbit-closure setting",
     "pinned no-go wall"),
    ("monitor_2026-10-03b.md", "arXiv:2609.35927 (pseudo-solutions / AC0[p]-Frege program): CLEAN",
     "monitor verdict"),
    ("monitor_2026-10-03b.md", "arXiv:2609.23015 (unrestricted Res(+o+) BPHP lower bound): CLEAN",
     "monitor verdict"),
    ("monitor_frontiers_2026-10-03.md", "FIRED: none. WEAKENED: none.",
     "frontiers monitor verdict"),
    ("README.md", "No fractional confidence",
     "README carries no confidence claim (GUIDANCE 2026-10-04)"),
    ("README.md", "2^{-Theta(d^2)}",
     "README states Theorem F"),
    ("README.md", "BUDGETED",
     "README states the budgeted reframing"),
]

# (README substring, detail doc, [detail substrings], note). Every README needle
# must appear in README.md and every detail needle in the detail document, so a
# constant cannot silently drift out of either side.
NUMERIC_CONSISTENCY: list[tuple[str, str, list[str], str]] = [
    ("0.97 at (32,2)", "two_phase_tree.md", ["0.97 at (32,2)"],
     "two-phase tree measured success"),
    ("1.000 at d=8 with retries", "two_phase_tree.md", ["1.0000 at d = 8"],
     "retry extension at d=8"),
    ("0.9067", "proof_complexity.md", ["0.9067 at (64,2)"],
     "Prop D counterexample success"),
    ("beating Theorem B's single-variable cap 4x", "two_phase_tree.md",
     ["beats the cap by 4x"], "4x advantage"),
    ("measured 0.8500", "two_phase_tree.md", ["0.8500"],
     "literal two-phase tree error (correction block)"),
    ("2^{-Theta(d^2)}", "cert_floor.md", ["2^{-Theta(d^2)}"],
     "Theorem F floor exponent"),
    ("(1,439 / 80,639 / >150,000 nodes at h = 6/8/10)", "clues.md",
     ["1439 nodes at h=6", "80639 nodes at h=8", "150000-node cap at h=10"],
     "PHP node counts"),
    ("|Des(4,2)| = 2^65", "proof_complexity.md", ["2^65"],
     "design-space dimension"),
    ("|Des(6,3)| = 2^2079", "proof_complexity.md", ["2^2079"],
     "design-space dimension"),
    ("violation rate 0.0005, not 0.37", "proof_complexity.md", ["0.0005", "0.37"],
     "corrected vs retracted violation rates"),
    ("success ~ n^{-1.77}", "proof_complexity.md", ["n^{-1.77}"],
     "adaptive cap scaling law"),
    ("success 0.24 vs 0.019 baseline", "proof_complexity.md",
     ["0.2367", "((2d+1)/(n+1)) * (2d/n)"],
     "adaptive lift vs Prop A base rate (5*4/(33*32) = 0.019)"),
    ("THR o THR from n^{2-o(1)} to n^{2.5-eps}", "williams_ladder.md",
     ["n^{2.5-eps}-size THR o THR circuits"], "frontier exponent"),
    ("~3.1n (B2) / 5n-o(n) (U2)", "williams_ladder.md",
     ["3.1n - o(n)", "5n - o(n)"], "circuit lower bound stall"),
    ("n^{2eps-delta} vs needed n^{2eps+o(1)}", "magnification_gap.md",
     ["2*eps - delta", "2*eps + o(1)"], "magnification bookkeeping"),
]

# Posterior identity checked arithmetically: at (32,2) proof_complexity.md pins
# f = 20/1056 and m = 28/1056, so the answer-1 posterior is
# (f/2)/(f/2 + m) = 10/38 = 0.263 (q), quoted in proof_complexity.md and LOG.md.
Q_IDENTITY_DETAILS = [
    ("proof_complexity.md", ["f = 20/1056, m = 28/1056", "0.263"]),
    ("LOG.md", ["0.263"]),
]


def norm(text: str) -> str:
    """Collapse all whitespace runs to single spaces for robust substring matching."""
    return re.sub(r"\s+", " ", text)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


class Report:
    """Accumulates per-check results and failure details."""

    def __init__(self) -> None:
        self.rows: list[tuple[str, int, str]] = []
        self.details: list[str] = []

    def add(self, name: str, items: int, failures: list[str]) -> None:
        self.rows.append((name, items, "FAIL" if failures else "PASS"))
        for failure in failures:
            self.details.append(f"[{name}] {failure}")

    @property
    def ok(self) -> bool:
        return not self.details


# ---------------------------------------------------------------------------
# Checks
# ---------------------------------------------------------------------------

def check_compile(scripts: list[Path], report: Report) -> None:
    failures = []
    with tempfile.TemporaryDirectory(prefix="verify_corpus_") as tmp:
        for script in scripts:
            try:
                py_compile.compile(
                    str(script),
                    cfile=f"{tmp}/{script.name}.pyc",
                    doraise=True,
                )
            except py_compile.PyCompileError as exc:
                failures.append(f"{script.name} does not compile: {exc}")
    report.add("1. compile scripts", len(scripts), failures)


def check_references(docs: list[Path], report: Report) -> None:
    ref_re = re.compile(r"`([^`\n]+)`")
    name_re = re.compile(r"[A-Za-z0-9][A-Za-z0-9_./-]*\.(?:md|py)")
    # Resolve references by basename anywhere in the corpus tree (the corpus is
    # organized into docs/, docs/monitors/, experiments/, paper/, lean_channel/),
    # excluding toolchain internals.
    index = {
        p.name: p
        for p in CORPUS.rglob("*")
        if p.is_file()
        and not {"lean_channel", "__pycache__", ".lake", "mathlib4", ".git"}.intersection(
            p.parts
        )
    }
    failures = []
    total = 0
    for doc in docs:
        text = read(doc)
        seen: set[str] = set()
        for match in ref_re.finditer(text):
            token = match.group(1).strip().rstrip(".,;:)!?")
            if not name_re.fullmatch(token) or token in seen:
                continue
            seen.add(token)
            total += 1
            if Path(token).name in index:
                continue
            if (doc.name, token) in REFERENCE_WHITELIST or ("__any__", token) in REFERENCE_WHITELIST:
                continue
            line = text[: match.start()].count("\n") + 1
            failures.append(
                f"{doc.name}:{line}: backtick reference `{token}` does not resolve"
            )
    report.add("2. backtick file references", total, failures)


def check_retractions(docs_raw: dict[str, str], report: Report) -> None:
    others = {n: t for n, t in docs_raw.items() if n != "LOG.md"}
    markers = [ln.rstrip() for ln in docs_raw.get("LOG.md", "").splitlines()
               if ln.lstrip().startswith(">>")]
    failures = []
    if not markers:
        failures.append("LOG.md contains no '>>' retraction markers; check is vacuous")
    for name in sorted(others):
        text_norm = norm(others[name])
        for marker in markers:
            if marker in text_norm:
                failures.append(f"{name} quotes LOG.md retraction marker: {marker!r}")
        for lineno, ln in enumerate(others[name].splitlines(), 1):
            if ln.lstrip().startswith(">>"):
                failures.append(f"{name}:{lineno}: uses the '>>' retraction-marker style")
    report.add("3. retracted-claim containment", len(markers) * len(others), failures)


def check_key_claims(doc_norm: dict[str, str], report: Report) -> None:
    failures = []
    for fname, needle, why in KEY_CLAIMS:
        if needle not in doc_norm.get(fname, ""):
            failures.append(f"{fname}: missing required substring {needle!r} ({why})")
    report.add("4. key claims", len(KEY_CLAIMS), failures)


def check_log_structure(log_text: str, report: Report) -> None:
    failures = []
    lines = log_text.splitlines()
    headings = [(i, ln) for i, ln in enumerate(lines, 1) if ln.startswith("#")]
    entry_re = re.compile(r"^### (\d{4}-\d{2}-\d{2})")
    dates: list[str] = []
    for lineno, heading in headings:
        if heading.startswith("### "):
            match = entry_re.match(heading)
            if not match:
                failures.append(
                    f"LOG.md:{lineno}: entry heading lacks a YYYY-MM-DD timestamp: {heading!r}"
                )
            else:
                dates.append(match.group(1))
    if dates != sorted(dates):
        failures.append("LOG.md: entry timestamps are not monotone non-decreasing")
    duplicates = [h for h, n in Counter(h.rstrip() for _, h in headings).items() if n > 1]
    for heading in duplicates:
        failures.append(f"LOG.md: duplicate heading line: {heading!r}")
    if not any(ln.startswith("# ") for _, ln in headings):
        failures.append("LOG.md: no '# ' title heading")
    if not any(ln.rstrip() == "## Log" for _, ln in headings):
        failures.append("LOG.md: no '## Log' section heading")
    report.add("5. LOG structure", len(headings), failures)


def check_orphan_scripts(scripts: list[Path], docs: list[Path], report: Report) -> None:
    # PENDING_SCRIPTS are also exempt here (their owning doc is in flight).
    corpus_text = "\n".join(read(p) for p in docs + sorted((CORPUS / "paper").glob("*.tex")))
    failures = []
    for script in scripts:
        if script.name not in corpus_text:
            failures.append(
                f"{script.name} is an orphan: its name appears in no corpus documentation"
            )
    report.add("6. orphan scripts", len(scripts), failures)


def check_numbers(doc_norm: dict[str, str], report: Report) -> None:
    failures = []
    for readme_needle, detail, needles, note in NUMERIC_CONSISTENCY:
        if readme_needle not in doc_norm.get("README.md", ""):
            failures.append(f"README.md: missing quoted constant {readme_needle!r} ({note})")
        for needle in needles:
            if needle not in doc_norm.get(detail, ""):
                failures.append(
                    f"numeric consistency ({note}): {detail} lacks {needle!r} "
                    f"(quoted in README as {readme_needle!r})"
                )
    # q = 10/38 at (32,2): arithmetic identity plus its documented forms.
    f_half, m = 10 / 1056, 28 / 1056
    q = f_half / (f_half + m)
    if abs(q - 10 / 38) > 1e-12 or round(q, 3) != 0.263:
        failures.append(f"q identity broken: (f/2)/(f/2+m) = {q} != 10/38 = 0.263")
    for fname, needles in Q_IDENTITY_DETAILS:
        for needle in needles:
            if needle not in doc_norm.get(fname, ""):
                failures.append(
                    f"numeric consistency (q = 10/38 at (32,2)): {fname} lacks {needle!r}"
                )
    items = sum(len(n) for _, _, n, _ in NUMERIC_CONSISTENCY) + len(NUMERIC_CONSISTENCY) + 1
    report.add("7. numeric consistency", items, failures)


# ---------------------------------------------------------------------------
# Check 8 (proved registry) and check 9 (label hygiene)
# ---------------------------------------------------------------------------

# Lines that DEFINE the marker vocabulary (file legends such as
# "markers [PROVED], [MV]") are documentation of the label system, not
# statement positions for check 9.
LABEL_LEGEND_RE = re.compile(r"markers \[PROVED|Markers: PROVED|\[PROVED\], \[MEASURED\]")

# Proof-kind vocabulary accepted by check 9: the base list is Proof/proof,
# enumerated, machine-checked, Theorem, Lemma; "enumerat" is the stem covering
# "enumerated"/"enumeration", the two forms the corpus uses for the enumerated
# proof kind (docs/current_results.md section 1). Extended 2026-10-04 with the
# cls_cnt.md proof vocabulary stems (Buchberger, reduction, identities,
# exhaustive machine check) and PROOF pointers phrased as "proof chain"/"by
# induction".
PROOF_KIND_RE = re.compile(
    r"Proof|proof|enumerat|machine-checked|machine-check|Theorem|Lemma"
    r"|Buchberger|reduc|identit|induction|cor:coin"
)

# current_results.md section-2 entry headers ("### 2.N Title").
RESULTS_HEADER_RE = re.compile(r"^### (2\.\d+)\s+(.+)$")


def _resolve_doc(name: str) -> Path | None:
    for base in (CORPUS / "docs", CORPUS):
        candidate = base / name
        if candidate.is_file():
            return candidate
    return None


def check_proved_registry(docs_raw: dict[str, str], report: Report) -> None:
    """Check 8: the PROVED registry against docs/current_results.md.

    Forward: every registry entry's anchor substring must appear in its proof
    document, and the claim must have a corresponding line in
    current_results.md (matched on claim_id, or on the statement's first 40
    characters, whitespace-normalized). Converse: the section-2 entry headers
    of current_results.md must be exactly the REQUIRED_CLAIMS mirror, and each
    mirrored entry must have a registry claim.
    """
    failures: list[str] = []
    cur_lines = docs_raw.get("current_results.md", "").splitlines()
    cur_norm = [norm(ln) for ln in cur_lines]

    registry = proved_registry.PROVED_CLAIMS
    registry_ids = {claim[0] for claim in registry}

    doc_text: dict[str, str] = {}
    for claim_id, short, doc, anchor, kind in registry:
        if kind not in proved_registry.VERIFICATION_KINDS:
            failures.append(f"{claim_id}: unknown verification_kind {kind!r}")
        if doc not in doc_text:
            path = _resolve_doc(doc)
            doc_text[doc] = read(path) if path else ""
        if not doc_text[doc]:
            failures.append(f"{claim_id}: proof document {doc} not found in the corpus")
        elif norm(anchor) not in norm(doc_text[doc]):
            failures.append(f"{claim_id}: proof anchor {anchor!r} not present in {doc}")
        # The short statement is "<entry title> - <gloss>"; match on the
        # title part (capped at 40 chars), which appears verbatim in the
        # entry header line.
        prefix = norm(short).split(" - ")[0][:40].strip()
        if not any(claim_id in raw or prefix in nl
                   for raw, nl in zip(cur_lines, cur_norm)):
            failures.append(
                f"{claim_id}: no corresponding line in current_results.md "
                f"(matched on claim_id or statement prefix {prefix!r})"
            )

    parsed: dict[str, str] = {}
    for ln in cur_lines:
        match = RESULTS_HEADER_RE.match(ln)
        if match:
            parsed[match.group(1)] = norm(match.group(2))
    required = {num: norm(title) for num, title in proved_registry.REQUIRED_CLAIMS}
    for num, title in parsed.items():
        if num not in required:
            failures.append(
                f"current_results.md: entry {num} ({title!r}) is not mirrored in "
                f"REQUIRED_CLAIMS"
            )
        elif required[num] != title:
            failures.append(
                f"current_results.md: entry {num} title drifted from REQUIRED_CLAIMS: "
                f"{title!r} != {required[num]!r}"
            )
    for num, title in required.items():
        if num not in parsed:
            failures.append(
                f"current_results.md: REQUIRED_CLAIMS entry {num} ({title!r}) has "
                f"no section-2 header"
            )
        if f"CR-{num}" not in registry_ids:
            failures.append(f"REQUIRED_CLAIMS entry {num} has no registry claim CR-{num}")

    items = 2 * len(registry) + len(required) + len(parsed)
    report.add("8. proved registry", items, failures)


def check_label_hygiene(docs: list[Path], docs_raw: dict[str, str], report: Report) -> None:
    """Check 9: label-hygiene tripwire over docs/*.md.

    HEURISTIC, not a proof: a PROVED marker in statement position must carry
    proof-kind vocabulary somewhere in its enclosing section, or cite a
    registry claim_id. Statement position excludes LOG.md, lines of the
    correction/retraction machinery (RETRACT/DOWNGRADE), and marker-legend
    lines. The corpus's one-sentence-per-line style splits labels from their
    proof pointers, so the unit of inspection is the enclosing markdown
    section, not the bare line.
    """
    claim_ids = [claim[0] for claim in proved_registry.PROVED_CLAIMS]
    failures: list[str] = []
    total = 0
    docs_dir = CORPUS / "docs"
    for doc in docs:
        if doc.parent != docs_dir or doc.name == "LOG.md":
            continue  # scope: docs/*.md top level
        lines = docs_raw[doc.name].splitlines()
        total_lines = len(lines)
        # Headers are markdown headings only: lines starting with '#' OUTSIDE
        # fenced code blocks (a '#'-comment inside a fence is not a heading,
        # and treating it as one truncates the section scan).
        headers = []
        in_fence = False
        for i, ln in enumerate(lines):
            if ln.lstrip().startswith("```"):
                in_fence = not in_fence
                continue
            if not in_fence and ln.startswith("#"):
                headers.append(i)
        def heading_level(ln: str) -> int:
            n = 0
            for ch in ln:
                if ch == '#':
                    n += 1
                else:
                    break
            return n
        for i, ln in enumerate(lines):
            if not re.search(r"\bPROVED\b", ln):
                continue
            if "RETRACT" in ln or "DOWNGRADE" in ln:
                continue
            # Label/status assignment lines are metadata, not statements: the
            # enclosing section carries the proof pointer (check 8 covers
            # traceability for registry claims).
            if re.match(r"^\s*(Label|Status)\s*:", ln):
                continue
            total += 1
            if LABEL_LEGEND_RE.search(ln):
                continue
            # A flagged HEADING line owns its whole section including nested
            # subsections: the section ends at the next heading of the same or
            # higher level. A flagged body line uses the enclosing subsection.
            if i in headers:
                lvl = heading_level(ln)
                section_start = i
                section_end = min(
                    (j for j in headers if j > i and heading_level(lines[j]) <= lvl),
                    default=total_lines,
                )
            else:
                section_start = max((j for j in headers if j <= i), default=-1)
                section_end = min((j for j in headers if j > i), default=total_lines)
            context = norm("\n".join(lines[section_start:section_end])) \
                if section_start >= 0 else norm(ln)
            if PROOF_KIND_RE.search(context):
                continue
            if any(cid in ln for cid in claim_ids):
                continue
            failures.append(
                f"{doc.name}:{i + 1}: PROVED statement with no proof pointer in "
                f"its section (heuristic tripwire): {ln.strip()[:90]!r}"
            )
    report.add("9. label hygiene (heuristic tripwire)", total, failures)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    scripts = sorted(p for p in (CORPUS / "experiments").glob("*.py")
                     if p.name not in PENDING_SCRIPTS)
    doc_dirs = [CORPUS, CORPUS / "docs", CORPUS / "docs" / "monitors"]
    docs = sorted({p for d in doc_dirs for p in d.glob("*.md")})
    docs_raw = {d.name: read(d) for d in docs}
    doc_norm = {name: norm(text) for name, text in docs_raw.items()}
    log_text = docs_raw.get("LOG.md", "")

    report = Report()
    check_compile(scripts, report)
    check_references(docs, report)
    check_retractions(docs_raw, report)
    check_key_claims(doc_norm, report)
    check_log_structure(log_text, report)
    check_orphan_scripts(scripts, docs, report)
    check_numbers(doc_norm, report)
    check_proved_registry(docs_raw, report)
    check_label_hygiene(docs, docs_raw, report)

    print(f"Corpus root: {CORPUS}")
    print(f"Documents: {len(docs)}   Scripts: {len(scripts)}")
    print()
    name_w = max(len(name) for name, _, _ in report.rows) + 2
    items_w = max(len(str(items)) for _, items, _ in report.rows)
    print(f"{'Check':<{name_w}}{'Items':>{items_w + 2}}    Result")
    print("-" * (name_w + items_w + 12))
    for name, items, verdict in report.rows:
        print(f"{name:<{name_w}}{items:>{items_w + 2}}    {verdict}")
    total_items = sum(items for _, items, _ in report.rows)
    total_fail = len(report.details)
    print("-" * (name_w + items_w + 12))
    print(f"{'TOTAL':<{name_w}}{total_items:>{items_w + 2}}    "
          f"{'CLEAN' if report.ok else f'{total_fail} failure(s)'}")
    if report.details:
        print()
        print("Failures:")
        for detail in report.details:
            print(f"  - {detail}")
    print()
    print("CORPUS_LINT: " + ("PASS (corpus clean)" if report.ok else "FAIL"))
    return 0 if report.ok else 1


if __name__ == "__main__":
    sys.exit(main())
