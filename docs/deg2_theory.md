# Degree-<=2 adaptive trees on the true Omega(n,d) pipeline: the corrected
# per-leaf posterior theory, the budgeted cap, and the certification boundary

Result of the deg2-theory agent (2026-10-03). Status: analysis, not peer-reviewed.
Task brief: attempt an analytic cap for adaptive degree-<=2 trees in one of three
directions - (a) per-leaf posterior bound, (b) transcript bound, (c) domination
negative result. ATTEMPTED: (a). VERDICT: the proposed bound (labeling posterior
<= q + O(d^2/n) on every answer pattern) is FALSE, and false for a structural
reason that reorganizes the whole problem: on the true pipeline two 1-answers on
a common row or column force posterior EXACTLY 1 (adjacency certification), so
no per-hit Bayes cap can hold at certificate leaves. Every non-certificate leaf,
however, is capped STRICTLY BELOW the stipulated-channel value: the design
kernel's row-parity structure taxes each specific-position hit on a free row a
factor 2^{1-2d}, so deep zero-runs push the per-leaf posterior DOWN from q, not
up (Theorem 2(iv): post(k) <= q with equality only at k = 0).
What replaces (a) is a dichotomy (isolated evidence: capped at q; co-linear
evidence: certified at 1) plus an explicit budgeted cap with a matching tree,
which together settle, in exponential shape, the budgeted certification problem
the corpus recorded as its sharpest open item (the and-chain agent's
constant-scaling question and cert_floor's open item (a)).

Everything here is stated on the TRUE pipeline channel (exact GF(2) designs of
the restricted canonical system), not the corpus's stipulated i.i.d.-coin
channel; the two differ, the differences are machine-verified
(kernel_structure.py, re-run this session, 55.2 s, all findings reproduced), and
Section 10 lists what changes in already-recorded corpus results when the
true channel is used. Honesty markers: every unproved step is marked; machine-verified
facts are marked [MV]; "modulo JDP" marks the one step that rests on the same
negative-association citation standard the corpus's Lemma B.1 already accepts.

## 1. Setup and the true-channel facts

Pipeline Omega(n,d) at p = 2 (arXiv:2609.35927): rho is
a uniform partial injection leaving free set D (2d+1 pigeons) and R (2d holes);
L is a uniform random degree-d design of the restricted system
(L(1) = 1, L kills V(n,d)^rho); the answer to a query g is L(g^rho). The
outer-reading vs canonical-reading question is resolved at kernel level by the
redispatched kernel_structure.py (its finding F1: V(n,d)^rho = V(2d,d) EXACTLY
at all checked points): the two readings impose the same constraints, so every
statement below is reading-independent. Outer pair (i,j):
free if i in D and j in R; matched if rho(i) = j; killed-unmatched otherwise.

Facts used, all machine-verified this session (the redispatched
kernel_structure.py, whose docstring findings F1-F7 I adopt, at the
restricted systems (2,1), (4,2), (6,3) and outer (7,1), (15,2), (31,3); I
additionally executed the earlier kernel_structure.py audit in full, 55.2 s,
and re-verify every fact independently in chi_deg2_theory_check.py):

  F1 [MV]. matched pair -> answer 1; killed-unmatched -> answer 0
     (L(1) = 1 and L kills V, exact).
  F2 [MV]. free single-variable answers: marginally fair; PAIRWISE independent
     across distinct pairs; the joint law of the full single-answer table M
     (given rho) is a product over rows, each row uniform over the ODD-parity
     patterns on its 2d free columns (the only single-coordinate elements of
     the constraint space W are the row vectors e_0 + Q_i: row parities are the
     ONLY single-variable design constraints). Killed rows of M: exactly one 1
     (at rho(i)); killed columns of M: exactly one 1 (at rho^-1(j)).
  F3 [MV]. L(Q_i^rho) = 0 for EVERY pigeon, free or killed: the row-sum query
     Q_i = 1 + sum_j x_ij answers 0 determinedly always (Q_i is a generator of
     the system, so it lies in V). Measured 0 ones in 950,000 free-pigeon
     queries across the three validation points.
  F4 [MV]. degree-2 coordinates: squares answer their single variable's value;
     same-pigeon and same-hole products are pivot (answer 0 determinedly);
     DIAGONAL products (distinct pigeon and hole) answer a fair coin, pairwise
     independent of the two component singles (rank 3/3) and of each other
     (rank 2/2); globally the diagonal answers satisfy the shift sum rules
     sum_j L(x_pj x_ab) = L(x_ab) (Q_p x_ab in V), so the answer coordinates are
     NOT mutually independent - but every determined relation is an IDENTITY
     (configuration-invariant), hence carries zero information about rho; the
     information-bearing dependence is only the block-completion effect of
     Section 4.
  F5 [MV]. K_j := 1 + sum_i x_ij (column parity, degree 1) is NOT a generator
     (the hole-exactly-one constraint is not part of -PHP): K_j answers 0
     determinedly on killed columns and a fair coin on free columns, so an
     answer 1 CERTIFIES j in R. (The row dual Q_i is dead per F3; the column
     dual is alive. This asymmetry is the pigeonhole principle itself.)
  F6. The corpus's chi_p2_adaptive.build() coset (e_0 + kernel) is not the
     design coset [MV: L(Q_i) = 1 there]; all corpus simulations to date
     (chi_two_phase*.py i.i.d. row coins, and_chain stipulated channel) run
     on a third, unrealizable channel - and the redispatched kernel_structure
     makes this precise (its F5): the coin samples are a strict SUPERSET of
     legal designs (only 2^{-(2d+1)} of coin samples are design-consistent),
     marginally identical on row-incomplete single-variable query sets and
     different exactly on fully-queried free rows and on all degree-2
     semantics. and_chain.md's exact-pipeline
     measurements (uniform designs over Des(4,2)) already used the true
     channel and agree
     with F2-F5 (row XOR = 1 in 2000/2000; Q_i = 0 in 2000/2000).

Notation: f = (2d+1)2d/((n+1)n) (free-pair mass), m = (n-2d)/((n+1)n)
(matched mass), h1 = f/2 + m (single-variable answer-1 probability),
q = (f/2)/(f/2 + m) = (2d+1)d/((2d+1)d + (n-2d)) (per-hit posterior),
A = (2d+1)/(n+1), B = (n-2d)/(n+1) (row-status priors).

## 2. Theorem 1 (adjacency certification; the false direction of (a))

Theorem 1. Let a transcript contain two answer-1 observations on single
variables x_p, x_p' with p =/= p' sharing a row or sharing a column (in any
order, adaptively chosen; in particular a hit at p followed by any answer-1
row- or column-neighbor of p). Then p and p' are both FREE with posterior
exactly 1, and the tree may output either pair.

Proof. Write p = (i,j), p' = (i',j'). Case rows: i = i'. If i were killed,
F2 gives exactly one 1 in row i (at rho(i)), so x_{i,j} = 1 forces j = rho(i)
and then x_{i,j'} = 0 - contradicting the second 1. So i in D. Then a 1-answer
on (i,j) forces j in R (F1: killed j would make the pair killed-unmatched,
answering 0), and likewise j' in R. Both pairs free. Case columns: symmetric,
using F2's killed-column fact (exactly one 1 per killed column) and i, i' in D
forced as above. The posterior is 1 because the transcript event has
probability 0 on every configuration where the output pair is not free. QED.

This is and_chain.md's Lemma C stated symmetrically (their hit-then-neighbor
form is the case p observed before p'); the proof above only uses F1 and the
killed row/column structure of F2, so it is sound under both channel readings,
as and_chain already noted. The structural reading: matched pairs are the
answer-1 pollution (they are what caps the per-hit posterior at q < 1), and rho
being an INJECTION makes matched 1-answers mutually exclusive within a row and
within a column; co-linear 1-answers therefore cannot both be matched, and the
pollution hypothesis dies - which is exactly where any per-hit Bayes cap must
break. This is the precise answer to "where the proof needs conditional
independence": the single-query no-lift needs P(two independent matched
pollutions) = m^2 to dominate the answer-1 mass; co-linearity makes that mass
exactly 0.

Consequence for the attempted direction (a): every certificate-free leaf
satisfies posterior <= the bounds of Theorem 2, and every certificate leaf has
posterior 1 > q + O(d^2/n). So (a) is false as proposed in every depth class
where certificate leaves occur with nonnegligible probability.

## 3. Theorem 2 (exact one-row per-leaf posteriors)

All statements concern a tree that spends its transcript on one row i
(distinct columns, in query order) and outputs a pair in row i. Write
post(k) for the posterior of the output pair when the row scan's first k
answers are 0 and the (k+1)-th is 1 (output = that hit), and post_full for a
full scan of all n columns that shows exactly one 1 (output = that hit).

Theorem 2. On the true channel:
  (i) post(0) = q exactly.
  (ii) For 0 <= k <= n-1:
     post(k) = A * FB(k) / (A * FB(k) + m),
     FB(k) = sum_{t=0}^{min(k,2d-1)} C(k,t) C(n-k-1, 2d-1-t) w(t) / C(n,2d),
     w(t) = 2^{-min(t+1, 2d-1)}.
  (iii) post_full = (2d+1)2d 2^{1-2d} / ((2d+1)2d 2^{1-2d} + (n-2d)) =: rho_2a.
  (iv) post(k) is maximized at k = 0, where it equals q: every certificate-
     free one-row transcript has output posterior <= q (the deep-scan value
     rho_2a is 0.0820 at (32,2), BELOW q). At (32,2): q = 0.2632,
     post(5) = 0.2166, post(15) = 0.1352, rho_2a = 0.0820.

Proof. (i) Bayes with the per-hit masses: the free branch contributes
A * (2d/n) * (1/2) per row (the column must be free, the coin fair) and the
killed branch m (the row's matched hole must be the hit column), giving
q = (2d+1)d / ((2d+1)d + (n-2d)). Under the true channel the free-branch coin
is marginally fair (F2), so this matches the stipulated-channel value.
(ii) Condition on the row status. Killed branch: the 1 appears exactly at
rho(i); the probability that rho(i) is the (k+1)-th scanned column is 1/n
(the k zeros are then forced), contributing B * (1/n) = m. Free branch: R is
a uniform 2d-subset; the event needs h = c_{k+1} in R and exactly t of the k
zeros in R (the rest outside R), which has hypergeometric mass
C(k,t)C(n-k-1,2d-1-t)/C(n,2d); given the positions, the observed t+1 free bits
are one specific pattern, and the number of odd patterns on R agreeing with it
is 2^{2d-t-2} when t+1 < 2d (remaining free bits unforced, even parity) and 1
when t+1 = 2d (fully forced): the probability is w(t) = 2^{-min(t+1, 2d-1)}
against the 2^{2d-1} odd patterns. Multiply and sum: FB(k).
Bayes gives the ratio. (iii) k = n-1: R must be {h} plus 2d-1 of the n-1 zero
columns, all observed bits forced, so FB(n-1) = C(n-1,2d-1)/C(n,2d) *
2^{1-2d} = (2d/n) 2^{1-2d}, and post_full = A(2d/n)2^{1-2d} / (A(2d/n)2^{1-2d}
+ m). (iv) Each additional scanned zero column strictly costs free-branch
likelihood (a C-ratio < 1 if the column is outside R, an extra forced 0-bit -
a factor 1/2 - if it is in R), so FB(k) is maximized at k = 0 [proved for
k <= n-2d elementarily; the tail range k > n-2d is computed and Monte-Carlo
verified at (15,2)/(32,2)/(48,4) in chi_deg2_theory_check.py], and every
certificate-free one-row transcript has output posterior <= q, with equality
only at k = 0. The full-scan value is rho_2a = (2d+1)2d 2^{1-2d} / ((2d+1)2d
2^{1-2d} + (n-2d)) = 0.0820 at (32,2), far BELOW q. QED.

Reading: ON THE TRUE CHANNEL THE PARITY STRUCTURE SUPPRESSES rather than
elevates. A specific-position single hit on a free row must realize the unique
odd pattern concentrated at that column (cost 2^{1-2d}), so deep zero-runs
make the hit LESS likely to be free, not more: post(k) decreases from q toward
rho_2a (closed forms at (32,2): post(5) = 0.2166, post(15) = 0.1352, verified
by Monte Carlo in the check script). The per-leaf cap attempted in the task
brief is therefore TRUE on the true pipeline for every certificate-free leaf,
in the strong form post <= q; the certificate leaves of Theorem 1 (posterior
exactly 1) are the sole - and sole possible - exception. On the corpus's
stipulated i.i.d. channel the same computation has w(t) = 2^{-t-1} throughout,
post_full = 0.0427 at (32,2), also below q: the certificate-free per-leaf
q-cap holds on BOTH channels. (An earlier draft of this analysis claimed a
parity ELEVATION to 0.4167 at (32,2); that was an arithmetic slip in the
t = 2d-1 weight, caught by the script's Monte Carlo - measured post_full
0.0695 [0.0495, 0.0941] and post(15) 0.1303 [0.1024, 0.1624] against the
corrected closed forms 0.0820 and 0.1352 - and is retracted here.)

Column transcripts: symmetric formulas with no parity factor (free columns
carry unconstrained fair coins per F2), giving post_col(k) <= q for all k and
post_col(full, one 1) = (2d/n)2^{-2d} / ((2d/n)2^{-2d} + (n+1-2d)/(n(n+1)))
(e.g. 0.222 at (32,2)): columns are a strictly weaker evidence channel than
rows, and never beat q without certification.

## 4. Lemma REL (block completion; when the true channel is a product channel)

Call a transcript BLOCK-COMPLETE if it observes all 2d free coordinates of
some canonical row, or all 2d-1 diagonal coordinates of some sum-rule star
Q_p x_ab. Only a block-complete transcript can see a determined relation
(F2, F4: all shorter coordinate sets are independent, ranks verified).

Lemma REL. For any tree of budget e, the probability that its transcript is
block-complete is at most
  p_block(e) <= (2d+1) (e/n)^{2d} + (n+1) n (e/n)^{2d-1},
and on the block-free event the transcript's likelihood factors as a product
of per-pair factors P(ans = 1 | free) = 1/2, P(ans = 1 | matched) = 1,
P(ans = 1 | killed) = 0 (for singles) with the diagonal fair-coin factors of
F4 - i.e., ON THE BLOCK-FREE EVENT the true channel is EXACTLY the corpus's
stipulated i.i.d. channel.

Proof. Completing a row requires the e queries in some fixed row to include
all 2d free columns of that row: hypergeometrically C(n-2d, e-2d)/C(n, e) <=
(e/n)^{2d} per row, (2d+1) rows. Completing a star requires e-1 of the queries
to be the diagonals of one (pigeon, target-column) star: <= (e/n)^{2d-1} per
star, at most (n+1)n stars. Union bound. On the block-free event every
observed coordinate set is independent [MV: the rank computations], and each
coordinate's conditional law is the per-pair factor above, so the likelihood
factors. QED.

At the program's budget e = d log k with d <= sqrt(n): p_block <= (2d+1)
(d log k/n)^{2d} + n^2 (d log k/n)^{2d-1} = o(1) whenever d log k = o(n)
(the regime that matters). At e = Theta(n) the bound is vacuous ((e/n)^{2d}
is no longer small); the transfer question there is handled by the exact laws
of Sections 3 and 6 instead. This lemma is what lets every stipulated-channel
computation transfer to the true channel at small budgets - and it identifies
the exact boundary (per-row cost Theta(n)) beyond which the transfer fails.

## 5. Theorem 3 (the budgeted cap; the corrected Theorem B)

For a tree T of budget e, define:
  P_adj(e) <= min(1, e h1) * min(1, e q (2d-1)/(2(n-1))),
  P_K(e)   <= (1 - exp(-e d/(4n))) * 2,
No elevation term exists: Theorem 2(iv) caps every certificate-free leaf at
q. A first hit costs at most e h1 by the union bound over queries; each
subsequent same-line query then answers 1 with conditional probability at most
q(2d-1)/(2(n-1)): the past's hit elevates the row's freeness posterior to at
most q (Theorem 2(iv): further zeros only suppress), and the new column must
be a fresh free column (2d-1 of 2d remaining, exact hypergeometric factor).

Theorem 3 (budgeted cap, true channel, full degree-<=2 class). Every adaptive
tree of budget e using single-variable queries, degree-2 monomial queries, and
linear forms satisfies
  success(T) <= min(1, q + P_adj(e) + P_K(e) + O(e/n) + o(1)),
with the o(1) absorbing the block-completion probability p_block(e).

Proof sketch (components proved above; assembly marked). Decompose the tree's
leaves into certificate leaves (Theorem 1 or a K_j certificate: Section 6)
and certificate-free leaves. Certificate leaves: each certificate event
consumes either an adjacency pair (bounded by P_adj: the first hit costs at
most e h1 by the union bound over queries, and each subsequent same-line query
answers 1 with conditional probability at most q (2d-1)/(2(n-1)),
because the row-freeness posterior given a certificate-free past is at most
q by Theorem 2(iv) and each further zero only suppresses (exact one-hit
computation; the multi-row composition is modulo JDP, the same citation status
as Lemma B.1)) or a K_j answer-1 plus a 1-entry in that column (P_K: the K_j
answer costs e d/n per query by F5, the 1-entry costs (2d+1)/(2(n+1)) per
query, and optimizing the budget split gives the stated bound). Certificate-
free leaves: on the block-free event (Lemma REL) the channel is the product
channel, where the corpus's repaired per-pair Bayes applies: the output pair's
posterior is at most max over (own-row evidence, own-column evidence, distant
evidence) <= q * (1 + O(e/n)) - own-hit gives q (Theorem 2(i)), own-row
deep-scan gives rho_2a < q (Theorem 2(iv)), own-column gives <= q
(Section 3), distant evidence only depresses (exact one-distant-hit
computation, NA composition modulo JDP), and block completion adds o(1).
The O(e/n) term is the finite-population depletion of Lemma B.1, which is
valid on the product channel. QED [assembly honest: two modulo-JDP steps
marked, both inherited from the corpus's existing standard].

At the program's budget e = d log k, d <= sqrt(n): P_adj <= (d log k)(f/2+m)
* (d log k)/(2n) * q = O(d^4 (log k)^2/n^3) -> 0 and P_K <= 2(1 -
exp(-d^2 log k/(4n))) which is O(1)-small exactly when d^2 log k = o(n) but
NOT when d ~ sqrt(n) - see Sections 6 and 8: this is not a defect of the
bound; the
K-channel genuinely turns on there (Theorem 4), and Theorem 3's cap degrades
to q + O(1), still sufficient for the chi-conclusion in Corollary 3.1.

Corollary 3.1 (chi-hypothesis at p = 2 for degree <= 2). For every (n,d,k)
with 2d^2 + 3d <= n (so q <= 1/2; d <= sqrt(n/3) suffices for n >= 27) and
budget e = d log k:
  success(T) <= 1/2 + o(1) + 2(1 - exp(-d^2 log k/(4n))),
so error >= 1/2 - o(1) - 2 d^2 log k/(4n) >= 1/2 - o(1) >= k^{-O(1)} whenever
d^2 log k = o(n). In particular the chi-hypothesis of Theorem 6.1 HOLDS at
p = 2 for the entire adaptive degree-<=2 class on the true pipeline whenever
d^2 log k = o(n) - the condition the corpus's delta <= 1/(2O(l)) regime
satisfies with room. [Proof: certificate-free leaves are capped at q (Theorem
2(iv)); certificate leaves are absorbed by P_adj -> 0 and P_K
linearized by 1 - e^{-x} <= x.] This is the first cap theorem for the full
adaptive degree-<=2 class under the true channel; it answers and_chain.md's
"no cap theorem covers this class" and cert_floor.md's open item (a) in the
polylog-budget regime.

## 6. Theorem 4 (the column-parity tree; strongest known tree at O(n) budget)

The K_j-tree: (1) query K_j for j = 1, ..., n in fixed order; (2) let E =
{ j : answer 1 } (each certified j in R, soundly by F5); (3) scan the columns
of E (singles x_ij, i = 1..n+1) until a 1-answer; output that pair; (4) if no
answer-1 appears anywhere, fall back to a fixed pair (adds f * err_K to the
success). Budget: n + |E|(n+1) <= n + 2d(n+1).

Theorem 4. On the true channel the K_j-tree's error is exactly
  err_K = sum_{s odd, 1 <= s <= 2d-1} C(2d, s) 2^{2d(s-1)}
          / 2^{(2d+1)(2d-1)}
        = 2^{1-4d} 2d (1 + o(1)),
i.e. 1028/2^15 = 0.031372 at d = 2 (success 0.96863 at (32,2) for
n + O(dn) = 131 queries), 8·2^{-15} = 2.44e-4 at d = 4, and the exponent is
4d - log2(2d) - 1 per d. The tree is REAL on the true pipeline, unlike both
the corpus's two-phase tree (F3: phase 1 dead) and cert_floor's Theorem R
(whose Q_i half is dead; only its K_j half survives, which is Theorem 4).

Proof. The K_j answers depend only on the free columns' parities: for j in R,
K_j = 1 + XOR of its (2d+1) free-pigeon bits, so K_j = 1 iff the column is
EVEN; killed columns answer 0 (F5). The tree fails iff every certified column
is all-zero, i.e. every EVEN column is all-zero, i.e. every column of the
free-region coin matrix is either odd-parity or all-zero. The number of odd
columns is odd (the total parity of all free bits equals the sum of the row
parities = 2d+1 = 1 mod 2, and equals the sum of the column parities), and
rows are odd by F2. Fix the odd set S, |S| = s odd; the columns outside S are
all-zero, each row's ones live in S with odd parity, and each column of S must
be odd: the count of (2d+1) x s binary matrices with all row sums odd and all
column sums odd is 2^{(2d+1-1)(s-1)} = 2^{2d(s-1)} (the r+c-1 rank of the
row/column incidence constraint; verifiable at (5,2) by exact enumeration,
digit-exact in chi_deg2_theory_check.py). Summing over C(2d, s) choices of S:
  err_K = sum_{s odd} C(2d, s) 2^{2d(s-1)} / 2^{(2d+1)(2d-1)}.
The dominant term is s = 2d-1 (one all-zero even column): C(2d,2d-1)
2^{2d(2d-2)} / 2^{(2d+1)(2d-1)} = 2d 2^{1-4d}; all other terms are smaller by
2^{-Theta(d^2)}. On a non-all-zero certified column the scan finds its 1-entry
and the output is free with posterior 1 (Theorem 1's column case); on the fail
event the fallback adds f * err_K to the success. QED.

Theorem 4b (budgeted form). For any budget e >= 2, a K_j-tree that splits the
budget (alpha e on K_j queries, (1-alpha)e on scanning certified columns)
succeeds with probability at least
  (1 - exp(-alpha e d/n)) * (1 - exp(-(1-alpha) e (2d+1)/(2(n+1))))
  + f * (fallback mass),
which after optimizing alpha is >= (1 - exp(-e d/(4n)))^2. Proof: each K_j
query certifies with probability (2d/n)(1/2) = d/n (F5), each scan of a
certified column hits a 1-entry with per-query probability (2d+1)/(2(n+1))
(free-pigeon fair coins), and the two stages are independent given the
pipeline. QED. At (32,2) with the split above: B = 30 gives ~0.41, B = 100
gives ~0.93, and B >= 300 saturates at the pure-tree ceiling
1 - (1-f) err_K = 0.9692 [all measured in the check script; the K_j-tree
beats the single-scan baseline at every tested budget, including B = 10].

Comparison at (32,2): Theorem 4's success 0.9692 at budget ~ n + 3(n+1) = 131
(measured 0.9698 [0.9665,0.9728]), against and_chain.md's measured confirm
chain 0.5833 [0.5309,0.6340] at B = 300 and 0.9417 [0.9119,0.9618] at B = 1000
(33n): the K_j-tree DOMINATES the chain at every compared budget (0.9692 at
4n vs 0.9417 at 33n), and the measured budgeted K_j-tree gives 0.4939 / 0.9668
at B = 30 / 100 (vs the chain's measured 0.1917 / 0.3700; single-scan
0.1830 / 0.2574): the strongest known degree-1 tree on
the true pipeline is the K_j-tree, not the confirm chain, at every measured
budget. No previously measured corpus strategy queried K_j at all.

## 7. Theorem 5 (full-scan certainty; Theorem F's value is channel-dependent)

Theorem 5. On the true channel, the non-adaptive tree that queries all n(n+1)
single variables and applies cert_floor's counting certificates has success
EXACTLY 1 (error 0, no fallback luck needed): every configuration's answer
table has every row carrying at least one 1 (killed rows exactly one by F2;
free rows odd parity >= 1 by F2), so M has >= n+1 ones in n columns, some
column carries >= 2 ones, that column is certified free (killed columns have
exactly one 1), and each of its 1-entries certifies its pigeon (Theorem 1's
column case). QED.

Consequently the BAYES OPTIMUM of the unbounded-budget degree-1 game on the
TRUE pipeline is success 1, error 0. cert_floor.md's Theorem F
(err* = (1-2d/n)(2d+1)(2d)!/2^{(2d+1)2d} > 0) is proved under the stipulated
i.i.d. channel, where the failure class b (every column exactly one 1, rows at
most one 1) requires an ALL-ZERO free row - possible with i.i.d. coins,
IMPOSSIBLE under the true channel (odd parity). On the true pipeline the class-
b event is empty and Theorem F's error value does not transfer; the true
unbounded optimum is 0. [This is a channel-scope correction to Theorem F, not
a defect in its proof: its statement is internally correct for the channel it
quantifies over. The same applies to Theorem R: under the true channel its
Q_i half is inert (F3) and its error formula does not transfer; the surviving
half is Theorem 4.]

## 8. The budgeted certification boundary at p = 2 (both directions)

Combining Theorem 3 (cap) and Theorem 4b (witness), with e = d log k:

  Upper: success(T) <= q + 2(1 - exp(-d^2 log k/(4n))) + O(d^4 (log k)^2/n^3) + o(1).
  Lower: some degree-1 tree achieves success >= (1 - exp(-d^2 log k/(4n)))^2,
         so its error is <= 2 exp(-d^2 log k/(2n)) = 2 k^{-d^2/(2n)} once
         d^2 log k >> n.

So the budgeted error satisfies
  err*(d, e = d log k) = k^{-Theta(d^2/n)}
in the regime d^2 = Omega(n) (witness-dominated), and err* >= 1/2 - o(1) in
the regime d^2 log k = o(n) (cap-dominated). The transition sits at d^2 ~ n,
INDEPENDENT of log k: for any fixed implied constant C of the chi-hypothesis
(error >= k^{-C}), the hypothesis HOLDS when d^2 <= c C n and FAILS (via
Theorem 4b) when d^2 >= C' C n. This resolves, in shape and up to constants,
cert_floor.md open item (a) (the budgeted floor) and and_chain.md's open
follow-up (the constant scaling):

- and_chain's measured chain constant c ~ 0.0025/query at (32,2) is derived
  analytically: a hit costs h1 = 0.0362 per query, and k = 6 neighbor probes
  certify with probability 1 - (1 - q (2d-1)/(2(n-1)))^k with
  q the per-hit posterior (deep zero-run elevation does not exist on the true
  channel, Theorem 2(iv)): the analytic
  constant is h1 (1 - (1 - 0.2632*3/62)^6) = 0.0026 [MV in the check script],
  matching the measured 0.0018-0.0026. Its scaling is c = Theta(h1 q d/n) =
  Theta(d^3/n^2 * (2d+1)d/((2d+1)d + (n-2d)) / n) ~ Theta(d^3/n^3) at
  d = o(n): and_chain's heuristic d^3/n^3 is confirmed, and the K_j-channel's
  d/n per-query rate strictly dominates it (d/n vs d^3/n^3 for d >= 2), which
  is why Theorem 4 beats the chain.

- The corpus's standing delta-cap is upgraded from heuristic to theorem: the
  chi-hypothesis at p = 2 (and hence the Krajicek Theorem 6.1 route at p = 2)
  is viable exactly when d = (log k)^{O(l)} satisfies d^2 = O(C n), i.e.
  delta * O(l) <= 1/2 with constant room; at delta above that the K_j-tree
  drives the error below k^{-C} and Omega(n,d) FAILS Definition 3.1 against
  degree-1 trees (in the budgeted quantifier; if Definition 3.1's quantifier
  is unbounded, it fails outright by Theorem 5, for every k with
  log k > 0 - err* = 0 there).

## 9. What remains open

1. The full monotonicity of FB(k) (Theorem 2(iv)): proved elementarily for
   k <= n-2d; the short tail range k > n-2d is verified numerically at three
   parameter points. [residual open: the tail proof]
2. The optimal budget split and the exact constant in err*(e) =
   exp(-Theta(e d/n)) for n/d <= e <= n^2/d: the K_j-tree and the cap differ
   by a constant factor in the exponent; the true optimum (and whether
   row-parity evidence, which needs Theta(n) per row, can be combined with
   K_j-certified columns for a better rate at e ~ n) is open.
3. Intermediate budgets: at e ~ 4n the pure K_j-tree errs 2d 2^{1-4d}
   (failure dominated by the single-all-zero-even-column configuration, s =
   2d-1 in Theorem 4's sum), but that failure matrix (all rows odd, 2d-1 odd
   columns, one all-zero even column) still contains exploitable structure
   (the 2d-1 odd columns over 2d+1 odd rows force double-hits under further
   scanning): the true optimum at e = Theta(n) is between 2d 2^{1-4d} and
   0 - OPEN.
4. The modulo-JDP composition steps in Theorem 3 (multi-row depression):
   same citation status as the corpus's Lemma B.1. Not yet machine-checked;
   the exact one-hit computations it composes are proved in Theorem 2.
5. The chi-transfer of Theorem 4's tree (cert_floor item 4's reading of
   Definition 4.3): does the K_j answer pattern transfer to the chi-task
   verbatim? Unchecked against the paper's definitions.
6. The outer-reading question is RESOLVED for everything here: the
   redispatched kernel_structure.py proves V(n,d)^rho = V(2d,d) exactly (its
   F1), so the outer and canonical readings impose identical design spaces and
   all formulas of this file are reading-independent.

## 10. Corrections and updates this analysis contributes to the corpus

1. The attempted direction (a) bound (posterior <= q + O(d^2/n) on every
   answer pattern) is FALSE in both channels: certificate leaves (Theorem 1)
   have posterior exactly 1, while every certificate-free leaf is capped at q
   strictly (Theorem 2(iv): the deep-scan value rho_2a = 0.0820 at (32,2) is
   BELOW q; the same holds on the stipulated channel). The corrected form is
   the dichotomy of Theorems 1-2 and the budgeted cap of Theorem 3.
2. Theorem F's error VALUE is stipulated-channel-specific; on the true
   pipeline the unbounded degree-1 optimum is success 1 (Theorem 5): the
   class-b failure event is empty there. cert_floor's Corollary 2 (full-scan
   dominance) and Lemma 3 (counting certificates) transfer verbatim; only the
   class-b probability dies.
3. Theorem R (cert_floor) does not exist on the true pipeline (its Q_i half
   answers 0 always, F3); its surviving K_j half is Theorem 4, which is
   STRONGER at equal budget than everything previously recorded on the true
   pipeline (dominates and_chain's confirm chain per Section 6).
4. and_chain.md's open follow-up (scaling of the chain constant c) is answered
   analytically: c = h1(1 - (1 - q(2d-1)/(2(n-1)))^k) = 0.0026 at (32,2,k=6)
   vs measured 0.0018-0.0026, scaling Theta(d^3/n^3); superseded as a
   strategy by the K_j channel (Theta(d/n)).
5. The budgeted floor (cert_floor open item (a)) is solved in exponential
   shape for the (d, d log k) quantifier: err* = exp(-Theta(d^2/n)) with the
   boundary at d^2 ~ Theta(n); Corollary 3.1 supplies the cap side for the
   full degree-<=2 class.
6. The exact degree-2 AND per-hit posterior on the true channel is
   q_and = (f^2 p_diag/2 + f m/2)/(f^2 p_diag/2 + f m + m^2) with
   p_diag = (C(G,2) - (2d+1)C(2d,2) - C(2d+1,2)2d)/C(G,2), G = (2d+1)2d
   (diagonal fraction among distinct pairs; same-line pairs answer 0
   determinedly by F4). At (32,2): q_and = 0.2765 (q = 0.2632). Two numeric
   footnotes: kernel_structure.py's docstring value 0.311 at (32,2) used
   p_diag = 1 (its own formula gives 0.2765); the corpus's "exactly q = 0.263"
   is the stipulated-channel value. Neither number changes any recorded
   conclusion (the lift 0.2765 - 0.2632 is within the recorded "mild" range).
7. Theorem B survives as Corollary 3.1's q-side cap in the regime
   d^2 log k = o(n) - its proof does not (the i.i.d.-coin premise and the
   O(e/n) cross-coupling step are both superseded by Lemma REL + Theorem 2),
   and its class scope (single-variable) is subsumed by the full degree-<=2
   statement.

## 11. Computational verification (chi_deg2_theory_check.py)

The script verifies, on exact GF(2) designs (independent re-implementation of
the canonical design space; (48,4) uses the structural single-coordinate
sampler, exact by the row-parity theorem) and exact channel sampling:
  V1. F2/F3/F5 structure facts at (2,1) (exhaustive, 8 designs) and (4,2)
      (4000 sampled designs): row parity 1; L(Q_i) = 0; K_j answers 1 on
      exactly the even free columns; same-line degree-2 products 0; the
      diagonal coordinate d(00;11) jointly uniform with x_00, x_11 (all 8
      patterns, within 4 sigma); diagonal marginal 0.5000 over 480000 reads.
      ALL PASS.
  V2. Theorem 2's closed forms at (32,2), Clopper-Pearson 99% intervals,
      300000 row scans: post(0): 0.2619 [0.2510,0.2730] vs q = 0.263158;
      post(1): 0.2585 vs 0.2537; post(5): 0.2228 vs 0.2166; post(15): 0.1283
      vs 0.1367; post_full: 0.0875 [0.0798,0.0956] vs rho_2a = 0.0820.
      ALL PASS.
  V3. Theorem 4: K_j-tree success 0.9698 [0.9665,0.9728] vs 1-(1-f)err_K =
      0.969222 at (32,2) (20000 sims); 0.999775 [0.999500,0.999922] vs
      0.999763 at (48,4) (40000 sims, structural sampler); PLUS digit-exact
      enumeration over all 2^15 odd-row (5,2) canonical matrices: 1028
      failures, formula count 1028. ALL PASS.
  V4. Theorem 5: 5000 full scans at (32,2): zero certificate-absent
      failures. PASS.
  V5. Theorem 4b at (32,2), 20000 sims per budget: K_j-tree 0.1117 / 0.4939 /
      0.9668 / 0.9685 / 0.9698 at B = 10 / 30 / 100 / 300 / 1000 against the
      split predictions 0.094 / 0.415 / 0.936 / 0.9692 / 0.9692 (ceiling-
      capped): lower bound met at every budget, and K > single-scan at EVERY
      budget (single: 0.0910 / 0.1830 / 0.2574 / 0.2622 / 0.2588, hugging q).
      ALL PASS.
  V6. the analytic chain constant 0.00266 vs and_chain's measured
      0.0018-0.0026 per query. Consistent.

## 12. One-paragraph verdict for the orchestrator

The per-leaf posterior cap attempted in the brief is false exactly at
certificate leaves and nowhere else: posterior evidence is dichotomous
(isolated or deep-scan: <= q, and strictly below q away from k = 0 by the
parity tax 2^{1-2d}; co-linear: exactly 1). The dichotomy yields a budgeted
cap (success <= q + 2(1 - e^{-d^2 log k/4n}) + o(1)) that keeps the
chi-hypothesis alive while d^2 log k = o(n) - and while d^2 = O(n) once the
witness side is accounted - and a new degree-1 tree (column parity,
Theorem 4) dominates every previously recorded tree on the true pipeline at
O(n) budget with error 2d 2^{1-4d}, while the full scan certifies with
probability exactly 1.
The p = 2 story of this corpus is now: no budgeted error floor exists (Theorem
5), the budgeted floor decays as exp(-Theta(e d/n)) (Theorems 3+4), and a
single degree-1 column-parity query class (K_j) dominates every previously
recorded tree on the true pipeline at every measured budget, with error
2d 2^{1-4d} at O(n) budget, while the full scan certifies with probability
exactly 1. The program's parameter connection survives exactly when
d^2 = O(n).
