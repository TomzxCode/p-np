# Guidance on the P vs NP corpus

Rewritten 2026-10-04 (second review) after the corpus grew from a study of one
reduction into a large formal program. Reviewed: layout, README, GOAL, LOG
tail, bibliography, current_results.md, all_degrees.md, cls_cnt.md, inv3.md,
mixture3.md, deg5_theory.md, open_problems.md, theorem_map.md, the Lean gate,
paper currency, and the uncommitted working tree. The prior review's content is
superseded here; items it raised that are now addressed are dropped.

## What this is now

Still not a P vs NP investigation. It has become a serious, well-organized
attempt to prove one conditional step: the all-degrees budgeted error floor
(O2) for Krajicek's pseudo-solution pipeline (arXiv:2609.35927), which would
feed Theorem 6.1 and yield AC^0[2]-Frege PHP lower bounds. That is a legitimate
research target. The headline ("prove or disprove P != NP") still oversells it,
but the corpus now says so plainly, and the earlier "93% confidence" is gone.

## What is genuinely good

- Framing discipline is fixed. README, GOAL, and current_results.md all state
  the problem is open and that no progress toward resolving it was made, and
  the PROVED / MEASURED / INFERRED distinction is now a written convention with
  a mechanical registry (`proved_registry.py`) and lint checks 8-9.
- The corpus converged on ONE current statement (`docs/current_results.md`),
  with retractions and falsification conditions in the same document. That is
  the single best structural change since the last review.
- The channel semantics are frozen (`docs/channel_spec.md`), which is exactly
  what the last review asked for (freeze semantics before coding).
- Verification culture is real: registered runs with deterministic seeds, a
  Lean sorry-budget gate, and content-hash pins on the four cited sources.
- The self-correction ledger is candid and now large (sixteen plus
  correction-class events), each logged with provenance.

## The problems, most important first

1. **The newest load-bearing claim does not hold up (verified).** `docs/inv3.md`
   claims "INV(3)(i) PROVED at d = 4 [MV]" via a "degree-truncated Buchberger
   completion" engine. I verified this independently and it is unsound:
   (a) the engine's inference to the ideal identity `I cap S_<=t = W_t` rests on
   "Lemma TB" (`docs/cls_cnt.md:124-145`), which is FALSE as stated. Explicit
   counterexample: `G = {x^2, xy+1}` over F_2[x,y], `t = 2`. The only pair has
   lcm-degree 3 > 2, so the hypothesis is vacuous, yet `1 in I cap S_<=2` and
   `1 not in W_2` (the `xy`-coefficient argument in the doc is correct, and
   proves the negation). The proof sketch needs the canceling pair's S-poly to
   be reducible, which fails whenever the representation's top degree exceeds
   `t`.
   (b) The engine never examines pairs with lcm-degree > t
   (`experiments/chi_inv3_check.py:412-415, 484-486`), but their S-polynomials
   can have degree <= t (e.g. a star row paired with a disjoint degree-2 row
   leaves a degree-3 residue). Those residues are invisible to the run, so it
   cannot detect the exotics that would refute the claim.
   (c) The verification pass can time out mid-scan and still report closure
   (`:481, 495-496, 507`).
   (d) The doc says the pass checks "all pairs" (`inv3.md:270`) but the code
   checks only lcm <= t pairs. The "four independent configurations" are also
   overstated: orders A and C are conjugate by a variable relabeling, and
   variants G/G' span the same `W_t` and share the neutrality echelon.
   The `t = 2` conclusion survives (it is separately confirmed by an exact
   dimension computation in `chi_cls_cnt_check.py` at (6,3)), but the `t = 3`,
   `d = 4` claim is not established. This is the fourth review-worthy case of
   promoting a computational artifact to a proof; it must be downgraded now,
   before anything consumes it.

2. **The tooling gate does not test the thing that matters.** `corpus_lint.py`
   PASSes ("784 CLEAN") while the load-bearing claim above is unsound. It checks
   that files contain expected substrings, scripts compile, and LOG headings are
   ordered. `proved_registry.py` checks that a PROVED claim points at a proof
   anchor; it does not check that the anchor is valid. The gate is now better
   labeled (a "linter"), which is good, but the corpus still leans on "PASS" as
   if it meant something. The only gates that mean anything are the Lean budget
   check and re-running experiments, and neither touches the algebraic claims.

3. **Consolidation lag.** `current_results.md` and `theorem_map.md` stop before
   the newest wave (all_degrees, cls_cnt, inv3, mixture3, deg5). So the "one
   current statement" is already stale, and the newest claims (including the
   unsound one) live only in un-reconciled side documents. By its own
   maintenance rule, current_results.md must be updated when a result lands or
   dies; that rule is being broken at exactly the moment it matters.

4. **Scope is narrowing while the framing still points at a Millennium
   Problem.** Even a complete proof of O2 gives only a conditional lower bound.
   The real work is now a self-referential algebra program (truncated
   Buchberger completions on an increasing family of rectangles), where each new
   rung is memory-walled (`9x8` at t=3, `11x10` next) and each claim is exactly
   as strong as its weakest engine. This is worth doing, but it should be
   presented as "a study of a finite algebraic obstruction", not as a path to
   P != NP, and the effort should be sized accordingly.

5. **Hygiene drift has returned in the working tree.** Uncommitted:
   `experiments/chi_mixture_cap.py` modified, and `docs/inv3.md` +
   `experiments/chi_inv3_check.py` untracked. GOAL section 4 requires committing
   "only a PASSING state" after every consolidated turn; the new inv3 work was
   never committed and never reconciled, which is how an unverified claim ends
   up load-bearing. Related: `lean_channel/FEASIBILITY.md:146` still says elan
   lives under `/tmp/opencode`, contradicting GOAL section 7 and the file's own
   later section, and the paper dates to 2026-10-03 while current_results is
   2026-10-04.

6. **Label vocabulary is overloaded.** "Theorem B", "Theorem R", "Theorem 3''",
   and "Lemma CNT" each name two distinct objects; the corpus disambiguates by
   citation, which is fragile. The use of "PROVED" as a bare marker inside
   side documents (deg5_theory.md, mixture3.md) blurs the formal label
   definition in current_results.md. Pick one naming scheme and one label set.

## What to do next, in priority order

1. **Downgrade the inv3 claim now.** Reclassify `docs/inv3.md`'s t=3 results as
   "engine output, unverified" until the completion argument either (a) is
   re-proved on a correct lemma (the truncated-Buchberger argument needs the
   genuine multivariate-division/Groebner theory for the *dehomogenized*
   problem, not the naive reduction), or (b) is replaced by a direct,
   independently-audited computation at a feasible rectangle. Do not consume it
   in current_results.md or the theorem map until then.

2. **Report the Lemma TB counterexample as a correction.** It is a clean,
   checkable disproof of a lemma the corpus relies on. Log it with the same
   prominence as the other correction-class events, and fix `cls_cnt.md`'s
   Section 3 label (the t=2 *conclusion* is fine; the *engine* is not).

3. **Make the gate adversarial.** Add a negative test that feeds a *known-false*
   identity through the completion engine and asserts it is flagged. An engine
   that has never been shown to reject anything has not been validated.

4. **Re-reconcile the corpus.** Fold all_degrees, cls_cnt, mixture3, deg5, and
   (corrected) inv3 into current_results.md and theorem_map.md, then commit and
   push the working tree. Update the paper's date or freeze it explicitly.

5. **Highest-value external action, unchanged:** turn `note_to_author.md` into a
   reading-check question to Krajicek or a proof-complexity person ("is my
   reading of Def 3.1/4.3 correct, and is the p=2 restriction the right place
   to look?"). Sending is the owner's call. Everything here is contingent on a
   reading that no expert has confirmed.

6. **Right-size the effort.** Set explicit stop rules for the algebra program:
   if the next rung (11x10) is memory-walled and no cheaper certificate appears,
   write it up as a bounded negative result. The current trajectory (each degree
   a new rectangle, each verified at one machine point) has no finite endpoint.

7. **Clean the vocabulary and the drift.** Disambiguate the duplicated theorem
   names, fix the FEASIBILITY.md elan note, and stop using "PROVED" in side
   documents without the anchor link the registry requires.

## Bottom line

The infrastructure and the honesty culture are genuinely good, and the corpus
correctly located the true open crux. The recurring failure is unchanged in
kind: a computational or fortunate artifact is promoted to a labeled proof
before it is verified, and the surrounding "PASS" gate does not catch it. The
newest such artifact (inv3) is load-bearing and I have shown it unsound, so the
immediate priority is to downgrade it and re-verify the engine adversarially.
After that, the work is worth continuing, but as a bounded study of a finite
algebraic obstruction, not as a run at P vs NP.
