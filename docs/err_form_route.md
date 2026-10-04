# The err-form route: the complete conditional proof assembled from printed
# pieces of arXiv:2609.35927

Result of the theory agent (2026-10-04). Status: proof document, conditional on
one stated premise (the all-degrees budgeted err-floor, O2); not peer-reviewed.
Source: https://arxiv.org/html/2609.35927 (v2, 30 Sep 2026), re-fetched this
session (251,655 bytes HTML, LaTeXML, byte-identical to the fetch recorded in
chi_transfer.md), converted and re-verified against the raw math alttext.

This document expands chi_transfer.md Theorem 4 (the err-form assembly) from a
proof sketch into a complete, self-contained proof. Three things are new
relative to that sketch, all bookkeeping rather than mathematics:
1. The threshold matching between the route's floor value
   $\gamma = k^{-C}$ and Theorem 3.2's denial threshold $S^{-1}$ is repaired.
   chi_transfer.md's phrasing "C large enough that $\gamma \ge S^{-1}$" does not
   arrange the inequality by itself; Section 4 Step 3 does, via an ENS padding
   observation (Lemma P) and the free accuracy parameter of printed Theorem 2.2.
   Marked [CORRECTION to chi_transfer.md].
2. Definition 3.1's condition 2 is proved through $(fg)^\rho = f^\rho g^\rho$
   in $V(n,d_0)^\rho$ (Step 4), not through closure of $V(n,d)^\rho$ under
   multiplication, which is not printed. Marked [REFINEMENT of chi_transfer.md].
3. Every printed ingredient is quoted verbatim, including Theorem 2.2,
   Definition 2.1, Theorem 4.1 and Corollary 4.2, which chi_transfer.md cited
   only in paraphrase.

Marks: [PRINTED] quoted from the source (quotes normalized to corpus ASCII
math, chi_transfer.md convention); [ASSEMBLY] a lemma not printed in the paper
but immediate from printed definitions, proved here in full; [READING NOTE] /
[INFERENCE] flagged interpretation; [MV] corpus machine-verified. No corpus
file other than this one was edited; LOG.md was not touched.

## 1. Scope: what is proved here and what is not

Theorem R below is a conditional. Premise (A) is the err-floor of
open_problems.md O2, the corpus's open core. Conclusion (C) is the printed
conclusion of Theorem 6.1 of arXiv:2609.35927, quoted verbatim.
Nothing in this document proves (A).
The value of the document: (A) is shown to be EXACTLY sufficient for (C), with
every quantifier, constant, budget, and regime condition surfaced, and with the
printed $\chi$-quantity of Theorem 6.1(3) appearing nowhere in the proof.
All quantitative constants are carried explicitly, because the printed
statements carry implied constants whose values the paper does not print; the
route theorem says precisely how they must be fixed.

## 2. Notation (set up once)

### 2.1 The system and the proof systems

Fix a prime $p$ (the paper's convention: "we fix an arbitrary prime p for the
rest of the paper") and, throughout, a constant $\ell \ge 2$.
Variables $x_{ij}$, $i \in [n+1]$, $j \in [n]$. The system $\neg\mathrm{PHP}_n$
consists of the left-hand sides of:

    x_{i1 j} * x_{i2 j} = 0   for each i1 != i2 in [n+1], j in [n]
    x_{i j1} * x_{i j2} = 0   for each i in [n+1], j1 != j2 in [n]
    1 - sum_{j in [n]} x_{ij} = 0   for each i in [n+1]
    x_{ij}^2 - x_{ij}   for all i in [n+1], j in [n]

[PRINTED, Sec 1, bullets and naming:] "Denote the left-hand sides of the
equations in the first three items as $Q_{i_1,i_2;j}$, $Q_{i;j_1,j_2}$ and
$Q_i$, respectively, and let $\neg\mathrm{PHP}_n$ be the set of all these
polynomials together with all $x_{ij}^2 - x_{ij}$."
So $\neg\mathrm{PHP}_n$ contains the three axiom families (degrees $2, 2, 1$)
and the Boolean axioms (degree $2$); every $f \in \neg\mathrm{PHP}_n$ has
$\deg f \le 2$.
$F_\ell(\mathrm{MOD}_p)$ is depth-$\ell$ Frege with $\mathrm{MOD}_p$ connectives
[PRINTED, Sec 1]; a "$k$-step refutation" of $\neg\mathrm{PHP}_n$ is a refutation
with $k$ inference steps.
ENS is the Extended Nullstellensatz system [PRINTED, Sec 2, Definition 2.1 and
the sentence after it:] "An ENS-refutation of $\mathcal{F}$ consists of a triple
$(h, \mathcal{E}, L)$, where $h \ge 1$ is its accuracy, $\mathcal{E}$ is a set
satisfying Definition 2.1 and $L$ is an NS-refutation of
$\mathcal{F} \cup \mathcal{E} \cup \mathcal{R}(\mathcal{E})$. Its degree is the
degree of $L$."
$\mathcal{R}(\mathcal{E})$ is the set of polynomials $r^p - r$ for extension
variables $r$ occurring in $\mathcal{E}$ [PRINTED, Definition 2.1, item 3].
An NS-refutation of a set $G$ is a tuple $(h_g)_{g \in G}$ with
$\sum_{g \in G} h_g \cdot g = 1$; its degree is $\max_g \deg(h_g g)$
[PRINTED, Sec 2].

### 2.2 Polynomial spaces, Razborov's theorem, designs

[PRINTED, Sec 4:] "To avoid a baroque notation put

    S(n,d) := F_p^{\le d}[Var(\neg\mathrm{PHP}_n)]

and define an $\mathbb{F}_p$-vector subspace $V(n,d)$ of $S(n,d)$ to be

    V(n,d) := Span[\{gf | f \in \neg\mathrm{PHP}_n and deg(fg) \le d\}] ."

So $S(n,d)$ is the full space of polynomials of degree at most $d$ in the
system's variables; Sec 3's notation $\mathbb{F}_p^{\le d}[x]$ denotes the same
space and we use $S(n,d)$ throughout.
[PRINTED, Sec 4, Theorem 4.1 ([12], Razborov):] "For $2 \le d \le n/2$ it holds:
1. $1 \notin V(n,d)$, 2. for any $g \in V(n,d)$ and $h \in S(n,d)$:
$\deg(gh) \le d \rightarrow gh \in V(n,d)$."
[PRINTED, Sec 4, Corollary 4.2:] "For $2 \le d \le n/2$ there are maps
$L : S(n,d) \rightarrow \mathbb{F}_p$ satisfying the first two conditions of
Definition 3.1: $L$ is $\mathbb{F}_p$-linear, $L(1) = 1$ and vanishes on
$V(n,d)$." Followed by: "Maps satisfying the conditions in the corollary are
usually called designs in proof complexity (cf. [7]) and we shall denote their
set by ${\sf Des}(n,d)$."

### 2.3 Restrictions

For a partial injective $\rho :\subseteq [n+1] \to [n]$, the restriction $g^\rho$
substitutes the printed 0/1 values for killed variables; $x_{ij}^\rho = x_{ij}$
survives exactly on free cells [PRINTED, Sec 4:] "Note that
$x_{ij}^\rho = x_{ij}$ iff $(i,j) \in D^\rho \times R^\rho$", where
"$D^\rho := [n+1] \setminus \mathrm{dom}(\rho)$,
$R^\rho := [n] \setminus \mathrm{rng}(\rho)$ and
$n_\rho := |R^\rho| (= n - |\rho|)$".
For a set $A \subseteq S(n,d)$: $A^\rho := \{g^\rho \mid g \in A\}$ [PRINTED].
[PRINTED, Sec 4, the homomorphism paragraph:] "Substitution $\rho$ is a
homomorphism of vector space $S(n,d)$ to $S(n,d)$ preserving multiplication when
defined. The restricted system $(\neg\mathrm{PHP}_n)^\rho$ represents the
negation of the PHP principle where pigeons and holes are taken from $D^\rho$
and $R^\rho$, respectively, and $S(n,d)^\rho$ is isomorphic to $S(n_\rho,d)$.
Similarly, $V(n,d)^\rho$ is the set of polynomials with a degree $\le d$ PC
derivation from $(\neg\mathrm{PHP}_n)^\rho$."
The restricted rectangle carries $(2d+1)$ pigeons against $2d$ holes when
$n_\rho = 2d$.
[PRINTED, Sec 4:] "We shall denote by ${\sf Des}(n,d)^\rho$ the set of degree
$d$ designs on $S(n,d)^\rho$, to keep a consistent notation when talking about a
restriction."
[READING NOTE, used once in Step 4: a design on $S(n,d)^\rho$ is a map
$L : S(n,d)^\rho \to \mathbb{F}_p$ that is $\mathbb{F}_p$-linear, satisfies
$L(1) = 1$, and vanishes on $V(n,d)^\rho$; this is Corollary 4.2's design
definition transported through the printed "consistent notation" sentence, and
it is confirmed by Sec 5's use ("Given $\rho$ such $L$ exists iff
$1 \notin \mathrm{Span}(W(P)^\rho)$", where $L$ must vanish on $V(n,d)^\rho \cup
A(P)^\rho$).]

### 2.4 Trees, conflict pairs, free pairs

[PRINTED, Sec 3:] "An $\mathbb{F}_p^{\le d}[x]$-tree $T$ is a finite $p$-ary
tree whose each non-leaf vertex is labeled by a query $g = $ ? for some
polynomial $g \in \mathbb{F}_p^{\le d}[x]$ and the $p$ outgoing edges are
labeled by $g = a$, for all $a \in \mathbb{F}_p$. The leaves of $T$ are labeled
by elements of some non-empty set $I$. The height of $T$ is the maximum number
of edges on a path from the root to a leaf. $\mathbb{F}_p^{\le d}[x]$-trees of
height $\le e$ are called $(d,e)$-trees."
A map $\omega : S(n,d) \to \mathbb{F}_p$ defines a path by answering queries;
$T(\omega)$ is the leaf label on that path [PRINTED, Sec 3].
[PRINTED, Sec 3:] "If $\omega$ is a linear map but not a homomorphism there must
be a conflict pair: a pair of polynomials $g, g' \in \mathbb{F}_p^{\le d}[x]$,
such that $\deg(gg') \le d$ and

    \omega(g) * \omega(g') \neq \omega(gg') ."

So a printed conflict pair is a pair of POLYNOMIALS.
A pair $(i,j) \in D^\rho \times R^\rho$ (a free cell, called a free pair in the
corpus) is a different object; Lemma 4.4 maps one to the other one-way
[chi_transfer.md Sec 2.2, dictionary row 1].
Two labeled classes are kept apart throughout:
- conflict-task trees: leaves labeled by polynomial pairs (the objects in
  Definition 3.1's condition 3, after the ill-typing repair below);
- reduced trees: leaves labeled in $[n+1] \times [n]$ (the objects of Sec 5).
[READING NOTE, ill-typing:] Definition 3.1 allows leaf labels in "some non-empty
set $I$", but its condition 3 speaks of "$T(\omega)$ is not a conflict pair for
$\omega$", which is well-formed only when the labels are polynomial pairs. The
quantifier in condition 3 is therefore read over conflict-task trees. The same
reading is forced by Theorem 3.2, whose proof (the paper's, quoted in Sec 4
Step 2 below) uses condition 3 exactly on conflict-task trees.

### 2.5 The pipeline $\Omega(n,d)$

[PRINTED, Sec 4, Definition 4.3 ([8, Def.4.2]):] "For $2 \le d \le n/2$ let
$\Omega(n,d)$ be the set of all maps $\omega \in {\sf Des}(n,d)$ that are
defined as follows: 1. Pick (a) a restriction
$\rho :\subseteq [n+1] \to [n]$ with $n_\rho = 2d$, (b) a map
$L \in {\sf Des}(n,d)^\rho$. 2. For $g \in S(n,d)$ put:
$\omega(g) := L(g^\rho)$."
And [PRINTED, Sec 4:] "Note that Corollary 4.2 implies that
$\Omega(n,d) \neq \emptyset$."
We write $\omega = (\rho_\omega, L_\omega)$ [PRINTED: "We shall write
$\omega = (\rho_\omega, L_\omega)$"].
For Lemma 5.1's sampling, $\omega$ is drawn uniformly from $\Omega(n,d)$.
[INFERENCE, inherited from chi_transfer.md Sec 2.2: uniform over the set means
uniform over pairs $(\rho, L)$, which is well-defined because
$|{\sf Des}(n,d)^\rho| = |{\sf Des}(2d,d)|$ is independent of $\rho$ by the
printed isomorphism $S(n,d)^\rho \simeq S(n_\rho,d)$.]
[READING NOTE: ${\sf Res}(n,d)$ is used in Lemmas 5.1, 5.2 and Theorem 6.1 but
never defined in the paper (with the typo ${\sf Res}(d,n)$ in the Lemma 5.2
derivation); the working reading, from context and Definition 4.3(1a), is
${\sf Res}(n,d) = \{$partial injective $\rho :\subseteq [n+1] \to [n] : n_\rho
= 2d\}$.]

### 2.6 The err quantity (the route's quantity) and the chi quantity (not used)

[PRINTED, Sec 5, opening:] "Let $T'$ be a $(d,e')$-tree with labels in
$[n+1] \times [n]$. Our aim in this section is to express the error $T'$ must
make on $\Omega(n,d)$ in terms of restrictions only. The phrase $T'$ errs on
$\omega = (\rho,L)$ means that $T'(\omega) \notin D^\rho \times R^\rho$."
Definition (corpus shorthand for the printed quantity, chi_transfer.md Sec 3):

    err(T') := Prob_{\omega in Omega(n,d)}[ T' errs on \omega ]

with $\omega$ uniform in $\Omega(n,d)$. This is chi_transfer.md's $(P_2)$, the
corpus's failure quantity; $1 - \mathrm{err}(T')$ is the probability that $T'$
outputs a free pair.
For contrast, the printed $\chi$-quantity of Theorem 6.1(3) is $(P_3)$:
$\mathrm{Prob}_{\rho,P}[\chi(P,\rho) = 1]$ with $\rho$ uniform over
${\sf Res}(n,d)$, $P$ uniform over the paths of the depth-padded tree, and
[PRINTED, Sec 5, display (2):] "$\mathrm{lab}(P) \notin D^\rho \times R^\rho$
and $1 \notin \mathrm{Span}(W(P)^\rho)$", where
$W(P) := {\sf Span}(V(n,d) \cup A(P))$ and $A(P)$ collects the query-answer
forms $g - a$ along $P$.
$(P_3)$ samples paths uniformly and carries the $\mathrm{Span}$ conjunct; it is
a different, smaller quantity than $(P_2)$ (chi_transfer.md Sec 2.1, 3).
Theorem R uses only $(P_2)$; $(P_3)$, $\chi(P,\rho)$, $\dim^\rho(P)$,
$\mathrm{Error}(\rho)$, Lemma 5.1 and Lemma 5.2 appear nowhere in its proof.
[READING NOTE: $\log$ in the paper is immaterial to base choice up to constant
factors; constants below are stated so that no base convention matters.]
[READING NOTE, "over $S(n,d)$": Lemma 4.4's hypothesis "Let $T$ be a $(d,e)$-tree
over $S(n,d)$" means the queries are polynomials from $S(n,d)$; since Sec 3's
$\mathbb{F}_p^{\le d}[x]$ equals $S(n,d)$, Definition 3.1's tree quantifier and
Lemma 4.4's hypothesis range over the same class.]

## 3. The route theorem

Fix, once and for all: the prime $p$; the constant $\ell \ge 2$; and the
absolute constants $c_S, c_d$ guaranteed by printed Theorem 2.2 (their existence
is the printed sentence after Theorem 2.2, quoted in Step 2) and $c_{44}$
guaranteed by printed Lemma 4.4's bound $e' \le e + O(d \log n)$ (its implied
constant, fixed once). Fix the route constant $C \ge 1$ and define, for each $n$
and each $k = k(n) \ge 2$:

    S* := k^{c_S + C}
    h* := the least integer h >= 1 with e^{h/p} >= 2 (S*)^2
    d_0 := ceil( (2 + \log k) (h* + 1)^{c_d \ell} )
    e* := ceil( h* + \log S* )
    E  := e* + c_{44} d_0 \log n
    gamma := k^{-C}

(The definitions of $S^*, h^*$ are exactly the paper's own choices in its proof
of Theorem 3.3, quoted in Step 2, up to the padding of $S$ in Lemma P; the
definitions of $d_0, e^*, E, \gamma$ are the route's. Note
$h^* = O(\log S^*) = O(\log k)$, hence $d_0 = (\log k)^{O(\ell)}$, and
$S^{*-1} = k^{-(c_S + C)} \le k^{-C} = \gamma$. The ceiling in $e^*$ keeps
tree heights integral, and $e^* \ge h^* + \log S^*$ is what Step 6 needs.)

Theorem R (err-form route). Fix $p$, $\ell \ge 2$, $C \ge 1$ and the constants
$c_S, c_d, c_{44}$ as above. Assume, for all sufficiently large $n$:
(A) [the err-floor premise; the $(P_2)$-form of O2] for $k = k(n)$ satisfying
(B1) and (B2) below, every $(d_0, E)$-tree $T'$ with labels in $[n+1] \times
[n]$ satisfies $\mathrm{err}(T') \ge \gamma$, where err is Sec 5's printed
quantity over $\omega \in \Omega(n,d_0)$;
(B1) [budget regime, printed] $k(n) \ge n^3/2$ (printed parenthetical of
Theorem 6.1, quoted in Sec 5 below);
(B2) [pipeline regime, printed] $2 \le d_0 \le n/2$, so that Definition 4.3
defines $\Omega(n,d_0)$ (the lower inequality is automatic for large $k$; the
upper is a genuine constraint on the pair $(k(n), \ell)$).
Then the printed conclusion of Theorem 6.1 holds: [PRINTED, Sec 6:] "Then for
all $n \gg 1$ any $F_\ell(\mathrm{MOD}_p)$-refutation of $\neg\mathrm{PHP}_n$
requires at least $k(n)$ steps."

Remarks on the hypotheses.
1. (A) quantifies over the FULL printed tree class at degree $d_0$ and budget
$E$. Slice results (degree $\le 2$, degree $\le 3$) do not feed it, because
$d_0$ grows; see Sec 6.
2. No hypothesis involves $\chi(P,\rho)$, the $\mathrm{Span}$ conjunct, uniform
path sampling, or Lemma 5.2. The printed (3) is not assumed and not concluded.
3. The value $C$ is arbitrary but fixed. Larger $C$ weakens (A) (smaller floor)
and is harmless below: the route closes for every fixed $C$.
4. If one prefers the conflict-task floor (the $(P_1)$-form), Lemma 4.4 converts
a $(P_1)$-floor at budget $e$ into the $(P_2)$-floor (A) only in one direction
and with budget slack, so (A) in $(P_2)$-form is the form of record; see Sec 6,
checklist entry 1.

## 4. The proof of Theorem R

### Step 0: setup and non-emptiness

Work at one value of $n$ satisfying (B1), (B2), with $k = k(n)$, and the
constants of Sec 3. By (B2) and the printed note
"Corollary 4.2 implies that $\Omega(n,d_0) \neq \emptyset$", $\Omega(n,d_0)$ is
a non-empty set; it is finite (finitely many pairs $(\rho, L)$), as Definition
3.1 requires. Every $\omega \in \Omega(n,d_0)$ is a map
$S(n,d_0) \to \mathbb{F}_p$, i.e. a map
$\mathbb{F}_p^{\le d_0}[x] \to \mathbb{F}_p$, the domain Definition 3.1 names.

### Step 1: the contradiction assumption

Assume, for contradiction, that $\neg\mathrm{PHP}_n$ admits an
$F_\ell(\mathrm{MOD}_p)$-refutation with $k$ steps. (The ENS-refutation
existence that Theorem 3.2's premise needs is thus carried as an explicit
assumption of the proof by contradiction; it is discharged in Steps 2 and 3 by
the printed Theorem 2.2.)

### Step 2: printed Theorem 2.2 at accuracy $h^*$

[PRINTED, Sec 2, Theorem 2.2 ([3, Thm.6.7(1)]):] "For any constant
$\ell \ge 2$, any parameter $h \ge 1$ and any $n \ge 1$: if
$\neg\mathrm{PHP}_n$ has an $F_\ell(\mathrm{MOD}_p)$-refutation with $k$ steps
then there is an ENS-refutation of $\neg\mathrm{PHP}_n$ with $S = k^{O(1)}$
number of extension polynomials stratified into $\ell + O(1)$ levels, accuracy
$h$ and of degree

    d \leq (2 + \log k)(h + 1)^{O(\ell)} .

The constants implicit in the O-notation depend only on F and p ."
Fix $c_S, c_d$ so that $S \le k^{c_S}$ and
$d \le (2 + \log k)(h+1)^{c_d \ell}$ hold for every $k$-step refutation and
every accuracy parameter $h \ge 1$; the printed sentence makes both constants
absolute (independent of $n$, $k$, $h$).
[READING NOTE, used here once: the printed sentence is read as covering all
three O-occurrences of Theorem 2.2, in particular the constant in $S = k^{O(1)}$
does not deteriorate with the chosen accuracy $h$; without this reading the
$h^*$-choice below could not bound $S$ in advance.]
Apply Theorem 2.2 with accuracy parameter $h := h^*$ (legitimate: $h^* \ge 1$).
We obtain an ENS-refutation $T_2 = (h^*, \mathcal{E}, L)$ of
$\neg\mathrm{PHP}_n$ with: accuracy $h^*$; $|\mathcal{E}| = S' \le k^{c_S} \le
S^*$ extension polynomials, stratified into $\ell + O(1)$ levels; and degree
$d' \le (2 + \log k)(h^*+1)^{c_d \ell} \le d_0$.
The $h^*$-choice is the paper's own [PRINTED, Sec 3, proof of Theorem 3.3:]
"Choosing the accuracy $h$ minimal such that $e^{h/p} \ge 2S^2$, i.e.
$h = O(\log S)$"; here it is applied to the padded count $S^*$ (Lemma P below)
rather than to $S'$, which enlarges $h^*$ by the additive term
$2 p (c_S + C) \ln k$ with absolute constant factor and keeps
$h^* = O(\log k)$.

### Step 3: ENS padding, then the denial of Theorem 3.2

Lemma P (ENS padding). [ASSEMBLY, from printed Definition 2.1.]
From any ENS-refutation $(h, \mathcal{E}, L)$ of $\mathcal{F}$ and any integer
$S'' \ge |\mathcal{E}|$ one obtains an ENS-refutation
$(h, \mathcal{E}'', L'')$ of $\mathcal{F}$ with $|\mathcal{E}''| = S''$, the
same accuracy $h$ and the same degree.
Proof. Choose $S'' - |\mathcal{E}|$ fresh tuples of polynomials $g$ and fresh
extension variables $r_{uj}$, all new and not occurring in
$\mathcal{F} \cup \mathcal{E}$; form their extension polynomials
$E_{i,g} = g_i \cdot \prod_{u \le h} (1 - \sum_j r_{uj} g_j)$ at accuracy $h$
[printed display (1)], and add them as one additional level, which satisfies
Definition 2.1's stratification clauses (companion polynomials together; the
new $g_j$'s variables and new $r_{uj}$'s occur nowhere else). Extend
$\mathcal{R}$ by the new $r^p - r$. Define $L''$ from $L$ by the same nonzero
coefficients on the old polynomials and coefficient $0$ on every new polynomial
of $\mathcal{F} \cup \mathcal{E}'' \cup \mathcal{R}(\mathcal{E}'')$; the printed
identity $\sum_g h_g g = 1$ is unchanged, so $L''$ is an NS-refutation with the
same degree ($L$'s degree, by the printed "Its degree is the degree of $L$").
QED
Apply Lemma P with $S'' := S^*$ to the Step 2 refutation: there is an
ENS-refutation of $\neg\mathrm{PHP}_n$ with exactly $S^*$ extension polynomials,
accuracy $h^*$, stratified into $\ell + O(1) + 1$ levels, of degree
$d'' \le d_0$ (unchanged by padding).
Now quote the denial tool. [PRINTED, Sec 3, Theorem 3.2 ([8, Thm.3.2]):]
"Assume that there exists an ENS-refutation of $\mathcal{F}$ with $S$ extension
polynomials, of degree $d$ and accuracy $h$ satisfying $e^{h/p} \ge 2S^2$. Then
there is no $(d, h + \log S, S^{-1})$-solution of $\mathcal{F}_n$."
Its premise holds for the padded refutation: $e^{h^*/p} \ge 2 (S^*)^2$ by the
definition of $h^*$ in Sec 3. Its conclusion, with
$\mathcal{F}_n := \neg\mathrm{PHP}_n$ (the specialization the paper itself
makes in its proof of Theorem 3.3, quoted in Step 7), gives:

    no (d'', h* + log S*, (S*)^{-1})-solution of \negPHP_n,
    where d'' \le d_0 is the padded refutation's degree.
    (*)

The paper's own two-line summary of Steps 2-3 is [PRINTED, Sec 3, proof of
Theorem 3.3:] "If we start with an $F_\ell(\mathrm{MOD}_p)$-refutation of
$\neg\mathrm{PHP}_n$ with $k$ steps, Theorem 2.2 gives us an ENS-refutation
with: $S = k^{O(1)}$, $\ell + O(1)$ levels and degree
$d \le (2 + \log k)(h+1)^{O(\ell)}$. Choosing the accuracy $h$ minimal such
that $e^{h/p} \ge 2S^2$, i.e. $h = O(\log S)$, gives the bound to the degree

    d \leq (\log k)^{O(\ell)} .

Theorem 3.2 then implies that there is no
$((\log k)^{O(\ell)}, O(\log k), k^{-O(1)})$-solution of
$\neg\mathrm{PHP}_n$."
[CORRECTION to chi_transfer.md: the route cannot take the denial threshold
$S^{-1}$ with the unpadded $S' $, because (A)'s floor $\gamma = k^{-C}$ would
then need $\gamma \ge S'^{-1}$, i.e. $k^C \le S'$, a lower bound on $S'$ that
nothing printed provides; and chi_transfer.md's "C large enough that
$\gamma \ge S^{-1}$" points the constant the wrong way (larger $C$ shrinks
$\gamma$). Lemma P removes the issue: the route pads $S'$ up to
$S^* = k^{c_S + C} \ge k^C$, so $(S^*)^{-1} \le \gamma$ holds unconditionally,
and the accuracy $h^*$ is chosen for $S^*$, as printed Theorem 2.2 allows any
$h \ge 1$.]

### Step 4: $\Omega(n,d_0)$ satisfies conditions 1 and 2 of Definition 3.1

[PRINTED, Sec 3, Definition 3.1 ([8]):] "For any $d, e \ge 0$ and
$1 \ge \gamma \ge 0$, a $(d,e,\gamma)$-solution of $\mathcal{F}$ is a non-empty
finite set $\Omega$ of maps

    \omega : F_p^{\le d}[x] \rightarrow F_p

satisfying the following three conditions:
1. $\omega$ is $\mathbb{F}_p$-linear map: $\omega(a) = a$ and
$\omega(g) + \omega(h) = \omega(g+h)$, for all $a \in \mathbb{F}_p$ and all
$g, h \in \mathbb{F}_p^{\le d}[x]$.
2. For any two polynomials $f \in \mathcal{F}$ and
$g \in \mathbb{F}_p^{\le d}[x]$ it holds that $\omega(fg) = 0$, assuming
$\deg(fg) \le d$.
3. For any $(d,e)$-tree $T$:

    Prob_{\omega \in \Omega}[T(\omega) is **not** a conflict pair for \omega]
    \ge \gamma .

A pseudo-solution is a collective name for $(d,e,\gamma)$-solutions."
Condition 1 for $\Omega(n,d_0)$. Fix $\omega = (\rho, L) \in \Omega(n,d_0)$.
For $a \in \mathbb{F}_p$:
$\omega(a) = L(a^\rho) = L(a \cdot 1) = a\, L(1) = a$, since constants are
fixed by $\rho$ and $L(1) = 1$ (Sec 2.3 READING NOTE).
For $g, h \in S(n,d_0)$:
$\omega(g+h) = L((g+h)^\rho) = L(g^\rho + h^\rho) = L(g^\rho) + L(h^\rho)
= \omega(g) + \omega(h)$, using linearity of $\rho$ (printed homomorphism
sentence) and of $L$. So condition 1 holds.
Condition 2 for $\Omega(n,d_0)$. Fix $f \in \neg\mathrm{PHP}_n$ and
$g \in S(n,d_0)$ with $\deg(fg) \le d_0$.
First, $f \in V(n,d_0)$: write $f = 1 \cdot f$ in the printed definition of
$V(n,d_0)$ (the multiplier $1 \in S(n,d_0)$, and
$\deg(1 \cdot f) = \deg f \le 2 \le d_0$).
Second, $fg \in V(n,d_0)$ by printed Theorem 4.1(2) applied with the pair
($g := f \in V(n,d_0)$, $h := g \in S(n,d_0)$) and $\deg(fg) \le d_0$.
Third, $(fg)^\rho \in V(n,d_0)^\rho$ by the printed set-definition
$A^\rho = \{g^\rho \mid g \in A\}$.
Fourth, $L$ vanishes on $V(n,d_0)^\rho$ because
$L \in {\sf Des}(n,d_0)^\rho$ (Sec 2.3 READING NOTE). Hence
$\omega(fg) = L((fg)^\rho) = 0$. So condition 2 holds.
[REFINEMENT of chi_transfer.md: the sketch argued from $f^\rho \in V(n,d)^\rho$
plus "$L$ vanishes on $V(n,d)^\rho$", which needs
$f^\rho g^\rho \in V(n,d)^\rho$, i.e. closure of the restricted space under
multiplication, not printed. The argument above goes through the unrestricted
closure (printed Theorem 4.1(2)) and then restricts once, which uses only
printed definitions.]

### Step 5: condition 3 for $\Omega(n,d_0)$, from premise (A) and printed Lemma 4.4

Let $T$ be an arbitrary $(d_0, e)$-tree with
$e := e^* = \lceil h^* + \log S^* \rceil$, of the conflict task (Sec 2.4
READING NOTE; $e^* \ge h^* + \log S^*$, so $T$ ranges over a class at least as
large as Definition 3.1's condition-3 class at budget $h^* + \log S^*$).
[PRINTED, Sec 4, Lemma 4.4 ([8, L.4.3]):] "Let $T$ be a $(d,e)$-tree over
$S(n,d)$. Then there is $(d,e')$-tree $T'$ with $e' \le e + O(d \log n)$ such
that for any $\omega = (\rho,L) \in \Omega(n,d)$ if $T(\omega)$ is a conflict
pair for $\omega$ then $T'(\omega)$ is a pair $(i,j) \in D^\rho \times R^\rho$."
[Its printed proof idea:] "tree $T'$ uses a conflict pair found by $T$ to find
(by a binary search argument) a conflict pair consisting of monomials and then
another pair where one of the monomials is a variable $x_{ij}$. Clearly then
$\rho(x_{ij}) \neq 0,1$, i.e. $(i,j) \in D^\rho \times R^\rho$."
Fix $c_{44}$ to dominate the printed $O(d \log n)$; then, with $e = e^*$,
$e' \le e + c_{44} d_0 \log n = e^* + c_{44} d_0 \log n = E$, so $T'$ is a
$(d_0, E)$-tree,
and $T'$ carries labels in $[n+1] \times [n]$ (its outputs are such pairs).
Premise (A) applies to $T'$:

    err(T') = Prob_\omega[T'(omega) \notin D^\rho x R^\rho] >= gamma.

Lemma 4.4's implication is pointwise in $\omega$, hence

    Prob_\omega[T(omega) is a conflict pair for \omega]
      \le Prob_\omega[T'(omega) \in D^\rho x R^\rho]
      = 1 - err(T')
      \le 1 - gamma,

so $\mathrm{Prob}_\omega[T(\omega)$ is not a conflict pair for
$\omega] \ge \gamma$. As $T$ was an arbitrary $(d_0, e^*)$-tree,
$\Omega(n,d_0)$ satisfies Definition 3.1's condition 3 at parameters
$(d_0,\, e^*,\, \gamma)$, and hence (by Lemma M below with the budget
$h^* + \log S^* \le e^*$) at parameters
$(d_0,\, h^* + \log S^*,\, \gamma)$.

### Step 6: monotonicity, contradiction, conclusion

Lemma M (solution monotonicity). [ASSEMBLY, from printed Definition 3.1.]
If $\Omega$ is a $(d', e', \gamma')$-solution of $\mathcal{F}$ and
$d \le d'$, $e \le e'$, $\gamma \le \gamma'$, then $\Omega$ is a
$(d,e,\gamma)$-solution.
Proof. The maps of $\Omega$ have domain $\mathbb{F}_p^{\le d'}[x]
\supseteq \mathbb{F}_p^{\le d}[x]$, so the $(d,e,\gamma)$-reading of
conditions 1 and 2 is a restriction of the $(d',e',\gamma')$-reading (smaller
$g$-range and $\deg(fg) \le d \le d'$). For condition 3, every $(d,e)$-tree is
a $(d',e')$-tree (queries from the smaller space, height $\le e \le e'$), so
the printed probability is at least $\gamma' \ge \gamma$ for each of them. QED
By Steps 0, 4, 5, $\Omega(n,d_0)$ is a
$(d_0,\, e^*,\, \gamma)$-solution of $\neg\mathrm{PHP}_n$, and by Lemma M (with
$e := h^* + \log S^* \le e^*$) also a
$(d_0,\, h^* + \log S^*,\, \gamma)$-solution.
Apply Lemma M with $d := d''$, $e := h^* + \log S^*$,
$\gamma := (S^*)^{-1}$, noting $d'' \le d_0$ (Step 3) and
$(S^*)^{-1} = k^{-(c_S+C)} \le k^{-C} = \gamma$ (Sec 3): $\Omega(n,d_0)$ is a
$(d'', h^* + \log S^*, (S^*)^{-1})$-solution of $\neg\mathrm{PHP}_n$.
This contradicts $(*)$. Therefore no $F_\ell(\mathrm{MOD}_p)$-refutation of
$\neg\mathrm{PHP}_n$ with $k$ steps exists.
We have assumed (A), (B1), (B2) "for all sufficiently large $n$"; hence the
conclusion holds for all sufficiently large $n$, which is the printed "for all
$n \gg 1$". [READING NOTE: Theorem 3.3's literal conclusion is "does not admit
$F_\ell(\mathrm{MOD}_p)$-refutation with $k$ steps"; Theorem 6.1's paraphrase
"requires at least $k(n)$ steps" is the paper's own rendering of the same
statement. Under the standard padding of step counts, "no refutation with $k$
steps" is equivalent to "every refutation has more than $k$ steps"; this
equivalence is not printed and is not used above.] Theorem R is proved. QED

### Step 7: the packaged form via printed Theorem 3.3

Steps 2-3 and 5-6 with $C$ fixed are one instance of the paper's own summary
theorem. [PRINTED, Sec 3, Theorem 3.3:] "For any constant $\ell \ge 2$ and any
function $k = k(n) \ge 1$ the followings holds: if there is an
$((\log k)^{O(\ell)}, O(\log k), k^{-O(1)})$-solution for
$\neg\mathrm{PHP}_n$ then $\neg\mathrm{PHP}_n$ does not admit
$F_\ell(\mathrm{MOD}_p)$-refutation with $k$ steps, for all $n \gg 1$.
The constants implicit in the O-notation depend only on F and p ."
The solution produced in Steps 0, 4, 5 has parameters
$d_0 = (\log k)^{O(\ell)}$ (since $h^* = O(\log k)$),
$h^* + \log S^* = O(\log k)$, $\gamma = k^{-C} = k^{-O(1)}$, all with absolute
constants; so Theorem 3.3 can be cited in place of Steps 2, 3, 6, provided the
constants in (A), (B1), (B2) are matched to Theorem 3.3's implicit ones, which
is what Steps 2, 3 and Lemma M do explicitly. The route document keeps the
unpacked form (Theorems 2.2 and 3.2 separately) because that is where every
constant enters; the packaged citation is the one-line form of record.

## 5. Reconciliation with the printed Theorem 6.1(3)

### 5.1 What (3) says and why the route neither assumes nor proves it

[PRINTED, Sec 6, Theorem 6.1, in full:] "Let $\ell \ge 2$. Assume that for a
$(d,e')$-tree $T'$ with

    d = (\log k)^{O(\ell)}  and  e' = O(\log n) + O(d \log n) = d(\log k)

it holds that:

    Prob_{\rho,P} [\chi(P,\rho) = 1] \ge k^{-O(1)}    (3)

where $\omega \in \Omega(n,d)$, $\rho \in {\sf Res}(n,d)$ and path $P \in T'$
are chosen randomly and uniformly. Then for all $n \gg 1$ any
$F_\ell(\mathrm{MOD}_p)$-refutation of $\neg\mathrm{PHP}_n$ requires at least
$k(n)$ steps.

(For the estimate of $e'$ by $d(\log k)$ we use that $k \ge n^3/2$ as any
refutation of $\neg\mathrm{PHP}_n$ must use all polynomials
$Q_{i_1,i_2;j}$.)"
Hypothesis (3) is the $(P_3)$-quantity: paths uniform over the padded tree's
$p^{e'}$ branches, no $L$ sampled, the $\mathrm{Span}$ conjunct active.
Theorem R's premise is the $(P_2)$-quantity. The two are linked one-way:
[PRINTED, Sec 5, Lemma 5.2:] "Assume that every path in $T'$ has the length
$e'$. Then

    Prob_\omega[T' errs on \omega] \ge Prob_{\rho,P} [\chi(P,\rho) = 1]" .

So $(3) \Rightarrow \mathrm{err}(T') \ge k^{-O(1)}$ for every tree, i.e. (3)
implies premise (A) at the printed budget: the printed hypothesis is STRICTLY
STRONGER than the route's.
The converse fails, so Theorem R cannot be read as a proof of (3): from
$\mathrm{err} \ge \gamma$ nothing follows for the smaller $(P_3)$-quantity.
Quantitatively (chi_transfer.md Proposition 1, from printed Lemma 5.1 and the
padding identity in the Lemma 5.2 derivation):

    err(T') >= chi(T')  and  chi(T') >= p^{-Delta(T')} err(T'),

where $\mathrm{defect}(P,\rho) = e' - \dim^\rho(P)$ and $\Delta(T')$ is the
maximum defect over $\chi$-good paths. The gap $\exp(\ln p \cdot \Delta(T'))$
is unbounded over the tree class.

### 5.2 The trivial tree: (3) is false as a universal statement

chi_transfer.md Theorem 3 (proved there; compact reproof with anchors). Let
$2 \le d \le n/4$, $e' \ge 1$, and let $T_0$ query the row polynomials
$Q_1, \ldots, Q_{e'}$ (each of degree 1, hence admissible in the printed class
at any $d \ge 1$; repeating one query also works) and
output the fixed label $(1,1)$ on every leaf.
Each $Q_i$ lies in $V(n,d)$ (they are Sec 1's system polynomials; the argument
of Sec 4, Step 4), so $Q_i^\rho \in V(n,d)^\rho$ and $L(Q_i^\rho) = 0$ for
every design $L$; a branch with any answer $a_i \neq 0$ carries
$Q_i^\rho - a_i \in W(P)^\rho$, hence $1 = a_i^{-1} a_i \in
\mathrm{Span}(W(P)^\rho)$ and $\chi(P,\rho) = 0$; only the all-0 branch is
$\chi$-eligible, and on it
$\mathrm{Span}(W(P)^\rho) = \mathrm{Span}(V(n,d)^\rho)$, and
$1 \notin \mathrm{Span}(V(n,d)^\rho)$ holds by the printed identification of
$V(n,d)^\rho$ with the restricted system's degree-$\le d$ consequences (the
restricted rectangle is $\neg\mathrm{PHP}$ on $(2d+1) \times 2d$) plus printed
Theorem 4.1(1) at parameter $2d$ (chi_transfer.md Sec 2.3), so

    chi(T_0) = (1 - f) p^{-e'},   f = (2d+1) 2d / ((n+1) n),

by the corpus's fixed-pair freeness probability (corpus Prop A [MV]; also
chi_transfer.md Sec 6). Every $\omega \in \Omega(n,d_0)$ answers all $Q_i$
by $0$, so $T_0$ never errs:

    err(T_0) = 1 - f >= 1/2  (f \le 1/2 for d \le n/4) .

At the printed budget $e' = \Theta(d \log k)$:
$\chi(T_0) = (1-f) p^{-e'} = k^{-\Theta(d)}$.
Consequently, for $d = \omega(1)$ and any fixed $C$:
$\chi(T_0) < k^{-C}$ for all large $k$: the universal statement "every
$(d,e')$-tree satisfies (3)" is FALSE at growing $d$.
Padding sensitivity (chi_transfer.md Theorem 3, remark (a)): padding any tree
to depth $e'$ by repeating the determined query $Q_1$ leaves err unchanged and
multiplies $\chi$ by $p^{-(e'-e'')}$, so even a hypothetically good tree fails
(3) in padded form, and the universal quantifier includes padded forms.
This is why the assembly does not, and cannot, prove the printed (3): the
route's premise lives on the design-sampled side where determined queries are
free, while (3) taxes every determined or killed query on a uniform path a
full factor $p$ (chi_transfer.md Sec 2.3: the defect tax). No strengthening of
any err-cap can prove (3) for all trees; the route's premise and (3) separate
already on $T_0$.

### 5.3 Where the paper's closing hope goes wrong

[PRINTED, Sec 6, the paragraph after Theorem 6.1:] "It appears possible that
the hypothesis in the theorem holds for $k(n) = 2^{n^\delta}$, for sufficiently
small $\delta > 0$, even with the bound in (3) being $\Omega(1)$."
Under the quantifier the reduction logic forces (Sec 5.4), this hope is
refuted by $T_0$: at $k = 2^{n^\delta}$ and fixed $\ell$, the printed degree
regime has $d = (\log k)^{O(\ell)} = n^{\Theta(\delta \ell)}$ (taking
$d \le n/4$, consistent for small $\delta$), and the printed budget gives
$e' = \Theta(d \log k) = \Theta(n^{\Theta(\delta \ell)} \cdot n^\delta)$, so

    chi(T_0) = (1 - f) 2^{-e'} = 2^{-\Theta(n^{\Theta(\delta \ell) + \delta})}
             \le k^{-C'} \ \text{for every fixed } C' \text{ and large } n,

while $\mathrm{err}(T_0) = 1 - f \ge 1/2$. So the $\Omega(1)$ bound on (3) is
unprovable as stated, for every $\delta > 0$ in the printed regime: the
determined-query collapse puts $T_0$'s $(P_3)$-value at
$2^{-\Theta(e')}$ while its $(P_2)$-value stays $\Omega(1)$.
The hope overlooks exactly the uniform-path tax: a quantity can be
$\Omega(1)$ on the design-sampled side and $2^{-\Theta(e')}$ on the
uniform-path side of the same tree.
[Corpus note, not needed for the route: the budgeted err-floor itself is also
sub-constant at growing $d$ in the full printed regime, since
$\mathrm{err}^*(d, d\log k) = k^{-\Theta(d^2/n)}$ at degree $\le 2$
(deg2_theory.md Sec 8); the route needs only $k^{-O(1)}$, which is O2's form.]

### 5.4 The quantifier reading

Theorem 6.1's literal grammar is "for a $(d,e')$-tree $T'$ ... it holds that
(3)", which reads existentially; the reduction logic forces the universal
reading (chi_transfer.md Sec 2.2, READING NOTE row; open_problems.md O2).
The forced reading, made explicit: Theorem 3.3's hypothesis is the EXISTENCE of
a pseudo-solution, i.e. Definition 3.1's condition 3 must hold for EVERY
$(d,e)$-tree at the solution's parameters; feeding that from the pipeline
requires a floor on every reduced tree of budget $E$ (premise (A)), or a fortiori
(3) for every tree of budget $e'$ (the printed reading). Under the literal
existential reading the hypothesis would assert one tree's behavior and could
not interface with Theorem 3.3, which quantifies over all trees of a solution.
The err-form route inherits the universal reading through Definition 3.1's
printed "For any $(d,e)$-tree $T$".

### 5.5 Net statement

The printed Theorem 6.1 chains (3) into the err-floor through printed Lemma 5.2
and then into the conclusion through Lemmas 4.4 and Theorem 3.3.
Theorem R deletes the head of that chain: it starts at the err-floor, which is
the weaker and falsifiable-alive quantity (O2), and runs the same tail
(Lemma 4.4, Theorem 3.2 or 3.3) with all constants made explicit. The Span
conjunct, uniform path sampling, and (3) itself appear nowhere. The false
universal (3) is not a hypothesis of any live route; it is a strictly stronger
statement whose failure (Theorem 3 above) is a formulation artifact of the
$(P_3)$ quantity and carries no evidence about the pipeline.

## 6. Hypothesis checklist (1:1 with the corpus's open problems)

1. (A), the err-floor at $(d_0, E)$, err in the $(P_2)$ sense: this is O2
   (open_problems.md), the all-degrees budgeted floor, in its err-form. Budget
   bookkeeping: $E = e^* + c_{44} d_0 \log n$ with
   $e^* = \lceil h^* + \log S^* \rceil = O(\log k)$ and $d_0 \ge 3$; under
   (B1), $\log n \le \log k$, so $E \le b_E \, d_0 \log k$ for an absolute
   $b_E$. Hence O2's floor at budget $d_0 \log k$ with implied constant
   $\ge b_E$ implies (A). The slack $b_E$ and $c_{44}$ are unprinted on both
   sides (chi_transfer.md Sec 4.1), and O2's $e = d \log k$ matches $E$ up to
   that constant.
   Status against O2's sub-items: degree $\le 2$ slice proved
   (deg2_theory.md Corollary 3.1), modulo the two JDP composition steps
   (O2(v)) and the mixture-query gap (chi_transfer.md Sec 4.3, GAP B', a
   proper-subset issue inside degree 2); degree $\le 3$ slice proved
   (deg3_theory.md Theorem 3'); the open core is the degree $\ge 4$ cap
   (O2(i)), which is exactly the substantive content since $d_0$ grows;
   O2(ii) (the exact exponent constant) matters here because the floor's
   exponent must merely beat the route's fixed $C$; O2(iii) (the
   $\chi$-transfer) is MOOT for the route: the route uses the $(P_2)$-form and
   never needs the transfer that O2(iii) asked for; O2(iv) (intermediate
   budgets) is not needed at the printed budget.
   [READING NOTE: O2's literal phrasing "T(omega) is not a conflict for omega"
   is the corpus's unified phrasing; the form of record for (A) is the
   $(P_2)$-form of Sec 2.6, which is what the corpus's measurements sample
   (chi_transfer.md Sec 5, item 4). A $(P_1)$-form floor does not imply (A)
   by Lemma 4.4 (that lemma maps conflict trees forward only), so the
   $(P_2)$-form is the one to prove.]
2. (B1), $k(n) \ge n^3/2$: printed (Theorem 6.1's parenthetical). Its printed
   role is the identification $e' = d(\log k)$; the route's role is the same
   budget bookkeeping ($\log n \le \log k$ in entry 1). Theorem 3.3 itself
   allows any function $k = k(n) \ge 1$, so the corpus's target regime
   $k(n) = 2^{n^\delta}$ is admissible from the theorem side; the binding
   constraint on $\delta$ comes from entry 3.
3. (B2), $2 \le d_0 \le n/2$: printed range of Definition 4.3 (and of Theorem
   4.1, Corollary 4.2, and the homomorphism paragraph's rectangle reading).
   The lower side is automatic for large $k$ ($d_0 \ge 3$); the upper side is
   the corpus's $\delta$-cap regime: $d_0 = (\log k)^{c_d \ell + o(1)} \le n/2$
   requires, at $k = 2^{n^\delta}$, roughly $\delta \cdot c_d \ell < 1$
   (open_problems.md O2: "Theorem 6.1's quantifier allows degree up to
   $d = (\log k)^{O(\ell)}$, which grows"; the corpus's
   $\delta \cdot O(\ell) \le 1/2$ band lives here, deg2_theory.md Corollary
   3.1's closing remark).
4. What Theorem 2.2 requires (all printed): $\ell$ a fixed constant;
   accuracy parameter $h \ge 1$, arranged ($h := h^*$, and $h^* \ge 1$ since
   $S^* \ge 1$); $n \ge 1$ unrestricted; and the absolute-constants sentence
   "The constants implicit in the O-notation depend only on F and p", read as
   covering $S = k^{O(1)}$ uniformly in $h$ (Sec 4 Step 2 READING NOTE).
   This fixes $c_S, c_d$; together with the route's $C$ it fixes
   $S^*, h^*, d_0$ and hence the premise (A)'s parameters.
   Theorem 3.2's own premise $e^{h/p} \ge 2S^2$ is not an open condition: it
   is arranged by the $h^*$-choice plus Lemma P's padding to $S^*$.
5. Theorem 3.3's constants ("depend only on F and p"): the route's
   $\gamma = k^{-C}$, $d_0 = (\log k)^{O(\ell)}$,
   $h^* + \log S^* = O(\log k)$ must be matched to the O-constants of the
   single cited theorem if the packaged form (Step 7) is used. This is a
   bookkeeping requirement, not an open problem; the unpacked Steps 2-6 do the
   matching by hand.
6. The two assembly lemmas (Lemma P: ENS padding; Lemma M: solution
   monotonicity) are proved in Sec 4 from printed definitions. They are not
   hypotheses and correspond to no corpus open problem.
7. Not on the list, deliberately: the $\mathrm{Span}$ conjunct, the
   $\chi(P,\rho)$ machinery, Lemma 5.1, Lemma 5.2, and any path-uniformity
   convention. The route bypasses all of them; that is its content.

## 7. Verdict

The err-form route is now a complete conditional proof: printed Definition 3.1
+ Lemma 4.4 + Theorem 2.2 + Theorem 3.2 (packaged equivalently by printed
Theorem 3.3), with one assembly lemma for the threshold matching (Lemma P) and
one for the parameter bookkeeping (Lemma M), both two-line consequences of the
printed definitions. Its single mathematical premise is the all-degrees
budgeted err-floor in the $(P_2)$ form, at budget
$E \le b_E d_0 \log k$ and degree $d_0 = (\log k)^{O(\ell)}$, with the regime
$k \ge n^3/2$ and $d_0 \le n/2$. That premise is exactly O2 with its open core
at degree $\ge 4$; degree 2 and degree 3 slices are in hand modulo the JDP
steps and the degree-2 mixture sub-gap. The printed Theorem 6.1(3) is not part
of this route, is strictly stronger than its premise, and is false as a
universal statement at growing $d$ (trivial row-sum tree,
$\mathrm{err} \ge 1/2$, $\chi = k^{-\Theta(d)}$); the paper's closing hope of
an $\Omega(1)$ bound on (3) fails on the same tree for every
$\delta > 0$ in the printed regime, because it taxes determined queries that
the design measure does not tax. The program of record stands as consolidated:
prove O2; Theorem R then delivers the super-polynomial
$F_\ell(\mathrm{MOD}_p)$-Frege lower bound for $\neg\mathrm{PHP}_n$.
