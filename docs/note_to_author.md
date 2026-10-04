# Reading-check question on "Pseudo-solutions of polynomial systems and the lower
# bound problem for AC0[p]-Frege systems" (arXiv:2609.35927 v2)

Prepared 2026-10-04 (rewritten per GUIDANCE.md: this was a claim-style draft; it
is now a question-style draft, which is what the content supports). Draft for
communication to the author (Jana Krajicek, Charles University) or to a proof
complexity colleague. NOT sent or posted; the decision belongs to the corpus
owner, and the guidance recommends sending it as a question, not a claim.

## The question

We have been studying the p = 2 case of your pseudo-solution framework
(arXiv:2609.35927) and would like to check our reading of two definitions
before drawing any conclusions from it.

(1) Under Definition 3.1 as printed, is condition 3 quantified over ALL
(d, e)-trees (so that a pseudo-solution must be robust against every shallow
decision tree), or over the specific tree T' extracted in the contrapositive
argument of Theorem 3.2? The distinction matters for us: under the first
reading, we can show that a particular simple tree (a two-scan strategy using
only degree-1 queries) forces the failure probability of any candidate
Omega(n,d) built from independently randomizable designs down to a constant
Theta(2^{-2d}) at p = 2 - constant failure, not the required k^{-O(1)} failure
direction, but ALSO not below k^{-O(1)}, so the definition is not obviously
violated; under the second reading, our computation applies to a different
object than the one your proof consumes.

(2) Under Definition 4.3 as printed, we read the design L as vanishing on
V(n,d)^rho, and we found that at p = 2 this forces the free-pigeon row sums of
the answer table to be locked (their XOR is always 1), while free-hole columns
remain unconstrained. Is that the intended reading, or did you intend L to
range over a canonical design space Des(2d,d) with different constraints? The
two readings give materially different behavior for degree-1 linear queries.

(3) Conditional on our reading being correct: is the p = 2, constant-d regime
the right place to look for counterexamples to candidate pseudo-solutions, or
do you expect the interesting obstructions at growing d?

## What we can offer if useful

At p = 2 we have exact descriptions of the answer channel for degree-1 and
degree-2 queries (with computer verification at small parameters), a proved
budgeted error cap for the full adaptive degree-2 and degree-3 tree classes
(the error stays above k^{-Theta(d^2/n)}-style bounds while d^2 log k = o(n)),
and an inventory of the "certain-certificate" mechanisms available to shallow
trees. We are aware this is a toy-scale study of one restriction; we are not
claiming it obstructs the program, and we would value your reading of (1)-(3)
before deciding whether any of it is worth writing up properly.

## Practical note

If the reading-check surfaces a misreading, we will correct our study and
nothing needs to be sent. If the reading is right, we would ask only whether a
short note on the p = 2 restriction (2-3 pages, the tree construction and the
cap) would be useful to you or to the proof complexity community, and in what
form.
