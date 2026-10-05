# Guidance on the P vs NP corpus

Rewritten 2026-10-05 (fifth review). Reviewed: layout, README, GOAL, the LOG
tail, current_results.md (all of section 2, plus sections 3-6), theorem_map.md,
all_degrees.md section 5, inv3.md (sections 0, 3.3, 7.4-7.6), mixture4.md
(sections 0, 7, 10-11), proved_registry.py, corpus_lint.py checks 2/6/8/9, the
in-flight chi_inv3_certify.py, chi_mixture4.py, note_to_author.md,
paper/CHANGES.md, the working tree, and git history. References to "GUIDANCE
priority N" elsewhere point at the second review unless stated.

## State of play since the fourth review

- No consolidated turn has landed. HEAD is the fourth review (commit 6fc3432),
  which changed only GUIDANCE.md; the last substantive commit is c0a669c
  (MIXTURE-4). The working tree carries only the same two untracked scripts the
  fourth review already reviewed (chi_inv3_certify.py, mtime 03:45;
  chi_mixture4.py, mtime 00:22), and both predate the 04:03 fourth-review
  commit. No /tmp/opencode certification or mixture artifacts exist.
- Every fourth-review priority is still open, so nothing is dropped as
  addressed. This review keeps the live items, sharpens three of them with new
  evidence (the certification script cannot return CERTIFIED in either mode;
  the MIXTURE-4 repair is missing from five more places than the fourth review
  named, including current_results.md itself; the gate's file check reads the
  disk, not git), and drops the fourth review's historical accounting.

## What this is now

Still not a P vs NP investigation. It is a source-anchored study of one finite
algebraic obstruction, INV(d) (the degree-truncated Buchberger completion on
increasing rectangles) for Krajicek's pseudo-solution pipeline, plus a survey
and a claim-forensics record. Even a complete proof of INV(d) yields only a
conditional lower bound (Theorem R, premise O2). The object is now: O2's cap
assembled at every degree 2-5 with the same d^2 ~ n boundary, MIXTURE-d closed
at d <= 4 (Theorem M4-D) and open at d >= 5, and exactly one mathematical gap
left (INV(d) at t >= 3).

## What is genuinely good

- The correction culture still works. MIXTURE-4 is a clean, well-bounded result
  (star-4M winner, constants digit-exact, its own assert caught a coin-keying
  non-conformance), and mixture4.md corrects mixture3.md section 2.2's
  support-4 attribution without moving a registered number. Nineteenth
  correction-class event.
- current_results.md is still the right idea: one current statement, labels
  PROVED/MEASURED/INFERRED, with proved_registry.py and corpus_lint.py checks
  8-9 enforcing traceability.
- The adversarial gate (chi_engine_adversarial.py) and the downgrade block at
  the top of inv3.md are the structural response to the recurring
  promotion-before-verification failure, and they are working.

## Problems, most important first

1. **The in-flight certification scan cannot certify in any coded mode, and the
   closure still rests on the false Lemma TB.** New, checkable evidence:
   - Its sharded JOB_PLAN samples six classes, not one: (AD3, b), (AD3, C),
     (AD3, H), (AD3, ST), (AD2, AD3) take 2,000-4,000 pairs each, and
     (AD3, AD3) takes 600 of 217,470. But do_collect marks only AD3xAD3 as
     sampled, so its coverage check fails on the other five and the verdict is
     INCONCLUSIVE, not the "exit 0 CERTIFIED ... on the stated coverage" the
     docstring advertises.
   - The single-process path's default 3000 s guard cannot cover the
     (AD3, AD3) class (12-40 h alone), so it too ends INCONCLUSIVE.
   - inv3.md still frames the result through Lemma TB (section 7.4: "By Lemma
     TB ... PROVED at d = 5"), though that lemma is false as stated.
   Fix the contract to match the argument the scan actually implements: if the
   engine closes over all lcm <= t pairs with the neutrality checks, and an
   EXHAUSTIVE hidden-pair scan of the final G* finds every in-cap residue in
   W_t, then G* is a truncated Groebner basis and I cap S_{<=3} = W_3, with no
   appeal to Lemma TB. Either make the scan exhaustive (no sampling, and a
   verdict that is never CERTIFIED on partial coverage), or state the verdict
   as SAMPLED and leave d = 5 as engine output. Sampling the (AD3, AD3) class
   is the worst place to sample. Even a full 11x10 scan certifies one
   rectangle; the open-ended per-rung trajectory remains.

2. **The PROVED gate is still not mechanical, and the lint cannot see the
   gap.** chi_mixture4.py, the registered script behind PROVED claim CR-2.22,
   is untracked, and the registry anchors CR-2.22 to a prose substring in
   mixture4.md. corpus_lint.py check 2 builds its index from CORPUS.rglob, so
   an untracked script resolves and a fresh clone would instead fail; check 6
   flags only orphan scripts, never a missing referenced one. Extend the gate:
   (a) every script named as a registered run in a PROVED entry must be tracked
   by git (git ls-files, not rglob); (b) an engine-derived PROVED label must
   carry a gate-verdict token (CERTIFIED or UNCERTIFIED); (c) add both
   requirements to GOAL section 4's passing state.

3. **current_results.md is no longer a single current statement, and the
   MIXTURE-4 repair is missing from five more places than the fourth review
   named.** Beyond the 2.10-versus-2.22 degree-4 cap duplication (2.10 shows
   q4*, 2.22 shows q4^mix and calls the degree-4 cap "Theorem 3'''", a name
   section 2.20 already uses for degree 5):
   - 2.18 line 749: mixtures "covered only at d <= 3"; 2.19 line 800:
     MIXTURE-d "open at d >= 4"; section 4 item (ii) line 1038: "closed at
     d <= 3"; section 5 line 1106: "closed at d <= 3"; section 6's
     consolidation note lines 1130-1133 still says "No live inconsistency ...
     closed at d <= 3".
   - 2.22 does not follow the entry template (Label first, no Proof location,
     no Regime of validity), is written in ASCII where section 2 uses LaTeX,
     and omits the CONJECTURED support <= 4 truncation dominance that
     mixture4.md section 10 item 2 states (2.19 carries the analogous caveat
     for d <= 3).
   Repair 2.10 or fold it into 2.22, rename the theorem to 3'' (degree 4),
   rewrite 2.22 in the section-2 template and LaTeX, and propagate "closed at
   d <= 4, open at d >= 5" to 2.18, 2.19, and sections 4-6.

4. **The newest wave also did not reach the map or the premise document.**
   theorem_map.md diagram 3 still lists GAP D (de-modularize the JDP steps) as
   open though ADDENDUM 8 closed it, still prints GAP E's superseded constants
   (cap ~0.32 vs witness 0.06; now 0.1864 and 0.1264), and still says
   "MIXTURE-d OPEN at d >= 4". all_degrees.md section 5.2 item 2 (and its
   lines 67 and 489) still says the mixture class "is covered only at d = 2".
   Run propagate-changes or an equivalent sweep so the map and the premise
   document match the statement of record.

5. **The external reading-check is still unsent, and it is still the
   highest-value action.** Every result rests on a reading of Krajicek's
   Definition 3.1 and 4.3 and the p = 2 restriction that no expert has
   confirmed. note_to_author.md is a question draft; sending or explicitly
   parking it is the owner's call, and no amount of algebra removes the
   dependency.

6. **The program still has no finite endpoint, and two GOAL rules still
   contradict the record.** The 11x10 memory wall was bypassed by Lemma Q, so
   the adopted "if 11x10 is memory-walled, write it up and stop" rule cannot
   fire; the certification wall replaced it. GOAL section 1 still says no new
   rectangle is attempted before the engine passes the adversarial gate, but
   the gate FAILed and d = 5 was run and committed. Name the single result
   that justifies continuing past d = 5, and the condition under which the
   study is written up as a bounded result (the certified low-degree facts,
   the 4-hole exotic, the false Lemma TB, the uncertified engine, and the
   five closed MIXTURE/CLS/CNT scope repairs), then stop.

7. **Hygiene, cheap and still open.** README is a 2026-10-03 portrait: it
   never names current_results.md, its artifact guide lists superseded files,
   it counts "nine" corrections (nineteen now), and its session-outcome list
   numbers 1, 2, 3, 2, 3, 4. GOAL section 9's O2 status still says MIXTURE-d
   is covered only at d = 2, and its INV status still says "an adversarial
   engine-validation agent is dispatched" (it ran and FAILed). inv3.md has two
   consecutive "### 7.6" headings. The duplicated names (Theorem B, Theorem R,
   Theorem 3'', Theorem 3''', Lemma CNT) are still disambiguated only by
   citation, and problem 3 shows the collision now costs a wrong label.

## What to do next, in priority order

1. Land or drop the in-flight work. Commit chi_mixture4.py (its run is already
   quoted as registered), and do not register or certify anything from
   chi_inv3_certify.py until it can certify by an argument it actually
   implements. Fix its verdict contract and coverage table, or make the plan
   exhaustive.
2. Re-base inv3.md section 7 (and sections 0, 3.3, 7.5) on the completion
   criterion rather than Lemma TB, and soften the inline "PROVED [MV]" labels
   at section 0 (d = 4), 3.3 (d = 4), 7.4 (d = 5), and the 7.5 table.
3. Make the gate mechanical (tracked run scripts; gate-verdict token) as in
   problem 2.
4. Repair current_results.md (problem 3): one degree-4 cap entry, the right
   theorem number, the conjectured-truncation caveat, LaTeX and template order,
   and MIXTURE-d propagated to 2.18, 2.19, and sections 4-6.
5. Propagate the newest wave to theorem_map.md and all_degrees.md (problem 4).
6. Replace the moot stop rule with the decision point of problem 6, and
   reconcile GOAL section 1 with the d = 5 record and GOAL section 9 with the
   current status.
7. Send or explicitly park the reading-check note, and record the decision
   either way.
8. Do the cheap hygiene (problem 7).

## Bottom line

The finding this pass is the stall. Nothing has landed since the fourth review,
and the in-flight certification scan cannot certify in either coded mode, let
alone by the false Lemma TB. The recurring failure (a computational artifact
promoted before verification) now sits in that scan and in the registry, and
the one current statement has spread the MIXTURE-d status across two answers
(d <= 3 and d <= 4). Land the clean mixture4 script, repair the statement of
record in one place, and do not extend an uncertified engine before d = 5
becomes another d = 4. The work is worth continuing only as a bounded study
with a declared endpoint, and only once the reading is confirmed.
