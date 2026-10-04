# The odd-$p$ theory of the $\Omega(n,d)$ answer channel: the sum-locked
# row / free column asymmetry, the value-based certificate inventory, the
# exact odd-$p$ posteriors, the $K_j$-tree error law, and the budgeted cap
# (Open Problem O6, degree $\le 2$)

Result of the odd-p-theory agent (2026-10-04). Status: analysis, not
peer-reviewed. Task: recompute the $p = 2$ degree-$2/3$ theory
(deg2_theory.md, ADDENDUM 3; deg3_theory.md, ADDENDUM 5) at odd
characteristic, on five questions: (1) the odd-$p$ channel law, (2) the
certificate inventory recompute, (3) the exact per-hit posteriors, (4) the
budgeted cap analogue with its boundary condition, (5) the verdict on O6.

Channel: the TRUE $\Omega(n,d)$ pipeline at characteristic $p$ (uniform
restrictions $\rho$ leaving $2d$ free holes, uniform degree-$d$ designs $L$
of the restricted canonical system over $\mathbb{F}_p$; answer
$\omega(g) = L(g^\rho)$). Script: chi_odd_p_check.py (registered run, 78 s,
ALL CHECKS PASS, self-contained GF($p$) sparse linear algebra; p = 2
regressions reproduce the corpus numbers digit-exact). Markers:
[PROVED], [MEASURED], [MV] machine-verified, [CONJECTURED], [GAP].

Scale facts that drive everything: all kernel work lives at the restricted
systems (2,1) and (4,2) (degrees $\le 2$); the (6,3) degree-3 build over
$\mathbb{F}_p$ is out of reach for tuple-based GF($p$) elimination (the
$p = 2$ bitmask toolkit does not transfer), so the degree-3 odd-$p$
statements are template transfers, flagged. Outer pipeline work: (7,2)
exhaustive (11,760 restrictions, exact projected-design cosets), (8,2) and
(9,2) status-level exact (211,680 and 3,810,240 restrictions), (15,2)
Monte Carlo on the proved closed forms (60,000 sampled restrictions; full
enumeration is $2.4 \times 10^{14}$ restrictions, infeasible and
unnecessary once the closed forms are digit-exact at the smaller points).

## 0. Summary (the five answers in one paragraph each)

Q1 (channel law). [PROVED + MV] The structural driver is
characteristic-uniform: the row axiom $Q_i = 1 - \sum_j x_{ij}$ is an
EQUALITY over $\mathbb{F}_p$, so $L(Q_i^\rho) = 0$ on EVERY pigeon at every
$p$, i.e. each free row's design values are locked to $\sum = 1$ exactly
(the odd-$p$ form of the $p = 2$ XOR $= 1$ lock), while injectivity remains
an INEQUALITY (collision monomials), so columns carry no linear lock. The
single-variable design law is therefore: each free row uniform on the
sum-$1$ hyperplane $\{a \in \mathbb{F}_p^{2d} : \sum a_j = 1\}$
($p^{2d-1}$ points), rows independent; any row-incomplete query window is
jointly uniform over $\mathbb{F}_p^{|T|}$ (independent die rolls); killed
rows show exactly one $1$; killed columns exactly one $1$; free columns are
iid uniform entries. Row-sum queries are dead at every $p$; column queries
are alive at every $p$. The T_p analysis flag in p_family.md section 4 is
confirmed structurally, and that section's Proposed Theorem $T_p$ is
REFUTED as stated (Section 7).

Q2 (certificates). [PROVED, rates MEASURED] The odd-$p$ inventory is the
$p = 2$ inventory with every count of ONES replaced by a count of NONZEROS
and with one new entry: SELF-CERTIFICATION (a single answer in
$\mathbb{F}_p \setminus \{0, 1\}$ certifies its pair free outright, 1
query, per-query rate $f(p-2)/p$), which does not exist at $p = 2$ because
there the determined set $\{0, 1\}$ covers the alphabet. Adjacency (two
nonzeros co-row or co-column), the Z-certificate ($\{\mathrm{ans}(x_p)
\ne 1, \mathrm{ans}(m) \ne 0\}$ with $p \in m$), the wedge (two nonzeros
through a common pigeon in distinct holes), and the $K_j$ column channel
($\mathrm{ans}(K_j) \ne 0$ certifies $j \in R$; killed columns answer $0$
determinedly) all survive with the same one-line proofs. The full-scan
counting certificate succeeds with probability EXACTLY 1 at every $p$
(pigeonhole on nonzeros: $\ge n+1$ rows each carrying a nonzero, $n$
columns, killed columns carry exactly one). All new certificates are
rate-dominated by the $K_j$ channel's $\Theta(d/n)$, exactly as wedge and
Z are at $p = 2$.

Q3 (posteriors). [PROVED, digit-exact] Every $p = 2$ closed form transfers
by the single substitution "free-branch hit mass $1/2 \to 1/p$":
$q_p = (2d{+}1)2d/((2d{+}1)2d + p(n-2d))$ (at $p = 2$ this IS the corpus's
$q$), $\mathrm{post0}_p = (2d{+}1)2d/((2d{+}1)2d + p(n^2 - 4d^2))$,
$q_p^{\ne 0} = (p{-}1)f/((p{-}1)f + pm)$, the column posterior
$\mathrm{colq}_p = 2d/(2d + p(n{-}2d))$ for $K_j = 0$, and the degree-2
$q_{\mathrm{and},p} = (M_1 + M_2)/(pM_0 + 2M_1 + M_2)$. The row-scan
Theorem 2 analogue: $\mathrm{post}_p(k) = A\,\mathrm{FB}_p(k)/(A\,\mathrm{FB}_p(k) + m)$
with weight $w_p(t) = p^{-\min(t+1,\,2d-1)}$, still maximized at $k = 0$
(zeros only suppress). All digit-exact against restriction enumeration at
(7,2), (8,2), (9,2) and design-level at (7,2).

Q4 (cap). [ASSEMBLY, two modulo-JDP flags inherited] Theorem 3'' extends
the budgeted cap to the odd-$p$ adaptive degree-$\le 2$ class:
$\mathrm{success}(T) \le \min(1, q_p^* + P_{\mathrm{sc}} + P_{\mathrm{adj}}
+ P_K + P_Z + P_{\mathrm{blk}} + o(1))$ with $q_p^* = \max(q_p,
\mathrm{post0}_p, q_{\mathrm{and},p})$ and the new self-certification term
$P_{\mathrm{sc}} \le e f (p-2)/p = \Theta(d^3 \log k / n^2) = o(1)$
whenever $d^2 \log k = o(n)$ and $d = o(n)$. The $K_j$-tree witness
(Theorem 4''/4b'') errs $C(2d, p{-}1)\,p^{1-2pd}$ at $O(dn)$ budget and
$k^{-\Theta(d^2/n)}$ at budget $e = d \log k$. The budgeted boundary is
$\mathrm{err}^*(d, d\log k) = k^{-\Theta(d^2/n)}$ at EVERY $p$: the same
$d^2 \sim n$ transition as degree 2 and 3 at $p = 2$, with better
constants as $p$ grows ($P_K$ carries $(p-1)/p$).

Q5 (O6 verdict). ALIVE in the printed regime. The chi-hypothesis (err-form)
holds at odd $p$ for the entire adaptive degree-$\le 2$ class on the true
pipeline whenever $d^2 \log k = o(n)$, modulo the same two JDP composition
steps as the $p = 2$ cap; the all-degrees quantifier remains the open core,
shared with O2. Nothing at odd $p$ opens a budgeted route past the
$p = 2$ boundary; the characteristic asymmetry (row equality vs column
inequality) is why the surviving channel is the column one at every $p$.

## 1. Setup and the equality/inequality asymmetry [PROVED]

Pipeline at characteristic $p$ (arXiv:2609.35927, stated for a fixed
arbitrary prime): $\rho$ a uniform partial injection leaving free set $D$
($2d+1$ pigeons) and $R$ ($2d$ holes); $L$ a uniform degree-$d$ design of
the restricted system ($L(1) = 1$, $L$ kills $V(n,d)^\rho = V(2d,d)$,
kernel finding F1 of kernel_structure.md, whose proof is coefficient-free
and holds at every $p$); the answer to $g$ is $L(g^\rho)$. Restricted
canonical system over $\mathbb{F}_p$: collision monomials, two-hole
monomials, $Q_i = 1 - \sum_j x_{ij}$, Boolean $x^2 - x$ (coefficients read
in $\mathbb{F}_p$).

The asymmetry. The pigeon axiom $Q_i$ is a system polynomial, so
$Q_i \in V$ and $L(Q_i^\rho) = 0$ for every design: for a free pigeon this
reads $1 - \sum_{j \in R} L(x_{ij}) = 0$, an EXACT equality constraint on
each free row's answers, at every $p$. Injectivity is expressed by the
collision monomials $x_{i_1 j} x_{i_2 j} = 0$: quadratic vanishing
conditions, which constrain designs only through products and impose NO
linear condition on any column. Consequently: row sums are locked to $1$
at every $p$ ($p = 2$: XOR $= 1$; odd $p$: $\sum = 1$ in
$\mathbb{F}_p$), column sums are free at every $p$, and the
$K_j = 1 - \sum_i x_{ij}$ column form is not a generator at any $p$.
Row-sum queries are dead at every $p$; column queries are the surviving
linear channel at every $p$. This confirms the task's structural fact
[PROVED; one line each, plus MV at (4,2) for $p \in \{2,3,5\}$: the
single-table projected-kernel dimension check of Section 2, which
certifies both the row rows and the absence of any column-type
single-variable relation].

New dimension data [MV]. The (4,2) build gives rank $V = 165$, dim Des
$= 65$ at $p = 2$, 3, AND 5 (identical to the corpus's $p = 2$ tables);
(2,1): rank 3, dim Des 3 at all three primes. The design-space dimension
is characteristic-independent at both tested points [MEASURED at
(2,1),(4,2); no general claim]. Also at single-variable level: the
projected kernel on all $2d(2d{+}1)$ singles has dimension exactly
$(2d{+}1)(2d-1)$ at all three primes, i.e. the ONLY single-variable
relations are the $2d+1$ row rows (this is precisely the
non-membership of any column form such as $K_j$, at single-variable
level).

## 2. Theorem ChP: the channel law at odd $p$ (Q1) [PROVED + MV]

Theorem ChP (single-variable law). Under uniform $(\rho, L)$ at odd $p$:
(i) killed-matched pair: answer exactly $1$; killed-unmatched: exactly
$0$ (restriction semantics, every $p$). (ii) The joint law of the full
free-region single table $M$ (given $\rho$) is the product over the
$2d+1$ free rows of the uniform measure on the sum-$1$ hyperplane
$\{a \in \mathbb{F}_p^{2d} : \sum_j a_j = 1\}$: $p^{(2d+1)(2d-1)}$
tables, each equally likely. (iii) Any row-incomplete window $T$ (at
least one unqueried cell per free row) has its answers jointly uniform
over $\mathbb{F}_p^{|T|}$: independent die rolls. (iv) Killed rows of
$M$: exactly one $1$; killed columns: exactly one $1$; free columns: iid
uniform over $\mathbb{F}_p$ on the $2d+1$ free-pigeon entries. (v)
$Q_i$ answers $0$ on every pigeon; $K_j$ answers $0$ determinedly on
killed columns and is uniform on $\mathbb{F}_p$ on free columns (so
$P(K_j \ne 0) = (p-1)/p$ there).

Proof. (ii): the constraint space $W = \mathrm{span}(V\text{-rows} + e_0)$
meets the single-coordinate subspace exactly in the span of the $2d+1$
restricted $Q_i$ rows and $e_0$. Odd-$p$ proof: rows with a monomial
unique to them (collisions, two-holes, Boolean squares) have coefficient
$0$ in any such relation; a diagonal degree-2 monomial $x_{ij} x_{ab}$
($i \ne a$, $j \ne b$) lies in exactly two $V$ rows, $Q_i \cdot x_{ab}$
and $Q_a \cdot x_{ij}$, each with coefficient $-1$, so cancelling it
forces their coefficients equal ($= t$) and the total is $-2t \ne 0$ at
odd $p$ unless $t = 0$: the $2$-torsion obstruction (at $p = 2$ this
step fails and the corpus's separate argument applies:
kernel_structure.md Finding 2). Remaining: combinations of the pure
$Q_i$ rows and $e_0$, supported inside $T$ only when whole rows are
contained. So the projected kernel has
dimension $(2d+1)(2d) - (2d+1)$ and the answer coset is exactly the
product of the hyperplanes (each row: $L(\mathrm{row}_i) = L(1) = 1$).
Uniformity of the coset is the kernel-projection structure (deg3
machinery over $\mathbb{F}_p$). (iii): a relation supported inside $T$
must combine $Q_i$ rows with $\mathrm{row}_i \subseteq T$;
row-incompleteness kills every $\alpha_i$, then $e_0$'s coefficient
forces the combination to $0$. (iv): from (ii), coordinate-wise. (v):
$Q_i \in V$; killed columns are $\rho$-determined; free columns are iid
by (ii). QED.

Consequences verified at (4,2) [MV, all $p \in \{2,3,5\}$]: single-table
kernel dim 15 ($= 20 - 5$) with all sampled designs row-locked
(3000/3000 at each $p$); the full free row's coset is EXACTLY the $p^3$
sum-$1$ patterns ($8$, $27$, $125$ points, each once); a 13-cell
row-incomplete window has projected kernel dim 13 (joint uniformity);
the star sum rule over $\mathbb{F}_p$ (below); the alias law
$\mathrm{ans}(x^2) = \mathrm{ans}(x)$ (Boolean row); and at $p = 3$ the
nonzero-count law of Lemma CNT.

Star sum rules (the degree-$\le d-1$ locks). For any monomial $g$ with
$\deg g \le d - 1$ and any pigeon $p$: $Q_p \cdot g \in V$, hence
$\sum_{j \in R} \mathrm{ans}(x_{pj} g) = \mathrm{ans}(g)$, the
$j \in \{g\text{'s holes}\}$ terms dying through collision/two-hole rows
(degrees $\le d$). Verified at (4,2), $g = x_{21}$, probe pigeon 0:
the combination row $Q_0 \cdot g + x_{01} g$ is in $V$ exactly, the
window coset has dim 3 ($p^3$ points: $8/27/125$), and the sum rule
holds with 0 violations at all three primes. This is the odd-$p$
degree-2 star lock; the right-hand side is configuration-dependent
($\mathrm{ans}(g)$), so stars carry information only through status
decomposition, exactly as at $p = 2$. A completed star pins the fresh
answers to the $\mathbb{F}_p$-hyperplane $\sum = \mathrm{ans}(g)$.

Lemma CNT (nonzero-count law). On a fully scanned free row,
$P(c \text{ nonzeros}) = \binom{2d}{c} \frac{(p-1)^c - (-1)^c}{p \cdot p^{2d-1}}$
for $c \ge 1$, and count $0$ is impossible (the sum is $1 \ne 0$).
Verified digit-exact at (4,2), $p = 3$: counts $\{1{:}\,4, 2{:}\,6,
3{:}\,12, 4{:}\,5\}$, summing to $27$ [MV]. Reading: at $p = 2$ this is
the odd-count law (only odd $c$ occur); at odd $p$ every $c \ge 1$
occurs, so the counting certificates must count NONZEROS, not ones.

Independence answer (Q1's last clause): on star-free, row-free,
alias-free windows the answers are independent UNIFORM DIE ROLLS
(jointly uniform over $\mathbb{F}_p^{|T|}$), the exact analogue of the
$p = 2$ completion structure with bits replaced by die values. The
channel law's short form: free pair $\to$ uniform $\mathbb{F}_p$ die
(marginally always, jointly on row-incomplete sets); killed-matched
$\to 1$; killed-unmatched $\to 0$; full free rows sum-locked; full free
columns unconstrained.

## 3. The certificate inventory at odd $p$ (Q2) [PROVED; rates MEASURED]

Lemma SC (self-certification; NEW at $p > 2$). If a single-variable
answer $a = \mathrm{ans}(x_{ij}) \notin \{0, 1\}$ then $(i,j)$ is FREE.
Proof: a matched pair answers exactly $1$ and a killed-unmatched pair
answers exactly $0$; only a free pair can answer a third value. One
query, posterior exactly 1, per-query rate $f (p-2)/p$. At $p = 2$ the
certificate is empty (the alphabet is $\{0,1\}$); at $p = 3$ it fires on
$1/3$ of free-cell queries. QED.

Theorem AdjP (adjacency, value form). Two NONZERO answers on single
variables of a common row (or common column) force both pairs FREE.
Proof: a killed row shows exactly one nonzero (the matched $1$), so two
nonzeros force the row free; on a free row a nonzero answer cannot sit
on a killed-unmatched cell (answer $0$) and no cell of a free pigeon is
matched. Column case symmetric (killed columns show exactly one
nonzero). At $p = 2$ this is deg2_theory Theorem 1 with $1$s; the
zero-violation check at (7,2) over all 11,760 restrictions $\times$
exact cosets: 0 violations at $p = 2, 3$ [MV]. QED.

Lemma ZP (Z-certificate, value form). If $\mathrm{ans}(x_p) \ne 1$ and
$\mathrm{ans}(m) = b \ne 0$ for a monomial $m$ containing the pair $p$,
then $p$ is FREE. Proof: $b \ne 0$ forces every pair of $m$ to be
matched-or-free (a killed factor contributes $0$); $\mathrm{ans}(x_p)
\ne 1$ forces $p$ non-matched (matched answers exactly $1$). At $p = 2$
the trigger set is exactly $\{x_p = 0, \mathrm{ans}(m) = 1\}$, the
corpus's Z form; the value form strictly generalizes it. Two queries.
QED.

Lemma WP (wedge, value form). Two NONZERO answers on $x_{p j_1} m$,
$x_{p j_2} m$ ($j_1 \ne j_2$ outside $m$'s holes) certify the pigeon $p$
FREE: an assigned pigeon kills every wedge term except the matched
hole's, whose value is $\mathrm{ans}(m)$, so at most one nonzero. Same
proof as deg3_theory Lemma S3, values replacing 1s. QED.

Theorem KP (the column channel). Killed column $j$: the cell table is
$(0, \ldots, 0, 1, 0, \ldots, 0)$ DETERMINEDLY (matched pair $= 1$,
killed-unmatched $= 0$), so $K_j = 1 - \sum_i x_{ij}$ answers $0$
always, and any deviation is impossible. Free column $j$: the
free-pigeon entries are iid uniform, so $K_j$ is uniform on
$\mathbb{F}_p$: $\mathrm{ans}(K_j) \ne 0$ CERTIFIES $j \in R$
(posterior 1), firing with probability $(p-1)/p$ per free-column query;
and within a certified column, ANY nonzero entry certifies its pigeon
free (a killed pigeon's entry in a free column is $0$). Measured exact
per-query certify rate at (7,2): $0.2857$ ($p=2$) and $0.38095$ ($p=3$),
matching the closed form $(2d/n)(p-1)/p$ [MV: free-column cosets are
the full $\mathbb{F}_p^{2d+1}$, $K_j$ uniform, all 11,760
restrictions]. QED.

What a column answer certifies at odd $p$ (the task's question),
compactly: killed hole: the column is DETERMINED (one $1$, value
included; $K_j = 0$; any nonzero count-of-ones-style certificate is
vacuous); free hole: the column is a $2d{+}1$-tuple of iid
$\mathbb{F}_p$ die rolls; the certificates are VALUE-based
($K_j \ne 0$; a nonzero entry in a certified column; two nonzeros
anywhere in the column), not count-of-ones-based.

Theorem 5'' (full-scan certainty, every $p$). The non-adaptive tree that
queries all $n(n+1)$ single variables and applies the nonzero counting
certificates has success EXACTLY 1: every row carries a nonzero (killed
rows exactly one; free rows $\ge 1$ by the sum lock), so $M$ carries
$\ge n+1$ nonzeros in $n$ columns, some column carries $\ge 2$, that
column is certified free (killed columns: exactly one nonzero), and each
of its nonzeros certifies its pigeon. Characteristic-uniform pigeonhole;
the unbounded-budget optimum is error 0 at EVERY $p$, generalizing
deg2_theory Theorem 5. QED.

Measured exact per-attempt rates at outer (7,2) (exhaustive over all
11,760 restrictions, exact projected-design cosets; instances fixed by
symmetry) [MEASURED]:

| certificate                          | p=2      | p=3      | queries |
|--------------------------------------|----------|----------|---------|
| Z (m = x33.x22, pair (3,3))          | 0.025510 | 0.053855 | 2       |
| wedge (deg-1 base, 2 probe terms)    | 0.014031 | 0.024943 | 2       |
| K_j != 0 (per free-column query)     | 0.285714 | 0.380952 | 1       |
| self-cert SC (closed f(p-2)/p)       | 0        | f/3      | 1       |

with ZERO soundness violations for every mechanism at both primes
(11,760 restrictions each, per-point cosets enumerated exactly). Rate
ordering: the two-stage $K_j$ channel remains $\Theta(d/n)$ per query
(certify $(2d/n)(p-1)/p$, then hit $(2d+1)(p-1)/(p(n+1))$), while SC is
$\Theta(d^2/n^2)$, Z and wedge $o(d^2/n^2)$ per query: the inventory
grows at odd $p$ but nothing new beats the $K_j$ channel, the same
situation deg3_theory recorded for wedge/Z against $K_j$ at $p = 2$.

The sum-rule certificate remains NOT realizable at odd $p$: the
fresh-hole set is $\rho$-hidden and a full probe makes the star
invariant $\bigoplus_{\mathrm{probe}} = \mathrm{ans}(g)$ an identity
(the $\mathbb{F}_p$ sum rule verified above), information-free;
deg3_theory's non-realizability remark transfers verbatim [PROVED,
structure only].

## 4. Theorem P1: exact per-hit posteriors at odd $p$ (Q3) [PROVED]

Write $f = (2d{+}1)2d/((n{+}1)n)$, $m = (n{-}2d)/((n{+}1)n)$,
$\kappa = 1 - f - m = (n^2 - 4d^2)/((n{+}1)n)$, $A = (2d{+}1)/(n{+}1)$.

Theorem P1 (single-variable posteriors). On the true channel at odd $p$,
for one single-variable query:
  $\mathrm{ans} = a \notin \{0,1\}$: posterior of freeness EXACTLY 1
    (Lemma SC; probability $f/p$ per value),
  $\mathrm{ans} = 1$: $q_p = \dfrac{f/p}{f/p + m}
    = \dfrac{(2d{+}1)2d}{(2d{+}1)2d + p(n-2d)}$,
  $\mathrm{ans} = 0$: $\mathrm{post0}_p = \dfrac{f/p}{f/p + \kappa}
    = \dfrac{(2d{+}1)2d}{(2d{+}1)2d + p(n^2 - 4d^2)}$,
  $\mathrm{ans} \ne 0$ (value hidden): $q_p^{\ne 0}
    = \dfrac{(p-1)f}{(p-1)f + pm}$.
At $p = 2$ these reduce to the corpus's $q$ (deg2_theory Theorem 2(i))
with $\mathrm{post0} < q$; at every $p$, $\mathrm{post0}_p < q_p$ since
$\kappa \gg m$. The per-hit probability mass moves from $1/2$ to $1/p$
and $q_p < q^{(2)}$ (the same $(n,d)$ at $p = 2$): a specific-value hit
is WEAKER evidence at odd $p$,
while the hidden-value nonzero hit $q_p^{\ne 0}$ is STRONGER
(at (7,2), $p = 3$: $q_3^{\ne 0} = 40/49 = 0.8163 > q_2 = 10/13 =
0.7692 > q_3 = 20/29 = 0.6897$, all at $(n,d) = (7,2)$: a specific-value
hit is weaker at $p = 3$ than at $p = 2$, a nonzero hit stronger).
Digit-exact vs restriction enumeration at $p = 3$, at (7,2)
(11,760), (8,2) (211,680), (9,2) (3,810,240) [MV].

Theorem P1c (one column query). For one $K_j$ query:
$P(j \in R \mid \mathrm{ans}(K_j) = 0) = \dfrac{2d}{2d + p(n-2d)}$
(closed form; digit-exact at (7,2)/(8,2)/(9,2): $4/13$, $1/4$, $4/19$ at
$p = 3$), and $\mathrm{ans}(K_j) \ne 0$ certifies $j \in R$ outright.
Given a certified column, the scan hit posterior is 1 (Theorem KP). A
full single-column scan showing exactly one nonzero at $(i_0, j)$ with
value $a$: posterior of $(i_0, j)$ free is
$\dfrac{(2d/n) p^{-(2d+1)}}{(2d/n) p^{-(2d+1)} + ((n-2d)/n)\,[a = 1]/(n{+}1)}$
(the killed branch contributes only $a = 1$), the odd-$p$ form of
deg2_theory's column-scan formula.

Theorem P2'' (row scan; Theorem 2's odd-$p$ form). For the row scan with
first $k$ answers $0$ and the $(k{+}1)$-th equal to $1$ (output = that
hit): $\mathrm{post}_p(k) = \dfrac{A\,\mathrm{FB}_p(k)}{A\,\mathrm{FB}_p(k) + m}$,
$\mathrm{FB}_p(k) = \dfrac{1}{\binom{n}{2d}} \sum_{t=0}^{\min(k,2d-1)}
\binom{k}{t}\binom{n-k-1}{2d-1-t} p^{-\min(t+1,\,2d-1)}$,
i.e. the $p = 2$ weight $w(t) = 2^{-\min(t+1,2d-1)}$ becomes
$p^{-\min(t+1,2d-1)}$ (the number of sum-$1$ hyperplane points extending
$t+1$ observed cells is $p^{2d-t-2}$ for $t+1 \le 2d-1$ and $1$
consistently at $t+1 = 2d$). Each additional observed zero costs free
likelihood exactly as at $p = 2$, so $\mathrm{post}_p(k)$ is maximized
at $k = 0$ ($= q_p$) and decreases; the elementary proof covers
$k \le n - 2d$ exactly as in deg2_theory Theorem 2(iv), and the short
tail range keeps the same status as at $p = 2$ [PROVED for
$k \le n-2d$; tail MEASURED at $k = 1, 2$ here, tail proof inherited
open item]. Digit-exact at (7,2), $p = 3$, $k = 0, 1, 2$: $20/29$,
$40/67$, $76/157$ [MV]. At (15,2), $p = 3$, $k = 1$: closed form
$0.34188$, 60,000-sample Monte Carlo $0.34405$ (consistent; the full
$2.4 \times 10^{14}$-restriction enumeration is infeasible and the
closed form is proved) [MEASURED].

The substitution rule (why every $p = 2$ form transfers). Per
restriction, an answer event's probability is a sum of matched-branch
masses (probability $1$ each) and free-branch masses (probability
$1/p$ per specific value, $(p-1)/p$ per nonzero); the $p = 2$
derivations never use anything else about the channel, by the balance
theorem (every undetermined coordinate is uniform, the one-line
kernel-coset argument, characteristic-uniform). Hence every closed form
is obtained from its $p = 2$ form by $1/2 \to 1/p$ in the free factors.
Example (degree-2): $q_{\mathrm{and},p} = (M_1 + M_2)/(pM_0 + 2M_1 + M_2)$
with $M_i$ the exact labeled hypergeometric counts of deg3_theory
Section 3; digit-exact at (7,2)/(8,2)/(9,2) at $p = 3$ [MV]; at $p = 2$
this reproduces the corpus's $q_{\mathrm{and\_exact}} = 100/359 =
0.278552$ at (32,2), against the printed independent-masses form's
$0.276346$ (gap $0.0022$, consistent with the deg3 finding that the
printed form is fine in this regime) [MV, regression].

## 5. Theorem 4'': the $K_j$-tree error law at odd $p$ [PROVED + MV]

The $K_j$-tree (deg2_theory Theorem 4), at characteristic $p$: (1) query
$K_j$ for all $j$; (2) $E = \{j : \mathrm{ans}(K_j) \ne 0\}$, each
certified $j \in R$ (Theorem KP); (3) scan the columns of $E$ (singles)
until a nonzero; output that pair; (4) fall back to a fixed pair.

Theorem 4''. At characteristic $p$, the $K_j$-tree's error is EXACTLY
  $\mathrm{err}_K(p) = \dfrac{1}{p^{(2d+1)(2d-1)}} \displaystyle\sum_{s} \binom{2d}{s}\, p^{2d(s-1)}$
where the sum runs over $1 \le s \le 2d$ with $s \equiv 2d+1 \pmod p$.
The dominant term is $s^* = 2d+1-p$ (for $p \le 2d$):
$\binom{2d}{p-1} p^{1-2pd}$; so $\log_p(1/\mathrm{err}_K) =
2pd - O_p(\log d)$: the error decays as $p^{-\Theta(pd)}$, much faster
in $d$ than the $p = 2$ law $2d\,2^{1-4d}$, and the congruence condition
prunes all infeasible subset sizes. At $p = 2$ the condition is "$s$
odd" and the formula is exactly deg2_theory Theorem 4. Moreover the
feasible set is EMPTY whenever $p \ge 2d+1$ (the class of $2d+1$ modulo
$p$ is then $\{2d+1\}$ itself or larger, outside $[1, 2d]$), giving the
exact zero regions $\mathrm{err}_K(p) = 0$ for $p \ge 2d+1$ [PROVED
from the closed form; MV at $(3,1), (5,1), (5,2)$].

Proof. The tree's success is a function of the single table alone (the
answers to $K_j$ and to singles are single-table functionals; killed
columns answer $0$ and never certify). Failure: no certified column
shows a nonzero entry. Column $j$ (free) is certified iff its sum
$S_j \ne 1$ (since $K_j = 1 - S_j$); a certified column with a nonzero
entry yields success; hence in a failure table every column is either
all-zero (then $S_j = 0$) or has $S_j = 1$. Conversely any such table
fails. So failure tables are exactly: choose $S$, the set of columns
with $S_j = 1$ (all other columns all-zero), rows locked to sum $1$
within $S$: the count is the number of $(2d{+}1) \times s$ matrices over
$\mathbb{F}_p$ with all row sums $1$ and column sums $1$, which is
$p^{(2d+1-1)(s-1)} = p^{2d(s-1)}$ (the difference of two solutions has
zero row and column sums, a $(r-1)(c-1)$-dimensional space; solutions
exist iff the totals agree: $s \equiv 2d+1 \pmod p$). Sum over
$\binom{2d}{s}$ choices of $S$, divide by the total $p^{(2d+1)(2d-1)}$.
QED.

Verified by exact DP over the single-table law (state = column sums +
nonzero flags; every table counted exactly) [MV]:

| p | d | DP failure count / total          | closed form | err          |
|---|---|-----------------------------------|-------------|--------------|
| 2 | 1 | 2 / 8                             | 2           | 0.25         |
| 3 | 1 | 0 / 27                            | 0           | 0 (exact)    |
| 5 | 1 | 0 / 125                           | 0           | 0 (exact)    |
| 2 | 2 | 1028 / 2^15                       | 1028        | 0.031372     |
| 3 | 2 | 486 / 3^15                        | 486         | 3.387e-05    |
| 5 | 2 | 0 / 5^15                          | 0           | 0 (exact)    |
| 2 | 3 | 100745222 / 2^35                  | 100745222   | 0.0029321    |

The $p = 2$, $d = 2$ row is the corpus's digit-exact regression
(deg2_theory Theorem 4: 1028/2^15) [MV]. Two odd-$p$ effects are visible
already at $d = 2$: the $p = 3$ error is about $927\times$ smaller than
the $p = 2$ error, and at $p = 5$ the congruence class of $2d+1 = 5$
contains NO feasible $s \le 4$, so the $K_j$-tree NEVER fails, matching
the zero-region clause above.

Budgeted form (Theorem 4b''). A budget-$e$ split ($\alpha e$ on $K_j$
queries, the rest scanning certified columns) succeeds with probability
at least $(1 - \exp(-\alpha e c_1))(1 - \exp(-(1-\alpha) e c_2))$ with
$c_1 = \frac{2d}{n}\frac{p-1}{p}$ and $c_2 = \frac{2d+1}{n+1}\frac{p-1}{p}$,
hence $\ge (1 - \exp(-e d (p-1)/(2pn)))^2$ at $\alpha = 1/2$: error
$\le 2 k^{-\Theta(d^2/n)}$ once $d^2 \log k \gg n$. Same form as
$p = 2$'s Theorem 4b with the improved constant $(p-1)/p$ [PROVED;
standard two-stage independence given the pipeline, the same
citation-grade step as deg2_theory Theorem 4b].

## 6. Lemma REL-p and Theorem 3'': the budgeted cap at odd $p$

Lemma REL-p (block completion, degree $\le 2$, odd $p$). A degree-$\le 2$
transcript sees a determined relation only if it completes (a) a free
row ($2d$ cells, cost $\Theta(n)$, the free columns being
$\rho$-hidden), (b) a star ($\mathrm{ans}(x_{ab})$ plus all fresh
$x_{pj} x_{ab}$, cost $n - 1$), or (c) an alias coincidence
($\mathrm{ans}(x^2) = \mathrm{ans}(x)$: per-query, but
configuration-invariant, zero information). The relation list is exactly
$p = 2$'s (Lemma REL), because the underlying identities are coefficient
patterns of the same rows; completion probabilities carry the same
hypergeometric factors, and an adversarial transcript pays
$\Theta(n)$ per completed relation, giving
$P_{\mathrm{blk}}(e) \le e/(n - 2d - 2)$ at budget $e$ [PROVED
structure; MV dims at (4,2); the degree-3 odd-$p$ relations (star-at-
degree-3, alias classes $x^2y = xy$, cubes) are NOT recomputed: the
(6,3) GF($p$) build is out of reach for the tuple machinery; template
transfer CONJECTURED with $1/2 \to 1/p$, flagged].

Theorem 3'' (budgeted cap, true channel at characteristic $p$, full
adaptive degree-$\le 2$ class). Every adaptive tree of budget $e$ using
single-variable queries, degree-2 monomial queries, and linear forms
over $\mathbb{F}_p$ satisfies
  $\mathrm{success}(T) \le \min(1,\, q_p^* + P_{\mathrm{sc}}(e)
   + P_{\mathrm{adj}}(e) + P_K(e) + P_Z(e) + P_{\mathrm{blk}}(e) + o(1))$,
with $q_p^* = \max(q_p, \mathrm{post0}_p, q_{\mathrm{and},p})$,
  $P_{\mathrm{sc}} \le \min(1, e f (p-2)/p)$  (Lemma SC, union bound),
  $P_{\mathrm{adj}} \le \min(1, e h_1^{(p)}) \cdot \min(1, e\,
     q_p^{\ne 0} (2d{-}1)(p{-}1)/(p(n{-}1)))$, $h_1^{(p)} = (p{-}1)f/p + m$,
  $P_K \le \min(1, 2 e^2 d^2 (p{-}1)^2/(p^2 n^2))$  (Theorem KP two-stage),
  $P_Z, P_{\mathrm{wedge}} = o(P_K)$  (measured rates, Section 3),
  $P_{\mathrm{blk}} \le e/(n - 2d - 2)$  (Lemma REL-p).
Assembly status: the per-evidence caps are proved (own hit: $q_p$;
own zero: $\mathrm{post0}_p$; own degree-2 monomial:
$q_{\mathrm{and},p}$; zeros never elevate, Theorem P2''), the
certificate terms are proved sound with their rates, and the
MULTI-evidence composition (deep zero-runs, distant evidence) is carried
modulo the same JDP negative-association citation standard as
deg2_theory Theorem 3 [GAP, inherited, flagged: two steps, same status
as the $p = 2$ cap].

Corollary O6-d2 (chi-aliveness at odd $p$, degree $\le 2$). For every
$(n, d, k)$ with $(2d{+}1)2d \le p(n - 2d)$ (so $q_p^* \le 1/2 + o(1)$;
at $p = 3$, $n \ge \frac{4d^2 + 8d}{3}$ suffices) and budget
$e = d \log k$:
  $\mathrm{success}(T) \le 1/2 + o(1) + \Theta(d^2 \log k / n)$,
so the error is $\ge k^{-O(1)}$ whenever $d^2 \log k = o(n)$ (and
$d = o(n)$, which the program's polylog regime satisfies with room).
The chi-hypothesis (in its err-form reading of record, chi_transfer.md
Theorem R / ADDENDUM 4: the printed Theorem 6.1(3) is dead as printed at
every $p$) HOLDS at odd $p$ for the entire adaptive degree-$\le 2$
class, with the SAME boundary $d^2 \sim n$ as at $p = 2$, degrees 2 and
3. [PROVED modulo the two JDP steps]

Measured cap/witness table (V5; cap terms at $e = d \log_2 k$, witness
$= (1 - e^{-ec_1/2})^2$) [MEASURED on the closed forms]:

| (n,d)     | p | logk | q*_p  | P_sc  | P_K    | P_blk | cap    | witness | verdict  |
|-----------|---|------|-------|-------|--------|-------|--------|---------|----------|
| (127,2)   | 3 | 16   | 0.0538| 0.0131| 0.2257 | 0.2645| 0.5705 | 0.0814  | stressed |
| (255,2)   | 3 | 16   | 0.0265| 0.0033| 0.0560 | 0.1285| 0.2159 | 0.0237  | stressed |
| (1023,2)  | 2 | 16   | 0.0097| 0     | 0.0020 | 0.0315| 0.0432 | 0.0009  | ALIVE    |
| (1023,2)  | 3 | 16   | 0.0065| 0.0002| 0.0035 | 0.0315| 0.0417 | 0.0017  | ALIVE    |
| (1023,2)  | 2 | 64   | 0.0097| 0     | 0.0313 | 0.1259| 0.1671 | 0.0138  | stressed |
| (1023,2)  | 3 | 64   | 0.0065| 0.0008| 0.0557 | 0.1259| 0.1893 | 0.0236  | stressed |

The table shows the transition the corollary predicts: the cap drops
toward $q_p^* + o(1)$ exactly when $d^2 \log k = o(n)$, at both primes,
with the odd-$p$ terms strictly smaller at equal $(n, d, \log k)$
(P_sc is the only qualitatively new term and it is
$\Theta(d^3 \log k/n^2) = o(d^2 \log k/n)$).

## 7. Correction-class flag: p_family.md's Proposed Theorem $T_p$

p_family.md section 4 (ANALYSIS) proposes Theorem $T_p$: a two-phase
tree whose phase 1 scans row-sum queries $Q_i$ until the first NONZERO
answer, with claimed per-free-pigeon nonzero probability $(p-1)/p$. This
is REFUTED at every characteristic including $p > 2$ [PROVED this
session]: $Q_i$ is a system polynomial, so $L(Q_i^\rho) = 0$ for EVERY
design and EVERY pigeon, free or assigned; the free-pigeon row sum is
LOCKED to $1$, which is why $Q_i^\rho = 0$ identically. The same
refutation was already recorded at $p = 2$ (kernel_structure.md
Findings 2-3, deg2_theory F3: the two-phase parity certificate is a
coin-channel-only object); the present check shows the coin-channel
error does not disappear at odd $p$ (it is channel-level, not
characteristic-level). What SURVIVES of $T_p$'s program is the column
dual: the $K_j$-tree (Theorem 4''), which is the strongest known tree
at every $p$. Section 4's channel-law derivation itself (free
variables answer uniformly in $\mathbb{F}_p$; killed-matched 1;
killed-unmatched 0) is CONFIRMED [PROVED + MV]. Flag for the
orchestrator: p_family.md section 4's $T_p$ paragraph needs a
correction block; this document supplies the replacement (Theorem 4'').

## 8. Verdict on O6

O6 (the $p > 2$ analogue, p_family.md section 5) is ALIVE in the printed
regime, with the same $d^2 \log k = o(n)$ boundary, at degree $\le 2$:

1. The reduction chain and the design foundation are
   characteristic-uniform (the paper's own text; Razborov's degree
   theorem over every field), so an odd-$p$ err-floor yields odd-$p$
   $F_l(\mathrm{MOD}_p)$ bounds exactly as at $p = 2$.
2. CAP (Theorem 3''): no budgeted degree-$\le 2$ tree at odd $p$ gets
   error below $1/2 - o(1) - \Theta(d^2 \log k/n)$; the new
   self-certification channel and the enlarged certificate inventory are
   all absorbed with $o(1)$ rates in the program's regime. [PROVED
   modulo the two inherited JDP steps]
3. WITNESS (Theorem 4''/4b''): the $K_j$-tree errs
   $\binom{2d}{p-1} p^{1-2pd}$ at $O(dn)$ budget and
   $k^{-\Theta(d^2/n)}$ at budget $d \log k$; the boundary has the same
   location and better constants at larger $p$. [PROVED + MV]
4. So $\mathrm{err}^*(d, d\log k) = k^{-\Theta(d^2/n)}$ at every prime
   $p$, and the odd-$p$ chi-hypothesis (err-form) holds exactly when
   $d^2 \log k = o(n)$: O6's answer mirrors O1's degree-$\le 2$ state
   (ADDENDUM 3) characteristic-for-characteristic. The genuinely open
   core is unchanged and shared: the all-degrees quantifier (O2(i) at
   $p = 2$, its O6 analogue here).

Characteristic-specific observations worth keeping: (a) the row-lock is
an equality at every $p$, so the row/column asymmetry (row queries dead,
column queries alive) is NOT a characteristic effect; (b) odd $p$ adds
the self-certification channel (answers off $\{0,1\}$), the only
one-query certificate of a PAIR outright, but $\Theta(n/d)$-dominated by
the two-stage $K_j$ channel asymptotically; (c) the
$K_j$-tree error acquires the congruence pruning
$s \equiv 2d+1 \pmod p$ and equals ZERO for $p \ge 2d+1$; (d) counting
certificates switch from ones to nonzeros, with the free-row nonzero
count law of Lemma CNT; (e) the design-space DIMENSION measured so far
is characteristic-independent (165/65 at (4,2) for $p = 2, 3, 5$) [MV;
open whether this persists at degree 3 and beyond].

## 9. What remains open

1. The degree-3 odd-$p$ recompute: the (6,3) kernel classification over
   $\mathbb{F}_3$ (ten classes, star-at-degree-3, alias classes, cube)
   is out of reach for the tuple-based GF($p$) machinery at this scale;
   the deg3 template (star sum rules, wedge/Z, posterior post3 with
   $1/2 \to 1/p$) is CONJECTURED to transfer, on the evidence that every
   degree-$\le 2$ structure did. [CONJECTURED, flagged]
2. The two modulo-JDP composition steps of Theorem 3'' (multi-evidence
   deep zero-runs, distant evidence), inherited from the $p = 2$ cap
   with unchanged status. [GAP, flagged]
3. The post_p(k) monotonicity tail $k > n - 2d$: same residual open
   item as deg2_theory Theorem 2(iv); here measured at $k \le 2$ only.
4. Whether the self-certification channel composes with $K_j$ for a
   better budgeted exponent than $\max$ of the two (the $p = 2$ open
   item 2 analogue); everything measured here says no at the program's
   regime. [open]
5. The characteristic-independence of dim Des beyond (4,2): measured at
   (2,1) and (4,2) for $p \in \{2,3,5\}$; no proof, no counterexample.
   [open, cheap to extend at degree 2]
6. The all-degrees quantifier (the shared open core of O2 and O6): the
   degree-$\ge 4$ err-floor at every characteristic. [the open core]

## 10. Registered run

  cd /home/tomzx/pnp/experiments && python3 chi_odd_p_check.py      (78 s, ALL PASS)
  python3 chi_odd_p_check.py --smoke                                (reduced samples)

Checks (full run, 2026-10-04, 78 s; rerun with the command above to
reproduce digit-for-digit; a scratch copy of the output was kept at
/tmp/opencode/chi_odd_p_run.log at run time):
  V0 builds and p = 2 regressions (rank 165 / dim 65 at (4,2), all p) PASS
  V1 channel law at (4,2), p in {2,3,5}: dims, locks, hyperplanes,
     star rule, alias, nonzero counts: ALL PASS
  V2 certificate soundness at (7,2), 11760 restrictions x exact cosets,
     p in {2,3}: 0 violations for SC/adjacency/Z/K/wedge; exact rates PASS
  V3 posteriors digit-exact at (7,2),(8,2),(9,2) status-level and (7,2)
     design-level; (15,2) Monte Carlo consistent: PASS
  V4 K_j-tree DP vs closed form at (p,d) in {(2,1),(3,1),(5,1),(2,2),
     (3,2),(5,2),(2,3)}: digit-exact, p = 2 regression 1028/2^15: PASS
  V5 cap/witness table: PASS (informative)
  V6 p = 2 regressions q(32,2) = 5/19, q_and_exact vs printed form: PASS

Instrument notes (corrections made during the run, per corpus
discipline): (1) the augmented RREF originally read the particular
solution as {pivot: rhs}, which is wrong on a triangular (non-reduced)
echelon once a pivot row carries an earlier pivot column; replaced by
exact back-substitution (particular_backsub), with build-time
self-verification that the particular solution kills every V row and
that kernel vectors are orthogonal to V rows. (2) the star-row check
originally placed the constant term on e_0 instead of on the shifted
monomial; rebuilt via shift_p and re-verified in V. (3) a variable-index
conflation (canonical variable indices used directly as monomial
columns) produced phantom relations on windows whose first free
coordinate is index 0 (which coincides with the e_0 column); all
window/spec construction now maps canonical variables through mi; the
bug's exact footprint (1/5 of restrictions at (7,2)) matched the
probability that hole 2 is the smallest free hole, which is how it was
found. (4) the printed-q_and generalization was first written with the
wrong denominator powers; corrected to the form that reduces to
deg2_theory item 6 at p = 2 (V6 now pins it).
