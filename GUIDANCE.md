# Guidance on the P vs NP corpus

Rewritten 2026-10-05 (eighth review). Reviewed: the git state, the artifacts the
seventh review covered (current_results.md, open_problems.md, inv3.md,
cls_cnt.md, theorem_map.md, all_degrees.md, mixture4.md, proved_registry.py,
corpus_lint.py and a live lint run, the two untracked scripts, README, GOAL),
plus the meta files (bibliography.md, instruction_log.md, the monitors) and a
fresh cross-file numeric/status sweep. Findings new to this pass are marked NEW.
The seventh review's unresolved items all stand; nothing was addressed.

## State of play since the seventh review

- Nothing landed. HEAD is d139eed, the seventh review, a GUIDANCE-only commit.
  The working tree still carries the same two untracked scripts,
  chi_inv3_certify.py (mtime 03:45) and chi_mixture4.py (mtime 00:22), both
  unchanged since the fourth review. No /tmp/opencode certification artifacts.
- The guidance queue is now six reviews deep (third through eighth). LOG.md has
  adopt/reject entries for the first and second reviews only, though GOAL
  section 9 makes that record mandatory. The 4-hour review cadence has outrun
  the work cadence: the interval produced no artifact.
- The substantive picture is unchanged: O2's cap is assembled at degrees 2
  through 5 with the same $d^2 \sim n$ boundary, MIXTURE-d is closed at $d \le 4$
  (mixture4.md), the $d = 5$ closure is engine output and uncertified, and the
  single mathematical gap is INV(d) at $t \ge 3$.

## What is genuinely good

- The correction culture still works, and mixture4.md's own registered assert
  caught a coin-keying non-conformance before any number was trusted.
- current_results.md remains the right idea: one current statement with
  PROVED/MEASURED/INFERRED labels, enforced by proved_registry.py and
  corpus_lint.py checks 8-9.
- The adversarial gate and the inv3.md downgrade block are the right structural
  response to the recurring promotion-before-verification failure. They work at
  the position of record.

## Problems, most important first

1. **The guidance queue is the first problem, and it is now six deep.**
   Process the queue before producing anything new, record adopt/reject for the
   third through eighth reviews in LOG.md, then do ONE consolidation turn
   instead of another result wave.

2. **The in-flight certification scan still cannot return CERTIFIED in either
   coded mode.**
   - Sharded mode: JOB_PLAN samples six classes ((AD3, b), (AD3, C), (AD3, H),
     (AD3, ST), (AD2, AD3), (AD3, AD3)); do_collect treats only AD3xAD3 as
     sampled, so the coverage check fails on the other five and the verdict is
     INCONCLUSIVE. The docstring's "Exit code: 0 CERTIFIED (on the stated
     coverage)" is unreachable.
   - Single-process mode: the default 3000 s guard cannot cover the (AD3, AD3)
     class, so the scan is marked incomplete and the verdict is again
     INCONCLUSIVE.
   - inv3.md's body still asserts PROVED over the downgraded claim: section 0
     line 53, section 1, the section 3.2-3.3 and 7 tables, and section 7's
     intro, while the top DOWNGRADE block and section 7.6 relabel the same claim
     engine output. Lint check 9 passes these because it never reads the
     top-of-file downgrade. NEW: the file also has two consecutive "### 7.6"
     headings (lines 675, 690).
   - Fix the contract to match the argument the scan implements: if the engine
     closes over all lcm $\le t$ pairs and an EXHAUSTIVE hidden-pair scan of the
     final $G^*$ finds every in-cap residue in $W_3$, then $I \cap S_{\le 3} =
     W_3$, with no appeal to Lemma TB. Either make the scan exhaustive (never
     CERTIFIED on partial coverage) or state the verdict as SAMPLED and leave
     $d = 5$ as engine output. Relabel the inv3 body, and add a check: a file
     whose top block carries a DOWNGRADE must not assert PROVED for that claim
     in its body.

3. **The statement of record is still split and stale.**
   - open_problems.md (a deliverable of record) never received the newest wave
     and contradicts current_results.md on six points: the O2 open core says
     "Degree $\ge 3$ trees: no cap of any kind" (lines 122-126); the displayed
     cap uses the invalid printed term $2(1 - \exp(-d^2 \log k/(4n)))$ (line
     113); the thresholds are the superseded 0.317/0.35 (lines 142-143, 457);
     O5 is headed OPEN with the general-$d$ writeup "missing" (lines 268,
     297-298); the O2 open core (i) says the degree-3 kernel is classified
     "only in count" (lines 123-126); and the ledger says "eight corrections"
     (lines 53-61).
   - MIXTURE-d is stated three ways. The live answer is closed at $d \le 4$,
     open at $d \ge 5$ (current_results 2.22, mixture4.md). Stale "closed at
     $d \le 3$" loci: current_results 2.8 lines 351-352 (NEW instance), 2.18
     line 749, section 4 item (ii) line 1037, section 5 line 1105, section 6
     line 1133; mixture3.md lines 508-509; proof_complexity.md ADDENDUM 12 line
     1186; theorem_map.md lines 105, 131, 174-175; GOAL.md lines 237-238,
     241-244. Stale "covered only at $d = 2$" loci: all_degrees.md lines 67,
     489. Section 6 still declares "No live inconsistency between sources was
     found" (line 1130).
   - The degree-4 cap is mislabeled twice: mixture4.md lines 72-73 names the
     repaired cap "Theorem 3'''" while citing deg4_theory.md Theorem 3'', and
     current_results.md 2.22's title repeats "Theorem 3'''". Degree 4 is 3'';
     degree 5 is 3'''.
   - NEW: all_degrees.md line 57 says "INV(d) for $d \ge 3$ is OPEN at general
     $d$", but current_results 2.21 closes INV(3) (the $t = 3$ layer is a
     tautology and step (6a) is closed by the $(6,3)$ sweep); INV(d) is open
     only for $d \ge 4$.
   - NEW: lemma_m.md section 3.3 still labels Lemma CLS "OPEN in general" and
     Lemma CNT "OPEN", while current_results 2.16 and 2.17 label both closed in
     regime.
   - Fix: repair the statement in one place, name the caps consistently,
     propagate "closed at $d \le 4$, open at $d \ge 5$", and fold
     open_problems.md into current_results.md or sweep it with
     propagate-changes.

4. **The false Lemma TB still grounds cls_cnt.md's Q-A in the body.**
   cls_cnt.md's section 3.2 correction block says Lemma TB is false as stated,
   but section 3.3 (lines 194-200) still concludes "Lemma TB applies with $t = 2$
   and gives ... [PROVED]". proved_registry.py anchors CR-2.16 to the section-3
   header. Re-base Q-A on the repaired completion engine, as inv3.md section 7
   already does.

5. **The PROVED gate is still not mechanical, and nothing ties a registered run
   to a tracked script.**
   chi_mixture4.py, the registered script behind PROVED claim CR-2.22, is
   untracked, and the registry anchors CR-2.22 to the prose "Repaired cap
   (Theorem M4-D)" rather than a run. corpus_lint.py check 2 resolves references
   via CORPUS.rglob, so the untracked script passes on this disk but would fail
   in a fresh clone; check 6 flags only orphan scripts, never a missing
   referenced one. Extend the gate: (a) every registered-run script must be
   tracked by git (git ls-files); (b) every engine-derived PROVED label must
   carry a CERTIFIED or UNCERTIFIED token; (c) add both to GOAL section 4's
   passing state.

6. **The newest wave still has no independent regeneration coverage.**
   regeneration_2026-10-04.md re-runs none of the six newest scripts
   (chi_cls_cnt_check.py, chi_deg5_check.py, chi_mixture3.py, chi_mixture4.py,
   chi_inv3_check.py, chi_engine_adversarial.py), yet current_results.md line 16
   says every number matches that file or the cited source. Run one regeneration
   pass over the newest wave, or narrow line 16 to the covered set.

7. **The external reading-check is still unsent.**
   Every result rests on a reading of Krajicek's Definition 3.1 and 4.3 and the
   $p = 2$ restriction that no expert has confirmed. note_to_author.md is a
   question draft; sending or explicitly parking it is the owner's call, and no
   amount of algebra removes the dependency.

8. **The program still has no finite endpoint, and two GOAL rules contradict the
   record.**
   The 11x10 memory wall was bypassed by Lemma Q, so the adopted "if 11x10 is
   memory-walled, write it up and stop" rule cannot fire; the certification wall
   replaced it. GOAL section 1 still says no new rectangle is attempted before
   the engine passes the adversarial gate, but the gate FAILed and $d = 5$ was
   run and committed. Name the single result that justifies continuing past
   $d = 5$ and the condition under which the study is written up as a bounded
   result (the certified low-degree facts, the 4-hole exotic, the false Lemma
   TB, the uncertified engine, the closed MIXTURE/CLS/CNT scope repairs), then
   stop.

9. **Hygiene, cheap and still open.**
   - README is a 2026-10-03 portrait: it never names current_results.md, its
     artifact guide lists superseded files, it counts "Nine" errors (line 105)
     and "eight corrections" (line 113), and its session-outcome list numbers
     1, 2, 3, 2, 3, 4. NEW: proof_complexity.md line 924 still says "after eight
     corrections".
   - GOAL section 3's ledger says "nine correction-class events" (nineteen plus
     one now); section 9's O2 status says MIXTURE-d is covered only at $d = 2$;
     its INV status still says an adversarial engine-validation agent is
     dispatched (it ran and FAILed); and NEW, line 150 still says
     "(docs/cls_cnt.md when it lands)".
   - NEW: bibliography.md line 33 says "proof_complexity.md (+ ADDENDA 1-4)"
     (it runs to ADDENDUM 13) and line 35 says "deg3_theory.md (pending agent)"
     (it landed).
   - NEW: theorem_map.md lines 7 and 110 still name the superseded
     chi_transfer.md Theorem 4 as the route of record; chi_transfer.md itself
     says to use err_form_route.md Theorem R.
   - theorem_map.md diagram 3 still lists GAP D as open though ADDENDUM 8 closed
     it, still prints GAP E's superseded constants (cap ~0.32 against 0.1864,
     witness 0.06 against 0.1264), and still says "MIXTURE-d OPEN at $d \ge 4$"
     (lines 99, 100, 105, 174).
   - NEW: all_degrees.md lines 549-551 say proof_complexity.md "ends at ADDENDUM
     10"; it now runs to ADDENDUM 13.
   - NEW: mixture4.md lines 47-48 say the killed-branch check covered "2.49M
     (config, rho) pairs at (10,4) alone"; the (10,4) count is 2,434,860, and
     2.49M is the two-point total with the 51,000 at (9,4) (line 326).
   - NEW: instruction_log.md omits two owner instructions that LOG.md records
     (lines 1647 and 1689: continue research rather than wait on typesetting;
     do more parallel work), though GOAL section 8 requires a complete verbatim
     history.
   - The duplicated names (Theorem B, Theorem R, Theorem 3'', Theorem 3''',
     Lemma CNT) are disambiguated only by citation, and problem 3 shows the
     collision now costs a wrong cap label.

## What to do next, in priority order

1. Process the guidance queue (third through eighth) and record adopt/reject in
   LOG.md, then do ONE consolidation turn instead of another result wave.
2. Repair the statement of record: fix MIXTURE-d in one form, fold
   open_problems.md into current_results.md (or sweep it), correct the cap
   labels, and propagate to all_degrees.md, theorem_map.md, and GOAL.md.
3. Land or drop the in-flight work: commit chi_mixture4.py, and fix or drop
   chi_inv3_certify.py's verdict contract so it can certify only by an argument
   it implements.
4. Re-base cls_cnt.md section 3.3 on the completion criterion and relabel the
   inv3.md body.
5. Make the gate mechanical (tracked run scripts, gate-verdict token,
   regeneration coverage), and run one regeneration pass over the newest wave.
6. Send or explicitly park the reading-check note, then name the endpoint and
   write up the bounded result.
7. Do the cheap hygiene of problem 9.

## Bottom line

The eighth review finds no work landed in the interval, so the queue is now six
reviews deep and the same defects persist: the certification scan still cannot
certify, open_problems.md still trails current_results.md, the MIXTURE-d status
is still spread across three answers while section 6 declares consistency, the
false Lemma TB still grounds the cls_cnt Q-A in the body, and the gate is still
not mechanical. This pass adds a cluster of smaller drift on top (the superseded
route reference in theorem_map.md, the INV(3) status conflict in all_degrees.md,
the stale lemma_m CLS/CNT status, and stale pointers in GOAL, bibliography, and
instruction_log). Land the clean mixture4 script, repair the statement of record
in one place, pull open_problems.md back, and stop extending an uncertified
engine. The work is worth continuing only as a bounded study with a declared
endpoint, and only once the reading is confirmed.
