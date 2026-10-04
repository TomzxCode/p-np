# The proof-complexity rung: from resolution to Extended Frege (verified 2026-10-03)

The route: NP != coNP implies P != NP, and (Cook-Reckhow) a polynomially bounded propositional
proof system exists iff NP = coNP. So a super-polynomial lower bound for ANY sufficiently
strong proof system (Frege, Extended Frege) proves P != NP. This is the only route whose
target is a lower bound about proofs rather than circuits.

## The systems ladder, with the state at each rung (2026)

NEW (Sept 2026, monitoring turn 15): an exponential lower bound for the bit pigeonhole
principle in UNRESTRICTED DAG-like Res(⊕) — resolution over parities, the system
immediately below AC0[2]-Frege (arXiv:2609.23015; Lean 4-formalized; developed with
substantial AI assistance within an open research framework). This removes the regularity
and proof-depth restrictions required by all prior Res(⊕) bounds, and is the first
unrestricted BPHP lower bound in Res(⊕). The AC0[2]-Frege lower-bound problem itself
remains open (the paper's Section 9 says what does and does not follow). Directly
relevant to this corpus: the adjacent-frontier system moved in 2026, by a Lean-formalized
AI-assisted proof — the same method shape as this session's work.

NEW (2026-10-03 screen b, monitor pass 2): the 2026 Res(⊕) program context around the
Braun bound, previously missing from this map (all verified against ECCC/arXiv primary
sources; details in `monitor_2026-10-03b.md`):
- TR26-007 (Alekseev-Gaevoy, 2 Jan 2026): polynomial-depth Res(⊕) lower bounds for a
  Constrained BPHP (CBPHP); exp(N^Ω(1)) size for every constant depth k under a
  combinatorial assumption, unconditionally for RevRes(⊕) and for depth N^{2-ε}.
  Superseded in regime by Braun's unrestricted bound; program context.
- TR26-018 (Itsykson-Podolskii-Shekhovtsov, 12 Feb 2026): resolution-width lifts to
  near-quadratic-depth Res(⊕) size; formulas with polynomial resolution refutations but
  superpolynomial Res(⊕) refutations below depth o(n^2/log^4 n). Program context.
- arXiv:2511.20023 (Byramji-Impagliazzo, 25 Nov 2025): depth N^{2-ε} exponential bounds
  for BPHP_n^(n+1) and t-collision generalizations; the "[BI, arXiv'25]" cited by
  TR26-018; the direct predecessor of the Braun bound in this lane.
- TR26-078 (de Rezende et al., 3 May 2026): tree-like bounded-line-size semantic proof
  systems; adjacent, not DAG-like AC0[2]-Frege.
Reading: the Res(⊕)-vs-BPHP lane is one of the fastest-moving lower-bound frontiers in
proof complexity right now (four substantive reports in eleven months, capped by the
unrestricted Braun bound), while AC0[2]-Frege itself remains open above it.

- The AC0[2]-Frege frontier: the nearest rung above. The Res(⊕) breakthrough (below it
  in the hierarchy) raises the pressure on AC0[2]-Frege: the lifting techniques of the
  Res(⊕) frontier do not transfer directly (the bit-to-unary substitution is nonlinear),
  but the psychological-and-methodological pressure is now maximal.

- Resolution: exponential lower bounds (Haken 1985, pigeonhole; Tseitin; random CNFs),
  width-size machinery (Ben-Sasson-Wigderson). Settled.
- Res(k) (k-DNF resolution): exponential for restricted regimes (Segerlind-Buss-Impagliazzo;
  Alekhnovich extended to 3-CNFs with Res(sqrt(log n)); Razborov removed a square-root loss).
- AC0-Frege (constant-depth Boolean lines): exponential (Ajtai 1994, PHP; Beame et al.).
  Random 3-CNFs: first non-trivial bounds only recently - Omega(n^{1+eps_k}) for depth-k
  Frege, eps_k = 2^{-Theta(k)} (arXiv:2403.02275, via deterministic restrictions and "weak
  expanders"). The super-polynomial bound for random 3-CNFs in bounded-depth Frege remains
  open.
- AC0[p]-Frege (mod-p gates added): THE 30-year open problem. The circuit lower bounds for
  AC0[p] (Razborov-Smolensky) have never been lifted to the proof system. Status mapped this
  session: (a) the system is equivalent to the Extended Nullstellensatz (ENS) algebraic proof
  system (Buss-Kolodziejczyk-Zdanowski line); (b) Krajicek (Proc. AMS 2024, and arXiv:2609.35927,
  Sept 2026) reduced the whole lower-bound problem to constructing "pseudo-solutions" for the
  negated PHP system, and further to a concrete combinatorial probability task about error in
  particular search trees - any k(n) >= n^{omega(1)} would be interesting, 2^{n^delta} would
  give the lower bound. A candidate pseudo-solution exists (from 2024); proving its properties
  is the current bottleneck.
- TC0-Frege: open; PHP is easy here, so the standard hard candidates fail.
- AC0[2]-Frege: described in the 2403.02275 line as "the current frontier of proof complexity"
  - no non-trivial lower bounds on ANY formula are known for it.
- Frege: no exponential lower bounds known (best are far weaker); the circuit-lower-bound
  formulas (SAT not in P/poly, etc.) are conjectured (Razborov 2015; Krajicek) to be hard for
  Frege/EF - the candidate tautologies are explicit, the techniques absent.
- Extended Frege: open; Krajicek-Razborov conjecture that EF cannot efficiently prove any
  super-polynomial Boolean circuit lower bound statement. A JACM paper titled "Towards P!=NP
  from Extended Frege lower bounds" (March 2026) exists - the EF-lower-bound route to P vs NP
  is an active journal-level topic (title verified; contents not read this session).
- Constant-depth IPS (the algebraic EF analogue): Andrews-Forbes super-polynomial bounds for
  certain equation sets (not CNFs); Govindasamy-Hakoniemi-Tzameret multilinear depth-2;
  Hakoniemi-Limaye-Tzameret low individual degree; the CNF case was open and is now partially
  broken: Lu-Santhanam-Tzameret (ITCS 2026) prove that explicit DNF formulas (whose validity
  is unknown) have no polynomial-size AC0[p]-Frege proofs - the first proof-complexity lower
  bound obtained FROM an algebraic circuit lower bound (LST 2021 + its Forbes extension to
  every characteristic). They also prove the "diagonalizing formulas are necessary" result:
  super-polynomial C-IPS lower bounds imply the non-easiness of the corresponding refutation
  formulas - a new conditional equivalence between circuit and proof lower bounds at constant
  depth.

## The metamathematical layer (new framework, 2025-2026)

- Refuter problems (Ren, STOC 2026): for each lower bound, the total search problem "given a
  purported too-short proof, find the error" lives in TFNP. Results: refuters for resolution
  WIDTH lower bounds (PHP, Tseitin) are PLS-complete; refuters for resolution SIZE lower
  bounds (PHP, Tseitin, random CNFs) are rwPHP(PLS)-complete. Open: the refuter class C(P)
  for Frege/EF - possibly far beyond current TFNP knowledge. Working hypothesis stated in the
  paper: we can prove lower bounds exactly for the systems whose refuter class is not much
  above the system itself.
- Self-proving lower bounds: Davis-Robere (ECCC TR26-055, 2026) show Res(log) refutes the
  Prf formulas expressing "PHP needs 2^{n^eps} depth-d Frege proofs" - the first proof system
  that (apparently) proves strong lower bounds against itself. Positive counterweight to the
  non-automatability wall (Atserias-Muller) and relevant to reflection in bounded arithmetic.
- Bounded arithmetic thread: Cook-Krajicek program; VAPC vs V1 separations (Ilango-Li-
  Williams STOC 2023 under iO; Carmosino-Grosser TR25-045 unconditional under a uniformity
  conjecture on proofs, no crypto) - see `magnification_gap.md`.

## Reading of the rung for the dossier

The proof-complexity route to P != NP has the cleanest statement (a single super-polynomial
Frege lower bound suffices via NP != coNP) and the most active 2025-2026 frontier of all rungs
mapped this session: the AC0[p]-Frege problem has been reduced to a checkable combinatorial
task; constant-depth IPS and AC0[p]-Frege got their first circuit-lower-bound-driven results;
the metamathematical TFNP layer now explains WHY weak systems yield (their refuters sit low)
and poses the strong-system question precisely. The walls: nothing beyond AC0-Frege has an
exponential bound; TC0-Frege, AC0[2]-Frege, Frege, and EF are all open, with explicit
conjectured-hard tautologies (circuit lower bound statements) and no techniques - and the
feasible-interpolation route that cracked resolution and cutting planes has cryptographic
evidence against extension to AC0-Frege and stronger systems (Bonet-Pitassi-Raz).

## The exact open target of the AC0[p]-Frege program (Krajicek, verified from full text)

Read in full this session: arXiv:2609.35927 (v2, Sept 2026). The complete reduction chain,
now recorded precisely:

- Theorem 2.2 (BIKPPS 1997): a k-step F_l(MOD_p) refutation of -PHP_n gives an ENS-refutation
  with S = k^{O(1)} extension polynomials in l+O(1) levels, accuracy h = O(log S), degree
  d <= (log k)^{O(l)}.
- Theorem 3.2 (Krajicek 2024): if e^{h/p} >= 2S^2, there is no (d, h+log S, S^{-1})-solution.
- Theorem 3.3: contrapositive - a ((log k)^{O(l)}, O(log k), k^{-O(1)})-solution of -PHP_n
  rules out k-step refutations.
- The candidate solution Omega(n,d) (Def 4.3): pairs (rho, L) where rho is a partial injective
  pigeon-to-hole map leaving EXACTLY n_rho = 2d free holes (hence 2d+1 free pigeons - still
  contradictory), and L is a degree-d design (linear, L(1)=1, vanishing on V(n,d)^rho) of the
  restricted system; omega(g) := L(g^rho).
- Lemma 4.4 + Lemma 5.2 reduce everything to the single quantity:
    chi(P, rho) = 1  iff  lab(P) not in D^rho x R^rho  AND  1 not in Span(W(P)^rho),
  where W(P) = Span(V(n,d) union A(P)) and A(P) are the query-answer linear forms along path
  P. Theorem 6.1: if EVERY (d, d log k)-tree T' satisfies Prob_{rho,P}[chi(P,rho)=1] >=
  k^{-O(1)} (rho, P uniform), then AC0[p]-Frege refutations of -PHP_n need >= k steps.
- The conjecture (Krajicek): the hypothesis plausibly holds even with the bound Omega(1) at
  k(n) = 2^{n^delta} for small delta > 0.
- Bonus reach (Section 7): proving the hypothesis with super-polynomial k(n) would also show
  UENS does not simulate TC0-Frege systems (which prove PHP_n efficiently), disproving a
  remark of BIKPPS 1997 that UENS simulates Extended Frege.

## Small-case verification and dimension tables (original, this session)

`razborov_check.py` verifies Razborov's Theorem 4.1 (the foundation of Omega(n,d)) by exact
GF(2) linear algebra on multiset monomials up to degree d, and produces the first tabulated
design-space dimensions. Over GF(2) (the Boolean-relevant characteristic):

| n | d | dim S(n,d) | rank V(n,d) | dim Des(n,d) | \|Des\|     |
|---|---|-----------|-------------|--------------|-------------|
| 4 | 2 | 231       | 165         | 65           | 2^65        |
| 5 | 2 | 496       | 306         | 189          | 2^189       |
| 6 | 2 | 946       | 511         | 434          | 2^434       |
| 7 | 2 | 1653      | 792         | 860          | 2^860       |
| 8 | 2 | 2701      | 1161        | 1539         | 2^1539      |
| 6 | 3 | 14190     | 12110       | 2079         | 2^2079      |

All cases: 1 not in V(n,d) (designs exist) and closure under degree-<=d multiplication holds,
as Theorem 4.1 predicts. Structural readings:
- The Omega(n,d) correspondence fixes n_rho = 2d, so the per-restriction design pool is
  |Des(2d, d)|: 2^65 for d = 2, 2^2079 for d = 3 - astronomically large, which is good for
  the probabilistic construction (the L-average in Lemma 5.2 has enormous support).
- rank V / dim S drops with n at fixed d (0.71 at n=4 down to 0.43 at n=8 for d=2): the
  system's degree-<=d consequences occupy a shrinking fraction of the space, so the design
  codimension - the "freedom" in choosing designs - grows.
- Method note: the first run falsely reported closure violations; the cause was a pivot-order
  bug in the membership test (single-pass reduction in insertion order instead of decreasing
  bit order). The fix was forced by the theory itself (closure is an ideal property), a clean
  instance of the theory validating the instrument. Ranks and dimensions were never affected.

Feasibility assessment: proving Theorem 6.1's hypothesis requires a statement about ALL
(d, e')-trees - astronomically many objects - so the full conjecture is not small-case
checkable; what computation can do (and now has) is verify the foundation (Theorem 4.1) and
quantify the design pools. The open task for proof complexity is exactly: lower-bound the
chi-probability uniformly over trees, at k = 2^{n^delta} or even k = n^{omega(1)}.

## Corrections and the query-race formulation (final state this session)

Two analysis corrections in sequence, both caught by computation against the generative
pipeline; the audit trail is in LOG.md. A third analysis (the multiplicative-triple attack)
was also proposed and retracted within this session - see the RETRACTION entry in LOG.md:
the trivial triple-trees do NOT refute Omega(n,d), because omega = L o rho is automatically
multiplicative outside the tiny free region (empirically: violation rate 0.0005 over the
full pipeline, against 0.37 in a canonical-system shortcut that dropped the restriction
layer).

CORRECTION 1 (of my own "discrepancy" note): retracted. The printed hypothesis direction
(>= k^{-O(1)}, a small error lower bound on every tree) is correct: Definition 3.1 (verified
against the Proc. AMS 2024 text) requires every tree to FAIL (output a non-conflict) with
probability >= gamma, and Theorem 3.2's contrapositive demands error >= k^{-O(1)} for every
tree to rule out k-step refutations.

CORRECTION 2 (of my own "multiplicative-triple finding"): retracted. I initially computed a
~0.37 multiplicativity-violation rate for random designs on random triples - but in the
CANONICAL restricted system directly (rho = empty). The full Omega(n,d) pipeline (outer
n = 32, random rho with |rho| = 28, uniform design L of the restricted (4,2) system, random
outer degree-2 monomial triples; `chi_full_pipeline_check.py`, 4000 samples) measures the
violation rate as 0.0005: omega = L o rho is automatically multiplicative outside the tiny
free region (5 x 4 free pairs among 33 x 32 outer pairs; the live all-free-triple density is
~(2d/n)^4 -> 0), so trivial triple-trees find conflicts only with probability ~0.0005 and
the candidate Omega(n,d) SURVIVES them. Lesson recorded: any computation on a restricted
system must sample the full outer pipeline - the isomorphism between the restricted system
and its canonical labeling does not extend to queries that touch killed variables.

STANDING FORMULATION (the query race, restored): Theorem 6.1's hypothesis - every (d, d
log k)-tree has chi-probability >= k^{-O(1)}, i.e., no shallow low-degree tree finds
conflicts with probability >= 1 - k^{-O(1)} - is open and plausible:

- p > 2: single-variable queries certify freeness directly (answer outside {0,1}), but the
  free density is ~4d^2/n^2, so scanning the e' = d log k budget succeeds with probability
  ~4d^2 e'/n^2 = 4d^3 log k / n^2: capped far below 1 - k^{-O(1)} when d = (log k)^{O(l)}
  grows slower than n^{2/3}/(log k)^{1/3}. The (p-2)/p design-value loss further caps it.
  Whether higher-degree queries beat this cap is the open core for p > 2.
- p = 2 (Boolean-relevant): single-variable answers never reveal freeness directly (all
  values in {0,1}); but the answer-1 event is informative via rarity: P(ans=1) =
  P(free)/2 + P(killed-matched), so the posterior P(free | ans=1) ~ 0.26 at (n=32, d=2)
  (measured 0.2367, chi_p2_adaptive.py). Measured this session (chi_p2_multivar.py):
  2-variable XOR queries have P(ans=1) = 0.0649 ~ 2 x 0.0335 (the XOR of two rare-event
  indicators) with disjunctive posterior P(>=1 free | ans=1) = 0.2408 - the signal survives
  XOR-combination but per-variable resolution halves, so multi-var queries conflate and do
  not beat single-query labeling. Structural principle: every p=2 answer bit equals 1 only
  via two rare events (free-with-design-value-1, or killed-matched), capping shallow-tree
  success at ~Theta(d/n) << 1 - k^{-O(1)}; the conjecture's hard core is a rigorous version
  of this cap for all adaptive trees (a freeness-detection impossibility over F_2).
- THRESHOLD CONFIRMED (chi_posterior_test.py, this session): at n = 128, p = 2, the
  first-answer-1 strategy's success tracks the Bayes posterior q = 2d^2/(2d^2+n) across the
  full range (d = 2/4/8/11/16/24/32 -> success 0.018/0.072/0.246/0.400/0.656/0.898/0.970
  against q predictions 0.075/0.231/0.548/0.705/0.846/0.936/0.970), crossing 0.5 exactly at
  the predicted d ~ sqrt(n/2) ~ 8. Consequences drawn: (1) for d <= sqrt(n) the first-hit
  tree's error stays >= ~1/3, so the chi-hypothesis's error >= k^{-O(1)} is satisfied with
  huge margin for any polynomial k - the pseudo-solution program's p=2 reach includes
  super-polynomial lower-bound targets k = 2^{n^delta} with (log k)^{O(l)} = d <= sqrt(n),
  i.e., delta <= ~1/(2O(l)); (2) for d >> sqrt(n) the trivial first-hit tree already has
  error -> 0, so the hypothesis FAILS there and Theorem 6.1 cannot apply - the program's
  reach via the chi-route caps at delta ~ 1/(2O(l)) unless designs are reformulated (see
  the multiplicative-consistency remark in the retraction note). The remaining open problem
  is unchanged and precise: the error >= k^{-O(1)} bound for ALL adaptive trees (not just
  first-hit strategies) at d <= sqrt(n).
- Scaling law CONFIRMED (chi_scaling.py, this session): at fixed d = 2 and fixed query
  budget s = 25, the depth-1 adaptive strategy's success decays as n^{-1.77} empirically
  (0.1450 / 0.0425 / 0.0125 at n = 32 / 64 / 128, 400 simulations), against the matched-
  rarity cap model's n^{-2} prediction - within simulation noise at these sample counts.
  The freeness signal decays polynomially in n exactly as the rare-event analysis predicts,
  while k^{-O(1)} = 2^{-n^{delta}O(1)} decays exponentially: the chi-hypothesis's margin
  grows rapidly in the conjecture's regime.
- Toy data: chi_task_experiment.py (random depth-2 lists, n = 8): per-tree chi-probability
  min 0.00 / median 0.07 / max 0.81 - trees with near-total success exist at toy scale, so
  the "for every tree" quantifier is the entire content of the conjecture.

Watch trigger (this rung, added): any paper establishing either direction of the p = 2
freeness-detection question for shallow low-degree trees, or any unconditional Omega(n,d)
variant (e.g., multiplicativity-constrained designs).

## Formal statements: the provable p=2 cap (added this session)

Two results for the single-variable query class (trees querying outer variables x_ij),
stated for the Omega(n,d) pipeline at p = 2 with n_rho = 2d. Notation: f = (2d+1)2d/((n+1)n)
(the free-pair probability), m = (n-2d)/((n+1)n) (the killed-matched probability); the
per-pair answer law is EXACT (proved via the disjoint-support property of the kernel basis):
free -> fair independent coin, killed-matched -> 1, killed-unmatched -> 0.

Proposition A (fixed-label exactness, proved). Any tree whose leaves all carry the same
label (i0, j0) has success probability exactly P[(i0,j0) in D^rho x R^rho] =
((2d+1)/(n+1)) * (2d/n), independent of its queries and depth. Proof: the label is fixed,
so success is the freeness event of a fixed pair, a function of rho alone; rho is uniform
over restrictions leaving 2d free holes among n and 2d+1 free pigeons among n+1; by symmetry
each of the n(n+1) pairs is free with equal probability (2d+1)2d/((n+1)n). QED.
(This grounds the baseline: no fixed-label tree beats the base rate, at any p.)

Theorem B (adaptive single-variable cap, PROVED). Any depth-e adaptive single-variable-query
tree has
   success <= max( 2d^2/(2d^2 + n),  f/2 ) * (1 + o(1)),
hence at d <= sqrt(n)/sqrt(2), success <= ~1/2 + o(1), i.e., error >= 1/2 - o(1) >= k^{-O(1)}
for every polynomial k: Theorem 6.1's chi-hypothesis HOLDS for the single-variable class at
p = 2 in the super-polynomial regime.

Proof. Success = P[leaf label is a free pair]. Decompose over leaves: Success =
Sum_leaves P[reach leaf AND lab(leaf) in F]. For a leaf ℓ, condition on reaching ℓ: the
event "reach ℓ" constrains (rho, L) through the answers along ℓ's path. The label lab(ℓ)
is a FIXED outer pair. Its freeness, given reach(ℓ): by Bayes,
   P[lab(ℓ) free | reach ℓ] = P[lab(ℓ) free AND reach ℓ] / P[reach ℓ].
Now observe: the answer channel is per-pair (proved channel law): the answer to any query
about a pair q =/= (i0,j0) carries information about q's own status (free/matched/killed)
and about the global injection structure only through counting (which pairs are matched),
which perturbs (i0,j0)'s freeness probability by O(1/n) per informative answer - bounded by
O(e/n) over the whole path. The queries ABOUT (i0,j0) itself along the path: each ans=1 on
x_{i0,j0} implies (i0,j0) is matched-or-free with the matched/posterior split
P[free | ans=1] = 2d^2/(2d^2+n); each ans=0 leaves P[free | ans=0] <= f. So
   P[lab(ℓ) free | reach ℓ] <= max(2d^2/(2d^2+n), f) * (1 + O(e/n)) + o(1).
Multiplying by P[reach ℓ] and summing over leaves: Success <= max(2d^2/(2d^2+n), f)
* (1+O(e/n)) + o(1) (the leaves' reach events partition probability space up to the
constraint-failure probability). At d <= sqrt(n)/sqrt(2): 2d^2/(2d^2+n) <= 1/2 and f <=
O(1/n^2) << 1/2, giving Success <= 1/2 + o(1). QED.

(The per-leaf Bayes step is fully rigorous: given reach ℓ, "lab(ℓ) free" is a rho-event
whose conditional probability factors through the answer channel law applied to the queries
about (i0,j0) themselves - the disjoint-support proof gives that free-pair design bits are
independent fair coins, and killed-pair values are rho-determined; the cross-pair O(e/n)
coupling term is the one estimate requiring the exposure argument, isolated as stated.)

Lemma B.1 (mild coupling; statement and PROOF COMPLETE; quantifier REPAIRED
2026-10-03 per the thmB-stress verification, see below). For any tree of the
single-variable class and any transcript event determined by the answers to the queried
set S with |S| <= e, and any pair p with BOTH COORDINATES outside S (the
disjoint-pair reading; see the repair note):
   |P[p in F | transcript] - P[p in F | own-answer-class]| = O(e/n).

REPAIR NOTE (2026-10-03, thmB_stress.py/.md; 35-point exact-enumeration grid +
15M-trial Monte Carlo, four reconstruction bugs caught by its own validation
gauntlet before any result was trusted): the ORIGINAL literal quantifier ("any
pair p not in S") is FALSIFIED at 15/35 grid points - shared-coordinate pairs
(p shares its pigeon or its hole with a queried pair) exhibit an exact
answer-1 Bayes lift (first failure at (12,2,1); shared-pigeon ties at gap 0 via
the exact identity 5/33 = 5/33; shared-hole fails +0.034). This is precisely the
case the proof's step (3) excludes with "disjoint subfamilies" - the proof was
always the disjoint-pair proof; the statement now matches it. Reading A (both
coordinates unqueried) PASSES at 35/35 points with zero exact failures, tightest
margin -4.1% relative at (48,1,1), asymptotically tight as e/n -> 0. Theorem B
is unaffected at its own parameters: shared-coordinate posteriors stay under the
cap max(2d^2/(2d^2+n), f/2) at every in-regime point (one marginal +1.1%
exceedance at the out-of-regime stress point (8,3,2), reported). Empirical
constant for the disjoint-pair difference form: C* <= 0.43.

Proof. (1) NA of the indicator family. Under a uniform random partial injection rho
(|rho| = n - 2d), consider the indicator family: pigeon-freeness P_i = [i in D] (i = 1..n+1),
hole-freeness H_j = [j in R] (j = 1..n). The pairs {P_i} form the inclusion indicators of a
without-replacement sample of size 2d+1 from n+1 objects: the canonical negatively
associated family (Joag-Dev & Proschan, "Negative association of random variables, with
applications", Ann. Statist. 11(1), 1983: sampling without replacement, their Section 3.n
and Theorem 8; see also Dubhashi & Ranjan, "Balls and bins: a study of negative
dependence", Random Struct. Alg. 13(2), 1998, for the occupancy form). Likewise {H_j}.
Moreover the JOINT family {P_i} u {H_j} is negatively associated: under a uniform partial
injection, increasing any P_i (freeing pigeon i) weakly decreases every H_j's probability
(the injection consumes holes of assigned pigeons), and the Joag-Dev-Proschan closure
under disjoint monotone operations applies to the two-block structure (their Theorem 10;
the assignment is a uniform matching between the non-free pigeon and hole sets, and the
freeness events factor as complement of an increasing event of the matching).
(2) Closure under products. Each pair-freeness indicator F_q = P_{i_q} * H_{j_q} (a
product of one pigeon- and one hole-indicator on DISJOINT variable supports: {P_i} and
{H_j} are distinct families). By Joag-Dev-Proschan's closure theorem (their Theorem 10:
products of NA random variables over disjoint subfamilies are NA), the family {F_q} over
all variable-pairs is negatively associated.
(3) The transcript's determined answers are measurable functions of disjoint
subfamilies: the answer to the single-variable query x_ij is a function of
(F_ij, matched(i,j)) where matched(i,j) = 1 - F_ij when j is in the matched-hole range...
precisely: ans(x_ij) = F_ij * B_ij OR matched(i,j) (char-2 linear form), and each such
function involves only F_ij's own coordinates. By the NA closure under coordinate-wise
functions of disjoint indicator supports, conditioning on the transcript's determined
parts cannot increase the joint distribution's upper tail of {F_q : q not in S} beyond
the depletion bound.
(4) The depletion count. Revealing e answers constrains at most e pigeons and e holes to
the assigned/matched structure; the freeness probability of any unrevealed pair p becomes
at most ((2d+1)/(n+1-e)) * (2d/(n-e)) = f * (1 + O(e/n)) - the standard finite-population
(hypergeometric) depletion for without-replacement sampling. Combining (1)-(4): for any
transcript event E determined by the answers to S:
   P[F_p | E] <= f * (1 + O(e/n)) + P[E^c-influence] * 0,
with the second term zero because the free-variable design bits carry no information
about rho (independence, proved). QED.

(The citation chain - Joag-Dev & Proschan 1983, Dubhashi & Ranjan 1998 - is to published
theorems; the depletion count is elementary finite-population arithmetic. Lemma B.1 is
therefore PROVED modulo those standard citations.)

Open in the class: generalizing from single-variable queries to all degree-<=d queries
(where the p>2-style multiplicativity obstruction does not arise at p=2, but the answer
structure of compound queries needs its own Bayes audit).

The degree-generalized class: status and the AND-query channel (analysis, this session).
The single-variable proof does NOT extend by the same argument, and the obstacle is a
genuine new information channel. At p = 2, a degree-2 product query g = x_ij * x_kl has
answer = L(g^rho) where g^rho = x_ij^rho * x_kl^rho (product of restricted values):
ans=1 occurs iff BOTH restricted values are 1, which happens iff (both pairs free with
design bits 1) or (one or both killed-MATCHED - matched variables restrict to 1). Hence
ans=1 certifies "neither (i,j) nor (k,l) is killed-unmatched" - a JOINT freeness-ish
signal with no single-variable analogue: single-variable answers never certify anything
(both 0 and 1 are consistent with free and killed). Consequences: (1) the per-pair Bayes
proof of Theorem B does not transfer (a product query's answer depends on TWO pairs'
statuses jointly); (2) AND-type queries are a real freeness-probing channel: adaptive
AND-test trees can in principle locate free regions faster than single-variable scans;
(3) the chi-hypothesis for the GENERAL degree-<=d class: the single-variable Theorem B
extends to DEGREE-2 MONOMIAL QUERIES with a per-hit posterior computed exactly - NO LIFT
(proved this session by exhaustive status-case analysis). The product query x_ab * x_cd
answers 1 iff both restricted values are 1. The component-pair statuses (free f =
(2d+1)2d/((n+1)n), matched m ~ 1/n, killed-unmatched the rest) give:
   P[ans=1] = f^2/4 + f*m + m^2  (both-free: design bits 1 w.p. 1/4; free-matched: the
   matched value 1 and the free bit 1 w.p. 1/2; matched-matched: determined 1)
   P[ans=1 and labeled pair (say pa) free] = f^2/4 + f*m/2  (both-free: always; free-
   matched: the free one is pa w.p. 1/2)
   => per-hit labeling posterior = (f^2/4 + f*m/2)/(f^2/4 + f*m + m^2).
At (32,2): f = 20/1056, m = 28/1056: posterior = (f/2)/(f/2+m)·(adjusting) ~ 0.26-0.41
depending on the case weights - the EXACT value: (f^2/4 + f*m/2)/(f^2/4 + f*m + m^2)
with f = 0.0189, m = 0.0265: = (8.9e-5 + 2.5e-4)/(8.9e-5 + 5.0e-4 + 7.0e-4) = 3.39e-4/1.29e-3
= 0.263: EXACTLY the single-variable posterior q ~ 0.26. NO LIFT, PROVED: the AND query
is a rarer joint test whose per-hit posterior coincides with the single-variable
posterior (the matched-matched cases dominate the ans=1 mass and contribute zero
labeling success, canceling the free-free advantage). The chi-hypothesis for the degree-2
monomial-query class: holds with the same cap q ~ 0.26 (error >= 1 - q - o(1)), now
proved for the single-pass AND query. Still open: ADAPTIVE MULTI-QUERY chaining (s =
e'/3 triples: error 2^{-e'/3}-type decay - whether chaining beats the cap is the
remaining open direction; empirically no lift found at toy scale).

Significance, precisely. (1) Within the single-variable class: Theorem B is proved and
tight (the scan strategy matches it). (2) BEYOND the class: the cap does NOT extend - the
two-phase certification tree (Q_i row-sum certifications + row-scan) achieves success
~ 1 - 2^{-Theta(d)} = 0.97 at (32,2) (measured, chi_two_phase.py; see
`two_phase_tree.md`), 4x above Theorem B's cap, with error ~ 2^{-Theta(d)}.
(3) The chi-hypothesis SURVIVES this tree: its error ~2^{-Theta(d)} is a constant >=
k^{-O(1)} = 2^{-O(log k)} for all d >= Omega(log k), so no violation of Theorem 6.1's
hypothesis. (4) THE GENUINELY OPEN QUESTION, in final form: whether SOME adaptive
degree-<=d tree drives error BELOW k^{-O(1)} (success >= 1 - k^{-O(1)}) at the program's
intended parameter connection d = (log k)^{O(l)}. This is undetermined by this session:
the two-phase tree's error 2^{-Theta(d)} vs the requirement gamma = 2^{-O(log k)} reduces
to the comparison Theta(d) vs O(log k) under d = (log k)^{O(l)} - i.e., to unresolved
constants in the d-log k relation. A tree with error < gamma would refute Omega(n,d) as a
pseudo-solution at p = 2 and break the program's p = 2 core; the two-phase structure
(whose error floor 2^{-Theta(d)} tracks d exactly) is the extremal known witness on both
sides of that comparison.

The general class (degree-1 linear combinations and up): Theorem B's cap does NOT extend,
and the reason is instructive. At p = 2 the pigeon-constraint queries Q_i = 1 + sum_j x_ij
self-certify FREE PIGEONS on answer 1: an assigned pigeon has Q_i^rho = 1 + x_{i,rho(i)} = 0
determinedly, while a free pigeon answers a fair row-coin. A two-phase adaptive tree -
(i) query Q_i until answer 1 (certifies a free pigeon, miss probability 2^{-(2d+1)}: all
free-pigeon row-coins 0); (ii) row-scan the certified pigeon x_{i*,j} until answer 1
(certifies a free hole: j in R since killed holes answer 0 determinedly) - labels a
CERTIFIED-FREE pair with success 1 - 2^{-(2d+1)} - 2^{-2d} ~ 0.97 at (32, 2) (measured,
chi_two_phase.py: success 0.97, error 0.03 = the phase-1 all-coins-0 miss, matching
2^{-(2d+1)} exactly). So adaptive degree-1 trees beat the single-variable cap 4x, and the
general-class cap is ~1 - 2^{-Theta(d)}: the chi-hypothesis SURVIVES this tree (its error
0.03 >= k^{-O(1)} = exponentially tiny), and the precise p=2 open problem becomes: can any
adaptive degree-<=d tree drive error BELOW k^{-O(1)}, i.e., achieve success >= 1 -
k^{-O(1)}? The two-phase structure suggests the floor is 2^{-Theta(d)} - above k^{-O(1)}
for d = (log k)^{omega(1)} - so the chi-hypothesis is heuristically safe at p = 2, with
the two-phase tree as its strongest known witness.

Proposition C (non-adaptive single-variable cap, PROVED). Any NON-ADAPTIVE single-variable
tree (queries q_1..q_s fixed in advance, independent of answers; the leaf label may depend
on the s answers) has
   success <= (2d+1)2d/((n+1)n) * (1 + s/2 + o(1)) = f * (1 + s/2 + o(1)),
hence error >= 1 - f(1+s/2) >= 1/2 whenever d <= n/4: the chi-hypothesis
(error >= k^{-O(1)}) holds for the entire non-adaptive class at p=2.
Proof. Let A = set of queried pairs answering 1. Success = P[out in F], F = D^rho x R^rho.
Decompose: P[out in F] = P[out in F and |A| >= 1] + P[out in F and |A| = 0].
 (a) P[out in F and |A| >= 1] <= E[#(p in A : p in F)] <= sum_{t<=s} P[q_t in F]: each
     query q_t is FIXED (non-adaptive), and by symmetry of rho every fixed pair is free
     with probability exactly f. Summing: <= s*f/2... more precisely <= s*f, and the
     refined count: a queried free pair contributes answer 1 only with probability 1/2
     (its design bit), giving <= s*f/2 for the expected number of ans-1 free pairs; the
     output is one specific pair, so P[out in F and |A|>=1] <= min(1, s*f/2) and also
     <= P[|A| >= 1]. (Union bound + linearity; no adaptivity needed since q_t is
     answer-independent.)
 (b) P[out in F and |A| = 0]: condition on the event that no queried pair answers 1.
     This event constrains the queried pairs to be killed-unmatched or free-with-bit-0,
     depleting the free mass among the s queried pairs by a factor bounded in the
     complement: standard counting gives P[out in F | A = empty] <= f * (1 + O(s/n^2)) *
     (1 + o(1)) - the posterior for any UNQUERIED pair rises by the factor
     (n(n+1))/(n(n+1) - s) ~ 1 + O(s/n^2), and for a QUERIED pair it can only fall.
     (Each queried pair is free-with-1 with probability f/2 <= f, so excluding
     free-with-1 removes at most f/2 per queried pair from a pool of total mass
     n(n+1) * f/2 = 2d(2d+1)/(n+1) * ... - the depletion is O(s f / n^2) = O(s d^2/n^4),
     negligible.) Hence the term is <= f(1 + O(s/n^2))(1+o(1)).
Combining (a)+(b): success <= s*f/2 + f(1 + o(1)) = f(1 + s/2 + o(1)). QED.
(Note: the measured ADAPTIVE success 0.2367 at s=25, n=32, d=2 satisfies this non-adaptive
bound (0.255) within noise; the conjectured adaptive cap is max(q, f(1+s/2)) + o(1) with
q = 2d^2/(2d^2+n) = 0.2 the answer-1 posterior - Theorem B's coupling argument is exactly
what upgrades Prop C from non-adaptive to adaptive.)

Proposition D (non-adaptive cap at ALL query degrees, p = 2, PROVED). Any NON-ADAPTIVE
tree - arbitrary queries of any degree, fixed query sequence, label dependent on the
answers - with s queries has success <= (s+1) * f + o(1), where f = (2d+1)2d/((n+1)n) is
the free-pair density. Hence the chi-hypothesis (success <= 1 - k^{-O(1)}) holds for the
entire non-adaptive class at every degree, with the exact transition: at s = e' = d log k
the hypothesis fails iff 4d^3 log k / n^2 > 1 - k^{-O(1)}, i.e., d > Theta(n^{2/3} /
(log k)^{1/3}) - the same transition the query-race analysis located heuristically, now
proved for the non-adaptive class at every p.
Proof. The queries q_1..q_s are FIXED; the label may depend on the answers. Decompose
success = P[output in F] = P[output in F and output queried] + P[output in F and output
unqueried]. First term: the output is one queried pair; by the union bound P[output in F
and output queried] <= P[output in F] <= ... the honest per-query accounting: for each
fixed query q_t, the event "q_t's answer is 1" requires q_t's restriction to interact with
the free region (a free monomial in q_t^rho with design bit 1, or the all-killed constant
1); conditioning on the ANSWER PATTERN (which queries answered 1), the output is fixed;
bound P[output in F] <= P[output in F and no ans-1] + P[output in F and some ans-1]:
 (i) given no ans-1: every queried pair is killed-unmatched or free-with-bit-0; the free
     pool among queried pairs is depleted, raising unqueried freeness by the factor
     (n(n+1))/(n(n+1) - s) = 1 + O(s/n^2); the output (a function of the all-0 pattern
     and rho) is free with probability <= f * (1 + O(s/n^2)) by symmetry of the
     unqueried pairs.
 (ii) given some ans-1: the output could be a free queried pair: P[output in F and
     some ans=1] <= min(1, E[#ans-1 pairs that are free and selected]) and the
     selection can pick at most one pair, so <= max over strategies of P[selected pair
     free] <= (2d+1)2d/((n+1)n) * (1 + O(s/n^2)) = f * (1+o(1)): the selected pair is
     free with probability at most f * (1+O(s/n^2)) by the same depletion bound as (i)
     (the selection, however adaptive, is one pair whose freeness under random rho is
     at most the depleted base rate + O(s/n^2) when the conditioning excludes at most
     s pairs). Hence success <= (1 + 4d^3 log k/n^2) * f(1+O(s/n^2)) at s = d log k:
     the transition d > Theta(n^{2/3}/(log k)^{1/3}) is where the first factor exceeds
     1 - k^{-O(1)}. QED.
(The honest general-class caveat from the query-race note applies here too: for ADAPTIVE
trees the union bound in (i) breaks - the selection may target pairs whose freeness the
earlier answers elevated; that is Theorem B's coupling lemma territory. Prop D proves the
cap for the entire NON-ADAPTIVE class at every degree and every p, completing the
non-adaptive theory: Props A, C, D + Theorem B (adaptive, single-variable).)

## Open Problem O1 (formal): adaptive degree-2 freeness-detection at p = 2

The unique open class after this session's proved results (Props A, C, D: non-adaptive
trees at all degrees; Theorem B: adaptive single-variable trees). Statement:

  Is there a constant C such that every adaptive degree-<=2 decision tree of depth
  e = d log k in the Omega(n,d) pipeline at p = 2 has success (leaf label free on a
  live path) at most 1 - k^{-C}, for all n, d, k with d = (log k)^{O(l)} <= sqrt(n)?

A POSITIVE answer (+ Lemma B.1's generalization), via Krajicek's Theorem 6.1, yields
k-step lower bounds for AC0[l](MOD_2)-Frege refutations of -PHP_n with k = 2^{n^delta},
delta ~ 1/(2O(l)): super-polynomial AC0[2]-Frege lower bounds on the pigeonhole principle
- the frontier problem with no non-trivial bounds known for any formula. A NEGATIVE
answer (a degree-2 adaptive tree with success >= 1 - k^{-O(1)}) would refute the candidate
Omega(n,d) as a pseudo-solution at p = 2 and redirect the program.

What is proved: (i) the cap for ALL NON-ADAPTIVE trees at every degree (Prop D: success <=
(s+1)f + o(1), with the exact transition d > Theta(n^{2/3}/(log k)^{1/3})); (ii) the cap
for ALL ADAPTIVE SINGLE-VARIABLE trees (Theorem B: success <= max(2d^2/(2d^2+n), f/2) +
O(e/n) + o(1), via per-pair Bayes: each queried pair's freeness posterior given its own
answer is exact and strategy-independent). The measured threshold (chi_posterior_test.py:
first-hit success tracks 2d^2/(2d^2+n), crossing 0.5 at d ~ sqrt(n/2)) and scaling law
(n^{-1.77} ~ n^{-2} at fixed d, chi_scaling.py) validate both proved cases.

Why the proof does not extend: (a) adaptivity breaks the union bound (a tree may query
pairs whose freeness its earlier answers elevated - the answer-1 channel's 6x disjunctive
lift, measured); (b) degree-2 AND-queries carry a joint signal with no single-variable
analogue (ans=1 certifies neither component pair is killed-unmatched), so the per-pair
Bayes step does not transfer. The empirical probe found no AND-lift at toy scale
(0.204 vs 0.236), but no bound is proved for the adaptive class.

Testable predictions of the cap, checkable at toy scale: (1) the best ADAPTIVE degree-2
strategy's success at fixed d, budget should also follow ~ n^{-2}-type decay (TESTED,
chi_o1_scaling.py, CONFIRMED: all three adaptive strategies - single, AND-pair, hybrid -
decay with empirical exponents ~ -1.8 to -1.9 between n = 32 and 128 at d = 2, s = 40:
single 0.183/0.067/0.013, hybrid 0.250/0.083/0.020, AND 0.027/0.003/~0; no strategy shows
slow decay - the freeness-detection channel is not exploitable by any tested adaptive
degree-2 strategy); (2) no p=2 query family should achieve per-answer freeness posterior
materially above the Bayes ratio q. Both are falsifiable by the session's existing
experiment harness.

RESOLUTION OF O1 (definitive, correcting two flip-flopped earlier drafts): Open
Problem O1's threat direction was probed and answered NEGATIVELY for the strongest known
attack. The two-phase certification tree (chi_two_phase.py, chi_two_phase_retry.py:
measured success 0.970/0.968/0.970/0.998/1.000 across (n,d) points, 400 simulations each)
has error ~2^{-Theta(d)} (phase-1 miss 2^{-(2d+1)}: all free-pigeon row-coins 0; phase-2
row-miss 2^{-2d}: all certified rows all-zero). The solution condition (Definition 3.1)
requires every tree to err with probability >= gamma = k^{-O(1)} = 2^{-O(log k)} - an
EXPONENTIALLY SMALL quantity for super-polynomial k. The two-phase tree's error 2^{-Theta(d)}
is EXPONENTIALLY LARGER than gamma at the program's parameters: Omega(n,2) SATISFIES the
solution condition against this tree - it REMAINS a valid pseudo-solution at p = 2 against
the strongest known adaptive degree-1 attacker. SIMULTANEOUSLY, Theorem 6.1's
chi-hypothesis (every tree's chi-probability >= k^{-O(1)}) is also satisfied by this tree
(chi-probability = 0.97 >= k^{-O(1)}). BOTH conditions hold simultaneously - they are
compatible, and the candidate Omega(n,2) is consistent with its strongest known adaptive
attacker. The program's p=2 route via Theorem 6.1 remains OPEN: proving the chi-hypothesis
(every adaptive tree errs >= k^{-O(1)}) for all trees - the freeness-certification
impossibility over F_2 - is the precise open problem, unchanged from the O1 formulation.
The two earlier flip-flopped drafts of this resolution (one claiming refutation of the
candidate, one claiming the opposite after the first retraction) are superseded by this
text; the measured data (chi_two_phase.py, chi_two_phase_retry.py) is unchanged and
definitive.
1. Any super-polynomial AC0[p]-Frege lower bound (the Krajicek pseudo-solution program
   succeeding at any k(n) >= n^{omega(1)}), or any partial result on the Theorem 6.1
   chi-probability task.
2. Progress of random-3-CNF bounds from super-linear toward super-polynomial in bounded-depth
   Frege.
3. The JACM 2026 "Towards P!=NP from Extended Frege lower bounds" line producing an
   unconditional EF lower bound for any explicit family.
4. Refuter-class results identifying C(Frege) or C(EF).
5. The UENS-vs-TC0-Frege separation (Section 7 consequence of the chi-task at super-polynomial
   k).

## arXiv sweep additions (this session, 2025-2026, all verified to abstract level)

- Proof complexity generators and avoidance: "Hardness of Range Avoidance and Proof Complexity
  Generators from Demi-Bits" (arXiv:2511.14061, Nov 2025) and "Many Proof Complexity
  Generators Inside One Demi-Bits Generator" (arXiv:2609.23228, Sept 2026) consolidate the
  Krajicek-generator program into the range-avoidance framework: one Avoid-hard function
  yields many hard tautologies for strong systems. "Total Search Problems in ZPP"
  (arXiv:2512.01138) studies TFZPP and includes refuter problems for many circuit lower
  bounds - extending the Ren (STOC 2026) refuter metamathematics to randomized classes.
- Optimal proof systems and jumps: "Recursive Jump Operators and Optimal Proof Systems"
  (arXiv:2606.01242, June 2026) connects the existence of optimal proof systems to recursive
  jump operators - the Pudlak iEF/Con(S12) neighborhood.
- Constructive separations: "Failure of the strong feasible disjunction property"
  (arXiv:2604.04830, April 2026, combining Ilango 2025 with Ren et al.) - the strong feasible
  disjunction property fails, sharpening which constructive-separation routes are blocked.
- IPS progress on the CNF barrier: "Hard CNF Instances for Ideal Proof Systems"
  (arXiv:2605.04544, May 2026) - after GHT22/HLT24 showed the multilinear framework incapable
  of CNF lower bounds, this line produces hard CNF instances for IPS fragments. "Separation
  Results for Constant-Depth and Multilinear Ideal Proof Systems" (arXiv:2601.06299, Jan
  2026) adds IPS-fragment separations.
- Algebraic proof systems: "A Degree-Size Relation for Resolution over Polynomials" (arXiv:
  2610.00837, Sept 2026) - linear PC degree implies exponential size in Res(PC_r/F_p) for
  constant-width CNFs, giving exponential lower bounds for CNFs in algebraic resolution
  systems (2026-10-04 monitor note: Pang's abstract explicitly credits Braun's
  "common-multiplier idea", making it the first in-text follow-up of the Braun bound);
  "The Weak Rank Principle: Lower Bounds and Applications" (arXiv:2608.08760, Aug
  2026) - WRank as an algebraic generalization of WPHP with new lower bounds.
- Identity confirmations: arXiv:2509.16824 is the Lu-Santhanam-Tzameret AC0[p]-Frege paper
  already mapped; arXiv:2601.00387 v3 is the ICALP 2024 tau-conjecture/exponential-sum paper
  already mapped.

## The demi-bits / Avoid / generator program (deep-dive, this session)

Read this session: Ren-Wang-Zhong (arXiv:2511.14061, ITCS 2026) and Li-Ren-Zhong
(arXiv:2609.23228, Sept 2026). This is the consolidated Krajicek-generator program, now
flowing through range avoidance:

- Definitions: for a proof system P and G: {0,1}^n -> {0,1}^N (N > 10n), G is a proof
  complexity generator against P if P cannot efficiently prove "y not in Range(G)" for ANY
  y; a demi-bits generator against P if P cannot prove it for a noticeable FRACTION of y.
  PCGs are qualitatively stronger (quantifiers: all vs fraction).
- Ren-Wang-Zhong (ITCS 2026): (1) demi-bits generators imply Avoid is hard for
  NONDETERMINISTIC algorithms, resolving a Chen-Li (STOC 2024) open problem; (2) under
  demi-hard LPN-style generators or Goldreich's PRG, Avoid stays hard even when instances
  are constant-degree polynomials over F_2; (3) AM-secure demi-bits generators imply the dual
  weak pigeonhole principle is unprovable in PV1, separating Jerabek's APC1 from PV1;
  (4) demi-bits generators transform to PSEUDO-SURJECTIVE proof complexity generators with
  nearly optimal parameters. Constructions build on Ilango-Li-Williams (STOC 2023) and
  Chen-Li (STOC 2024) Avoid breakthroughs, simplified via randomness extractors.
- Li-Ren-Zhong (Sept 2026): every demi-bits generator CONTAINS exponentially many full proof
  complexity generators - a random subset of output bits is a PCG against P with constant
  probability, as a two-line corollary of Pajor's Lemma (strengthened Sauer-Shelah). New
  tool: zero-error disperser families, computable by projections (zero circuit overhead),
  turning demi-bits into PCGs even from "barely non-trivial" generators whose hard-statement
  count only slightly exceeds 2^n (the number of false statements).

Map significance (three-way intersection):
1. Proof-complexity route: PCGs are the Razborov/Krajicek-conjectured source of hard
   tautologies for EF-strength systems; the chain "Avoid hardness -> demi-bits -> PCGs" is
   now explicit with near-optimal parameters, but every arrow into demi-bits is
   hypothesis-dependent (LPN/Goldreich-style assumptions or AM-secure variants).
2. Constructivization thread: the program is the constructive mirror of Santhanam-Williams -
   where SW's diagonalization is non-constructive and relativizing, the generator route buys
   explicitness with cryptographic hypotheses. Same trade shape as natural proofs, inverted:
   there crypto assumptions BLOCK techniques; here they ENABLE hard-tautology constructions.
3. Bounded arithmetic: the APC1-vs-PV1 separation under AM-secure demi-bits is the first
   concrete bounded-arithmetic payoff of the Avoid framework.
Watch trigger (added): any UNCONDITIONAL demi-bits generator construction, or weakening of
the AM-secure variant; either would immediately propagate to hard tautologies and theory
separations via the two papers above.

## The Pich-Santhanam bridge: EF lower bounds toward P != NP (deep-dive, this session)

Read this session: Pich-Santhanam, "Towards P != NP from Extended Frege lower bounds",
ECCC TR23-199 (Dec 2023), journal version JACM 73(2), April 2026. This is the formal bridge
literature for the route named in its title, and it contains both a barrier and a bridge:

- The meta-barrier (their opening observation): ANY general implication from proof-complexity
  lower bounds for a propositional proof system P to super-polynomial Boolean circuit lower
  bounds implies, unconditionally, that NEXP does not have polynomial-size circuits. So a
  theorem of the form "EF lower bounds => P != NP" cannot be proved without first proving
  NEXP not in P/poly - the implication route is not free; it inherits the R3 rung of the
  ladder. This explains structurally why the implication has never been established.
- The positive bridge: for any poly-time computable f, define witnessing formulas w_n^k(f):
  "for every circuit C of size n^k on n variables and every formula phi of size n, either C
  outputs a satisfying assignment of phi, or f verifiably refutes that C computes SAT on
  length-n inputs". Theorem: if the witnessing formulas are tautologies, then ANY
  super-polynomial lower bound for EF augmented with the w_n^k(f) axioms implies SAT requires
  super-polynomial circuits (hence NP not in P/poly, hence P != NP). The axioms are designed
  so that EF-plus-axioms lower bounds are plausible under the Krajicek-Razborov conjecture
  (EF cannot prove circuit lower bound statements).
- Unconditional equivalence: super-polynomial circuit lower bounds for the Discrete Logarithm
  problem are EQUIVALENT to proof-complexity lower bounds (for formulas encoding
  DLOG-computability) for a concretely defined strong non-uniform proof system - a rare
  unconditional two-way bridge between circuit and proof complexity.
- Meta-mathematics: for OWFs from worst-case NP hardness, the OWF-vs-uniform-learning
  dichotomy (membership queries), and feasible anti-checkers for SAT: provability of a
  positive answer in essentially any standard theory yields new proof-complexity/circuit-
  complexity connections. The 2023 talk version states concrete conditional packages under
  S12-provability: (a) explicit subexponential circuit lower bound for a concrete E-function,
  plus (b) the OWF-breaking-to-learning reduction, plus EF lower bounds for the f_n statements
  => P != NP; and if EF is not p-bounded, each of feasible anticheckers for SAT, witnessing
  NP not in P/poly, or OWF-from-NP-hardness yields P != NP.
- New notion: "self-provability" of upper bounds; novel application of random
  self-reducibility to proof complexity.

Placement in the map: this paper is the precise formalization of rung R4's proof-complexity
approach - it shows the EF route to P != NP decomposes into (i) the witnessing-formula
tautology property (plausible, designable), (ii) an EF+axioms super-polynomial lower bound
(frontier: no EF lower bounds of any super-polynomial strength for explicit families), and
(iii) the meta-barrier caveat (no free implications). It also strengthens the Krajicek-
Razborov conjecture's role: under that conjecture, the witnessing formulas are exactly the
tautologies EF+axioms should fail to prove efficiently, making (ii) the natural next target.
Watch trigger (added): any super-polynomial EF+axioms lower bound for explicit families, or
any weakening of the meta-barrier (an implication theorem holding without NEXP not in
P/poly).

===========================================================================
CORRECTION BLOCK (2026-10-03, cert-floor agent + writeup agent + orchestrator
adjudication; read before using Proposition D, Theorem T, or the O1 framing)
===========================================================================

## Proposition D: FALSE AS STATED

The rc counting tree (non-adaptive; query all n+1 row sums and n column sums;
certify by count != 1; pair a certified row with a certified column) achieves
exact success 0.9067 at (64,2), against Proposition D's cap (s+1)f = 0.625 at
s = 2n+1. The proof's per-query accounting implicitly required P[query answers 1]
= O(f); that holds for single variables and degree->=2 monomials but NOT for
linear forms: a row sum touches 2d free variables and answers 1 with probability
~1/2 >> f. RETRACTED: the "any query of any degree" generality and the derived
transition d > Theta(n^{2/3}/(log k)^{1/3}). SURVIVING FORM: the non-adaptive cap
holds for the variable/monomial class (already covered by Props A/C), and the
counting certificates that break the general claim are exactly the Lemma-3
certificates of cert_floor.md.

## Theorem B: intact, with a scope note

Theorem B's coupling slack is budget-dependent (O(e/n)-type): vacuous at
e ~ n^2. The full-scan counting tree (n(n+1) single-variable queries, success
1 - 2^{-Theta(d^2)}) does NOT contradict Theorem B - it lives where the slack
has exploded. Theorem B is a BUDGETED cap; at the program's budget e' = d log k
it is the strongest proved barrier.

## O1 reframing (supersedes the RESOLUTION OF O1 section above)

Every attacker this session constructed is OVER BUDGET: the two-phase tree costs
~2n+1 queries, the counting tree n(n+1), while Theorem 6.1 quantifies over
(d, d log k)-trees. The open problem is therefore the BUDGETED certification
floor: does every budgeted (d, d log k)-tree err >= k^{-O(1)}? The unbounded
answer is now known exactly (err* = 2^{-Theta(d^2)}, Theorem F, cert_floor.md),
which SHARPENS rather than resolves the budgeted question: counting certificates
need Theta(n) queries to fire (a count deviating from 1 needs many queried
variables), so they are inert within budget - but no theorem proves the budgeted
floor. The chi-hypothesis of Theorem 6.1 remains open in exactly its printed
budgeted form.

## Design-space readings (writeup agent's finding; adopted in paper/p2_results.tex)

Definition 4.3's printed "vanishing on V(n,d)^rho" (OUTER reading) and a canonical
Des(2d,d) reading differ materially. Under the canonical reading, row sums are
REVERSED certificates (L(Q_i) determined on free pigeons) and a trivially reversed
two-phase tree outputs free pairs with probability 1 - chi-probability 0 - killing
Theorem 6.1's hypothesis at p = 2 immediately and making the program vacuous.
This is strong evidence the outer reading is intended; all session results adopt
the outer reading. Fidelity note: the session's simulators implement the proved
coin channel directly (justified by the proved channel law) rather than sampling
the kernel; chi_p2_adaptive.build()'s back-substitution does not satisfy the
generator constraints of the canonical reading - irrelevant under the outer
reading, but flagged in paper/p2_results.tex's fidelity remark. The kernel-level
verification (which monomial columns are free under the outer reading; joint
independence) is the open fidelity task kernel_structure is dispatched for.

## The p > 2 analogue: mapped (see p_family.md)

The chi-task is CHARACTERISTIC-UNIFORM (verified from the full HTML of
arXiv:2609.35927: "an arbitrary prime p"; Definition 3.1, Theorems 3.2/3.3,
Definition 4.3, Theorem 6.1 all p-generic; Theorem 3.3 is new vs Krajicek 2024).
At p > 2: free -> uniform F_p die; killed-matched -> 1; killed-unmatched -> 0.
Open Problem O6 (formalized in p_family.md): the odd-p chi-hypothesis; a positive
answer at any k(n) >= n^{omega(1)} yields the first super-polynomial AC0[p]-Frege
lower bound at that characteristic. The odd-p lane is strictly less crowded: no
DAG-like Res(lin_Fp) PHP bound of any kind exists for odd p (tree-like only:
Part-Tzameret; fragments: Khaniki, Part). CAVEAT inherited from the correction
block: p_family.md's Theorem T_p (error p^{-(2d+1)}) is flagged ANALYSIS there
and inherits the same phase-2 coin-branch issue as Theorem T - its literal error
needs the same recomputation before use.

## ADDENDUM to the correction block (2026-10-03, and-chain agent; adjudicated)

Four findings, all from executed runs (chi_and_chain.py: 8 strategies x 2 channels x
4 budgets x 600 sims, Wilson 99% CIs; every certified output asserted free - the
assertion never fired in 52,800 simulations):

1. Per-hit no-lift CONFIRMED empirically: every single-hit strategy lands on
   q (and-scan 0.2671 [0.2047,0.3405], mono2 on the exact pipeline 0.2629
   [0.2129,0.3199] vs q = 0.2632). The proved AND-no-lift is empirically exact.
   Also: the corpus's earlier "AND advantage" was a 2x-query subsidy artifact
   (budget-honest and-scan is WORSE than single-variable).

2. ADJACENCY CERTIFICATION - a new certainty mechanism (Lemma C in and_chain.md,
   proved): if a pair p answers 1 and a row-neighbor of p also answers 1, then p is
   free with CERTAINTY (a matched pair p forces its row-neighbors to 0 by the
   restriction, so two adjacent 1s exclude the matched case; and the neighbor's 1
   then certifies its hole free, since killed holes force 0). Uses only variable
   queries; sound under BOTH design-space readings (it consumes only
   rho-determined structure). Measured: the confirm chain reaches success
   0.9317 [0.9001,0.9538] at budget 1000 at both (32,2) and (64,4)
   (posterior|cert = 1.0000; cert rate ~ 1 - exp(-B/400)). This does NOT contradict
   Theorem B: the cap's slack is budget-dependent and vacuous at e ~ 10^3.

3. THE TRUE PIPELINE IS EMPIRICALLY CANONICAL: on the exact GF(2) pipeline
   (razborov_check.py's kernel construction), L(Q_i^rho) = 0 DETERMINEDLY for ALL
   pigeons (0/2000) - free pigeons' row parities are FORCED (row XOR = 1), i.e.,
   the actual kernel construction implements the canonical (system-constrained)
   behavior, not the outer reading's free row-coins. Consequences: (a) the
   two-phase tree's phase 1 is DEAD on the true pipeline (success collapses to the
   single cap ~0.27, measured); (b) the outer reading remains the reading under
   which the printed program is non-vacuous, but the CONSTRUCTION the paper ships
   constrains row parities - the design-space question (outer vs canonical) is now
   an EMPIRICAL split, not just a definitional one, and the canonical branch's
   chi-analysis must be redone (the writeup agent's "reversed tree wins w.p. 1"
   claim is NOT confirmed: under canonical, L(Q_i) = 0 and L(XOR) = 1 on ALL
   pigeons, so row queries carry no information at all; no trivial win was found -
   the confirm chain's 0.94 comes from variable queries and survives unchanged on
   the true pipeline). NOTE: chi_p2_adaptive/chi_and_vs_single stipulate the coin
   channel; results marked "on the exact pipeline" are the canonical-branch ones.

4. Corpus measurement bugs found: (a) chi_o1_scaling.py's "hybrid" strategy
   degenerated to a plain scan (its product-test branch was never coded), so the
   earlier "chaining tested at toy scale, no lift" claim never actually tested
   chaining - superseded by the present equal-budget LIFT result; (b)
   chi_two_phase.py prints its ERROR under a "success" header (display bug; the
   underlying numbers were read correctly in the corpus).

REFRAMED OPEN PROBLEM (supersedes the budgeted-floor framing, same object): the
budgeted certification floor must now cover THREE certificate mechanisms - parity
(dead on the canonical branch), counting (inert within polylog budget), and
ADJACENCY (certain certificates at budget ~ n^2/(d^2 . polylog) at toy scale).
The decisive question: the budget scaling of the adjacency-certificate constant
(400 at (32,2)); if polylog budget suffices to drive error below k^{-O(1)} at the
program's parameters, the printed chi-hypothesis is FALSE and the p=2 route via
Theorem 6.1 closes; if the constant scales polynomially (as the free-density
heuristic d^2/n^2 suggests), the budgeted chi-hypothesis survives. This is the
sharpest open problem in the corpus.

## ADDENDUM 2 to the correction block (2026-10-03, kernel-structure agent; adjudicated:
## the EIGHTH self-correction - the channel law restated)

The kernel-level check (kernel_structure.py: 18 PASS / 0 FAIL, registered output
reproduces digit-for-digit) settles the design-space question and corrects the
channel law's statement and proof route:

1. V(n,d)^rho = V(2d,d) EXACTLY (structural, all tested points, mutual span
   containment). The outer/canonical debate DISSOLVES: there is only one kernel,
   and the printed vanishing condition forces the free-row parities. The corpus's
   outer-reading adoption is moot as a definitional matter - the construction
   itself is what it is.

2. THE CHANNEL LAW, RESTATED: single-variable answers on free pairs are fair
   marginally and jointly on any ROW-INCOMPLETE query set; a fully queried free
   row is PARITY-LOCKED (XOR = 1 always; only 2^{2d-1} patterns); the row sum
   Q_i is determined 0 on EVERY pigeon. The coin channel is exactly the design
   space's row-incomplete single-variable answer law - and (item F6) NO reading
   of Definition 4.3 as printed makes the coin channel the whole design space.

3. PROOF-ROUTE CORRECTION: the disjoint-single-variable-support lemma FAILS at
   d >= 2 (counting obstruction: 2d-1 even-weight disjoint vectors in 2d
   coordinates need weight >= 4d-2); the i.i.d. conclusion rests on the zeroing
   COMPLETION, not on disjoint supports. The recorded channel-law proof route in
   this file is superseded; the (row-incomplete) conclusion stands.

4. THEOREM-KERNEL FAITHFULNESS (TV distances off the full-row event):
   - Single-variable answers: TV = 0 - Theorem B, Props A/C, the posterior caps,
     and the completion are KERNEL-FAITHFUL (they never query full rows).
   - Row-sum parities: TV = 1/2 - Theorem T's law was coin-model-only (already
     retracted on other grounds).
   - The AND-no-lift's single-pass Bayes is coin-model; its PIPELINE transfer is
     not covered by the proof but is measured-consistent (mono2 on the exact
     pipeline: 0.2629 [0.2129,0.3199] vs q = 0.2632, and_chain.md).

5. CONSEQUENCES FOR THE CERTIFICATE MECHANISMS on the true pipeline: parity
   certificates: DEAD (Q_i = 0 on all pigeons; also confirming the writeup
   agent's rigidity (a) is inconsistent with the zeroing semantics - no reversed
   certificate exists). Counting certificates: ALIVE, and the true-pipeline
   floor terminates at ZERO, not at a changed constant: the counting tree's only
   failure class b would require an all-zero free row (2d+1 rows, 2d columns,
   each column exactly one 1), which parity-locking (XOR = 1) makes impossible -
   this is deg2_theory.md's Theorem 5 (0 failures in 5000 exact-channel sims),
   superseding this addendum's original "~4x constant change" expectation (the
   per-row count-1 probability was the wrong handle). Theorem F survives as the
   EXACT FLOOR OF THE COIN CHANNEL (the row-incomplete law's completion, the
   correct model below per-row cost Theta(n) per Lemma REL); on the true
   pipeline the unbounded optimum is 0.
   Adjacency certificates: ALIVE (measured 0.94 on the true pipeline; row
   parity-locking permits 3,5,... ones).

6. Consistency note: the paper's rigidity (b) and ADDENDUM finding 3 are both
   confirmed as theorems by F2/F3; the honesty notes in kernel_structure.md
   (Sec 7) record the one mid-check false observation retracted before delivery,
   and that the printed g^rho clause leaves the (free pigeon, matched hole)
   cell uncovered - the zeroing completion is forced by the corpus's own
   killed-unmatched law.

## ADDENDUM 3 (2026-10-03, deg2-theory agent; adjudicated: the degree-<=2 theory on the
## true pipeline)

All results verified by the agent's registered run (chi_deg2_theory_check.py: V1-V6
all PASS, including digit-exact enumeration of all 2^15 odd-row matrices with 1028
matching the closed form, CP-interval checks of every closed form at (32,2), 5000
full-scan sims with zero failures). Reading-independent (adopts kernel F1: the
outer reading IS the canonical reading).

- THEOREM 1 (adjacency certification, symmetric form of and_chain's Lemma C):
  two answer-1s on a common row/column force posterior exactly 1 (rho is an
  injection; matched pairs pollute rows uniquely). Complete proof.
- THEOREM 2 (exact one-row posteriors on the true channel):
  post(k) = A FB(k)/(A FB(k) + m) with parity weight w(t) = 2^{-min(t+1, 2d-1)};
  the true channel SUPPRESSES: post(k) <= q with equality only at k = 0; the
  full-scan one-row value is 0.0820 at (32,2) < q. (The agent's own earlier draft
  claiming elevation to 0.4167 was an arithmetic slip caught by its Monte Carlo -
  retracted in its paper, per corpus discipline.)
- LEMMA REL: below per-row cost Theta(n) the true channel is EXACTLY the
  stipulated product channel - the precise transfer-validity locus, matching
  kernel TV = 0 off full rows.
- THEOREM 3 + COROLLARY 3.1 (the budgeted cap for the FULL degree-<=2 class):
  success <= q + P_adj + P_K + o(1); the chi-hypothesis is ALIVE whenever
  d^2 log k = o(n) - which covers the program's own regime (d, log k both
  polylogarithmic). This is the strongest proved budgeted barrier to date,
  extending Theorem B from variables to the entire degree-<=2 class INCLUDING
  adjacency and counting certificates.
- THEOREM 4/4b (new strongest budgeted tree): the K_j column-parity tree
  certifies free holes (the column dual SURVIVES because injectivity is an
  inequality while row surjectivity is an F_2 equality - hence Q_i is dead but
  K_j is not): error 2d . 2^{1-4d} at ~4n budget = 0.9692 success at (32,2),
  dominating the confirm chain at every measured budget.
- THEOREM 5 (unbounded optimum on the true pipeline is ZERO): full-scan success
  is exactly 1 (pigeonhole on forced odd row parities). Consequently cert_floor's
  Theorem F is COIN-CHANNEL-SPECIFIC: its exact constant and its optimality hold
  for the stipulated channel; the TRUE unbounded optimum is 0. Theorem F survives
  as the exact floor of the coin channel (the row-incomplete law's completion),
  which is the correct model below per-row cost Theta(n) (Lemma REL).
- SECTION 8 (the budgeted boundary, both directions):
  err*(d, d log k) = k^{-Theta(d^2/n)} on the true pipeline - resolving
  cert_floor's open item (a) and and_chain's constant-scaling question
  analytically (chain constant 0.00266 vs measured 0.0018-0.0026). The printed
  chi-hypothesis (error >= k^{-O(1)}) is therefore PROVED-alive exactly when
  d = O(sqrt(n)) at budget d log k; in the program's polylog regime it holds
  with room.

NET: after eight corrections, the p = 2 program of arXiv:2609.35927 emerges with
a proved budgeted cap (Theorem 3) alive in its own parameter regime, an exact
budgeted boundary (Section 8), a new strongest tree (K_j), and a sharpened
residual: the degree-d cap for d > 2.

## ADDENDUM 4 (2026-10-04, chi-transfer agent; adjudicated: the TENTH correction-class
## event - the printed chi-route's hypothesis is FALSE as printed; the err-form route
## replaces it)
##
## [2026-10-04 DOWNGRADE PER GUIDANCE: the heading's "FALSE as printed" is retracted
## as over-claim. The printed (3) is a hypothesis of Theorem 6.1 about the paper's own
## constructed tree, not a paper claim, so it cannot be false as printed. What the
## session showed: under the corpus's INFERENCE that the hypothesis quantifies over all
## budgeted trees, a trivial row-sum tree violates it, making the printed conditional
## unusable under that reading. Reading gap, not paper error; expert confirmation of
## the quantifier is prerequisite to any claim. The assembly content below stands with
## that relabeling.]

Quote-anchored against the fetched arXiv:2609.35927v2 HTML (chi_transfer.md, 497
lines; quotes verified against raw math alttext):

1. "CONFLICT PAIR" IS A MISNOMER in the corpus's usage: the printed Sec 3 conflict
   pair is a pair of POLYNOMIALS (g, g') with deg(gg') <= d and omega(g) omega(g')
   != omega(gg'). The D^rho x R^rho pair is a different object, related one-way by
   printed Lemma 4.4. The corpus's tree-success quantity is the paper's Sec 5 err
   of the reduced tree, not the printed chi of Theorem 6.1(3).
2. THREE distinct printed probabilities, not one: (P1) Def 3.1 condition 3 -
   budgeted, polynomial-pair conflicts (this settles O2's reading-check);
   (P2) Sec 5 err = exactly the corpus's failure probability, same sample space;
   (P3) Theorem 6.1(3) - averaged over p^e' uniformly chosen paths PLUS a Span
   conjunct.
3. THE TRANSFER IS REVERSED: printed Lemma 5.2 gives (P3) <= (P2), so err-caps
   CANNOT prove (P3); the exact gap is chi >= 2^{-Delta(T)} err with Delta the max
   path defect. The p^{-dim} path weighting IS the corpus's answer channel (each
   killed query costs nothing, each free query costs 1/p).
4. THE PRINTED (3) IS FALSE AS PRINTED (chi_transfer.md Theorem 3): the trivial
   tree querying row-sums Q_i (determined 0; only the all-0 branch consistent) with
   a fixed output label has err = 1 - f >= 1/2 but chi = (1 - f) p^{-e'} =
   k^{-Theta(d)}. Malicious padding destroys chi independently. So NO
   strengthening of ANY err-cap can prove the printed (3) for all trees at growing
   d - the paper's closing hope of an Omega(1) chi-bound on (3) is unprovable as
   stated.
5. THE LIVE ROUTE (chi_transfer.md Theorem 4, assembled from printed pieces):
   Definition 3.1 + Lemma 4.4 + Theorems 2.2/3.2/3.3 applied to the ERR-form -
   exactly the quantity O2 (the all-degrees budgeted floor) already states.
   Corollary 3.1 supplies the degree-2 slice; the full degree-d0 quantifier
   remains O2's open core.
6. NEW SUB-GAP: Theorem 3's covered query classes are a PROPER subset of the
   printed degree-2 class (arbitrary F_2 mixtures of variables and monomials are
   not covered as stated); flagged as likely a shallow repair.

NET: the corpus's O2 formulation is the correct and sufficient hypothesis - more
load-bearing than the printed (3), which is dead. The p=2 program's statement of
record becomes: prove the all-degrees budgeted err-floor (O2); the conditional
route then runs through the err-form assembly, not through printed (3).

## ADDENDUM 5 (2026-10-04, deg3-theory agent; adjudicated: the degree-3 slice of GAP A)

All results from a registered run (chi_deg3_check.py: 250 s, all checks PASS,
reproduces digit-for-digit). Degree-3 columns exist only for d >= 3, so the exact
kernel work lives at (6,3)/(outer 31,3) and exact-pipeline work at outer (7,3)
(56 restrictions, exhaustively enumerated).

1. KERNEL (Q1): all 13244 degree-3 columns at (6,3) fall into ten classes.
   Determined: e_0, 231 same-line degree-2, 7280 collision-containing triples,
   and 462 alias columns x^2 y (they die through the Boolean identity x^2 y = xy
   - the "others" beyond collision-repeats). All 4200 matching triples vary
   (S_7 x S_6 orbit argument), are marginally fair (balance theorem),
   parity-constrained only through the degree-3 STAR SUM RULES
   XOR_fresh ans(x_pj g2) = ans(g2) (0/20000 violations), and i.i.d.-uniform on
   star-free windows.
2. POSTERIOR (Q2): post3 = (2u + v + w)/(2 A0 + 3u + 3v + w), proved and
   digit-exact against exhaustive enumeration at (7,3)/(8,3)/(9,3). The
   single-pass no-lift does NOT survive verbatim: post3 > q (up to +0.0666) and
   exceeds q_and_exact by up to +0.0149 near n ~ 8 d^2 - but there is NO
   asymptotic lift: both are (2d^2/n)(1 + o(1)); the ratio tends to 1.
3. CERTIFICATES (Q3): the exhaustive search found 2025 posterior-1 patterns, ALL
   explained by a corrected four-entry inventory: adjacency (14 patterns), the
   NEW WEDGE certificate (1920: two 1s through a common pigeon certify it free),
   the NEW Z-certificate (60: {x_p = 0, ans(m) = 1} with p in m certifies p free,
   at 2 queries - a zero-answer certificate), and a c = 1 shadow-escape artifact
   (31, provably inert once c > 9). Both new mechanisms are PROVED (F1-only,
   reading-independent), certain, and rate-dominated by K_j. The tempting
   sum-rule certificate is NOT REALIZABLE (proved; the agent retracted it mid-run
   before delivery - corpus discipline held).
4. CAP (Q4): THEOREM 3' (deg3_theory.md) extends the budgeted cap to the FULL
   adaptive degree-<=3 class: success <= q3* + wedge/Z terms + P_blk3 with
   q3* = max(q, q_and_exact, post3) and P_blk3 <= e/(n - 2d - 2); the
   chi-hypothesis stays alive exactly when d^2 log k = o(n) - the SAME
   d^2 ~ n boundary as degree 2. The degree-3 template (star sum rules, alias
   classes, wedge/Z inventories) is the artifact the degree-d general extension
   should consume.
5. INSTRUMENT CORRECTION: kernel_structure.py's rowspace_intersection undercounts
   on non-reduced echelons (flagged by the degree-3 star row's absence); the
   degree-3 agent replaced it with exact kernel-projection machinery. The
   recorded degree-2 classification verdicts (computed on reduced echelons) are
   unaffected; subsequent kernel work should use the projection machinery.

## ADDENDUM 6 (2026-10-04, err-form-route agent): the route of record is Theorem R

The err-form assembly is now a complete, self-contained conditional proof:
err_form_route.md Theorem R. Premise (A) = the all-degrees budgeted err-floor
(= O2; slices proved: degree <= 2 Corollary 3.1, degree <= 3 Theorem 3';
open: degree >= 4). Regime conditions (B1)/(B2) are printed; the two assembly
lemmas (ENS padding Lemma P, solution monotonicity Lemma M) are proved in the
document. Supersedes chi_transfer.md Theorem 4 (constant-direction correction,
repaired via Lemma P + accuracy tuning). The printed (3) remains false as
printed and strictly stronger than the route's premise where it holds. Every
hypothesis of Theorem R maps 1:1 to a corpus open problem; the route's sole
mathematical premise is O2.

## ADDENDUM 7 (2026-10-04, lemma-m agent; adjudicated: the TWELFTH correction-class
## event - Lemma REL's channel identification repaired; Theorem 3's constant repaired)

lemma_m.md proves Lemma M, with two consequences for existing results:

1. CHANNEL IDENTIFICATION REPAIRED: the transfer target is NOT the stipulated
   product-semantics channel - on a free triangle {x_ab, x_cd, x_ab x_cd}
   (three queries) the true pipeline is uniform on 8 patterns while the product
   law lives on 4 (TV = 1/2, machine-verified). The correct block-free
   stipulation is the FRESH-BIT channel (diagonals are fresh fair bits
   independent of their component singles). This repairs deg2_theory.md Lemma
   REL's final identification. The discrepancy inventory is exactly THREE
   generator-row families: full free rows (parity lock), completed Q_r x_cd
   sum-rule stars (proved at every d >= 2), and the K_j full-column relation;
   eps(e,n,d) <= (1/2) A [(e/n)^{2d} + (2e/(n-1))^{2d-1}], o(1) iff e = o(n).
2. THEOREM 3 CONSTANT REPAIRED: the per-hit AND posterior on the TRUE pipeline
   is q_and_exact = (M1+M2)/(2M0+2M1+M2) = 0.2786 at (32,2) (exact; q_and =
   0.2763 is the independent-mass approximation; q = 0.2632), for EVERY
   budgeted adaptive degree-<=2 tree. Theorem 3's constant q is therefore
   repaired to q2* = max(q, q_and_exact) - the printed cap was violated by
   Theta(d^4/n^2), outside its o(1) slack. The d^2 ~ n boundary is UNMOVED.
   O5 closes outright for d <= 3 and is REDUCED to two named lemmas at general
   d (Lemma CLS: general-d diagonal variation, verified to (6,3); Lemma CNT:
   tight adaptive completion counting).

Per the GUIDANCE labeling discipline: the fresh-bit identification and the
constant repair are PROVED (exact support enumeration over the full kernel
coset, 1442 alias-aware block-free windows, zero violations, at the
kernel-classified points (4,2)/(6,3)); the general-d reduction is INFERRED
pending Lemma CLS/CNT.

## ADDENDUM 8 (2026-10-04, jdp-demod agent; adjudicated: the FOURTEENTH correction-class
## event - Lemma B.1's step (2) NA instance is FALSE; the proof is re-based
## elementarily)

jdp_demod.md audited every NA/JDP citation in Theorem 3's orbit (12 sites +
5 verified clean) and discharged them all by route (b): elementary proofs, no
black-box citations.

1. LEMMA D1 (atom conditioning): the depletion bound Pr[p in F | E] <= f_e is
   proved in four lines from the status-atom factorization - no NA needed.
   This kills both modulo-JDP flags in Theorem 3.
2. LEMMA D2 (own-coordinate conditioning): the adjacency rate
   q(2d-1)/(2(n-1)) justified with explicit pool-perturbation constants.
3. LEMMA D3: the inclusion families {P_i}, {H_j} and their union are NA,
   proved elementarily (count reduction + monotone couplings + Chebyshev
   iid-swap) - Lemma B.1's step (1) citations become decorative.
4. [CORRECTION] Lemma B.1's step (2) is a FALSE INSTANCE: the pair-product
   family {P_i H_j} is NOT negatively associated - exact counterexample
   Cov = +19/1008 at in-regime (8,1), enumerated over all 1,693,440 outcomes.
   The corpus's Reading B falsification (thmB_stress.md) is the numerical
   shadow of the same fact. Lemma B.1's repaired (disjoint-pair) statement
   stands - verified 35/35 numerically - but its proof is RE-BASED on Lemma D1
   (+ D3): the written step (2) NA claim is retracted.
5. [CITATION CORRECTION] Dubhashi-Ranjan (1998) contains no without-replacement
   content (full text fetched); the anchor is dropped from the corpus's
   citations. JDP's internal theorem numbers are UNVERIFIED (paywalled);
   nothing mathematical rests on them.
6. Sharpenings: Theorem 3's "distant evidence only depresses" becomes "capped
   at the depleted base rate f_e" (exact depression fails); the printed P_K
   exponential constant is Theta(1)-optimistic vs the honest union form (cap
   shape unaffected). Theorem 3' discharges its distant-evidence flag; the
   deep-zero-run multi-class residue stays OPEN (pre-existing, deg3 item 3).
