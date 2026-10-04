# Degree-4 extension of the true-pipeline theory: the degree-4 kernel
# classification (with the matching-hierarchy theorem), the exact per-hit
# posterior post4, the certificate mass proposition, and the budgeted cap at
# degree <= 4

Result of the deg4-theory agent (2026-10-04). Status: analysis, not
peer-reviewed. Task: extend the degree-$\le 3$ theory (deg3_theory.md) to
degree 4 on five questions: (1) the degree-4 kernel classification and the
degree-4 alias classes, (2) the degree-4 star sum rules, (3) the exact
per-hit posterior of an all-distinct degree-4 query with its asymptotic
behavior, (4) an exhaustive small-scale certificate search with attention to
degree-4-plus-collision combinations, (5) the cap extension (Theorem 3'' best
effort or the exact breaking mechanism).

Channel: the TRUE $\Omega(n,d)$ pipeline at $p = 2$ (uniform designs of the
restricted canonical system; kernel_structure.py F1: $V(n,d)^\rho = V(2d,d)$).
Script: chi_deg4_check.py (registered run, 14 s, 25 PASS / 0 FAIL; output
reproduced at the end). Everything is on the true channel. Markers:
[PROVED], [MEASURED], [MV] machine-verified, [CONJECTURED], [GAP].

Scale facts that drive everything. Degree-4 monomial columns exist only for
$d \ge 4$, so the smallest restricted system carrying them is $(8,4)$ = 9
pigeons $\times$ 8 holes = 72 variables, with
$|S(8,4)| = 1 + 72 + 2628 + 64840 + 1215450 = 1{,}282{,}975$ monomial
columns. The degree-3 instrument (full augmented echelon over the whole
monomial space, then a per-column membership sweep) does not survive this
scale: at the measured pivot fractions (0.71 at $(4,2)$, 0.854 at $(6,3)$)
the echelon alone needs 167-180 GB against 15 GB RAM, and the sweep is 88x
the $(6,3)$ sweep. This is itself a finding: the deg3 template's kernel
instrument dies at $d = 4$, and everything below is built from four
instruments that do survive: (a) a degree-$\le 2$ slice echelon at $(8,4)$
(2701 columns, exact), (b) WITNESS ALGEBRA (membership in $V$ by explicit
machine-checked generator-row sums, no echelon needed), (c) the new
matching-hierarchy theorem (star induction), which removes the need for any
sweep of the matching columns, and (d) F1-level enumeration on the outer
pipeline (restriction statuses only), exact because the per-$\rho$ answer
law is $\{0, 1/2, 1\}$ once the matching columns are known to vary.

Notation: $c = n - 2d$ (matched pairs), $q$, $q_{\mathrm{and\_exact}}$,
$\mathrm{post}_3$ as in deg3_theory.md; a matching-$k$ monomial is a
degree-$k$ monomial whose $k$ cells have distinct pigeons and distinct
holes; $b_m(n,d,k) = \binom{n+1-k}{c-m}\binom{n-k}{c-m}(c-m)!$ is the count
of configurations in which a FIXED set of $m$ pairs of a matching-$k$ $T$ is
matched and the rest of $T$ is free.

## 0. Summary (the five answers in one paragraph each)

Q1 (kernel classification). [PROVED + MV] Every degree-4 column at every
restricted system is exactly one of three mechanism classes: (i) FIXED 0:
all-distinct and containing a same-pigeon or same-hole pair (a collision or
two-hole generator monomial times a degree-$\le 2$ monomial: a literal
generator row), (ii) ALIAS: containing a repeated variable, value $= L$ of
its square-free reduction (Boolean-identity family $x^2 + x \in V$, witness
chains below), (iii) VARYING: all-distinct with no line pair, i.e.
matching4. Counts at $(8,4)$: 912,978 fixed-0 (817,110 line-pair
all-distinct + 94,248 $x^2yz$ alias-to-0 + 1,080 $x^3y$ alias-to-0 + 540
$x^2y^2$ alias-to-0), 302,472 varying-valued (211,680 matching4 + 84,672
$x^2yz$ alias-to-matching3 + 4,032 $x^3y$ + 2,016 $x^2y^2$ + 72 $x^4$);
$912{,}978 + 302{,}472 = 1{,}215{,}450 = \binom{75}{4}$ exactly. The alias
classes are ALL Boolean-identity consequences ($x^4 \to x$, $x^3y \to xy$,
$x^2y^2 \to xy$, $x^2yz \to xyz$); nothing new arises from higher field
equations. The supporting NEW THEOREM (matching hierarchy, Theorem A): at
every restricted $(2d,d)$, if matching-$(k-1)$ columns vary then matching-$k$
columns vary, for $k \le d$; with the corpus base (singles vary,
cor:coin + kernel measurements), ALL matching-$k$ columns vary for
$1 \le k \le d$. This closes deg3_theory.md open item 1 (their general-$d$
classification conjecture) and removes their diagonal-variation condition;
it also proves marginal fairness (balance) of every matching answer at
every degree, which is what makes the posterior theory below exact.

Q2 (star sum rules). [PROVED] The degree-4 stars: for any pigeon $p$ and
matching3 $g_3$ with $p$ outside it, the generator row $Q_p \cdot g_3$
(degree 4) gives
$\bigoplus_{j \in R \setminus \mathrm{holes}(g_3)} \mathrm{ans}(x_{pj} g_3)
= \mathrm{ans}(g_3)$ when $p$ is free and $= 0$ when $p$ is assigned, with
the injectivity automatism: $\rho(p) \in \mathrm{holes}(g_3)$ forces
$\mathrm{ans}(g_3) = 0$ (the $g_3$ cell at hole $\rho(p)$ is
killed-unmatched because $\rho$ is an injection). The degree-$\le 3$ stars
persist (their rows are still in $V$), and the alias relations gain the
degree-4 family (per-query, configuration-invariant, zero information).
REL-4 (the completion inventory) therefore has five classes: free rows
(cost $\Theta(n)$), degree-2 stars ($n-1$), degree-3 stars ($n-2$), NEW
degree-4 stars ($n-3$), alias pairs (per-query, info-free). No other
determined-relation class appears at degree 4.

Q3 (exact per-hit posterior). [PROVED + MV] For a matching4 $T$,
$\mathrm{post}_4 = P[p_1 \text{ free} \mid \mathrm{ans}(T) = 1] =
\frac{b_0 + 3b_1 + 3b_2 + b_3}{2b_4 + b_0 + 4b_1 + 6b_2 + 4b_3}$
with $b_m = \binom{n-3}{c-m}\binom{n-4}{c-m}(c-m)!$; digit-exact against
exhaustive enumeration at outer $(9,4)$, $(10,4)$, $(11,4)$, $(12,4)$ (the
first point where the all-matched class is nonempty; 8,494,200 restrictions,
both triples at $(9,4)$). General form:
$\mathrm{post}_k = \frac{\sum_{m<k} \binom{k-1}{m} b_m}{2b_k + \sum_{m<k}
\binom{k}{m} b_m}$, and $\mathrm{post}_k = \frac{2d^2+d}{c-k+1}(1+o(1))$ as
$c \to \infty$ at fixed $d$: NO asymptotic lift and NO demotion, the whole
single-pass family $\{q, q_{\mathrm{and\_exact}}, \mathrm{post}_3,
\mathrm{post}_4\}$ shares the leading form $2d^2/n$ and the ratios tend to
1 (measured 1.0013 at $(16383,4)$). Finite-$n$: $\mathrm{post}_4 -
\mathrm{post}_3$ changes sign on the grid (negative for $n \le 63$,
positive for $n \ge 127$ at $d = 4$), and $\mathrm{post}_4$ peaks at
$1.084 \times q_{\mathrm{and\_exact}}$ at $(255,4)$: a small finite-$n$
lift over the degree-2 hit, the same pattern deg3 found, vanishing as
$\Theta(d^2/n^2)$.

Q4 (certificates). [PROVED + MEASURED] The certain-mechanism inventory does
NOT grow at degree 4: the only F1-level certain mechanisms found in an
exhaustive 1- and 2-query search (all 736 symmetry classes over the 208-query
matching pool: singles, matching2, matching3, matching4 in a $4 \times 4$
window at outer $(9,4)$) plus 18,236 sampled 3-query classes are the
degree-generic wedge (adjacency included) and Z certificates and the
$c = 1$ shadow-pin artifact: 68,945 F1-certain patterns, 0 unexplained.
Degree-4 answers combined with degree-2 collision structure yield NO better
budget scaling: this is a proved mass proposition - every certain
certificate must consume at least one answer-1, its firing rate is at most
$e \cdot \max P(\mathrm{ans} = 1)$, and the answer-1 masses form the exact
dominance chain $P_4 < P_3 < P_2 < P_1 = h_1$ (e.g. $P_4 = 1.0 \times
10^{-8}$ at $(127,4)$ against the $K_j$ rate $d/n$: a dominance factor
$3 \times 10^6$), so any degree-4-dependent certificate is rate-dominated by
every degree-1 channel.
Q5 (cap). [ASSEMBLY, two modulo-JDP flags inherited] Theorem 3'' extends
the budgeted cap to the full adaptive degree-$\le 4$ class:
$\mathrm{success}(T) \le q_4^* + P_{\mathrm{adj}} + P_K + P_{\mathrm{cert4}}
+ P_{\mathrm{blk4}} + o(1)$ with $q_4^* = \max(q, q_{\mathrm{and\_exact}},
\mathrm{post}_3, \mathrm{post}_4)$ (achieved by $\mathrm{post}_4$ for
$n \ge 127$ on the grid), $P_{\mathrm{cert4}} \le e \cdot P_4 = o(P_K)$,
$P_{\mathrm{blk4}} \le e/(n - 2d - 3)$. The chi-hypothesis stays ALIVE
exactly when $d^2 \log k = o(n)$: the SAME boundary as degrees 2 and 3.
Nothing breaks at degree 4: the exact change list is one more star class
(cost $n-3$), the degree-4 alias family (info-free), a slightly purer
per-hit posterior (same leading form), and strictly dominated certificate
masses. The open core remains the all-degrees quantifier (O2); the
structural lesson for it is that the $k$-th degree adds a star class
costing $n-k+1$ queries and an evidence class of mass $\le$ the previous
degree's, which is why the $d^2 \log k = o(n)$ boundary has persisted
unchanged through degree 4 [CONJECTURED to persist at all degrees].

## 1. The instrument wall at d = 4, and the replacement instruments

The degree-3 classification ran a full augmented echelon at $(6,3)$
(14,190 columns, rank 12,110). At $(8,4)$: $|S| = 1{,}282{,}975$; the
corpus's measured rank fractions (0.707 at $(4,2)$, 0.854 at $(6,3)$)
project to a 1.1-1.2M-pivot echelon at ~160 KB per pivot row: 167-180 GB.
[MEASURED arithmetic; the machine has 15 GB.] The full sweep is declared
infeasible and nothing below depends on it.

What replaces it, and what each instrument proves:
  (a) Degree-$\le 2$ slice echelon at $(8,4)$: 1269 generator rows over
      2701 columns; exact classification of every degree-$\le 2$ column at
      $d = 4$. [MV this run]
  (b) Witness algebra: a vector is proved to lie in $V$ by exhibiting an
      explicit list of generator rows whose sum is the vector; the machine
      check verifies each listed row is a legal generator shift
      (system poly of the restricted grid times a monomial, deg $\le 4$)
      and the sum equals the target. No echelon is involved. [MV this run]
  (c) The matching-hierarchy theorem: reduces the varying-status question
      for ALL matching columns to the base case (singles), with a proved
      induction step. [PROVED step; base = cor:coin + MV]
  (d) F1-level outer enumeration: over restrictions $\rho$ only, using the
      proved per-$\rho$ answer law $\{0, 1/2, 1\}$ (all matched $\to 1$;
      any killed $\to 0$; else the free part is a matching-$j$ column,
      varying hence fair by (c) + balance). Exact, and cheap: 90
      restrictions at outer $(9,4)$, 8.49M at $(12,4)$. [PROVED
      soundness; the channel law it consumes is (c) + balance]

Instrument note (corpus discipline): an earlier draft of this analysis
claimed a fully analytic proof that singles are never value-determined at
general $d$ ("degree-$\ge 2$ rows have no single coordinates"). That is
FALSE: the Boolean rows $x^2 + x$ have a single coordinate, so combinations
of Boolean and $Q_i \cdot x$ rows can cancel their degree-2 parts and leave
single residues; no elementary graded argument was found within this
session. The base fact is therefore taken from the corpus (the completion
lemma cor:coin, the same standing general-$d$ fact under every prior
degree's posterior theory) plus the exact $(8,4)$ slice measurement here.

## 2. Q1: the degree-4 classification and Theorem A (matching hierarchy)

### 2.1 The three mechanism classes at degree 4

Lemma W4 (fixed-0 class). [PROVED] Any all-distinct degree-4 monomial
containing two cells that share a pigeon (distinct holes) or a hole
(distinct pigeons) is a generator monomial (line-pair times a degree-$\le 2$
monomial) and is determined 0. Count at $(8,4)$: 817,110.

Lemma A4 (alias class). [PROVED + MV] Any degree-4 monomial with a repeated
variable $x$ satisfies $\mathrm{ans}(m) = \mathrm{ans}(\mathrm{sqfree}(m))$,
where the square-free reduction has degree $\le 3$. Witness chains (each an
explicit sum of generator rows, machine-checked):
  $x^2 + x$                       (the Boolean generator itself),
  $x^4 + x^2 = x \cdot (x^3 + x)$ and $x^3 + x = (x^2+x) + x \cdot (x^2+x)$
                                  (2 rows: $(x^2+x)x^2 + (x^2+x)x$),
  $x^4 + x$                       (3 rows),
  $x^3y + xy = (x^2+x)xy + (x^2+x)y$  (2 rows),
  $x^2y^2 + xy = (x^2+x)y^2 + (y^2+y)x$  (2 rows),
  $x^2yz + xyz = z \cdot (x^2+x)$  (1 row).
So the degree-4 alias classes are exactly the Boolean-identity family: no
higher-degree field equation contributes anything beyond $x^2 = x$ at
degree 4 (over $\mathbb{F}_2$ with the Boolean axioms, $x^k = x$ for all
$k \ge 1$). Answer to the task's dichotomy: repetition-containing columns
are determined by BOOLEAN identities (and then only in the alias sense:
their value is a lower column's value, fixed 0 exactly when the reduction
is same-line); pipeline generators (collisions, two-holes) determine
exactly the line-pair-containing all-distinct columns; nothing else is
determined. Counts at $(8,4)$: alias-to-0: 94,248 ($x^2yz$) + 1,080
($x^3y$) + 540 ($x^2y^2$) = 95,868; alias-to-varying: 84,672 ($x^2yz \to$
matching3) + 4,032 ($x^3y$) + 2,016 ($x^2y^2$) + 72 ($x^4$) = 90,792.

Theorem A (matching hierarchy). [PROVED step; PROVED base via cor:coin + MV]
Fix a restricted system $(2d, d)$ and $1 < k \le d$. If every matching-$(k-1)$
column is design-varying, then every matching-$k$ column is
design-varying. Consequently, at every $(2d,d)$, every matching-$k$ column
varies for $1 \le k \le d$, and (by the balance lemma) its answer under
uniform designs is a fair coin.

Proof. Step: suppose all matching-$k$ columns were value-determined (fixed
value per $\rho$ across designs). Take any matching-$(k-1)$ column $h$ with
cell set $H$ and any $\rho$. Choose a pigeon $p \in D(\rho) \setminus
\mathrm{pigeons}(H)$; this exists because $|D| = 2d+1 \ge k$. The star row
$Q_p \cdot h$ has degree $k \le d$, hence lies in $V$ (a generator row by
construction), so for every design
$\bigoplus_j \mathrm{ans}(x_{pj} h) = \mathrm{ans}(h)$. Terms: $j \in
\mathrm{holes}(H)$ give monomials with a repeated hole (fixed 0, Lemma W4
mechanism); $j$ with $(p,j)$ killed-unmatched give 0; the remaining terms
are exactly the fresh-hole terms $j \in R \setminus \mathrm{holes}(H)$,
whose monomials $x_{pj} h$ are matching-$k$ (pigeons: $p \notin
\mathrm{pigeons}(H)$; holes: $j \notin \mathrm{holes}(H)$), hence fixed
values by assumption. So $\mathrm{ans}(h)$ is fixed across designs at this
$\rho$. For any other $\rho'$ the same argument applies with a free pigeon
outside $\mathrm{pigeons}(H)$ (exists for every $\rho'$). So $h$ is
value-determined: matching-$(k-1)$ all-determined. Contrapositive gives the
step. Orbit closure: the generator set is $S_{2d+1} \times S_{2d}$-stable,
so the determined set is a union of orbits, and matching-$k$ columns form a
single orbit (any matching relabels to any other); hence one varying
matching-$k$ column makes them all vary. Iterating the step down to
matching-1 (singles) and using the base (singles vary: cor:coin's marginal
fairness clause, kernel-verified at $(2,1)$, $(4,2)$, $(6,3)$, and exact at
the $(8,4)$ slice this run: 0/72 value-determined, 2016/2016 matching2
varying), all matching columns vary. QED.

Consequences. (1) deg3_theory.md open item 1 is CLOSED and strengthened:
the general-$d$ classification conjecture there was conditioned on
diagonal variation; Theorem A needs no such condition (its induction goes
matching-to-matching, not through diagonals). (2) The balance lemma
applies to every matching answer at every degree: the per-$\rho$ answer law
is exactly $\{0, 1/2, 1\}$, which is the exactness license for Q3/Q4/Q5.
(3) The $(8,4)$ degree-4 classification is thereby complete WITHOUT a
sweep: the three classes partition $\binom{75}{4} = 1{,}215{,}450$ columns
as 912,978 fixed-0 + 302,472 varying-valued (the varying-valued split:
211,680 matching4 + 90,792 alias-to-varying). [MV for the arithmetic; the
$(8,4)$-specific status claims rest on Theorem A + the witnessed identities.]

## 3. Q2: degree-4 star sum rules (Theorem B) and REL-4

Theorem B (degree-4 stars). [PROVED + MV] For any pigeon $p$ and
matching3 $g_3$ with $p$ outside it, the row $Q_p \cdot g_3$ (degree 4, a
generator row) gives, for every $(\rho, L)$:
  $\bigoplus_{j \in R \setminus \mathrm{holes}(g_3)}
   \mathrm{ans}(x_{pj} \cdot g_3) = \mathrm{ans}(g_3) \cdot [p \in D]$,
with the automatism: if $\rho(p) \in \mathrm{holes}(g_3)$ then
$\mathrm{ans}(g_3) = 0$ (the $g_3$ cell at that hole has a different
pigeon, which cannot also map there, so it is killed-unmatched). The
status decomposition was verified exhaustively at outer $(9,4)$ over all
90 restrictions: live-term structure 0 errors, killed-elsewhere 0 errors,
fresh-terms-killed 0 errors, automatism 0 errors. The right-hand side is
status-dependent ($[p \in D]$, the free-pigeon indicator), which is the
same information-bearing structure as the degree-3 stars; and the same
non-realizability remark as deg3 Section 4 applies verbatim: the fresh set
$R \setminus \mathrm{holes}(g_3)$ is $\rho$-hidden, so the star identity
itself cannot be probed into a certainty certificate.

REL-4 (block completion at degree $\le 4$). [PROVED structure] A
degree-$\le 4$ transcript observes a determined relation only if it
completes (a) a free row (2d coordinates, cost $\Theta(n)$, rows
$\rho$-hidden), (b) a degree-2 star ($\mathrm{ans}(x_{ab})$ + fresh
diagonals, cost $n-1$), (c) a degree-3 star ($\mathrm{ans}(g_2)$ + fresh
triples, cost $n-2$), (d) NEW a degree-4 star ($\mathrm{ans}(g_3)$ + fresh
matching4 terms, cost $n-3$), or (e) an alias pair ($x^4$ with $x$,
$x^3y$ with $xy$, $x^2y^2$ with $xy$, $x^2yz$ with $xyz$; per-query but
configuration-invariant, zero information). Per-star completion
probabilities carry the usual hypergeometric factors for a spread
transcript; an adversarial transcript pays $\Theta(n)$ per completed
star, giving $p_{\mathrm{blk4}}(e) \le e/(n - 2d - 3)$ plus the spread
bound. At budget $e = d \log k = o(n)$ both are $o(1)$, unchanged from
REL-3 except for the one new class.

## 4. Q3: Theorem C, the exact per-hit posterior post4

Theorem C. [PROVED + MV] Fix a matching4 $T$ and the event
$\mathrm{ans}(T) = 1$. Per $\rho$: the answer is 1 if all four pairs of $T$
are matched (the restricted monomial collapses to the constant), 1/2 if no
pair is killed and at least one is free (the free part is a
matching-$j$ column, $j \ge 1$, varying by Theorem A, fair by balance), 0
if any pair is killed. Bayes over the per-subclass counts
$b_m = \binom{n-3}{c-m}\binom{n-4}{c-m}(c-m)!$ gives
  $\mathrm{post}_4 = \frac{b_0 + 3b_1 + 3b_2 + b_3}
                {2b_4 + b_0 + 4b_1 + 6b_2 + 4b_3}$.
Verified digit-exact (rational equality) against exhaustive enumeration at
$(9,4)$ [90 restrictions, both triples], $(10,4)$ [4,950], $(11,4)$
[217,800], $(12,4)$ [8,494,200; the first point with the all-matched class
nonempty]. General-$k$ form (with $b_m^{(k)} =
\binom{n+1-k}{c-m}\binom{n-k}{c-m}(c-m)!$):
  $\mathrm{post}_k = \frac{\sum_{m=0}^{k-1} \binom{k-1}{m} b_m^{(k)}}
                {2 b_k^{(k)} + \sum_{m=0}^{k-1} \binom{k}{m} b_m^{(k)}}$,
which reproduces $q_{\mathrm{and\_exact}}$ at $k = 2$ and deg3's
$\mathrm{post}_3$ at $k = 3$.

Asymptotics (answer to "lift or not"). [PROVED from the closed forms]
$b_{k-1}^{(k)}/b_k^{(k)} = (2d+1)(2d)/(c-k+1)$, and the numerator
(denominator) is dominated by its $m = k-1$ ($m = k$ and the $\binom{k}{k-1}
b_{k-1}$) term once $c \gg 4d^2$, giving
  $\mathrm{post}_k = \frac{2d^2+d}{c-k+1}\left(1 + o(1)\right)$,
so ALL single-pass per-hit posteriors ($k = 1, 2, 3, 4$) share the leading
form $2d^2/n$: NO asymptotic lift, and no demotion either; every pairwise
ratio tends to 1 (measured $\mathrm{post}_4/\mathrm{post}_3 = 1.0013$ and
$\mathrm{post}_4 \cdot (c-3)/(2d^2+d) = 1.0014$ at $(16383,4)$).

Finite-$n$ structure [MEASURED, exact arithmetic]:
  - $\mathrm{post}_4 - \mathrm{post}_3$ changes sign: $-7 \times 10^{-3}$
    to $-3 \times 10^{-2}$ for $n \le 63$ ($d = 4$), $+6 \times 10^{-3}$ at
    $(127,4)$, $+5 \times 10^{-4}$ at $(1023,4)$: the proved asymptotic
    difference $(2d^2+d)/((c-2)(c-3)) > 0$ takes over only for
    $c \gtrsim 2d^2$; below that the subleading classes dominate and the
    ordering flips.
  - $\mathrm{post}_4$ exceeds the degree-2 value $q_{\mathrm{and\_exact}}$
    by up to $+8.4\%$ relative at $(255,4)$ (a finite-$n$ purity lift, the
    degree-4 mirror of deg3's post3 finding), and exceeds the single
    posterior $q$ by up to $+19\%$ relative at $(127,4)$.
  - At every cap-relevant point the max $q_4^*$ is achieved by
    $\mathrm{post}_3$ (small $n$) or $\mathrm{post}_4$ ($n \ge 127$); the
    choice is immaterial asymptotically.

## 5. Q4: certificates at degree 4

Proposition M (mass dominance). [PROVED + MV] Let $P_k(n,d) =
P[\mathrm{ans}(\text{matching-}k) = 1] = \frac{1}{2}\left(Q_k +
b_k^{(k)}/T\right)$ with $Q_k = \sum_{m \le k} \binom{k}{m} b_m^{(k)}/T$
(the no-killed probability) and $T = \binom{n+1}{c}\binom{n}{c}c!$. Then
$P_1 = h_1$ exactly, and $P_4 < P_3 < P_2 < P_1$ at every tested point
$(31,4), (63,4), (127,4), (255,4), (1023,4), (63,5), (1023,5)$ (e.g. $P_4
= 1.008 \times 10^{-8}$ vs $P_1 = 9.5 \times 10^{-3}$ at $(127,4)$). Since
every certain certificate's pattern must contain at least one answer-1
(an all-0 transcript admits a consistent configuration matching any
candidate pair, on the block-free event), the firing rate of any
certificate that consumes degree-4 evidence is at most $e \cdot P_4$,
which is $o(e \cdot P_3) = o(P_K)$: NO degree-4 mechanism can improve the
budget scaling over the known degree-1 channels ($K_j$ at $\Theta(d/n)$
per query dominates $P_4$ by factors $4.6 \times 10^3$ to $3.8 \times
10^9$ across the $d = 4$ grid).

Exhaustive search at outer $(9,4)$ [MEASURED, F1-level, exact]. Pool: all
208 monomial queries on a $4 \times 4$ window restricted to the matching
classes (16 singles + 72 matching2 + 96 matching3 + 24 matching4).
Constant-0 queries (line-pair monomials) are excluded with the proved
reason (determined answers carry zero information); alias queries are
excluded because their answers are design-coins equal to their targets'
(Theorem A-level facts, not F1-visible), so an F1-only search cannot
legally include them. Scanned: ALL 16 singleton and 720 pair symmetry
classes, and 18,236 triple classes (sampled from 23,799 raw triples of
1,478,256). Every answer pattern's F1-consistency was evaluated over all
90 restrictions; a pattern is F1-CERTAIN if some window pair is free in
every F1-consistent restriction. F1-certainty implies certainty (proved:
the fully consistent configurations are a subset of the F1-consistent
ones). Results:
  singletons: 0 certain patterns (matches theory: single queries never
              certify),
  pairs:      650 certain patterns = 175 wedge/Z-explained + 475
              shadow(c=1),
  triples:    68,295 certain patterns = 12,264 wedge/Z + 56,031
              shadow(c=1),
  UNEXPLAINED: 0.
The wedge and Z templates were applied at ALL degrees (the deg3 lemmas S3
and Z are degree-generic: two answer-1s on monomials sharing a pigeon in
distinct holes certify that pigeon free; a 0-single plus a containing
answer-1 monomial certifies that pair free). The shadow tag is the $c = 1$
consistency-pin artifact of deg3 Section 5 (at $c = 1$ the transcript pins
the unique matched pair to a small set, certifying pairs outside its row
and column shadows), provably inert once $c > 9$, hence absent at every
cap-relevant scale.

Verdict on the task's target question: degree-4 answers combined with
degree-2 collision structure produce NO new certain mechanism and NO better
budget scaling. The collision structure enters only as determined-0
queries (information-free) and through the fixed-0 status of
line-pair-containing degree-4 monomials (equally information-free); the
combining patterns that DO certify (e.g. two Z-forms sharing one
matching4) are inventory instances with rate $\le P_4$. Inventory conjecture
update (O7): the certain inventory {co-linear 1s, co-vertex 1s (wedge, any
degree), zero-single + containing 1 (Z, any degree), $K_j = 1$, counting,
shadow-pins (toy $c$ only)} is COMPLETE at degree $\le 4$ at the searched
scale; the completeness direction at general scale rests on the same
evidence as deg3 (exact completeness at $(7,3)$), now with a second exact
F1-level confirmation at $(9,4)$.

## 6. Q5: Theorem 3'' (the cap at degree <= 4) and Corollary 3.3

Theorem 3'' (budgeted cap, true channel, full adaptive degree-$\le 4$
class). [ASSEMBLY; certificate terms and the certificate-free leaf cap
PROVED; multi-evidence composition modulo the same JDP negative-association
citation standard as deg2/deg3 - two flags inherited, unchanged] Every
adaptive tree of budget $e$ using degree-$\le 4$ monomial queries and
linear forms satisfies
  $\mathrm{success}(T) \le \min(1,\; q_4^* + P_{\mathrm{adj}}(e) +
   P_K(e) + P_{\mathrm{cert4}}(e) + P_{\mathrm{blk4}}(e) + o(1))$,
  $q_4^* = \max(q,\; q_{\mathrm{and\_exact}},\; \mathrm{post}_3,\;
   \mathrm{post}_4)$,
  $P_{\mathrm{adj}} \le \min(1, e h_1)\min(1, e q(2d-1)/(2(n-1)))$
   (deg2_theory Theorem 3),
  $P_K \le 2(1 - \exp(-e d/(4n)))$,
  $P_{\mathrm{cert4}} \le e \cdot P_4(n,d)$ (Proposition M; the
   wedge/Z/cert4 family is $o(P_K)$),
  $P_{\mathrm{blk4}} \le e/(n - 2d - 3)$ + spread bound (REL-4).
What is genuinely new at degree 4 is only: one more completion class
($n-3$), one more posterior entry ($\mathrm{post}_4$, same leading form),
and one more mass term ($P_4$, dominated). Nothing breaks; there is no
degree-4 mechanism that Theorem 3' missed.

Corollary 3.3 (chi-hypothesis at degree $\le 4$). [PROVED modulo the two
inherited JDP steps] For every $(n, d, k)$ with $d \ge 4$ and budget $e =
d \log k$:
  $\mathrm{success}(T) \le 1/2 + o(1) + 2(1 - \exp(-d^2 \log k/(4n)))$,
so the error is $\ge 1/2 - o(1) - \Theta(d^2 \log k / n) \ge k^{-O(1)}$
whenever $d^2 \log k = o(n)$. The boundary is DEGREE-INDEPENDENT through
degree 4. Measured cap terms (V6): at $(4095,4)$, $e = 64$: cap 0.056
(ALIVE); at $(1023,4)$, $e = 64$: cap 0.221; the $K_j$ term is the first
to bite, exactly as at degrees 2 and 3.

Forward note for the all-degrees quantifier (O2). [CONJECTURED] The reason
the boundary has not moved through four degrees is structural: degree $k$
adds (i) one star class costing $n - k + 1$ queries to complete (so an
adversarial transcript pays $\Theta(n)$ per class, $\Theta(dn)$ over all
classes, and $e = d \log k$ covers $o(n/\log k)$ classes... precisely:
$P_{\mathrm{blk}} \le \sum_{k \le d} e/(n-k) = \Theta(ed/n) = d^2 \log k/n$)
and (ii) an evidence class whose answer-1 mass $P_k$ strictly decreases in
$k$. If both monotonicities persist (mass: proved for all $k$ at the
closed-form level; classes: one star family per degree, witnessed), the
cap of Theorem 3'' extends verbatim to all degrees with the SAME
condition $d^2 \log k = o(n)$, and O2's open core is the assembled proof
of that per-degree induction (the degree-$d$ analogue of Proposition M is
closed-form; the degree-$d$ analogue of REL is the only structural piece
needing care, since higher-degree relation classes could in principle
appear with sub-$\Theta(n)$ completion costs - none do through degree 4).

## 7. What remains open

1. The base of Theorem A at general $d$: singles vary is cor:coin +
   kernel measurements through $d = 3$ and the exact $(8,4)$ slice here; a
   self-contained elementary proof (my graded-row attempt failed on the
   Boolean rows) would make Theorem A fully unconditional. [GAP, small]
2. The exact finite-$n$ constants of the post4-post3 sign change
   (crossover location as a function of $d$): measured between $n = 63$
   and $127$ at $d = 4$, 63 and 127 at $d = 5$; not pinned analytically.
   [open, easy]
3. Completeness of the certain inventory at degree $\le 4$ on the TRUE
   channel (patterns certified only through design-law coincidences,
   beyond F1-determined structure): the (7,3) exact search (deg3) and the
   (9,4) F1 search here both found none beyond the inventory, but an
   exact-channel search at $d = 4$ is infeasible (no exact design
   sampler at $(8,4)$). [CONJECTURED complete]
4. The multi-evidence composition (JDP) steps in Theorem 3''; inherited
   from deg2/deg3, unchanged. [GAP, flagged]
5. The all-degrees extension (O2): the induction sketch in Section 6's
   forward note (mass monotonicity + one star class per degree + no
   sub-$\Theta(n)$ completion classes) is the template the degree-5 agent
   should attack first; its failure mode to rule out is a NEW relation
   class with cheap completion. [open]

## 8. Registered run

  cd /home/tomzx/pnp/experiments && python3 chi_deg4_check.py      (14 s,
  25 PASS / 0 FAIL)
  python3 chi_deg4_check.py --smoke                                (reduced
  samples)

Output (abridged; full text in the run log):
  [V0] (4,2) anchor rank 165 / dim 231 / Des 65 PASS; (8,4) deg<=2 slice
       1269 rows, 2701 columns; singles value-determined 0/72, Q_i-row
       single-projection rank 9 PASS; e_0 determined PASS; squares alias
       mismatches 0/72 PASS; same-line fixed 0: 540/540 PASS; diagonals
       2016, value-fixed 0 PASS
  [V1] witness sums x^2+x, x^4+x^2, x^4+x, x^3y+xy, x^2y^2+xy, x^2yz+xyz,
       x^3+x, x^2y+xy: all == target, all rows legal generator shifts
       PASS; Q_0.g3 / Q_4.g3 structural form + membership PASS
  [V2] (9,4) star decomposition over 90 restrictions: 0 errors PASS
  [V3] post4 digit-exact at (9,4) [both triples], (10,4), (11,4), (12,4)
       [8,494,200 restrictions] PASS; grid and leading form as in
       Section 4
  [V4] P1 = h1 exact and P4 < P3 < P2 < P1 at all 7 grid points PASS;
       P4/K_j dominance 2e-4 to 2e-10
  [V5] 736 full classes + 18,236 sampled triple classes: 68,945
       F1-certain patterns, tags wedge/Z + shadow(c=1) only,
       UNEXPLAINED 0 PASS
  [V6] cap terms and aliveness verdicts as in Section 6

Instrument notes (corrections made during the run, per corpus discipline):
(1) the alias witness for $x^4 + x^2$ was first written as
$x^2 \cdot (x^2+x)$, which is $x^4 + x^3$ (algebra slip caught by the
script's own sum check before any result was trusted); corrected to the
2-row chain $(x^2+x)x^2 + (x^2+x)x$. (2) an earlier canonical-form helper
sorted inside each (pigeon, hole) pair, corrupting the bipartite roles;
caught by a pool-membership assertion on canonical representatives
(deg3's helper sorts cells, not pairs, and is unaffected). (3) the
"analytic" proof that singles never determined was retracted before
delivery (Section 1 instrument note).
