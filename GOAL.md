# GOAL.md - standing instructions for this session (compiled 2026-10-04)

This file compiles every standing instruction the corpus owner has given. It is
the resume-point for any future session: read it, then GUIDANCE.md, then
README.md, then LOG.md's tail. Maintenance: when the owner issues a new standing
instruction, update the relevant section here, append the verbatim entry to
instruction_log.md, and note the change in LOG.md. GUIDANCE.md is re-read
periodically per section 9.

## 1. The objective

Prove or disprove P != NP.

Status of that objective (GUIDANCE.md, 2026-10-04, supersedes earlier framing):
the problem is open, and this corpus has made no progress toward resolving it.
What the corpus is: (1) a careful, source-anchored reading of Krajicek's
reduction (arXiv:2609.35927) toward AC0[p]-Frege PHP lower bounds, restricted to
p=2, together with its open crux O2 (the all-degrees budgeted error floor);
(2) toy-scale proved results about that p=2 restriction; (3) claim forensics on
unrelated resolution preprints; (4) a formal open-problems catalog. It is not a
P vs NP investigation, and no fractional confidence in P != NP is claimed
anywhere in the corpus (the earlier "93%" line was a subjective prior, removed
per guidance).

Purpose of record (priority 2 of the guidance, adopted): a small contribution -
a careful note on the p=2 restriction of Krajicek's reduction - CONTINGENT on an
expert confirming the reading of Definitions 3.1 and 4.3 (see
docs/note_to_author.md, rewritten as a reading-check question). Until that
confirmation, everything here is a learning log and survey.

## 2. Operating mode: maximum parallel agents

- "Use as many agents as possible to work on parts of the problem in parallel."
- Fan out on non-overlapping tracks; every agent gets a self-contained prompt
  (corpus files to read first, exact deliverable paths, verification standard,
  no-corpus-writes rule).
- Only the orchestrator writes corpus documents and LOG.md; agents write only
  their own deliverable files. This avoids write conflicts and keeps one
  consolidation voice.
- Consolidate every agent result before relying on it: re-run or spot-check the
  work (rerun scripts, check proofs line by line, verify quotes against primary
  sources) before recording anything in the corpus.
- Concurrency discipline learned by experience: on a provider rate-limit death,
  queue the dead brief and probe with ONE redispatch when >= 8 agents are
  running; redispatch freely below that. Agents editing the same directory can
  collide (the lean-channel zombie incident): give concurrent agents disjoint
  write paths.

## 3. Verification standards (non-negotiable)

- Every claimed number comes from an executed run; every quote is anchored to
  the primary source (fetch the arXiv HTML/ECCC page; never trust a summary of a
  summary).
- Every finding is recorded with what is PROVED vs MEASURED vs CONJECTURED,
  explicitly marked.
- Self-corrections are caught by computation or primary-source checks, never by
  argument alone, and are logged in LOG.md as prominently as the findings
  (standing ledger: nine correction-class events + one quantifier repair so
  far). Retractions stay visible (corpus convention: correction blocks and
  RETRACTED markers in place).
- ascii style: one sentence per line; no em-dashes; no banned terms.
- Math (owner instruction, 2026-10-04): markdown renders `$...$` / `$$...$$`
  LaTeX. Use it for math in presentation documents (theorem map prose, README,
  open problems, audits); plain ASCII math remains the norm inside Mermaid node
  labels (no TeX there) and inside LOG.md working entries. If a conversion would
  alter a corpus_lint.py needle string, update the needle in the same change.

## 4. Corpus conventions

- LOG.md: timestamped audit trail, append-only, orchestrator-only. Every
  dispatch, finding, correction, screen, and incident gets an entry.
- corpus_lint.py (corpus root; renamed from verify_corpus.py per GUIDANCE) is a
  DOCUMENTATION CONSISTENCY LINTER, not a verifier: it checks that required
  substrings appear where expected, that scripts compile, and that LOG headings
  are ordered. A PASS means the documentation agrees with itself. It is NOT
  mathematical validation and must never be cited as such. The gate that means
  something is lean_channel/: lake build with the sorry/axiom budget asserted
  (see lean_channel/check_budget.sh), plus executed experiments regenerating
  quoted numbers.
- PROVED discipline (GUIDANCE, mechanical): a result may carry PROVED only with
  a written line-by-line proof or a machine-checked statement of the same
  proposition. Measured constants from simulations are MEASURED, never PROVED.
  Reading-dependent statements (e.g. the quantifier on printed (3)) are
  INFERRED and must say whose reading they depend on.
- Monitoring reduction (GUIDANCE): crank-claim monitoring is reduced to a
  one-line appendix per screen in docs/monitors/; no full audits of low-value
  claims unless the owner asks.
- Deliverables of record and their homes:
  * Route maps (docs/): williams_ladder.md, magnification_gap.md,
    algebraic_rung.md, proof_complexity.md (correction blocks and ADDENDA are
    part of the record).
  * Theorem map (docs/theorem_map.md): Mermaid blocks (no YAML front matter
    inside fences; renderers choke on it), validated structurally; keep it
    current when theorems land or die.
  * Bibliography (bibliography.md, corpus root): status-coded [V]/[L]/[R]/[I],
    correct-as-of dates, maintenance rule at the foot.
  * Open problems (docs/open_problems.md): formal statements, decisive
    toy-scale predictions, per-problem falsification conditions.
  * Paper (paper/p2_results.tex +PDF): kept at the corpus's post-correction
    state; recompile after every substantive change (tectonic; zero errors).
  * Claim forensics (docs/): goertzel_audit.md, edwards_audit.md,
    failure_modes.md (F1-F7 taxonomy).
  * Monitoring screens (docs/monitors/): one dated deliverable per screen.
  * Experiments (experiments/): every script, run-backed; mutual imports stay
    same-dir (razborov_check.py is the shared F_2 machinery).
  * Lint gate: corpus_lint.py (corpus root); Lean gate: lean_channel/check_budget.sh; Lean artifacts: lean_channel/.
- Commit and push (owner instruction, 2026-10-04): whenever relevant - i.e.,
  after every consolidated turn (agent results integrated, corrections applied,
  reorganizations, paper or doc updates), run corpus_lint.py (lint) and the
  lean budget check first; commit
  only a PASSING state, with a descriptive message naming the substantive
  change; push to the remote immediately after committing. Exclusions live in
  .gitignore (the mathlib4 clone and .lake are multi-GB rebuildable toolchain
  state; never force-add them). Never amend or rewrite pushed history - the
  LOG.md audit trail and git history are both append-only disciplines.
- The corpus owner's two reserved decisions: nothing is sent or posted anywhere
  (note_to_author.md is a draft; communication is the owner's call), and no
  public claims are made on the owner's behalf.

## 5. Monitoring obligations

- Screen arXiv/ECCC on a daily delta basis (monitor_YYYY-MM-DD.md deliverables):
  the engaged papers (2609.35927, 2609.23015) and their citations; the audited
  claims (2510.08814, 2512.11820) for author responses; new Res(+o+)/AC0[p] lane
  reports; new P vs NP resolution claims (triage against failure_modes.md, full
  audit only for load-bearing items).
- Known tripwires: pith.science machine reviews (note: its author rebuttals are
  machine-simulated), OpenAlex citation counts, the Braun-bound follow-up chain
  (Pang arXiv:2610.00837 was the first).

## 6. Current open core (what to attack next)

- The all-degrees budgeted err-floor (O2): degrees 2, 3, and 4 are PROVED
  (Theorem 3, Theorem 3', Theorem 3''; the SAME d^2 ~ n chi-boundary at every
  degree, degree-independent through 4). Theorem A (deg4_theory.md: matching-k
  columns vary at every d) is the general-d tool; the open quantifier is
  degree >= 5, consuming the degree-4 template (star classes, alias identities,
  mass monotonicity).
- Theorem 3's query-class coverage is a proper subset of the printed degree-2
  class (F_2 mixtures; likely shallow repair - GAP B').
- Rigor gaps: Lemma M (O5 degree-2 transfer), de-modularizing the JDP steps,
  exact exponent constants.
- Second front: the odd-p analogue (O6, p_family.md; T_p needs the parity-locked
  recompute).
- Route note of record (DOWNGRADED PER GUIDANCE): under the corpus's INFERENCE
  that the printed Theorem 6.1(3) quantifies over all budgeted trees, that
  hypothesis is violated by a trivial row-sum tree (chi_transfer.md Theorem 3),
  making the printed conditional unusable under our reading. The printed text
  quantifies over a tree T' from the paper's own construction, so this is a
  READING GAP, not a paper error; expert confirmation of the quantifier is a
  prerequisite for any claim. The err-form assembly (err_form_route.md Theorem R)
  is the conditional route under our reading, with premise = O2.

## 7. Environment constraints (learned, still binding)

- Disk: keep >1 GB free; formalization work needs >= 10 GB (mathlib). Never let
  agents download large toolchains without a disk check; clean build artifacts
  from lean_channel/ before re-cloning. The elan toolchain lives at its DEFAULT
  home /home/tomzx/.elan (moved out of /tmp on 2026-10-04; PATH line in
  ~/.bashrc) - do not reinstall it into /tmp or /tmp/opencode.
- Provider rate limits bite above ~8 concurrent agents; queue, probe, drain.
- Prefer /tmp/opencode for external temp files.

## 8. Owner instruction log

Moved to instruction_log.md (corpus root) on 2026-10-04. That file holds the
verbatim, dated history of every owner instruction; this file holds the
compiled, normative version. New instructions: update the section above,
append the verbatim entry there.

## 9. Standing self-review: read GUIDANCE.md

Owner instruction (2026-10-04): read GUIDANCE.md from time to time.

- GUIDANCE.md (corpus root) is the standing external review of this corpus,
  written 2026-10-04 after a full read of the artifacts and the primary sources.
- Read it at the start of every session (right after this file), and re-read it
  at least after every consolidated turn, so its recommendations are in view
  while the work is being framed and consolidated.
- Treat it as advisory: the owner decides which recommendations to adopt. When
  a recommendation is adopted, rejected, or already satisfied, say which and
  why, and record the decision in LOG.md.
- Where GUIDANCE.md and the current framing of this file or the corpus diverge,
  surface the divergence in LOG.md rather than silently following one or the
  other. In particular, its critique of the confidence verdict, of the verifier
  labeling, and of the Theorem 6.1(3) wording is unresolved until the owner
  rules on it.
- Do not delete or rewrite GUIDANCE.md. Extend it in place with dated addenda
  as recommendations are resolved, so the review stays a single living document.

- O5 status (2026-10-04): Lemma M PROVED (fresh-bit channel identification);
  O5 closes outright for d <= 3 and is reduced to Lemma CLS + Lemma CNT at
  general d. Theorem 3's constant repaired q -> q2* = max(q, q_and_exact);
  the d^2 ~ n boundary is unmoved (proof_complexity.md ADDENDUM 7).
