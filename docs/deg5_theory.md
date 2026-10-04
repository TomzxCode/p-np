# Degree-5 extension of the true-pipeline theory: the degree-5 column
# classification (Theorem A at k = 5, with a sparse-sweep verification of the
# partition at d = 5), the degree-5 star sum rules, the exact per-hit
# posterior post5, the certificate search, the budgeted cap Theorem 3''', and
# the general-d induction assessment

Result of the deg5-theory agent (2026-10-04). Status: analysis, not
peer-reviewed. Task: extend the degree-$\le 4$ theory (deg4_theory.md) to
degree 5 on five questions: (1) the degree-5 column classes (fixed-0, alias,
matching-5 varying), (2) the degree-5 star sum rules, (3) the exact per-hit
posterior post5 and the no-asymptotic-lift comparison with post4 and $q$,
(4) an exhaustive small-case certificate search beyond the inventory,
(5) the cap extension (Theorem 3''') plus a precise statement of what a
general-$d$ induction needs.

Channel: the TRUE $\Omega(n,d)$ pipeline at $p = 2$ (uniform designs of the
restricted canonical system; kernel_structure.py F1:
$V(n,d)^\rho = V(2d,d)$).
Script: chi_deg5_check.py (registered run, 21 s, ALL PASS; smoke variant
15 s; output reproduced at the end).
Everything is on the true channel.
Markers: [PROVED], [MEASURED], [MV] machine-verified, [CONJECTURED], [GAP],
[ASSEMBLY] (cap assembled from proved pieces modulo the two inherited JDP
composition flags).

## 0. Summary (the five answers in one paragraph each)

Q1 (degree-5 classes). [PROVED + MV] Every degree-5 column at every
restricted $(2d,d)$ with $d \ge 5$ is exactly one of three mechanism
classes: (i) FIXED 0: all-distinct containing a line pair (a literal
generator monomial: collision or two-hole pair times three further cells),
(ii) ALIAS: containing a repeated variable, value = the value of its
square-free reduction (Boolean-identity family; the degree-5 reduction
system has the six patterns $x^5 \to x$, $x^4y \to xy$, $x^3y^2 \to xy$,
$x^3yz \to xyz$, $x^2y^2z \to xyz$, $x^2yzw \to xyzw$; fixed 0 exactly when
the reduction is same-line), (iii) VARYING: all-distinct with no line pair,
i.e. matching-5, which varies by Theorem A at $k = 5$ (base machine-checked
at the $(10,5)$ slice: 0/110 singles determined, 4950/4950 matching-2
varying; star-row steps witnessed).
Counts at $(10,5)$: alias 24,411,750 (to-0 17,026,240, to-varying
7,385,510); all-distinct 122,391,522 = matching-5 13,970,880 + line-pair
108,420,642; the partition identity
$125{,}446{,}882 + 21{,}356{,}390 = 146{,}803{,}272 = \binom{114}{5}$ holds
exactly.
NEW INSTRUMENT RESULT: a sparse degree-$\le 3$ sweep at $(10,5)$ (234,136
columns, 196,581 sparse generator rows, 151,097 pivots, max pivot row 38
terms, 3 s) verifies the three-class partition BY FULL SWEEP at $d = 5$ for
degree $\le 3$: the determined set is exactly $\{e_0\}$ + same-line
degree-2 (1,045) + $x^2y$ with same-line reduction (2,090) + all-distinct
line-pair triples (97,020) = 100,156, and every other class varies (singles
110, squares 110, diagonals 4,950, cubes 110, alias-to-diagonal 9,900,
matching-3 118,800).
This is the first sweep verification of the partition beyond $d \le 3$, and
it gives direct sweep evidence that all 118,800 matching-3 columns vary at
$d = 5$.

Q2 (star sum rules). [PROVED + MV] The degree-5 stars: for any pigeon $p$
and matching-4 $g_4$ with $p$ outside it, the generator row $Q_p \cdot g_4$
(degree $5 = d$) gives
$\bigoplus_{j \in R \setminus \mathrm{holes}(g_4)}
\mathrm{ans}(x_{pj} g_4) = \mathrm{ans}(g_4) \cdot [p \in D]$, with the
injectivity automatism $\rho(p) \in \mathrm{holes}(g_4) \Rightarrow
\mathrm{ans}(g_4) = 0$.
The structural form and legality were machine-checked at $(10,5)$ for all
star degrees 2 through 5, and the status decomposition (live terms,
killed-elsewhere, fresh-terms-killed, automatism) is exact over all 132
restrictions at outer $(11,5)$ for two $(p, g_4)$ choices.
The degree-$\le 4$ stars persist; the alias relations gain the six-pattern
degree-5 family (per-query, configuration-invariant, zero information).
REL-5 therefore has six completion classes: free rows (cost $\Theta(n)$),
degree-2 stars ($n-1$), degree-3 stars ($n-2$), degree-4 stars ($n-3$), NEW
degree-5 stars ($n-4$), alias pairs (per-query, info-free).
No other determined-relation class is known at degree 5; the completeness
status of that negative claim is exactly the missing lemma of Section 6.

Q3 (exact per-hit posterior). [PROVED + MV; finite-n MEASURED] For a
matching-5 $T$,
$\mathrm{post}_5 = P[p_1 \text{ free} \mid \mathrm{ans}(T) = 1] =
\frac{b_0 + 4b_1 + 6b_2 + 4b_3}{2b_5 + b_0 + 5b_1 + 10b_2 + 10b_3 + 5b_4}$
with $b_m = \binom{n-4}{c-m}\binom{n-5}{c-m}(c-m)!$, digit-exact against
exhaustive enumeration at outer $(11,5)$ [46/47, both quints, 132
restrictions], $(12,5)$ [703/733, 10,296], $(13,5)$ [18362/19517, 624,624].
Leading form [PROVED from the closed form]:
$\mathrm{post}_5 = \frac{2d^2+d}{c-4}(1+o(1))$ at fixed $d = 5$, $c \to
\infty$; measured ratio $\mathrm{post}_5/\mathrm{post}_4 = 1.000546$ at
$(65535,5)$: NO asymptotic lift.
No-asymptotic-lift conjecture NAL stated (all degrees $k$): every
single-pass per-hit posterior shares the leading form $2d^2/n$ and the
pairwise ratios tend to 1; PROVED for $k \le 5$ from the closed forms,
CONJECTURED for all $k$.
Finite-$n$ [MEASURED, exact arithmetic]: $\mathrm{post}_5 -
\mathrm{post}_4$ is negative for $n \le 127$ and positive for $n \ge 255$
at $d = 5$; $\mathrm{post}_5$ exceeds $q_{\mathrm{and\_exact}}$ by up to
$+13.0\%$ relative (sup 1.1297 at $(255,5)$), the same purity pattern as
degrees 3 and 4, one degree stronger and vanishing as $\Theta(d^2/n^2)$.

Q4 (certificates). [PROVED + MEASURED] The certain inventory does NOT grow
at degree 5.
The answer-1 mass chain extends with the general-k event-inclusion proof:
$P_{k+1} < P_k$ at fixed $(n,d)$ for all $k$ (strict event inclusion on the
common configuration space), verified exactly at 10 grid points with
$d \in \{5, 6, 7\}$: $P_5 < P_4 < P_3 < P_2 < P_1 = h_1$ (e.g. $P_5 =
9.879 \times 10^{-6}$ against $P_1 = 7.66 \times 10^{-2}$ at $(31,5)$), so
$P_5$ is dominated by the $K_j$ rate $d/n$ by factors $1.6 \times 10^{4}$
to $4.3 \times 10^{12}$ across the grid.
The exhaustive-plus-sampled F1 search at outer $(11,5)$ (5x5 window pool of
1,545 matching-class queries; exhaustive singles, exhaustive
(m5, single) and (m5, m2) pairs, sampled (m5, m3/m4/m5) and general pairs,
triples, quads) found every F1-certain pattern explained by wedge/Z plus
the $c = 1$ shadow-pin artifact; unexplained 0.
Targeted degree-5 wedge and Z certificates are sound over all 132
restrictions.
Self-certification is vacuous at $p = 2$ ($\mathbb{F}_2 \setminus
\{0,1\} = \emptyset$).

Q5 (cap and the induction). [ASSEMBLY, two inherited JDP flags] Theorem
3''' extends the budgeted cap to the full adaptive degree-$\le 5$ class:
$\mathrm{success}(T) \le \min(1,\ q_5^* + P_{\mathrm{adj}} + P_K +
P_{\mathrm{cert5}} + P_{\mathrm{blk5}} + o(1))$ with
$q_5^* = \max(q, q_{\mathrm{and\_exact}}, \mathrm{post}_3, \mathrm{post}_4,
\mathrm{post}_5)$, $P_{\mathrm{cert5}} \le e \cdot P_5 = o(P_K)$,
$P_{\mathrm{blk5}} \le e/(n - 2d - 4)$.
The chi-hypothesis stays alive exactly when $d^2 \log k = o(n)$: the SAME
boundary through degree 5.
Measured cap at $(4095,5)$, $e = 80$: 0.0816 (ALIVE), the $K_j$ term first
to bite, as at every degree.
The general-d induction step is stated precisely in Section 6: Theorem A
plus mass monotonicity close every per-degree ingredient (classification,
star class, posterior, certificate mass) EXCEPT the completeness of the
relation inventory; the exact missing lemma is SPARSE-d (Section 6.3), the
general-$d$ form of Lemma CLS.

## 1. The instrument wall at d = 5, and the replacement instruments

Degree-5 monomial columns exist only for $d \ge 5$, so the smallest
restricted system carrying them is $(10,5)$ = 11 pigeons x 10 holes = 110
variables (restricted systems are $(2d,d)$, so there is no "$(8,5)$"
restricted system), and the smallest outer pipeline is $(11,5)$
($c = 1$, 132 restrictions, all enumerable).
The monomial space is $|S(10,5)| = \binom{114}{5} = 146{,}803{,}272$
degree-5 columns.
The deg3-style full augmented echelon needs pivot rows of 146.8M bits =
18 MB each; at the measured pivot fractions (0.71 to 0.86) that is 2.3
petabytes and change: the deg4 wall (167-180 GB at $d = 4$) is crossed by
four orders of magnitude.
Even the degree-$\le 4$ slice (6.0M columns, about 9.1M sparse rows) has a
pivot store projected at 5-15 GB against 15 GB of shared machine RAM under
concurrent agent load: declared infeasible and not attempted.
What replaces it (instruments a-e, all exercised this run):

  (a) Degree-$\le 2$ slice echelon at $(10,5)$: 2,376 generator rows over
      6,216 columns, 2,212 pivots, exact; verifies the Theorem-A base at
      $d = 5$ (0/110 singles determined, 4950/4950 matching-2 vary) and the
      conformance anchors D4/D6/D7, L1, F5. [MV this run]
  (b) NEW: SPARSE degree-$\le 3$ sweep at $(10,5)$: 234,136 columns, rows
      carried as sets of monomial indices (max 11 terms before
      elimination), pivot store 151,097 rows of at most 38 terms, runtime
      3 s, memory a few hundred MB.
      This is the deg3 full-sweep instrument resurrected one slice higher
      than deg4 could reach: the partition is verified BY SWEEP at
      degree $\le 3$, $d = 5$. [MV this run]
  (c) Witness algebra: alias chains (all six degree-5 reduction patterns,
      each an explicit sum of legal generator shifts of degree $\le 5$),
      star rows $Q_p \cdot g_k$ for $k = 2, 3, 4$, and line-pair generator
      monomials at degree 5; no echelon involved. [MV this run]
  (d) Theorem A at $k = 5$ (the proved star induction): reduces
      matching-5 variation to the base, machine-checked in (a), with the
      matching-3 link additionally confirmed by the sweep in (b).
  (e) F1-level outer enumeration over restrictions only, exact because the
      per-$\rho$ answer law is $\{0, 1/2, 1\}$ once Theorem A + balance
      hold: exhaustive at $(11,5)$ [132], $(12,5)$ [10,296], $(13,5)$
      [624,624]. [PROVED soundness; the channel law it consumes is
      channel_spec.md rows D1-D12 + I7]

Instrument notes (corrections made during the run, per corpus discipline):
(1) the $x^5 + x^3$ alias witness was first written as $(x^2+x)x^3$, which
is $x^5 + x^4$ (algebra slip caught by the script's sum check); corrected
to the 2-row chain $(x^2+x)x^3 + (x^2+x)x^2$.
(2) the line-pair generator-monomial witness first shifted the generator
poly by the full monomial (repeating the pair cells); caught by the
structural check; corrected to shift by the three remaining cells only.
(3) a first hand count of the degree-5 alias-to-0 mass used set-counts
where the monomial class is ordered ($x^4y$, $x^3y^2$, $x^2y$ each carry a
factor 2); the sweep's 2,090 determination count at degree 3 exposed the
slip and the partition identity now asserts the corrected total
17,026,240.
(4) the $(11,5)$ F1 search samples raw query sets rather than symmetry
classes: the $S_5 \times S_5$ window group has 14,400 elements, and
canonicalizing even the 1.19M raw pairs is out of reach, so the search is
exhaustive only over singles and the (m5, single)/(m5, m2) pair families
and sampled elsewhere; the completeness statement is correspondingly a
sampled statement at this scale.
(5) one full-run attempt was killed by ambient memory pressure (concurrent
agents, swap full), not by the script: the script's own peak stays a few
hundred MB.

## 2. Q1: the degree-5 classification and Theorem A at k = 5

### 2.1 The three mechanism classes at degree 5

Lemma W5 (fixed-0 class). [PROVED] Any all-distinct degree-5 monomial
containing two cells that share a pigeon (distinct holes) or a hole
(distinct pigeons) is a generator monomial (line pair times three
variables, degree 5), hence determined 0.
The script verifies two representatives as single-term generator rows and
the sweep verifies the whole degree-3 layer of this class (97,020/97,020
determined at $(10,5)$).

Lemma A5 (alias class). [PROVED + MV] Any degree-5 monomial with a
repeated variable $x$ satisfies
$\mathrm{ans}(m) = \mathrm{ans}(\mathrm{sqfree}(m))$, where the
square-free reduction has degree $\le 4$.
The degree-5 reduction system has exactly six patterns (the partitions of
5 with a part $\ge 2$; in general $p(k) - 1$ patterns at degree $k$, $p$
the partition function), each with an explicit witnessed chain (sums of
legal generator shifts, machine-checked):
  $x^2 + x$                    (the Boolean generator, 1 row),
  $x^3 + x$                    (2 rows),
  $x^4 + x^2$                  (2 rows),
  $x^4 + x$                    (3 rows),
  $x^5 + x^3$                  (2 rows),
  $x^5 + x$                    (4 rows, telescoping),
  $x^2y + xy$                  (1 row),
  $x^3y + xy$                  (2 rows),
  $x^2y^2 + xy$                (2 rows),
  $x^3y^2 + xy$                (3 rows: $(x^2+x)xy^2 + (x^2+x)y^2 +
                                (y^2+y)x$),
  $x^4y + xy$                  (3 rows),
  $x^2yz + xyz$                (1 row: $(x^2+x)yz$),
  $x^2y^2z + xyz$              (2 rows),
  $x^2yzw + xyzw$              (1 row: $(x^2+x)yzw$).
As at degree 4, nothing new arises from higher field equations: over the
Boolean rows $x^k = x$ for all $k \ge 1$, so the alias class is exactly
the Boolean-identity family.
Fixed 0 exactly when the reduction is same-line (the reduction's own
class decides).

Theorem A at $k = 5$. [PROVED step (deg4_theory.md); base MV this run]
At $(10,5)$: singles 0/110 determined and matching-2 4950/4950 varying
(slice echelon); matching-3 118,800/118,800 varying (sparse sweep); the
star rows $Q_p \cdot g_2, Q_p \cdot g_3, Q_p \cdot g_4$ witnessed legal
(degrees 3, 4, 5 $\le d$); orbit closure under $S_{11} \times S_{10}$.
Hence every matching-4 and every matching-5 column varies at $(10,5)$, and
(balance lemma) every matching-$k$ answer is a fair coin, $1 \le k \le 5$.
Direct machine evidence reaches matching-3; matching-4 and matching-5 rest
on the proved induction.

Counts at $(10,5)$ [MV arithmetic; the counting rules verified exactly on
the complete 5x5 subgrid (all 118,755 degree-5 monomials classified by
direct cell inspection)]:

  class                  count        status
  alias x^5              110          varying (= ans(x))
  alias x^4y             11,990       2,090 fixed-0 / 9,900 varying
  alias x^3y^2           11,990       2,090 fixed-0 / 9,900 varying
  alias x^3yz            647,460      291,060 fixed-0 / 356,400 varying
  alias x^2y^2z          647,460      291,060 fixed-0 / 356,400 varying
  alias x^2yzw           23,092,740   16,439,940 fixed-0 / 6,652,800 varying
  all-distinct line-pair 108,420,642  fixed-0
  matching-5             13,970,880   varying
  TOTAL                  146,803,272  125,446,882 fixed-0 / 21,356,390 varying

  alias total            24,411,750   17,026,240 to-0 / 7,385,510 to-varying
  partition identity: 125,446,882 + 21,356,390 = 146,803,272 = C(114,5)

Lemma D5 (degree-$\le 3$ determination at $(10,5)$, by sweep). [MV] The
sparse sweep of all 234,136 degree-$\le 3$ columns gives determined
exactly 100,156 = 1 ($e_0$) + 1,045 (same-line degree-2) + 2,090 ($x^2y$
with same-line reduction) + 97,020 (all-distinct line-pair triples), and
no other column: singles 110, squares 110, diagonals 4,950, cubes 110,
$x^2y$ with diagonal reduction 9,900, matching-3 118,800 all vary.
This extends the deg3 exact classification from $(6,3)$ to $(10,5)$: the
three-class partition is sweep-verified at $d = 5$ for degree $\le 3$.

## 3. Q2: degree-5 star sum rules (Theorem B5) and REL-5

Theorem B5 (degree-5 stars). [PROVED + MV] For any pigeon $p$ and
matching-4 $g_4$ with $p$ outside it, the row $Q_p \cdot g_4$ (degree
$5 = d$, a generator row) gives, for every $(\rho, L)$:
  $\bigoplus_{j \in R \setminus \mathrm{holes}(g_4)}
   \mathrm{ans}(x_{pj} \cdot g_4) = \mathrm{ans}(g_4) \cdot [p \in D]$,
with the automatism: if $\rho(p) \in \mathrm{holes}(g_4)$ then
$\mathrm{ans}(g_4) = 0$ (the $g_4$ cell at that hole carries a different
pigeon and is killed-unmatched).
Machine checks: the structural form of $Q_p \cdot g_4$ at $(10,5)$
(degrees 3, 4, 5 star rows all witnessed), and the status decomposition at
outer $(11,5)$ over ALL 132 restrictions for two $(p, g_4)$ choices
(p = 4 diagonal $g_4$, p = 9 non-diagonal $g_4$): live-term structure 0
errors, killed-elsewhere 0 errors, fresh-terms-killed 0 errors, automatism
0 errors.
The stars relate degree-5 answers to degree-4 answers exactly as the
degree-4 stars relate degree-4 to degree-3: the right-hand side is
status-dependent ($[p \in D]$), and the same non-realizability remark as
deg3 Section 4 applies verbatim (the fresh set $R \setminus
\mathrm{holes}(g_4)$ is $\rho$-hidden, so the star identity cannot be
probed into a certainty certificate).

REL-5 (block completion at degree $\le 5$). [PROVED structure] A
degree-$\le 5$ transcript observes a determined relation only if it
completes (a) a free row (2d coordinates, cost $\Theta(n)$, rows
$\rho$-hidden), (b) a degree-2 star (cost $n-1$), (c) a degree-3 star
($n-2$), (d) a degree-4 star ($n-3$), (e) NEW a degree-5 star
($\mathrm{ans}(g_4)$ + the fresh matching-5 terms, cost $n-4$), or (f) an
alias pair ($x^5$ with $x$, $x^4y$ and $x^3y^2$ with $xy$, $x^3yz$ and
$x^2y^2z$ with $xyz$, $x^2yzw$ with $xyzw$; per-query, but
configuration-invariant, zero information).
An adversarial transcript pays $\Theta(n)$ per completed star, giving
$p_{\mathrm{blk5}}(e) \le e/(n - 2d - 4)$ plus the spread bound; at
$e = d \log k = o(n)$ both are $o(1)$.
Completeness status: as at REL-4, the inventory is structural (derived
from the classification + star templates), and the sweep now backs it by
computation at degree $\le 3$, $d = 5$; at degrees 4 and 5 the negative
claim ("no other class") is exactly the SPARSE-d lemma of Section 6.3,
still open.

## 4. Q3: Theorem C5, the exact per-hit posterior post5

Theorem C5. [PROVED + MV] Fix a matching-5 $T$ and the event
$\mathrm{ans}(T) = 1$.
Per $\rho$: the answer is 1 if all five pairs of $T$ are matched, 1/2 if
no pair is killed and at least one is free (the free part is a
matching-$j$ column, $j \ge 1$, varying by Theorem A, fair by balance),
0 if any pair is killed.
Bayes over the per-subclass counts
$b_m = \binom{n-4}{c-m}\binom{n-5}{c-m}(c-m)!$ gives
  $\mathrm{post}_5 = \frac{b_0 + 4b_1 + 6b_2 + 4b_3}
                {2b_5 + b_0 + 5b_1 + 10b_2 + 10b_3 + 5b_4}$.
Verified digit-exact (rational equality) against exhaustive enumeration at
$(11,5)$ [46/47 = 0.978723, both quints, 132 restrictions], $(12,5)$
[703/733 = 0.959072, 10,296], $(13,5)$ [18362/19517 = 0.940821, 624,624].
This closes the $k \le 5$ case of the deg4 general-$k$ closed form.

Asymptotics. [PROVED from the closed forms]
$b_4^{(5)}/b_5^{(5)} = (2d+1)(2d)/(c-4) = 110/(c-4)$ at $d = 5$, and the
numerator and denominator are dominated by their $m = 4$ and $m = 5$
terms once $c \gg 4d^2$, giving
  $\mathrm{post}_5 = \frac{55}{c-4}(1+o(1))$ at $d = 5$,
so all single-pass per-hit posteriors $k = 1, \ldots, 5$ share the leading
form $2d^2/n$: measured $\mathrm{post}_5 \cdot (c-4)/55 = 1.00129$ and
$\mathrm{post}_5/\mathrm{post}_4 = 1.000546$ at $(65535,5)$; at $d = 6, 7$
the same holds ($1.0310$, $1.0368$ at $(1023,d)$).

Conjecture NAL (no asymptotic lift, all degrees). [CONJECTURED; $k \le 5$
PROVED] For every fixed $d$ and every fixed $k \ge 1$:
$\mathrm{post}_k(n,d) = \frac{2d^2+d}{c-k+1}(1+o(1))$ as $c \to \infty$;
equivalently $\mathrm{post}_k/q \to 1$ and $\mathrm{post}_k/\mathrm{post}_h
\to 1$ for all fixed $k, h$; and the finite-$n$ excess
$\sup_n (\mathrm{post}_k - q_{\mathrm{and\_exact}})$ is $o(1)$, attained at
$n = \Theta(d^2)$.
Test at $k = 5$ [MEASURED, exact arithmetic, grid
$n \in \{11, \ldots, 65535\}$ at $d = 5$]:
  - $\mathrm{post}_5 - \mathrm{post}_4 < 0$ for $n \le 127$,
    $> 0$ for $n \ge 255$: the sign change sits between $n = 127$ and 255
    at $d = 5$ (degrees 3 and 4 showed the same flip near $c \approx
    2d^2$).
  - $\sup \mathrm{post}_5 / q_{\mathrm{and\_exact}} = 1.1297$ at
    $(255,5)$: a finite-$n$ purity lift over the degree-2 hit, one degree
    stronger than post4's 1.084 at $(255,4)$, vanishing as
    $\Theta(d^2/n^2)$ (1.0016 at $(65535,5)$).
  - $\mathrm{post}_5$ exceeds the single posterior $q$ by up to $+23.8\%$
    relative at $(255,5)$ (0.2270 against 0.1833).
Nothing here lifts the ASYMPTOTIC constant: the family
$\{q, q_{\mathrm{and\_exact}}, \mathrm{post}_3, \mathrm{post}_4,
\mathrm{post}_5\}$ has max $q_5^*$ achieved by post3 (small $n$), post4
($(127,5)$) and post5 ($n \ge 255$), all with the same leading form.

## 5. Q4: certificates at degree 5

Proposition M5 (mass chain, general k). [PROVED + MV] On the common
configuration space (all $(D, R, \mu)$ with $c = n - 2d$), let $A_k$ be
the event that a fixed matching-$k$ set is all matched and $B_k$ the event
that it has no killed pair; then
$P_k = P[\mathrm{ans}(\text{matching-}k) = 1] = P(A_k) +
\tfrac{1}{2} P(B_k \setminus A_k)$.
For $S \subset S'$ with $|S| = k$, $|S'| = k+1$: $A_{k+1} = A_k \cap
\{(u,v) \text{ matched}\}$ and $B_{k+1} = B_k \cap \{(u,v) \text{ not
killed}\}$ are strict subsets whenever a strictness configuration exists
($c \ge 1$, $k + 1 \le d$), so $P_{k+1} < P_k$ for all $k$.
This upgrades deg4's measured chain to a general-k proof.
Verified exactly at 10 grid points ($d = 5, 6, 7$):

  point      P1        P2        P3        P4        P5
  (31,5)     7.66e-2   8.33e-3   9.29e-4   9.86e-5   9.88e-6
  (127,5)    1.06e-2   1.21e-4   1.44e-6   1.75e-8   2.14e-10
  (1023,5)   1.02e-3   1.04e-6   1.07e-9   1.10e-12  1.13e-15
  (63,6)     3.20e-2   1.32e-3   5.76e-5   2.46e-6   1.01e-7
  (1023,7)   1.06e-3   1.14e-6   1.23e-9   1.34e-12  1.46e-15

$P_1 = h_1$ exact at every point; $P_5/K_j$ ratios $6.1 \times 10^{-5}$
($(31,5)$) to $2.3 \times 10^{-13}$ ($(1023,5)$), i.e. the $K_j$ channel
dominates $P_5$ by factors $1.6 \times 10^4$ to $4.3 \times 10^{12}$.
Consequence: every certain certificate consuming degree-5 evidence fires
at rate $\le e \cdot P_5 = o(P_K)$, strictly dominated by the degree-1
channels, as at degree 4.

Exhaustive-plus-sampled search at outer $(11,5)$ [MEASURED, F1-level,
exact]. Pool: all 1,545 matching-class monomial queries on a 5x5 window
(25 singles + 200 matching2 + 600 matching3 + 600 matching4 + 120
matching5; the 4x4 window of deg4 cannot hold a matching-5).
Constant-0 and alias queries are excluded with the proved reasons.
Scanned: ALL 25 singleton classes; ALL 3,000 (m5, single) and ALL 24,000
(m5, m2) pair classes; 3,000 sampled (m5, m3/m4/m5) pairs; 5,000 sampled
general pairs; 4,000 sampled triples; 1,200 sampled quads.
Every answer pattern's F1-consistency was evaluated over all 132
restrictions. Results:
  singletons:          0 certain patterns,
  (m5, single) pairs:  3,000 certain = 720 wedge/Z + 2,280 shadow(c=1),
  (m5, m2) pairs:      22,800 certain = 1,560 wedge/Z + 21,240 shadow,
  (m5, *) sampled:     2,947 certain = 186 wedge/Z + 2,761 shadow,
  general pairs:       4,818 certain = 418 wedge/Z + 4,400 shadow,
  triples:             15,484 certain = 1,220 wedge/Z + 14,264 shadow,
  quads:               12,849 certain = 839 wedge/Z + 12,010 shadow,
  UNEXPLAINED:         0.
The wedge and Z templates were applied at all degrees (they are
degree-generic); the shadow tag is the $c = 1$ consistency-pin artifact,
provably inert once $c > 9$.
Targeted soundness over all 132 restrictions: the degree-5 wedge (two
answer-1s on $x_{pj_1} g_4$, $x_{pj_2} g_4$, distinct fresh holes,
certifies $p$ free) and the degree-5 Z (single 0 + containing matching-5
answer-1 certifies the pair free) have 0 violations.

Verdict: degree-5 answers combined with lower-degree collision structure
produce NO new certain mechanism and NO better budget scaling.
Inventory conjecture update (O7): the certain inventory $\{$co-linear 1s,
co-vertex 1s (wedge, any degree), zero-single + containing 1 (Z, any
degree), $K_j = 1$, counting, shadow-pins (toy $c$ only)$\}$ is COMPLETE
at degree $\le 5$ at the searched scale; the completeness direction at
general scale rests on the $(7,3)$ exact search (deg3), the $(9,4)$
class-level search (deg4), and this $(11,5)$ search (exhaustive in the
singles and (m5, single)/(m5, m2) families, sampled elsewhere).
Self-certification remains n/a at $p = 2$.

## 6. Q5: Theorem 3''' (the cap at degree <= 5) and the induction assessment

### 6.1 Theorem 3'''

Theorem 3''' (budgeted cap, true channel, full adaptive degree-$\le 5$
class). [ASSEMBLY; certificate terms and the certificate-free leaf cap
PROVED; multi-evidence composition modulo the same two JDP
negative-association flags inherited from deg2/deg3/deg4] Every adaptive
tree of budget $e$ using degree-$\le 5$ monomial queries and linear forms
satisfies
  $\mathrm{success}(T) \le \min(1,\; q_5^* + P_{\mathrm{adj}}(e) +
   P_K(e) + P_{\mathrm{cert5}}(e) + P_{\mathrm{blk5}}(e) + o(1))$,
  $q_5^* = \max(q,\; q_{\mathrm{and\_exact}},\; \mathrm{post}_3,\;
   \mathrm{post}_4,\; \mathrm{post}_5)$,
  $P_{\mathrm{adj}} \le \min(1, e h_1)\min(1, e q(2d-1)/(2(n-1)))$,
  $P_K \le 2(1 - \exp(-e d/(4n)))$,
  $P_{\mathrm{cert5}} \le e \cdot P_5(n,d)$  (Proposition M5; the whole
   degree-$\ge 2$ certificate family is $o(P_K)$),
  $P_{\mathrm{blk5}} \le e/(n - 2d - 4)$ + spread bound (REL-5).
Measured cap terms ($e = d \log_2 k$):

  point      e    q5*         P_adj   P_K     P_cert5   P_blk5   cap     verdict
  (1023,5)   80   0.0574(5)   0.0015  0.1863  9.05e-14  0.0793   0.3245  stressed
  (4095,5)   80   0.0137(5)   0.0000  0.0482  7.4e-17   0.0196   0.0816  ALIVE
  (4095,5)   320  0.0137(5)   0.0004  0.1861  2.9e-16   0.0784   0.2786  stressed

(the achieving member of the max is post5; at $(63,5)$ and $(127,5)$ it
is post3/post4).
Nothing breaks at degree 5: the exact change list over degree 4 is one
more star class (cost $n-4$), four more alias patterns (six at degree 5
against four at degree 4; $p(k)-1$ in general), one more posterior entry
(same leading form), and one more mass term (strictly dominated).

Corollary 3.4 (chi-hypothesis at degree $\le 5$). [PROVED modulo the two
inherited JDP steps] For every $(n, d, k)$ with $d \ge 5$ and budget
$e = d \log k$:
  $\mathrm{success}(T) \le 1/2 + o(1) + 2(1 - \exp(-d^2 \log k/(4n)))$,
so the error is $\ge 1/2 - o(1) - \Theta(d^2 \log k/n) \ge k^{-O(1)}$
whenever $d^2 \log k = o(n)$.
The boundary is DEGREE-INDEPENDENT through degree 5.
The completion-sum arithmetic behind it:
$\sum_{j \le d} e/(n-j) = \Theta(ed/n) = \Theta(d^2 \log k/n)$ (measured
1.256 against 1.564 at $(1023,5)$, $e = 320$), so the star classes cannot
bite at the program budget.

### 6.2 The general-d induction step, stated precisely

The per-degree template that degrees 2 through 5 instantiate is the
following.
To pass from a degree-$k$ cap to a degree-$(k+1)$ cap ($k + 1 \le d$) one
needs:

  (1) Classification: every degree-$(k+1)$ column is fixed-0 / alias /
      matching-$(k+1)$-varying.
      Available at every degree: the fixed-0 half is literal generator
      monomials; the alias half is the Boolean telescoping chains (the
      reduction system at degree $k+1$ is the $p(k+1)-1$ multiplicity
      patterns, each reducing to degree $\le k$); matching-$(k+1)$
      variation is Theorem A's step (star row $Q_p \cdot g_k$, degree
      $k+1 \le d$), which needs only matching-$k$ variation (induction
      hypothesis) and the base (singles vary, cor:coin).
      CLOSED at every degree by Theorem A + witnesses, modulo the base gap
      (deg4_theory.md Section 7 item 1, inherited).
  (2) One new star class: $Q_p \cdot g_k$ rows.
      The star lock L2 is PROVED at general $d$ (channel_spec.md L2, the
      generator argument), so no new mathematics; each degree needs only
      its status-decomposition check. CLOSED.
  (3) One new posterior entry: the status Bayes assembly is
      degree-independent; the per-$\rho$ law $\{0, 1/2, 1\}$ comes from
      (1) + balance. CLOSED as a template (each degree needs its
      digit-exact check, done through $k = 5$).
  (4) Mass monotonicity: $P_{k+1} < P_k$.
      PROVED at general $k$ this run (Proposition M5, event inclusion).
  (5) Certificate inventory: wedge/Z/$K_j$/counting are degree-generic;
      any new degree-$(k+1)$-dependent certificate is rate-dominated by
      $P_{k+1} < P_k \le P_2$, hence $o(P_K)$ inductively. CLOSED.
  (6) Completion inventory: the new degree-$(k+1)$ star class costs
      $n - k$ queries and the alias family is info-free; the cap needs
      that NO OTHER determined-relation family exists with a completion
      window that is small or identifiable from the transcript.
      OPEN at general $k$: this is the one step Theorem A and
      monotonicity do NOT deliver.

### 6.3 The exact missing lemma

Why (6) is not covered: a determined relation among low-degree coordinates
is an arbitrary $\mathbb{F}_2$-combination of generator rows whose
high-degree parts cancel; such a "short" combination need not decompose
into inventoried low-degree rows (the deg4 instrument note: Boolean rows
have single coordinates, so Boolean and $Q_i \cdot x$ rows can cancel
their degree-2 parts and leave single residues; no graded argument
controls this).
Theorem A rules out short relations only for MATCHING columns (its
induction is matching-to-matching); it says nothing about relations
living on the fixed-0, alias, or mixed windows.

Lemma SPARSE-d (the missing induction lemma). [GAP, open; verified only
at the swept points] For every restricted $(2d,d)$ and every
$0 \le j \le d$: every $\mathbb{F}_2$-combination $R$ of generator rows
(shifts of hole-collisions, two-holes, $Q_p$, Boolean rows, of total
degree $\le d$) whose support lies inside the degree-$\le j$ columns is,
on that support, an $\mathbb{F}_2$-combination of the inventoried
families restricted to the same coordinates: row-parity relations (the
$Q_i$ projections, $2d$ coordinates per row), star rows of degree
$\le j$ restricted to their fresh windows, same-line pins, Boolean alias
pairs, and $e_0$.

Role in the cap: SPARSE-d is exactly what makes every relation family's
completion window $\rho$-hidden and of size $\ge 2d - j + 2 \ge d + 2$
(stars) or $2d$ (free rows), which is what turns REL into the adversarial
bound $P_{\mathrm{blk}} \le \sum_{j \le d} e/(n-j) = \Theta(ed/n) =
\Theta(d^2 \log k/n) \to 0$ at $e = d \log k$.
If SPARSE-d fails at some $(d, j)$, there is a relation family with a
short or transcript-identifiable window, i.e. a sub-$\Theta(n)$
completion mechanism, and the $P_{\mathrm{blk}}$ term of every cap from
Theorem 3 onward breaks there; this is the corpus's named failure mode
for O2 (deg4_theory.md Section 6 forward note; current_results.md
Section 5).

Evidence status: SPARSE-d holds exactly at the swept points, which are the
full sweeps at $(4,2)$ and $(6,3)$ (deg3), the $(8,4)$ and $(10,5)$
degree-$\le 2$ slices, and now the $(10,5)$ degree-$\le 3$ sparse sweep
(100,156 determined columns, all inventoried, 0 unexplained; this run).
It is open at every point of degree $\ge 4$, and no sweep beyond degree 3
at $d = 5$ (or beyond degree 2 at $d \ge 6$) is machine-reachable by the
current instruments (Section 1 wall).

### 6.4 Verdict on the induction

Theorem A + mass monotonicity + the alias/generator/star templates close
induction steps (1)-(5) at every degree.
Step (6) is equivalent to SPARSE-d (plus its $\rho$-hidden-window
corollary), which is open in general.
So an all-degrees induction exists, but it is an induction over
(degree, SPARSE-d-instance) pairs: it closes O2's degree $\ge 5$
quantifier if and only if SPARSE-d is proved (or swept) at each degree,
together with the standing cor:coin base gap and the two inherited JDP
composition steps.
Degree 5 is now the last degree where the cap can be assembled from
per-degree machine evidence without a new instrument: at $d \ge 6$ the
degree-$\le 2$ slice and the degree-3 sweep stay feasible ($(12,6)$: 156
variables, degree-$\le 3$ slice about 657K columns and 470K sparse rows),
and the first true wall is the degree-4 slice, per Section 1.

## 7. What remains open

1. SPARSE-d (Section 6.3): the relation-inventory completeness at general
   $(d, j)$; the single lemma separating the degree-by-degree cap
   assembly from an all-degrees O2 induction. [GAP, the named target]
2. The base of Theorem A at general $d$ (singles vary, cor:coin):
   inherited unchanged from deg4. [GAP, small]
3. Conjecture NAL at $k \ge 6$: the closed-form template predicts no
   lift; only $k \le 5$ is proved from the forms. [CONJECTURED]
4. The two multi-evidence composition (JDP) steps inside Theorem 3''';
   inherited from deg2/deg3/deg4, unchanged. [GAP, flagged]
5. Completeness of the certain inventory on the TRUE channel at general
   scale: exact at $(7,3)$; class-level at $(9,4)$; mixed
   exhaustive/sampled at $(11,5)$. [CONJECTURED complete]
6. The sparse-sweep instrument itself: degree-$\le 4$ at $(10,5)$
   (about 6.0M columns) and degree-$\le 3$ at $(12,6)$ (about 657K
   columns) are the next reachable rungs for SPARSE-d evidence; the
   degree-4 rung needs a leaner pivot store (bitset rows) to fit the
   shared machine. [instrument note]

## 8. Registered run

  cd /home/tomzx/pnp/experiments && python3 chi_deg5_check.py      (21 s,
  ALL PASS)
  python3 chi_deg5_check.py --smoke                                (15 s,
  reduced search samples)

Output (abridged; full text in the run log):
  [V0] (4,2) anchor rank 165 / dim 231 / Des 65 PASS; (10,5) deg<=2 slice
       2376 rows, 6216 columns, 2212 pivots; singles 0/110 determined;
       Q_i-projection rank 11; e_0 determined; squares alias 110/110;
       same-line 1045/1045; diagonals 4950/4950 vary; Q_i in V; K_j 0/10
       determined PASS
  [V1] 14 alias witnesses (x^2+x through x^2yzw+xyzw) all == target, all
       rows legal generator shifts PASS; star rows Q_0.g2/g3/g4, Q_5.g4
       structural + legal PASS; two line-pair generator monomials PASS;
       degree-5 class arithmetic: partition 125,446,882 + 21,356,390 =
       146,803,272 = C(114,5) PASS; 5x5-subgrid rule check (118,755
       monomials) PASS
  [V2] (11,5) degree-5 star status decomposition, 132 restrictions, two
       (p, g4): 0 errors in all four categories PASS
  [V7] sparse degree-<=3 sweep at (10,5): 196,581 rows, 234,136 columns,
       151,097 pivots, max row 38; determined exactly 100,156 = 1 + 1,045
       + 2,090 + 97,020; all other classes vary PASS
  [V3] post5 digit-exact at (11,5) [46/47, both quints], (12,5) [703/733],
       (13,5) [18362/19517, 624,624 restrictions] PASS; grid, leading
       form, finite-n structure as in Section 4
  [V4] P1 = h1 exact and P5 < P4 < P3 < P2 < P1 at all 10 grid points
       (d = 5, 6, 7) PASS; P5/K_j dominance 6.1e-05 to 2.3e-13
  [V5] 25 single + 27,000 exhaustive pair + 13,200 sampled pair/triple/
       quad classes at (11,5): every F1-certain pattern tagged wedge/Z or
       shadow(c=1), UNEXPLAINED 0 PASS; wedge-5 and Z-5 soundness 0
       violations over 132 restrictions PASS
  [V6] cap terms and aliveness verdicts as in Section 6.1; completion-sum
       1.256 vs d^2 log k / n = 1.564 at (1023,5), e = 320
  [V8] channel_spec conformance checklist: D1-D12 (as consumed), I7, L1,
       L2, 5.6 guards -> PASS (notes on the non-exercised rows in the log)
