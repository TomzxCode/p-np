# The chi-transfer: the printed chi-quantity of arXiv:2609.35927 vs the
# corpus's capped quantity

Result of the theory agent (2026-10-04). Status: analysis against the primary
source, not peer-reviewed. Source: https://arxiv.org/html/2609.35927 (v2,
30 Sep 2026), fetched this session (251,655 bytes HTML, LaTeXML), converted
with pandoc and re-verified against the raw math alttext. All quotes below are
from that HTML, normalized to corpus ASCII math; section numbers are the
paper's. Inferences beyond the quotes are marked INFERENCE; corpus
machine-verified facts are marked [MV]. No corpus file was edited; LOG.md was
not touched.

## 0. Executive answer

1. The printed "conflict pair" is a pair of POLYNOMIALS $(g, g')$, not a pair in
   $D^\rho \times R^\rho$ (Sec 3). The corpus's reading of "conflict pair" as a free
   pair is a misnomer relative to the printed text; the two notions are
   connected one-way by Lemma 4.4.
2. There are THREE distinct printed probabilities. The corpus's failure
   quantity is the printed $\mathrm{err}$ of the reduced tree $T'$ (Sec 5: output outside
   $D^\rho \times R^\rho$, sampled by $\omega \in \Omega(n,d)$). Theorem 6.1's hypothesis (3)
   is a DIFFERENT quantity: $\mathrm{Prob}$ over $(\rho, P)$ with $P$ UNIFORM over the $p^{e'}$
   paths, carrying the extra $\mathrm{Span}$ conjunct. Lemma 5.2 (printed) gives
   $\mathrm{err} \ge \chi$-prob: the printed $\chi$-quantity is SMALLER than the corpus's
   failure. The direction the task calls (a) ($\chi \ge$ failure) is false.
3. The cap of deg2_theory.md (Corollary 3.1) lower-bounds $\mathrm{err}$; it does NOT
   lower-bound $\chi$-prob. The exact transfer formula is
   $\chi$-prob $\ge p^{-\Delta(T)}\,\mathrm{err}(T)$, where $\Delta(T)$ is the maximal
   "defect" $e' - \dim^\rho(P)$ over $\chi$-good paths of $T$. The transfer closes
   iff $\Delta(T) = O(\log_p k)$.
4. $\Delta$ is not bounded in general: a trivial tree (query $e'$ row-sum
   polynomials $Q_i$, which lie in the printed system and are determined $0$;
   output a fixed pair) has $\mathrm{err} = 1 - f \ge 1/2$ but
   $\chi$-prob $= (1 - f)\,p^{-e'} = k^{-\Theta(d)}$. So the printed hypothesis (3),
   under the universal tree quantifier the reduction logic forces, is FALSE at
   growing $d$. The budgeted $\chi$-hypothesis is alive only in the $\mathrm{err}$-form (the
   form O2 actually states), and the reduction closes in the $\mathrm{err}$-form through
   Definition 3.1 + Lemma 4.4 + Theorem 3.3, bypassing the printed (3).
5. Reading checks settled: Definition 3.1's tree quantifier IS budgeted ($e$ is
   a parameter of a $(d, e, \gamma)$-solution; condition 3 says "For any
   $(d,e)$-tree $T$"). Theorem 6.1's budget is $(d, e')$ with
   $e' = O(\log n) + O(d \log n)$, printed as "= $d(\log k)$" via $k \ge n^3/2$.
   Theorem 3's degree-$\le 2$ class is a (proper) subset of the printed class at
   $d = 2$.

## 1. Exact quotes (arXiv:2609.35927v2)

### 1.1 Section 3 (Reduction to pseudo-solutions): trees and conflict pairs

"An $\mathbb{F}_p^{\le d}[x]$-tree $T$ is a finite $p$-ary tree whose each non-leaf vertex is
labeled by a query $g = ?$ for some polynomial $g \in \mathbb{F}_p^{\le d}[x]$ and the $p$
outgoing edges are labeled by $g = a$, for all $a \in \mathbb{F}_p$. The leaves of $T$ are
labeled by elements of some non-empty set $I$. The height of $T$ is the maximum
number of edges on a path from the root to a leaf. $\mathbb{F}_p^{\le d}[x]$-trees of
height $\le e$ are called $(d, e)$-trees."

"Any map $\omega : \mathbb{F}_p^{\le d}[x] \to \mathbb{F}_p$ defines a path in $T$ by answering the
queries by $\omega$. The label of the leaf on the path defined by $\omega$ is
denoted $T(\omega)$."

"If $\omega$ is a linear map but not a homomorphism there must be a conflict
pair: a pair of polynomials $g, g' \in \mathbb{F}_p^{\le d}[x]$, such that $\deg(gg') \le d$ and

   $\omega(g) \cdot \omega(g') \neq \omega(gg')$ ."

### 1.2 Definition 3.1 ([8]) and Theorems 3.2/3.3

"Definition 3.1 ([8]). For any $d, e \ge 0$ and $1 \ge \gamma \ge 0$, a
$(d, e, \gamma)$-solution of $F$ is a non-empty finite set $\Omega$ of maps
$\omega : \mathbb{F}_p^{\le d}[x] \to \mathbb{F}_p$ satisfying the following three conditions:
1. $\omega$ is $\mathbb{F}_p$-linear map: $\omega(a) = a$ and $\omega(g) + \omega(h) =
   \omega(g + h)$, for all $a \in \mathbb{F}_p$ and all $g, h \in \mathbb{F}_p^{\le d}[x]$.
2. For any two polynomials $f \in F$ and $g \in \mathbb{F}_p^{\le d}[x]$ it holds that
   $\omega(fg) = 0$, assuming $\deg(fg) \le d$.
3. For any $(d, e)$-tree $T$:

   $\mathrm{Prob}_{\omega \in \Omega}[T(\omega) \text{ is \textbf{not} a conflict pair for } \omega]$
   $\ge \gamma$ .

A pseudo-solution is a collective name for $(d, e, \gamma)$-solutions."

"Theorem 3.2 ([8, Thm.3.2]). Assume that there exists an ENS-refutation of $F$
with $S$ extension polynomials, of degree $d$ and accuracy $h$ satisfying
$e^{h/p} \ge 2S^2$. Then there is no $(d, h + \log S, S^{-1})$-solution of $F_n$."

"Theorem 3.3. For any constant $l \ge 2$ and any function $k = k(n) \ge 1$ the
followings holds: if there is an $((\log k)^{O(l)}, O(\log k), k^{-O(1)})$-solution
for $\neg\mathrm{PHP}_n$ then $\neg\mathrm{PHP}_n$ does not admit $F_l(\mathrm{MOD}_p)$-refutation with $k$ steps, for
all $n \gg 1$."

### 1.3 Section 4 (Pseudo-solutions for the PHP): the pipeline and Lemma 4.4

System polynomials (Sec 1): the left-hand sides named "$Q_{i_1,i_2;j}$,
$Q_{i;j_1,j_2}$ and $Q_i$" for the three bullets
"$x_{i_1,j} \cdot x_{i_2,j} = 0$", "$x_{i,j_1} \cdot x_{i,j_2} = 0$",
"$1 - \sum_{j \in [n]} x_{ij} = 0$", together with all "$x_{ij}^2 - x_{ij}$".
(Denote "the set of all these polynomials" by $\neg\mathrm{PHP}_n$.)

Restriction (Sec 4): "For a polynomial $g$ over $\mathrm{Var}(\neg\mathrm{PHP}_n)$ and a partial
injective map $\rho :\subseteq [n+1] \to [n]$ define the restriction $g^\rho$ of $g$ by $\rho$
the polynomial obtained by the following substitution of 0/1 values for some
variables: $x_{ij}^\rho = 1$ if $i \in \mathrm{dom}(\rho)$ and $\rho(i) = j$; $0$ if $i \in \mathrm{dom}(\rho)$
and $\rho(i) \neq j$; $0$ if $j \in \mathrm{rng}(\rho)$ and $\rho^{-1}(j) \neq i$; $x_{ij}$ otherwise.""
"Denote $D^\rho := [n+1] \setminus \mathrm{dom}(\rho)$, $R^\rho := [n] \setminus \mathrm{rng}(\rho)$ and
$n_\rho := |R^\rho|$ ($= n - |\rho|$). Note that $x_{ij}^\rho = x_{ij}$ iff
$(i,j) \in D^\rho \times R^\rho$."

"Definition 4.3 ([8, Def.4.2]). For $2 \le d \le n/2$ let $\Omega(n,d)$ be the set of
all maps $\omega \in \mathrm{Des}(n,d)$ that are defined as follows: 1. Pick (a) a
restriction $\rho :\subseteq [n+1] \to [n]$ with $n_\rho = 2d$, (b) a map
$L \in \mathrm{Des}(n,d)^\rho$. 2. For $g \in S(n,d)$ put: $\omega(g) := L(g^\rho)$."

"Lemma 4.4 ([8, L.4.3]). Let $T$ be a $(d,e)$-tree over $S(n,d)$. Then there is
$(d,e')$-tree $T'$ with $e' \le e + O(d \log n)$ such that for any
$\omega = (\rho, L) \in \Omega(n,d)$ if $T(\omega)$ is a conflict pair for $\omega$ then
$T'(\omega)$ is a pair $(i,j) \in D^\rho \times R^\rho$."

"The proof can be found in [8] but its idea is simple: tree $T'$ uses a conflict
pair found by $T$ to find (by a binary search argument) a conflict pair
consisting of monomials and then another pair where one of the monomials is a
variable $x_{ij}$. Clearly then $\rho(x_{ij}) \neq 0, 1$, i.e. $(i,j) \in D^\rho \times R^\rho$."

### 1.4 Section 5 (Expressing the error of a tree): err, chi, Error, Lemmas

"Let $T'$ be a $(d,e')$-tree with labels in $[n+1] \times [n]$. Our aim in this section
is to express the error $T'$ must make on $\Omega(n,d)$ in terms of restrictions
only. The phrase $T'$ errs on $\omega = (\rho, L)$ means that
$T'(\omega) \notin D^\rho \times R^\rho$."

"A path $P$ in $T'$ is a sequence of edges connecting the root with a leaf and
$\mathrm{lab}(P)$ denotes its label. For a path $P$ we define the set of polynomials
$A(P) \subseteq S(n,d)$ consisting of all $g - a$ such that $g = ?$ is queried on $P$ and $P$
follows the edge corresponding to $g = a$. Put $W(P) := \mathrm{Span}(V(n,d) \cup A(P))$."

"Define: $\dim^\rho(P) := \dim(W(P)^\rho) - \dim(V(n,d)^\rho)$."

"Sample $\omega = (\rho, L)$ will follow in $T'$ path $P$ and thus define
$T'(\omega) = \mathrm{lab}(P)$ iff $L$ vanishes on $A(P)^\rho$. Given $\rho$ such $L$ exists iff
$1 \notin \mathrm{Span}(W(P)^\rho)$ and in this case a random $L \in \mathrm{Des}(n,d)^\rho$ will define
$\omega := (\rho, L)$ following $P$ with probability $p^{-\dim^\rho(P)}$."

"Let $\chi(P, \rho)$ be the characteristic function of the set of pairs $P, \rho$
such that

   $\mathrm{lab}(P) \notin D^\rho \times R^\rho$  and  $1 \notin \mathrm{Span}(W(P)^\rho)$ .   (2)

That is, $\chi$ is a 0 - 1 function and it equals $1$ iff (2) holds. The first
condition in (2) means that for any $L$ $T'$ errs on $\omega = (\rho, L)$ following $P$
and the second one implies that for some $L$ $(\rho, L)$ indeed follows $P$."

"Define a random variable with values in $[0,1]$ fo $\rho \in \mathrm{Des}(n,d)$:
[sic: 'fo' for 'for', and Des where Res is meant]

   $\mathrm{Error}(\rho) := \sum_P \chi(P, \rho)\, p^{-\dim^\rho(P)}$

where $P$ ranges over all paths in $T'$."

"Lemma 5.1. For any $\rho \in \mathrm{Res}(n,d)$ and $L$ chosen randomly from $\mathrm{Des}(n,d)^\rho$:

   $\mathrm{Prob}_L[T' \text{ errs on } (\rho, L)] = \mathrm{Error}(\rho)$

and for $\omega$ chosen randomly from $\Omega(n,d)$:

   $\mathrm{Prob}_\omega[T' \text{ errs on } \omega] = \mathbb{E}_\rho[\mathrm{Error}(\rho)]$ ."

The derivation before Lemma 5.2: "The term $\mathbb{E}_\rho[\mathrm{Error}(\rho)]$ is the expected
value $\sum_\rho r^{-1}\,\mathrm{Error}(\rho)$ where $\rho$ ranges over $\mathrm{Res}(d,n)$ and
$r := |\mathrm{Res}(d,n)|$, [sic: Res(d,n) for Res(n,d)] and using $\dim^\rho(P) \le e'$ we
can lower bound this by $\sum_\rho \sum_P r^{-1} p^{-e'}\,\chi(P, \rho)$. Assuming
w.l.o.g. that all paths in $T'$ have the length $e'$ this is just the expected
value of $\chi(P, \rho)$ and as $\chi(P, \rho)$ has values $0, 1$ it is the probability
$\mathrm{Prob}_{\rho,P}[\chi(P, \rho) = 1]$."

"Lemma 5.2. Assume that every path in $T'$ has the length $e'$. Then

   $\mathrm{Prob}_\omega[T' \text{ errs on } \omega] \ge \mathrm{Prob}_{\rho,P}[\chi(P, \rho) = 1]$

where $\omega \in \Omega(n,d)$, $\rho \in \mathrm{Res}(n,d)$ and path $P \in T'$ are chosen
randomly and uniformly."

### 1.5 Section 6: Theorem 6.1

"The following summary statement follows at once from Theorem 3.3 and Lemmas
4.4 and 5.2.

Theorem 6.1. Let $l \ge 2$. Assume that for a $(d,e')$-tree $T'$ with

   $d = (\log k)^{O(l)}$  and  $e' = O(\log n) + O(d \log n) = d(\log k)$

it holds that:

   $\mathrm{Prob}_{\rho,P}[\chi(P, \rho) = 1] \ge k^{-O(1)}$    (3)

where $\omega \in \Omega(n,d)$, $\rho \in \mathrm{Res}(n,d)$ and path $P \in T'$ are chosen
randomly and uniformly. Then for all $n \gg 1$ any $F_l(\mathrm{MOD}_p)$-refutation of
$\neg\mathrm{PHP}_n$ requires at least $k(n)$ steps.

(For the estimate of $e'$ by $d(\log k)$ we use that $k \ge n^3/2$ as any refutation
of $\neg\mathrm{PHP}_n$ must use all polynomials $Q_{i_1,i_2;j}$.)

It appears possible that the hypothesis in the theorem holds for
$k(n) = 2^{n^\delta}$, for sufficiently small $\delta > 0$, even with the bound in
(3) being $\Omega(1)$."

## 2. The dictionary

### 2.1 The three printed probabilities (do not conflate)

$(P_1)$ Definition 3.1, condition 3: $\mathrm{Prob}_{\omega \in \Omega}[T(\omega)$ is not a
conflict pair for $\omega] \ge \gamma$. Sample: $\omega$ uniform in $\Omega$ (a solution
parameter; for the candidate, $\Omega = \Omega(n,d)$). Output: an arbitrary label
(for the conflict task, a polynomial pair $(g, g')$ violating multiplicativity).

$(P_2)$ Section 5's error of the REDUCED tree: $\mathrm{err}(T') := \mathrm{Prob}_\omega[T'$ errs on
$\omega] = \mathrm{Prob}_\omega[T'(\omega) \notin D^\rho \times R^\rho]$, $\omega$ uniform in
$\Omega(n,d)$. By Lemma 5.1 this equals $\mathbb{E}_\rho[\mathrm{Error}(\rho)]$ with
$\mathrm{Error}(\rho) = \sum_P \chi(P,\rho)\, p^{-\dim^\rho(P)}$: paths weighted by the true
design measure. THIS is the corpus's failure quantity. The corpus's success =
$1 - \mathrm{err}$.

$(P_3)$ Theorem 6.1's hypothesis (3): $\chi$-prob$(T') := \mathrm{Prob}_{\rho,P}[\chi(P,\rho)$
$= 1]$ with $\rho$ uniform over $\mathrm{Res}(n,d)$ and $P$ UNIFORM over the $p^{e'}$ paths of the
padded tree. No $L$ is sampled; the $\mathrm{Span}$ conjunct replaces it.

Printed relations: Lemma 4.4 gives $(P_1)$'s success for $T$ $\le (1 - (P_2))$ for the
reduced $T'$; Lemma 5.2 gives $(P_2) \ge (P_3)$. There is no printed relation in the
reverse directions.

Answer to the task's question: the printed $\chi$-probability $(P_3)$ is NOT
$\mathrm{Prob}$[tree outputs a non-conflict pair]. It is $\le$ the corpus's failure $(P_2)$,
and $(P_1)$ is a third, different quantity (polynomial-pair conflicts, $\omega$-
sampled). The corpus's informal "success $= 1 - \chi$" identifies $(P_2)$ with $(P_3)$;
they differ by the defect tax of Sec 3 below.

### 2.2 Dictionary table

| Printed object | Printed content | Corpus object | Same? |
|---|---|---|---|
| conflict pair (Sec 3) | polynomial pair $(g,g')$, $\deg(gg') \le d$, $\omega(g)\,\omega(g') \neq \omega(gg')$ | "conflict pair" = pair in $D^\rho \times R^\rho$ | NO: different objects; Lemma 4.4 maps one to the other one-way; the printed text never names $(i,j) \in D^\rho \times R^\rho$ a conflict pair |
| tree class (Sec 3) | adaptive $p$-ary tree, queries any $g \in \mathbb{F}_p^{\le d}[x]$ (outer variables, total degree $\le d$ over $\mathbb{F}_p$), height $\le e$ | adaptive tree, budget $e$ queries, degree $\le d$ polynomials over $\mathbb{F}_2$ | YES in form at $p = 2$ ($p = 2$ makes the tree binary); see 4.3 for the subset question at $d = 2$ |
| budget | height $\le e'$; Theorem 6.1: $e' = O(\log n) + O(d \log n)$, "= $d(\log k)$" for $k \ge n^3/2$ | $e = d \log k$ | YES up to an unprinted constant factor |
| output label | Sec 5: $T'$ labels in $[n+1] \times [n]$ | leaf label = outer pair $(i,j)$ | YES |
| error $(P_2)$ | $T'(\omega) \notin D^\rho \times R^\rho$, $\omega$ uniform in $\Omega(n,d)$ | failure | YES, exactly |
| sample for $(P_2)$ | $\omega = (\rho, L)$, $\rho$ uniform with $n_\rho = 2d$, $L$ uniform in $\mathrm{Des}(n,d)^\rho$ (uniform over pairs; $\lvert\mathrm{Des}(n,d)^\rho\rvert = \lvert\mathrm{Des}(2d,d)\rvert$ independent of $\rho$ by the printed isomorphism $S(n,d)^\rho \simeq S(n_\rho,d)$: INFERENCE) | the $\Omega(n,d)$ pipeline | YES |
| $\chi$-prob $(P_3)$ | $\mathrm{Prob}_{\rho,P}[\chi(P,\rho)=1]$, $P$ uniform over $p^{e'}$ paths, $\mathrm{Span}$ conjunct $1 \notin \mathrm{Span}(W(P)^\rho)$ | failure | NO: $(P_3) \le (P_2)$, gap = defect tax (Sec 3) |
| $\mathrm{Span}$ conjunct | $1 \notin \mathrm{Span}(W(P)^\rho)$: the path is realizable by some design | absent from the corpus's task | MISMATCH component (automatic on $L$-sampled paths, not on uniform ones) |
| $\rho$ space | $\mathrm{Res}(n,d)$: USED but never defined in this paper (only occurrences: Lemmas 5.1/5.2, Thm 6.1; plus the typo $\mathrm{Res}(d,n)$) | $\rho$ uniform partial injection, $n_\rho = 2d$ | YES by context (INFERENCE: $\mathrm{Res}(n,d) = \{\text{partial injective } \rho :\subseteq [n+1] \to [n] : n_\rho = 2d\}$) |
| Def 3.1 quantifier | "For any $(d,e)$-tree $T$", $e$ a parameter of the solution | the budgeted reading | CONFIRMED budgeted: no unbounded-tree quantifier anywhere; Theorem 3.2's no-solution has $e = h + \log S$ |
| Thm 6.1 quantifier | "Assume that for a $(d,e')$-tree $T'$ ... it holds that (3)" (literal grammar: per-tree) | "EVERY $(d, d \log k)$-tree" | Universal reading forced by the proof logic (Def 3.1(3) + Thm 3.3 need all trees to fail); the literal grammar is sloppier than the mathematics (READING NOTE) |
| degree ring | total degree $\le d$ over $\mathbb{F}_p$ in the outer variables $x$ ($\mathbb{F}_p^{\le d}[x]$, Sec 3); evaluation $\omega(g) = L(g^\rho)$ | degree $\le d$ over $\mathbb{F}_2$ | YES at $p = 2$ |

### 2.3 Why the p^{-dim^rho(P)} weighting IS the corpus's channel

On the true path of $\omega = (\rho, L)$, a queried single variable $x_{ij}$
contributes to $\dim^\rho(P)$ iff the pair is free: killed-matched gives
$x_{ij}^\rho = 1$ and answer $1$, so $(x_{ij} - 1)^\rho = 0$; killed-unmatched gives
$x_{ij}^\rho = 0$ and answer $0$; both add $0$ to $\dim$. A free pair adds the independent
condition $x_{ij} = L(x_{ij})$, increment $1$ ($x_{ij} - a \notin V(n,d)^\rho$: the
degree-$\le 1$ part of $V(2d,d)$ is spanned by the restricted row axioms; corpus
kernel finding [MV], consistent with the printed reading of $V(n,d)^\rho$ as the
degree-$\le d$ PC consequences of the restricted system). Hence

   $p^{-\dim^\rho(\text{true path})} = (1/p)^{(\#\text{ free pairs queried on it})}$ ,

which is exactly the corpus's answer-channel weight (each free single costs a
factor $1/p$, killed queries are free; F1 [MV]). So Lemma 5.1's $\mathrm{Error}(\rho)$ is
the corpus's simulated quantity, and the printed $(P_3)$ replaces the true
weights by the uniform $p^{-e'}$: it taxes every killed or determined query on a
$\chi$-good path by an extra factor $p$. That is the whole transfer gap.

## 3. The transfer

Notation: for a $(d,e')$-tree $T'$ (padded to uniform depth $e'$, as Lemma 5.2
assumes w.l.o.g.), define

   $\mathrm{err}(T') := \mathrm{Prob}_\omega[T'(\omega) \notin D^\rho \times R^\rho]$        $(P_2)$
   $\chi(T') := \mathrm{Prob}_{\rho,P}[\chi(P,\rho) = 1]$                     $(P_3)$
   $\mathrm{defect}(P,\rho) := e' - \dim^\rho(P) \ge 0$   (printed: $\dim^\rho(P) \le e'$)
   $\Delta(T') := \max\{\mathrm{defect}(P,\rho) : \chi(P,\rho) = 1\}$  ($0$ if no $\chi$-good path).

Proposition 1 (direction of the transfer; from printed identities). For every
$T'$,

   $\mathrm{err}(T') = \mathbb{E}_\rho[\, \sum_{P:\,\chi=1} p^{-e'}\, p^{\mathrm{defect}(P,\rho)}\, ]$
   $\chi(T') = \mathbb{E}_\rho[\, \sum_{P:\,\chi=1} p^{-e'}\, ]$
   $\mathrm{err}(T') \ge \chi(T')$  and  $\chi(T') \ge p^{-\Delta(T')}\,\mathrm{err}(T')$.

Proof. The first two lines are Lemma 5.1(i)-(ii) plus the printed padding
identity in the derivation of Lemma 5.2 (sum over paths, weight $p^{-e'}$). The
inequalities: $p^{\mathrm{defect}} \ge 1$ gives $\mathrm{err} \ge \chi$; $p^{\mathrm{defect}} \le p^{\Delta}$ on
$\chi$-good paths gives $\mathrm{err} \le p^{\Delta}\chi$. QED.

So the printed $\chi$-quantity is smaller than the corpus's failure, and the gap
is exactly $\exp(\ln(p)\,\Delta)$: a tree makes $\chi \ll \mathrm{err}$ by having its $\chi$-good
paths carry many killed/determined queries.

Theorem 2 (positive transfer; the form in which Corollary 3.1 feeds (3)).
Fix $p = 2$ and suppose the hypothesis of deg2_theory.md's Corollary 3.1 (full
adaptive degree-$\le 2$ class, budget $e = d \log k$, $2d^2 + 3d \le n$, $d^2 \log k =$
o(n)). Then every degree-$\le 2$ tree $T'$ at budget $e' \le c \cdot d \log k$ (any fixed $c$)
satisfies

   $\chi(T') \ge 2^{-\Delta(T')} \cdot (1/2 - o(1) - 2(1 - \exp(-d^2 \log k/(4n))))$
           $\ge 2^{-\Delta(T') - O(1)}$ ,

and in particular $\chi(T') \ge k^{-O(1)}$ HOLDS for every such tree with
$\Delta(T') \le C \cdot \log_2 k$ (any fixed $C$), which is the printed hypothesis (3)
for that tree. If $\Delta(T') = 0$ (all $\chi$-good paths fully informative,
$\dim^\rho(P) = e'$) then $\chi(T') = \mathrm{err}(T')$ EXACTLY and Corollary 3.1 transfers
verbatim. Proof: Proposition 1 with $\mathrm{err}(T') \ge 1/2 - o(1) - 2(1 -$
$\exp(-d^2 \log k/(4n))) \ge k^{-C'}$ from Corollary 3.1; the equality case is
defect $= 0$ on all $\chi$-good paths. QED.

Theorem 3 (negative; the printed (3) is violated by trivial trees). Let
$2 \le d \le n/4$ (the program's regime; $f = (2d+1)2d/((n+1)n) \le 1/2$). There is
a $(d, e')$-tree $T_0$ with $\mathrm{err}(T_0) = 1 - f \ge 1/2$ and

   $\chi(T_0) = (1 - f)\,p^{-e'} \le p^{-e'} = k^{-\Theta(d \ln p)}$

at the printed budget $e' = \Theta(d \log k)$. Hence for $d = \omega(1)$ and any
fixed $C$, $\chi(T_0) < k^{-C}$ for all large $k$: the printed hypothesis (3),
quantified over ALL $(d,e')$-trees, is FALSE at growing $d$.

Proof. $T_0$ queries $Q_1, \dots, Q_{e'}$ (the row polynomials of Sec 1, degree
$1 \le d$; the same query repeated also works), every leaf labeled $(1,1)$.
(i) Each $Q_i$ is a system polynomial, so $Q_i \in V(n,d)$ ($g = 1$ in the printed
span definition), so $Q_i^\rho \in V(n,d)^\rho$ and $L(Q_i^\rho) = 0$ for every
design $L$ (printed condition 2 of Def 3.1 satisfied by $\Omega(n,d)$; corpus F3
[MV]). On a path whose $i$-th answer is $a_i$, $W(P)^\rho$ contains
$(Q_i - a_i)^\rho = Q_i^\rho - a_i$; since $Q_i^\rho \in V(n,d)^\rho$, $\mathrm{Span}(W(P)^\rho)$
contains the constant $a_i$, and if some $a_i \neq 0$ then
$1 = a_i^{-1} \cdot a_i \in \mathrm{Span}(W(P)^\rho)$: $\chi = 0$. So the only $\chi$-eligible path
is the all-$0$ path. (ii) On it, $\chi = 1$ iff $(1,1) \notin D^\rho \times R^\rho$, an event
of probability $1 - f$ over uniform $\rho$ (corpus Prop A: a fixed pair is free
with probability exactly $f = (2d+1)2d/((n+1)n)$). Hence
$\chi(T_0) = (1 - f)\,p^{-e'}$. (iii) $\mathrm{err}(T_0) = 1 - f$: every $\omega$ follows the
all-$0$ path (all answers determined $0$), and the label is fixed. (iv)
$p^{-e'} = \exp(-e' \ln p)$ and $e' = \Theta(d \log k)$ gives $k^{-\Theta(d)}$. QED.

Two remarks on Theorem 3. (a) Padding sensitivity: the same collapse follows
from padding ALONE. Take any tree of height $e'' < e'$ and pad it to depth $e'$
by repeating the determined query $Q_1$: $\mathrm{err}$ is unchanged (determined queries
add nothing on $L$-sampled paths) while $\chi$ is multiplied by $2^{-(e'-e'')}$. So
even a hypothetically good tree fails (3) in a badly padded form, and the
universal quantifier includes padded forms. (b) The violated tree poses no
threat to the pseudo-solution: $\mathrm{err}(T_0) \ge 1/2$ means $T_0$ finds no conflict pair
with probability $\ge 1/2$, which is all that Definition 3.1 asks. The failure is
a defect of the printed $(P_3)$ formulation, not of $\Omega(n,d)$.

Theorem 4 (the reduction that works; $\mathrm{err}$-form, assembled from printed
pieces). Fix $p$, $l \ge 2$, $k = k(n)$, and put $d_0 = (\log k)^{O(l)}$ (the degree
bound of Theorem 2.2), $E = h + \log S + O(d_0 \log n)$ where $S = k^{O(1)}$ and
$h = O(\log S)$ are the ENS parameters of Theorem 2.2 applied to a hypothetical
$k$-step $F_l(\mathrm{MOD}_p)$-refutation, and let $\gamma = k^{-C}$ with $C$ large enough that
$\gamma \ge S^{-1}$. Suppose

   $\mathrm{err}(T') \ge \gamma$ for EVERY $(d_0, E)$-tree $T'$ with labels in $[n+1] \times [n]$

($\mathrm{err}$ in the printed Sec 5 sense, over $\omega \in \Omega(n,d)$, with
$2 \le d_0 \le n/2$ so that Definition 4.3 applies). Then $\neg\mathrm{PHP}_n$ admits no
$F_l(\mathrm{MOD}_p)$-refutation with $k$ steps.

Proof. Let $T$ be any $(d_0, e)$-tree over $S(n,d)$ with $e \le h + \log S$ (the budget
in Theorem 3.2's no-solution statement), of the conflict task (leaves labeled
by polynomial pairs). Lemma 4.4 (printed) gives a $(d_0, e')$-tree $T'$ with
$e' \le e + O(d_0 \log n) \le E$ such that, for every $\omega \in \Omega(n,d)$, if
$T(\omega)$ is a conflict pair for $\omega$ then $T'(\omega) \in D^\rho \times R^\rho$.
Hence $\mathrm{Prob}_\omega[T(\omega) \text{ is a conflict pair}] \le \mathrm{Prob}_\omega[T'(\omega)$
$\in D^\rho \times R^\rho] = 1 - \mathrm{err}(T') \le 1 - \gamma$, i.e. $\mathrm{Prob}_\omega[T(\omega)$ is NOT a
conflict pair for $\omega] \ge \gamma$. As $T$ was arbitrary, $\Omega(n,d)$ satisfies
Definition 3.1's condition 3 at parameters $(d_0, h + \log S, \gamma)$; conditions
1-2 hold (1: every $\omega \in \Omega(n,d)$ is $\mathbb{F}_p$-linear by construction; 2:
$\omega(fg) = L((fg)^\rho) = L(f^\rho g^\rho) = 0$ since $f^\rho$ lies in the span of
the restricted system, i.e. in $V(n,d)^\rho$, $\deg(f^\rho g^\rho) \le d_0$, and $L$
vanishes on $V(n,d)^\rho$: INFERENCE, one line from printed Definition 4.3 +
Corollary 4.2). So $\Omega(n,d)$ is a $(d_0, h + \log S, \gamma)$-solution. But a
$k$-step refutation yields via Theorem 2.2 an ENS-refutation with $S = k^{O(1)}$
extension polynomials, accuracy $h = O(\log S)$ minimal with $e^{h/p} \ge 2S^2$, and
degree $\le (\log k)^{O(l)}$, so Theorem 3.2 denies the existence of any
$(d_0, h + \log S, S^{-1})$-solution, and $\gamma \ge S^{-1}$ makes our solution one
of those. Contradiction. QED.

Honest bookkeeping for Theorem 4. (a) The quantifier "EVERY $(d_0, E)$-tree" is
the full printed tree class at degree $d_0 = (\log k)^{O(l)}$: the degree-$\le 2$ cap
(Corollary 3.1) proves the hypothesis only on the degree-2 SLICE of the
quantifier, which yields no lower bound by itself; the full conclusion needs
the degree-$d_0$ cap (O2's open core (i)). This theorem is recorded because it is
the route around the printed (3), which Theorem 3 blocks; every ingredient is
printed, the assembly is the only new step. (b) The constants $C$ and the
$O(d_0 \log n)$ slack are unprinted on both sides (same status as the corpus's
"constant room" comments).

Answer to task 3(b), precisely. The mismatch between the printed $\chi$-quantity
and the corpus's capped quantity has three components: (M1) naming: printed
conflict pairs are polynomial pairs, related to free pairs one-way by Lemma
4.4; (M2) sampling: $(P_3)$ samples paths uniformly while $(P_2)$ samples them by
the design measure, giving $(P_3) \le (P_2)$ with gap $\exp(\ln p \cdot \Delta(T'))$; (M3)
the $\mathrm{Span}$ conjunct, which only bites on the uniform-path side. The transfer in
the direction needed by Theorem 6.1 ((3) from the cap) cannot be closed in
general: Theorem 3 exhibits trees with $\mathrm{err} \ge 1/2$ and $\chi = k^{-\Theta(d)}$, so
NO strengthening of the $\mathrm{err}$-cap alone can prove (3) for all trees. What closes
the program instead is Theorem 4: run Definition 3.1 + Lemma 4.4 + Theorem
3.3 on the $\mathrm{err}$-form, which is exactly the quantity O2 states
("$\mathrm{Prob}_\omega[T(\omega) \text{ is not a conflict for } \omega] \ge k^{-C}$"). The only
usable sufficient condition that refers to $\chi$ is Theorem 2's defect bound
$\Delta(T') \le C \log_p k$, which trivial trees violate maximally.

## 4. Task-4 checks: budget quantifier, degree ring, subset relation

4.1 Budget quantifier. PRINTED, in Theorem 6.1: "$(d, e')$-tree $T'$ with
$d = (\log k)^{O(l)}$ and $e' = O(\log n) + O(d \log n) = d(\log k)$", and the
parenthetical "(For the estimate of $e'$ by $d(\log k)$ we use that $k \ge n^3/2$ ...)".
So yes: the printed budget is $(d, e')$ with $e' = O(\log n) + O(d \log n)$, and the
printed identification with $d \log k$ holds because $\log n \le \log k$ for
$k \ge n^{3/2} \ge n$ makes $O(\log n) \le O(d \log n) \le O(d \log k)$ for $d \ge 2$
(INFERENCE; the $O$-constants are not printed, so the corpus's $e = d \log k$
matches $e'$ up to an unknown constant factor; boundary statements of the shape
$d^2 \log k = o(n)$ are constant-insensitive, the falsifiable numeric predictions
are not).

4.2 Degree bound. The printed tree queries polynomials of total degree $\le d$
over $\mathbb{F}_p$ in the OUTER variables $x = \{x_{ij}\}$ ($\mathbb{F}_p^{\le d}[x]$, defined at the start
of Sec 3), evaluated by $\omega(g) = L(g^\rho)$. At $p = 2$ this is the corpus's
query model. Definition 4.3 requires $2 \le d \le n/2$ (so $n_\rho = 2d \ge 4$ and the
restricted system is $\neg\mathrm{PHP}$ on $(2d+1) \times 2d$, matching the corpus pipeline).

4.3 Is Theorem 3's degree-$\le 2$ class a subset of the printed class at $d = 2$?
YES: single variables $x_{ij}$ (degree 1), degree-2 monomials $x_{ij} x_{kl}$ (degree
2), linear forms $\sum a_{ij} x_{ij} + a_0$ (degree 1), squares and constants, are
all elements of $\mathbb{F}_2^{\le 2}[x]$, adaptive trees of height $\le e'$ are $(2, e')$-
trees in the printed sense. The subset is PROPER as stated: the printed class
at $d = 2$ also contains arbitrary $\mathbb{F}_2$-mixtures of variables and degree-2
monomials (e.g. $x_{11} + x_{23} x_{34}$), which deg2_theory.md's Theorem 3 does not
list among its covered query types ("single-variable queries, degree-2
monomial queries, and linear forms"). INFERENCE on the likely repair, not
proved in the corpus: on the block-free event (Lemma REL) every free single
and free diagonal coordinate is an independent fair coin, so any mixture query
answers a fair coin as soon as its free support is nonempty, and its killed
part is a linear-form-type channel; the K-certificate and q-cap bookkeeping
should absorb mixtures. Until that is written down, Corollary 3.1 covers a
proper subclass of the printed degree-2 quantifier.

## 5. Consequences for the corpus

1. O2's stated quantity is the $(P_1)/(P_2)$ $\mathrm{err}$-form and is the RIGHT living
   form; the cap (Corollary 3.1) closes the reduction through Theorem 4's
   route, not through printed (3).
2. O2's open core (iii) (the $\chi$-transfer, "unchecked") is now checked,
   NEGATIVELY in the direction Theorem 6.1 needs: $(P_3) \le (P_2)$, gap
   $\exp(\ln p \cdot \Delta)$, and (3) is falsified by trivial trees at growing $d$ [under the corpus's quantifier reading - INFERENCE; downgraded per GUIDANCE 2026-10-04: the printed (3) is a hypothesis about the paper's own constructed tree, not a paper claim]
   (Theorem 3). The parenthetical in O2 ("Whether Definition 3.1's printed
   quantifier is budgeted is a reading check against the paper") is settled:
   BUDGETED, $e$ is a printed parameter (Sec 1.2 above).
3. The "reading is verified in proof_complexity.md" claim for O2 is correct
   about the tree quantifier and the budget, but the quantity named there is
   $(P_1)$, not the printed (3); proof_complexity.md's line "$\chi(P, \rho) = 1$ iff
   $\mathrm{lab}(P) \notin D^\rho \times R^\rho$ AND $1 \notin \mathrm{Span}(W(P)^\rho)$" is accurate; the
   missing piece was that (3) samples $P$ uniformly over paths, which no corpus
   quantity does.
4. All corpus measurements (two-phase 0.97, $K_j$ 0.9692, cap band 0.32 at
   $(128,2)$, $e = 32$) are $L$-sampled, hence evidence about $(P_2)$. They neither
   support nor endanger $(P_3)$; by Theorem 3, $(P_3)$-style quantities are
   padding-dominated and arguably not worth measuring.
5. The degree-2 slice of Theorem 4's hypothesis is exactly what Corollary 3.1
   proves (modulo its two JDP steps and the mixture-query gap of 4.3): so the
   budgeted $\chi$-hypothesis is proved-alive at degree $\le 2$ in the ERR sense,
   and in the printed (3) sense for defect-bounded trees (Theorem 2); the
   printed (3) sense for ALL trees is dead (Theorem 3).

## 6. Falsifiable toy-scale prediction (exact, no simulation needed)

At $(n, d) = (32, 2)$, $p = 2$: $f = 20/1056$, and for the trivial tree $T_0$ of
height $e' = 16$: $\mathrm{err}(T_0) = 1 - f = 1036/1056 = 0.9811$ and
$\chi(T_0) = (1036/1056)\,2^{-16} = 1.4979 \times 10^{-5}$. Both are exact theorems here; a
kernel-harness check would consist of (a) confirming $1 \notin V(2d,2) +$
$\mathrm{span}\{Q_i - a\}$ iff $a = 0$ (rank check on $V(4,2)$, 165-dim inside 231-dim
[corpus MV]), and (b) confirming the fixed-pair freeness mass $f$ by sampling
$\rho$. Any deviation falsifies the pipeline implementation, not this analysis.

## 7. Verdict (one paragraph)

The printed text gives three distinct probabilities where the corpus had one
informal $\chi$: the Definition 3.1 solution condition (polynomial-pair
conflicts, $\omega$-sampled, budgeted), the Sec 5 error of the reduced tree (the
corpus's failure, design-sampled), and Theorem 6.1's (3) (uniform-path,
$\mathrm{Span}$-conjunct). Lemma 5.2 makes (3) a LOWER bound on the corpus's failure, so
the cap transfers to (3) only with a defect bound (Theorem 2: factor
$2^{-\Delta}$), and (3) itself is falsified [under the corpus's quantifier reading - INFERENCE; downgraded per GUIDANCE 2026-10-04] by a trivial determined-query tree at
growing $d$ (Theorem 3: $\chi = (1-f)\,2^{-e'} = k^{-\Theta(d)}$ while $\mathrm{err} \ge 1/2$),
including via malicious padding. The budgeted $\chi$-hypothesis of the program is
therefore alive exactly in the $\mathrm{err}$-form O2 states, and the lower-bound route
should be assembled as in Theorem 4 (Definition 3.1 + Lemma 4.4 + Theorems
2.2/3.2/3.3), with the degree-2 slice of its hypothesis supplied by
Corollary 3.1 and the full degree-$d_0$ quantifier remaining O2's open core (i).
The paper's closing hope that (3) holds with $\Omega(1)$ appears to overlook the
determined-query/padding collapse; a note to the author along the lines of
note_to_author.md's discipline is the natural follow-up.

## CORRECTION (2026-10-04, err-form-route agent): Theorem 4's constant matching

Theorem 4 above ("gamma = k^{-C} with C large enough that gamma >= S^{-1}") has
the constant direction wrong, and matching to Theorem 3.2's threshold S'^{-1}
would need an unprinted lower bound on S'. The corrected assembly is Theorem R
of err_form_route.md: pad the extension-polynomial count up to
S^* = k^{c_S + C} (Lemma P, proved there) and re-run Theorem 2.2 at accuracy
h^* tuned to S^* (Theorem 2.2 takes any h >= 1). The route then closes
unconditionally for every fixed C. Theorem 4's structure and quantity (P2) are
unchanged; only the constant bookkeeping is superseded. A REFINEMENT also
landed: Def 3.1 condition 2 is proved via (fg)^rho in V(n,d0)^rho (unrestricted
closure, printed Theorem 4.1(2)), not via closure of V(n,d)^rho under
multiplication (not printed). Use err_form_route.md Theorem R as the route of
record.
