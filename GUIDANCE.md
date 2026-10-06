# Guidance on the P vs NP corpus

Rewritten 2026-10-06 (tenth review). Reviewed: the git history and log, and
every artifact the ninth review covered (current_results.md, open_problems.md,
inv3.md, cls_cnt.md, theorem_map.md and its .mmd source, all_degrees.md,
lemma_m.md, mixture4.md, proved_registry.py, corpus_lint.py plus a fresh run,
the two untracked scripts, README, GOAL, bibliography.md, instruction_log.md,
paper/CHANGES.md, the monitoring screens, regeneration_2026-10-04.md), with a
fresh cross-file status sweep and a check of /tmp/opencode for in-flight
artifacts. NOTHING the third through ninth reviews flagged has been addressed.
NEW marks findings new to this pass.

## State of play

- No work has landed. The last substantive commit is c0a669c (mixture4,
  2026-10-05 00:42); every commit since is GUIDANCE (the fourth through ninth
  reviews, plus one trim), seven commits spanning about 27 hours. The only
  working-tree changes are the same two untracked scripts, chi_inv3_certify.py
  (mtime 2026-10-05 03:45) and chi_mixture4.py (mtime 2026-10-05 00:22).
- The guidance queue is eight reviews deep (third through tenth). LOG.md's only
  adopt/reject entries are for the first and second reviews (the second at LOG
  line 2062); GOAL section 9 makes the record mandatory. The substantive picture
  is unchanged: O2's cap is assembled at degrees 2 through 5 with the same
  d^2 ~ n boundary, MIXTURE-d is closed at d <= 4 in the newest entry but d <= 3
  everywhere else, the d = 5 closure is engine output and uncertified, and the
  single mathematical gap is INV(d) at t >= 3.
- corpus_lint.py reports CLEAN (862 items, 0 FAIL) while the statement of record
  contradicts itself. A PASS means the needle strings matched, not that the
  corpus agrees with itself, and check 8 now enshrines a wrong label. Do not read
  it as a status certificate.
- NEW: the daily monitoring obligation has slipped. The last screen is
  monitor_2026-10-05.md; the material 6-Oct wave posts about Tue 00:00 UTC and no
  2026-10-06 deliverable exists (GOAL section 5). The 10-05 screen itself says
  the next screen is the material one.

## What is genuinely good

- The correction culture works (mixture4.md's own registered assert caught a
  coin-keying non-conformance before any number was trusted), and the adversarial
  gate genuinely attacks the engine rather than trusting it.
- current_results.md remains the right idea: one statement with
  PROVED/MEASURED/INFERRED labels, enforced by proved_registry.py and
  corpus_lint.py checks 8-9. Its problem is maintenance, not conception.
- The 11x10 quotient construction (Lemma Q) is a real engineering result: a
  0.63 GB quotient echelon replaced an infeasible ~5.1 GB dense one and
  reproduced the closure at two configurations.

## Problems, most important first

1. **The review mechanism is now the problem, and it is directly harmful.**
   The ninth review's own rule was: if a later pass finds no landed artifact,
   stop writing reviews until one lands. This is that pass, and no artifact
   landed. Seven consecutive GUIDANCE-only commits now give the appearance of
   activity while the corpus stands still. Do not produce an eleventh review.
   The owner should pick a direction (land, drop, or park) rather than commission
   another pass. The actionable content below is unchanged from the ninth review
   and will not move until a human decides.

2. **The statement of record contradicts itself on MIXTURE-d, in three ways.**
   (a) The newest entry, current_results.md 2.22 (and mixture4.md), closes
   MIXTURE-d at d <= 4, open at d >= 5. Sections 2.8 (line 351), 2.18 (line
   749), 4(ii) (line 1037), 5 (line 1105), and 6 (line 1133) still close it at
   d <= 3, and section 6's "No live inconsistency between sources was found"
   (line 1130) is false as written.
   (b) Section 2.10 (Theorem 3'', the degree-4 cap) still states q4* as the
   degree-4 cap, while 2.22 says that exact cap is false at finite n and repairs
   it to q4^mix = (2d^2 + d)/c. The two are not cross-referenced, so the "one
   current statement" holds two different degree-4 caps.
   (c) The degree-4/5 label collision is machine-enshrined on both sides.
   mixture4.md (lines 72-73 and section 7) calls the repaired degree-4 cap
   "Theorem 3'''" while citing deg4_theory.md Theorem 3''; current_results 2.22's
   title repeats it; proved_registry.py carries CR-2.10 anchored to
   "Theorem 3'' ... the q_4* cap" and CR-2.22 anchored to "Theorem 3''' cap
   constant repaired", so check 8 passes while asserting the collision.
   Fix: state MIXTURE-d once as "closed at d <= 4, open at d >= 5", forward the
   M3-D and 2.10 entries to 2.22, relabel the degree-4 repair to 3'', and
   propagate to all_degrees.md (57, 65, 486), mixture3.md, theorem_map.md
   (26, 99-105, 174), proof_complexity.md ADDENDUM 12, GOAL sections 6 and 9, and
   registry CR-2.10/CR-2.22.

3. **The certification scan still cannot return CERTIFIED in either coded mode,
   and no run exists.**
   - Sharded: JOB_PLAN samples six classes, but do_collect hard-codes
     `sampled = cls_s == "AD3xAD3"` (chi_inv3_certify.py line 900). The other
     five sampled classes fail the exhaustive coverage check, so the verdict is
     INCONCLUSIVE and the docstring's "Exit code: 0 CERTIFIED (on the stated
     coverage)" (line 89) is unreachable.
   - Single-process: CERTIFIED needs full coverage of about 217,470 (AD3,AD3)
     pairs (line 1202) at the docstring's own ~0.1-0.7 s/pair, so the default
     3000 s guard leaves complete False. INCONCLUSIVE again.
   - /tmp/opencode (CERTDIR) holds no certification artifacts, and none appeared
     in the ~27 hours since dispatch (session
     ses_ef6a1f5e5ffeg8LkDCHqqEFJCP).
   Fix: derive `sampled` from job_plan()'s mode field, or state the verdict as
   SAMPLED. Then land a run or drop the tool and leave d = 5 as engine output.

4. **inv3.md's body still asserts PROVED over the downgraded claim.**
   Section 0 line 53, section 1, the 3.2-3.3 and 7.5 tables, and section 7's
   intro assert PROVED, while the top DOWNGRADE block (lines 5-33) and section
   7.6 relabel the same claim engine output. Lint check 9 passes these because
   it never reads the top-of-file downgrade. The file also has two consecutive
   "### 7.6" headings (lines 675, 690). Relabel the body, merge the duplicate,
   and add a check: a file whose top block carries a DOWNGRADE must not assert
   PROVED for that claim in its body.

5. **The PROVED gate is not mechanical, and the counts it would police are
   wrong.**
   - Both registered-run scripts are untracked: chi_mixture4.py (behind CR-2.22)
     and chi_inv3_certify.py. Check 2 resolves references via CORPUS.rglob, so
     they pass on this disk but would fail in a fresh clone; check 6 flags only
     orphan scripts, never a missing referenced one. Require every registered-run
     script to be tracked (git ls-files) and every engine-derived PROVED label to
     carry a CERTIFIED or UNCERTIFIED token.
   - The corpus cannot state how many corrections it has made; the counts span
     eight to nineteen. open_problems.md (lines 53-61) says "eight"; README says
     "Nine" (line 105) and "eight corrections" (line 113); GOAL section 3 line 65
     says "nine"; proof_complexity.md line 924 says "eight" while its ADDENDUM 13
     calls cls_cnt "the SEVENTEENTH"; LOG.md calls mixture4 "the NINETEENTH".
     Derive one ledger from LOG/ADDENDA and cite it everywhere.
   - cls_cnt.md section 3.3 still concludes "Lemma TB applies with t = 2 and
     gives ... [PROVED]" (lines 194-200) although its 3.2 correction block says
     Lemma TB is false as stated, and CR-2.16 anchors to that header. Re-base
     Q-A on the repaired completion engine, as inv3.md section 7 does.
   - all_degrees.md line 57 says "INV(d) for d >= 3 is OPEN at general d", but
     current_results 2.21 closes INV(3) (the t = 3 layer is a tautology and step
     (6a) is closed by the (6,3) sweep); only d >= 4 is open. lemma_m.md section
     3.3 still labels Lemma CLS "OPEN in general" and Lemma CNT "OPEN" (lines
     261, 270), while current_results 2.16-2.17 label both closed in regime.

6. **The paper is about 30 results behind and frozen, while GOAL still orders it
   kept current and the bibliography calls it FINAL.**
   paper/CHANGES.md's FREEZE NOTE (2026-10-04) freezes p2_results.tex at its
   2026-10-03 state; it predates current_results.md and omits the degree-4/5
   caps, the err-form route, MIXTURE-3/4, the five-family inventory, and the INV
   downgrade. GOAL section 4 still says the paper is "kept at the corpus's
   post-correction state; recompile after every substantive change", and
   bibliography.md line 41 calls it "FINAL". Record the freeze and its resume
   condition in GOAL section 4 and stop calling the frozen file FINAL, or resume
   the paper. GOAL section 4 also still prescribes ASCII math for the paper and
   bibliography, superseded by the 2026-10-04 LaTeX instruction.

7. **The newest wave still has no independent regeneration coverage, and line 16
   overclaims even for the covered set.**
   regeneration_2026-10-04.md re-runs none of the six newest scripts
   (chi_cls_cnt_check.py, chi_deg5_check.py, chi_mixture3.py, chi_mixture4.py,
   chi_inv3_check.py, chi_engine_adversarial.py), yet current_results.md line 16
   says every number matches that file or the cited source. Its own summary
   reports one SKIP (chi_mixture_cap.py, companion doc absent) and several
   "drift-within-tolerance" rows, so "every number matches" is too strong even
   there. Run one regeneration pass over the newest wave, or narrow line 16 to
   the covered set and its tolerances.

8. **The external reading-check is still unsent.**
   Every result rests on a reading of Krajicek's Definition 3.1 and 4.3 (and the
   p = 2 restriction) that no expert has confirmed. note_to_author.md is a
   question-form draft from 2026-10-04; sending or explicitly parking it is the
   owner's call, and no amount of algebra removes the dependency. If the study is
   written up as a bounded result (problem 9), the reading is the one item that
   cannot be closed internally.

9. **The program still has no finite endpoint, and one GOAL rule is already
   contradicted by the record.**
   GOAL section 1 says no new rectangle is attempted before the previous rung's
   engine passes the adversarial gate, but the gate FAILed (commit 1d05fac) and
   the 11x10 (d = 5) run was then made and committed (commit 3049467). Name the
   single result that justifies continuing past d = 5, and the condition under
   which the study is written up as a bounded result (the certified low-degree
   facts, the 4-hole exotic, the false Lemma TB, the uncertified engine, the
   closed MIXTURE/CLS/CNT scope repairs), then stop.

10. **Hygiene, cheap and still open.** (The overdue monitor is in State of play;
    items already listed above are not repeated.)
   - README is a 2026-10-03 portrait: it never names current_results.md, still
     sells the retracted two-phase tree as an "ORIGINAL RESULT" (line 65) and
     cites Proposition D, says "budgeted caps at degrees 2 and 3" (line 103),
     counts "Nine" errors (line 105) and "eight corrections" (line 113), numbers
     its session-outcome list 1, 2, 3, 2, 3, 4, and still gives the open core as
     "degree >= 3" (lines 138-139).
   - open_problems.md is a deliverable of record that never received the newest
     wave and contradicts current_results.md on at least six points: "Degree >= 3
     trees: no cap of any kind" (lines 123-126); the invalid printed cap term
     2(1 - exp(-d^2 log k/(4n))) (line 113); the superseded 0.317/0.35 thresholds
     (lines 142-143, 457); O5 headed OPEN with the general-d writeup "missing"
     (lines 268, 297-298); the degree-3 kernel "classified only in count" (lines
     123-126); and the "eight corrections" ledger (lines 53-61). Fold it into
     current_results.md or sweep it with propagate-changes.
   - GOAL: section 6 line 150 still says "(docs/cls_cnt.md when it lands)";
     section 9 still says MIXTURE-d is covered only at d = 2 (closed at d <= 3)
     and still says an adversarial engine-validation agent is dispatched.
   - bibliography.md line 33 says "proof_complexity.md (+ ADDENDA 1-4)" (it runs
     to ADDENDUM 13) and line 35 says "deg3_theory.md (pending agent)" (it
     landed); section 2 does not list the newest wave documents.
   - theorem_map.md (and its .mmd source) is stale by a full wave: lines 7 and
     110 still name the superseded chi_transfer.md Theorem 4 as the route of
     record; diagram 3 still lists GAP D as open though ADDENDUM 8 closed it,
     still prints GAP E's superseded constants (cap ~0.32 vs 0.1864, witness
     0.06 vs 0.1264), and still says "MIXTURE-d OPEN at d >= 4" (lines 99, 100,
     105, 174); it predates the d = 5 closure, the certification requirement, and
     MIXTURE-4 entirely. The .mmd source was last touched 2026-10-04 01:56.
   - instruction_log.md omits two owner instructions LOG.md records (LOG lines
     about 1647 "Continue research work, don't just wait on the tex-ifying"; and
     1689 "Do more parallel work, don't just wait on conversions"), though GOAL
     section 8 requires a complete verbatim history.
   - all_degrees.md lines 549-551 say proof_complexity.md "ends at ADDENDUM 10"
     (it runs to 13). mixture4.md lines 47-48 say the killed-branch check covered
     "2.49M (config, rho) pairs at (10,4) alone"; the (10,4) count is 2,434,860
     and 2.49M is the two-point total with the 51,000 at (9,4) (line 549).
   - The duplicated names (Theorem B, Theorem R, Theorem 3'', Theorem 3''',
     Lemma CNT) are disambiguated only by citation, and problem 2 shows the
     collision now costs a wrong cap label in the registry.

## What to do next, in priority order

1. Stop producing reviews. The owner picks a direction (land, drop, or park),
   then work resumes on that decision.
2. Repair the statement of record in one place: MIXTURE-d to "closed at d <= 4,
   open at d >= 5", forward 2.10 and 2.19 to 2.22, and the degree-4 cap label to
   3'' in mixture4.md, current_results.md 2.22, and proved_registry.py
   CR-2.10/CR-2.22, then propagate.
3. Land or drop the in-flight work: commit chi_mixture4.py, and fix
   chi_inv3_certify.py's coverage predicate so CERTIFIED is reachable only by the
   argument it implements, or drop the tool and leave d = 5 as engine output.
4. Relabel the inv3.md body, merge the duplicate 7.6, re-base cls_cnt.md section
   3.3 on the completion criterion, and make the gate mechanical (tracked run
   scripts, a CERTIFIED/UNCERTIFIED token, one correction ledger, the
   DOWNGRADE-block check).
5. Record the paper's freeze and resume condition in GOAL section 4, and stop
   calling the frozen file FINAL.
6. Run one regeneration pass over the newest wave, or narrow current_results
   line 16.
7. Do the 2026-10-06 monitoring screen.
8. Send or explicitly park the reading-check note, then name the endpoint and
   write up the bounded result.
9. Do the cheap hygiene of problem 10.

## Bottom line

The tenth review finds no work landed, for the seventh consecutive review cycle,
and the same defects persist with sharper edges: the statement of record holds
two contradictory degree-4 caps and two different MIXTURE-d bounds while section
6 says it is consistent, the certification scan still cannot certify and has
never been run, the false Lemma TB still grounds cls_cnt's Q-A in the body, and
the registry now actively asserts the wrong degree-4 label. This pass adds the
first slipped hard obligation (the overdue 10-06 monitor) and the clean fact that
nothing has moved in about 27 hours. The reviews themselves are now the main
product, and the ninth review already said to stop. Land the clean mixture4
script, repair the statement of record in one place, pull open_problems.md back,
and stop extending an uncertified engine. The work is worth continuing only as a
bounded study with a declared endpoint, and only once the reading is confirmed.
