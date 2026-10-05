# Guidance on the P vs NP corpus

Rewritten 2026-10-05 (sixth review). Reviewed: layout, README, GOAL, the LOG
tail, current_results.md (the section 1 header, entries 2.10 and 2.16-2.22,
sections 3-6), theorem_map.md, all_degrees.md (sections 0 and 5), inv3.md (the
downgrade block and sections 0, 3.3, 7.4-7.6), mixture4.md, cls_cnt.md (section
3), regeneration_2026-10-04.md, proved_registry.py, corpus_lint.py checks
1/2/6/8/9, the two untracked scripts, note_to_author.md, and git history.
References to "GUIDANCE priority N" elsewhere point at the second review unless
stated.

## State of play since the fifth review

- Nothing has landed. HEAD is still the fifth review (e2d72f4, a GUIDANCE-only
  commit), with no commits after it. The working tree carries only the same two
  untracked scripts the fourth and fifth reviews already reviewed
  (chi_inv3_certify.py, mtime 03:45; chi_mixture4.py, mtime 00:22), both older
  than the 04:03 fourth-review commit. No /tmp/opencode certification or mixture
  artifacts exist.
- The guidance loop is not being closed. LOG.md has adopt/reject entries for the
  first and second reviews and none for the third, fourth, or fifth. GOAL
  section 9 requires that decision to be recorded. Instead, new result waves
  (MIXTURE-4, the d=5 closure, the certification scan) kept landing, and the
  newest wave's consolidation skipped exactly the passages the reviews named.
- Every fifth-review priority is still open. This pass adds five checkable
  findings: the MIXTURE-d status has split three ways, not two;
  current_results.md section 6 declares "no live inconsistency" while its own
  2.22 contradicts it; a second source document (mixture4.md) now misnumbers the
  degree-4 cap; the false Lemma TB still grounds cls_cnt.md's headline Q-A; and
  no independent regeneration pass covers the newest wave. The fifth review's
  historical accounting is dropped; its live items are kept and sharpened.

## What this is now

Still not a P vs NP investigation. It is a source-anchored study of one finite
algebraic obstruction, INV(d) (the degree-truncated Buchberger completion on
increasing rectangles) for Krajicek's pseudo-solution pipeline, plus a survey and
a claim-forensics record. Even a complete proof of INV(d) yields only a
conditional lower bound (Theorem R, premise O2). The statement of record is now:
O2's cap assembled at every degree 2-5 with the same d^2 ~ n boundary, MIXTURE-d
closed at d <= 4 (mixture4.md, the newest wave) and open at d >= 5, exactly one
mathematical gap left (INV(d) at t >= 3), and the d=5 closure labeled engine
output, uncertified.

## What is genuinely good

- The correction culture still works. MIXTURE-4 is a clean, well-bounded result
  (star-4M winner, constants digit-exact), and its registered run's own assert
  caught a coin-keying non-conformance before any number was trusted.
  Nineteenth correction-class event. mixture4.md also corrects mixture3.md
  section 2.2's support-4 attribution without moving a registered number.
- current_results.md is still the right idea: one current statement, labels
  PROVED/MEASURED/INFERRED, with proved_registry.py and corpus_lint.py checks
  8-9 enforcing traceability.
- The adversarial gate (chi_engine_adversarial.py) and the downgrade block at the
  top of inv3.md are the structural response to the recurring
  promotion-before-verification failure, and they are working. The current
  statements now carry the engine caveat explicitly (for example 2.16).

## Problems, most important first

1. **The in-flight certification scan cannot return CERTIFIED in either coded
   mode.** Re-verified this pass:
   - Sharded mode. Its JOB_PLAN samples six classes: (AD3, b), (AD3, C),
     (AD3, H), (AD3, ST), (AD2, AD3), and (AD3, AD3). do_collect treats only
     AD3xAD3 as sampled (line 900), so the coverage check fails on the other
     five and the verdict is INCONCLUSIVE. The docstring's "Exit code: 0
     CERTIFIED (on the stated coverage)" cannot be reached.
   - Single-process mode. The default 3000 s guard cannot cover the (AD3, AD3)
     class (12-40 h alone), so the scan is marked incomplete and the verdict is
     again INCONCLUSIVE.
   - inv3.md still frames the result through Lemma TB (section 7.4: "By Lemma TB
     ... PROVED at d = 5"), though that lemma is false as stated.
   Fix the contract to match the argument the scan actually implements: if the
   engine closes over all lcm <= t pairs with the neutrality checks, and an
   EXHAUSTIVE hidden-pair scan of the final G* finds every in-cap residue in
   W_3, then G* is a truncated Groebner basis and I cap S_{<=3} = W_3, with no
   appeal to Lemma TB. Either make the scan exhaustive (no sampling, and a
   verdict that is never CERTIFIED on partial coverage), or state the verdict as
   SAMPLED and leave d = 5 as engine output. Note where the sampling lands: the
   (AD3, AD3) pairs carry 73-94 term bodies and are exactly the ones the engine
   cannot see. Even a full 11x10 scan certifies one rectangle; the per-rung
   trajectory remains open-ended.

2. **The PROVED gate is still not mechanical, and nothing ties a registered run
   to a tracked script.** chi_mixture4.py, the registered script behind PROVED
   claim CR-2.22, is untracked, and the registry anchors CR-2.22 to the prose
   substring "Repaired cap (Theorem M4-D)" in mixture4.md. corpus_lint.py check
   2 builds its file index from CORPUS.rglob, so the untracked script resolves on
   this disk while a fresh clone would instead fail; check 6 flags only orphan
   scripts, never a missing referenced one. Extend the gate: (a) every script
   named as a registered run in a PROVED entry must be tracked by git (git
   ls-files, not rglob); (b) an engine-derived PROVED label must carry a
   gate-verdict token (CERTIFIED or UNCERTIFIED); (c) add both requirements to
   GOAL section 4's passing state.

3. **The MIXTURE-d statement has split three ways, and the consolidation note
   declares the corpus consistent.** The live answers are:
   - d = 2: all_degrees.md lines 65-67 and 486-489 ("covered only at d = 2").
   - d <= 3: current_results.md 2.18 (line 749), 2.19 (title line 771 and line
     799), section 4 item (ii) (line 1037), section 5 (lines 1104-1105), section
     6 (lines 1131-1133); proof_complexity.md ADDENDUM 12 (line 1186);
     theorem_map.md (lines 105, 174).
   - d <= 4: current_results.md 2.22 (lines 926, 953); mixture4.md.
   Worse, current_results.md section 6 says "No live inconsistency between
   sources was found" and states the resolved form as "closed at d <= 3" (line
   1133), contradicting the file's own 2.22. And mixture4.md itself mislabels the
   degree-4 cap: line 73 reads "Theorem 3''' as printed (deg4_theory.md Theorem
   3'')", conflating the degree-5 cap (3''') with the degree-4 cap (3''). Repair
   2.10 or fold it into 2.22, name the degree-4 cap 3'' and the degree-5 cap 3'''
   consistently, rewrite 2.22 in the section-2 template and LaTeX (it is ASCII
   and omits Proof location and Regime of validity), and propagate "closed at d
   <= 4, open at d >= 5" to 2.18, 2.19, sections 4-6, all_degrees.md,
   proof_complexity.md, and theorem_map.md.

4. **The false Lemma TB still grounds a headline result outside inv3.**
   cls_cnt.md's own correction block (lines 124-134) says Lemma TB is false as
   stated, but section 3.3 (lines 194-200) still concludes "Lemma TB applies with
   t = 2 and gives ... [PROVED]" for the Q-A dimension identity, and that is the
   anchor CR-2.16 and current_results 2.16 cite. current_results 2.16 carries the
   engine caveat, but the source derivation was not re-based. Apply the same
   repair as inv3 section 7: state Q-A through the repaired completion engine
   (degree-capped Buchberger with machine-enforced span neutrality), not Lemma
   TB.

5. **The newest wave has no independent regeneration coverage.**
   regeneration_2026-10-04.md re-runs the earlier scripts, and current_results.md
   line 16 says "Every number matches regeneration_2026-10-04.md or the cited
   source document." None of the six newest scripts (chi_cls_cnt_check.py,
   chi_deg5_check.py, chi_mixture3.py, chi_mixture4.py, chi_inv3_check.py,
   chi_engine_adversarial.py) appears in the regeneration table, so the newest
   numbers rest only on the agents' own runs. Run one regeneration pass over the
   newest wave, or narrow line 16 to the covered set.

6. **theorem_map.md and all_degrees.md did not receive the newest wave.**
   theorem_map diagram 3 still lists GAP D (de-modularize the JDP steps) as open
   though ADDENDUM 8 closed it, still prints GAP E's superseded constants (cap
   ~0.32 vs witness 0.06; now 0.1864 and 0.1264), and still says "MIXTURE-d OPEN
   at d >= 4" (lines 105, 174). all_degrees.md section 5.2 item 2 (and lines 67,
   489) still says the mixture class "is covered only at d = 2". Run
   propagate-changes or an equivalent sweep.

7. **The external reading-check is still unsent, and it is still the
   highest-value action.** Every result rests on a reading of Krajicek's
   Definition 3.1 and 4.3 and the p = 2 restriction that no expert has confirmed.
   note_to_author.md is a question draft; sending or explicitly parking it is the
   owner's call, and no amount of algebra removes the dependency.

8. **The program still has no finite endpoint, and two GOAL rules still
   contradict the record.** The 11x10 memory wall was bypassed by Lemma Q, so the
   adopted "if 11x10 is memory-walled, write it up and stop" rule cannot fire;
   the certification wall replaced it. GOAL section 1 still says no new rectangle
   is attempted before the engine passes the adversarial gate, but the gate
   FAILed and d = 5 was run and committed. Name the single result that justifies
   continuing past d = 5, and the condition under which the study is written up
   as a bounded result (the certified low-degree facts, the 4-hole exotic, the
   false Lemma TB, the uncertified engine, and the closed MIXTURE/CLS/CNT scope
   repairs), then stop.

9. **Hygiene, cheap and still open.** README is a 2026-10-03 portrait: it never
   names current_results.md, its artifact guide lists superseded files, it counts
   "nine" corrections (nineteen now), and its session-outcome list numbers 1, 2,
   3, 2, 3, 4. GOAL section 9's O2 status still says MIXTURE-d is covered only at
   d = 2, and its INV status still says "an adversarial engine-validation agent
   is dispatched" (it ran and FAILed). inv3.md has two consecutive "### 7.6"
   headings. The duplicated names (Theorem B, Theorem R, Theorem 3'', Theorem
   3''', Lemma CNT) are still disambiguated only by citation, and problem 3 shows
   the collision now costs two wrong labels (current_results 2.22 and mixture4.md
   line 73).

## What to do next, in priority order

1. Process the guidance before producing anything new. Record adopt/reject for
   the third, fourth, and fifth reviews (and this one) in LOG.md, then do ONE
   consolidation turn instead of another result wave.
2. Land or drop the in-flight work. Commit chi_mixture4.py (its run is already
   quoted as registered), and fix or drop chi_inv3_certify.py's verdict contract
   and coverage table so it can certify by an argument it actually implements.
3. Repair the statement of record in one place (problem 3), then re-base inv3.md
   section 7 and cls_cnt.md section 3.3 on the completion criterion rather than
   Lemma TB (problems 1 and 4).
4. Run one independent regeneration pass over the newest wave (problem 5).
5. Make the gate mechanical (tracked run scripts; gate-verdict token) and add
   regeneration coverage as a passing condition (problem 2).
6. Propagate to theorem_map.md and all_degrees.md (problem 6).
7. Replace the moot stop rule with the decision point of problem 8, and
   reconcile GOAL section 1 with the d = 5 record and GOAL section 9 with the
   current status.
8. Send or explicitly park the reading-check note, and record the decision
   either way (problem 7).
9. Do the cheap hygiene (problem 9).

## Bottom line

The finding this pass is the stall, now compounded: nothing has landed since the
fifth review, the last three reviews were never processed, and the in-flight
certification scan cannot certify in either coded mode, let alone by the false
Lemma TB. The recurring failure (a computational artifact promoted before
verification) now sits in that scan, in the registry, and in a second source
derivation (cls_cnt.md's Q-A), while the one current statement has spread the
MIXTURE-d status across three answers and declares itself consistent. Land the
clean mixture4 script, repair the statement of record in one place, and do not
extend an uncertified engine before d = 5 becomes another d = 4. The work is
worth continuing only as a bounded study with a declared endpoint, and only once
the reading is confirmed.
