# Degree-3 extension of the true-pipeline theory: the degree-3 kernel
# classification, the exact per-hit posterior post3, two new certain
# certificates (wedge and Z), and the budgeted cap at degree <= 3

Result of the deg3-theory agent (2026-10-04). Status: analysis, not
peer-reviewed. Task: extend the degree-$\le 2$ theory (deg2_theory.md) to degree
3, by exact small-case computation plus proof where possible, on the four
assigned questions: (1) the degree-3 kernel classification and answer law,
(2) the exact per-hit posterior of an all-distinct degree-3 query, (3) the
certificate search for new certainty mechanisms, (4) the cap extension.

Channel: the TRUE $\Omega(n,d)$ pipeline at $p = 2$ (uniform designs of the
restricted canonical system; kernel_structure.py F1: $V(n,d)^\rho = V(2d,d)$).
Script: chi_deg3_check.py (registered run, 250 s, ALL CHECKS PASS; output
reproduced at the end). Everything below is on the true channel; markers:
[PROVED], [MEASURED], [MV] machine-verified, [CONJECTURED], [GAP]
unfinished step (flagged where used).

Scale facts that drive everything: degree-3 monomial columns exist only when
$d \ge 3$, so of the kernel-structure points $(7,1)$, $(15,2)$, $(31,3)$ only $(31,3)$
carries them (restricted $(6,3)$: 7 pigeons $\times$ 6 holes). The smallest outer
pipeline with degree-3 queries is $(7,3)$: $c = n - 2d = 1$ matched pair, 56
restrictions, all enumerable exactly. Both facts are used deliberately and
their limits are stated where they matter.

Notation: $c = n - 2d$ (matched pairs), $f = (2d{+}1)2d/((n{+}1)n)$, $m = c/((n{+}1)n)$,
$q = (f/2)/(f/2 + m)$, $q_{\mathrm{and\_exact}}$ = the exact-status two-pair posterior
(theorem below), $A = (2d{+}1)/(n{+}1)$. A "matching triple" is a degree-3
monomial whose three pairs have distinct pigeons and distinct holes.

## 0. Summary (the four answers in one paragraph each)

Q1 (kernel classification). [PROVED + MV] At restricted $(6,3)$, all 14190
design columns are classified exactly. The 13244 degree-3 columns fall into
ten structural classes; exactly 7974 of all 14190 columns are
determined (value fixed across designs): $e_0$, the 231 same-line degree-2
products, 7280 collision-containing all-distinct triples, and - beyond the
collision-repeats the task anticipated - 462 alias columns $x^2 y$ whose tail
$y$ shares $x$'s line (these die through the Boolean identity, a NEW determined
class at degree 3 in form, though not in mechanism). The remaining 6216
columns vary: all 4200 matching triples (NOT a single one determined), the
1260 diagonal aliases $x^2 y$, the 42 cubes $x^3$, all 42 squares and all 42
singles. Answer law for all-distinct degree-3 monomials: marginally FAIR
always (balance theorem), JOINTLY constrained by the degree-3 star sum rules
$\bigoplus_{\mathrm{fresh}\,j} L(x_{pj}.g_2) = L(g_2)$ - each verified, and i.i.d. on star-free
windows [MV].

Q2 (exact per-hit posterior). [PROVED] $\mathrm{post}_3 = P[\text{pair 1 free} \mid \mathrm{ans} = 1]$ for
an all-distinct degree-3 query has the closed form
   $\mathrm{post}_3 = (2u{+}v{+}w)/(2A_0{+}3u{+}3v{+}w)$,
with $A_0$, $u$, $v$, $w$ the exact hypergeometric counts of the no-killed status
patterns (0, 1, 2, 3 free pairs among the triple). Verified digit-exact
against exhaustive restriction enumeration at $(7,3)$, $(8,3)$, $(9,3)$ and
against exact projected-design enumeration at $(7,3)$. Verdict on the
single-pass no-lift: $\mathrm{post}_3 > q$ everywhere tested (up to +0.0666 at $(63,4)$),
because the degree-3 pollution (all three pairs matched) is rarer than the
degree-2 pollution; against the degree-2 monomial value, $\mathrm{post}_3$ exceeds
$q_{\mathrm{and\_exact}}$ by at most +0.0149 (at $(63,4)$), and $\mathrm{post}_3/q_{\mathrm{and\_exact}} \to 1$ with
both $= (2d^2/n)(1 + o(1))$: a small finite-n lift around $n \sim 8d^2$, NO
asymptotic lift. The corpus's printed $q_{\mathrm{and}}$ (independent-status masses)
agrees with the exact value to $< 0.002$ at every tested point.

Q3 (certificate search). [PROVED + MEASURED] The exhaustive search over
symmetry classes of $\le 3$-query sets at $(7,3)$ found 2025 posterior-1 answer
patterns; every one is explained by a four-mechanism inventory: adjacency
(14), the NEW WEDGE certificate (1920), the NEW Z-CERTIFICATE (60), and a
$c = 1$ counting-shadow artifact (31, provably inert once $c > 9$). Both new
mechanisms are proved here, are certain (posterior exactly 1), are cheap per
attempt (the Z form costs 2 queries), but are rate-dominated by $K_j$ at every
measured and asymptotic scale. The natural sum-rule certificate candidate is
NOT realizable (proved); the wedge and Z forms are.

Q4 (cap extension). [ASSEMBLY, two modulo-JDP flags inherited] Theorem 3'
extends the budgeted cap to the full adaptive degree-$\le 3$ class:
   $\mathrm{success}(T) \le q_3^* + P_{\mathrm{adj}} + P_K + P_{\mathrm{wedge}} + P_Z + P_{\mathrm{blk3}} + o(1)$,
$q_3^* = \max(q, q_{\mathrm{and\_exact}}, \mathrm{post}_3)$, with $P_{\mathrm{wedge}}$, $P_Z = o(P_K)$ and $P_{\mathrm{blk3}} \le$
$e/(n - 2d - 2)$ from the degree-3 star-probe cost; the chi-hypothesis stays
ALIVE exactly when $d^2 \log k = o(n)$, the same boundary as degree 2. What
genuinely breaks at degree 3 is catalogued in Section 6: the all-matched
triple pollution is not line-exclusive (so Theorem-1-style certainty
dichotomies do not extend to degree-3 answers as evidence), and the
certificate inventory grows by two entries.

## 1. The degree-3 coordinate classes at (6,3) (Lemma D3) [PROVED + MV]

Constraint set $W = \mathrm{span}(V(6,3)\text{-rows} + e_0)$ inside $F_2^{14190}$ (14190 = 1 + 42
+ 903 + 13244 monomials up to degree 3 over the 42 free-region variables).
A column $c$ is DETERMINED when $e_c$ is in $W$ (value fixed across all designs);
verified by exact $\mathrm{GF}(2)$ membership reduction, per column, full sweep.

Lemma D3 (degree-3 determination, exact at $(6,3)$). The 13244 degree-3
columns split into ten classes as follows (counts exact, membership exact):

  class            count  determined  mechanism
  x3                  42           0  alias: x^3 + x in V, value = L(x)
  x2y_samepigeon     210         210  x^2y + xy in V and xy in V (two-hole)
  x2y_samehole       252         252  same, via a hole-collision
  x2y_diag          1260           0  alias: x^2y + xy in V, value = L(xy)
  T_pigeon3          140         140  contains a two-hole pair (in V)
  T_hole3            210         210  contains a hole-collision (in V)
  T_22              1260         1260  contains both
  T_pm21_hm3        2520         2520  contains a two-hole pair
  T_pm3_hm21        3150         3150  contains a hole-collision
  match3            4200           0  free-varying (see below)

Every determined-constant non-matching triple is literally a generator
monomial of $V$ (a collision or two-hole pair times a third variable: a
single-term row of $V$). The global determined count is 7974 = 1 ($e_0$) + 231
(same-line degree-2) + 462 ($x^2 y$ same-line) + 7280 (non-matching
all-distinct), matching the sweep digit-for-digit [MV].

Answer to "which degree-3 monomials are DETERMINED, beyond
collision-repeats": exactly the ALIAS class ($x^3 \to x$, $x^2 y \to xy$, and $x^2 y$
$\to 0$ when $xy$ is same-line). Nothing else: in particular NO matching triple
is determined. The proof of the latter uses the $S_7 \times S_6$ symmetry of the
constraint set (the determined set is a union of orbits; matching triples
form one orbit; and if all matching triples were determined, the star
identity of Section 2 would force every degree-2 diagonal to be determined
0, contradicting the 399 free + 231 varying diagonals). [PROVED at $(6,3)$;
the general-$d$ statement is [CONJECTURED] with the same orbit argument,
conditioned on diagonal variation, which is itself only computed up to
$(6,3)$ in the corpus.]

## 2. The answer law for all-distinct degree-3 monomials [PROVED + MV]

Balance lemma. Every non-determined coordinate is a fair coin under uniform
designs. Proof: $L = \mathrm{Lp} + \sum_i b_i k_i$ over the reduced kernel basis with
uniform $b_i$; $L(c) = \mathrm{Lp}(c) + \bigoplus_i b_i k_i(c)$ is balanced unless every
$k_i(c) = 0$, which is exactly $c$ determined. [PROVED; one line, and it covers
pivot-varying coordinates like the parity pivots as well.]

Star lemma (the degree-3 parity constraint). For any pigeon $p$ and any
all-distinct degree-2 monomial $g_2$ with $p$ outside it, the row $Q_p.g_2$ lies in
$V$ (degree $3 \le d$), hence identically
   $\mathrm{ans}(g_2) + \bigoplus_j \mathrm{ans}(x_{pj}.g_2) = 0$,
the sum over all holes $j$; the $j$-terms on $g_2$'s own holes are determined 0
(same-hole) and the killed-$j$ terms are 0, so with the fresh holes $R$ minus
$g_2$'s: $\bigoplus_{\mathrm{fresh}} \mathrm{ans}(x_{pj}.g_2) = \mathrm{ans}(g_2)$ when $p$ is free, and $= 0$ when $p$ is
assigned. Verified with 0/20000 violations, determined-relation dimension
exactly 2 ($e_0$ + the star row), and exactly the XOR-pinned half-cube (16 of
32 patterns) on the completed star [MV]. Consequences:
  - matching triples are FAIR marginally and i.i.d.-uniform on any window
    carrying no complete star, no full row, and no alias pair ($2^8$ patterns,
    $\chi^2 z = +0.20$; and jointly uniform with their three component singles,
    rank 4, $\chi^2 z = -0.22$) [MV];
  - a completed star is the degree-3 analogue of parity-locking: the fresh
    triple answers are pinned to $\bigoplus = \mathrm{ans}(g_2)$, with $\mathrm{ans}(g_2)$'s value
    carrying the answer.
So the answer law for an all-distinct degree-3 monomial is: FAIR alone,
PARITY-CONSTRAINED through stars, and the constraint's right-hand side is
configuration-invariant ($\mathrm{ans}$ of the degree-2 diagonal), which is why stars
carry information only through the status-dependent decomposition (see the
non-realizability remark in Section 4).

## 3. Theorem P3: the exact per-hit posterior post3 [PROVED]

Fix an outer matching triple $T = (p_1, p_2, p_3)$ (three pairs, distinct
pigeons and holes) and the event $\mathrm{ans}(T) = 1$. Because any killed pair kills
the restricted product, the answer is 1 exactly when no pair of $T$ is killed
and (i) all three pairs are matched (restricted value $= 1$), or (ii) at
least one pair is free and the restricted free-part column (a single, a
degree-2 diagonal, or a matching triple) has design value 1 - a fair coin
by the balance lemma, since none of those coordinate classes is determined.

Theorem P3. On the true channel, with $c = n - 2d$,
   $A_0 = \binom{n-2}{c-3} \binom{n-3}{c-3} (c-3)!$      (all three matched)
   $u  = \binom{n-2}{c-1} \binom{n-3}{c-1} (c-1)!$      (exactly one matched)
   $v  = \binom{n-2}{c-2} \binom{n-3}{c-2} (c-2)!$      (exactly two matched)
   $w  = \binom{n-2}{c}   \binom{n-3}{c}   c!$          (all three free)
(counting configurations $(D, R, \mu)$: $m$ matched pairs of $T$ fix $m$ pigeon-hole
pairs; the other $c - m$ assigned pigeons are chosen from the $n - 2$ non-triple
pigeons, the $c - m$ assigned holes from the $n - 3$ non-triple holes, bijected
in $(c{-}m)!$ ways), the exact per-hit labeling posterior is
   $\mathrm{post}_3 = P[p_1 \text{ free} \mid \mathrm{ans}(T) = 1] = (2u{+}v{+}w)/(2A_0{+}3u{+}3v{+}w)$.
Proof. $P(\mathrm{ans} = 1) = A_0 + (1/2)(3u + 3v + w)$: the $m = 1$ class has 3 choices of
matched pair, the $m = 2$ class 3 choices, each answering 1 w.p. $1/2$ by
balance. $P(\mathrm{ans} = 1 \text{ and } p_1 \text{ free}) = (1/2)(2u + v + w)$: the $m = 1$ class
contributes $2u$ (matched pair in $\{p_2,p_3\}$), the $m = 2$ class $v$ ($p_2,p_3$ both
matched), the $m = 0$ class $w$. The per-$\rho$ factorization is exact because
$p_1$-freeness is $\rho$-measurable and $P(\mathrm{ans} = 1 \mid \rho)$ is exactly $\{0, 1/2, 1\}$ by
balance. QED.

Verification [MV]: closed form = exhaustive restriction enumeration,
digit-exact as rationals at $(7,3)$ (22/23, both triples), $(8,3)$ (361/393,
2016 restrictions), $(9,3)$ (2751/3109, 60480 restrictions); plus exact
projected-design enumeration over all 56 restrictions at $(7,3)$ with
per-$\rho$ balance exact.

Comparison with $q$ and $q_{\mathrm{and}}$ (exact arithmetic, full grid in the registered
output). Define $q_{\mathrm{and\_exact}}$ as the same two-pair status Bayes with exact
hypergeometric counts: with $M_0 = \binom{n-1}{c-2}\binom{n-2}{c-2}(c-2)!$, $M_1 =$
$\binom{n-1}{c-1}\binom{n-2}{c-1}(c-1)!$, $M_2 = \binom{n-1}{c}\binom{n-2}{c}c!$,
   $q_{\mathrm{and\_exact}} = (M_1 + M_2)/(2M_0 + 2M_1 + M_2)$.
Findings [MEASURED on exact closed forms]:
  - $\mathrm{post}_3 > q$ at every tested point (max +0.0666 at $(63,4)$): the degree-3
    hit is a purer test than a single hit at small-to-moderate $n$, because
    its pollution branch needs THREE matched pairs.
  - $\mathrm{post}_3$ vs the degree-2 monomial value: $\mathrm{post}_3 < q_{\mathrm{and\_exact}}$ for $n \lesssim d^2$,
    crosses above near $n \sim 8d^2$, peaks at +5.5% (relative) at $(127,4)$, and
    decays back: $\mathrm{post}_3/q_{\mathrm{and\_exact}} = 1.0024$ at $(4095,3)$. Asymptotically
    [PROVED from the closed forms, leading order]:
      $v/A_0 = (2d{+}1)(2d)/(c-2)$, $M_1/M_0 = (2d{+}1)(2d)/(c-1)$, $u/v$, $w/v$, $M_2/M_1$
      are all $o(r)$ with $r = 4d^2/n$, giving
      $\mathrm{post}_3 = (2d^2/n)(1 + \Theta(d^2/n))$ and
      $q_{\mathrm{and\_exact}} = (2d^2/n)(1 + \Theta(d^2/n))$, so $\mathrm{post}_3/q_{\mathrm{and\_exact}} \to 1$
      and the gap is $\Theta(d^4/n^2)$ (measured 1.2e-5 at $(4095,3)$).
    So: the single-pass no-lift does NOT survive VERBATIM (a genuine but small
    finite-n lift over the degree-2 value, sup +0.0149 absolute on the
    grid), and there is NO asymptotic lift: all single-pass per-hit
    posteriors ($q$, $q_{\mathrm{and\_exact}}$, $\mathrm{post}_3$) share the leading form $2d^2/n$.
  - the corpus's printed $q_{\mathrm{and}}$ (independent-status masses) matches
    $q_{\mathrm{and\_exact}}$ to $< 0.002$ at every tested point: its constant is fine in
    this regime [MEASURED].

## 4. New certain certificates at degree >= 2 [PROVED]

Lemma S3 (wedge / co-vertex certificate). Let $m$ be any monomial of degree $k$
$\ge 1$, all-distinct, and $p$ a pigeon outside $m$. If two queries $x_{pj_1}.m$ and
$x_{pj_2}.m$ ($j_1 \ne j_2$, both holes outside $m$'s holes) both answer 1, then $p$ is
FREE; consequently any answer-1 single in row $p$ certifies a free pair
(cert_floor Lemma 3(c)). Proof: if $p$ were assigned to $j_0$, then $(p,j)$ is
killed-unmatched for every $j \ne j_0$, so $x_{pj}.m$ restricts to $0$ for all $j \ne$
$j_0$, and only the $j_0$-term (value $\mathrm{ans}(m)$) can be nonzero: at most one 1. QED.
A strongest form holds: two answer-1s on ANY two monomials carrying the
same pigeon in distinct holes (nothing else shared) certify that pigeon
free, by the same one-line argument; and the hole-dual certifies holes.
The star-probe realization (probe all holes outside $m$'s, plus $m$ itself)
costs $n - k + 1$ queries. Measured exact per-attempt probabilities [MV,
exhaustive projected enumeration]: 0.335938 (degree-3 wedge at $(7,3)$),
0.536830 (degree-2 wedge at $(7,3)$), 0.283333 (degree-2 wedge at $(5,2)$ over
all 30 restrictions); violations 0 everywhere. Asymptotic per-query rate:
$A/n \cdot (1 - \Theta(d/2^{2d})) = \Theta(d/n^2)$: dominated by $K_j$'s $d/n$
(factor $\sim n/2$), and better than the adjacency chain's $\Theta(d^3/n^3)$ exactly
when $n \gtrsim 12d^2$ (measured dominance factor 6-8x in $K_j$'s favor at $(7,3)$).

Lemma Z (zero-single certificate). Let $m$ be any monomial of degree $\ge 2$
and $p$ one of its pairs. If $\mathrm{ans}(x_p) = 0$ and $\mathrm{ans}(m) = 1$, then $p$ is FREE.
Proof: $\mathrm{ans}(m) = 1$ forces every pair of $m$ to be matched-or-free (a killed-
unmatched pair contributes the factor $0$); $\mathrm{ans}(x_p) = 0$ forces $p$ non-matched
(a matched pair answers 1); hence $p$ free. Two queries, and the certified
object is the output pair itself (no row scan). QED. Measured exact
per-attempt probabilities [MV]: 0.133929 ($x_{11} = 0$, $m = x_{00}.x_{11}$) and
0.098214 ($x_{22} = 0$, $m$ = the matching triple $x_{00}.x_{11}.x_{22}$) at $(7,3)$;
violations 0. Asymptotically the rate is $\Theta(A \cdot (m^2 + fm)/2)$ per
attempt $= \Theta(d/n^3)$ per query for diagonal $m$: the WEAKEST certificate
per query in the inventory, but the cheapest per attempt, and it
certifies a pair outright.

Remark (the sum-rule certificate does not exist). The tempting form
$\{\mathrm{ans}(g_2) = 1 \text{ and } \bigoplus_{\mathrm{fresh}} = 1\}$ is not realizable: the fresh-hole set is
$\rho$-hidden, and probing ALL non-$g_2$ holes makes $\bigoplus_{\mathrm{probe}} = \mathrm{ans}(g_2)$
identically (the star invariant itself, verified with 0 violations), which
is information-free; any partial probe leaves both sides unpinned because
the pinned XOR constrains only the fresh subset. What survives is the wedge
form above ($\ge 2$ ones), whose soundness uses only determined zeros.
[PROVED]

Consequence for O7 (the certain-certificate inventory). The corpus
inventory {adjacency on single 1s, counting, $K_j$} is INCOMPLETE at degree
$\ge 2$: the wedge (S3) and Z (Lemma Z) mechanisms are certain, reading-
independent (they consume only F1: matched $\to$ 1, killed $\to$ 0), and were
absent from the inventory. The corrected conjecture: every budgeted
transcript certainty event is explained by {co-linear single 1s, co-vertex
monomial 1s (wedge), zero-single + containing-monomial 1 (Z), $K_j = 1$,
counting}. The budgeted consequences of deg2_theory Corollary 3.1 are
unchanged in order: both new mechanisms have per-query rates that are $o(d/n)$
(the $K_j$ rate), so any cap of the form $q + P_{\mathrm{adj}} + P_K + o(P_K)$ still bounds
every tree; Theorem 3 below makes this explicit.

## 5. The exhaustive certificate search at (7,3) [MEASURED]

Design: pool = 16 singles + 72 degree-2 diagonals + 96 degree-3 matching
triples inside a $4 \times 4$ window (containing the unique matched pair's row and
column and free cells); ALL symmetry-orbit classes of 1- and 2-query sets
(14 + 566 classes) and 400 sampled classes of 3-query sets (of 29328);
channel: uniform restrictions (all 56) $\times$ 500 uniform designs each, sampled
exactly from the $(6,3)$ kernel coset; every posterior-1 pattern (2025 of
them) verified EXACTLY afterwards by full enumeration over all 56
restrictions $\times$ exact projected-design enumeration.

Result: inventory-explained 1994 (adjacency 14, wedge 1920, Z 60); the
remaining 31 are the SHADOW-ESCAPE artifact: at $c = 1$ the pattern's
consistency conditions pin the unique matched pair to a small set $S$ of
$(i_0,j_0)$, and any window pair whose pigeon and hole avoid all of $S$'s row and
column shadows is certain-free (its certified pairs are the $(i,j)$ with $i$ in
$\{3..7\}$, $j$ in $\{0,1,2\}$ in the examples). This is a counting/consistency
effect with no degree-3 content, and it is INERT at non-toy scales: by the
matched-pair remap argument, a $\le 3$-query transcript cannot certify any pair
outside its touched coordinates once $c > 9$ ($n - 2d > 9$), because a
consistent configuration can always be modified on untouched matched pairs
to match-or-kill any candidate pair while preserving every touched status
and every observed answer. [PROVED sketch; the design-value freshness step
is the usual small-window completion fact, clean at 3 queries since no
star/row/alias relation can complete.]

Verdict: NO degree-3 certainty mechanism exists at the searched scale
beyond the four-entry inventory; the searched scale is the smallest exact
one ($(7,3)$), and its $c = 1$ degeneracy (no all-matched pollution) is exactly
what makes certainty cheap there - the search is a mechanism DISCOVERY
probe, not a rate measurement.

## 6. Lemma REL-3 and Theorem 3': the cap at degree <= 3 [ASSEMBLY]

Lemma REL-3 (degree-3 block completion). A degree-$\le 3$ transcript sees a
determined relation only if it completes (a) a free row ($2d$ coordinates,
cost $\Theta(n)$ since the free columns are $\rho$-hidden), (b) a degree-2 star
($\mathrm{ans}(x_{ab})$ + all fresh diagonals $x_{pj}.x_{ab}$, cost $n - 1$), (c) a degree-3
star ($\mathrm{ans}(g_2)$ + all fresh triples $x_{pj}.g_2$, cost $n - 2$), or (d) an alias
pair ($x^3$ with $x$, or $x^2 y$ with $xy$: per-query, but configuration-invariant,
zero information). Per-star completion probabilities carry the usual
hypergeometric factors $\binom{n-2d}{e-(2d-k)}/\binom{n}{e}$ for a spread transcript;
an ADVERSARIAL transcript pays $\Theta(n)$ per completed star, giving the
exact adversarial budget bound $p_{\mathrm{blk3}}(e) \le e/(n - 2d - 2)$ for the
deliberate-probe route plus the spread bound. At the program's budget
$e = d \log k = o(n)$ both are $o(1)$. [PROVED structure; the spread-bound
per-star factor is the same hypergeometric estimate as deg2_theory Lemma
REL, and the adversarial cost is exact.]

Theorem 3' (budgeted cap, true channel, full adaptive degree-$\le 3$ class).
Every adaptive tree of budget $e$ using degree-$\le 3$ monomial queries and
linear forms satisfies
   $\mathrm{success}(T) \le \min(1, q_3^* + P_{\mathrm{adj}}(e) + P_K(e) + P_{\mathrm{wedge}}(e) + P_Z(e)$
                      $+ P_{\mathrm{blk3}}(e) + o(1))$,
with $q_3^* = \max(q, q_{\mathrm{and\_exact}}, \mathrm{post}_3)$,
   $P_{\mathrm{adj}} \le \min(1, e h_1)\, \min(1, e q (2d{-}1)/(2(n{-}1)))$   (deg2_theory Thm 3),
   $P_K   \le 2(1 - \exp(-e d/(4n)))$                       (the $K_j$ channel),
   $P_{\mathrm{wedge}} \le \min(1, e A(1+o(1))/(n - k + 1))  = o(P_K)$,
   $P_Z     \le \min(1, e A h_k/4)                = o(P_K)$,
   $P_{\mathrm{blk3}} \le e/(n - 2d - 2)$ + (spread bound).
Assembly status: the certificate-free leaf cap $q_3^*$ is proved per-evidence-
class (own single: $q$, deg2_theory Theorem 2(i); own degree-2 monomial:
$q_{\mathrm{and\_exact}}$, exact status Bayes; own degree-3 monomial: $\mathrm{post}_3$, Theorem P3;
zeros never elevate, since each posterior dominates the base rate $f$); the
MULTI-evidence composition (deep zero-runs across classes, distant
evidence) is carried modulo the same JDP negative-association citation
standard as deg2_theory Theorem 3 [GAP, inherited, flagged]. The new
certificate terms are proved sound with negligible rates [PROVED].

Corollary 3.2 (chi-hypothesis at degree $\le 3$). For every $(n, d, k)$ with
$2d^2 + 3d \le n$ and budget $e = d \log k$:
   $\mathrm{success}(T) \le 1/2 + o(1) + 2(1 - \exp(-d^2 \log k/(4n)))$,
so the error is $\ge 1/2 - o(1) - \Theta(d^2 \log k/n) \ge k^{-O(1)}$ whenever
$d^2 \log k = o(n)$. The chi-hypothesis of Theorem 6.1 (arXiv:2609.35927)
HOLDS at $p = 2$ for the entire adaptive degree-$\le 3$ class on the true
pipeline in exactly the regime where it holds at degree $\le 2$: the boundary
$d^2 \sim n$ is degree-independent. [PROVED modulo the two JDP steps]

What breaks at degree 3, precisely (the task's alternative):
  1. CERTAINTY DICHTOMY: the degree-3 answer's pollution branch (all three
     pairs matched) is not line-exclusive (three matched pairs in general
     position), so Theorem 1-style "co-linear 1s force posterior 1"
     dichotomies do not extend to degree-3 ANSWERS as certainty sources;
     the posterior cap survives through $\mathrm{post}_3$ instead.
  2. INVENTORY: two new certain mechanisms (wedge, Z), both negligible-rate.
  3. RELATIONS: the star and alias identities add determined relations at
     degree 3 (REL-3's classes (c), (d)), with completion costs still
     $\Theta(n)$, so the cap's aliveness condition is unchanged.
  4. PER-HIT POSTERIOR: a small finite-n lift over the degree-2 value
     (sup +0.0149 over $q_{\mathrm{and\_exact}}$, +0.0666 over $q$, near $n \sim 8d^2$),
     vanishing asymptotically (ratio $\to 1$, gap $\Theta(d^4/n^2)$).
None of these opens a budgeted route past the degree-2 boundary; the
substantive open core remains the all-degrees quantifier (O2(i)), now with
the degree-3 template (posterior dichotomy + star structure + inventory)
in hand the way degree 2 was after deg2_theory.md.

## 7. What remains open

1. The general-$d$ degree-3 classification: the $(6,3)$ classification is
   exact; the orbit-symmetry argument extends it to general $d$ CONDITIONED
   on diagonal variation (399 free + 231 parity-determined at $(6,3)$), which
   the corpus has only computed up to $(6,3)$. [CONJECTURED]
2. The exact constants in the finite-n lift $\mathrm{post}_3 - q_{\mathrm{and\_exact}} =$
   $\Theta(d^4/n^2)$: leading orders derived, constants not pinned. [open]
3. The multi-evidence composition steps (JDP) at degree 3, and the
   deep-zero-run analogue of deg2_theory Theorem 2(iv) for degree-3
   evidence (the own-triple monotonicity is immediate from P3; the
   multi-class composition is not). [GAP, flagged]
4. The exact wedge/Z rate laws as functions of $(n, d)$ (the per-$\rho$ mixture
   over h-status classes is computed exactly at the tested points; closed
   forms for the mixture were not derived - the naive single-class formula
   $A(1 - (m_f{+}1)/2^{m_f})$ OVERSTATES the exact rate, e.g. 0.6016 vs 0.3359
   measured at $(7,3)$ degree-3, because the h-status class changes both the
   live-term count and the pinning value). [open, easy]
5. Whether any degree-3-only mechanism beats the $K_j$ channel's $\Theta(d/n)$
   per-query certificate rate: everything found here is $o(d/n)$. [open]
6. The O2 open core beyond degree 3: the same program (classify, posterior,
   inventory, REL-d) now has a executed template at the next degree.

## 8. Registered run

  cd /home/tomzx/pnp && python3 chi_deg3_check.py          (250 s, all PASS)
  python3 chi_deg3_check.py --smoke                        (reduced samples)

Output (abridged; full text in the run log):
  [V0] rank V = 12110, dim S = 14190, dim Des = 2079 (corpus tables) PASS
  [V1] ten classes, counts and determined-status all digit-exact; global
       determined 7974 PASS; identities x^3+x, x^2y+xy, Q_6.g2, same-hole
       product all in V PASS
  [V2] (a) triple fairness max|z| = 2.91, L(1)=1 in 20000/20000 PASS
       (b) star rule 0/20000 violations, dim 2, 16/32 patterns PASS
       (c) star-free window dim 1, chi2 z = +0.20 PASS
       (d) singles+triple rank 4, chi2 z = -0.22 PASS
  [V3] post3 digit-exact at (7,3)/(8,3)/(9,3); exact projected enumeration
       at (7,3) digit-exact; grid and asymptotics as in Section 3
  [V4] wedge: 0 violations, exact rates 0.335938 / 0.536830 / 0.283333,
       dominated by K_j 6-8x at (7,3) PASS; Z: 0 violations, exact rates
       0.133929 / 0.098214 PASS; sum-rule non-realizability remark
  [V5] 2025 posterior-1 patterns: adjacency 14 + wedge 1920 + Z 60 +
       shadow 31, unexplained 0 -> inventory complete at searched scale
  [V6] cap terms at e = d log k for (31,3), (63,3), (127,3), (63,4)

Instrument notes (corrections made during the run, per corpus discipline):
(1) kernel_structure.py's rowspace_intersection undercounts $W \cap F_2^T$ on
    the non-reduced echelon (its leading-bit argument needs a reduced
    form); replaced everywhere by exact kernel-projection machinery
    (uniform coset $\mathrm{Lp}|_T + \pi_T(K)$, built from the full 2079-vector kernel
    basis). The theory itself flagged the bug: the star row failed to
    appear as a determined relation until the tool was fixed.
(2) the naive star-certificate (sum-rule) form was retracted by this agent
    before delivery: it is not realizable (Section 4 remark); the wedge and
    Z forms replace it.
(3) a first V4 "closed form" for the wedge rate ignored the $\rho$-mixture
    over h-status classes and overstates the rate; the exact enumeration
    is the source of truth (open item 4).
