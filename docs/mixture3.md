# MIXTURE-3: the per-hit cap over the FULL printed degree-<=3 class
# (arbitrary F_2 mixtures) on the true pipeline

Result of the theory+experiments agent (2026-10-04). Status: analysis with a
registered machine run, not peer-reviewed. Resolves the MIXTURE-3 scope gap
(all_degrees.md section 5.2 item 2): O2's literal quantifier allows arbitrary
degree-$\le d$ polynomials as queries, and the mixture class was covered only
at $d = 2$ (mixture_cap.md, Theorems M-A/M-B/M-E/M-D).

Task interpretation note: a degree-3 query needs $d \ge 3$ ($\mathrm{ans}(g)
= L(g^\rho)$ is defined only for $\deg g \le d$), so the $d = 2$ slice points
$(7,2)$, $(15,2)$ have no degree-3 reading and the slice points here are
$(7,3)$, $(8,3)$, $(9,3)$, $(15,3)$, with $(31,3)$, $(63,3)$ as the
$(32,2)$-style regime points and $d = 4$ rows probing the $d$-dependence.
This matches deg3_theory.md, where $(7,3)$ is the smallest exact point
(all 56 restrictions enumerable).

Script: `experiments/chi_mixture3.py` (registered output reproduced in
section 9). No existing corpus file was edited.

## 0. Executive verdict

1. The exact per-hit posterior maximum over the FULL printed degree-$\le 3$
   class EXCEEDS the covered constant
   $q_3^* = \max(q, q_{\mathrm{and\_exact}}, \mathrm{post}_3)$ at every
   measured $(n,d)$, by a finite-$n$ amount that peaks near $n \sim 16$ at
   $d = 3$ and decays to a relative $o(1)$:
   $+0.0169$ absolute at $(15,3)$, $+0.0048$ at $(31,3)$, $+5.2 \times
   10^{-5}$ at $(63,3)$, and $\mathrm{max}/\mathrm{post}_3 = 1.000000$
   by $(1023,3)$.
2. The maximizers are again monomial-star mixtures through the output pair.
   Through degree 3 the class gains two new winning forms: the degree-3
   triple-star mixtures (two or three matching triples through the output
   pair) and the mixed monomial/triple stars. The measured winner is
   the degree-2 champion family itself (three diagonals through the output
   pair) at $8 \le n \le 31$, the single-plus-triple form
   $x_{ab} + x_{ab}x_{cd}x_{ef}$ ties it at the degenerate point $(7,3)$,
   and the disjoint triple-star wins at $n \ge 63$ where the excess is
   already $\le 10^{-4}$.
3. The mechanism question has a clean answer: the killed-branch
   self-exclusion of Theorem M-A extends VERBATIM (Theorem M3-1 below).
   Every term through the output pair contains it as a factor, a killed
   factor zeroes the restricted product regardless of the design, and no
   degree-$\le 3$ term through the output pair has an undetermined answer
   on the killed branch. The machine check finds killed-branch answer-1
   mass EXACTLY $0$ for every through-output configuration.
4. No new single-query certificates: $0$ among the $1474$ enumerated
   configurations (Theorem M3-B), and the degree-3 mixture Z form is the
   covered Z certificate folded into one query at equal budget
   (Proposition M3-E, measured sound).
5. Repaired cap (Theorem M3-D): over the FULL printed degree-$\le 3$
   class, $\mathrm{success}(T) \le q_3^{\mathrm{mix}}(n,d) +
   P_{\mathrm{adj,mix3}}(e) + P_K(e) + P_{\mathrm{wedge}}(e) + P_Z(e) +
   P_{\mathrm{blk3}}(e) + O(e/n) + o(1)$, with
   $q_3^{\mathrm{mix}}/\mathrm{post}_3 \to 1$ and therefore the SAME
   aliveness condition $d^2 \log k = o(n)$. The MIXTURE-d scope gap closes
   at $d = 3$ with a constant repair, not a structural one.
6. Budgeted toy-scale verdict: at $(15,3)$ no mixture strategy beats the
   covered champions at any tested budget. At the degenerate point $(7,3)$
   ($c = 1$) a mixture scan beats the covered champions at budget $10$ only,
   an artifact of $f \gg m$ there; it loses from budget $30$ on.

## 1. Setup and the normal form (Lemma M3-1)

Pipeline $\Omega(n,d)$ at $p = 2$, $d \ge 3$, as in channel_spec.md
section 1: $\rho$ uniform with $n_\rho = 2d$ free holes, $L$ a uniform
design of the restricted canonical system, $\mathrm{ans}(g) = L(g^\rho)$,
$c = n - 2d$, $f = (2d{+}1)2d/((n{+}1)n)$, $m = c/((n{+}1)n)$.

The printed degree-$\le 3$ class in normal form (Lemma M3-1; PROVED, same
proof as mixture_cap.md Lemma N1 plus the degree-3 alias classes of
deg3_theory.md Lemma D3): every $g \in \mathbb{F}_2^{\le 3}[x]$ is
answer-equivalent to a constant, a set of singles, a set of non-degenerate
degree-2 diagonals, and a set of matching triples (degree-3 monomials with
three distinct pigeons and three distinct holes). Proof: squares alias to
variables ($x^3 \mapsto x$), $x^2 y$ aliases to $xy$ or dies on a line,
same-line degree-2 products and collision-containing triples are generator
monomials and answer $0$ determinedly; all fold into the constant or drop.
"Support" = the number of generators; the scan covers support $\le 3$
(same truncation as mixture_cap.md, for the same reason, see section 2.2).

## 2. The per-restriction answer law (Lemmas M3-2 and M3-3)

### 2.1 The alive/dead law at degree 3

Lemma M3-2 (alive/dead; PROVED). Fix $\rho$ and a normal-form query of
support $\le 3$. Per term: a variable on a free pair contributes the live
single column, on a matched pair the determined $1$; a diagonal
contributes the fresh diagonal column (both free), the free component's
single column (one free), the determined $1$ (both matched), nothing (any
killed); a matching triple contributes the triple column (all free), the
diagonal column of its two free pairs (two free), the single column of its
free pair (one free), the determined $1$ (all matched), nothing (any
killed). Live coordinates XOR-cancel pairwise (same column = same
coordinate; the shared output column of a star's matched partners is the
corpus's partner-parity cancellation). If the cancelled live set is
nonempty, $\mathrm{ans}$ is a fair coin; otherwise
$\mathrm{ans} = c_0 \oplus$ (matched parity) determinedly.

Proof: the per-term columns are exactly the restricted coordinates
(restriction is a ring homomorphism; each restricted term is one raw
column, the constant, or $0$); distinct live columns of one query carry
independent fair coins whenever no determined relation lives on their set,
and at $d \ge 3$ the smallest determined relation on all-distinct free
coordinates is a degree-3 star ($2d - 2 \ge 4$ fresh triple columns), a
free row needs $2d \ge 6$, a degree-2 star $2d - 1 \ge 5$, so no relation
lives on $\le 3$ live coordinates. The degenerate (non-all-distinct)
columns are generator monomials, excluded by the normal form. QED.

This is Lemma N2 of mixture_cap.md with the degree-3 term law; the
relation-size input changes from "$2d-1 \ge 5$" to "$2d-2 \ge 4$", which
is why the truncation stays at support $\le 3$.

### 2.2 Why support 4 is different at degree 3 (instrument note)

At support $4$ the per-$\rho$ law $\{0, 1/2\}$ FAILS for the first time:
four triples through a free pigeon $p$ over the two holes of a
both-matched diagonal $g_2$ complete the degree-3 star sum rule
$\bigoplus \mathrm{ans}(x_{pj} g_2) = \mathrm{ans}(g_2) = 1$ determinedly,
so the query answers a determined $1$ while carrying four live columns.
The same failure exists at degree 2 (its star completes at support 4
through the alias), which is why mixture_cap.md truncated at support
$\le 3$ as well. Dominance of the maximum beyond support 3 remains
CONJECTURED (section 10), with the same dilution argument as
mixture_cap.md residual 1.

### 2.3 Pattern weights (Lemma M3-3)

The weight of an exact status pattern is Lemma N3 of mixture_cap.md
verbatim (`weight_pattern`, degree-agnostic hypergeometric
inclusion-exclusion over the $K_p/K_h$ split). Machine-validated here by
partition of the restriction space at $(7,3)$ (section 9, V0) and by the
digit-exact Engine A agreement (V1).

## 3. The two engines and their validation

Engine A (design-exact). Restricted coordinate sets are computed per
restriction (each restricted term is one raw monomial column, the
constant, or empty), and $P[\mathrm{ans}=1 \mid \rho]$ is the exact
fraction of the design coset $L^\star + \ker$ with $L(v) = 1$, computed
through the projected kernel on the support (dimension $\le 3$ for
support $\le 3$).

Engine B (status-exact). Lemma M3-2's law on the query's status patterns
with Lemma M3-3's exact weights, exact rational arithmetic throughout.
Roles scanned: every support pair, the generic external role, and
same-line virtual partners for $\le 3$-slot configurations.

Validation (registered output, section 9):

  V0  pattern weights partition the 56 restrictions at (7,3); Engine B
      pure single / diagonal / triple reproduce q, q_and_exact, and
      post3 (Theorem P3) DIGIT-EXACTLY at (7,3), (8,3), (15,3), (31,3),
      (15,4). The degree-3 status calculus is pinned to the corpus's
      proved closed form before any scan.
  V1  (7,3): Engine B == Engine A DIGIT-EXACT on all 4648 enumerated
      queries x both answers x support roles over ALL 56 restrictions
      (0 mismatches). The enumeration covers all concrete instantiations
      of the winning abstract configurations.
  V3  (15,3): 12 panel queries on 20000 sampled restrictions: every
      comparison inside its own 5-sigma sampling tolerance (worst
      difference 0.0573) (PASS).

## 4. The finding: the degree-3 mixture lift (Theorem M3-A)

Theorem M3-A (per-hit maximum over the FULL printed degree-$\le 3$
class; PROVED for the enumerated configuration space by exact
computation, MEASURED on the grid). Over all support-$\le 3$ queries,
all answers, and all roles, the maximum per-hit posterior is

  $q_3^{\mathrm{mix}}(n,d) = q_3^*(n,d) + \epsilon_3(n,d)$,
  $\epsilon_3 > 0$ at every measured point, attained inside the
  through-output star families.

Grid (Engine B, exact rationals; the full point set is in section 9):

  | (n,d)    |      q | q_and_ex |   post3 |   q3_cov |  max mix |   excess |  max/post3 | argmax      |
  |----------|--------|----------|---------|----------|----------|----------|------------|-------------|
  | (7,3)    | 0.9545 |   0.9688 |  0.9565 |   0.9688 |   0.9767 | +0.00799 |   1.021142 | VT/ MMM tie |
  | (8,3)    | 0.9130 |   0.9385 |  0.9186 |   0.9385 |   0.9522 | +0.01367 |   1.036626 | MMM-star3   |
  | (9,3)    | 0.8750 |   0.9094 |  0.8849 |   0.9094 |   0.9262 | +0.01672 |   1.046690 | MMM-star3   |
  | (15,3)   | 0.7000 |   0.7583 |  0.7345 |   0.7583 |   0.7752 | +0.01691 |   1.055401 | MMM-star3   |
  | (31,3)   | 0.4565 |   0.5066 |  0.5087 |   0.5087 |   0.5135 | +0.00479 |   1.009413 | MMM-star3   |
  | (63,3)   | 0.2692 |   0.2939 |  0.3047 |   0.3047 |   0.3048 | +0.000052 |   1.000171 | TTT-star6   |
  | (127,3)  | 0.1479 |   0.1567 |  0.1630 |   0.1630 |   0.1630 | +0.000005 |   1.000028 | TTT-star6   |
  | (255,3)  | 0.0778 |   0.0804 |  0.0827 |   0.0827 |   0.0827 | +0.000000 |   1.000004 | TTT-star6   |
  | (1023,3) | 0.0202 |   0.0204 |  0.0206 |   0.0206 |   0.0206 | +0.000000 |   1.000000 | TTT-star6   |
  | (15,4)   | 0.8372 |   0.8852 |  0.8683 |   0.8852 |   0.8965 | +0.01123 |   1.032389 | MMM-star3   |
  | (31,4)   | 0.6102 |   0.6807 |  0.6768 |   0.6807 |   0.6885 | +0.00780 |   1.017324 | MMM-star3   |
  | (63,4)   | 0.3956 |   0.4467 |  0.4616 |   0.4616 |   0.4617 | +8.9e-05 |   1.000193 | TTT-star6   |

Here MMM-star3 = $x_{ab}x_{cd} + x_{ab}x_{ef} + x_{ab}x_{gh}$ (the
degree-2 champion family, read inside the degree-$\le 3$ class),
TTT-star6 = three matching triples through $ab$ with pairwise disjoint
all-distinct partners, and VT-star2 = $x_{ab} + x_{ab}x_{cd}x_{ef}$.
Exact fractions: at $(15,3)$,
$q_3^{\mathrm{mix}} - q_3^* = 20059/1186440 = 1.691 \times 10^{-2}$ with
$q_3^{\mathrm{mix}} = 38324/49435$; at $(31,3)$,
$26368230/5506445071 = 4.789 \times 10^{-3}$ with
$q_3^{\mathrm{mix}} = 3805872/7411097$.

Reading:

- The excess is finite-$n$ only. Along the $d = 3$ row it rises from
  $+0.008$ at the degenerate $c = 1$ point to a peak $+0.0169$ near
  $c \approx 9$, falls to $+5 \times 10^{-5}$ by $n = 63$, and
  $\mathrm{max}/\mathrm{post}_3 \to 1.000000$. There is NO asymptotic
  lift over the covered constants (MEASURED; leading order PROVED, see
  section 5.2).
- The winning family is the degree-2 star-3M family for all moderate
  $n$: degree-3 monomials do not improve on it inside the finite-$n$
  window; the triple-stars take over only where the excess has already
  collapsed.
- $d = 4$ behaves identically (peak $+0.0112$ at $(15,4)$, decay by
  $(63,4)$): the lift is governed by the same finite-$n$ branch
  asymmetry at every $d \ge 3$.

## 5. The mechanism (Theorem M3-1 and the branch tables)

### 5.1 Self-exclusion extends verbatim

Theorem M3-1 (killed-branch self-exclusion at degree $\le 3$; PROVED).
Let $c$ be the output pair. Every normal-form term containing $c$ (the
single $x_c$, a diagonal $x_c x_p$, a triple $x_c x_p x_q$) answers $0$
DETERMINEDLY on the event $c$ killed: $x_c^\rho = 0$ and the restricted
term is the zero polynomial regardless of the design. Hence any mixture
all of whose terms pass through $c$ answers $0$ determinedly on the
killed branch, and the hit event self-excludes that branch
(probability $\approx 1$) instead of only its unmatched part. Moreover
no degree-$\le 3$ term through $c$ has an undetermined answer on the
killed branch: the degree-3 structure does NOT break the argument.
A mixture with any term NOT through $c$ loses the exclusion (that term
can answer $1$ on the killed branch) and is dominated in the scan.

Machine check (section 9, V6): killed-branch answer-1 mass is exactly $0$
for every through-output configuration in the mechanism table.

### 5.2 Branch table and the leading form

Mechanism table at $(15,3)$ (V6; $s_0$ = the output pair's status; mass
= $P(\mathrm{ans}=1 \wedge s_0)$):

  | query            | P(s0=F) | mass F   | P(s0=M) | mass M   | P(s0=K) | mass K | post     |
  |------------------|---------|----------|---------|----------|---------|--------|----------|
  | triple (post3)   | 0.175   | 0.002775 | 0.0375  | 0.001003 | 0.7875  | 0      | 0.734545 |
  | shared-2M        | 0.175   | 0.029560 | 0.0375  | 0.008970 | 0.7875  | 0      | 0.767201 |
  | MMM-star3        | 0.175   | 0.040495 | 0.0375  | 0.011740 | 0.7875  | 0      | 0.775240 |
  | TTT-disjoint     | 0.175   | 0.008116 | 0.0375  | 0.002882 | 0.7875  | 0      | 0.737971 |

(post = mass F / (mass F + mass M); the K branch contributes exactly
nothing, by Theorem M3-1.)

Reading: the star lifts the posterior by inflating the free-branch
answer-1 mass faster than the matched-branch mass (triple: factor
$14.6$ on F versus $11.7$ on M going to MMM-star3), i.e. by
partner-parity dilution of the matched pollution, exactly the Theorem
M-A mechanism. The triple-stars dilute the matched branch hardest (their
determined-$1$ event needs BOTH partners matched) but also carry the
least free-branch mass, which is why they win only where all posteriors
have converged.

Leading form (PROVED per family, from the exact pattern tables; sketch).
For every fixed squarefree support-$\le 3$ query through the output pair
without the bare output variable, the dominant answer-1 event class on
the two branches is the same minimal matched-partner configuration
(live on F through the shared output column, visible only at odd
partner count; determined-parity on M), giving
$P(\mathrm{ans}=1 \mid c{=}M) / P(\mathrm{ans}=1 \mid c{=}F) \to 2$ and
$\mathrm{post} \to f/(f + 2m) = (2d^2/n)(1 + o(1))$, the same leading
form as $q$, $q_{\mathrm{and\_exact}}$, and $\mathrm{post}_3$. A bare
$x_c$ term breaks the balance (it answers $1$ on the whole matched
branch) and is dominated from $(8,3)$ on [MEASURED]. Hence
$q_3^{\mathrm{mix}} = (2d^2/n)(1 + o(1))$ at fixed $d$ [PROVED leading
order, MEASURED ratio $\to 1.000000$ on the grid].

## 6. Certificates (Theorem M3-B and Proposition M3-E)

Theorem M3-B (no single-query certificates; PROVED, machine-checked).
No single query of the FULL printed degree-$\le 3$ class attains
posterior $1$ at any answer event with positive numerator. Proof sketch
(the Theorem M-B argument, degree-3 form): posterior $1$ requires the
answer determined and equal to $a$ on every restriction where $c$ is not
free; on every $c$-killed restriction any term not through $c$ is alive
with positive probability (its pairs can all be free), so all terms pass
through $c$ and $a = 0$; on $c$-matched restrictions the answer is the
XOR of the terms' matched values, and over the $c$-matchings the number
of fully-matched terms varies between $0$ and $1$ (at most one partner
can sit on $c$'s hole, and the variation cannot cancel in a squarefree
support), so the answer is not constant. Machine check: $0$ certificates
among all $1474$ configurations at $(7,3)$ (section 9, V2).

Proposition M3-E (mixture certificates fold; PROVED, measured). The
degree-3 Z certificate of deg3_theory.md (Lemma Z with a triple $m$)
folds into the mixture pair $g_1 = x_p + x_p x_q x_r$,
$g_2 = x_p x_q x_r$: $\mathrm{ans}(g_1) = 1 \wedge \mathrm{ans}(g_2) = 1$
forces $x_p = 0$ with $p$ non-killed, hence $p$ free. Two queries either
way, the same budget the covered class pays; no new budget scaling.
Measured sound: the mixz3 strategy's certified outputs were free with
$0$ violations in $11000$ simulations (section 9, V5).

## 7. The repaired budgeted cap (Theorem M3-D)

Theorem M3-D (repaired Theorem 3' over the FULL printed degree-$\le 3$
class; assembly). Every adaptive tree of budget $e$ using arbitrary
$\mathbb{F}_2^{\le 3}$ queries satisfies

  $\mathrm{success}(T) \le \min\big(1,\ q_3^{\mathrm{mix}}(n,d)
  + P_{\mathrm{adj,mix3}}(e) + P_K(e) + P_{\mathrm{wedge}}(e) + P_Z(e)
  + P_{\mathrm{blk3}}(e) + O(e/n) + o(1)\big)$

with $q_3^{\mathrm{mix}}$ of Theorem M3-A,
$P_K(e) \le 2(1 - \exp(-ed/(4n)))$ and
$P_{\mathrm{wedge}}, P_Z = o(P_K)$ as in Theorem 3',
$P_{\mathrm{blk3}} \le e/(n - 2d - 2)$ plus the spread bound (the
degree-$\le 3$ completion inventory of Lemma REL-3 is unchanged by
mixtures: rows, degree-2 and degree-3 stars, alias pairs, plus the
$\Delta$ terms of the enlarged inventory), and
$P_{\mathrm{adj,mix3}}$ the rate-weighted two-query certificate bound
in the form of Theorem M-D:
$\binom{e}{2}\,\sup_g\big(P[\mathrm{hit}(g)]\cdot
\mathrm{elev}(g)\big)\cdot\frac{2d-1}{2(n-1)} + \binom{e}{2}\frac{f^2}{4}$.

Status: PROVED as an assembly with exactly the modulo set of Theorem 3'
(the two JDP composition steps) plus two marked pieces inherited from
the degree-2 repair: the rate-weighted elevation sup is measured at
degree 2 (Theorem M-D) and NOT separately re-measured at degree 3
[marked], and the completeness of the two-query mixture certificate
classification beyond the folded families is CONJECTURED (the $(7,3)$
enumeration found no posterior-1 pair; same partial check as
mixture_cap.md section 6). The cap constant is
$q_3^{\mathrm{mix}}(n,d)$, replacing
$\max(q, q_{\mathrm{and\_exact}}, \mathrm{post}_3)$.

Corollary M3-D1 (aliveness over the FULL printed quantifier at degree
3). At budget $e = d\log k$ with $d^2 \log k = o(n)$:
$q_3^{\mathrm{mix}} = (2d^2/n)(1+o(1)) = o(1)$ (section 5.2),
$P_{\mathrm{adj,mix3}}$ and the covered adjacency term have the same
order (the higher hit rates of live mixtures are offset by
proportionally lower elevation, as at degree 2), $P_K$ is unchanged, and
$P_{\mathrm{blk3}} = o(1)$; hence

  $\mathrm{error}(T) \ge 1/2 - o(1) - 2(1 - e^{-d^2 \log k/(4n)})
  \ge k^{-O(1)}$,

exactly the covered aliveness condition. Status: PROVED modulo the same
JDP steps inherited from Theorem 3'.

## 8. Budgeted toy-scale test (MEASURED)

Exact-channel simulations (uniform $\rho$; $L$ sampled uniformly from the
$(6,3)$ design coset; budget counts query evaluations; scan orders
shuffled per configuration so the first-hit baseline is the corpus's
exchangeable scan; $4000$ simulations at $(7,3)$ and $1500$ at $(15,3)$;
certified outputs asserted free, $0$ violations):

  | (n,d)  | budget | single_scan | kj_budget | kj_direct | triple_scan | mix3_mmm | mix3_ttt | mixz3 | wedge3 | hybrid3 |
  |--------|--------|-------------|-----------|-----------|-------------|----------|----------|-------|--------|---------|
  | (7,3)  | 10     | 0.9585      | 0.7688    | 0.9457    | 0.9390      | 0.9755   | 0.9762   | 0.8742| 0.7755 | 0.9557  |
  | (7,3)  | 30     | 0.9580      | 0.9397    | 0.9990    | 0.9507      | 0.9780   | 0.9775   | 0.9657| 0.8223 | 0.9585  |
  | (7,3)  | 100    | 0.9493      | 0.9992    | 0.9992    | 0.9595      | 0.9748   | 0.9742   | 0.9990| 0.9447 | 0.9547  |
  | (15,3) | 10     | 0.5580      | 0.1667    | 0.1667    | 0.1867      | 0.3427   | 0.2107   | 0.1747| 0.1667 | 0.4120  |
  | (15,3) | 30     | 0.6800      | 0.2947    | 0.9860    | 0.2407      | 0.4753   | 0.2433   | 0.1973| 0.1660 | 0.6207  |
  | (15,3) | 100    | 0.6953      | 0.5847    | 0.9987    | 0.3767      | 0.5427   | 0.2860   | 0.2947| 0.1953 | 0.6993  |

Reading:

- At $(15,3)$ no mixture strategy beats the covered champions at any
  tested budget. The dominant covered champion is kj_direct (the $K_j$
  column channel queried as ONE linear-form query per column,
  certification rate $d/n$-type), which reaches $0.986$ at budget $30$;
  the best mixture (MMM-star scan) reaches $0.54$ at budget $100$.
  Instrument note for the corpus: the previously simulated covered
  champion kj_budget computes each column parity through $n+1$ single
  queries and understates the covered class; linear forms are in the
  covered class, so kj_direct is the correct champion to compare
  against.
- At the degenerate point $(7,3)$ ($c = 1$, $f = 0.75 \gg m$) the
  mixture scan beats everything at budget $10$ ($0.976$ versus
  $0.946$ for kj_direct): there the partners are almost never killed,
  so the star mixtures are simultaneously high-rate and
  high-posterior. This is the same $c = 1$ degeneracy that
  deg3_theory.md section 5 flags as making certainty cheap at the
  smallest exact point, it disappears by budget $30$, and it does not
  occur at any $c > 1$ point tested.
- Consistent with Theorem M3-D: the finite-$n$ per-hit lift does NOT
  convert into budgeted success in regime, because the mixture hit
  rates ($\Theta(m^2)$ to $\Theta(fm)$ per query) are far below the
  $K_j$ certification rate ($\Theta(d/n)$ per query).

## 9. Registered run

Command: `python3 experiments/chi_mixture3.py` (2026-10-04; about five to
twelve minutes depending on machine load, deterministic seeds, reruns
byte-identical on every `[V*]` line; `--smoke` for a fast pass).

```
[setup] restricted system (6,3): 14190 columns, kernel dim 2079 (dim Des = 2079 expected), Lstar(1) = 1 (must be 1)
[V0] (7,3) 3-slot shared-pigeon weights sum: 56 vs restriction count 56 -> PASS
[V0] (7,3) pure single/diag/triple = 0.954545 / 0.968750 / 0.956522 vs q / q_and_ex / post3 = 0.954545 / 0.968750 / 0.956522 -> PASS (digit-exact)
[V0] (8,3) pure single/diag/triple = 0.913043 / 0.938547 / 0.918575 vs q / q_and_ex / post3 = 0.913043 / 0.938547 / 0.918575 -> PASS (digit-exact)
[V0] (15,3) pure single/diag/triple = 0.700000 / 0.758333 / 0.734545 vs q / q_and_ex / post3 = 0.700000 / 0.758333 / 0.734545 -> PASS (digit-exact)
[V0] (31,3) pure single/diag/triple = 0.456522 / 0.506579 / 0.508748 vs q / q_and_ex / post3 = 0.456522 / 0.506579 / 0.508748 -> PASS (digit-exact)
[V0] (15,4) pure single/diag/triple = 0.837209 / 0.885246 / 0.868346 vs q / q_and_ex / post3 = 0.837209 / 0.885246 / 0.868346 -> PASS (digit-exact)
[cfg] star configs 896, general-2 178, general-3 sampled 400, total 1474 (4.6 s)
[V2] full abstract scan at (7,3) over 1474 configs
[V2] (7,3) MAX posterior = 42/43 = 0.976744 vs q3_cov = max(q, q_and_ex, post3) = 31/32 = 0.968750 -> EXCEEDED
[V2] argmax: VT-star2 role ('pair', 0) terms (('V', 0), ('T', 0, 1, 2)) geo ((0, 0), (1, 1), (2, 2))
[V2] single-query certificates (posterior = 1) among all 1474 configs: 0 (Theorem M3-B analogue: 0 expected)
[V1] (7,3): 56 pairs, 12992 generators, 4648 queries x all 56 restrictions
[V1] Engine A pass done in 36.3 s
[V1] Engine B vs Engine A: 4648 queries x 2 answers x support roles: 0 mismatches -> PASS (digit-exact)
[V3] (15,3): 12 panel queries x 20000 sampled restrictions (exact per-rho law)
[V3] worst |Engine B - Engine A| over the panel: 0.05729 (0 comparisons over tolerance, per-comparison 5-sigma tolerance) -> PASS
[V4] (15,3) MAX posterior = 0.775240 vs q3_cov = 0.758333 -> EXCEEDED; argmax MMM-star3
[V4] grid: 77 configs on the grid; 12 points        (see section 4 table)
[V4] worst excess over the grid: +0.016907 at (15, 3): MMM-star3 role pair -> EXCEEDED (repaired constant q3*_mix needed)
[V4] exact (15,3): max - q3_cov = 20059/1186440 = 1.691e-02; max = 38324/49435 = 0.775240 [MMM-star3]; q3_cov = 91/120 = 0.758333
[V4] exact (31,3): max - q3_cov = 26368230/5506445071 = 4.789e-03; max = 3805872/7411097 = 0.513537 [MMM-star3]; q3_cov = 378/743 = 0.508748
[V6] MMM-star3: F: P=0.175000 P(ans=1&s0)=0.040495 | M: P=0.037500 P(ans=1&s0)=0.011740 | K: P=0.787500 P(ans=1&s0)=0.000000  killed-branch ans-1 mass = 0 (SELF-EXCLUDED)
[V6] shared-2M: F: P=0.175000 P(ans=1&s0)=0.029560 | M: P=0.037500 P(ans=1&s0)=0.008970 | K: mass 0 (SELF-EXCLUDED)
[V6] star-3T-disjoint: F: P=0.175000 P(ans=1&s0)=0.008116 | M: P=0.037500 P(ans=1&s0)=0.002882 | K: mass 0 (SELF-EXCLUDED)
[V6] triple: F: P=0.175000 P(ans=1&s0)=0.002775 | M: P=0.037500 P(ans=1&s0)=0.001003 | K: mass 0 (SELF-EXCLUDED)
[V5] (7,3) budget 10: single_scan=0.9585 kj_budget=0.7688 kj_direct=0.9457 triple_scan=0.9390 mix3_mmm=0.9755 mix3_ttt=0.9762 mixz3=0.8742 wedge3=0.7755 hybrid3=0.9557
[V5] (7,3) budget 30: kj_direct=0.9990 ... ; budget 100: kj_budget=0.9992 kj_direct=0.9992 ...
[V5] (15,3) budget 10: single_scan=0.5580 kj_direct=0.1667 mix3_mmm=0.3427 ... ; budget 30: kj_direct=0.9860 ...
[V5] (15,3) budget 100: single_scan=0.6953 kj_direct=0.9987 mix3_mmm=0.5427 hybrid3=0.6993 ...
[V5] soundness: every certified output was free (0 violations), both points
```

(The full V2 top-12 list, the complete V4 grid, the complete V5 tables,
and the V6 branch tables are in sections 4, 8, and 5.2; the console
output is copied verbatim from the registered run
`/tmp/opencode/mixture3_run.txt`.)

## 10. Verdict and open residuals

1. VERDICT (MIXTURE-3). Theorem 3'-type cap structure extends to the
   FULL printed degree-$\le 3$ class with the constant repaired to
   $q_3^{\mathrm{mix}}(n,d) > q_3^*$, attained by star mixtures through
   the output pair, with the excess finite-$n$ only (peak $+0.0169$ at
   $(15,3)$, relative excess $1.7 \times 10^{-4}$ at $(63,3)$,
   $1.000000$ ratio by $(1023,3)$), the same aliveness condition
   $d^2 \log k = o(n)$, and the same modulo set as Theorem 3'. No
   genuine degree-3 mixture gap opens: the self-exclusion mechanism
   extends verbatim (Theorem M3-1), no new certificates exist
   (Theorem M3-B), mixture certificates fold at equal budget
   (Proposition M3-E), and no budgeted mixture gain appears in regime
   (section 8).
2. Residual (support $\ge 4$): the scan is exhaustive for through-output
   configurations with $\le 4$ partner slots over all geometries, covers
   the all-distinct geometry of the $5$- and $6$-partner stars, and
   samples shared-class $5$/$6$-partner stars ($60$/$20$ geometries per
   hypergraph) and general non-through configurations ($178$ exhaustive
   $\le 4$-slot hypergraphs, $400$ sampled $3$-term hypergraphs).
   Dominance of the maximum by the enumerated families beyond support 3
   is CONJECTURED with the same dilution argument as mixture_cap.md
   residual 1.
3. Residual (the support-4 wrinkle): at support 4 the per-$\rho$ answer
   law leaves $\{0, 1/2\}$ for the first time at degree 3 (completed
   degree-3 star with a determined right-hand side, section 2.2). Any
   future support-$\ge 4$ extension needs the pinned-coset law, not the
   w2 logic.
4. Residual (constants): the excess
   $\epsilon_3(n,d) = q_3^{\mathrm{mix}} - q_3^*$ decays to a relative
   $o(1)$ along the grid with the ratio
   $\mathrm{max}/\mathrm{post}_3$ decreasing monotonically to
   $1.000000$; the drop between $(31,3)$ and $(63,3)$ coincides with
   the winner switch from MMM-star3 to TTT-star6, so no single decay
   form was extracted (the pattern-table rational is the exact value,
   as at degree 2).
5. Residual (marked pieces in Theorem M3-D): the rate-weighted
   elevation sup at degree 3 is not separately measured (inherited form
   from Theorem M-D), and the two-query mixture certificate
   classification beyond the folded families is open (same status as
   Proposition M-E).
6. Standing caveats inherited: the general-$d$ classification (Lemma
   CLS and the degree-3 classification conjecture) carries all
   statements beyond the machine-verified points, as everywhere in the
   corpus.
7. Implication for O2: the MIXTURE-d scope gap (all_degrees.md section
   5.2 item 2) is now closed at $d \in \{2, 3\}$ with constant-only
   repairs and is OPEN at $d \ge 4$. The degree-3 template (normal
   form, alive/dead law with the relation-size input, star-family scan,
   self-exclusion, folding, repaired cap) is the thing to carry to
   degree 4, where the first new phenomenon will be degree-4 star sum
   rules completing at support $\le 3$ + 1.

## 11. One-paragraph verdict for the orchestrator

MIXTURE-3 is resolved with a repaired statement: over the FULL printed
degree-$\le 3$ class (all $\mathbb{F}_2$ mixtures of singles, diagonals,
and matching triples), the exact per-hit posterior maximum
$q_3^{\mathrm{mix}}$ exceeds the covered constant
$\max(q, q_{\mathrm{and\_exact}}, \mathrm{post}_3)$ at every measured
point, by up to $+0.0169$ at $(15,3)$ and by a relative $o(1)$
asymptotically ($\mathrm{max}/\mathrm{post}_3 = 1.000000$ by
$(1023,3)$); the maximizers are monomial-star mixtures through the
output pair (the degree-2 star-3M family wins through $n \sim 31$,
triple-stars beyond); the mechanism is the verbatim extension of
killed-branch self-exclusion plus partner-parity dilution (Theorem
M3-1, machine-checked: killed-branch answer-1 mass exactly $0$); there
are no new single-query certificates (Theorem M3-B, $0$ of $1474$),
mixture certificates fold covered ones at equal budget (M3-E), and no
budgeted mixture strategy beats the covered $K_j$-direct champion at
$(15,3)$ at any tested budget. Theorem 3'-type budgeted caps extend to
the full printed quantifier at degree 3 with the constant
$q \to q_3^{\mathrm{mix}}$ and the SAME aliveness condition
$d^2 \log k = o(n)$ (Theorem M3-D, Corollary M3-D1), so the MIXTURE-d
scope gap is closed at $d \le 3$ and remains open only at $d \ge 4$.
