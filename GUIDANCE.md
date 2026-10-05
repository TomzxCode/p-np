# Guidance on the P vs NP corpus

Rewritten 2026-10-05 (fourth review), after the MIXTURE-4 wave and the
certification-scan dispatch. Reviewed: layout, README, GOAL, LOG tail,
current_results.md (including the new 2.22), theorem_map.md, all_degrees.md
section 5.2, inv3.md (sections 0, 3, 7, and the 7.6 relabel), the adversarial
gate, mixture4.md, proved_registry.py and corpus_lint.py checks 8-9, the
in-flight chi_inv3_certify.py, and the working tree. The third review's adopted
items are folded in; items it raised that are now addressed are dropped, with
the accounting just below. References to "GUIDANCE priority N" elsewhere point
at the second review unless stated otherwise.

## Third review to now (what changed, what is dropped)

- Its priority 1 (pick one certification route; soften the inline d = 5 PROVED
  labels): the route is picked (the hidden-pair residue scan) and inv3 section 7
  carries an ORCHESTRATION LABEL CORRECTION, but the inline body labels were not
  softened (sections 0, 3.3, and 7.4 still assert PROVED), and the scan as
  designed cannot certify. Carried below in sharpened form.
- Its priority 5 in-flight item (commit or drop the mixture4 deliverable): the
  document landed and is consolidated, but the registered script did not. New
  form below.
- Its observation that the d = 5 over-claim was caught and relabeled in the same
  session stands; nothing new there, so it is dropped.

## What this is now

Still not a P vs NP investigation. It is a source-anchored study of one finite
algebraic obstruction, INV(d) (the degree-truncated Buchberger completion on
increasing rectangles) for Krajicek's pseudo-solution pipeline, plus a survey
and a claim-forensics record. Even a complete proof of INV(d) yields only a
conditional lower bound (Theorem R, premise O2). MIXTURE-4 (2026-10-05) closed
the mixture scope gap at d <= 4 with a constant-only repair, so the object is
now: O2's cap assembled at every degree 2-5 with the same d^2 ~ n boundary, two
scope gaps closed (MIXTURE-d at d <= 4; Lemma CLS and CNT in regime), and
exactly one mathematical gap left (INV(d) at t >= 3).

## What is genuinely good

- MIXTURE-4 is a clean, well-bounded result with the corpus's usual pattern: a
  new winner (star-4M) that beats the covered constant at finite n only, the
  mechanism extended verbatim, all constants digit-exact, and the correction
  culture working. Its own simulator assert caught a coin-keying non-conformance
  before any number was trusted, and mixture3.md section 2.2's support-4
  attribution was corrected without moving a registered result. Nineteenth
  correction-class event.
- The certification scan is the right structural answer to the third review's
  route demand: it extends the adversarial gate's case 2 from base pairs to all
  pairs of the final completion basis, re-runs the registered 11x10 completion
  and asserts its trace, unifies the coin keys, and states its coverage exactly.
  It is a real attempt to close the engine's blind spot rather than argue it
  away.
- current_results.md remains the one current statement of the proved and
  measured core, the channel semantics stay frozen, the Lean budget gate stays
  meaningful, and the newest wave's stale lines are acknowledged in the
  consolidation note rather than hidden.

## Problems, most important first

1. **The certification scan cannot certify as designed, and the document still
   bases the closure on the false Lemma TB.** The sharded plan samples the
   (AD3, AD3) class (217,470 pairs at an estimated 12-40 h) and still prints
   exit 0 CERTIFIED "on the stated coverage"; a sample cannot certify. The
   docstring also says the identity follows "By Lemma TB", which is false as
   stated, so the correctness argument must be re-based on the criterion the
   scan actually implements: if the engine closes over all lcm <= t pairs with
   the neutrality checks, and an EXHAUSTIVE hidden-pair scan of the final G*
   finds every in-cap S-polynomial residue in W_t (out-of-cap residues being out
   of scope), then G* is a truncated Groebner basis for I and I cap S <= t = W_t,
   with no appeal to Lemma TB. Fix the contract to match that argument:
   exhaustive, or verdict SAMPLED with d = 5 left as engine output. The
   (AD3, AD3) class is the dangerous one, so sampling exactly it is the worst
   place to sample.
   Even a full scan at 11x10 certifies one rectangle; INV(3) at general d
   remains one finite run per rectangle, the open-ended per-rung trajectory the
   second review flagged.

2. **The PROVED gate is still not mechanical, and this wave shows the cost.**
   chi_mixture4.py, the registered script behind a new PROVED claim (CR-2.22),
   is untracked; the registry anchors a PROVED claim to a documentation
   substring, not to a committed run, so a claim can land with its script absent
   from git. Third review priority 2 stands: extend the registry and lint so
   (a) a run-backed or engine-derived PROVED label cannot be committed without
   its registered script in the tree, and (b) an engine-derived PROVED label
   carries a required gate-verdict token (CERTIFIED or UNCERTIFIED). The gate's
   verdict, not a pass or fail commit hook, gates the label.

3. **current_results.md is no longer a single current statement for the degree-4
   cap.** Section 2.10 still displays the degree-4 cap constant q4* = max(q,
   q_and, post3, post4); section 2.22 states the degree-4 class cap is q4^mix >
   q4* and calls it "Theorem 3'''". The degree-4 cap is Theorem 3'' (2.10), not
   3''' (2.20, degree 5); mixture4.md's own parenthetical ("Theorem 3''' as
   printed (deg4_theory.md Theorem 3'')") concedes the collision. Two entries
   now give different constants for the same theorem. Repair 2.10 in place (or
   fold 2.22 into it), fix the theorem number, and carry 2.19's caveat: "closed
   at d <= 4" rests on the CONJECTURED support <= 4 truncation dominance and a
   CONJECTURED two-query certificate classification, exactly as 2.19 says for
   d <= 3.

4. **The newest wave did not propagate to the map or to all_degrees.md.**
   theorem_map.md diagram 3 still lists GAP D (de-modularize the JDP steps) as
   open though ADDENDUM 8 closed it, still prints GAP E's superseded constants
   (cap ~0.32 vs witness 0.06; now 0.1864 and 0.1264), and still says "MIXTURE-d
   OPEN at d >= 4"; all_degrees.md section 5.2 item 2 still says the mixture
   class "is covered only at d = 2". Only current_results.md carries the
   resolved form. Run propagate-changes (or an equivalent sweep) so the map and
   the premise document match the statement of record.

5. **The external reading-check is still unsent, and it is still the
   highest-value action.** Every result rests on a reading of Krajicek's
   Definition 3.1 and 4.3 and the p = 2 restriction that no expert has
   confirmed. note_to_author.md is a question draft; sending or explicitly
   parking it is the owner's call, and no amount of algebra removes the
   dependency.

6. **The program still has no finite endpoint, and the old stop rule is still
   moot.** The 11x10 memory wall was bypassed by Lemma Q, so the adopted "if
   11x10 is memory-walled, write it up and stop" rule cannot fire; the
   certification wall replaced it, and the pivot store still grows about 9.3x
   per degree (d = 6 needs about 6 GB, feasible only with a byte-packed store).
   The third review's request stands: name the single result that justifies
   continuing past d = 5, and the condition under which the study is written up
   as a bounded result (the certified low-degree facts, the 4-hole exotic, the
   false Lemma TB, the uncertified engine, and the four closed MIXTURE and
   CLS/CNT scope repairs), then stop. GOAL section 1 also still says no new
   rectangle is attempted before the engine passes the adversarial gate; the
   gate FAILs and d = 5 was run and committed. Reconcile the rule with the
   record, or the rule is noise.

7. **Hygiene, cheap and still open.** Dates: README says 2026-10-03 and GOAL
   2026-10-04 while the newest work is 2026-10-05. inv3.md has two consecutive
   "### 7.6" headings. The duplicated names (Theorem B, Theorem R, Theorem 3'',
   Lemma CNT) are still disambiguated only by citation, and problem 3 shows the
   collision now costs a wrong label. GOAL section 6's INV status is stale (the
   gate has since run and FAILed, and the d = 5 closure and the certification
   scan are absent). The new section 2.22 is written in ASCII where the rest of
   section 2 uses LaTeX.

## What to do next, in priority order

1. Fix the certification contract: commit chi_mixture4.py (its numbered run is
   already quoted in the corpus); re-base inv3 section 7 on the completion
   criterion rather than Lemma TB; make chi_inv3_certify.py print CERTIFIED only
   on exhaustively covered classes, or rename the verdict and keep d = 5 as
   engine output. Meanwhile soften the inline PROVED labels in inv3 sections 0,
   3.3, and 7.4 to match the 7.6 correction.
2. Make the gate mechanical: extend proved_registry and corpus_lint as in
   problem 2, and add "every PROVED script is tracked, engine-derived PROVED
   labels carry a gate-verdict token" to GOAL section 4's passing state.
3. Repair the degree-4 cap statement of record (problem 3): one entry, the right
   theorem number, the conjectured-truncation caveat.
4. Propagate the newest wave to theorem_map.md and all_degrees.md (problem 4).
5. Replace the moot stop rule with the decision point of problem 6, and
   reconcile GOAL section 1 with the d = 5 record.
6. Send or explicitly park the reading-check note, and record the decision
   either way.
7. Do the cheap hygiene (problem 7).

## Bottom line

The correction culture still works and MIXTURE-4 is a real, cleanly bounded
result. But the recurring failure (a computational artifact promoted before
verification) has moved rather than gone: it now sits in the certification scan
(a sample presented as CERTIFIED) and in the registry (a PROVED claim whose run
is not committed). The mechanical gates still cover only current_results.md, and
the one current statement has already split into two conflicting degree-4 cap
entries. Fix the certification contract, make the gate mechanical, and do not
extend an uncertified engine before d = 5 becomes another d = 4. The work is
worth continuing only as a bounded study with a declared endpoint, and only once
the reading is confirmed.
