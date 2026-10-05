# Guidance on the P vs NP corpus

Rewritten 2026-10-05 (third review) after the second review's adoption wave.
Reviewed: layout, README, GOAL, LOG tail, current_results.md, theorem_map.md,
inv3.md (the new section 3 engine, the section 7 d=5 run, the DOWNGRADE block,
and the closing label correction), the adversarial gate
(chi_engine_adversarial.py, committed run), chi_mixture4.py (in flight), the
PROVED registry and corpus_lint checks 8-9, and the working tree. I re-derived
the Lemma TB counterexample independently (G = {x^2, xy+1}, t = 2: the only pair
has lcm-degree 3, its S-polynomial is x, so 1 is in the ideal, while
W_2 = span{x^2, xy+1} does not contain 1). The second review's content is
superseded; items it raised that are now addressed are dropped. Its priorities
1-4 and 6 are done (inv3 downgraded and relabeled, the Lemma TB counterexample
logged, the adversarial gate built and run, the corpus re-reconciled, the study
framing and stop rules adopted). Its priorities 5 (the external reading-check)
and 7 (vocabulary and drift) remain and are carried below. References elsewhere
to "GUIDANCE priority N" point at the second review.

## What this is now

Still not a P vs NP investigation. It is a source-anchored study of one finite
algebraic obstruction, INV(d) (the degree-truncated Buchberger completion on
increasing rectangles) for Krajicek's pseudo-solution pipeline, plus a survey and
a claim-forensics record. Even a complete proof of INV(d) yields only a
conditional lower bound (Theorem R, premise O2), and the corpus now says so
plainly.

## What is genuinely good

- The adversarial gate is the right structural answer and it works. It fed a
  known-false identity through the completion engine and the engine reported a
  wrong closure (case 1 FAIL), it reproduced the timeout dishonesty live (case 3
  FAIL), and it showed the hidden-pair scan leaves the 7x6 closure unrefuted but
  uncertified (case 2). An engine that has been shown to reject something is
  finally in place, and the gate was committed with a pinned engine hash.
- The candor machinery is real and was used: the second review's findings were
  adopted rather than argued away, and the newest over-claim (the d=5 result) was
  caught and relabeled inside the same work session.
- current_results.md remains a strong single current statement (it folds the
  newest wave and correctly excludes the uncertified d=5 work), the channel
  semantics stay frozen, the Lean sorry/axiom budget gate stays meaningful, and
  the self-correction ledger is large and dated.

## Problems, most important first

1. **The engine is still unsound, and the corpus is extending it.** The "repair"
   in inv3.md section 3 (degree-capped completion plus span neutrality) does not
   address the root defect: it still infers the ideal identity from a closure via
   Lemma TB, which is false as stated, and it still processes only pairs with
   lcm-degree <= t, while the refuting elements come from pairs with lcm-degree
   > t. The adversarial gate proves this on the known-false G, and the 4-hole
   exotic shows the blind spot has real bite. Section 7 (added 2026-10-04) extends
   the same engine to the 11x10 rectangle, and its body still labels the result
   "INV(3)(i) at d = 5 PROVED [MV]"; a closing note now relabels it "engine
   output, uncertified", and current_results.md and the theorem map correctly
   exclude it, so the document asserts two tiers and only the appended note
   carries the boundary. GOAL section 1 also states that no new rectangle is
   attempted before the engine passes the adversarial gate; the gate FAILs and
   the 11x10 run was made and committed (it was in flight when the gate landed,
   but the rule and the record currently disagree).
   Two specifics on the planned certification scan: it must cover all pairs of
   the final G* (the gate's case 2 enumerates only base pairs with two disjoint
   degree-2 heads, and the completion adds generators), and it must be shown
   equivalent to the ideal identity, not merely sample it. If that cannot be
   shown, the sound route is the direct, independently audited computation at a
   feasible rectangle that the second review asked for, which the new quotient
   reduction (Lemma Q) may now make feasible. Pick one route and say which.

2. **The block is documentary, not mechanical.** The PROVED registry (check 8)
   covers only docs/current_results.md section 2, and the label-hygiene tripwire
   (check 9) only requires proof-kind words in the enclosing section. That is why
   the unsound d=5 PROVED label in inv3.md passed lint: the side documents where
   the algebra actually lives are outside enforcement. Extend it: any document
   whose PROVED claims feed current_results.md must be registered, or an
   engine-derived PROVED label must carry a required gate-verdict token
   (CERTIFIED / UNCERTIFIED). The gate cannot be a pass/fail commit gate while it
   correctly FAILs, but its verdict must gate every engine-derived PROVED label.

3. **The external reading-check is still unsent, and it is still the highest-value
   action.** Every result here rests on a reading of Krajicek's Definition 3.1
   and 4.3 and on the p=2 restriction that no expert has confirmed.
   note_to_author.md is a draft reading-check question; sending (or explicitly
   parking) it is the owner's call. Until it is answered the whole frame is
   contingent, and no amount of algebra removes that dependency.

4. **The program still has no finite endpoint; the wall moved rather than
   vanished.** The 11x10 memory wall was bypassed (Lemma Q, 1.32 GB peak), so the
   adopted stop rule ("if 11x10 is memory-walled, write it up and stop") no longer
   fires. But the certification wall replaced the memory wall, the pivot store
   still grows about 9.3x per degree (d=6 needs about 16 GB dense or a byte-packed
   store), and at d >= 4 each new degree also needs a new MIXTURE family
   (chi_mixture4.py is in flight). This is the open-ended per-rung trajectory the
   second review flagged. Replace the moot stop rule with a decision point: name
   the single result that would justify continuing past d=5, and the condition
   under which the study is written up as a bounded result (the certified
   low-degree facts, the 4-hole exotic, the false Lemma TB, and the uncertified
   engine), then stop.

5. **Consolidation and vocabulary, cheap but open.** Keep the tier boundary
   explicit (certified in current_results.md and the theorem map; engine output
   only in inv3.md section 7), and soften the inline labels in 7.4 and the 7.5
   table, not just the appended note. The duplicated names (Theorem B,
   Theorem R, Theorem 3'', Lemma CNT) are still disambiguated only by citation;
   pick one naming scheme. README and GOAL still date 2026-10-03/04 while the
   newest work is 2026-10-05, and the untracked chi_mixture4.py is in-flight
   drift.

## What to do next, in priority order

1. Commit to one certification route for the engine, and promote nothing
   engine-derived (including d=5) until it passes. Either a full all-pairs
   hidden-residue scan shown equivalent to the ideal identity, or the direct
   audited computation. Meanwhile soften the inline PROVED labels in inv3.md
   sections 3-7 under the existing DOWNGRADE banner, so the body no longer
   contradicts the banner.
2. Make the block mechanical: extend the registry and lint so an engine-derived
   PROVED label cannot be committed without a CERTIFIED gate line, and add the
   gate verdict to the "passing state" check in GOAL section 4.
3. Send or explicitly park the reading-check note to a proof-complexity person,
   and record the decision either way.
4. Replace the moot stop rule with the concrete decision point of problem 4, and
   reconcile GOAL section 1 with what actually happened at 11x10.
5. Do the cheap hygiene: one naming scheme, date updates, and either commit the
   in-flight mixture4 deliverable with its document or drop it from the tree.

## Bottom line

The infrastructure, the self-correction culture, and now the adversarial gate are
genuinely good, and the second review's findings were adopted rather than
defended. The recurring failure (a computational artifact promoted to a labeled
proof before verification) has not gone away; it just recurred at d=5, and the
mechanical gates still do not block it because they cover only
current_results.md. The fix is to make the engine's certification a precondition
for any PROVED label, not a follow-up note, and to stop extending an uncertified
engine. The work is worth continuing only as a bounded study with a declared
endpoint, and only once the reading is confirmed.
