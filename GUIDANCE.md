# Guidance on the P vs NP corpus

Rewritten 2026-10-05 (seventh review). Reviewed: layout, README, GOAL, the LOG
tail, current_results.md (section 1 header, entries 2.8-2.10 and 2.16-2.22,
sections 3-6), theorem_map.md, all_degrees.md (sections 0 and 5), inv3.md (the
downgrade block and sections 1, 3, 7), cls_cnt.md (section 3), mixture4.md,
open_problems.md (in full), regeneration_2026-10-04.md, proved_registry.py,
corpus_lint.py (checks 1/2/6/8/9 plus a live run), the two untracked scripts,
note_to_author.md, and git history. References to "GUIDANCE priority N"
elsewhere point at the second review unless stated.

## State of play since the sixth review

- Nothing has landed. HEAD is still the sixth review (f6cc52a, a GUIDANCE-only
  commit). The working tree carries only the same two untracked scripts every
  review since the fourth has seen (chi_inv3_certify.py, mtime 03:45;
  chi_mixture4.py, mtime 00:22), both older than the 04:03 fourth-review commit.
  No /tmp/opencode certification or mixture artifacts exist.
- The guidance loop is now five reviews deep. LOG.md has adopt/reject entries
  for the first and second reviews and none for the third, fourth, fifth, or
  sixth. GOAL section 9 requires that decision. Instead the newest wave (MIXTURE-4,
  the d=5 closure, the certification scan) kept landing, and its consolidation
  skipped exactly the passages the reviews named.
- Every sixth-review priority is still open. This pass adds one new finding of
  substance (open_problems.md, a deliverable of record, never received the wave
  and now contradicts current_results.md on six points), sharpens the inv3
  relabeling gap, and shows the lint gate is blind to both.

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
- The adversarial gate (chi_engine_adversarial.py) and the downgrade block at
  the top of inv3.md are the structural response to the recurring
  promotion-before-verification failure, and they are working at the position of
  record. The current statement now carries the engine caveat explicitly (for
  example 2.16).

## Problems, most important first

1. **The guidance queue is the first problem, and it is now five reviews deep.**
   Nothing has been adopted or rejected since the second review. GOAL section 9
   makes the adopt/reject record mandatory; LOG.md's tail ends at the mixture4
   agent, with no third-, fourth-, fifth-, or sixth-review processing entry.
   Process the queue before producing anything new, then make ONE consolidation
   turn instead of another result wave.

2. **The in-flight certification scan cannot return CERTIFIED in either coded
   mode.** Re-verified this pass:
   - Sharded mode. JOB_PLAN samples six classes: (AD3, b), (AD3, C), (AD3, H),
     (AD3, ST), (AD2, AD3), and (AD3, AD3). do_collect treats only AD3xAD3 as
     sampled (line 900), so the coverage check fails on the other five and the
     verdict is INCONCLUSIVE. The docstring's "Exit code: 0 CERTIFIED (on the
     stated coverage)" cannot be reached.
   - Single-process mode. The default 3000 s guard cannot cover the (AD3, AD3)
     class (12-40 h alone), so the scan is marked incomplete and the verdict is
     again INCONCLUSIVE.
   - inv3.md still frames the result through Lemma TB (section 3.1: "Lemma TB
     applies verbatim to G*", section 7.4: "INV(3)(i) ... PROVED at d = 5 [MV]"),
     though that lemma is false as stated.
   Fix the contract to match the argument the scan actually implements: if the
   engine closes over all lcm <= t pairs and an EXHAUSTIVE hidden-pair scan of
   the final G* finds every in-cap residue in W_3, then G* is a truncated
   Groebner basis and I cap S_{<=3} = W_3, with no appeal to Lemma TB. Either
   make the scan exhaustive (no sampling, and a verdict that is never CERTIFIED
   on partial coverage), or state the verdict as SAMPLED and leave d = 5 as
   engine output. Note where the sampling lands: the (AD3, AD3) pairs carry
   73-94 term bodies and are exactly the ones the engine cannot see. Even a
   full 11x10 scan certifies one rectangle and one t layer; the per-rung
   trajectory stays open-ended.

3. **open_problems.md, a deliverable of record (GOAL section 4), never received
   the newest wave and now contradicts current_results.md.** Checkable items:
   - O2's open core says "Degree >= 3 trees: no cap of any kind" (lines 122-126),
     but current_results sections 2.9, 2.10, 2.20 and section 4 give caps at
     degrees 3, 4, 5, and degree 2 holds at general d in regime (2.18).
   - O2's displayed cap (line 113) uses the printed certificate term
     $2(1 - \exp(-d^2 \log k/(4n)))$, which ADDENDUM 9 and current_results
     2.8/2.11 declare invalid as a cap term; the valid form is
     $\chi + (1-\chi)(q+A)$.
   - O2's falsification thresholds (line 142: cap band 0.317; lines 143 and 457:
     above 0.35) are superseded by the sharpened cap 0.1864 and Conjecture E5's
     0.135 (current_results 2.13 and section 5).
   - O5 is still headed OPEN with the general-d writeup "missing" (lines 268,
     297-298), but current_results 2.16/2.17 and GOAL record CLS/CNT closed in
     regime.
   - O7 (lines 123-126) still says the degree-3 kernel is classified "only in
     count", but deg3_theory.md classified all 13,244 degree-3 columns in ten
     classes (current_results 2.1).
   - The correction ledger says "eight corrections" (lines 53-61); the standing
     ledger is nineteen correction-class events plus one quantifier repair
     (GOAL section 3).
   Run propagate-changes (or an equivalent sweep) over open_problems.md, or fold
   it into current_results.md and mark it provenance.

4. **The MIXTURE-d statement is still split, and the flagship entry is the stale
   one.** The live answers are:
   - d = 2: all_degrees.md lines 65-67 and 486-489 ("covered only at d = 2").
   - d <= 3: current_results.md 2.18 (line 749), 2.19 (title line 771 and line
     799), section 4 item (ii) (line 1037), section 5 (line 1105), section 6
     (line 1133); mixture3.md lines 508-509; proof_complexity.md ADDENDUM 12
     (line 1186); theorem_map.md (lines 105, 131, 174-175); GOAL.md lines 237-238
     and 241-244.
   - d <= 4: current_results.md 2.22 (lines 926, 953); mixture4.md.
   Worse, current_results.md section 6 says "No live inconsistency between
   sources was found" and states the resolved form as "closed at d <= 3" (line
   1133), contradicting the file's own 2.22. And the degree-4 cap is mislabeled
   in two places: mixture4.md lines 72-74 names the repaired cap "Theorem 3'''"
   while citing "deg4_theory.md Theorem 3''", and current_results.md 2.22's
   title repeats "Theorem 3'''". The degree-4 cap is 3'' (deg4_theory.md section
   6); 3''' is degree 5 (deg5_theory.md section 6.1). Repair the statement of
   record in one place, name the caps consistently, and propagate "closed at
   d <= 4, open at d >= 5" to every source above.

5. **The false Lemma TB still grounds cls_cnt.md's Q-A in the body, and inv3.md's
   body still asserts PROVED over the downgraded result.** Two halves:
   - cls_cnt.md's correction block (lines 124-134) says Lemma TB is false as
     stated, but section 3.3 (lines 194-200) still concludes "Lemma TB applies
     with t = 2 and gives ... [PROVED]" for the Q-A dimension identity, and
     proved_registry.py anchors CR-2.16 to the section-3 header. current_results
     2.16 carries the engine caveat, but the source derivation was not re-based.
     Apply the same repair as inv3 section 7: state Q-A through the repaired
     completion engine (degree-capped Buchberger with machine-enforced span
     neutrality), not Lemma TB.
   - inv3.md's top DOWNGRADE block and section 7.6 relabel the d=4/d=5 closure
     as engine output, but the body still reads "PROVED [MV]" in section 1 (line
     53), section 3.1 (line 307), the section 3.2-3.3 and 7 tables (lines
     318-336, 664), section 3.3's verdict (line 358), and section 7's intro
     (line 542). Lint check 9 passes these because each section contains
     proof-kind vocabulary and the lint never reads the top-of-file downgrade.
     Apply the relabel in the body, and add a check: a file whose top block
     carries a DOWNGRADE must not assert PROVED for that claim in its body.

6. **The PROVED gate is still not mechanical, and nothing ties a registered run
   to a tracked script.** chi_mixture4.py, the registered script behind PROVED
   claim CR-2.22, is untracked, and the registry anchors CR-2.22 to the prose
   substring "Repaired cap (Theorem M4-D)" in mixture4.md rather than to a run.
   corpus_lint.py check 2 builds its file index from CORPUS.rglob, so the
   untracked script resolves on this disk while a fresh clone would fail (mixture4.md
   backticks reference it at lines 19 and 495); check 6 flags only orphan
   scripts, never a missing referenced one. The live lint run prints CLEAN 862,
   which is exactly the blind spot. Extend the gate: (a) every script named as a
   registered run in a PROVED entry must be tracked by git (git ls-files, not
   rglob); (b) an engine-derived PROVED label must carry a gate-verdict token
   (CERTIFIED or UNCERTIFIED); (c) add both requirements to GOAL section 4's
   passing state.

7. **The newest wave still has no independent regeneration coverage.**
   regeneration_2026-10-04.md re-runs only the earlier scripts, and it names
   none of the six newest (chi_cls_cnt_check.py, chi_deg5_check.py,
   chi_mixture3.py, chi_mixture4.py, chi_inv3_check.py,
   chi_engine_adversarial.py); a grep confirms zero mentions of each.
   current_results.md line 16 nevertheless says "Every number matches
   regeneration_2026-10-04.md or the cited source document." Run one
   regeneration pass over the newest wave, or narrow line 16 to the covered set.

8. **The external reading-check is still unsent, and it is still the
   highest-value action.** Every result rests on a reading of Krajicek's
   Definition 3.1 and 4.3 and the p = 2 restriction that no expert has
   confirmed. note_to_author.md is a question draft; sending or explicitly
   parking it is the owner's call, and no amount of algebra removes the
   dependency.

9. **The program still has no finite endpoint, and two GOAL rules still
   contradict the record.** The 11x10 memory wall was bypassed by Lemma Q, so the
   adopted "if 11x10 is memory-walled, write it up and stop" rule cannot fire;
   the certification wall replaced it. GOAL section 1 still says no new rectangle
   is attempted before the engine passes the adversarial gate, but the gate
   FAILed and d = 5 was run and committed. Name the single result that justifies
   continuing past d = 5, and the condition under which the study is written up
   as a bounded result (the certified low-degree facts, the 4-hole exotic, the
   false Lemma TB, the uncertified engine, and the closed MIXTURE/CLS/CNT scope
   repairs), then stop.

10. **Hygiene, cheap and still open.** README is a 2026-10-03 portrait: it never
    names current_results.md, its artifact guide lists superseded files, it
    counts "Nine" corrections (line 105; nineteen now), and its session-outcome
    list numbers 1, 2, 3, 2, 3, 4. GOAL section 3's ledger still says "nine
    correction-class events", GOAL section 9's O2 status still says MIXTURE-d is
    covered only at d = 2, and its INV status still says "an
    adversarial engine-validation agent is dispatched" (it ran and FAILed).
    theorem_map.md diagram 3 still lists GAP D (de-modularize the JDP steps) as
    open though ADDENDUM 8 closed it, still prints GAP E's superseded constants
    (cap ~0.32 vs witness 0.06; now 0.1864 and 0.1264), and still says
    "MIXTURE-d OPEN at d >= 4" (lines 105, 174). inv3.md has two consecutive
    "### 7.6" headings. The duplicated names (Theorem B, Theorem R, Theorem 3'',
    Theorem 3''', Lemma CNT) are still disambiguated only by citation, and
    problem 4 shows the collision now costs two wrong labels.

## What to do next, in priority order

1. Process the guidance before producing anything new. Record adopt/reject for
   the third, fourth, fifth, and sixth reviews (and this one) in LOG.md, then do
   ONE consolidation turn instead of another result wave.
2. Land or drop the in-flight work. Commit chi_mixture4.py (its run is already
   quoted as registered), and fix or drop chi_inv3_certify.py's verdict contract
   and coverage table so it can certify by an argument it actually implements.
3. Repair the statement of record in one place (problem 4), fold open_problems.md
   into the current wave (problem 3), then re-base cls_cnt.md section 3.3 and
   inv3.md section 7 on the completion criterion rather than Lemma TB (problem 5).
4. Run one independent regeneration pass over the newest wave (problem 7).
5. Make the gate mechanical: tracked run scripts, gate-verdict token, and
   regeneration coverage as passing conditions (problem 6).
6. Propagate to theorem_map.md and all_degrees.md, and relabel the inv3.md body
   (problems 5 and 10).
7. Replace the moot stop rule with the decision point of problem 9, and reconcile
   GOAL section 1 with the d = 5 record and GOAL section 9 with the current
   status.
8. Send or explicitly park the reading-check note, and record the decision either
   way (problem 8).
9. Do the cheap hygiene (problem 10).

## Bottom line

The finding this pass is that the stall is now compounded into a drift of record:
the guidance queue is five reviews deep, the in-flight certification scan still
cannot certify in either coded mode, and a deliverable of record (open_problems.md)
has fallen six contradictions behind current_results.md while the lint prints
CLEAN. The recurring failure (a computational artifact promoted before
verification) still sits in the certification scan, in the registry, and in a
second source derivation (cls_cnt.md's Q-A), while the one current statement
spreads the MIXTURE-d status across three answers and declares itself consistent.
Land the clean mixture4 script, repair the statement of record in one place and
pull open_problems.md back, and do not extend an uncertified engine before d = 5
becomes another d = 4. The work is worth continuing only as a bounded study with
a declared endpoint, and only once the reading is confirmed.
