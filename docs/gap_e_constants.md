# GAP E: the constants of the budgeted boundary err*(d, d log k) at degree <= 2

Result of the gap-e agent (2026-10-04). Status: analysis + measurement, not
peer-reviewed. Scope: O2(ii) of open_problems.md, the exact constant in
$\mathrm{err}^*(d, e = d\log k) = k^{-\Theta(d^2/n)}$ at degree $\le 2$ on the
TRUE pipeline channel (deg2_theory.md facts F1-F5). Task brief: at (128,2)
with $e = 32$ the printed cap gives success $\approx 0.317$ while the best
witness achieves $\approx 0.06$; tighten the bracket from both sides,
numerically and analytically.

Deliverable pair: this file + `experiments/chi_gap_e_check.py` (registered run
at the foot). No other corpus file was edited; LOG.md was not touched.

## 0. Headline (all numbers MEASURED on the exact channel, 99% Clopper-Pearson)

The bracket at (128,2), $e = 32$ ($\log k = 16$), moves from
$[0.06,\ 0.317]$ to $[0.1264,\ 0.1864]$:

| point | printed cap | family-exact cap | DP model optimum | measured best policy | printed Thm 4b bound |
|---|---|---|---|---|---|
| (128,2), e=32 | 0.3170 | 0.1864 | 0.1269 | 0.1264 [0.1242,0.1286] | 0.0138 |
| (96,3), e=48 | 0.9513 | 0.6803 | 0.5515 | 0.5499 [0.5466,0.5532] | 0.0978 |
| (96,3), e=32 | 0.6924 | 0.4850 | 0.3429 | 0.3422 [0.3379,0.3465] | 0.0489 |

In error terms, $\mathrm{err}^* \in [0.814,\ 0.874]$ at (128,2),
$[0.320,\ 0.450]$ at (96,3) e=48, $[0.515,\ 0.658]$ at (96,3) e=32.

Three findings carry the tightening.

1. WITNESS UP, factor 1.5 to 1.8 (MEASURED + MODEL): the optimal ADAPTIVE
   certified
   tree beats the printed fixed-split Theorem 4b tree at every
   tested point (0.1264 vs 0.0706 at (128,2); 0.5499 vs 0.3592 at (96,3)
   e=48; 0.3422 vs 0.2070 at (96,3) e=32). Its exact value is computable at
   any $(n,d,e)$ by a small backward
   induction (Theorem E2); the model value and the measured value agree
   within Monte Carlo error at all three target points.
2. CAP DOWN, factor 1.4 to 1.7 (PROVED modulo the printed JDP steps): the
   printed certificate term $2(1-\exp(-ed/(4n)))$ charges a CONJUNCTION
   (column certification AND a found 1-entry) by roughly the probability of
   one factor alone: it is linear in $x = ed/n$ where the true certificate
   term is quadratic at leading order. The valid K-term is the exact adaptive
   chain supremum $\chi(e)$, computable by the same induction (Theorem E3/E4).
3. THE BRACKET COLLAPSES ONTO ONE QUANTITY: the cap's certificate term and
   the witness are the SAME number, $\chi(e)$, up to the fallback mass. The
   residual open mass is $(1-\chi)(q + A(e))$, i.e. whether any tree can
   realize the $q$-fallback on no-chain transcripts while keeping the chain
   budget intact (Conjecture E5). This replaces O2(ii)'s "constant factor in
   the exponent" with a sharper and computationally checkable question.

## 1. Setup

Channel: $\Omega(n,d)$ at $p=2$, kernel-verified law (open_problems.md F1-F5):
$\rho$ a uniform partial injection leaving free set $D$ ($2d+1$ pigeons) and
$R$ ($2d$ holes); the free-region single-answer matrix has independent rows,
each uniform over the odd-parity patterns on its $2d$ columns; $K_j =
1 + \sum_i x_{ij}$ answers 0 on killed columns and $1 + \mathrm{parity}_j$ on
free columns, so $K_j = 1$ certifies $j \in R$; same-line degree-2 products
answer 0 deterministically, diagonals are fair with the $Q$-shift sum rules.
The single-coordinate law is exact under the structural sampler (row parity is
the only single-coordinate constraint, kernel_structure.md F2/F3), which is
what the measurements run on.

Budget: $e = d\log k$ with $\log k = 16$ (the corpus's companion-check value,
open_problems.md O2 prediction): $e = 32$ at (128,2), $e = 48$ at (96,3);
$e = 32$ at (96,3) is run as a secondary point. With $x = ed/n$: $x = 0.5$,
$1.5$, $1.0$. Full answer-table Bayes enumeration (the cert_floor.md method)
is impossible here: the single-answer table has $(n+1)n \ge 9312$ bits at the
target points (16512 at (128,2)), so
the optimum is bracketed instead: exact family optimum below + proved cap.

Notation: $R = n+1$ (pigeons), $f = (2d+1)2d/((n+1)n)$ (free-pair mass),
$q = (2d+1)d/((2d+1)d + (n-2d))$ (per-hit posterior), $h_1 = f/2 +
(n-2d)/((n+1)n)$ (single-query answer-1 rate), $r_1 = d/n$ (K-certification
rate per query), $r_2 = (2d+1)/(2(n+1))$ (first-scan hit rate on a certified
column), $\rho = r_2/r_1 = (2d+1)n/(2d(n+1))$, $x = ed/n$.

## 2. Lemma E1 (exact certificate laws). PROVED; machine-verified [MV]

(i) $\mathrm{P}(K_j = 1) = d/n$ exactly: $\mathrm{P}(j \in R) = 2d/n$ and,
given $j$ free, the $2d+1$ free-pigeon bits of column $j$ are iid fair (rows
are independent uniform-odd patterns; each row's bit in a fixed column has
marginal $1/2$), so the column parity is even with probability exactly $1/2$.

(ii) The parity vector of the $2d$ free columns is uniform over the
$2^{2d-1}$ odd-XOR patterns: rows are iid uniform over the odd coset
$C = e + C_0$ of $\mathbb{F}_2^{2d}$ ($|C_0| = 2^{2d-1}$, the even code), and
the row-sum map $C^{2d+1} \to \mathbb{F}_2^{2d}$ has image $C$ (odd row count:
$e$ survives) with equal coset fibers.

(iii) Hence $\mathrm{P}(k\text{ certifications among } t\text{ queried free
columns}) = \binom{t}{k}2^{-t}$ for $t < 2d$, and at $t = 2d$:
$\binom{2d}{k}2^{-(2d-1)}$ if $2d - k$ is odd, else $0$
(known structure: the even-set has size $1$ or $3$ at $d = 2$, $1,3,5$ at
$d = 3$).

(iv) A certified column's bits are uniform subject to even column parity:
$\mathrm{P}(w\text{ ones}) = \binom{2d+1}{w}2^{-2d}$ ($w$ even), dud
(all-zero) probability $2^{-2d}$, and across $k$ certified columns the joint
dud probability is exactly $2^{-2dk}$: dud events are INDEPENDENT (count:
odd-row matrices with $k$ prescribed-zero columns total
$2^{(2d+1)(2d-k-1)}$, against $2^{(2d+1)(2d-1)-k}$ with $k$ prescribed even
parities; ratio $2^{-2dk}$). [MV, exhaustive at $d=2$ over $8^5$ matrices;
$10^6$-sample Monte Carlo at $d=3$.]

(v) Scanning a certified column on FRESH rows (no row reused across columns)
is exactly a coupon process: after $z$ zero answers, $\mathrm{P}(w \mid z)
\propto \mathrm{P}(w)\binom{R-w}{z}/\binom{R}{z}$ and the next fresh row hits
with probability $\mathbb{E}[w \mid z]/(R-z)$. Cross-column information in
shared rows is absent at $d=2$: the [MV] overlap conditional
$\mathrm{P}(M(r,c_1) = 0, M(r,c_2) = 0 \mid c_1, c_2 \text{ even}) =
0.2500$, the product of the marginals, so re-scanning a row gains nothing
and the fresh-row policy loses nothing.

(vi) Stage-1 transition, exact:
$\mathrm{p\_cert\_next}(n,d,u,k) = \mathrm{P}(\text{next fresh } K_j
\text{ certifies} \mid u \text{ distinct } K\text{-queries done}, k
\text{ certified})$, summed over $t = |R \cap Q|$ with hypergeometric weight
$\binom{2d}{t}\binom{n-2d}{u-t}/\binom{n}{u}$ times law (iii), times the
conditional next-column factor $\mathrm{P}(j\text{ free}\mid t)\,
\mathrm{P}(\text{even}\mid \text{free, history}) = \frac{2d-t}{n-u} \times
[\frac12 \text{ if } 2d-t \ge 2;\ \mathbb{1}[(t-k)\text{ odd}] \text{ if }
2d-t = 1]$. The determined case ($2d-t=1$) is essential: when one free
column remains unqueried, its parity is FIXED by the observed pattern (total
odd-XOR), not fair. [MV: exhaustive check over all $(u,k)$ states at (8,2),
digit-exact.]

(vii) Fallback values: with $k \ge 1$ certified columns and $m$ zero-scanned
rows, the pair (fresh row, certified column) is free with posterior
$(2d+1 - m\,p_{Dz})/(R - m)$, $p_{Dz} = \frac{2d+1}{2R}/(1 -
\frac{2d+1}{2R})$ (each zeroed row of a certified column carries D-posterior
$p_{Dz}$); with no certification the random-pair fallback is worth $f$. The
additivity over rows is the one MODEL clause (exact up to
$O(d^2/R^2)$ row-pair corrections); the (5,2) end-to-end brute force below
bounds its worst-case effect at 2.2 percentage points.

Proof status: (i)-(vi) are short exact computations on the kernel-verified
channel law; each clause is machine-checked in E1 of the registered run.
Nothing here uses the stipulated i.i.d.-coin channel.

## 3. Theorem E2 (the exact optimum of the certified family). PROVED as an
in-family statement; MEASURED on the exact channel

Certified family: adaptive trees whose queries are $K_j$ (fresh columns) and
single variables (fresh rows of certified columns), whose positive output is
a scanned 1-entry in a certified column (posterior exactly 1 by F5 +
Theorem 1 of deg2_theory.md), and whose fallback is (fresh row, certified
column) if any certification exists, else a random pair. State:
$(u, m, k, o, z)$ = (K-queries used, zero-scans used, certifications found,
certifications not yet opened, zeros on the opened column; $z = -1$: none
open). Actions: K (cost 1, transition law E1(vi)), NEXT (free: open a fresh
certified column), SCAN (cost 1: hit w.p. E1(v), else $z{+}1$, $m{+}1$),
FB (stop; value E1(vii)). Backward induction over this state space is exact:
by exchangeability the state is a sufficient statistic of the transcript, and
by Lemma E1 the transitions are the exact channel laws. Define:

  $W_{dp}(e)$ := the DP value at the root (total, certified fallback allowed);
  $W_{dp}^{ch}(e)$ := the chain-only variant (fallback value forced to $f$);
  $\chi(e) := (W_{dp}^{ch}(e) - f)/(1 - f)$ = the supremum over the family of
  the K-chain completion probability.

The DP policy in words: query $K_j$ on fresh columns until the first
certification, then open it and scan fresh rows until a hit or until the
value function prefers stopping; on budget exhaustion fall back to (fresh
row, certified column) worth $\approx \mathrm{P}(i \in D \mid \text{zeros})
\approx 0.044$ at (128,2), else random ($f = 0.0012$). Traces printed by the
run confirm this structure at the target points.

MEASURED (exact sampler, 150,000 sims): $W_{dp}$ vs realized:
(128,2): 0.12692 vs 0.12642 [0.1242, 0.1286]; (96,3) e=48: 0.55153 vs
0.54993 [0.5466, 0.5532]; (96,3) e=32: 0.34288 vs 0.34222 [0.3379, 0.3465].
All three model values sit inside the 99% intervals. Stress test: at (5,2),
$e = 6$, against the FULL exact configuration space (983,040 configurations
enumerated digit-exactly), the model value 0.99933 overestimates the realized
0.97760 by $-0.0217$ (all couplings maximally active at $R = 6$); the DP
policy is still the best of every grid policy tried. So the model clause
E1(vii) costs at most $\approx 2$ percentage points at toy scale and is
invisible at the target scale.

Degree-2 note: no degree-2 mechanism produces certificate leaves within
$o(n)$ budget (same-line products answer 0 deterministically; diagonal
products are fair coins whose 1-answers carry posterior $q_{\mathrm{and}}
\approx q$; the shift sum rules need $\Theta(n)$ queries per star,
deg2_theory.md F4 and Lemma REL). Measured: a diagonal-monomial scan at
(128,2), $e = 32$ on the exact design-space channel lands at 0.0202
[0.0182, 0.0224], at the level of the single-scan baseline 0.0176 and far
below the witness. So the family optimum is the degree-$\le 2$ optimum up to
the certificate-free mass, which the cap charges at $q$.

## 4. Theorem E3 (where the printed cap's constant dies). PROVED as an
identification; the cap itself inherits the printed JDP status

The printed cap (deg2_theory.md Theorem 3 / Corollary 3.1, open_problems.md
O2) is
  $\mathrm{success}(T) \le q + 2(1 - e^{-x/4}) + A(e) + o(1)$,
with $A(e) = \min(1, e h_1)\min(1, e q\frac{2d-1}{2(n-1)})$ the adjacency
term. Two slack steps are identifiable in the printed assembly.

(a) CONJUNCTION CHARGED AS DISJUNCTION (the order gap). A K-certificate leaf
requires the event "$K_j = 1$ for some queried $j$" AND "a 1-entry of a
certified column is found within budget". The printed $P_K(e) \le
2(1-e^{-ed/(4n)})$ bounds this conjunction by twice a single-stage
probability: after Corollary 3.1's linearization $1 - e^{-z} \le z$ the cap's
certificate term is $x/2$: LINEAR in $x$. The true term is the chain
supremum $\chi(e)$, which is quadratic at leading order (Section 5):
$\chi(e) = \frac{\rho}{2}x^2(1 + O(x))$. At the test points:
printed $2(1-e^{-x/4}) = 0.2350$ / $0.6254$ / $0.4424$ (linearized $x/2$ =
$0.25$ / $0.75$ / $0.50$) against $\chi$ = 0.1137 / 0.5257 / 0.3133. Near the
origin the slack is unbounded (linear vs quadratic); it shrinks as both
terms saturate.

(b) SPLIT CONSERVATISM (the constant gap). Theorem 4b's
$(1-e^{-ed/(4n)})^2$ uses exponent $1/4$; the split-optimal exponent constant
is $c_w = \rho/(1+\rho)$: fixing only the split,
$\mathrm{err} \le 2e^{-c_w x}(1+o(1))$ with $c_w = 0.55363$ ($d=2$),
$0.53589$ ($d=3$), a factor $2.21$ / $2.14$ in the exponent. Proof: both
stages run for $\beta = c_w x$ exponential units, so the product is exactly
$(1-e^{-\beta})^2$ and $1 - (1-e^{-\beta})^2 = 2e^{-\beta} - e^{-2\beta} \le
2e^{-\beta}$; the stage-2 linear-rate bound is valid by Jensen
($\mathrm{P}(\text{find} \mid w) \ge 1 - e^{-bw/R}$ pointwise in $w$, and
$\mathbb{E}[e^{-bw/R}] \ge e^{-b\mathbb{E}[w]/R}$); the stage-1 rate $d/n$ is
exact by Lemma E1(i) up to the clustering correction, which is $O(x/n)$ and
only HELPS (certifications cluster: $\mathrm{P}(k=0 \mid u) \le
(1-d/n)^u$ holds in every enumerated case). Status: same as the printed
Theorem 4b (whose independence step this reuses) plus Jensen; no new JDP
content.

(c) ADAPTIVITY (a second witness gap, measured). Even at the optimal split
the printed tree is a factor $\approx 2$ below the optimum at leading order:
the fixed split wastes its scan budget when no certification arrives in stage
1, and under-scans early certifications. The sequential policy
(K-until-cert, then all-in scan) achieves $\chi(e) \approx \frac{\rho}{2}x^2$
at small $x$, twice the split constant $\frac{\rho}{4}x^2$ (derivation:
chain $= \int_0^e r_1 e^{-r_1 u}(e-u)r_2\,du = \rho x^2/2\,(1 - x/3 +
\cdots)$). MEASURED: $\chi(e)/x^2$ = 0.512, 0.510, 0.485, 0.455 at $x$ =
0.125, 0.25, 0.375, 0.5 against the asymptote $\rho/2 = 0.6198$ (the gap is
the $O(x)$ and discreteness corrections, both downward). CONJECTURED: the
$\rho x^2/2$ asymptotic is the exact small-$x$ limit of the DP. At $x = 0.5$
the realized adaptive gain over the best fixed split is 1.79x (0.1264 vs
0.0706); at (96,3) e=48 it is 1.53x (0.5499 vs 0.3592).

## 5. Theorem E4 (the sharpened bracket). PROVED for the certified family
(exact); PROVED for all degree-$\le 2$ trees modulo the two printed JDP
composition steps of Theorem 3 (same citation status as Corollary 3.1)

For every adaptive degree-$\le 2$ tree $T$ of budget $e$ on the true channel,

  $\mathrm{success}(T) \le \chi(e) + (1 - \chi(e))\,(q + A(e))\,(1 +
  O(e/n) + o(1))$,

and some degree-1 tree achieves $\mathrm{success} \ge W_{dp}(e)$, both
quantities exact in the certified-family model at finite $(n,d,e)$ (Lemma E1
+ Theorem E2; the model is validated end-to-end on the exact channel at the
target points, Section 3). Proof: the
printed Theorem 3 assembly, with one change: the certificate-leaf mass is
bounded by the actual chain-event supremum $\chi(e)$ (an exact quantity, not
a relaxed bound) instead of the printed $P_K$; the adjacency certificates
that fire on no-chain transcripts are charged in the complement at $A(e)$;
certificate-free leaves are capped at $q(1 + O(e/n))$ by the printed
per-leaf dichotomy (Theorems 1-2). The bracket

  $W_{dp}(e) \ \le\ \mathrm{success}^*(e)\ \le\ \chi(e) + (1-\chi(e))(q +
  A(e)) + o(1)$

is the sharpened form of O2(ii) at degree $\le 2$. The two sides COINCIDE
in their certificate content: $\chi(e)$ is simultaneously the cap's
certificate term and (up to fallback harvest $W_{dp} - \chi \le
(1-\chi)\,\mathrm{P}(i \in D \mid \text{zeros}) < (1-\chi)q$) the witness's.
Residual gap at the test points: $0.060$ at (128,2), $0.130$ at (96,3) e=48,
$0.142$ at (96,3) e=32, i.e. exactly the unharvested $(1-\chi)(q+A)$ mass.

Leading constants (for the $k^{-\Theta(d^2/n)}$ form, $x = d^2\log k/n$):

  witness: $\mathrm{err}^* \le 2e^{-c_w x}(1+o(1))$, $c_w = \rho/(1+\rho) =
  \frac{(2d+1)n}{(2d+1)n + 2d(n+1)}$ = 0.55363 ($d=2$), 0.53589 ($d=3$);
  small-$x$: $\chi(e) = \frac{\rho}{2}x^2(1+O(x))$ =
  $\frac{2d+1}{4d}x^2(1+O(x))$ (adaptive; the printed split constant is half
  of it, $\frac{2d+1}{8d}x^2$);
  cap: $\mathrm{err}^* \ge 1 - q - A(e) - \chi(e) - o(1)$, with
  $\chi(e)$ exact and quadratic at leading order: the printed linear term
  $x/2$ is removed.

In the $k^{-C}$ bookkeeping at (128,2) ($k = 2^{16}$): the witness bound
gives $\mathrm{err} \le 0.874 = k^{-0.0122}$ where the printed Theorem 4b
bound gives $\mathrm{err} \le 0.9862 = k^{-0.0013}$ ($9.7\times$ in the
realized exponent constant at this point), and per unit of $x$ the exponent
constant improves from the printed $1/4$ to $c_w = 0.5536$ ($2.2\times$).

## 6. Measured inventory at the target points (all exact-channel, 99% CP)

(128,2), $e = 32$ (150,000 sims; degree-2 row: 30,000 on the design-space
channel):

| strategy | success | note |
|---|---|---|
| DP policy | 0.1264 [0.1242,0.1286] | model 0.1269: MATCH |
| best fixed split (s=16) | 0.0706 [0.0689,0.0723] | printed Thm 4b tree |
| split s=10 / 14 / 20 / 24 | 0.0584 / 0.0677 / 0.0691 / 0.0596 | split grid |
| split s=16, scan cap 8 / 4 | 0.0429 / 0.0267 | abandonment hurts here |
| single scan | 0.0176 [0.0168,0.0185] | $\approx e h_1 q$ |
| singles + K-check hybrid | 0.0185 [0.0176,0.0194] | pathwise >= single |
| diagonal monomial scan | 0.0202 [0.0182,0.0224] | no deg-2 certificates |
| (cap) printed | 0.3170 | O2's number |
| (cap) family-exact | 0.1864 | Theorem E4 |

(96,3), $e = 48$ (150,000 sims): DP 0.5499 [0.5466,0.5532] (model 0.5515);
best split s=26: 0.3592; single 0.0850; hybrid 0.0932; printed cap 0.9513
(vacuous); family cap 0.6803.
(96,3), $e = 32$ (80,000 sims): DP 0.3422 [0.3379,0.3465] (model 0.3429);
best split s=18: 0.2070; single 0.0648; hybrid 0.0689; printed cap 0.6924;
family cap 0.4850.

The DP outcome decomposition at (128,2): chain wins 0.1135, certified-column
fallback taken on 30.3% of episodes (winning 4.0% of those), random fallback
58.4% (winning $f = 0.0012$). The certified-column fallback alone is worth
+0.012 of success: the printed split tree leaves this on the table.

## 7. Boundary location (E6, exact DP sweep at (128,2))

The DP makes the boundary (success* = 1/2) a computation instead of a
guess. Computed exact values (chain-only DP per e; W_dp on a coarse grid):

| e | 8 | 16 | 24 | 32 | 40 | 48 | 56 | 64 |
|---|---|---|---|---|---|---|---|---|
| chi(e) | 0.0080 | 0.0319 | 0.0682 | 0.1137 | 0.1659 | 0.2226 | 0.2819 | 0.3423 |
| family cap | 0.0825 | 0.1059 | 0.1416 | 0.1864 | 0.2377 | 0.2934 | 0.3516 | 0.4107 |
| W_dp | - | - | - | 0.1269 | - | 0.2380 | - | 0.3583 |

Boundary readings (run lines quoted):
- COMPUTED: the family-exact cap is 0.4107 at e = 64, still below 1/2: the
  budgeted certification boundary at (128,2) lies beyond e = 64.
- INTERPOLATED (linear chi slope 0.00755 per query, labeled INTERPOLATED in
  the run): the family cap crosses 1/2 at e $\approx$ 80.
- COMPUTED (exact arithmetic, in-run): the PRINTED cap crosses 1/2 at
  e = 58.
- Witness side: W_dp(64) = 0.358; the same slope extrapolation puts the
  optimal-witness crossing at e $\approx$ 86, bracketing the true boundary
  from above.

So the certification boundary at (128,2) moves from e = 58 (printed cap,
computed) to e $\approx$ 80 (sharpened cap, interpolated), with the exact
optimum bracketed between the cap and witness crossings, $\approx$ [80, 86]
(both ends beyond the computed range are INTERPOLATED). In O2's boundary
language: at (128,2), $d = 2$, the hypothesis-friendly budget moves from
$\log k \approx 29$ to $\log k \approx 40$ before the witness side can kill
it. (96,3): chi(24) = 0.2033, cap(24) = 0.3813 (computed); cap(32) = 0.4850
and cap(48) = 0.6803 (computed in E4/E5): the (96,3) boundary sits at
e $\approx$ 34 (interpolated between the two computed caps), consistent with
the larger certificate rates at d = 3.

## 8. Conjecture E5 (the residual question). CONJECTURED, with measured
evidence

  $\mathrm{success}^*(e) = W_{dp}(e) + o((1-\chi(e))\,q)$, i.e. no tree
  realizes materially more than the family fallback on the no-chain event.

The cap's complement charges $q + A(e)$; the family harvests only the
certified-column fallback ($\approx \mathrm{P}(i \in D) \approx 0.044$ at
(128,2), below $q = 0.0746$). To realize $q$ a tree must spend queries on
singles (a hit carries posterior $q$), and every measured reallocation loses
more chain than it gains fallback: hybrids land at 0.0185-0.0194 against the
witness 0.1264 at (128,2), 0.0932 against 0.5499 at (96,3) e=48. Precise
open question: is
$\sup_T [\mathrm{success}(T) - W_{dp}(e)] = o((1-\chi(e))q)$, or is there a
budget-reallocation tree that beats the family by a non-vanishing fraction
of $(1-\chi)q$? A negative answer closes O2(ii) at degree $\le 2$ up to the
JDP steps; a positive answer would need a mechanism outside the
certified/certificate-free dichotomy (Theorems 1-2 bound every such
mechanism by $q$ per leaf, so the total is bounded by
$(1-\chi)q$ regardless: the question is only whether the bound is attained).

## 9. What this resolves in O2(ii)

1. The printed bracket [0.06, 0.317] at (128,2) is replaced by
   [0.1264, 0.1864] (MEASURED + PROVED-modulo-JDP): a $4\times$ narrower
   interval, with the witness side now backed by an exact computation rather
   than a point design.
2. The "constant factor in the exponent" is resolved into three named
   quantities: the union-for-conjunction slack (linear vs quadratic, the
   dominant cap-side term, now removed), the split-exponent conservatism
   ($1/4 \to 0.554$, factor 2.2), and adaptivity (factor $\approx 2$ at
   leading order, now provably available through the DP).
3. The exact budgeted optimum at ANY $(n,d,e)$ is computable in seconds by
   the registered script (Theorem E2): O2(ii) at degree $\le 2$ is no longer
   a search problem but a proof problem (upgrade the in-family exactness to
   the full class by demodularizing the two JDP steps; then close E5).
4. Scope guard: all statements are at degree $\le 2$; the O2 open core at
   degree $\ge 3$ (O2(i)) is untouched by this deliverable.

## 10. Falsifiable predictions (true channel, 99% CP)

1. Any adaptive degree-$\le 2$ tree at (128,2), $e = 32$, exceeding success
   0.20 falsifies the sharpened cap ($0.1864 + o(1)$) or the certificate
   dichotomy (Theorems 1-2) behind it. Exceeding 0.135 falsifies Conjecture
   E5 (a tree beating the family optimum materially).
2. The DP policy re-measured at 150,000 sims lands in [0.1242, 0.1286];
   the model value 0.12692 stays within 2 sigma of any rerun.
3. $\chi(e)/x^2$ at (128,2) stays above 0.45 for all $e \le 32$ (bounded
   below by the measured adaptive gain over $\rho x^2/4$) and rises toward
   $\rho/2 = 0.6198$ as $e \to 0$.
4. At (5,2), $e = 6$, no degree-1 policy among single-scan / any fixed
   split / the DP policy exceeds 0.98 exact success (current best 0.97760).

## 11. Registered run

    python3 experiments/chi_gap_e_check.py          # full, ~10 min
    python3 experiments/chi_gap_e_check.py --smoke  # ~1 min

Seeds: 271828 (channel/policy MC), 20261004 (E1 d=3 law). Output fields:
E1 (Lemma E1 laws, exhaustive at d=2, 10^6-sample at d=3), E3 ((5,2)
brute-force, 983,040 configurations), E4/E5 (target-point tables, caps,
bracket lines), E6 (boundary sweep). Registered output of record: the full
run transcript; key lines quoted above.

Environment: python3 only, imports chi_deg2_theory_check (same directory,
which imports razborov_check) for the exact structural sampler and
Clopper-Pearson intervals; disk use negligible.
