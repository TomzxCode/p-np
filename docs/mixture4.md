# MIXTURE-4: the per-hit cap over the FULL printed degree-<=4 class
# (arbitrary F_2 mixtures) on the true pipeline

Result of the theory+experiments agent (2026-10-05). Status: analysis with a
registered machine run, not peer-reviewed. Resolves the MIXTURE-d scope gap
at $d = 4$ (all_degrees.md section 5.2 item 2; O2's literal quantifier allows
arbitrary degree-$\le d$ polynomials as queries; the mixture class was
covered at $d = 2$ by mixture_cap.md and at $d = 3$ by mixture3.md).

Task interpretation note: a degree-4 query needs $d \ge 4$
($\mathrm{ans}(g) = L(g^\rho)$ is defined only for $\deg g \le d$), so the
exact slice points are outer $(9,4)$ (90 restrictions), $(10,4)$ (4950) and
$(11,4)$ (217800), all rho-exhaustive, with the deg4_theory.md-style window
enumeration pattern; the aggregated Engine-B grid runs at
$(15,4), (31,4), (63,4), (127,4), (255,4), (1023,4)$ and $(15,5)$; the
$d = 3$ points $(7,3), (8,3), (15,3), (31,3)$ anchor the machinery to the
corpus's registered exact values.

Script: `experiments/chi_mixture4.py` (registered output reproduced in
section 9; all `[V*]` result lines byte-identical across reruns, only the
wall-clock `t=` fields differ; `--smoke` for a fast pass). No existing
corpus file was edited; the script imports `chi_mixture_cap.py`
(`weight_pattern`, `DesignExact`, `rho_data`, closed forms) read-only.

## 0. Executive verdict

1. The exact per-hit posterior maximum over the FULL printed degree-$\le 4$
   class EXCEEDS the covered constant
   $q_4^* = \max(q, q_{\mathrm{and\_exact}}, \mathrm{post}_3,
   \mathrm{post}_4)$ at every measured $(n, d)$, by a finite-$n$ amount that
   decays to a relative $o(1)$: $+0.0153$ at $(15,4)$, $+0.0115$ at
   $(31,4)$, $+1.3 \times 10^{-4}$ at $(63,4)$, $1.8 \times 10^{-7}$ at
   $(127,4)$, $7.7 \times 10^{-9}$ at $(255,4)$, $9.4 \times 10^{-12}$ at
   $(1023,4)$, and $\mathrm{max}/\mathrm{post}_4 = 1.000000$ from
   $(255,4)$ on.
2. The maximizers are again monomial-star mixtures through the output pair.
   The degree-2 champion family gains a FOURTH diagonal inside the
   support-4 class: the new winner is the star-4M
   $x_{ab}(x_{cd} + x_{ef} + x_{gh} + x_{ij})$, which beats both
   $q_4^*$ and the degree-3 class maximum $q_3^{\mathrm{mix}}$
   ($0.9005$ versus $0.8965$ at $(15,4)$) for $n \le 31$; the triple-star
   $(2,2,2,2)$ wins at $(63,4)$ and the quad-star $(3,3,3,3)$ ties
   $\mathrm{post}_4$ from $(127,4)$ on, mirroring deg4_theory.md's
   post3-to-post4 switch.
3. The self-exclusion question has a clean answer: Theorem M3-A's
   killed-branch self-exclusion extends VERBATIM (Theorem M4-1 below,
   PROVED; killed-branch answer mass EXACTLY $0$ on $2.49$M
   (config, rho) pairs at $(10,4)$ alone). The support-4
   $\{0, 1/2\}$ breakdown of mixture3.md section 2.2 CANNOT occur at
   $d \ge 4$: the first per-rho law breakdown at degree $\le 4$ is the
   free-base degree-$(d-1)$ star at support $2d - 2 \ge 6$ coordinates,
   outside the scanned class, and even support 5 is clean at $d \ge 4$
   (the fresh columns alone answer the base coin). The breakdown is
   exhibited where it actually lives: at $d = 3$ support 5 (positive
   control, $(8,3)$, 30/2016 restrictions, fold-law == design-exact
   Engine A) and at $d = 4$ support 6 (positive control, $(11,4)$,
   336/217800). This also CORRECTS mixture3.md section 2.2's support-4
   attribution at $d = 3$ (section 2.2 here); no mixture3 registered
   result changes.
4. No new single-query certificates: $0$ among the $3000$ $(9,4)$ and
   $1503$ $(10,4)$ scanned configurations (Theorem M4-B analogue), and
   the degree-2 Z-certificate folds into a mixture pair at equal budget
   with measured soundness (Proposition M4-E; 0 violations in
   $\sim 7700$ certification attempts).
5. Repaired cap (Theorem M4-D): over the FULL printed degree-$\le 4$
   class, $\mathrm{success}(T) \le q_4^{\mathrm{mix}}(n,d) +
   P_{\mathrm{adj,mix4}}(e) + P_K(e) + P_{\mathrm{wedge}}(e) + P_Z(e) +
   P_{\mathrm{cert4}}(e) + P_{\mathrm{blk4}}(e) + O(e/n) + o(1)$ with
   $q_4^{\mathrm{mix}} = (2d^2 + d)/c \cdot (1 + o(1))$ (PROVED leading
   form) and therefore the SAME aliveness condition
   $d^2 \log k = o(n)$. The MIXTURE-d scope gap closes at $d = 4$ with a
   constant repair, not a structural one; Theorem 3''' as printed
   (deg4_theory.md Theorem 3'') is FALSE as a cap constant at finite $n$
   and is repaired to $q_4^* \to q_4^{\mathrm{mix}}$.
6. Budgeted toy-scale verdict: at $(10,4)$ no mixture strategy beats the
   covered champion kj_direct at any tested budget $\ge 15$
   ($0.994$ at budget 15, $0.996$ at 30, versus $0.945$/$0.954$ for the
   best mixture scan). At budget 7 (the exact-transfer regime
   $e < 2d = 8$) the posterior-output scans sit marginally ahead
   ($0.905$ single, $0.891$ mixture versus $0.853$ kj_direct): the same
   $f \gg m$ degenerate-point artifact mixture3.md section 8 found at
   $(7,3)$; it disappears by budget 15.

## 1. Setup and the normal form (Lemma M4-1)

Pipeline $\Omega(n,d)$ at $p = 2$, $d \ge 4$, as in channel_spec.md
section 1: $\rho$ uniform with $n_\rho = 2d$ free holes,
$L$ a uniform design of the restricted canonical system,
$\mathrm{ans}(g) = L(g^\rho)$, $c = n - 2d$,
$f = (2d{+}1)2d/((n{+}1)n)$, $m = c/((n{+}1)n)$.

Lemma M4-1 (normal form; PROVED). Every $g \in \mathbb{F}_2^{\le 4}[x]$
is answer-equivalent to a constant, a set of singles, a set of
non-degenerate degree-2 diagonals, a set of matching triples, and a set
of matching-4 monomials. Proof: the degree-4 alias classes
$x^4 \to x$, $x^3y \to xy$, $x^2y^2 \to xy$, $x^2yz \to xyz$ are witnessed
generator sums (deg4_theory.md Lemma A4), so every repeated-variable
monomial collapses to its square-free reduction; every all-distinct
monomial containing a same-pigeon or same-hole pair is a generator
monomial, determined $0$ (Lemma W4); same-line reductions fold into the
constant or drop; identical monomials in an $\mathbb{F}_2$ sum cancel
pairwise. QED. "Support" = the number of surviving generators; the scan
covers support $\le 4$ (dominance beyond: CONJECTURED, section 10, with
the same dilution argument as mixture_cap.md residual 1 and the
section 4 probes here).

## 2. The per-restriction answer law (Lemmas M4-2 and M4-3)

### 2.1 The law at degree 4, support <= 4

Lemma M4-2 (alive/dead; PROVED modulo corpus-inherited Theorem A, the
balance lemma, and REL-4 completeness). Fix $\rho$ with $d \ge 4$ and a
normal-form query of support $\le 4$. Per term: a matching-$k$ term
($1 \le k \le 4$) contributes the determined $1$ iff all $k$ cells are
matched, contributes nothing if any cell is killed-unmatched, and
otherwise contributes exactly one live coordinate: the matching-$j$
column of its free cells ($j \ge 1$). Live coordinates XOR-cancel
pairwise (same restricted column = same coordinate). If the cancelled
live set is nonempty, $\mathrm{ans}$ is a fair coin; otherwise
$\mathrm{ans} = (\#\,\text{all-matched terms}) \bmod 2$ determinedly.

Proof: the restriction is a ring homomorphism; a killed factor
substitutes to $0$ (channel_spec.md D12), an all-matched term
substitutes to the constant, and the free part of a matching term is a
matching-$j$ column of the restricted system, which varies by Theorem A
(the matching hierarchy, deg4_theory.md) and is a fair coin by the
balance lemma. The answer is $L(v)$ with
$v = (\text{matched parity})\cdot 1 + \sum \text{live columns}$; the
evaluation of the design coset on $v$ is a fair coin iff
$v \notin V + \mathrm{span}(1)$, and $v \in V + \mathrm{span}(1)$ would
exhibit a determined relation supported on at most $4$ matching columns
(plus the constant). By REL-4 (deg4_theory.md section 3, PROVED
structure) the determined-relation classes at degree $\le 4$ are the
free rows ($2d \ge 8$ live singles), the degree-2 and degree-3 stars
(free base: $2d-2$ fresh columns plus the base column; matched base:
$|R| = 2d$ fresh singletons), the degree-4 stars (free base:
$2d-3 + 1 = 2d-2$; matched base: $2d$), and the alias pairs (absent in
normal form). The smallest of these has $2d - 2 \ge 6$ coordinates at
$d \ge 4$; nothing fits inside $4$. QED.

Corollary (the canary; PROVED arithmetic, machine-checked at every scan
step). At $d \ge 4$ the per-rho law $\{0, 1/2, 1\}$ is EXACT on all
support-$\le 4$ queries, and even on support-5 queries (the $2d-3 = 5$
fresh columns of a degree-4 star alone answer the base's own coin). The
first breakdown of the naive per-rho law at degree $\le 4$ is at
support $2d - 2 \ge 6$.

### 2.2 The support arithmetic across degrees (correction to mixture3.md)

The breakdown coordinate counts, by degree:

| d | first breakdown | shape | live coords |
|---|-----------------|-------|-------------|
| 2 | support 4 | degree-2 star, matched target: fresh set = R, 2d = 4 singletons; or free target: 3 fresh diagonals + the target column | 4 |
| 3 | support 5 | free-base degree-3 star: 4 fresh triples + the g2 column, XOR = 0 determinedly | 5 |
| >= 4 | support 2d-2 >= 6 | free-base degree-(d-1) star: 2d-3 fresh + the base column | 2d-2 |

PROVED (arithmetic on the star rule
$\bigoplus_{j \in R \setminus \mathrm{holes}(g)} \mathrm{ans}(x_{pj} g)
= \mathrm{ans}(g) [p \in D]$, channel_spec.md L2). This CORRECTS
mixture3.md section 2.2, which attributed the first $d = 3$ breakdown to
support 4 via "four triples over the two holes of a both-matched
diagonal": a MATCHED base has fresh set $R \setminus \mathrm{holes}(g) =
R$ (its holes are not free), giving $2d = 6$ fresh singletons at
$d = 3$; the four-fresh completion is the FREE-base star, whose
right-hand side is the base's own live column, so the determined event
needs the base column too (support 5) and the four-triple sub-query
answers the base coin (fair). The correction changes no mixture3
registered result: their own V1 sweep found 0 Engine-B/Engine-A
mismatches on every enumerated $(7,3)$ query, exactly what the corrected
arithmetic predicts. Machine controls (section 9, V1): the 4-triple
query is fair on all 56 $(7,3)$ and all 2016 $(8,3)$ restrictions
(negative); the support-5 star is determined with 5 live columns on 30
of the 2016 $(8,3)$ restrictions and the REL-4 fold law matches
design-exact Engine A there (positive). At $d = 4$ the matching support-6
star fires on 336 of 217800 $(11,4)$ restrictions (V4).

### 2.3 Pattern weights (Lemma M4-3)

The weight of an exact status pattern is Lemma N3 of mixture_cap.md
verbatim (`weight_pattern`, degree-agnostic hypergeometric
inclusion-exclusion over the $K_p/K_h$ split with the U-edge
bad-event corrections). For the wide disjoint quad stars the script
aggregates the same counting over per-cell status counts
(`n3w_disjoint` + `dp_post`): all cells carry pairwise-distinct pigeon
and hole classes, so the weight of a count vector
$(n_F, n_M, n_{K_p}, n_{K_h})$ is
$\sum_u \binom{n_{K_p}}{u} (-1)^u \binom{n+1-p_u-p_m}{c-p_m}
\binom{n-h_u-h_m}{c-h_m} (c - e_{img})!$
with $p_u = n_F + n_{K_h}$, $p_m = n_M + n_{K_p}$,
$h_m = n_M + n_{K_h} + u$, $h_u = n_F$, $e_{img} = n_M + u$. Machine
checks: the aggregated weights match `weight_pattern` per pattern on all
$81$ patterns of a 4-slot geometry and the DP posteriors match both
`weight_pattern` and the rho-exhaustive concrete route digit-exactly on
18 families at both $(9,4)$ and $(10,4)$ (V0/V2).

## 3. The engines and their validation

Engine A (design-exact, $d \le 3$ only). `chi_mixture_cap.DesignExact(3)`;
at $d = 4$ the deg4_theory.md instrument wall applies ($|S(8,4)| =
1{,}282{,}975$ columns, 167-180 GB projected echelon), so no design-exact
engine exists at $d = 4$ and the corpus's own $d = 4$ standard is
rho-exhaustive F1-level enumeration on the PROVED per-rho law.

Engine B (status-exact). Lemma M4-2's law on the query's status patterns
with Lemma M4-3's exact weights, exact rational arithmetic. Two
realizations: per-pattern (`weight_pattern`, slot count $\le 8$) and the
aggregated disjoint-family DP (any width).

Concrete route (rho-exhaustive). Every restriction enumerated
(`rhos_all`/`rho_data`), per-rho exact law, exact rational posteriors.
Primary at $(9,4)$, $(10,4)$, $(11,4)$.

Validation (registered output, section 9):

  V0  pattern weights partition the restriction space at $(7,3)$
      (56) and $(9,4)$ (90); the DP pure single/diagonal/triple/quad
      reproduce $q$, $q_{\mathrm{and\_exact}}$, post3, post4
      DIGIT-EXACTLY at $(15,4)$, $(31,4)$, $(63,4)$, $(127,4)$ against
      `q_closed`, `q_and_exact` and the post_k b-forms of
      deg4_theory.md Theorem C; the degree-3 anchors reproduce
      mixture3.md's registered exact fractions $21/22$, $31/32$,
      $22/23$ at $(7,3)$, $38324/49435$ at $(15,3)$,
      $3805872/7411097$ at $(31,3)$, $42/43$ (VT-star2) at $(7,3)$.
  V1  (7,3) and (8,3): Engine B == design-exact Engine A DIGIT-EXACT
      per rho on a 10-query degree-$\le 3$ panel (all 56 and 2016
      restrictions for the small queries, 1500-rho subsamples for the
      rest; 0 mismatches), plus the section 2.2 controls.
  V2  (9,4) and (10,4): three-way agreement (concrete ==
      weight_pattern == DP) on the pure queries and on 18 families
      (0 mismatches), digit-exact.
  V3  grid DP against the corpus's printed post3/post4/q/q_and values.

Instrument notes (per corpus discipline): (1) the first DP draft
omitted the $K_p$ pigeons from the base forced-covered count and the
$\binom{n_{K_p}}{u}$ subset factor of the bad-event
inclusion-exclusion; the per-pattern comparison against the corpus's
`weight_pattern` caught both before any scan was trusted. (2) The
fresh-bit simulator initially keyed the single-variable coin apart from
the one-cell column coin; the Proposition M4-E soundness assert caught
the non-conformance (they are the same design coordinate,
channel_spec.md section 3.1) and the coin keys were unified.

## 4. The finding: the degree-4 mixture lift (Theorem M4-A)

Theorem M4-A (per-hit maximum over the FULL printed degree-$\le 4$
class; PROVED for the enumerated configuration space by exact
computation, MEASURED on the grid). Over all support-$\le 4$ queries,
all answers, and all output roles, the maximum per-hit posterior is

  $q_4^{\mathrm{mix}}(n,d) = q_4^*(n,d) + \epsilon_4(n,d)$,
  $\epsilon_4 > 0$ at every measured point, attained inside the
  through-output star families.

Concrete scans (rho-exhaustive, exact rationals):

  | point | q        | q_and    | post3    | post4    | q4_cov   | q4^mix   | excess        |
  |-------|----------|----------|----------|----------|----------|----------|---------------|
  | (9,4) | 0.972973 | 0.982759 | 0.977778 | 0.970588 | 0.982759 | 0.986301 | +0.003543     |
  | (10,4)| 0.947368 | 0.965772 | 0.956941 | 0.944030 | 0.965772 | 0.972973 | +0.007201     |

  Exact: at $(9,4)$: $q_4^{\mathrm{mix}} = 72/73$, excess
  $15/4234$; at $(10,4)$: $q_4^{\mathrm{mix}} = 36/37$, excess
  $288/39997$. At both points $q_4^{\mathrm{cov}}$ is attained by
  $q_{\mathrm{and\_exact}}$.

Grid (Engine B aggregated DP, exact rationals; all 59 disjoint star
families with $t \le 4$ terms, partner counts $0..3$):

  | (n,d)    | q       | q_and   | post3   | post4   | q4_cov  | q4^mix  | eps4      | max/post4 | argmax    |
  |----------|---------|---------|---------|---------|---------|---------|-----------|-----------|-----------|
  | (15,4)   | 0.837209| 0.885246| 0.868346| 0.840326| 0.885246| 0.900518| +0.015272 | 1.071629  | (1,1,1,1) |
  | (31,4)   | 0.610169| 0.680708| 0.676783| 0.649987| 0.680708| 0.692236| +0.011527 | 1.065000  | (1,1,1,1) |
  | (63,4)   | 0.395604| 0.446680| 0.461597| 0.456423| 0.461597| 0.461731| +0.000134 | 1.011629  | (2,2,2,2) |
  | (127,4)  | 0.232258| 0.255827| 0.269939| 0.276374| 0.276374| 0.276374| +1.8e-07  | 1.000001  | (3,3,3,3) |
  | (255,4)  | 0.127208| 0.135399| 0.141918| 0.146834| 0.146834| 0.146834| +7.7e-09  | 1.000000  | (3,3,3,3) |
  | (1023,4) | 0.034253| 0.034914| 0.035543| 0.036139| 0.036139| 0.036139| +9.4e-12  | 1.000000  | (3,3,3,3) |
  | (15,5)   | 0.916667| 0.946558| 0.937766| 0.924567| 0.946558| 0.954537| +0.007979 | 1.032415  | (1,1,1,1) |

  Exact: at $(15,4)$: $q_4^{\mathrm{mix}} = 1824572/2026137 = 0.900518$
  [star-4M], $\epsilon_4 = 1887494/123594357 = 1.527 \times 10^{-2}$
  over $q_4^{\mathrm{cov}} = 54/61$; at $(31,4)$:
  $q_4^{\mathrm{mix}} = 3969661068/5734551325 = 0.692236$ [star-4M],
  $\epsilon_4 = 138089986902/11979477717925 = 1.153 \times 10^{-2}$
  over $q_4^{\mathrm{cov}} = 1422/2089$.

Reading:

- The excess is finite-$n$ only. Along $d = 4$ it decays from $+0.0153$
  at $(15,4)$ to $10^{-11}$-scale at $(1023,4)$ with
  $\mathrm{max}/\mathrm{post}_4 \to 1.000000$. There is NO asymptotic
  lift over the covered constants (leading order PROVED, section 5.2).
- The winner is NEW relative to degree 3: the star-4M (four diagonals
  through the output pair, support 4) beats the degree-3 class maximum
  $q_3^{\mathrm{mix}}(15,4) = 0.8965$ (mixture3.md grid, MMM-star3) by
  $+0.0040$ at $(15,4)$: the fourth diagonal is a genuine degree-4-class
  gain, still finite-$n$. The argmax migration
  $(1,1,1,1) \to (2,2,2,2) \to (3,3,3,3)$ along the grid mirrors
  deg4_theory.md's post3-to-post4 crossover: at large $c$ the best
  mixture degenerates to the best pure monomial.
- At the degenerate small-$c$ points the winners reach a ceiling
  EXACTLY: $q_4^{\mathrm{mix}}(9,4) = 72/73 = f/(f+m)$ and
  $q_4^{\mathrm{mix}}(10,4) = 36/37 = f/(f+m)$ with $f/m = 72$ and $36$
  respectively (Proposition M4-C, section 5.2).
- $d = 5$ behaves like $d = 4$ (excess $+0.0080$ at $(15,5)$, same
  winner): the lift is governed by the same finite-$n$ branch asymmetry.

## 5. The mechanism (Theorem M4-1, Proposition M4-C, Proposition M4-L)

### 5.1 Self-exclusion extends verbatim

Theorem M4-1 (killed-branch self-exclusion at degree $\le 4$; PROVED).
Let $c$ be the output pair and let $g$ be a mixture ALL of whose terms
contain $x_c$. On the event $c$ killed ($x_c^\rho = 0$) every term
restricts to the zero polynomial (restriction is a ring homomorphism;
channel_spec.md D12), so $g^\rho = 0$ and
$\mathrm{ans}(g) = 0$ determinedly, regardless of the partners, the
design, or any star completion. The support-$2d-2$ breakdown of
section 2.2 cannot leak onto this branch: a completed star needs its
full live-coordinate set on top of the base, while a through-$c$
mixture on the killed branch has NO live coordinates at all. A mixture
with any term not through $c$ loses the exclusion (that term can answer
$1$ on the killed branch) and is dominated in the scan (MEASURED: the
non-through panel never appears in a top-8 at either concrete point).

Machine check (V2): killed-branch answer mass exactly $0$ on $51{,}000$
(config, rho) pairs at $(9,4)$ and $2{,}434{,}860$ at $(10,4)$, asserted
on every through-output configuration.

### 5.2 Branch structure, the small-c ceiling, and the leading form

Mechanism table at $(10,4)$ (V6; $s_0$ = the output pair's status; mass
$= P(\mathrm{ans}=1 \wedge s_0)$):

  | family   | P(s0=F) | mass F   | P(s0=M) | mass M   | P(s0=K) | mass K | post     |
  |----------|---------|----------|---------|----------|---------|--------|----------|
  | (3,) post4-by-term | 0.654545 | 0.076667 | 0.018182 | 0.004545 | 0.327273 | 0 | 0.944030 |
  | (1,1,1) star-3M    | 0.654545 | 0.318788 | 0.018182 | 0.009091 | 0.327273 | 0 | 0.972274 |
  | (2,2,2) star-3T    | 0.654545 | 0.273939 | 0.018182 | 0.009091 | 0.327273 | 0 | 0.967880 |
  | (3,3,3) star-3Q    | 0.654545 | 0.196364 | 0.018182 | 0.009091 | 0.327273 | 0 | 0.955752 |
  | (0,2) VT           | 0.654545 | 0.327172 | 0.018182 | 0.012323 | 0.327273 | 0 | 0.963701 |
  | (1,3) DQ           | 0.654545 | 0.244545 | 0.018182 | 0.008485 | 0.327273 | 0 | 0.966467 |

Reading: the killed branch contributes exactly nothing for every
through-output family (Theorem M4-1); the lift again comes from
inflating the free-branch mass faster than the matched-branch mass
(star-3M versus post4-by-term: factor $4.2$ on F versus $2.0$ on M).

Proposition M4-C (the small-c ceiling; PROVED at $c = 1$, MEASURED
exact at $c = 2$). At $c = 1$ the matching is exactly
$\{(\alpha, \beta)\}$: on the output-matched branch every other cell is
free, so every through-c term with at least one partner contributes an
independent fair coin on BOTH branches, $R_F = R_M = 1/2$, and
$\mathrm{post} = f/(f+m) = (f/m)/(f/m+1)$ exactly, for every such
mixture — the eight-way tie at $72/73$ in the $(9,4)$ scan
($f/m = 72$). The bare single alone is the exception (its own matched
cell answers $1$ on the matched branch,
$\mathrm{post} = (f/2)/(f/2+m)$). At $(10,4)$ ($c = 2$,
$f/m = 36$) the winning families again measure EXACTLY
$f/(f+m) = 36/37$; the exact-zero matched pollution there is measured,
with the mechanism unpinned.

Proposition M4-L (leading form of the disjoint star families; PROVED at
fixed $d$, from the exact aggregated pattern forms; sketch). For a
through-c disjoint star with $t$ terms and partner counts
$s_i \ge 1$: with $A = \sum_i (f+m)^{s_i}$ and $B = \sum_i m^{s_i}$,
$R_F = A/2 + O((f+m)^{2s})$ and
$R_M = (A + B)/2 + O((f+m)^{2s})$, giving

  $\mathrm{post} = \frac{f}{f + m\left(1 + B/A\right)} \cdot (1 + o(1))
  \to \frac{f}{2m} = \frac{(2d+1)d}{c} (1 + o(1))$,

the same leading form $2d^2/n$ as the whole single-pass family
$\{q, q_{\mathrm{and\_exact}}, \mathrm{post}_3, \mathrm{post}_4\}$
(deg4_theory.md Theorem C): NO asymptotic lift and no demotion; the
$t$-dependence cancels at leading order, and the finite-$n$
discriminator is $B/A = \sum_i m^{s_i}/\sum_i (f+m)^{s_i} < 1$, smaller
for more partners per term — which is why adding the fourth diagonal
helps at moderate $n$ and why every family ties post4 as
$B/A \to 1$. Bare-single terms ($s = 0$) give the single's
$f/(f+2m)$ form and never lead. MEASURED: the grid ratios
$\mathrm{max}/\mathrm{post}_4 \to 1.000000$; MEASURED winner ordering
star-4M $>$ star-3M $>$ star-3Q at $(15,4)$ (V6).

## 6. Certificates (Theorem M4-B and Proposition M4-E)

Theorem M4-B (no single-query certificates; PROVED argument,
machine-checked). No single query of the FULL printed degree-$\le 4$
class attains posterior $1$ at any answer event with positive numerator.
Proof sketch (the Theorem M-B/M3-B argument, degree-4 form): posterior
$1$ requires the answer determined and equal to $a$ on every restriction
where $c$ is not free; on every $c$-killed restriction any term not
through $c$ is alive with positive probability (its cells can all be
non-killed), so all terms pass through $c$ and $a = 0$; on $c$-matched
restrictions some partner cell is free with positive probability, so
some term carries a live coin and the answer is not constant across the
$c$-matchings. Machine check: $0$ certificates among the $3000$ scanned
configurations at $(9,4)$ and the $1503$ at $(10,4)$, both answer
events (V2).

Proposition M4-E (mixture certificates fold; PROVED sound, MEASURED).
The degree-2 Z-fold $g_1 = x_p + x_p x_q$,
$g_2 = x_p x_q$ with answers $(1,1)$ certifies $(p,q)$ free
(mixture_cap.md Proposition M-E) and stays inside the degree-$\le 4$
class at the same two-query budget; the budget accounting is the
covered class's. Measured sound: across the V5 simulations the fold
fired $\approx 2.6 \times 10^3$ times and kj_direct certified
$\approx 8.5 \times 10^3$ times, with $0$ violations; the simulation's
own soundness assert initially FIRED and exposed a non-conforming coin
keying in the simulator (section 3, instrument note 2) before any
number was trusted. Mass dominance (deg4_theory.md Proposition M,
inherited): every certain certificate consumes an answer-1, the
degree-4-dependent answer-1 masses satisfy
$P_4 < P_3 < P_2 < P_1$, and the high-rate/low-elevation live mixtures
are absorbed by the rate-weighted adjacency term exactly as at degrees
2 and 3. The two-query mixture certificate classification beyond the
folded families remains CONJECTURED (same status as Propositions M-E
and M3-E).

## 7. The repaired budgeted cap (Theorem M4-D)

Theorem M4-D (repaired Theorem 3''' over the FULL printed
degree-$\le 4$ class; assembly). Every adaptive tree of budget $e$
using arbitrary $\mathbb{F}_2^{\le 4}$ queries satisfies

  $\mathrm{success}(T) \le \min\big(1,\ q_4^{\mathrm{mix}}(n,d)
  + P_{\mathrm{adj,mix4}}(e) + P_K(e) + P_{\mathrm{wedge}}(e) + P_Z(e)
  + P_{\mathrm{cert4}}(e) + P_{\mathrm{blk4}}(e) + O(e/n) + o(1)\big)$

with $q_4^{\mathrm{mix}}$ of Theorem M4-A,
$P_K(e) \le 2(1 - \exp(-ed/(4n)))$,
$P_{\mathrm{wedge}}, P_Z = o(P_K)$ as in Theorem 3'',
$P_{\mathrm{cert4}} \le e \cdot P_4 = o(P_K)$ (Proposition M), and
$P_{\mathrm{blk4}} \le e/(n - 2d - 3)$ plus the spread bound (the REL-4
completion inventory is unchanged by mixtures: a mixture transcript's
determined relations are still exactly rows, degree-2/3/4 stars, and
alias pairs, since mixtures only XOR columns). The adjacency term keeps
the Theorem M-D/M3-D rate-weighted form
$\binom{e}{2}\,\sup_g(P[\mathrm{hit}(g)]\cdot \mathrm{elev}(g))
\cdot \frac{2d-1}{2(n-1)} + \binom{e}{2}\frac{f^2}{4}$.

Status: PROVED as an assembly with exactly the modulo set of
Theorem 3'' (the two JDP composition steps) plus the marked pieces
inherited from the degree-2/3 repairs: the rate-weighted elevation sup
is measured at degree 2 and NOT separately re-measured at degree 4
[marked]; the support-$\le 4$ truncation dominance is CONJECTURED
(section 10) with the section 4 probes as evidence. The cap constant is
$q_4^{\mathrm{mix}}(n,d)$, replacing $q_4^* = \max(q,
q_{\mathrm{and\_exact}}, \mathrm{post}_3, \mathrm{post}_4)$: Theorem
3''' as printed is FALSE as a cap constant at finite $n$ and is
repaired with no structural change.

Corollary M4-D1 (aliveness over the FULL printed quantifier at degree
4). At budget $e = d \log k$ with $d^2 \log k = o(n)$:
$q_4^{\mathrm{mix}} = (2d^2+d)/c \cdot (1 + o(1)) = o(1)$
(Proposition M4-L), the adjacency terms have the same order (the
higher hit rates of live mixtures are offset by proportionally lower
elevation, as at degrees 2 and 3), $P_K$ is unchanged, and
$P_{\mathrm{blk4}} = o(1)$; hence

  $\mathrm{error}(T) \ge 1/2 - o(1) - 2(1 - e^{-d^2 \log k/(4n)})
  \ge k^{-O(1)}$,

exactly the covered aliveness condition. Status: PROVED modulo the
same JDP steps inherited from Theorem 3''.

## 8. Budgeted toy-scale test (MEASURED)

Fresh-bit-channel simulations (Route B of channel_spec.md; uniform
rho; exact transfer only for $e < 2d = 8$, so budget 7 is exact and
budgets 15/30 are toy-scale instrument readings; certified outputs
(kj_direct, zfold2) asserted free with 0 violations in 3000 worlds per
budget; single/mix scans are posterior-output strategies; 3000
simulations; deterministic seeds):

  | budget | kj_direct | zfold2 | single_scan | mix3M_scan | mixQQQ_scan |
  |--------|-----------|--------|-------------|------------|-------------|
  | 7      | 0.8527    | 0.2220 | 0.9047      | 0.8913     | 0.8100      |
  | 15     | 0.9940    | 0.3100 | 0.9467      | 0.9450     | 0.8560      |
  | 30     | 0.9957    | 0.3320 | 0.9483      | 0.9540     | 0.8610      |

Reading: kj_direct (the covered $K_j$ column channel with single
confirmation) dominates everything from budget 15 on, exactly as at
degrees 2 and 3. At budget 7 the posterior-output scans sit marginally
ahead ($0.905$/$0.891$ versus $0.853$): the same $f \gg m$
degenerate-point artifact mixture3.md section 8 found at $(7,3)$ — at
$(10,4)$, $f/m = 36$ — and it inverts by budget 15. The mixture hit
rates ($\Theta((f+m)^{s})$ to $\Theta(fm)$ per query) remain far below
the $K_j$ certification rate ($\Theta(d/n)$), so the finite-$n$
per-hit lift does not convert into budgeted success in regime,
consistent with Theorem M4-D.

## 9. Registered run

Command: `python3 experiments/chi_mixture4.py` (2026-10-05; about
thirty seconds; deterministic seeds; every `[V*]` result line
byte-identical across reruns, only the `t=` wall-clock fields differ;
`--smoke` for a fast pass). Output tee'd to
`/tmp/opencode/mixture4_run.txt`.

```
[setup] MIXTURE-4 registered run (smoke=False) t=0.0s
[V0] pattern-weight partition + corpus pins
[V0] (n,d)=(7,3) 3-slot weights sum 56 vs restrictions 56 -> PASS
[V0] (n,d)=(9,4) 4-slot weights sum 90 vs restrictions 90 -> PASS
[V0] dp_post(7,3) (0,): post1 = 21/22 vs q (7,3) = 21/22 -> PASS (digit-exact)
[V0] dp_post(7,3) (1,): post1 = 31/32 vs q_and_exact (7,3) = 31/32 -> PASS (digit-exact)
[V0] dp_post(7,3) (2,): post1 = 22/23 vs post3 (7,3) = 22/23 -> PASS (digit-exact)
[V0] dp_post(15,3) (1, 1, 1): post1 = 38324/49435 vs star-3M (15,3) mixture3 = 38324/49435 -> PASS (digit-exact)
[V0] dp_post(31,3) (1, 1, 1): post1 = 3805872/7411097 vs star-3M (31,3) mixture3 = 3805872/7411097 -> PASS (digit-exact)
[V0] dp_post(7,3) (0, 2): post1 = 42/43 vs VT-star2 (7,3) mixture3 = 42/43 -> PASS (digit-exact)
[V0] (15,4) q 0.837209 q_and 0.885246 post3 0.868346 post4 0.840326 vs closed forms -> PASS (digit-exact)
[V0] (31,4) q 0.610169 q_and 0.680708 post3 0.676783 post4 0.649987 vs closed forms -> PASS (digit-exact)
[V0] (63,4) q 0.395604 q_and 0.446680 post3 0.461597 post4 0.456423 vs closed forms -> PASS (digit-exact)
[V0] (127,4) q 0.232258 q_and 0.255827 post3 0.269939 post4 0.276374 vs closed forms -> PASS (digit-exact)
[V1] design-exact law validation at the (6,3) rectangle
[setup] restricted (6,3): 14190 columns, coset kernel dim 2079 (dim Des = 2079 expected 2079)
[V1] (7,3) small panel x 56 rhos: mismatches 0; the 4-triple query carries 4 live
     singletons on 7 rhos and is DETERMINED on 0 (expected 0: at d = 3 the
     matched-base degree-3 star needs |R| = 2d = 6 fresh singletons, so
     support 4 completes NOTHING)
[V1] (7,3) support-5 control (4 fresh triples + the free g2 column): fold fires
     (determined 0 with 5 live columns) on 5 of 56 rhos; fold-law vs Engine A
     mismatches 0 -> PASS
[V1] (7,3) rest panel (support<=3) x subsample: mismatches 0 -> PASS (digit-exact)
[V1] (8,3) small panel x 2016 rhos: mismatches 0; ... DETERMINED on 0 ...
[V1] (8,3) support-5 control ... fold fires ... on 30 of 2016 rhos; fold-law vs
     Engine A mismatches 0 -> PASS
[V1] (8,3) corrected support arithmetic: the first per-rho law breakdown at
     d = 3 is SUPPORT 5 (the free-base degree-3 star, determined 0 with 5 live
     columns); mixture3.md section 2.2's support-4 example understated the
     fresh-set size (a matched base has fresh set = R = 2d = 6, not 4);
     support <= 4 is clean at d = 3, consistent with mixture3's own registered
     V1 0-mismatch sweep
[V1] (8,3) rest panel (support<=3) x subsample: mismatches 0 -> PASS (digit-exact)
[V1] d>=4 support<=4 canary (PROVED arithmetic, REL-4 inherited): the first
     completed relation at degree <= 4 is the free-base degree-(d-1) star with
     2d-3 fresh columns + the base column = 2d-2 >= 6 coordinates at d >= 4
     (matched-base stars need |R| = 2d >= 8; free rows 2d >= 8; alias pairs
     absent in normal form); support <= 4 < 6 completes nothing, and even
     support 5 is clean at d >= 4 (the 5 fresh columns alone answer the base
     coin) -> the per-rho law {0, 1/2, 1} is EXACT on the scanned class
[V2] (9,4): 90 restrictions, 3000 configurations (win=1096 + sampled/panel)
[V2] (9,4) pure-query three-way agreement (concrete == weight_pattern == DP): asserted
[V2] (9,4) MAX posterior = 72/73 = 0.986301 [pairs_win] vs q4_cov = 0.982759
     [attained by (1,)] -> EXCEEDED
[V2] (9,4) argmax = (((0, 0),), ((0, 0), (1, 1), (2, 2)))
[V2] (9,4) single-query certificates (posterior = 1 with positive numerator): 0
[V2] (9,4) killed-branch mass exactly 0 on 51000 (config, rho) pairs ->
     Theorem M4-1 SELF-EXCLUDED (machine check)
[V2]   0.986301 [pairs_win] (((0, 0),), ((0, 0), (1, 1), (2, 2)))          [+7 ties]
[V2] (9,4) family agreement on 18 families (concrete == weight_pattern == DP): PASS
[V2] (9,4) max live-column count over all (config, rho): 4 (<= 4, canary consistent)
[V2] (10,4): 4950 restrictions, 1503 configurations (win=279 + sampled/panel)
[V2] (10,4) MAX posterior = 36/37 = 0.972973 [disjoint] vs q4_cov = 0.965772
     [attained by (1,)] -> EXCEEDED
[V2] (10,4) argmax = single + three disjoint triples, family (0,2,2,2) [+3 ties]
[V2] (10,4) single-query certificates: 0; killed-branch mass exactly 0 on
     2434860 (config, rho) pairs -> Theorem M4-1 SELF-EXCLUDED
[V2] (10,4) family agreement on 18 families ...: PASS (0 bad)
[V6] mechanism table at (10,4): [8 families; killed-branch mass 0.000000
     everywhere; see section 5.2]
[V3]   (15,4)  q 0.837209 q_and 0.885246 post3 0.868346 post4 0.840326
       q4_cov 0.885246 max_mix 0.900518 excess +0.015272 (1.527e-02)
       max/post4 1.071629 argmax (1, 1, 1, 1)
[V3]   (31,4)  ... max_mix 0.692236 excess +0.011527 (1.153e-02)
       max/post4 1.065000 argmax (1, 1, 1, 1)
[V3]   (63,4)  ... max_mix 0.461731 excess +0.000134 (1.336e-04)
       max/post4 1.011629 argmax (2, 2, 2, 2)
[V3]   (127,4) ... excess +0.000000 (1.816e-07) max/post4 1.000001 argmax (3, 3, 3, 3)
[V3]   (255,4) ... excess +0.000000 (7.713e-09) max/post4 1.000000 argmax (3, 3, 3, 3)
[V3]   (1023,4) ... excess +0.000000 (9.430e-12) max/post4 1.000000 argmax (3, 3, 3, 3)
[V3]   (15,5)  ... max_mix 0.954537 excess +0.007979 (7.979e-03)
       max/post4 1.032415 argmax (1, 1, 1, 1)
[V3] exact (15,4): max - q4_cov = 1887494/123594357 = 1.527e-02;
     max = 1824572/2026137 = 0.900518 [(1, 1, 1, 1)]; q4_cov = 54/61 = 0.885246
[V3] exact (31,4): max - q4_cov = 138089986902/11979477717925 = 1.153e-02;
     max = 3969661068/5734551325 = 0.692236 [(1, 1, 1, 1)]; q4_cov = 1422/2089
[V4] (15,4) star-5Q (5 disjoint quads through c, support 5): post = 0.843356 vs
     q4_cov = 0.885246 -> DOMINATED
[V4] (31,4) star-5Q ...: post = 0.650081 vs q4_cov = 0.680708 -> DOMINATED
[V4] (11,4) free-base degree-4 star-completed query (5 fresh quads + the g3
     column; support 6): determined-0-with-6-live on 336 of 217800 restrictions
     (the wrinkle EXISTS at support 6 = 2d-2, d = 4); post true(folded) =
     0.931760 vs naive = 0.932586 vs q4_cov = 0.949062 -> DOMINATED
[V5] (10,4) budget 7:  kj_direct=0.8527 zfold2=0.2220 single_scan=0.9047
     mix3M_scan=0.8913 mixQQQ_scan=0.8100 (certified-output violations 0)
[V5] (10,4) budget 15: kj_direct=0.9940 zfold2=0.3100 single_scan=0.9467
     mix3M_scan=0.9450 mixQQQ_scan=0.8560 (certified-output violations 0)
[V5] (10,4) budget 30: kj_direct=0.9957 zfold2=0.3320 single_scan=0.9483
     mix3M_scan=0.9540 mixQQQ_scan=0.8610 (certified-output violations 0)
[done] total 28.3s
```

(The (9,4)/(10,4) top-8 lists, the complete V6 branch table, and the
V5 census fields are abridged here; their full content is in sections
2, 5, and 8. Every printed number above is verbatim from the run; long
machine lines are re-wrapped for the corpus.)

## 10. Verdict and open residuals

1. VERDICT (MIXTURE-4). Theorem 3'''-type cap structure extends to the
   FULL printed degree-$\le 4$ class with the constant repaired to
   $q_4^{\mathrm{mix}}(n,d) > q_4^*$, attained by star mixtures through
   the output pair (star-4M for $n \le 31$, triple/quad stars beyond),
   with the excess finite-$n$ only (peak $+0.0153$ at $(15,4)$, relative
   $o(1)$ by $(255,4)$), the same aliveness condition
   $d^2 \log k = o(n)$, and the same modulo set as Theorem 3''. No
   genuine degree-4 mixture gap opens: the self-exclusion mechanism
   extends verbatim (Theorem M4-1, machine-checked), no new single-query
   certificates exist (Theorem M4-B, $0$ of $4503$ scanned
   configurations), mixture certificates fold covered ones at equal
   budget (M4-E, measured sound), the support-4 wrinkle of
   mixture3.md does not exist at $d \ge 4$ (it lives at support
   $2d - 2 \ge 6$), and no budgeted mixture gain appears in regime
   (section 8). The MIXTURE-d scope gap is now closed at $d \le 4$ and
   remains open at $d \ge 5$.
2. Residual (support $\ge 5$): the scan is exhaustive up to
   isomorphism for through-output $\le 2$-term configurations (dense
   window), complete by family for the disjoint stars, and exhaustive
   within the one-row/one-column and $2 \times 4$ shared classes at
   $(9,4)$; 3/4-term beyond-window shared geometries are SAMPLED.
   Dominance beyond support 4 is CONJECTURED with the dilution argument;
   the support-5 star-5Q and the support-6 star-completed queries are
   MEASURED DOMINATED at the probed points.
3. Residual (the corrected support arithmetic): mixture3.md section
   2.2's support-4 attribution at $d = 3$ is off by the base-column
   coordinate (the corrected first breakdowns are support 5 at $d = 3$
   and support $2d - 2$ at degree $d$); no mixture3 registered result
   depends on it. Recorded here so the degree-5 agent inherits the
   right truncation calculus.
4. Residual (constants): $\epsilon_4$ decays along the grid with the
   argmax migration $(1,1,1,1) \to (2,2,2,2) \to (3,3,3,3)$ mirroring
   deg4_theory.md's post3/post4 crossover; no closed form was extracted
   (the pattern-table rational is the exact value, as at degrees 2
   and 3).
5. Residual (marked pieces in Theorem M4-D): the two JDP composition
   steps are inherited unchanged from Theorem 3''; the rate-weighted
   elevation sup is measured at degree 2 only [marked]; the two-query
   mixture certificate classification beyond the folded families is
   open (same status as Propositions M-E and M3-E).
6. Standing caveats inherited: Theorem A's base (singles vary) at
   general $d$, REL-4's completeness, and the general-$d$
   classification (Lemma CLS) carry all statements beyond the
   machine-verified points, as everywhere in the corpus.
7. Implication for O2: the MIXTURE-d scope gap is closed at
   $d \in \{2, 3, 4\}$ with constant-only repairs and the SAME
   aliveness condition; the degree-4 template adds exactly one new
   normal-form class (matching-4), one new completion class (degree-4
   stars, cost $n-3$), and one new tie-breaking term family (star-4M),
   and the degree-5 agent should expect the same shape with the
   breakdown threshold moving to support $2d - 2$.

## 11. One-paragraph verdict for the orchestrator

MIXTURE-4 is resolved with a repaired statement: over the FULL printed
degree-$\le 4$ class (all $\mathbb{F}_2$ mixtures of singles and
matching-2/3/4 monomials), the exact per-hit posterior maximum
$q_4^{\mathrm{mix}}$ exceeds the covered constant
$\max(q, q_{\mathrm{and\_exact}}, \mathrm{post}_3, \mathrm{post}_4)$ at
every measured point, by up to $+0.0153$ at $(15,4)$ and by a relative
$o(1)$ asymptotically ($\mathrm{max}/\mathrm{post}_4 = 1.000000$ from
$(255,4)$ on); the maximizers are monomial-star mixtures through the
output pair, with a NEW degree-4-class winner, the four-diagonal
star-4M, which also beats the degree-3 class maximum
$q_3^{\mathrm{mix}}$ by $+0.0040$ at $(15,4)$; the mechanism is the
verbatim extension of killed-branch self-exclusion plus
partner-parity dilution (Theorem M4-1, machine-checked: killed-branch
answer mass exactly 0 on 2.49M (config, rho) pairs), the small-$c$
winners hit the exactly-characterized ceiling $f/(f+m)$ (72/73 at
$(9,4)$, 36/37 at $(10,4)$), there are no new single-query
certificates (Theorem M4-B, 0 of 4503), mixture certificates fold
covered ones at equal budget (M4-E, measured sound), and no budgeted
mixture strategy beats the covered kj_direct champion at any tested
budget in regime. The task's support-4 worry dissolves with a
correction: the first per-rho law breakdown at degree $\le 4$ is the
free-base degree-$(d-1)$ star at support $2d - 2 \ge 6$ (at $d = 3$ it
is support 5, correcting mixture3.md section 2.2's support-4
attribution without touching any registered result), so support
$\le 4$ is provably clean at every $d \ge 3$ and the breakdown is
exhibited by positive controls at $(8,3)$ support 5 and $(11,4)$
support 6 where it actually lives, with the completed queries
posterior-dominated. Theorem 3'''-type budgeted caps extend to the
full printed quantifier at degree 4 with the constant
$q_4^* \to q_4^{\mathrm{mix}}$ and the SAME aliveness condition
$d^2 \log k = o(n)$ (Theorem M4-D, Corollary M4-D1, same modulo-JDP
status plus the inherited marked pieces), so the MIXTURE-d scope gap
is closed at $d \le 4$ and remains open only at $d \ge 5$.
