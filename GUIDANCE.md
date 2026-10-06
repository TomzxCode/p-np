# Guidance on the P vs NP corpus

Rewritten 2026-10-06 (ninth review). Reviewed: the git state, the artifacts the
eighth review covered (current_results.md, open_problems.md, inv3.md,
cls_cnt.md, theorem_map.md, all_degrees.md, lemma_m.md, mixture4.md,
proved_registry.py, corpus_lint.py and a live lint run, the two untracked
scripts, README, GOAL, bibliography.md, instruction_log.md), plus the paper's
CHANGES.md and a fresh cross-file status sweep. Findings new to this pass are
marked NEW. Nothing the seventh and eighth reviews flagged has been addressed.

## State of play

- Nothing landed. HEAD is 737de02, the eighth review, a GUIDANCE-only commit.
  The only working-tree change is the same two untracked scripts,
  chi_inv3_certify.py (mtime 2026-10-05 03:45) and chi_mixture4.py (mtime
  2026-10-05 00:22). /tmp/opencode, the certification scan's CERTDIR, holds no
  artifacts.
- The guidance queue is now seven reviews deep (third through ninth). LOG.md's
  only adopt/reject entries are for the first and second reviews (the second at
  LOG line 2062); GOAL section 9 makes the record mandatory. Four consecutive
  reviews have produced no line of work between them.
- The substantive picture is unchanged: O2's cap is assembled at degrees 2
  through 5 with the same d^2 ~ n boundary, MIXTURE-d is closed at d <= 4
  (mixture4.md), the d = 5 closure is engine output and uncertified, and the
  single mathematical gap is INV(d) at t >= 3.
- corpus_lint.py reports CLEAN (862 items, 0 FAIL) while the statement of
  record contradicts itself (problem 2). A PASS means the needle strings
  matched, not that the corpus agrees with itself; do not read it as a status
  certificate.

## What is genuinely good

- The correction culture still works. mixture4.md's own registered assert
  caught a coin-keying non-conformance before any number was trusted, and the
  adversarial gate is a real attempt to attack the engine rather than trust it.
- current_results.md remains the right idea: one current statement with
  PROVED/MEASURED/INFERRED labels, enforced by proved_registry.py and
  corpus_lint.py checks 8-9. Its problem is maintenance, not conception.
- The 11x10 quotient construction (Lemma Q) is a genuine engineering result:
  it replaced an infeasible ~5.1 GB dense echelon with a 0.63 GB quotient
  echelon, and the closure reproduced at two configurations. It is the right
  shape of "cheaper certificate" the stop rules asked for.

## Problems, most important first

1. **The review queue is the first problem, and it is now seven deep.**
   Process the queue before producing anything new: record adopt/reject for the
   third through ninth reviews in LOG.md, then do ONE consolidation turn
   (problem 2) instead of another result wave. If a subsequent review pass
   again finds no landed artifact, stop generating reviews until one lands;
   the reviews are now themselves the only commits, and that is the clearest
   signal that the process is stuck.

2. **The one current statement contradicts itself on MIXTURE-d, and section 6
   declares it consistent. NEW framing: the split is now internal to
   current_results.md, not only across files.**
   - Live answer: closed at d <= 4, open at d >= 5 (section 2.22, mixture4.md).
   - Same file says closed at d <= 3: section 2.8 lines 351-352, section 2.18
     line 749, section 4 item (ii) line 1037, section 5 line 1105, section 6
     line 1133. Section 6's claim that "No live inconsistency between sources
     was found" (line 1130) is false as written.
   - Fix: state MIXTURE-d once in current_results.md as "closed at d <= 4, open
     at d >= 5", have section 2.19 (M3-D) point forward to section 2.22, and
     propagate the single form to all_degrees.md (lines 67-68, 489),
     mixture3.md (its own d <= 3 scope), proof_complexity.md ADDENDUM 12,
     theorem_map.md line 105, and GOAL.md sections 6 and 9.
   - NEW: the degree-4/5 mislabel is now machine-enshrined. mixture4.md calls
     the repaired degree-4 cap "Theorem 3'''" while citing deg4_theory.md
     Theorem 3'' (lines 72-73, 422); current_results.md 2.22's title repeats it;
     and proved_registry.py's CR-2.22 short statement says "Theorem 3''' cap
     constant repaired to q4^mix". Degree 4 is 3'', degree 5 is 3'''. The
     registry cannot police the label it repeats, so fix all three together.

3. **The certification scan still cannot return CERTIFIED in either coded mode,
   and no run exists.**
   - Sharded mode: JOB_PLAN samples the six classes (AD3,b), (AD3,C), (AD3,H),
     (AD3,ST), (AD2,AD3), (AD3,AD3), but do_collect derives sampled coverage
     from a hard-coded class name, `sampled = cls_s == "AD3xAD3"`
     (chi_inv3_certify.py line 900). The other five sampled classes fail the
     "exhaustive" coverage check and the verdict is INCONCLUSIVE. The
     docstring's "Exit code: 0 CERTIFIED (on the stated coverage)" (line 89) is
     unreachable.
   - Single-process mode: CERTIFIED requires `complete and examined == grand`
     (line 1202) over ~217,470 (AD3,3) pairs; the docstring's own note puts
     (AD3,AD3) at ~0.1-0.7 s/pair (lines 65-68), so the default 3000 s guard
     cannot cover it and `complete` is False. INCONCLUSIVE again.
   - Fix: derive `sampled` from job_plan()'s mode field so the verdict's
     coverage declaration matches the plan, and either make the exhaustive
     predicate honest or state the verdict as SAMPLED. Then land a run or drop
     the tool. The dispatch named in LOG.md ("certification agent dispatched",
     session ses_ef6a1f5e5ffeg8LkDCHqqEFJCP) has produced no artifact in
     /tmp/opencode and no commit, so the d = 5 claim has been "pending
     certification" across five reviews.

4. **inv3.md's body still asserts PROVED over the downgraded claim.**
   Section 0 line 53, section 1, the section 3.2-3.3 and 7.5 tables, and
   section 7's intro assert PROVED, while the top DOWNGRADE block (lines 5-33)
   and section 7.6 relabel the same claim engine output. Lint check 9 passes
   these because it never reads the top-of-file downgrade. NEW: the file has
   two consecutive "### 7.6" headings (lines 675 and 690). Fix: relabel the
   body, merge the duplicate 7.6, and add a check that a file whose top block
   carries a DOWNGRADE must not assert PROVED for that claim in its body.

5. **The PROVED gate is not mechanical, and the counts it would police are
   wrong.**
   - Neither registered-run script is tracked by git: chi_mixture4.py (behind
     PROVED claim CR-2.22) and chi_inv3_certify.py (the d = 5 certification
     tool) are both untracked. corpus_lint.py check 2 resolves references via
     CORPUS.rglob, so the untracked scripts pass on this disk but would fail in
     a fresh clone; check 6 flags only orphan scripts, never a missing
     referenced one. The lint is green partly because it cannot see the gap.
   - CR-2.22 anchors to prose ("Repaired cap (Theorem M4-D)"), not to a run.
     Require every registered-run script to be tracked (git ls-files) and every
     engine-derived PROVED label to carry a CERTIFIED or UNCERTIFIED token, and
     add both to GOAL section 4's passing state.
   - NEW: the corpus cannot state how many corrections it has made. The counts
     span eight to nineteen: open_problems.md says "eight corrections" (lines
     53-61); README says "Nine analysis/instrument errors" (line 105) and
     "eight corrections" (line 113); GOAL section 3 says "nine correction-class
     events" (line 65); proof_complexity.md line 924 says "after eight
     corrections" and its ADDENDUM 13 header calls cls_cnt "the SEVENTEENTH
     correction-class event"; LOG.md calls mixture4 "the NINETEENTH". Derive
     one ledger from LOG/ADDENDA and cite it everywhere.
   - cls_cnt.md's section 3.3 still concludes "Lemma TB applies with t = 2 and
     gives ... [PROVED]" (lines 194-200) although its section 3.2 correction
     block says Lemma TB is false as stated, and proved_registry.py anchors
     CR-2.16 to that section header. Re-base Q-A on the repaired completion
     engine, as inv3.md section 7 already does.
   - all_degrees.md line 57 says "INV(d) for d >= 3 is OPEN at general d", but
     current_results 2.21 closes INV(3) (the t = 3 layer is a tautology and
     step (6a) is closed by the (6,3) sweep); INV(d) is open only for d >= 4.
     lemma_m.md section 3.3 still labels Lemma CLS "OPEN in general" and Lemma
     CNT "OPEN" (lines 261, 270), while current_results 2.16 and 2.17 label
     both closed in regime.

6. **NEW: the paper is ~30 results behind and frozen, while GOAL still orders
   it kept current and the bibliography calls it FINAL.**
   paper/CHANGES.md's FREEZE NOTE (2026-10-04, per the second review) freezes
   p2_results.tex at its 2026-10-03 content state; it predates current_results.md
   entirely and omits the degree-4/5 caps, the err-form route, MIXTURE-3/4, the
   five-family inventory, and the INV downgrade. GOAL section 4 still says the
   paper is "kept at the corpus's post-correction state; recompile after every
   substantive change", and bibliography.md line 41 labels the paper
   "(p2_results.tex/pdf, FINAL)". Record the freeze and its resume condition in
   GOAL section 4 (and stop calling the frozen file FINAL), or resume the paper;
   leaving the contradiction in place means the deliverable of record silently
   diverges from the current statement. Note that GOAL section 4 also still
   lists pre-LaTeX "ASCII math" for the paper/bibliography, which the 2026-10-04
   LaTeX instruction superseded.

7. **The newest wave still has no independent regeneration coverage, and line
   16 overclaims even for the covered set.**
   regeneration_2026-10-04.md re-runs none of the six newest scripts
   (chi_cls_cnt_check.py, chi_deg5_check.py, chi_mixture3.py, chi_mixture4.py,
   chi_inv3_check.py, chi_engine_adversarial.py), yet current_results.md line 16
   says every number matches that file or the cited source. NEW: the covered
   set itself is described in the file as one SKIP (chi_mixture_cap.py, its
   companion doc absent) and several "drift-within-tolerance" rows, so "every
   number matches" is too strong even there. Run one regeneration pass over the
   newest wave, or narrow line 16 to the covered set and its tolerances.

8. **The external reading-check is still unsent.**
   Every result rests on a reading of Krajicek's Definition 3.1 and 4.3 (and
   the p = 2 restriction) that no expert has confirmed. note_to_author.md is a
   question-form draft from 2026-10-04; sending or explicitly parking it is the
   owner's call, and no amount of algebra removes the dependency. If the study
   is to be written up as a bounded result (problem 9), the reading is the one
   item that cannot be closed internally.

9. **The program still has no finite endpoint, and one GOAL rule is already
   contradicted by the record.**
   GOAL section 1 says no new rectangle is attempted before the previous rung's
   engine passes the adversarial gate, but the gate FAILed (commit 1d05fac)
   and the 11x10 (d = 5) run was then made and committed (commit 3049467).
   Name the single result that justifies continuing past d = 5, and the
   condition under which the study is written up as a bounded result (the
   certified low-degree facts, the 4-hole exotic, the false Lemma TB, the
   uncertified engine, the closed MIXTURE/CLS/CNT scope repairs), then stop.

10. **Hygiene, cheap and still open.**
   - README is a 2026-10-03 portrait: it never names current_results.md, its
     artifact guide still sells the retracted two-phase tree as an "ORIGINAL
     RESULT" and still cites Proposition D, it counts "Nine" errors (line 105)
     and "eight corrections" (line 113), its session-outcome list numbers
     1, 2, 3, 2, 3, 4, and its open-core line still says the all-degrees floor
     is "degree >= 3" (lines 138-139) where the current gap is INV(d) at t >= 3
     plus MIXTURE-d at d >= 4.
   - open_problems.md is a deliverable of record that never received the newest
     wave and contradicts current_results.md on at least six points: the O2
     open core says "Degree >= 3 trees: no cap of any kind" (lines 122-126);
     the displayed cap uses the invalid printed term 2(1 - exp(-d^2 log k/(4n)))
     (line 113); the thresholds are the superseded 0.317/0.35 (lines 142-143,
     457); O5 is headed OPEN with the general-d writeup "missing" (lines 268,
     297-298); the O2 open core (i) says the degree-3 kernel is classified
     "only in count" (lines 123-126); and the ledger says "eight corrections"
     (lines 53-61). Fold it into current_results.md or sweep it with
     propagate-changes.
   - GOAL: section 3's ledger count (problem 5); section 6 line 150 still says
     "(docs/cls_cnt.md when it lands)" (it landed); section 9's O2 status says
     MIXTURE-d is covered only at d = 2, its INV status still says an
     adversarial engine-validation agent is dispatched (it ran and FAILed), and
     its MIXTURE-d line says closed at d <= 3.
   - bibliography.md line 33 says "proof_complexity.md (+ ADDENDA 1-4)" (it
     runs to ADDENDUM 13) and line 35 says "deg3_theory.md (pending agent)" (it
     landed); section 2 does not list the newest wave documents at all.
   - theorem_map.md lines 7 and 110 still name the superseded chi_transfer.md
     Theorem 4 as the route of record, while chi_transfer.md itself says to use
     err_form_route.md Theorem R; diagram 3 still lists GAP D as open though
     ADDENDUM 8 closed it, still prints GAP E's superseded constants (cap ~0.32
     against 0.1864, witness 0.06 against 0.1264), and still says "MIXTURE-d
     OPEN at d >= 4" (lines 99, 100, 105). Diagram 3 also predates the d = 5
     closure and the certification requirement.
   - instruction_log.md omits two owner instructions that LOG.md records (LOG
     lines ~1647 and ~1689: continue research rather than wait on typesetting;
     do more parallel work), though GOAL section 8 requires a complete verbatim
     history.
   - all_degrees.md lines 549-551 say proof_complexity.md "ends at ADDENDUM
     10"; it runs to ADDENDUM 13. mixture4.md lines 47-48 say the killed-branch
     check covered "2.49M (config, rho) pairs at (10,4) alone"; the (10,4)
     count is 2,434,860 and 2.49M is the two-point total with the 51,000 at
     (9,4) (line 549).
   - NEW: the daily monitor is behind. The last screen is
     docs/monitors/monitor_2026-10-05.md; the material 6-Oct wave (Tue 00:00
     UTC) is due and no 2026-10-06 deliverable exists. GOAL section 5 requires
     a daily screen.
   - The duplicated names (Theorem B, Theorem R, Theorem 3'', Theorem 3''',
     Lemma CNT) are disambiguated only by citation, and problem 2 shows the
     collision now costs a wrong cap label in the registry.

## What to do next, in priority order

1. Process the guidance queue (third through ninth) and record adopt/reject in
   LOG.md, then do ONE consolidation turn.
2. Repair the statement of record in one place: fix MIXTURE-d to "closed at
   d <= 4, open at d >= 5", correct the degree-4 cap label to 3'' in
   mixture4.md, current_results.md 2.22, and proved_registry.py CR-2.22, then
   propagate.
3. Land or drop the in-flight work: commit chi_mixture4.py, and fix
   chi_inv3_certify.py's coverage predicate so CERTIFIED is reachable only by
   the argument it implements, or drop the tool and leave d = 5 as engine
   output.
4. Relabel the inv3.md body, merge the duplicate 7.6, re-base cls_cnt.md
   section 3.3 on the completion criterion, and make the gate mechanical
   (tracked run scripts, a CERTIFIED/UNCERTIFIED token, one correction ledger,
   the DOWNGRADE-block check).
5. Record the paper's freeze and resume condition in GOAL section 4, and stop
   calling the frozen file FINAL.
6. Run one regeneration pass over the newest wave, or narrow current_results
   line 16.
7. Send or explicitly park the reading-check note, then name the endpoint and
   write up the bounded result.
8. Do the cheap hygiene of problem 10.

## Bottom line

The ninth review again finds no work landed, so the queue is seven deep and the
same defects persist, now with sharper edges: the statement of record
contradicts itself on MIXTURE-d and its section 6 says it is consistent, the
certification scan still cannot certify and has still never been run, the false
Lemma TB still grounds the cls_cnt Q-A in the body, and the gate is still not
mechanical. This pass adds the paper's freeze against GOAL's keep-it-current
rule, the eight-to-nineteen spread in the correction count, the registry now
repeating the wrong degree-4 theorem number, and the overdue daily monitor.
Land the clean mixture4 script, repair the statement of record in one place,
pull open_problems.md back, and stop extending an uncertified engine. The work
is worth continuing only as a bounded study with a declared endpoint, and only
once the reading is confirmed.
