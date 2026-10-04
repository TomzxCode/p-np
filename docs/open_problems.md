# Open problems of the corpus: the final catalog (post-correction state)

Compiled 2026-10-03 by the open-problems agent, after the EIGHTH logged
self-correction (the kernel-structure channel-law restatement) and the
analysis files that bear on it (and_chain.md, deg2_theory.md). Every
problem below is stated in its FINAL framing; where a correction or a later
corpus file superseded an earlier framing, the supersession is recorded
inline. No corpus file was edited; LOG.md was not touched. Status labels:
OPEN, SETTLED-IN-FORM (proved in form, constants or scope missing), RESOLVED.

Adjudication status of what this catalog leans on: kernel_structure.md
(18 PASS / 0 FAIL, reproduces digit-for-digit) and cert_floor.md (exact
enumeration + Bayes audit) are machine-verified; and_chain.md and
deg2_theory.md are measurement + analysis with machine-verified facts
flagged [MV] in place; the two modulo-JDP steps in deg2_theory.md's Theorem 3
carry the corpus's Lemma B.1 citation standard and are marked where used.

## 0. The channel everything below is phrased on (final state)

The object is the Omega(n,d) pipeline of arXiv:2609.35927 at p = 2
(Definition 4.3: rho a uniform partial injection leaving 2d free holes R and
2d+1 free pigeons D; L a uniform degree-d design of the restricted system;
ans(g) = L(g^rho)), under the kernel-verified answer law:

  F1. matched pair -> answer 1; killed-unmatched -> 0 (L(1) = 1, L kills V).
  F2. free singles: marginally fair, jointly i.i.d. on ROW-INCOMPLETE query
      sets; a fully queried free row is PARITY-LOCKED (XOR = 1; only
      2^(2d-1) of 2^(2d) patterns occur); killed rows and killed columns of
      the answer table M show exactly one 1.
  F3. the row-sum query Q_i = 1 + sum_j x_ij answers 0 DETERMINEDLY on
      every pigeon: Q_i is a generator of V(n,d)^rho = V(2d,d) (one kernel;
      the outer/canonical design-space debate is dissolved,
      kernel_structure.md Finding 1).
  F4. degree-2 columns: squares answer their single variable; same-pigeon
      and same-hole products answer 0 determinedly; diagonal products
      answer a fair bit independent of the two component singles (rank
      3/3), subject to the Q-shift sum rules, which are
      configuration-invariant and carry zero information about rho.
  F5. the column-parity K_j = 1 + sum_i x_ij is NOT a generator: it answers
      0 on killed columns, a fair coin on free columns, so an answer 1
      certifies the hole free. The row/column asymmetry is the pigeonhole
      principle itself.
  F6. the corpus's i.i.d.-coin simulators sample a STRICT SUPERSET of the
      legal designs (legal fraction 2^-(2d+1)); results proved only on the
      coin model are flagged coin-model below.

Notation: f = (2d+1)2d/((n+1)n) (free-pair mass), m = (n-2d)/((n+1)n)
(matched mass), h1 = f/2 + m (answer-1 rate per single query),
q = (f/2)/(f/2 + m) = (2d+1)d/((2d+1)d + (n-2d)) (per-hit labeling
posterior), e = d log k (the program's budget), gamma = k^{-O(1)} (the
solution threshold). Parameter points are written (n,d).

The eight corrections, for the record: (1) razborov_check.py pivot-order
bug; (2) the chi-direction inversion; (3) the canonical-shortcut
multiplicativity error (0.37 -> 0.0005); (4) the multi-variable no-lift
prediction refuted; (5) the O1-negative flip; (6) the two-phase refutation
flip; (7) Theorem T's exact law is a simulator artifact, Proposition D
false as stated, Theorem F proved; (8) the kernel-structure channel-law
restatement (one kernel, parity-lock, Q_i dead). deg2_theory.md contains
one further mid-analysis retraction (a parity-elevation arithmetic slip,
caught by its own Monte Carlo before delivery), recorded in place.

## O2. The budgeted chi-hypothesis (the printed quantifier). OPEN

Statement. Is there a constant C such that EVERY adaptive tree T with at
most e = d log k queries, each query a degree-<=d polynomial over F_2, in
the Omega(n,d) pipeline at p = 2, errs with probability

  Prob_omega[T(omega) is not a conflict for omega] >= k^{-C}

for all n and all d = (log k)^{O(l)}, i.e. no budgeted tree certifies a
free pair with probability >= 1 - k^{-C}? This is Theorem 6.1's hypothesis
in its printed budgeted form (it quantifies over (d, d log k)-trees,
arXiv:2609.35927; the reading is verified in proof_complexity.md). A
positive answer at any k(n) >= n^{omega(1)}, via Theorem 6.1, gives k-step
lower bounds for AC0[l](MOD_2)-Frege refutations of -PHP_n: super-polynomial
AC0[2]-Frege lower bounds, the frontier problem with no non-trivial bounds
known for any formula. A negative answer refutes Omega(n,d) as a
pseudo-solution at p = 2 and redirects the program.

The unbounded version is REFUTED, twice over.
(a) Coin model: Theorem F (cert_floor.md) proves every adaptive degree-1
    tree errs exactly err* = (1 - 2d/n)(2d+1)(2d)! / 2^((2d+1)2d)
    = 2^{-Theta(d^2)} (1.0e-4 at (32,2)), attained by a non-adaptive
    full-scan counting tree; so against unbounded trees Omega(n,d) fails
    Definition 3.1 for every k with log k > 4d^2 - O(d log d)
    (cert_floor.md, open item (c)).
(b) True channel: Theorem 5 (deg2_theory.md) proves the full scan certifies
    with probability EXACTLY 1 (every row of M carries a 1 by F2, so some
    column carries two, and a double-one column certifies its entries
    free), i.e. err* = 0: the unbounded hypothesis fails for every k >= 2.
Whether Definition 3.1's printed quantifier is budgeted is a reading check
against the paper; the corpus's working reading is budgeted, and only the
budgeted problem is alive.

Proved around it, budgeted and at p = 2.
- Non-adaptive: Props A and C (proof_complexity.md) cap the single-variable
  class; kernel-faithful (TV = 0 off full rows, kernel_structure.md item 4).
  Proposition D is RETRACTED as stated (the rc counting tree, exact 0.9067
  vs cap 0.625 at (64,2)); its surviving form covers the variable/monomial
  non-adaptive class only.
- Adaptive single-variable: Theorem B (proof_complexity.md) with Lemma B.1
  (negative-association coupling). Its CONTENT survives as the q-side of
  the degree-<=2 cap; its PROOF route (i.i.d.-coin premise, O(e/n)
  cross-coupling) is superseded by Lemma REL + Theorem 2 of
  deg2_theory.md.
- Adaptive degree <= 2, true channel: SETTLED IN EXPONENTIAL FORM
  (deg2_theory.md, Theorems 1-4, Corollary 3.1). The budgeted floor is
    err*(d, e = d log k) = k^{-Theta(d^2/n)},
  transition at d^2 ~ Theta(n), independent of log k. Cap side (upper
  bound on success, for the FULL adaptive degree-<=2 class, d <=
  sqrt(n/2)):
    success(T) <= q + 2(1 - exp(-d^2 log k/(4n))) + O(d^4 (log k)^2/n^3) + o(1)
  (Corollary 3.1; two composition steps modulo JDP). Witness side (lower
  bound): the K_j column-parity tree (Theorem 4b) achieves error
  <= 2 k^{-d^2/(2n)} at e = d log k. Consequence: for any fixed implied
  constant C the hypothesis holds when d^2 <= c C n and fails when
  d^2 >= C' C n; the program's connection delta * O(l) <= 1/2 survives
  with constant room, and the corpus's delta-cap is now theorem-backed at
  degree <= 2 (heuristic beyond).

Open core, in order.
(i) Degree >= 3 trees: no cap of any kind; the kernel's degree-3 structure
    is classified only in count (kernel_structure.md Sec 7). This is the
    substantive content of O2: Theorem 6.1's quantifier allows degree up to
    d = (log k)^{O(l)}, which grows.
(ii) The exact constant in k^{-Theta(d^2/n)}: cap and witness differ by a
    constant factor in the exponent (at (128,2), e = 32: cap ~ 0.32 vs
    best witness 0.06, single scan 0.02).
(iii) The chi-transfer: cap and witness are proved for the conflict-pair
    task; feeding Theorem 6.1 needs them for the printed chi-quantity with
    its Span condition (cert_floor.md item 4's conditional; deg2_theory.md
    open item 5, unchecked).
(iv) Intermediate budgets e = Theta(n): the optimum lies between
    2d . 2^{1-4d} and 0 (deg2_theory.md open item 3).
(v) The two modulo-JDP composition steps (deg2_theory.md item 4) and the
    FB(k) tail monotonicity for k > n-2d (its item 1).

Falsifiable toy-scale prediction. True channel, (128,2), budget e = 32
(log k = 16), 20,000 simulations per strategy, 99% Clopper-Pearson
intervals: the split K_j-tree (Theorem 4b) must land at 0.059 +/- 0.004 and
no adaptive degree-<=2 strategy may exceed the cap band 0.317 + o(1). A
strategy above 0.35 falsifies the cap's JDP steps; everything at
<= 0.10 tightens the exponent constant toward the witness side. Companion
boundary check at budget e = d log k with log k = 16: split K_j success
0.770 at (64,4) vs 0.9994 at (64,8): the success cliff between d = 4 and
d = 8 at n = 64 IS the d^2 ~ n transition, measurable with 2,000 sims per
point.

Difficulty. HARD: the all-degrees adaptive quantifier is the 30-year
program's core in local form. The degree-<=2 resolution supplies the attack
template (posterior dichotomy, block completion, negative association), so
the next increment is concrete: classify degree-3 determined structure and
extend Lemma REL.

Interdependencies. Consumes O3 (certificate rates: the cap's certificate
terms) and O5 (the degree-2 answer law under the certificate-free leaves);
it is the cap-side instance of O7's classification; it shares the reduction
core with O6 (Theorem 6.1 is characteristic-uniform).

## O3. The certificate budget constant (adjacency and column parity). OPEN

Statement. The confirm chain's certificate rate at (32,2) is
cert(B) ~ 1 - exp(-B/400), i.e. constant c ~ 0.0025 per query (measured
0.0018-0.0026 across B = 30/100/300/1000, posterior|cert = 1.0000 in every
cell of 52,800 simulations, and_chain.md). The constant 400 is the corpus's
sharpest measured number, and the eighth-correction block named its scaling
the decisive question: polynomial scaling keeps the budgeted chi-hypothesis
alive at the program's parameters; faster scaling closes the p = 2 route
via Theorem 6.1. Final framing, after deg2_theory.md:
(a) confirm the derived law c(n,d) = h1 (1 - (1 - q(2d-1)/(2(n-1)))^k) for
    k-neighbor probing (k = 6): analytic value 0.00266 at (32,2), machine-
    verified against the measured 0.0018-0.0026;
(b) decide whether depth-3 chaining (certify the certified) compounds the
    effective constant or saturates;
(c) decide the OPTIMAL certificate rate over all adaptive trees: is
    Theta(d/n) per query (the K_j channel) the degree-1 ceiling, and what
    is it at degree >= 2?

What is proved around it. Lemma C (and_chain.md) / Theorem 1
(deg2_theory.md): adjacency certification, posterior EXACTLY 1 (two
co-linear answer-1s cannot both be matched pollution, since a killed row or
column has exactly one 1); sound on both channel readings; it consumes only
rho-determined structure, hence survives the kernel truth (measured 0.9417
on the exact pipeline at B = 1000, cert 92.83%, asserted free with zero
failures). The per-hit no-lift at q is proved single-pass and empirically
exact on both channels (every single-hit strategy lands on q; the earlier
"AND advantage" was a 2x-query subsidy artifact). Theorem 4/4b
(deg2_theory.md): the K_j-tree, exact error 2d . 2^{1-4d} at O(n) budget
(0.031372 = 1028/2^15 at d = 2), enumeration digit-exact at (5,2); it
DOMINATES the confirm chain at every compared budget (0.9686 at 4n queries
vs 0.9417 at B = 1000).

Bounds. Chain constant c ~ 12 d^3/n^3 for fixed k = 6 and d = o(sqrt(n))
(h1 ~ 1/n, q ~ 2d^2/n, neighbor rate ~ d/n). K_j rate d/n per query
(F5: half the free columns, of mass 2d/n). Cap side: the certificate terms
of Theorem 3, P_K(e) <= 2(1 - exp(-e d/(4n))), against the witness
(1 - exp(-e d/(4n)))^2: a constant-factor gap in the exponent, which is
O2(ii).

Answer to the original fork. The scaling is polynomial, specifically
Theta(d^3/n^3) for the chain: the free-density heuristic was right in form,
the hypothesis survives the chain route at the program's parameters, and
the route via Theorem 6.1 does NOT close through adjacency chains. The "or
better" branch exists but sits in a different mechanism: the K_j channel
(Theta(d/n) per query) dominates the chain for all d >= 2, and it is what
moves the budgeted boundary to d^2 ~ n in O2.

Falsifiable toy-scale prediction. True channel, B = 10^4, 2,000
simulations per point. The law predicts cert(64,2) = 1 - e^{-3.405} = 0.967
(~67 failures) and cert(128,2) = 1 - e^{-0.428} = 0.348 (~697 certs). The
rival d^2/n^2 law predicts 0.9985 (~3 failures) and 0.803 (~1606 certs):
both points separate by > 7 sigma, so 2,000 sims decide. Depth-3 probe:
(32,2), B = 3000, 1,000 sims per depth, comparing the effective constant
-ln(1 - cert)/B across chain depths 2 and 3: compounding means growth
beyond the 1 - (1 - c)^{depth} saturation curve.

Difficulty. MODERATE: one multi-point experiment plus one composition
proof (the JDP steps).

Interdependencies. This is the witness side of O2; its mechanism inventory
is O7's first two entries.

## O4. The parity-locked counting floor (Theorem F's constant). RESOLVED

Task framing (the eighth-correction expectation, kernel_structure.md item
5): recompute Theorem F's exact constant under kernel truth; the hard class
is parity-locked, per-row count-1 probability 2d/2^{2d-1} vs 2d/2^{2d}, the
2^{-Theta(d^2)} order survives, the constant does not (an expected ~4x-class
change).

Final state: the recomputation terminates at ZERO, not at a changed
constant. The counting tree's only failure class is class b (every column
exactly one 1, every row at most one 1; cert_floor.md Lemma 5), and class b
requires an ALL-ZERO free row. Parity-locking (F2) forces every free row's
count to be odd, hence >= 1, so class b is EMPTY on the true channel: the
full-scan counting tree certifies with probability exactly 1 (deg2_theory.md
Theorem 5; measured 0 failures in 5,000 sims at (32,2), its check V4). The
per-row count-1 probability 2d/2^{2d-1} is correct but was the wrong
handle: the count-0 row is what dies. Theorem F's value
2^{-Theta(d^2)} remains exact for the channel it quantifies over (the
stipulated i.i.d. coin model) and is a coin-model number on the pipeline,
completing the flag already carried in kernel_structure.md item 4.

Bayes-optimality under parity-locking: YES, trivially at unbounded budget.
Error 0 is optimal and the counting tree attains the Bayes value on every
answer table (the exhaustively verified tree-vs-best agreement of
cert_floor.md's audit transfers; there is no gap left to audit). The
non-trivial remnant is BUDGETED counting-certificate optimality at
e = Theta(n): Theorem 4's failure matrix (all rows odd, 2d-1 odd columns,
one all-zero even column) still contains exploitable structure under
further scanning, and the true optimum lies between 2d . 2^{1-4d} and 0
(deg2_theory.md open item 3). That remnant is folded into O2(iv).

Falsifiable toy-scale prediction. Exact-design channel at (32,2): the
counting tree NEVER fails, so 0 failures in 100,000 simulations (the coin
channel predicts ~10 at err* = 1.0e-4; P[0 failures | coin model] = e^-10
= 4.5e-5, decisive). Exact form: extend chi_deg2_theory_check.py's (5,2)
enumeration (all 2^15 odd-row matrices, already digit-exact for Theorem 4)
to the counting tree's four-case analysis: it must certify on every matrix.

Difficulty. Closed. The residue (budgeted counting optimality at
e = Theta(n)) is moderate.

Interdependencies. None upward (unbounded budget, degree 1); its mechanism
is O7's second entry and its residue feeds O2(iv).

## O5. Degree-2 monomial semantics on the pipeline (the transfer lemma). OPEN

Statement. The AND no-lift's single-pass Bayes is coin-model:
kernel_structure.md item 4 records that the pipeline's degree-2 AND channel
differs from the product semantics and that the transfer "would need a
design-space redo"; the measured consistency (mono2 on the exact pipeline
0.2629 [0.2129, 0.3199] vs q = 0.2632) is noted but not covered by any
proof. The needed lemma, made precise (Lemma M): on the true channel, for
a single-pass DIAGONAL degree-2 monomial query x_ab . x_cd (distinct row
and column; same-line products answer 0 determinedly except the
matched-matched case, which is automatically diagonal), the answer is a
fair bit independent of the two component singles (F4, rank 3/3), so the
status-case Bayes with masses (free-free: f^2 p_diag, mixed: 2 f m,
matched-matched: m^2), where p_diag is the diagonal fraction among distinct
free-pair pairs, gives the per-hit labeling posterior

  q_and = (f^2 p_diag/2 + f m/2) / (f^2 p_diag/2 + f m + m^2),

equal to 0.2763 at (32,2), and no single-pass monomial transcript elevates
any component's posterior above max(q, q_and) without an adjacency event.

Already machine-verified around it: the B5 classification of ALL degree-2
columns (pivot/free) at (4,2) and (6,3); diagonal marginal fairness and
rank-3 independence from the component singles; the three design identities
the coin channel's product semantics violates (same-hole and same-pigeon
products of free pairs: determined 0 vs 1 w.p. 1/4; the Q-shift sum rule
XOR_j L(x_rj . x_cd) = L(x_cd): always vs w.p. 1/2; diagonals: fresh
independent bits vs the product; kernel_structure.md F5 table). The square
law L(x^2) = L(x) is the one identity product semantics gets right. What is
missing: the general-d writeup of Lemma M, and the adaptive multi-query
(chaining) version at degree 2, which belongs to O2(i)'s program.

Measurement caveat, recorded: the existing 600-sim mono2 interval contains
BOTH q = 0.2632 and q_and = 0.2763, so "measured-consistent" is true and
undecidable at that sample size; deg2_theory.md item 6 already flags the
corpus's "exactly q" as the stipulated-channel value.

Falsifiable toy-scale prediction. (32,2), true channel, B = 1000,
30,000 simulations (about 40,000 hits at hit rate 1.32e-3 per query):
predicted per-hit posterior 0.2763 with 99% CI half-width 0.006, i.e. the
band [0.270, 0.283]; q = 0.2632 sits 5.9 sigma below the prediction, so the
run is decisive in both directions: landing on q refutes Lemma M's
constant, landing in the band confirms the transfer and retroactively
strengthens Corollary 3.1's degree-2 leaf analysis. Component check at the
same run: 10^6 random same-line products of free pairs must answer 0 in
10^6/10^6 (any 1 refutes F4's outer-level form).

Difficulty. MODERATE: a finite Bayes audit over an already-classified
column space, machine-checkable end to end.

Interdependencies. O2's cap side at degree 2 (Corollary 3.1's
certificate-free leaves consume the degree-2 answer law); O7's degree-2
inventory entry.

## O6. The odd-p analogue. OPEN

Statement (p_family.md, core verbatim). Fix an odd prime p (or any fixed
p >= 3). Determine whether every (d, e')-tree with d = (log k)^{O(l)} and
e' = O(log n) + O(d log n) satisfies
Prob_{rho,P}[chi(P, rho) = 1] >= k^{-O(1)} in the Omega(n,d) pipeline at
characteristic p. A positive answer at any k(n) >= n^{omega(1)}, via the
characteristic-uniform Theorem 6.1 and the ENS equivalence, yields the
first super-polynomial AC0[p]-Frege lower bound at that characteristic and
the first lower bound of any kind for odd-p AC0[p]-Frege proofs of PHP. A
negative answer refutes Omega(n,d) at that p. The lane is strictly less
crowded than p = 2: no DAG-like Res(lin_Fp) PHP bound of any kind exists at
odd p (tree-like only: Part-Tzameret; fragments: Khaniki, Part).

Final-state caveats (added by the eighth correction and this catalog).
(a) Theorem T_p's phase-2 caveat (p_family.md: flagged ANALYSIS, inherits
    Theorem T's coin-branch gap) is now the SMALLER problem. The p-ary
    kernel is unaudited, and the p = 2 parity-lock has a
    characteristic-uniform explanation that transfers by inspection: for an
    assigned pigeon Q_i^rho is the zero polynomial at every p, and for a
    free pigeon Q_i^rho is a pigeon axiom OF THE RESTRICTED SYSTEM, killed
    by every design at every p (the mechanism of F3). Prediction: T_p's
    phase 1 is dead on the true p-ary pipeline exactly as at p = 2, and the
    p > 2 witness tree must be rebuilt (candidates: p-ary K_j, and
    self-certification). Flagged ANALYSIS: no F_3 computation has run.
(b) The parity-locked recomputation O6 needs, before any tree claim at
    odd p: the p-ary analogues of F2 (free singles uniform over F_p on
    row-incomplete sets; a fully queried free row's value-sum pinned to 1
    in F_p; only p^{2d-1} of p^{2d} patterns occur) and of F5 (is the
    p-ary column sum unconstrained?). The p-ary adjacency certificate is
    sound by inspection (a killed row has exactly one 1, so two co-linear
    1s still certify; moreover answers in {2, ..., p-1} self-certify
    outright, probability f(p-2)/p per query).
(c) The scan-cap arithmetic is characteristic-uniform (free-density
    counting): a budget-e single-variable scan certifies with probability
    <= e f (p-2)/p ~ 4 d^3 log k / n^2, capped far below 1 - k^{-O(1)}
    whenever d << n^{2/3}/(log k)^{1/3} (p_family.md Sec 4; the transition
    is Prop-D-type). Per-hit posteriors are higher at p > 2, hit probability
    is still f.

Falsifiable toy-scale prediction. F_3 kernel audit at outer (7,1) and
(15,2), restricted (2,1) and (4,2), 10,000 uniform F_3-design samples per
point (the kernel_structure.py harness with p = 3 arithmetic): (i)
L(Q_i^rho) = 0 in 10,000/10,000 for every pigeon, free ones included (any
nonzero answer collapses the transfer premise and with it T_p);
(ii) free singles marginally uniform on {0,1,2}, jointly uniform on
row-incomplete windows; (iii) full free rows: value-sum = 1 in
10,000/10,000 with only 3^{2d-1} of 3^{2d} patterns occurring; (iv) K_j:
P[ans = 1 | killed column] = 0 and P[ans = 1 | free column] = 1/3. Item
(iv) is the decisive one for the witness side: if the p-ary column sum is
constrained (the analogue of F3 for columns), the surviving certificate
inventory at odd p shrinks to self-certification plus adjacency, and O6's
budget analysis must be redone from those alone.

Difficulty. HARD: p-ary kernel machinery first, then the O2 program again
in a new algebra; both directions are frontier results.

Interdependencies. Shares the reduction core with O2 (characteristic-
uniform); its channel audit is the p-ary rerun of O7's inventory; nothing
in O2-O5 depends on it.

## O7. The certain-certificate classification (the trichotomy, made general). OPEN

Task framing (eighth-correction block): parity dead, counting alive-but-
constant-changed, adjacency alive; make precise the general question:
classify ALL certain-certificate mechanisms available to budgeted
variable-query trees over the true pipeline.

Final state of the trichotomy: it refines to a three-entry inventory, one
corpse, and one p > 2 extra; the "constant-changed" entry resolved to zero
(O4 above).

  ALIVE, variable queries. (1) ADJACENCY: two co-linear answer-1s certify
  both pairs free (Theorem 1 = Lemma C; consumes only F1/F2 killed
  structure; sound under every channel reading); per-hit cert probability
  1 - (1 - q(2d-1)/(2(n-1)))^k over k neighbor probes, chain constant
  c = h1 times that (O3). (2) COUNTING: two 1s in one line (the adjacency
  case), a 1 in an already-certified line (Lemma 3 transfers verbatim),
  and the global count (Theorem 5: perfect at unbounded budget).
  ALIVE, degree-1 linear queries. (3) COLUMN PARITY: K_j = 1 certifies the
  hole free at rate d/n per query (F5, Theorem 4). The row dual is the
  corpse: Q_i is a generator and answers 0 on every pigeon (F3); the
  asymmetry is the pigeonhole principle itself.
  DEAD. Row-parity certificates (the two-phase tree's phase 1; Theorem T's
  mechanism; coin-model-only, dead at kernel level, kernel_structure.md
  Finding 2).
  At p > 2. (4) SELF-CERTIFICATION: single answers outside {0,1} certify
  directly, probability f(p-2)/p per query (p_family.md).

The general question, made precise. Classify all transcript events E of
budgeted variable-query (and, in a second step, degree-<=2 and degree-<=d)
trees with P[E and output-not-free] = 0 over the full pipeline.
Conjecture (the classification target): every such E contains a co-linear
pair of 1s, or a 1 in a line already certified by an earlier certificate,
or (linear queries allowed) a K_j = 1. Consequences if true: the budgeted
certification rate of ANY tree is bounded by Theorem 3's sum (adjacency
term + K term + capped certificate-free mass), so O2's budgeted boundary
d^2 ~ n is exact at every degree <= 2, and the cap side of O2 reduces to
extending Lemma REL (block completion: determined relations require Theta(n)
coordinates per row and 2d-1 per sum-rule star, so low-budget transcripts
see a product channel) to higher degrees. What is missing: the degree-3+
kernel classification itself, the Lemma REL extension, and the rate-
optimality half (is d/n per query the ceiling?).

Falsifiable toy-scale prediction. (32,2), true channel, all symmetry
classes of 3-cell variable-query sets (same-row triple; same-column triple;
L-shape; one adjacent pair plus a distant cell; all scattered),
2,000,000 configuration samples per class: every posterior-1 answer pattern
must contain two co-linear 1s. A single posterior-1 pattern without
co-linear 1s at measurement resolution 1e-5 falsifies the inventory and
with it Corollary 3.1's certificate-term bookkeeping.

Difficulty. FRONTIER-HARD: a structural classification. The degree-<=2
base case is in hand (Theorems 1-3 of deg2_theory.md), which is what makes
the conjecture precise rather than speculative.

Interdependencies. Resolves O2's cap side and O3's optimality question if
carried through; O6's channel audit is its p-ary rerun; O4's residue is
one of its budgeted cases.

## How this catalog would be falsified

The single measurement or paper that collapses each framing.

- Catalog frame (kernel truth). The author of arXiv:2609.35927 correcting
  the intended reading of Definition 4.3's g^rho clause or vanishing
  condition, away from the zeroing completion and the V(n,d)^rho = V(2d,d)
  identity. Every problem above is phrased on the kernel-verified channel;
  a definitional correction dissolves the frame rather than any single
  item. Second: any paper analyzing the chi-task at all (the frontier has
  zero citations of the probability task); one would collapse the corpus's
  priority on O6 and possibly its framings.
- O2. One paper proving the chi-hypothesis for the all-degrees quantifier
  at any k(n) >= n^{omega(1)} (closes O2 and, via Theorem 6.1, delivers the
  AC0[2]-Frege bound), or one proving a degree-3 cap. One measurement: an
  adaptive strategy at (128,2), e = 32, exceeding success 0.35 over 20,000
  sims falsifies the cap side's composition steps; the (64,4) vs (64,8)
  cliff failing to appear falsifies the d^2 ~ n boundary. A reading check
  establishing that Definition 3.1 quantifies over UNBOUNDED trees would
  moot O2 entirely (the candidate is already dead by Theorem F on the coin
  model and Theorem 5 on the true channel).
- O3. The two-point run ((64,2) and (128,2), B = 10^4, 2,000 sims each)
  landing on the d^2/n^2 law (~3 failures at (64,2) and ~1606 certs at
  (128,2)) instead of d^3/n^3 (~67 and ~697): the chain route reopens at
  scale and the eighth-correction dilemma returns. A depth-3 run showing
  compounding beyond saturation reopens the witness side at fixed budget.
- O4. Any single counting-tree failure on exact designs at any (n,d)
  (predicted: never, at any sample size); or the definitional correction
  above.
- O5. The 40,000-hit mono2 run at (32,2) landing at 0.2632 rather than
  0.2763 (Lemma M's constant wrong, the stipulated-channel Bayes right for
  some deeper reason); or a kernel correction under which product
  semantics is exact.
- O6. The F_3 audit finding L(Q_i^rho) != 0 on any pigeon (the
  characteristic-uniform generator argument fails: the p-ary kernel is not
  the p = 2 kernel's analogue, and O6 must be rederived from scratch); or
  the first paper analyzing the chi-task at p != 2.
- O7. One posterior-1 answer pattern without co-linear 1s in the
  symmetry-class probe (a certificate mechanism outside the inventory); or,
  in the closing direction, a completeness proof of the inventory, which
  closes O7 by proving the classification true.
- Whole catalog. A super-polynomial AC0[2]-Frege lower bound for -PHP_n
  (the chi-hypothesis true at all degrees: O2, O3, O7 close as solved, the
  corpus's central open problem empties out) or a budgeted tree with error
  < k^{-O(1)} at the program's parameters d = (log k)^{O(l)} <= sqrt(n)
  (Omega(n,d) refuted at p = 2 and the p = 2 route via Theorem 6.1 closes,
  exactly as recorded in proof_complexity.md's correction block). Either
  outcome is the frontier moving, not the map failing; the map's job is to
  have said in advance which measurement would tell us which world we are
  in.

## STATUS UPDATE (2026-10-04, post deg3_theory.md)

- O2's open core narrows: the degree-3 slice is PROVED (Theorem 3' in
  deg3_theory.md; same d^2 ~ n boundary; star sum rules + wedge/Z certificate
  inventory). The remaining open quantifier is degree >= 4, for which the
  degree-3 template is the stated consumption target.
- O3/O4 unchanged (resolved in form at degree <= 2; boundary k^{-Theta(d^2/n)}).
- O5's Lemma M now has a degree-3 companion: the exact post3 (no verbatim
  no-lift, no asymptotic lift) is PROVED at degree 3; the degree-2 transfer
  proof (Lemma M proper) remains open.
- New sub-item: the wedge and Z certificates join the O7 trichotomy inventory
  (both certain, both rate-dominated by K_j).
