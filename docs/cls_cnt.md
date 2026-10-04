# Lemma CLS and Lemma CNT at general $d$: the two residual lemmas of O5

Result of the theory agent (2026-10-04). Status: analysis, not peer-reviewed.
Task: prove or further reduce Lemma CLS (general-$d$ diagonal variation plus
no-exotic-relations among degree-2 monomial answers, verified only to
restricted $(6,3)$) and Lemma CNT (tight adaptive completion counting, with
the exposure convention inherited from Lemma REL), then restate the
general-$d$ O5 status.

Markers: PROVED, REDUCED (proved modulo an explicitly named lemma), OPEN,
[MV] (machine-verified this session; harness in Section 9, script
`experiments/chi_cls_cnt_check.py`, 40 PASS / 0 FAIL, 171 s).
Everything is on the true channel (uniform designs of the restricted canonical
system; $V(n,d)^\rho = V(2d,d)$), at $p = 2$, $d \ge 2$.

## 0. Summary

1. **CLS(i) is PROVED at general $d$.** Diagonals are matching-2 columns, and
   the matching hierarchy (deg4_theory.md Theorem A) proves every matching-$k$
   column varies for $1 \le k \le d$, with base = the paper's completion lemma
   cor:coin (marginal fairness of free singles, [PROVED] at every $d$ and
   every $p$) and step = the star-row argument. Balance gives marginal
   fairness. The deg4 agent's residual GAP (a self-contained elementary base
   proof) is inherited unchanged and is the only caveat.
2. **CLS(ii)'s algebraic core is PROVED at general $d$.** The exact form of
   "no exotic relations" is the dimension identity
   $(V \oplus \langle e_0\rangle) \cap S_{\le 2} = V_{\le 2} \oplus \langle e_0\rangle$,
   where $V_{\le 2}$ is the span of the degree-$\le 2$ generator rows.
   It is proved by a degree-truncated Buchberger argument: every
   S-polynomial of generator pairs with lcm-degree $\le 2$ reduces to zero
   within degree $\le 2$ over the row set $\{Q_i,\ Q_i x_{ab},\ b_{ij},\ C,\ H\}$.
   The verification reduces to five master identities (M1-M5, I1) that are
   universal ring identities, machine-checked exhaustively at rectangles
   $5 \times 4$ and $7 \times 6$ [MV], and the dimension identity is
   machine-verified exactly at $(4,2)$ and, nontrivially (degree-3 shifts
   present), at $(6,3)$: $\dim(V \cap S_{\le 2}) = 511 = \dim V_{\le 2}$
   [MV].
3. **NEW CORRECTION (inventory gap).** The corpus's block-free event
   inventory $\{E_{row}, E_{star}, E_K\}$ is INCOMPLETE. Sums of inventoried
   rows have supports that complete no single row and no single star, yet are
   pinned: the double star DS (two same-target star columns, XOR $= 0$),
   the crossed-star pair UU, and the cross grid OFF (all [MV] in $V$ and
   alias-aware block-free at $(4,2)$ and $(6,3)$; the DS pin verified on
   200 sampled uniform designs at $(4,2)$). The block-free identification is
   repaired with the enlarged inventory. The recorded [MV] sweeps
   (1192/1192, 250/250) sampled random windows of size $\le 10$ and could not
   have hit these structured sparse supports; no recorded measurement moves.
4. **CNT.** The non-adaptive completion bound is PROVED for the enlarged
   inventory: $\varepsilon_{full} = (1 + o(1))\,\varepsilon_{headline}$; the
   headline form $(e/n)^{2d} + (2e/(n-1))^{2d-1}$ IS the tight form (probe
   lower bound matches up to factorial slack). The adaptive case is REDUCED
   to two explicit bookkeeping lemmas (B1, B2 below); B2 closes in the regime
   $d^2 \log k = o(n)$ with adaptive distortion $\exp(O(ed/n)) = 1 + o(1)$.
   The exact adaptive constant at the boundary $d^2 = \Theta(n)$ stays OPEN;
   no recorded conclusion moves.
5. **O5 assembled (Section 6):** the AND-no-lift transfer holds at general $d$
   for every adaptive degree-$\le 2$ tree with $e = o(n)$ and
   $d^2 \log k = o(n)$, modulo the CLS base caveat (cor:coin) and B2; it is
   EXACT for $e < 2d$; at $d \le 3$ it is unconditional; at $e = \Theta(n)$
   it stays open (O2(iv)).

## 1. Setup

Fix the restricted system $(2d, d)$: rectangle $D \times R$ with $|D| = 2d+1$
pigeons and $|R| = 2d$ holes; variables $x_{ij}$, $(i,j) \in D \times R$.
$S_{\le k}$ is the span of degree-$\le k$ monomials (multiset monomials).
The system generators are $Q_i = 1 + \sum_j x_{ij}$ (degree 1), the Boolean
rows $b_{ij} = x_{ij}^2 + x_{ij}$, the hole collisions
$C_{i_1 i_2 j} = x_{i_1 j}x_{i_2 j}$ and the two-hole rows
$H_{i j_1 j_2} = x_{i j_1}x_{i j_2}$ (degree 2).
$I$ is the ideal they generate in the polynomial ring
$\mathbb{F}_2[x_{ij}]$;
$V = \mathrm{span}\{m \cdot h : h$ a generator, $\deg(mh) \le d\}$ is the
naive truncation, and $I \cap S_{\le d} \supseteq V$ with equality unknown in
general (the exotic-relation question).
A design is $L$ with $L|_V = 0$, $L(1) = 1$; determined columns are exactly
$V \oplus \langle e_0 \rangle$ (columns constant on designs), and every other
column is a fair coin (balance lemma).
Write $V_{\le 2}$ for the span of the generator rows of degree $\le 2$:
$\mathrm{span}\{Q_i,\ Q_i x_{ab},\ b_{ij},\ C,\ H\}$; note the reduced star
rows $s_{r,cd} = Q_r x_{cd} + C_{r,c,d}$ lie in it.
For a window $T$ of degree-$\le 2$ coordinates, the projected law is uniform
on $L^*|_T + \pi_T(\Lambda)$ with $\Lambda = \{\lambda : \lambda|_V = 0,
\lambda(1) = 0\}$,
and it equals the fresh-bit law exactly iff $\pi_T(\Lambda)$ is full on the varying
coordinates of $T$; the obstruction is a nonzero $g$ supported on the varying
coordinates with $g \in V \oplus \langle e_0 \rangle$.

## 2. CLS(i): diagonals vary at general $d$ [PROVED]

A diagonal is a matching-2 column.
Theorem A of deg4_theory.md (matching hierarchy) proves: at every restricted
$(2d,d)$, if all matching-$(k-1)$ columns vary then all matching-$k$ columns
vary, for $1 < k \le d$, by the star-row argument (if all matching-$k$ were
determined, the star identity $\bigoplus_{j} \mathrm{ans}(x_{pj} h) =
\mathrm{ans}(h)$ for a free $p \notin h$ would determine the matching-$(k-1)$
column $h$, and orbit closure under $S_{2d+1} \times S_{2d}$ finishes).
The base $k = 1$ (singles vary) is the paper's cor:coin, [PROVED] at general
$d$ and every $p$ (channel_spec.md Section 2.1).
At $k = 2$: all matching-2 columns (all diagonals) vary at every $d \ge 2$.
The balance lemma upgrades variation to marginal fairness, which is the only
input Lemma M's posterior arithmetic consumes.
Caveat inherited from deg4_theory.md Section 7 item 1: the base is
cor:coin plus kernel measurement, not a self-contained elementary proof; the
gap is small and does not affect the $d \le 3$ unconditional statements.

## 3. CLS(ii) core: the degree-2 slice of the relation space [PROVED]

### 3.1 The exact claim (Q-A)

$$V^{(\le 2)} := (V \oplus \langle e_0 \rangle) \cap S_{\le 2}
 \;=\; V_{\le 2} \oplus \langle e_0 \rangle.$$

Equivalently: no combination of generator rows of degree $\le d$ (for any
$d \ge 2$, shifts of degree up to $d$ allowed) cancels down to a
degree-$\le 2$ polynomial outside the span of the degree-$\le 2$ rows.
At $d = 2$ this is trivial (there are no higher shifts); at $d = 3$ and
beyond it is not, because combinations of degree-$\ge 3$ shifts can cancel
their high-degree parts (the failure mode deg4_theory.md Section 1 recorded
for the graded argument).

### 3.2 The degree-truncated Buchberger lemma

Lemma TB. Let $J = \langle G \rangle \subseteq R$ and fix $t \ge 0$.
Suppose every S-polynomial $S(g_1, g_2)$ of a pair $g_1, g_2 \in G$ whose
leading-monomial lcm $M$ satisfies $\deg M \le t$ reduces to $0$ by steps
$r \mapsto r + m \cdot g$ ($m\,\mathrm{in}(g) \le$ the target monomial) that
never create degree $> t$.
Then every $g \in J$ with $\deg g \le t$ lies in
$\mathrm{span}\{m \cdot h : h \in G, \deg(mh) \le t\}$.

Proof sketch (standard; included because the corpus relies on it).
Take $g \in J$, $\deg g \le t$, and among its representations
$g = \sum_k q_k g_k$ choose one minimizing the maximum term degree $s$, then
the number of terms at degree $s$.
If $s \le t$ and each $q_k g_k$ has $\deg \le t$ we are done.
Otherwise the degree-$s$ homogeneous part of $g$ vanishes, so two top terms
$m_1 g_1, m_2 g_2$ share a top monomial $M' = m_1 \mathrm{in}(g_1) =
m_2 \mathrm{in}(g_2)$, and $m_1 g_1 + m_2 g_2 = m' S(g_1, g_2)$ exactly, with
$m' = M' / \mathrm{lcm}_0$.
By hypothesis $S(g_1, g_2)$ reduces to $0$ within degree $\le t$, and the
reduction steps multiplied by $m'$ keep degree $\le \deg M' \le s$; substituting
the reduction removes at least the two top terms without raising $s$,
contradicting minimality.
$\mathrm{QED}$

### 3.3 The master identities and the type enumeration

Take $G = \{Q_i,\ b_{ij},\ C,\ H,\ Q_r x_{cd}\}$ (the star rows $Q_r x_{cd}$
are ideal elements, added to make the reduced stars reducible).
With any fixed monomial order (deg-lex), the leading monomials of $G$ have
degree $\le 2$ (a single for each $Q_i$, squares and pairs for the rest),
and distinctness can fail (a shifted $Q_i x_{ib}$ can lead with the square
$x_{ib}^2$, colliding with $b_{ib}$'s lead), so the enumeration below is
trusted only as staged by the exhaustive machine sweep of Section 3.4,
which checks every pair mechanically, including equal-lead pairs.
The pairs with lcm-degree $\le 2$ are exactly those where one leading
monomial divides the other or the two are equal:
unshifted pairs $(Q_i, Q_{i'})$, $(Q_i, b)$, $(Q_i, C)$, $(Q_i, H)$,
$(Q_i, Q_r x_{cd})$;
singly-shifted pairs $(m Q_i, h)$ with $h \in G$, $m$ a single;
doubly-shifted pairs $(m_1 Q_i, m_2 Q_{i'})$ with equal leading monomials;
and the equal-lead pairs among the degree-2 rows themselves.
(Pairs where both leading monomials are distinct degree-2 monomials have
lcm-degree $\ge 3$ and are exempt.)

All of them reduce to zero within degree $\le 2$ via five master identities
(valid as universal ring identities for every rectangle with at least 4
holes, i.e. every $d \ge 2$; here $S(r, c, d) = Q_r x_{cd} + C_{r,c,d}$ is the
reduced star row):

- M1: $x_{i'j}\, Q_i = C_{i,i',j} + S(i, i', j)$ for $i \ne i'$
  (the star-row definition; it alone settles every $(Q, \cdot)$ S-poly,
  since each such S-poly is $m Q_i$ plus one row whose leading monomial the
  identity absorbs).
- M2: $x_{ij'}\, Q_i + H_{i,j,j'} = b_{ij'} + \sum_{t \notin \{j,j'\}} H_{i,t,j'}$.
- M3: $x_{ij}\, Q_i + b_{ij} = \sum_{t \ne j} H_{i,t,j}$.
- I1: $x_{i'j'}\, Q_i + x_{ij}\, Q_{i'} = S(i,i',j') + S(i',i,j) +
  C_{i,i',j'} + C_{i,i',j}$ for $j \ne j'$.
- M5: $Q_r x_{cd} = C_{r,c,d} + S(r,c,d)$ (definition of the reduced star).

Every reduction step multiplies by a monomial quotient and stays within
degree $\le 2$, so Lemma TB applies with $t = 2$ and gives
$I \cap S_{\le 2} = \mathrm{span}\{m \cdot h : h \in G, \deg(mh) \le 2\} =
\mathrm{span}\{Q_i,\ Q_i x_{ab},\ b_{ij},\ C,\ H\} = V_{\le 2}$.
Since $e_0 \notin V$ (designs exist; [MV] at both anchor points), this is
exactly Q-A: **the determined relations of degree $\le 2$ are generated by
the inventoried families, at general $d$.** [PROVED]

### 3.4 Machine verification [MV]

- Ring identities M1, M2, M3, I1, M5: ALL position instances at rectangles
  $5 \times 4$ and $7 \times 6$ (the second larger than every restricted
  system through $d = 3$): PASS.
- Generic sweep: ALL S-polynomials of generator pairs with lcm-degree $\le 2$
  (465 instances at $5 \times 4$, 1225 at $7 \times 6$) lie in the span of
  the degree-$\le 2$ row set: PASS. (The sweep enumerates all pairs
  mechanically; no hand list is trusted.)
- Exact dimension identity: at $(4,2)$,
  $\dim(V \cap S_{\le 2}) = 165 = \dim V_{\le 2}$ (harness anchor);
  at $(6,3)$, $\dim(V \cap S_{\le 2}) = 511 = \dim V_{\le 2}$ with the
  degree-3 shifts present (rank of $V$ restricted off $S_{\le 2}$ is 11599 $=
  12110 - 511$): PASS. This is the first exact confirmation of Q-A at a
  system where higher shifts exist.

### 3.5 Where the proof binds

The proof is $d$-uniform: the master identities are ring identities
independent of the hole count, and the truncated-Buchberger lemma needs only
that the exempt S-pairs (lcm-degree $\ge 3$) exist, which they do for every
$d \ge 2$.
The one critical enumeration (which pairs have lcm-degree $\le 2$) is
swept exhaustively by machine at two rectangle sizes, so within those
rectangles nothing can hide.
The first system not covered by an exact dimension check is restricted
$(8,4)$; the targeted computation there is
$\dim(V(8,4) \cap S_{\le 2})$ versus $\dim V_{\le 2}$, currently infeasible
(1.28M-coordinate echelon, the deg4 instrument wall) and unnecessary for the
proof, which covers it.

## 4. The inventory correction: supports of sums of rows [PROVED relations, MV]

### 4.1 The new pinned block-free windows

Q-A says the relations are generated by the inventoried rows; it does NOT say
the inventory's named events exhaust the supports.
The following sums of reduced star rows $s_{r,cd} = Q_r x_{cd} + C_{r,c,d}$
(all in $V_{\le 2}$, all [MV] at $(4,2)$ and $(6,3)$) have supports that
trigger neither $E_{row}$ (needs $2d$ effective singles) nor $E_{star}$
(needs all $2d-1$ fresh products plus the target in the effective set):

- DS (double star): $s_{r,cd} + s_{r',cd}$ for $r \ne r'$.
  The two target singles cancel; the support is the two fresh columns,
  $2(2d-1)$ diagonals with common pair $(c,d)$, and the pin is
  $\bigoplus = 0$.
  Needs $r, r' \in D$ for the pin to diverge from fresh-bit (if the target is
  matched the pin still fires; if it is killed all terms are $0$).
- UU (crossed star pair): $x_{c'd'}\, Q_{c} + x_{cd}\, Q_{c'}$ with
  $(c,d) \ne (c',d')$ (I1's combination).
  Each star's support loses exactly its crossed diagonal to the cancellation;
  the support is 2 target singles plus $4d-4$ diagonals (varying support
  $4d-2$ counting the two same-line collisions as determined), pinned to
  $0$.
  Each involved star misses exactly one fresh product, so no star completes.
- OFF (cross grid): $\sum_j Q_i x_{i'j} + Q_{i'} + \sum_j C_{i,i',j} =
  \Sigma_{off} + e_0$ where $\Sigma_{off}$ is all $2d(2d-1)$ diagonals
  $x_{cd'}x_{c'd}$ with $d \ne d'$ between the two rows.
  Pinned to $1$ (it is XOR of $2d$ star rules with the row lock).
  No star completes (each star target is absent) and no row completes.

All three supports are alias-aware block-free under lemma_m.md's $E_{row}$ /
$E_{star}$ definitions [MV], and on each of them the true law is a proper
parity coset while fresh-bit is uniform: TV $= 1/2$.
The DS pin is verified directly on 200 sampled uniform designs at $(4,2)$
(0 violations) [MV].
These are counterexamples to lemma_m.md Section 2.3's "no other discrepancy
exists" as an event statement, already at $(4,2)$ with 6 coordinates.
The corpus's sweeps tested random windows of sizes 2 to 10; at $(4,2)$ there
are 100 diagonal coordinates, so a random window of size $\le 10$ contains a
specific 6-coordinate support with probability of order $(10/100)^6$, and
1192 windows could not have found one.
The five sweep failures the corpus did catch were alias-assembled rows, a
different phenomenon, resolved by alias-awareness.

Provenance note: deg2_theory.md's ORIGINAL Lemma REL defined block-complete
as "all $2d-1$ diagonal coordinates of some sum-rule star", without the
target; that definition OVER-covers (every DS support contains a complete
fresh column) and was safe.
lemma_m.md's refinement added the target-single requirement, which is correct
for a single star alone (with the target unobserved and independent, the
projected law of the fresh column is uniform) but broke closure under sums:
two completed columns with a common cancelled target pin each other.
The repair below keeps the refinement and adds the missing classes.

### 4.2 The repaired inventory and covering theorem

Work in $\overline{V} :=$ the varying-coordinate projection of $V_{\le 2} \oplus
\langle e_0 \rangle$: alias and same-line rows project to $0$, so $\overline{V}$ is
spanned by the row vectors $R_i$ (weight $2d$, pairwise disjoint) and the
star vectors $S_{r,cd} = \{x_{cd}\} \cup \{x_{cd}x_{rj} : j \ne d\}$
(weight $2d$).
Overlap rules (each a two-line case check): a row and a star share the target
single iff $r = c$; same-target stars share the target single; crossed stars
($(c,d)$ and $(c',d')$ with the four cells distinct in the crossed alignment)
share exactly the diagonal $x_{cd}x_{c'd'}$, and every diagonal lies in
exactly two stars; same-row stars share nothing in $\overline{V}$.

Theorem (covering). Every support of a nonzero element of $\overline{V}$ contains one
of: (a) a full row $R_i$; (b) a full star $S_{r,cd}$; (c) a DS; (d) a UU;
(e) an OFF configuration. Status: PROVED for all two-star and star-plus-row
combinations (the case analysis above), and PROVED for the three named
multi-star families (DS, UU, OFF are themselves in $\overline{V}$ with the stated
supports [MV]); for sums of $\ge 3$ stars with cancellation chains the
covering is REDUCED to Lemma L-CLASS below, and is absorbed by the catch-all
counting bound of Section 5 either way.

Lemma L-CLASS (residual; OPEN as a classification, harmless for counting).
Every inclusion-minimal support of $\overline{V}$ either is one of (a)-(e) or has
$\ge 4d-1$ coordinates and multiplicity per coordinate $\le 2^{O(d)}
\,\mathrm{poly}(n)$ (each diagonal lies in exactly 2 stars, so minimal
supports through a coordinate are connected subconfigurations of the
star-overlap graph of degree $\le 4d$ through 2 vertices).
Not needed for any bound below: the catch-all term absorbs it.

Consequence (repaired identification, general $d$).
For every fixed $\rho$ and every window $T$ of degree-$\le 2$ coordinates,
the projected pipeline law on $T$ equals the fresh-bit law EXACTLY iff $T$
contains none of: a full row support, a full star support (target plus
$2d-1$ fresh products), a DS, a UU, an OFF (and, for linear-form queries, no
full $K$-column set).
Direction $\Leftarrow$: Q-A (Section 3) says any pin comes from
$V_{\le 2} \oplus \langle e_0 \rangle$, the covering theorem says its
support contains a named configuration, and the alias-aware convention makes
fresh-bit agree with every determined coordinate.
Direction $\Rightarrow$: each named configuration, when contained in $T$,
pins a proper parity coset against fresh-bit (TV $1/2$; [MV] for DS at
$(4,2)$ and for the completed star/row windows in the corpus).
[PROVED at general $d$ modulo the CLS base caveat; unconditional at
$d \le 3$.]

### 4.3 What changes in the corpus record

1. lemma_m.md Sections 2.2/2.3: the event inventory gains $E_{DS}$, $E_{UU}$,
   $E_{OFF}$; the sentence "no other discrepancy exists" is repaired to the
   covering theorem above.
   The [MV] sweep evidence is re-interpreted as sampling evidence, which it
   already was.
2. channel_spec.md Section 3.2 is FROZEN: per its own protocol it needs a
   dated amendment adding the three event classes to the block-free
   definition and to Route B's event tracking.
   Route B remains conforming-in-TV because the corrected
   $\varepsilon$ (Section 5) is still $o(1)$ in the regime, but a simulator
   that tracks only $E_{row}/E_{star}/E_K$ under-reports completions.
3. Lemma REL's original constants and its over-covering definition are
   unchanged and safe; Lemma M's headline bound survives with dominated
   extra terms (Section 5), so no downstream constant moves:
   $q$, $q_{and\_exact} = 0.2786$ at $(32,2)$, the cap $q^*_2$, and the
   regime line $c(c-1) \ge 2d^2(4d^2-1)$ are untouched.
4. deg4_theory.md's forward note for O2 conjectured "no relation class with
   sub-$\Theta(n)$ completion cost".
   DS/UU have support size $\Theta(d)$, not $\Theta(n)$: the conjecture is
   false in form.
   It is harmless for the budget asymptotics (their completion probabilities
   carry an extra $(e/n)^{2d-2}$-type factor and remain dominated), but the
   O2 induction must track support sizes, not query costs.

## 5. Lemma CNT: completion counting with the corrected inventory

### 5.1 Non-adaptive bound [PROVED]

Fix an oblivious query set $\mathcal{Q}$, $|\mathcal{Q}| = e$, of degree-$\le 2$ queries.
Let $s_{cd,r}$ be the number of queried diagonals with target pair $(c,d)$
and row $r$; each diagonal query lies in exactly two star families, so
$\sum_{(c,d),r} s_{cd,r} \le 2e$.

- $E_{row}$: $P \le A (e/n)^{2d}$ (corpus Step 2, unchanged).
- $E_{star}$: $P \le A (2e/(n-1))^{2d-1}$ (corpus Step 2, unchanged).
- $E_{DS}$: a double star at $(c,d; r,r')$ needs both fresh columns covered
  and $r, r' \in D$: per family $A^2 (s_{cd,r}s_{cd,r'})^{k}/(n-1)^{2k}$
  with $k = 2d-1$; with
  $\sum_{(c,d),r} s_{cd,r}^{k} \le (\max s)^{k-1} \cdot 2e \le 2e^{k}$ and
  $\sum_{r<r'} x_r x_{r'} \le \tfrac12(\sum_r x_r)^2$ over $x_r = s_{cd,r}^k$,
  $$P(E_{DS}) \le \frac{2 A^2\, e^{4d-2}}{(n-1)^{4d-2}}.$$
- $E_{UU}$: charging each single query to at most $n^2$ UU families and each
  diagonal to at most $2n$, the same arithmetic gives
  $P(E_{UU}) \le A^2 e^{4d-2} n^{10-8d}$.
- $E_{OFF}$: a cross grid needs $2d(2d-1)$ specific diagonals and two free
  rows: $P(E_{OFF}) \le \tfrac12 n^2 A^2 (e/n^2)^{2d(2d-1)}$.
- Catch-all (absorbs Lemma L-CLASS): any additional minimal class has
  supports of size $\ge 4d-1$ with per-coordinate multiplicity
  $2^{O(d)}\mathrm{poly}(n)$, giving the same-form term
  $\le 2^{O(d)}\,\mathrm{poly}(n)\, A^2 (e/n^2)^{4d-1}$.

Dominance. For $d \ge 2$ and $e = o(n)$:
$\Delta_{DS} \le A (e/n)^{2d} \cdot A(e/n)^{2d-2} \cdot 2 = o(E_{row}$ term$)$;
$\Delta_{UU}$, $\Delta_{OFF}$, and the catch-all are $o$ of the headline as
well (numerically illustrated in the run output: at $(128,2)$, $e = 32$:
headline $2.6 \times 10^{-3}$, all $\Delta$ terms $\le 2 \times 10^{-7}$).
Hence
$$\varepsilon_{full}(e,n,d) := \frac{A}{2}\Big[\Big(\frac{e}{n}\Big)^{2d}
 + \Big(\frac{2e}{n-1}\Big)^{2d-1}\Big] \cdot (1 + o(1)),$$
with the $o(1)$ uniform over the inventory enlargement, and
$\varepsilon_{full} = o(1)$ exactly when $e = o(n)$.
The minimum varying-support size over the whole inventory is $2d$, achieved
only by rows and stars (a combination of two or more generators has varying
support $\ge 4d-2$; the overlap rules of Section 4.2), so at $e < 2d$ no
event can fire and the transfer is EXACT.

### 5.2 Tightness of the headline form

A deliberate star probe costs $2d$ queries and succeeds with probability
$A / \binom{n-1}{2d-1} \approx A\,(2d/n)^{2d-1} \cdot (2d-1)!^{-1}$-type
factor: the same $(e/n)^{2d-1}$ form as the corpus's bound, with only
factorial slack.
A deliberate DS probe costs $4d-2$ queries and succeeds with probability
$\le A^2/\binom{n-1}{2d-1}^2$: the same form as $\Delta_{DS}$.
So the headline form is tight, and at budgets $e = \Theta(d)$ no adaptive
tree can push the completion probability above a constant multiple of the
probe values $A/\binom{n-1}{2d-1}$ (star) and $A^2/\binom{n-1}{2d-1}^2$
(double star): any sharper bound must keep these terms.

### 5.3 Adaptive trees [REDUCED to B1 + B2; closed in the regime]

Completion events depend only on the query SET, never on the answers.
Adaptivity therefore matters only through the distribution of the query set,
which the tree steers with answer information; under the fresh-bit coupling
(Lemma M Step 1) the answers separate into determined answers (which carry
$\rho$-information) and fresh coins (which carry none).
The per-answer classification:

- B1 (posterior formulas; PROVED, exact). For a single query answered $0$ at
  $(i,j)$: $P(j \in R \mid 0) = (2d/n) \cdot \frac{1 - (2d+3)/(2(n+1))}{1 -
  h_1}$, a relative distortion of the prior by $1 - \Theta(d/n)$: zeros are
  uninformative about $R$ at the scale that matters.
  A matched hit (probability $m = c/((n+1)n)$ per query) reveals $\rho(i) =
  j$, hence $j \notin R$: it can only EXCLUDE a hole from $R$ (anti-helpful
  for completion), at a total rate of $O(e/n)$ exclusions.
  A free hit (probability $A (2d/n) \cdot 1/2 = d(2d+1)/((n+1)n)$ per query)
  confirms $(i,j) \in D \times R$.
- B2 (distortion product bound; REDUCED, standard). Each free hit can remove
  at most one hidden condition from any completion event, multiplying that
  event's probability by at most $n/d$ (the larger of the exponent-gain
  $n/e$ and the factor $1/A \approx n/(2d)$).
  For $K \sim \mathrm{Bin}(e, d(2d+1)/((n+1)n))$ free hits,
  $\mathbb{E}[(n/d)^K] \le \exp(2ed/n)$ by the binomial moment generating
  function.

Proposition CNT-A. Every adaptive degree-$\le 2$ tree of budget $e$ satisfies
$$P[E_{full}] \;\le\; \varepsilon_{full}(e,n,d)\,\exp(2ed/n) \;+\; O(e/n),$$
and in the regime $d^2 \log k = o(n)$ with $e = d \log k$ the distortion is
$1 + o(1)$, so the non-adaptive bound is the tight adaptive form there.
Status: the classification B1 is PROVED; B2 is REDUCED (the multiplicative
bookkeeping must also track budget reallocation across rows whose death the
tree learns from matched hits; any polynomial loss in B2 leaves the regime
statement unchanged, and the $\exp(2ed/n)$ form is conjectured tight).
At the boundary $d^2 = \Theta(n)$ the exact adaptive constant remains OPEN
(this is the corpus's existing boundary; the headline form remains the
operative statement there, exactly as for Lemma REL).

So: the corpus's exposure convention is REPLACED, in the regime
$d^2 \log k = o(n)$, by the explicit bound above; CNT's non-adaptive case is
closed for the full corrected inventory; the adaptive case is closed in the
regime modulo B2; the boundary constant is the only residual OPEN.

## 6. O5 assembled

The AND-no-lift transfer (Lemma M) at general $d$, after this analysis:

| regime | status |
|---|---|
| $e < 2d$ | transfer EXACT, general $d$ [PROVED: min support $2d$; CLS(i)+(ii) core] |
| $d \le 3$ (restricted $(2,1),(4,2),(6,3)$), any $e = o(n)$ | PROVED unconditional modulo CNT-adaptive-in-regime (now closed there); Q-A additionally machine-checked |
| general $d$, adaptive, $e = o(n)$, $d^2 \log k = o(n)$ | PROVED modulo: CLS base = cor:coin (paper), Lemma L-CLASS (absorbed by catch-all), bookkeeping lemma B2 |
| general $d$, $e = \Theta(n)$ | OPEN (O2(iv), unchanged) |
| boundary $d^2 = \Theta(n)$, exact adaptive constant | OPEN (unchanged; headline form operative) |

Consequences for the AND chain: every budgeted certificate-free degree-2 hit
carries posterior $q_{and\_exact} + O(\varepsilon_{full})$ at general $d$ in
the regime, with $\varepsilon_{full} = (1+o(1))\,\frac{A}{2}[(e/n)^{2d} +
(2e/(n-1))^{2d-1}]$; the cap repair $q^*_2 = \max(q, q_{and\_exact})$ and the
regime line $c(c-1) \ge 2d^2(4d^2-1)$ stand verbatim; the $(32,2)$
prediction $q_{and\_exact} = 0.2786$ is untouched (single-pass, no
completion needed).

## 7. Residual opens and the minimal counterexample search space

1. CLS base (inherited): a self-contained elementary proof that free singles
   vary at general $d$ (deg4_theory.md Section 7 item 1).
   Until then CLS is PROVED relative to the paper's cor:coin.
2. Lemma L-CLASS: full classification of inclusion-minimal supports of $\overline{V}$
   beyond the five named classes.
   Where a surprise could hide: a $\ge 3$-star cancellation chain whose
   minimal support is NOT a supersupport of any pair configuration.
   Smallest probe: restricted $(4,2)$ and $(6,3)$, where
   $\overline{V} = \phi(V_{\le 2} \oplus \langle e_0 \rangle)$ has dimension 166 and
   512 over 231 and 946 coordinates: minimal-support enumeration (minimal
   codewords of a binary linear code) is exponentially bounded but
   randomized support-minimization probes are cheap and would run in
   seconds; the catch-all bound makes even a surprise harmless for the
   regime.
3. The targeted exact check at restricted $(8,4)$:
   $\dim(V(8,4) \cap S_{\le 2}) = \dim V_{\le 2}$ (needs the 1.28M-coordinate
   echelon; infeasible today, covered by the proof).
4. B2's exact form and the boundary constant at $d^2 = \Theta(n)$: smallest
   parameters where adaptive distortion could exceed $1 + o(1)$: $d \approx
   \sqrt{n}$ with $e \approx d \log k$; simulation probe: outer systems with
   $d = 3$ or $4$, trees that spend budget on $K_j$-style column-parity
   information before probing stars.
5. The degree-$\ge 3$ analogues: the fresh-bit inventory at degree 3
   (deg3_theory.md Lemma REL-3) inherits the same support-closure gap; the
   repaired template of Section 4 applies verbatim and has not been written
   out there.

## 8. Corrections this analysis records

1. lemma_m.md Section 2.2/2.3: the event inventory is enlarged by
   $E_{DS}$, $E_{UU}$, $E_{OFF}$; "no other discrepancy exists" is repaired
   to the covering theorem of Section 4.2.
2. channel_spec.md Section 3.2 (frozen): requires a dated amendment per its
   own protocol; Route B event tracking must include the new classes.
3. deg2_theory.md Lemma REL's original (target-free) block-complete
   definition over-covers and remains safe; lemma_m.md's refined $E_{star}$
   under-covered; the repair keeps the refinement and adds the classes.
4. Lemma M's $\varepsilon$ survives as $\varepsilon_{full} = (1+o(1))
   \varepsilon_{headline}$: no recorded constant or regime moves.
5. deg4_theory.md's O2 forward note ("no sub-$\Theta(n)$ completion
   classes"): false in form (DS/UU have $\Theta(d)$ supports); harmless in
   regime; the O2 induction should track support sizes.
6. deg2_theory.md Section 3 Step 3 / Section 5 item 2: CNT's non-adaptive
   case is closed for the full inventory; the adaptive case is closed in the
   regime $d^2 \log k = o(n)$ modulo B2; only the boundary constant remains
   open.
7. Instrument note: kernel_structure.py's `rowspace_intersection` undercounts
   on non-reduced echelons (already recorded in lemma_m.md Section 7); this
   session re-derived the same gotcha independently and used the exact
   concatenated-echelon method in `chi_cls_cnt_check.py` part D.

## 9. Verification record

Registered run: `cd /home/tomzx/pnp && python3 experiments/chi_cls_cnt_check.py`
(171 s, 40 PASS / 0 FAIL; `--fast` skips the $(6,3)$ heavy checks).
It imports `razborov_check.py` and `kernel_structure.py` unchanged.
Highlights:

- V0 anchors: rank 165 / dim Des 65 at $(4,2)$; rank 12110 / dim Des 2079 at
  $(6,3)$; $e_0 \notin V$.
- V1/V2 (Q-A): $\dim(V \cap S_{\le 2}) = \dim V_{\le 2} = 165$ at $(4,2)$
  and $= 511$ at $(6,3)$ (nontrivial: degree-3 shifts, restricted-off rank
  11599).
- V3: master identities M1-M5, I1 at all instances of $5 \times 4$ and
  $7 \times 6$; generic truncated-Buchberger sweep: 465 and 1225 S-polys
  with lcm-degree $\le 2$, all in the span of the degree-$\le 2$ rows.
- V4: DS, UU, OFF in $V$; supports alias-aware block-free at $(4,2)$ and
  $(6,3)$; DS pin $= 0$ on 200 sampled uniform designs at $(4,2)$.
- V5: minimality: every full row support carries exactly the parity pin and
  every full reduced-star support exactly the star row (80 stars at $(4,2)$,
  252 at $(6,3)$), by exact supported-subspace computation.
- V6: $\varepsilon_{full}$ table including the $\Delta$ terms at
  $(32,2), (128,2), (64,4), (1024,4), (2^{16},16), (2^{20},64)$: all
  $\Delta$ terms dominated by the headline at every printed point.

Corrections made during the run, per corpus discipline: (1) the first UU
probe used the leading-monomial naming $j = j'$, whose support contains two
COMPLETE stars (the cancelled common term is a collision, not a fresh
product) and is therefore $E_{star}$-covered; the genuinely new class is the
$I1$ combination with $j \ne j'$; (2) `rowspace_intersection` undercounted
(item 7 above) and was replaced.

## CORRECTION (2026-10-04, inv3 agent): the t=2 Buchberger engine consumed a false
## reduction hypothesis - conclusion re-proved by the repaired engine

Lemma TB's reduction hypothesis fails for the corpus's own G at t = 2 (live
witness S(Q_0, C_{0,1,3}) = RS(0,1,3), exhaustively non-reducible). The sweep
behind this document's t=2 record tested the weaker in-span condition and
treated it as equivalent to reduction - the equivalence is false (counterexample
G = {x^2, xy + 1}). The t=2 CONCLUSION (V_<=4 cap S_<=2 = V_<=2 at the recorded
parameters) is RE-PROVED by the repaired engine (degree-capped completion with
machine-enforced span neutrality): docs/inv3.md. The section-3 Buchberger
argument's master identities are unaffected; the engine repair is the record.
