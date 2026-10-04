# GOAL.md - standing instructions for this session (compiled 2026-10-04)

This file compiles every standing instruction the corpus owner has given. It is
the resume-point for any future session: read it, then README.md, then LOG.md's
tail. Maintenance: when the owner issues a new standing instruction, update the
relevant section here, append the verbatim entry to instruction_log.md, and
note the change in LOG.md.

## 1. The objective

Prove or disprove P != NP.

Honest framing (owner-accepted, in force since the first session): a bounded
session will not resolve a Millennium Problem. The operational goal is therefore
dual-track and both tracks are mandatory:

(a) Keep a rigorous, verified research corpus around the problem: route maps with
named walls and trigger conditions, claim forensics, original proved results,
experiments, and precisely-stated open problems.
(b) Make real mathematical progress on the most promising engaged program - the
p=2 core of the Krajicek pseudo-solution program (arXiv:2609.35927), whose open
core is the all-degrees budgeted err-floor (O2 in open_problems.md).

The objective is never redefined as met by a smaller subtask. Never present the
work as finished or blocked merely because it is hard, slow, or uncertain.

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
  alter a verify_corpus.py needle string, update the needle in the same change.

## 4. Corpus conventions

- LOG.md: timestamped audit trail, append-only, orchestrator-only. Every
  dispatch, finding, correction, screen, and incident gets an entry.
- verify_corpus.py (corpus root) is the machine gate: run it before declaring
  any turn's consolidation complete; it must PASS (the count grows with the
  corpus; ~398 checks as of 2026-10-04).
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
  * Machine gate: verify_corpus.py (corpus root); Lean artifacts: lean_channel/.
- Commit and push (owner instruction, 2026-10-04): whenever relevant - i.e.,
  after every consolidated turn (agent results integrated, corrections applied,
  reorganizations, paper or doc updates), run verify_corpus.py first; commit
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

- The all-degrees budgeted err-floor (O2): degrees 2 and 3 are PROVED (Theorem 3
  and Theorem 3'; same d^2 ~ n chi-boundary). The open quantifier is degree >= 4;
  the degree-3 template (star sum rules, alias classes via Boolean identities,
  wedge/Z certificate inventory) is the stated consumption target.
- Theorem 3's query-class coverage is a proper subset of the printed degree-2
  class (F_2 mixtures; likely shallow repair - GAP B').
- Rigor gaps: Lemma M (O5 degree-2 transfer), de-modularizing the JDP steps,
  exact exponent constants.
- Second front: the odd-p analogue (O6, p_family.md; T_p needs the parity-locked
  recompute).
- Route note of record: the PRINTED Theorem 6.1(3) is false as printed
  (chi_transfer.md Theorem 3); the live route is the err-form assembly
  (chi_transfer.md Theorem 4), whose premise is exactly O2.

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
