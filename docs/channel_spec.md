# Channel specification (FROZEN): the $\Omega(n,d)$ answer channel

Written 2026-10-04 (channel-spec agent), discharging GUIDANCE.md item 4:
"freeze the channel semantics in a written spec before coding".
This document is the single frozen statement of the channel semantics that
every corpus simulation must implement.
It states only CURRENT final forms; the layered corrections stay in their
home files as audit trail, and each supersession is noted here in one line
(the full ledger is Section 6).
If a simulator disagrees with this document, the simulator is wrong until
this document is amended by the orchestrator (new dated section plus a
LOG.md entry; this file is not edited in place after freeze).
Style: one sentence per line; math in LaTeX; markers [PROVED], [MV]
(machine-verified in a registered run), [MEASURED], [CONJECTURED], [GAP],
[SPEC-DERIVED] (an elementary derivation made in this document from sourced
facts, not stated as such in the corpus).
The primary case is $p = 2$; general $p$ is stated where the corpus supports
it.

## 1. The pipeline

### 1.1 Parameters, statuses, and the matching

Fix the characteristic $p$ (the reduction is printed for a fixed arbitrary
prime, arXiv:2609.35927, and the chi-task is characteristic-uniform,
proof_complexity.md "The p > 2 analogue").
Fix the outer dimension $n$ and the degree $d$ with $2d \le n$.
A configuration is a pair $(\rho, L)$ (cert_floor.md Setup).
$\rho$ is a uniform random partial injection from $[n+1]$ to $[n]$ leaving
exactly $n_\rho = 2d$ holes unfilled (arXiv:2609.35927 Definition 4.3, as
reproduced in paper/p2_results.tex def:pipeline item 1).
Equivalently, $\rho$ is uniform over triples $(D, R, \mu)$ where
$D \subseteq [n+1]$ is the free-pigeon set with $|D| = 2d+1$,
$R \subseteq [n]$ is the free-hole set with $|R| = 2d$, and
$\mu : [n+1] \setminus D \to [n] \setminus R$ is a bijection on the killed
pigeons and killed holes, giving $c = n - 2d$ matched pairs
(def:pipeline item 1; this is exactly how deg3_theory.md Theorem P3's proof
counts configurations).
An outer pair $(i,j)$ is FREE if $i \in D$ and $j \in R$ (there are
$(2d+1)\,2d$ free pairs), MATCHED if $\rho(i) = j$ (there are $c$), and
KILLED-UNMATCHED otherwise (def:pipeline; deg2_theory.md Section 1).
Notation used below: $f = (2d+1)2d/((n+1)n)$, $m = c/((n+1)n)$,
$A = (2d+1)/(n+1)$ (deg2_theory.md Section 1).
Queries are polynomials of degree $\le d$ in the outer variables; a tree is
an adaptive decision tree of depth $e$ whose leaves are labelled by pairs
(paper def:solution, quoting Definition 3.1 of arXiv:2609.35927).

All $\rho$ with the same free sizes give isomorphic restricted systems, and
the answer channel factors through the isomorphism class
(kernel_structure.md Section 1, the canonical-$Z$ convention).
Consequence for simulators: answer-law work may fix the canonical
restriction (pigeon $i \to$ hole $i$ for $i < c$, 0-based); any quantity
that depends on WHICH pairs are free must sample $(D, R, \mu)$ uniformly
(kernel_structure.md Section 1; cert_floor.md Setup).

### 1.2 The restricted system over $\mathbb{F}_p$

The restricted system is $\neg\mathrm{PHP}$ on the rectangle $D \times R$,
still contradictory ($2d+1$ pigeons, $2d$ holes) (def:pipeline item 1).
Its polynomial system over $\mathbb{F}_p$ has exactly these generators
(experiments/razborov_check.py, system_polys docstring; odd_p_theory.md
Section 1):

- hole-collision monomials $x_{i_1 j}\, x_{i_2 j}$ with $i_1 \ne i_2$;
- two-hole monomials $x_{i j_1}\, x_{i j_2}$ with $j_1 \ne j_2$;
- the pigeon-placed rows $Q_i = 1 - \sum_j x_{ij}$ (at $p = 2$ written
  $Q_i = 1 + \sum_j x_{ij}$; minus equals plus);
- the Boolean rows $x_{ij}^2 - x_{ij}$ (at $p = 2$: $x^2 + x$).

$V(2d,d)$ is the span of all generator rows shifted by monomials so that the
shifted degree stays $\le d$ (razborov_check.py; kernel_structure.md
Section 1; deg4_theory.md Section 1(b), the witness-algebra instrument).

### 1.3 Designs and the answer

$L$ is a uniform random degree-$d$ DESIGN of the restricted system: an
$\mathbb{F}_p$-linear functional on the degree-$\le d$ multiset monomials of
the variables $\{x_{ij} : (i,j) \in D \times R\}$, with
$$L(1) = 1, \qquad L|_{V(2d,d)} = 0$$
(def:pipeline item 2; designs exist, proof_complexity.md dimension tables,
$\dim \mathrm{Des} = 65$ at $(4,2)$ and $2079$ at $(6,3)$).
The answer to a query $g$ is
$$\mathrm{ans}(g) = \omega(g) := L(g^\rho)$$
(def:pipeline item 3).
The restriction $g^\rho$ substitutes $x_{ij} \mapsto 1$ if $\rho(i) = j$,
$x_{ij} \mapsto 0$ if $i$ is assigned and $j \ne \rho(i)$, and leaves
$x_{ij}$ untouched on $D \times R$ (def:pipeline item 3).
The printed clause leaves the cell (free pigeon, matched hole) uncovered;
the ZEROING COMPLETION sets such cells to $0$, the only choice consistent
with the determined killed-unmatched answer (paper def:pipeline item 3 and
Remark rem:proofroute; kernel_structure.md Sections 1 and 7).
Supersession note: the earlier disjoint-support proof route for the joint
law fails at $d \ge 2$ and is superseded by the zeroing completion
(proof_complexity.md ADDENDUM 2 item 3; paper rem:proofroute).

### 1.4 The one-kernel fact

$V(n,d)^\rho = V(2d,d)$ EXACTLY: the printed outer vanishing condition and
canonical design membership impose the same constraints
(kernel_structure.md Finding 1, [MV] at $(2,1)$, $(4,2)$, $(6,3)$ with
both-way containment; paper Remark rem:onekernel, with a coefficient-free
reason).
Supersession note: the corpus's earlier outer-vs-canonical design-space
debate is dissolved and retired as a definitional matter
(kernel_structure.md Finding 1; proof_complexity.md ADDENDUM 2 item 1).

## 2. The answer function, by query class

Every statement in this section is unconditional at the verified kernel
points (restricted $(2,1)$, $(4,2)$, $(6,3)$, i.e. outer $d \le 3$) and
carries its stated status at general $d$.

### 2.1 Degree-1 variables

For a single-variable query $x_{ij}$, at every $p$ [PROVED]:

- killed-unmatched: $\mathrm{ans} = 0$ deterministically
  (kernel_structure.md Finding 2; deg2_theory.md F1; odd_p_theory.md
  Theorem ChP(i); paper thm:channel(ii)).
- matched: $\mathrm{ans} = 1$ deterministically (same sources, ChP(i)).
- free: $\mathrm{ans}$ is uniform on $\mathbb{F}_p$, marginally always, and
  the answers of any row-incomplete query set (no row of the rectangle has
  all $2d$ of its cells queried) are JOINTLY uniform: independent die rolls
  (kernel_structure.md Finding 2, tests C2/C3/C4; odd_p_theory.md Theorem
  ChP(ii)/(iii); paper thm:channel(iii), from lem:completion(a)).

The joint law of the full free-region single table $M$ given $\rho$
[PROVED, every $p$]: the product over the $2d+1$ free rows of the uniform
measure on the sum-$1$ hyperplane
$\{a \in \mathbb{F}_p^{2d} : \sum_j a_j = 1\}$, which has $p^{2d-1}$
points, with rows independent (odd_p_theory.md Theorem ChP(ii); at $p=2$:
kernel_structure.md Finding 2 and deg2_theory.md F2).
Killed rows of $M$ show exactly one $1$ (at $\mu(i)$); killed columns show
exactly one $1$ (at $\mu^{-1}(j)$); free columns carry i.i.d. uniform
entries on their $2d+1$ free-pigeon cells (deg2_theory.md F2;
odd_p_theory.md ChP(iv)).
ROW LOCK (rigidity) [PROVED, every $p$]: every design satisfies
$\sum_{j \in R} L(x_{ij}) = 1$ for every free pigeon $i$ (paper
prop:rigidity, eq:rowparity; odd_p_theory.md Section 1).

### 2.2 The row-sum query $Q_i$

Define $Q_i := 1 - \sum_j x_{ij}$ (at $p = 2$ written $1 + \sum_j x_{ij}$).

- $\mathrm{ans}(Q_i) = 0$ DETERMINED on EVERY pigeon, free or killed, at
  every $p$ [PROVED]: $Q_i$ is a system polynomial, so $L(Q_i^\rho) = 0$
  for every design (deg2_theory.md F3, measured $0$ ones in $950{,}000$
  free-pigeon queries; kernel_structure.md Finding 2 C6, $0.0000$ at all
  three points; odd_p_theory.md Theorem ChP(v) and item Q1; paper
  prop:rigidity).
- The exact-lock statement behind it: on a free row the design values sum
  to exactly $1$ (Section 2.1 row lock); on a killed row the zeroing
  restriction gives $Q_i^\rho = 1 - 1 = 0$ identically (paper prop:rigidity
  proof).
- Consequence: row-sum queries carry no information, and a simulator that
  answers $Q_i$ with a fresh coin (or with parity $1$) on free pigeons is
  NON-CONFORMING (kernel_structure.md Findings 2 and 4; deg2_theory.md F3).
- Supersession note: the two-phase tree's parity certificate and Theorem
  T's law are coin-model-only objects, retracted as pipeline statements
  (kernel_structure.md Findings 2-3; deg2_theory.md F3 and Section 10
  item 3; cert_floor.md channel-law audit; two_phase_tree.md).

### 2.3 The column-parity query $K_j$

Define $K_j := 1 - \sum_i x_{ij}$ (at $p = 2$ written $1 + \sum_i x_{ij}$).

- $K_j$ is NOT a system generator at any $p$: the hole-exactly-one
  condition is not part of $\neg\mathrm{PHP}$ (deg2_theory.md F5;
  odd_p_theory.md Section 1, with [MV] support: the single-variable
  projected kernel has dimension $(2d+1)(2d-1)$ at $(4,2)$ for
  $p \in \{2,3,5\}$, so the only single-variable relations are the row
  rows).
- Killed column $j$: the cell column is
  $(0,\ldots,0,1,0,\ldots,0)$ determinedly, so $\mathrm{ans}(K_j) = 0$
  always [PROVED, every $p$] (odd_p_theory.md Theorem KP; deg2_theory.md
  F5).
- Free column $j$: the free-pigeon entries are i.i.d. uniform
  $\mathbb{F}_p$ values, so $\mathrm{ans}(K_j)$ is uniform on
  $\mathbb{F}_p$ and $P(\mathrm{ans}(K_j) \ne 0) = (p-1)/p$ [PROVED,
  every $p$] (odd_p_theory.md Theorems ChP(ii)/(v) and KP).
- Value certificate: $\mathrm{ans}(K_j) \ne 0$ certifies $j \in R$ with
  posterior exactly $1$ (odd_p_theory.md Theorem KP; deg2_theory.md F5 and
  Theorem 4).
- Column relation at $p = 2$ [MV]:
  $\bigoplus_{j \in R} \mathrm{ans}(K_j) = 1$, a consequence of the row
  pins read through the column view (lemma_m.md Section 2.2 E_K,
  $20000/20000$ designs at both tested points, lemma_m.md Section 7).
  [SPEC-DERIVED] General-$p$ form: the same derivation gives
  $\sum_{j \in R} \mathrm{ans}(K_j) = -1$ in $\mathbb{F}_p$ (sum the row
  locks: $2d - (2d+1) = -1$); the corpus states the relation only at
  $p = 2$, so treat the odd-$p$ form as derived here, not separately
  machine-verified.

### 2.4 Degree-2 monomials

Write a degree-2 monomial as a square $x_{ij}^2$, a same-line product
$x_{ij}x_{ij'}$ (same pigeon, $j \ne j'$) or $x_{ij}x_{i'j}$ (same hole,
$i \ne i'$), or a diagonal product $x_{ab}x_{cd}$ ($a \ne c$, $b \ne d$).

- Squares: $\mathrm{ans}(x^2) = \mathrm{ans}(x)$, the Boolean generator, at
  every $p$ [PROVED; MV at $(4,2)$ for $p \in \{2,3,5\}$]
  (kernel_structure.md Finding 4 table; lemma_m.md Section 2.1;
  odd_p_theory.md Section 2, V1 check list).
- Same-line products answer $0$ determinedly on EVERY status
  configuration: same-pigeon needs $\rho(i) = j = j'$ or a two-hole
  generator; same-hole needs two pigeons on one hole or a collision
  generator; a one-matched same-line product kills its other factor
  (a matched hole leaves every other pigeon killed-unmatched there)
  [PROVED; MV membership]
  (lemma_m.md Section 2.1, which sharpens O5's parenthetical: the
  matched-matched exception never lies on a line; kernel_structure.md
  Finding 4, the B5 classification: $40/40$ and $30/30$ pivot at $(4,2)$,
  $126/126$ and $105/105$ at $(6,3)$; deg3_theory.md Lemma D3, the $231$
  same-line degree-2 columns).
- Diagonal product, by status (at $p = 2$ fair bits, at general $p$ uniform
  $\mathbb{F}_p$ values; this is the fresh-bit law of Section 3.1):
  both components free, a fresh value independent of the two component
  singles (rank $3/3$) and of other diagonals (rank $2/2$), subject only to
  the star sum rule below [MV at $(4,2)$ and $(6,3)$; general $d$ modulo
  Lemma CLS] (deg2_theory.md F4; kernel_structure.md Finding 4, diagonal
  rows and C7; lemma_m.md Sections 2.3 and 3.3).
  One component matched, one free: the free component's own value, exactly
  (the restriction collapses the product to the free single) [PROVED,
  every $p$] (lemma_m.md Section 1.1; deg3_theory.md Theorem P3's status
  decomposition).
  At odd $p$ the degree-2 components of this bullet are supported by the
  star rule and alias checks at $(4,2)$ and by the digit-exact posterior
  substitution at outer $(7,2)$, $(8,2)$, $(9,2)$ (odd_p_theory.md
  Sections 2 and 4); the $p = 2$ rank facts above were measured at
  $(4,2)$ and $(6,3)$.
  Both matched: $1$, automatically diagonal by injectivity [PROVED]
  (lemma_m.md Section 2.1).
  Any killed component: $0$ [PROVED] (lemma_m.md Section 1.1).
- STAR SUM RULE (the Q-shift lock) [PROVED at every $d \ge 2$, every $p$]:
  for a free pigeon $r \ne c$ and a target pair $(c,d)$,
  $$\sum_{j \in R \setminus \{d\}} \mathrm{ans}(x_{rj}\, x_{cd})
      = \mathrm{ans}(x_{cd})$$
  (sum in $\mathbb{F}_p$; at $p = 2$: XOR): the row $Q_r\, x_{cd}$ has
  degree $2 \le d$ and is a generator of $V$ at every $d \ge 2$, the
  killed-$j$ terms vanish, and the same-hole terms are themselves
  generators (lemma_m.md Section 2.2 E_STAR, PROVED by the generator
  argument, [MV] $80/80$ star rows at $(4,2)$ and $252/252$ at $(6,3)$;
  deg2_theory.md F4, the shift sum rules; odd_p_theory.md Section 2, star
  sum rules at $(4,2)$ for $p \in \{2,3,5\}$ with $0$ violations).
- Consequence: the diagonal answers are not mutually independent globally;
  but every determined relation among them is an IDENTITY
  (configuration-invariant) and carries zero information about $\rho$
  (deg2_theory.md F4).
- Non-conforming product semantics: the rule "a monomial answers the
  product of its factor answers" fails on the pipeline in three places:
  same-line products ($0$ versus $1$ w.p. $1/4$ on two free factors), the
  star rule (identity versus holds w.p. $1/2$), and diagonal products
  (fresh bit versus product); on a free triangle
  $\{x_{ab}, x_{cd}, x_{ab}x_{cd}\}$ the true law is uniform on $8$ patterns
  and the product law lives on $4$, TV $= 1/2$, with no completion event
  needed [MV] (kernel_structure.md Finding 4 table; lemma_m.md Sections 0
  and 2.2, triangle check at $(4,2)$; deg2_theory.md F6).

### 2.5 Degree-$k$ monomials, $3 \le k \le d$

A degree-$k$ monomial is a product of $k$ outer cells (multiset; repeated
variables allowed).
Three mechanism classes exhaust every monomial column at every tested
degree [PROVED at $(6,3)$ exactly; at $(8,4)$ via Theorem A plus witness
algebra; the three-class partition is [CONJECTURED] to persist at all
degrees] (deg3_theory.md Lemma D3; deg4_theory.md Sections 2 and 6
forward note).

1. COLLISION class (all-distinct, containing a same-pigeon or same-hole
   pair): determined $0$; the monomial is literally a generator row
   (collision or two-hole monomial times a monomial, degree staying
   $\le d$) [PROVED] (deg3_theory.md Lemma D3, the $7280$
   collision-containing triples at $(6,3)$; deg4_theory.md Lemma W4, the
   $817{,}110$ fixed-0 line-pair columns at $(8,4)$; lemma_m.md
   Section 2.1, the same-line mechanism).
2. ALIAS class (containing a repeated variable $x$):
   $\mathrm{ans}(m) = \mathrm{ans}(\mathrm{sqfree}(m))$, the value of its
   square-free reduction, which is fixed $0$ exactly when the reduction is
   same-line [PROVED at $p = 2$ by explicit witnessed generator sums; the
   Boolean rows exist at every $p$ and the alias check passed at $(4,2)$
   for $p \in \{2,3,5\}$] (deg4_theory.md Lemma A4, with the witness
   chains $x^3 + x$, $x^4 + x^2$, $x^4 + x$, $x^3y + xy$, $x^2y^2 + xy$,
   $x^2yz + xyz$, $x^2y + xy$; deg3_theory.md Lemma D3, the $462$ alias
   columns at $(6,3)$; odd_p_theory.md Section 2, V1).
   In particular $x^k \mapsto x$ for all $k \ge 1$: over the Boolean rows
   no higher field equation contributes anything beyond $x^2 = x$
   (deg4_theory.md Lemma A4).
3. MATCHING-$k$ class (all-distinct, $k$ distinct pigeons and $k$ distinct
   holes): every matching-$k$ column varies, for $1 \le k \le d$, at every
   restricted $(2d,d)$ [PROVED: Theorem A, the matching hierarchy, with
   induction base = the single-variable law of Section 2.1 (paper
   cor:coin), step = the star-row argument, orbit closure under
   $S_{2d+1} \times S_{2d}$] (deg4_theory.md Theorem A; deg3_theory.md
   Section 1, $4200/4200$ matching triples vary at $(6,3)$).
   By the balance lemma every non-determined coordinate is uniform under
   uniform designs ($p = 2$: a fair coin) [PROVED at $p = 2$;
   characteristic-uniform by the kernel-coset argument]
   (deg3_theory.md Section 2, balance lemma; odd_p_theory.md Section 4,
   the substitution rule).
   Joint law: matching-$k$ answers are i.i.d. uniform on any window
   carrying no complete star, no complete free row, and no alias pair [MV
   at $(6,3)$, degree 3; general $d$ modulo Lemma CLS] (deg3_theory.md
   Section 2 consequences, star-free window dimension 1 and $2^8$ patterns;
   lemma_m.md Section 3.3, Lemma CLS).
   At odd $p$ the matching-hierarchy induction is coefficient-free, but the
   corpus has not re-run the odd-$p$ kernel classification, so degree
   $\ge 3$ odd-$p$ statements are [CONJECTURED] template transfers
   (odd_p_theory.md Sections 0 and 9 item 1).
- STAR SUM RULES at degree $k$ (the degree-$\le d-1$ locks) [PROVED at
  every degree, every $p$]: for any monomial $g$ with $\deg g \le d - 1$
  and any pigeon $p$ outside it, the row $Q_p \cdot g$ has degree
  $\le d$ and lies in $V$, hence
  $$\sum_{j \in R \setminus \mathrm{holes}(g)}
     \mathrm{ans}(x_{pj} \cdot g) = \mathrm{ans}(g) \cdot [\,p \in D\,],$$
  with the terms on $g$'s own holes determined $0$ (collisions and
  two-holes) and the killed-$j$ terms $0$; the INJECTIVITY AUTOMATISM: if
  $\rho(p) \in \mathrm{holes}(g)$ then $\mathrm{ans}(g) = 0$
  (lemma_m.md Section 2.2 E_STAR; deg3_theory.md Section 2 star lemma,
  $0/20000$ violations; deg4_theory.md Theorem B, status decomposition
  exact over all $90$ restrictions at $(9,4)$; odd_p_theory.md Section 2,
  star sum rules at every $p$).
  The right-hand side is status-dependent, which is the only channel
  through which stars carry information (deg3_theory.md Section 2;
  deg4_theory.md Theorem B).
- Completion inventory at degree $\le 4$, the only determined-relation
  classes: free rows (cost $\Theta(n)$), degree-2 stars ($n - 1$),
  degree-3 stars ($n - 2$), degree-4 stars ($n - 3$), and alias pairs
  (per-query, configuration-invariant, zero information)
  (lemma_m.md Section 2.2; deg3_theory.md Lemma REL-3; deg4_theory.md
  REL-4).
- Supersession note: deg2_theory.md Lemma REL's final identification
  ("on the block-free event the true channel is exactly the stipulated
  i.i.d. product channel") is false at degree 2 and is repaired to the
  fresh-bit channel; the block-free structure claim stands with improved
  constants (lemma_m.md Sections 0 and 6 item 1).
- [GAP (CLS)] at general $d$: "every diagonal degree-2 column varies" and
  "every determined relation among degree-$\le 2$ coordinates is generated
  by the inventoried families (row parities, star rows, same-line pins,
  Boolean alias, $e_0$)" are Lemma CLS, open in general and verified
  exactly through restricted $(6,3)$ (lemma_m.md Section 3.3;
  deg3_theory.md Section 1, the orbit argument).

### 2.6 Linear forms

$L$ is $\mathbb{F}_p$-linear with $L(1) = 1$, so for any affine-linear
query $g = a + \sum_{u \in S} x_u$ the answer is
$\mathrm{ans}(g) = a + \sum_{u \in S} \mathrm{ans}(x_u)$, the sum in
$\mathbb{F}_p$ [PROVED] (cert_floor.md Lemma 1 at $p = 2$; linearity is
built into the design space, def:pipeline item 2; the $\mathbb{F}_p$
machinery is chi_odd_p_check.py's).

## 3. The fresh-bit channel and its exact validity regime

### 3.1 The stipulation (the frozen simulator semantics)

The FRESH-BIT CHANNEL at degree $\le 2$ (lemma_m.md Sections 0 and 1.1;
fair bits at $p = 2$, uniform $\mathbb{F}_p$ values at general $p$ by the
substitution rule, odd_p_theory.md Section 4; same statuses $(D, R, \mu)$
as the pipeline):

- singles: free gives a fresh value, matched gives $1$, killed-unmatched
  gives $0$ (Section 2.1);
- squares give their single's value; same-line products give $0$
  (Section 2.4);
- diagonal products: both free gives a fresh value independent of
  everything else; one matched gives the free component's value; both
  matched gives $1$; any killed component gives $0$;
- all fresh values are mutually independent and independent of $\rho$, and
  the stipulation is claimed only on windows that complete no relation
  family (Section 3.2).

Supersession note: the corpus's earlier stipulated channel (PRODUCT
semantics, proof_complexity.md and and_chain.md: a monomial answers the
product of its factor answers) is the WRONG stipulation, refuted by free
triangles at TV $1/2$; the fresh-bit law is the unique stipulation realized
by the pipeline off completion events [MV at $d \le 3$] (lemma_m.md
Sections 0 and 2.3; kernel_structure.md Finding 4).
Why "row-incomplete stipulation": the fresh-bit singles law is exactly the
design space's row-incomplete single-variable answer law; no reading of
Definition 4.3 as printed makes the coin channel (i.i.d. bits without the
locks) the whole design space, and no design space satisfying the printed
condition realizes it (kernel_structure.md Findings 2 and 5, item F6;
paper rem:onekernel and cor:coin with its $E_{\mathrm{full}}$ clause).

### 3.2 The completion events (alias-aware)

Fix a transcript of budget $e$ of degree-$\le 2$ queries.
The EFFECTIVE SINGLE SET of a transcript is its queried singles together
with the pairs underlying queried squares, because the alias
$\mathrm{ans}(x^2) = \mathrm{ans}(x)$ makes a square carry its single's
information (lemma_m.md Section 1.2; Section 6 item 4, where five
first-sweep violations were all alias-assembled rows, resolved by this
definition).
The transcript is BLOCK-FREE if it triggers none of the following
[each with TV $1/2$ against the stipulation on the completed window, at
$p = 2$] (lemma_m.md Section 2.2):

- E_ROW: the effective single set covers all $2d$ free columns of some free
  pigeon; the completed row is pinned to odd parity
  ($p = 2$: XOR $= 1$, only $2^{2d-1}$ of $2^{2d}$ patterns occur, the
  all-zero pattern never occurs) [MV: affine pin, value $1$]
  (lemma_m.md Section 2.2 E_ROW; kernel_structure.md Finding 2 C5;
  odd_p_theory.md Section 2, the full free row's coset is exactly the
  $p^{2d-1}$ sum-$1$ patterns).
- E_STAR: the transcript queries all $2d-1$ fresh products of some star
  $(r; (c,d))$ with $r$ free AND the target single $(c,d)$ is in the
  effective single set (a square of the target suffices, by the alias);
  the completed window's support is the parity coset
  $\bigoplus = \mathrm{ans}(x_{cd})$, $2^{2d-1}$ of $2^{2d}$ patterns [MV:
  support $8 = 2^{4-1}$ at $(4,2)$ and $32 = 2^{6-1}$ at $(6,3)$]
  (lemma_m.md Section 2.2 E_STAR and Section 7).
- E_K (only if linear-form queries are allowed): the queried $K_j$ cover
  all $2d$ free columns, pinning the window through
  $\bigoplus_{j \in R} \mathrm{ans}(K_j) = 1$ [MV $20000/20000$ designs]
  (lemma_m.md Section 2.2 E_K and Section 7).

No other discrepancy exists at degree $\le 2$: the BLOCK-FREE
IDENTIFICATION says that on every alias-aware block-free window the
pipeline's projected answer law EQUALS the fresh-bit law, exactly [MV at
$d \le 3$: $1192/1192$ windows at $(4,2)$ and $250/250$ at $(6,3)$, sizes
$2$ to $10$ coordinates, at $p = 2$; general $d$ = Lemma CLS] (lemma_m.md
Sections 2.3 and 3.3; kernel_structure.md Section 3 C4; at odd $p$ the
relation list is exactly $p = 2$'s, the identities being coefficient
patterns of the same rows, with the inventoried relations verified at
$(4,2)$ for $p \in \{2,3,5\}$, odd_p_theory.md Lemma REL-p and Section 2
V1).

### 3.3 The validity regime and the $\varepsilon$ bound

Lemma M (transcript-level transfer) [PROVED at $d \le 3$ modulo the
counting convention CNT; REDUCED at general $d$ to CLS + CNT]
(lemma_m.md Section 3.1): for any adaptive degree-$\le 2$ tree of budget
$e$,
$$d_{TV}\big(\mathrm{law}_\Omega(\tau),\ \mathrm{law}_{fb}(\tau)\big)
   \ \le\ \varepsilon(e,n,d)
   \ \le\ \frac{A}{2}\Big[\Big(\frac{e}{n}\Big)^{2d}
      + \Big(\frac{2e}{n-1}\Big)^{2d-1}\Big],
   \qquad A = \frac{2d+1}{n+1},$$
where $\tau$ is the transcript, $\varepsilon = \varepsilon_{row} +
\varepsilon_{star}$, and if linear-form queries are allowed one adds
$\varepsilon_K \le \tfrac12 (e/n)^{2d}$.
The bound is $o(1)$ exactly when $e = o(n)$; a row event needs $e \ge 2d$
and a star event $e \ge 2d$, so at $e < 2d$ the transfer is EXACT
(lemma_m.md Section 3.1).
This is the precise form of "below per-row cost $\Theta(n)$ the true
channel is exactly the stipulated channel", matching the kernel facts that
the TV between coin law and design law is exactly $0$ on every
row-incomplete query set and exactly $1/2$ on a fully queried free row
(deg2_theory.md ADDENDUM 3, the Lemma REL entry; kernel_structure.md
Section 5).
Supersession note: deg2_theory.md Lemma REL's bound
$p_{\mathrm{block}}(e) \le (2d+1)(e/n)^{2d} + (n+1)n(e/n)^{2d-1}$ and its
product-channel identification are superseded by Lemma M's constants
($A(e/n)^{2d}$ and $(2e/(n-1))^{2d-1}$) and by the fresh-bit
identification (lemma_m.md Sections 3.2 and 6 item 1); the paper's
single-variable union bound
$\min\{1,\ (n+1)\binom{e}{2d}/\binom{n}{2d}\}$ remains valid for the
single-variable class (paper cor:coin).
At $e = \Theta(n)$ the bound is vacuous and the transfer question is open,
assigned to O2(iv) (lemma_m.md Section 5 item 3; deg2_theory.md
Section 4).
At odd $p$ (degree $\le 2$): the same completion structure holds, with the
adversarial budget bound $P_{\mathrm{blk}}(e) \le e/(n - 2d - 2)$,
structure [PROVED], and the degree-3 odd-$p$ relations NOT recomputed
[CONJECTURED template transfer] (odd_p_theory.md Section 6 Lemma REL-p and
Section 9 item 1).

## 4. What this spec does NOT cover (explicit exclusions)

1. The full joint law on windows that DO complete relations at degree
   $\ge 3$: the spec states the pinned-coset form of a single completed
   star (Section 2.5) and the i.i.d. law on windows with no completion,
   but the joint law of mixed multi-relation windows at degree $\ge 3$ is
   not axiomatized in the corpus (deg3_theory.md Lemma REL-3 and
   deg4_theory.md REL-4 are completion INVENTORIES, not joint laws).
2. General-$d$ classification and adaptive counting: the degree-$\le 2$
   statements at general $d$ carry Lemma CLS and the adaptive completion
   count carries Lemma CNT, both open (lemma_m.md Sections 3.3 and 5);
   the spec is unconditional only at the verified kernel points
   ($d \le 3$) and for the non-adaptive counting (lemma_m.md Section 3.3,
   Lemma CNT's non-adaptive case PROVED).
3. Odd-$p$ degree $\ge 3$: not covered; the deg3 template (star sum rules,
   wedge/Z, posterior transfer with $1/2 \to 1/p$) is [CONJECTURED] and
   flagged (odd_p_theory.md Sections 0 and 9 item 1).
4. Downstream tree-level quantities: per-hit posteriors
   ($q$, $q_{\mathrm{and\_exact}}$, $\mathrm{post}_3$, $\mathrm{post}_4$,
   and their odd-$p$ forms), the budgeted caps (Theorems B, 3, 3', 3'',
   and their constants $q^*_2$, $q^*_3$, $q^*_4$), the certificate
   mechanisms (adjacency, wedge, Z, self-certification, the $K_j$-tree,
   counting), and the err-boundary results are CONSEQUENCES of this
   channel, not channel semantics; their channel-scope caveats stay in
   their files (for example cert_floor.md Theorem F is coin-channel-
   specific and the true unbounded optimum is $0$, deg2_theory.md
   Theorem 5).
5. The chi-task semantics: Definition 3.1's solution condition, the Span
   conjunct $1 \in \mathrm{Sp}(W(P)^\rho)$, the printed chi probabilities,
   and the $p^{-\dim}$ path weighting are out of scope
   (chi_transfer.md; proof_complexity.md ADDENDUM 4).
6. Budgets $e = \Theta(n)$ and unbounded budgets: the transfer question is
   open (lemma_m.md Section 5 item 3); no stipulated-channel claim is
   licensed there by this spec.
7. The characteristic-independence of $\dim \mathrm{Des}$ beyond $(4,2)$:
   measured at $(2,1)$ and $(4,2)$ for $p \in \{2,3,5\}$, no proof, no
   counterexample (odd_p_theory.md Section 9 item 5).
8. Lean artifacts: lean_channel/CoreChannel.lean proves facts about a
   convenience model (a killed row has exactly one 1, true by
   construction) and says nothing about this pipeline, so it is not a
   conformance instrument for this spec (GUIDANCE.md item 8; README Lean
   caveat; GOAL.md Section 4).
9. Historical stipulations (product semantics, the coin channel as the
   whole design space, chi_p2_adaptive.build()'s coset, which satisfies
   $L(Q_i) = 1$ instead of $0$) are NON-CONFORMING and remain only as
   audit trail (deg2_theory.md F6; kernel_structure.md Findings 4 and 5;
   proof_complexity.md "Design-space readings" fidelity note).

## 5. Conformance checklist

A simulator claims conformance to THIS spec only if it satisfies every
item of 5.1, 5.2, and 5.3, and implements 5.4 or 5.5.

### 5.1 Determinism table (exact on every status configuration, every $p$)

| # | Query | Determined answer | Source |
|---|-------|-------------------|--------|
| D1 | matched single $x_{ij}$, $\rho(i)=j$ | $1$ | kernel_structure.md Finding 2; deg2_theory.md F1; odd_p_theory.md ChP(i) |
| D2 | killed-unmatched single | $0$ | same as D1 |
| D3 | restricted cell (free pigeon, matched hole) | $0$ (zeroing completion) | paper def:pipeline item 3; kernel_structure.md Sections 1, 7 |
| D4 | $Q_i$, any pigeon, any $p$ | $0$ | deg2_theory.md F3; kernel_structure.md C6; odd_p_theory.md ChP(v); paper prop:rigidity |
| D5 | $K_j$, killed column | $0$ | deg2_theory.md F5; odd_p_theory.md Theorem KP |
| D6 | square $x^2$ | $\mathrm{ans}(x)$ | kernel_structure.md Finding 4; lemma_m.md 2.1; odd_p_theory.md V1 |
| D7 | same-line degree-2 product, all statuses | $0$ | lemma_m.md 2.1; kernel_structure.md B5; deg3_theory.md D3 |
| D8 | all-distinct degree-$k$ monomial with a line pair | $0$ | deg3_theory.md D3; deg4_theory.md W4 |
| D9 | alias monomial $m$ | $\mathrm{ans}(\mathrm{sqfree}(m))$; $0$ if the reduction is same-line | deg4_theory.md A4; deg3_theory.md D3 |
| D10 | diagonal product, one matched one free | the free component's value | lemma_m.md 1.1; deg3_theory.md P3 decomposition |
| D11 | diagonal product, both matched | $1$ | lemma_m.md 2.1 |
| D12 | any monomial with a killed factor | $0$ | lemma_m.md 1.1; restriction semantics |

### 5.2 Independence and uniformity statements (on the stated windows)

| # | Statement | Window / regime | Source |
|---|-----------|-----------------|--------|
| I1 | free singles marginally uniform on $\mathbb{F}_p$ | always | kernel_structure.md C2; odd_p_theory.md ChP(ii); paper thm:channel(iii) |
| I2 | free singles jointly i.i.d. uniform | row-incomplete sets | kernel_structure.md C3/C4; odd_p_theory.md ChP(iii); paper lem:completion(a) |
| I3 | full free row uniform on the sum-$1$ hyperplane ($p=2$: the $2^{2d-1}$ odd patterns, XOR $=1$, all-zero absent) | completed row | kernel_structure.md C5; odd_p_theory.md ChP(ii); paper thm:channel(iv) |
| I4 | killed rows exactly one $1$; killed columns exactly one $1$; free columns i.i.d. uniform | full table $M$ | deg2_theory.md F2; odd_p_theory.md ChP(iv) |
| I5 | $K_j$ uniform on $\mathbb{F}_p$ on free columns, $P(K_j \ne 0) = (p-1)/p$ | free columns | odd_p_theory.md ChP(v), Theorem KP |
| I6 | diagonal (both free) fresh value, independent of component singles (rank $3/3$) and other diagonals (rank $2/2$) | block-free windows; $d \le 3$ [MV], general $d$ modulo CLS | deg2_theory.md F4; kernel_structure.md C7; lemma_m.md 2.3 |
| I7 | matching-$k$ columns all vary ($1 \le k \le d$) and are marginally uniform | every $(2d,d)$ | deg4_theory.md Theorem A; deg3_theory.md balance lemma; odd_p_theory.md Section 4 |
| I8 | matching-$k$ answers i.i.d. uniform | star-free, row-free, alias-free windows [MV at $(6,3)$] | deg3_theory.md Section 2; lemma_m.md CLS |
| I9 | block-free window law equals the fresh-bit law exactly | alias-aware block-free windows [MV $d \le 3$: $1192/1192$, $250/250$] | lemma_m.md 2.3; kernel_structure.md C4; odd_p_theory.md REL-p |

### 5.3 The locks (identities every design satisfies)

| # | Lock | Statement | Source |
|---|------|-----------|--------|
| L1 | row lock | $\sum_{j \in R} L(x_{ij}) = 1$ for every $i \in D$, every $p$ | paper prop:rigidity; odd_p_theory.md Section 1 |
| L2 | star lock | $\sum_{j \in R \setminus \mathrm{holes}(g)} \mathrm{ans}(x_{pj} g) = \mathrm{ans}(g)\cdot[p \in D]$ for $\deg g \le d-1$; automatism $\rho(p) \in \mathrm{holes}(g) \Rightarrow \mathrm{ans}(g) = 0$ | lemma_m.md E_STAR; deg3_theory.md star lemma; deg4_theory.md Theorem B; odd_p_theory.md Section 2 |
| L3 | column relation | $p=2$: $\bigoplus_{j \in R} \mathrm{ans}(K_j) = 1$ [MV]; general $p$: sum $= -1$ [SPEC-DERIVED] | lemma_m.md E_K, Section 7; derivation in Section 2.3 above |
| L4 | global parity ($p=2$) | sum of free-row XORs $=$ XOR of all free coins $= 2d+1 \equiv 1$; the odd-column count in any free-region matrix is odd | deg2_theory.md Theorem 4 proof; cert_floor.md Theorem R identity |

### 5.4 Route A (exact kernel route; unconditionally conforming)

Sample $(D, R, \mu)$ uniformly (or fix the canonical $Z$ for answer-law
work only, Section 1.1), build $V(2d,d)$ over $\mathbb{F}_p$ from the
generator list of Section 1.2, impose $L(1) = 1$, and sample $L$ uniformly
from the affine solution coset (kernel_structure.md Section 1;
razborov_check.py; chi_odd_p_check.py for $\mathbb{F}_p$).
Registered instruments to reuse or reproduce: experiments/razborov_check.py,
experiments/kernel_structure.py, experiments/chi_odd_p_check.py.

### 5.5 Route B (stipulated fresh-bit route; conforming inside the regime)

Implement Section 3.1's fresh-bit law and track the completion events
E_ROW, E_STAR, E_K alias-aware through the effective single set
(Section 3.2).
Conformance requires budget $e = o(n)$ (at $e < 2d$ the transfer is exact),
asserting the measured completion frequency against
$\varepsilon(e,n,d)$ of Section 3.3, and carrying the CLS/CNT caveat in
any claim at general $d$ (lemma_m.md Sections 3.1 and 3.3).
At odd $p$, counting certificates must count NONZEROS, with the free-row
nonzero-count law $P(c \text{ nonzeros}) = \binom{2d}{c}\frac{(p-1)^c - (-1)^c}{p \cdot p^{2d-1}}$
and count $0$ impossible (odd_p_theory.md Lemma CNT).

### 5.6 Known non-conforming patterns (must fail a conformance run)

1. Product semantics for diagonal products (free-triangle TV $1/2$)
   (lemma_m.md Sections 0 and 2.2).
2. I.i.d. row bits without the parity lock (legal fraction
   $2^{-(2d+1)}$ of coin samples) (kernel_structure.md Finding 4).
3. $Q_i$ answered as a fair coin or parity-1 on free pigeons
   (kernel_structure.md C6; deg2_theory.md F3).
4. Counting ONES instead of NONZEROS at odd $p$ (odd_p_theory.md
   Lemma CNT).
5. A "design coset" with $L(Q_i) = 1$ (chi_p2_adaptive.build()'s coset)
   (deg2_theory.md F6).

## 6. Supersession ledger (one line each; audit trails in the home files)

1. Disjoint-support proof route for the joint law: superseded by the
   zeroing completion (proof_complexity.md ADDENDUM 2 item 3).
2. Outer vs canonical design-space readings: dissolved, one kernel,
   $V(n,d)^\rho = V(2d,d)$ (kernel_structure.md Finding 1).
3. deg2_theory.md Lemma REL's identification (block-free = stipulated
   product i.i.d. channel): false at degree 2, repaired to the fresh-bit
   channel; REL's constants superseded by Lemma M's (lemma_m.md
   Sections 0 and 6 item 1).
4. Coin channel as the whole design space: false; it is exactly the
   row-incomplete single-variable law (kernel_structure.md Finding 5, F6;
   paper cor:coin).
5. Two-phase parity certificate and Theorem T's law: coin-model-only,
   retracted as pipeline statements (kernel_structure.md Findings 2-3;
   cert_floor.md channel-law audit).
6. cert_floor.md Theorem F's constant: coin-channel-specific; the true
   unbounded optimum is $0$ (deg2_theory.md Theorem 5).
7. p_family.md's Proposed Theorem $T_p$ (row-scan at $p > 2$): refuted at
   every characteristic; the surviving analogue is the $K_j$ column
   channel (odd_p_theory.md Section 7).
8. Theorem 3's cap constant $q$: repaired to
   $q^*_2 = \max(q, q_{\mathrm{and\_exact}})$ (downstream; recorded here
   because simulators comparing against caps must use the corrected
   constant) (lemma_m.md Sections 0 and 6 item 2).
9. The printed Theorem 6.1(3) "false as printed" heading: downgraded to a
   reading gap per GUIDANCE (proof_complexity.md ADDENDUM 4); not channel
   semantics, listed so the spec is not read through the retired framing.
