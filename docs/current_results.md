# Current results: the one current statement of the corpus

Consolidation deliverable, 2026-10-04; second pass the same day, folding in the
newest wave (all_degrees.md, cls_cnt.md, inv3.md, mixture3.md, deg5_theory.md)
with the two retractions of section 3. This file is the single current statement of
every proved or measured result the corpus holds.
It supersedes the layered correction history, which remains in the source documents
and in LOG.md for provenance.
Scope: the mathematics of the $\Omega(n,d)$ answer channel at $p = 2$ and at general
characteristic $p$.
Route maps, claim forensics, monitors, the bibliography, and the theorem map keep
their own homes (GOAL.md section 4); this file does not replace them.
Labels are PROVED (with the proof kind: written proof, machine-checked, or
enumerated), MEASURED, or INFERRED (a downstream conclusion whose named premise
is open), nothing else.
Every number matches regeneration_2026-10-04.md or the cited source document.

## 1. Semantics

The channel semantics are frozen in docs/channel_spec.md (2026-10-04) and are not
restated here: the object is the $\Omega(n,d)$ pipeline of arXiv:2609.35927 at a
fixed prime $p$, where $\rho$ is a uniform partial injection $[n+1] \to [n]$ leaving
$2d+1$ free pigeons $D$ and $2d$ free holes $R$, $L$ is a uniform degree-$d$ design
of the restricted system over $\mathbb{F}_p$ ($L(1) = 1$, $L$ vanishes on
$V(2d,d)$, with the zeroing completion of the printed restriction clause), the
answer is $\mathrm{ans}(g) = L(g^\rho)$, and $V(n,d)^\rho = V(2d,d)$ is the
one-kernel fact; the spec fixes the answer function per query class (12 determinism
rows, 9 independence statements, 4 locks), the fresh-bit stipulation with its
alias-aware completion events (E_ROW, E_STAR, E_K), two conforming implementation
routes, and the conformance checklist; a simulator that disagrees with the spec is
wrong until the spec is amended by a dated section plus a LOG.md entry.

## 2. Proved results

### 2.1 The channel law and its locks (kernel-true, every $p$)

Statement.
Determined answers, on every status configuration and every $p$: matched singles
answer 1, killed-unmatched singles answer 0, restricted (free pigeon, matched hole)
cells answer 0, the row-sum query $Q_i$ answers 0 on every pigeon, killed-column
$K_j$ answers 0, squares answer their single, same-line degree-2 products answer 0,
all-distinct degree-$k$ monomials containing a line pair answer 0, alias monomials
answer their square-free reduction (fixed 0 exactly when the reduction is
same-line), diagonal products answer the free component's value when one component
is matched and 1 when both are matched, and any monomial with a killed factor
answers 0 (channel_spec.md table 5.1, rows D1-D12).

Independence and uniformity, on the stated windows: free singles are marginally
uniform on $\mathbb{F}_p$ and jointly i.i.d. on row-incomplete sets; a completed
free row is uniform on the sum-$1$ hyperplane (at $p = 2$: the $2^{2d-1}$ odd
patterns, XOR $= 1$, all-zero absent); killed rows and killed columns of the answer
table show exactly one 1; free columns carry i.i.d. uniform entries; $K_j$ is uniform
on $\mathbb{F}_p$ on free columns with $P(K_j \ne 0) = (p-1)/p$; diagonal (both
free) answers are fresh values independent of their component singles and of each
other on block-free windows; matching-$k$ columns all vary and are marginally fair
(channel_spec.md table 5.2, rows I1-I9).

Locks: the row lock $\sum_{j \in R} L(x_{ij}) = 1$ for every free pigeon; the star
lock $\sum_{j \in R \setminus \mathrm{holes}(g)} \mathrm{ans}(x_{pj}g) =
\mathrm{ans}(g) \cdot [p \in D]$ for $\deg g \le d-1$, with the injectivity
automatism $\rho(p) \in \mathrm{holes}(g) \Rightarrow \mathrm{ans}(g) = 0$; the
column relation $\bigoplus_{j \in R} \mathrm{ans}(K_j) = 1$ at $p = 2$ (the
general-$p$ form $\sum_{j \in R} \mathrm{ans}(K_j) = -1$ is spec-derived, not
separately machine-verified); and the global parity lock (the number of odd columns
in any free-region matrix is odd) (channel_spec.md table 5.3, rows L1-L4).

Proof location.
channel_spec.md sections 2-3 and 5, on sources: kernel_structure.md Findings 1-4,
deg2_theory.md facts F1-F5, odd_p_theory.md Theorems ChP and KP, lemma_m.md
sections 1-2, deg3_theory.md Lemma D3, deg4_theory.md Lemmas W4 and A4 and
Theorem B (the degree-4 star lock).

Verification status.
Machine-checked at the kernel points (restricted $(2,1)$, $(4,2)$, $(6,3)$; odd-$p$
checks at $(4,2)$ for $p \in \{2,3,5\}$), written proofs for the generator-row
arguments (star lock at every $d \ge 2$ and every $p$, same-line pins, alias laws,
the odd-$p$ 2-torsion argument for the row lock), and enumerated classifications
(all 13,244 degree-3 columns at $(6,3)$; the $(8,4)$ three-class partition,
$912{,}978 + 302{,}472 = 1{,}215{,}450 = \binom{75}{4}$).

Regime of validity.
Unconditional at the verified kernel points (outer $d \le 3$).
The general-$d$ degree-2 statements carry Lemma CLS and Lemma CNT, closed in
regime by the newest wave (sections 2.16 and 2.17).
Odd-$p$ degree $\ge 3$ is not covered (section 4, O6).

Label: PROVED (machine-checked, plus written proofs per clause as listed).

### 2.2 Theorem A (the matching hierarchy, all $d$)

Statement.
At every restricted $(2d,d)$ and every $1 \le k \le d$, every matching-$k$ column
(all-distinct, $k$ distinct pigeons and $k$ distinct holes) is design-varying, and
its answer under uniform designs is a fair coin at $p = 2$.
No matching column is ever determined, at any degree up to $d$.

Proof location.
deg4_theory.md section 2 (Theorem A): star-row induction step, orbit closure under
$S_{2d+1} \times S_{2d}$, base case = the single-variable law (paper cor:coin).

Verification status.
Written proof for the induction step; the base is machine-checked at $(2,1)$,
$(4,2)$, $(6,3)$ and exact at the $(8,4)$ degree-$\le 2$ slice (0/72 singles
determined, 2016/2016 matching-2 varying); enumerated support: all 4200 matching
triples vary at $(6,3)$, all 211,680 matching-4 columns are varying-valued at
$(8,4)$.
Newest wave (deg5_theory.md section 2): the base re-verified at the $(10,5)$
degree-$\le 2$ slice (0/110 singles determined, 4950/4950 matching-2 varying),
the star-row steps $Q_p \cdot g_k$ witnessed legal for $k = 2, 3, 4$, and the
matching-3 link confirmed by the sparse degree-$\le 3$ sweep at $(10,5)$
(118,800/118,800 varying); matching-4 and matching-5 rest on the proved
induction.

Regime of validity.
$p = 2$, all $d$.
The induction is coefficient-free, but the odd-$p$ kernel classification has not
been re-run, so odd-$p$ degree $\ge 3$ statements remain open (section 4, O6).
The base's general-$d$ standing rests on the corpus's completion lemma (cor:coin)
plus the verified slices; a self-contained elementary proof is a flagged small gap
(deg4_theory.md section 7 item 1).
The degree-5 slice consumes Theorem A at $k = 5$ (section 2.20), and the
general-$d$ transfer and all-degrees assembly consume it at every $k$ (sections
2.16 and 2.21); the base caveat is inherited at every use.

Label: PROVED (written induction, machine-checked base).

### 2.3 Lemma M (transcript-level transfer) and the fresh-bit identification

Statement.
For any adaptive degree-$\le 2$ tree of budget $e$ with transcript $\tau$,
$$d_{TV}\big(\mathrm{law}_\Omega(\tau),\ \mathrm{law}_{fb}(\tau)\big)
   \le \varepsilon(e,n,d)
   \le \frac{A}{2}\Big[\Big(\frac{e}{n}\Big)^{2d}
      + \Big(\frac{2e}{n-1}\Big)^{2d-1}\Big],
   \qquad A = \frac{2d+1}{n+1},$$
with $\varepsilon = \varepsilon_{row} + \varepsilon_{star}$, and
$\varepsilon_K \le \tfrac12 (e/n)^{2d}$ added if linear-form queries are allowed.
The bound is $o(1)$ exactly when $e = o(n)$; a row event needs $e \ge 2d$ and a
star event $e \ge 2d$, so at $e < 2d$ the transfer is exact.
The transfer target is the FRESH-BIT channel (squares alias to their singles,
same-line products answer 0, diagonals are fresh fair bits independent of
everything), not the earlier product-semantics stipulation: on a free triangle
$\{x_{ab}, x_{cd}, x_{ab}x_{cd}\}$ the true law is uniform on 8 patterns and the
product law lives on 4, TV $= 1/2$, with no completion event needed.
The block-free identification, current final form: on every alias-aware
block-free window (one containing no completed relation of the FIVE-family
inventory {row, star, DS, UU, OFF}, plus no full $K_j$-column set when linear
forms are allowed) the pipeline's projected answer law equals the fresh-bit law
exactly.
INVENTORY CORRECTION (2026-10-04, cls_cnt.md section 4; ADDENDUM 11): the
three-family inventory $\{E_{row}, E_{star}, E_K\}$ that this entry originally
stated is INCOMPLETE - the double star DS, the crossed-star pair UU, and the
cross grid OFF (sums of reduced star rows, all machine-verified in $V$ at
$(4,2)$ and $(6,3)$) pin windows that fire no single inventoried event.
The correction supersedes lemma_m.md's refined $E_{star}$ (its target-single
requirement broke closure under sums; the original target-free Lemma REL
definition was safe), re-interprets the recorded sweep evidence (1192/1192,
250/250) as sampling evidence, moves no recorded measurement, and leaves
$\varepsilon$ at $\varepsilon_{full} = (1 + o(1))\,\varepsilon_{headline}$
(section 2.17); the catch-all class absorbs the residual L-CLASS classification
(section 2.16).

Proof location.
lemma_m.md sections 2-3.
The supersession of deg2_theory.md Lemma REL (its product-channel identification
repaired to fresh-bit; its constants improved:
$(2d+1)(e/n)^{2d} \to A(e/n)^{2d}$ for rows and
$(n+1)n(e/n)^{2d-1} \to (2e/(n-1))^{2d-1}$ for stars) is recorded in lemma_m.md
section 6 and channel_spec.md section 6.

Verification status.
Written proof (coupling step, non-adaptive count, adaptive feedback under the
exposure convention); machine-checked by exact support enumeration over the full
kernel coset, 1192/1192 alias-aware block-free windows at $(4,2)$ and 250/250 at
$(6,3)$, sizes 2 to 10 coordinates.

Regime of validity.
Unconditional at $d \le 3$; at general $d$ the two lemmas this entry was reduced
to (CLS, CNT) are closed in regime (sections 2.16 and 2.17), so the general-$d$
form holds in regime modulo their named caveats (the cor:coin base, B2, and the
engine-validity caveat of section 2.16).
Exact for $e < 2d$; vacuous at $e = \Theta(n)$, where the transfer question is open
(O2's intermediate-budget item).

Label: PROVED (written and machine-checked at $d \le 3$; the general-$d$ form is
closed in regime by sections 2.16 and 2.17, modulo their named caveats).

### 2.4 Propositions A and C (the single-variable non-adaptive theory)

Statement.
Proposition A (fixed-label exactness): any tree whose leaves all carry the same
label $(i_0,j_0)$ has success exactly $P[(i_0,j_0) \in D^\rho \times R^\rho] =
\frac{2d+1}{n+1} \cdot \frac{2d}{n} = f$, independent of its queries and depth.
Proposition C (non-adaptive cap): any non-adaptive single-variable tree with $s$
fixed queries has success $\le f(1 + s/2 + o(1))$, hence error $\ge 1/2$ whenever
$d \le n/4$.

Proof location.
proof_complexity.md, section "Formal statements: the provable p=2 cap".

Verification status.
Written proofs; kernel-faithful (TV $= 0$ off full rows, kernel_structure.md
item 4).

Regime of validity.
$p = 2$, single-variable class; Proposition C at fixed budget $s$ with
$f(1+s/2) < 1$.

Label: PROVED (written).

### 2.5 Theorem B (the adaptive single-variable budgeted cap)

Statement.
Every adaptive single-variable tree of budget $e$ has success
$\le \max\big(2d^2/(2d^2+n),\ f/2\big) + O(e/n) + o(1)$; at
$d \le \sqrt{n}/\sqrt{2}$ the error is $\ge 1/2 - o(1) \ge k^{-O(1)}$.
Its coupling lemma B.1 holds for pairs with BOTH coordinates outside the queried
set (the disjoint-pair quantifier; verified 35/35).

Proof location.
proof_complexity.md, Theorem B and Lemma B.1.
The proof is re-based on jdp_demod.md Lemmas D1 and D3 (ADDENDUM 8); the written
step (2) negative-association claim is retracted (section 3 below).

Verification status.
Written proof: the per-pair Bayes step is exact, the depletion bound is Lemma D1
with explicit constant (cross-checked digit-for-digit against thmB_stress.md), and
the inclusion-family NA fact is proved elementarily as Lemma D3.

Regime of validity.
Budgeted: the coupling slack is $O(e/n)$-type and vacuous at $e \sim n^2$
(proof_complexity.md correction block, "Theorem B: intact, with a scope note"); the
cap is strongest at the program's budget $e = d\log k$.
The class is subsumed by Theorem 3's full degree-$\le 2$ statement, whose proof
supersedes this route (deg2_theory.md section 10 item 7).

Label: PROVED (written, after the re-basing).

### 2.6 Theorem F (the exact coin-channel floor) and the true-pipeline unbounded optimum

Statement.
Theorem F: every adaptive degree-1 tree with no query budget, on the stipulated
i.i.d.-coin channel at $p = 2$, has error exactly
$$\mathrm{err}^* = (1 - 2d/n)\,(2d{+}1)(2d)!\,/\,2^{(2d+1)2d} = 2^{-\Theta(d^2)},$$
attained by a non-adaptive full-scan counting tree
($1.001 \times 10^{-4}$ at $(32,2)$; $6.724 \times 10^{-17}$ at $(64,4)$).
Channel scope: the value is coin-channel-specific.
On the true pipeline the unbounded degree-1 optimum is success exactly 1
(deg2_theory.md Theorem 5), because the counting tree's only failure class needs an
all-zero free row, which the row lock forbids; the same holds at every $p$
(odd_p_theory.md Theorem 5''), where counting certificates count nonzeros.

Proof location.
cert_floor.md (Lemmas 1-5, Theorem F, the channel-law audit); deg2_theory.md
section 7 (Theorem 5); odd_p_theory.md section 3 (Theorem 5'').

Verification status.
Written proofs; exact enumeration ($(4,1)$: all 7,680 configurations; $(5,2)$: all
$2^{20}$ coin matrices, digit-exact) plus a Bayes audit (tree equals the per-class
optimum on every class); Theorem 5: written pigeonhole argument plus a 5,000-sim
zero-failure run.

Regime of validity.
Theorem F quantifies over the coin channel only, unbounded budget, degree 1.
Theorem 5 quantifies over the true pipeline, unbounded budget, degree 1 (every $p$).

Label: PROVED (written and enumerated).

### 2.7 The certain-certificate inventory, with rates

Statement.
The certain mechanisms (posterior exactly 1) are:

| mechanism | statement | rate | source |
|---|---|---|---|
| adjacency | two answer-1s on a common row or column certify both pairs free | chain constant $c = h_1(1-(1-q(2d-1)/(2(n-1)))^k)$; $0.0026$ per query at $(32,2), k=6$, vs measured $0.0018$-$0.0026$ | deg2_theory.md Thm 1 |
| wedge (any degree) | two answer-1s on monomials sharing a pigeon in distinct holes certify that pigeon free | $\Theta(d/n^2)$ per query | deg3_theory.md Lemma S3 |
| Z (any degree) | single answer 0 plus containing-monomial answer 1 certifies the pair free (odd $p$: $\mathrm{ans}(x_p) \ne 1$, $\mathrm{ans}(m) \ne 0$) | $\Theta(d/n^3)$ per query | deg3_theory.md Lemma Z |
| $K_j$ column channel | $\mathrm{ans}(K_j) \ne 0$ certifies the hole free | $(2d/n)(p-1)/p$ per query | deg2_theory.md F5; odd_p_theory.md Thm KP |
| self-certification ($p > 2$) | a single answer in $\mathbb{F}_p \setminus \{0,1\}$ certifies its pair free, one query | $f(p-2)/p$ per query | odd_p_theory.md Lemma SC |
| counting | row/column count $\ne 1$ certifies free (odd $p$: nonzero counts, $P(c\text{ nonzeros}) = \binom{2d}{c}\frac{(p-1)^c - (-1)^c}{p \cdot p^{2d-1}}$, count 0 impossible) | inert within polylog budget; exact 1 at unbounded budget | cert_floor.md Lemma 3; odd_p_theory.md Lemma CNT |
| full scan | queries all $n(n+1)$ singles, applies counting certificates | success exactly 1, every $p$ | deg2_theory.md Thm 5; odd_p_theory.md Thm 5'' |

Measured exact per-attempt rates: wedge $0.335938$ (degree-3 base, $(7,3)$),
$0.536830$ (degree-2 base, $(7,3)$), $0.283333$ (degree-2, $(5,2)$); Z $0.133929$
and $0.098214$ at $(7,3)$; $K_j$ $0.285714$ ($p=2$) and $0.380952$ ($p=3$) at
$(7,2)$; $K_j$ dominates the wedge by 6-8x at $(7,3)$.
Mass dominance (deg4_theory.md Proposition M): the answer-1 masses satisfy
$P_4 < P_3 < P_2 < P_1$ at every tested point (e.g. $P_4 = 1.0 \times 10^{-8}$
against $P_1 = 9.5 \times 10^{-3}$ at $(127,4)$), so every degree-4-dependent
certificate is rate-dominated by every degree-1 channel.
Completeness evidence: at $(7,3)$ the exhaustive search explains all 2025
posterior-1 patterns as adjacency 14 + wedge 1920 + Z 60 + shadow 31, unexplained
0; at $(9,4)$ all 68,945 F1-certain patterns are explained, unexplained 0; the
$c = 1$ shadow artifact is provably inert once $c = n - 2d > 9$.
The sum-rule certificate candidate is not realizable (deg3_theory.md section 4
remark).

Proof location.
deg2_theory.md sections 2 and 6, deg3_theory.md sections 4-5, deg4_theory.md
section 5, odd_p_theory.md section 3.

Verification status.
Each mechanism: PROVED (written; all consume only determined structure, so they are
reading-independent).
Rates: MEASURED (exact enumeration over restrictions with exact design cosets).
Completeness: enumerated at $(7,3)$ and $(9,4)$; the general-scale classification is
open (folded into O2's program, section 4).

Regime of validity.
$p = 2$ and odd $p$ as marked; degrees 1 to 4 as searched; the rate ordering claims
carry the tested grids of their sources.

Label: mechanisms PROVED (written); rates MEASURED; completeness enumerated at two
scales, open in general.

### 2.8 Theorem 3 (the degree-2 budgeted cap; full printed class)

Statement.
Every adaptive tree of budget $e$ over the full printed degree-$\le 2$ class
(arbitrary $\mathbb{F}_2$ mixtures, normal form $c + \sum_p a_p x_p + \sum b_{pq}
x_p x_q$) satisfies
$$\mathrm{success}(T) \le \min\big(1,\ q_2^*(n,d) + P_{\mathrm{adj,mix}}(e) +
P_K(e) + O(e/n) + o(1)\big),$$
with $q_2^*(n,d) = \max(q,\ q_{\mathrm{and\_exact}},\ q_{\mathrm{mix}})$,
$q = \frac{(2d+1)d}{(2d+1)d + (n-2d)}$,
$q_{\mathrm{and\_exact}} = (M_1 + M_2)/(2M_0 + 2M_1 + M_2)$, and $q_{\mathrm{mix}}$
attained by monomial-star mixtures through the output pair, with
$q_{\mathrm{mix}}/q_{\mathrm{and\_exact}} \to 1$.
Reference values at $(32,2)$: $q = 5/19 = 0.263158$, $q_{\mathrm{and\_exact}} =
100/359 = 0.278552$, $q_2^* = 0.281688$; the star-mixture excess over
$q_{\mathrm{and\_exact}}$ is $+0.0362$ at $(7,2)$ ($787/934 = 0.842612$ vs
$25/31 = 0.806452$) and decays to $+0.0005$ by $(63,2)$.
Aliveness: error $\ge k^{-O(1)}$ whenever $d^2 \log k = o(n)$ (with room) at
$d \le \sqrt{n}$; the constant repair $q \to q_2^*$ does not move the
$d^2 \sim n$ boundary (lemma_m.md section 4.2).
Certificate form (ADDENDUM 9 correction): the printed certificate term
$2(1 - e^{-ed/(4n)})$ is invalid as a cap term; the valid form charges the exact
chain supremum,
$$\mathrm{success}(T) \le \chi(e) + (1 - \chi(e))\,(q + A(e))\,(1 + O(e/n) + o(1)),$$
with $\chi(e)$ the DP-computable $K$-chain supremum (quadratic at leading order,
$\chi(e) = \frac{\rho}{2}x^2(1+O(x))$ with $\rho = (2d+1)n/(2d(n+1))$ and $x =
ed/n$) and $A(e)$ the adjacency term.
Bookkeeping note: the proved $P_K$ form is the union bound $\min(1, ed/n)$; the
printed exponential constant is $\Theta(1)$-optimistic, and the cap form and
aliveness are unaffected (jdp_demod.md section 6).
The corpus states the full-class cap (Theorem M-D) and the sharpened certificate
form (Theorem E4) as two separate recorded statements; their constants have not
been merged into one displayed cap in any source document.
The general-$d$ standing of this cap in regime is section 2.18 (newest wave); the
mixture coverage here is the $d = 2$ instance of the MIXTURE-d line, closed at
$d \le 3$ (section 2.19).

Proof location.
deg2_theory.md Theorem 3 and Corollary 3.1; constant repair in lemma_m.md section 4
(ADDENDUM 7); full-class extension in mixture_cap.md Theorems M-A, M-B, M-E, M-D
(ADDENDUM 10); certificate-form correction in gap_e_constants.md Theorems E3/E4
(ADDENDUM 9).

Verification status.
Written proof with zero black-box citations: the two composition steps are
discharged elementarily by jdp_demod.md Lemmas D1 and D2 (ADDENDUM 8, GAP D
closed).
The mixture extension is a written assembly whose rate-weighted elevation
supremum is a measured constant ($\Theta(f)$), validated digit-exactly by a
dual-engine check (7,172 queries x 2 answers at $(7,2)$, 0 mismatches).
Measured: no mixture strategy beats the covered-class champions at any tested
budget; the $K_j$ tree dominates everything.
Channel facts machine-checked.

Regime of validity.
$p = 2$, degree $\le 2$, budget $e = o(n)$; at $e = \Theta(n)$ open (O2's
intermediate-budget item).

Label: PROVED (written; one measured constant inside the mixture certificate term).

### 2.9 Theorem 3' (the degree-3 budgeted cap)

Statement.
Every adaptive degree-$\le 3$ tree of budget $e$ satisfies
$$\mathrm{success}(T) \le \min(1,\ q_3^* + P_{\mathrm{adj}} + P_K + P_{\mathrm{wedge}}
+ P_Z + P_{\mathrm{blk3}} + o(1)),$$
with $q_3^* = \max(q,\ q_{\mathrm{and\_exact}},\ \mathrm{post}_3)$,
$\mathrm{post}_3 = (2u + v + w)/(2A_0 + 3u + 3v + w)$ (digit-exact at $(7,3)$:
$22/23$; $(8,3)$: $361/393$; $(9,3)$: $2751/3109$), and
$P_{\mathrm{blk3}} \le e/(n - 2d - 2)$.
The chi-hypothesis stays alive exactly when $d^2 \log k = o(n)$: the same boundary
as degree 2.
Posterior structure: $\mathrm{post}_3 > q$ at finite $n$ (up to $+0.0666$) and
exceeds $q_{\mathrm{and\_exact}}$ by at most $+0.0149$ near $n \sim 8d^2$; all
single-pass posteriors share the leading form $2d^2/n$ and their ratios tend to 1
(no asymptotic lift).

Proof location.
deg3_theory.md sections 3 and 6 (Theorem P3, Lemma REL-3, Theorem 3', Corollary
3.2).

Verification status.
Written assembly; the kernel classification it consumes is enumerated (13,244
degree-3 columns in ten classes at $(6,3)$); $\mathrm{post}_3$ digit-exact against
exhaustive restriction enumeration (56 to 60,480 restrictions); the
distant-evidence composition is discharged by the Lemma D1 transfer (jdp_demod.md
section 8); the multi-class deep-zero-run composition (deg3_theory.md open item 3)
remains open and, per the mitigation of record in jdp_demod.md section 8, does not
affect the cap's regime conclusion.

Regime of validity.
$p = 2$, degree $\le 3$.

Label: PROVED (written assembly, with enumerated kernel and posterior checks; one
flagged open composition residue that does not affect the regime conclusion).

### 2.10 Theorem 3'' (the degree-4 budgeted cap)

Statement.
Every adaptive degree-$\le 4$ tree of budget $e$ satisfies
$$\mathrm{success}(T) \le \min(1,\ q_4^* + P_{\mathrm{adj}} + P_K +
P_{\mathrm{cert4}} + P_{\mathrm{blk4}} + o(1)),$$
with $q_4^* = \max(q,\ q_{\mathrm{and\_exact}},\ \mathrm{post}_3,\ \mathrm{post}_4)$,
$$\mathrm{post}_4 = (b_0 + 3b_1 + 3b_2 + b_3)/(2b_4 + b_0 + 4b_1 + 6b_2 + 4b_3),$$
digit-exact at $(9,4)$: $33/34 = 0.970588$, and at $(10,4)$, $(11,4)$, $(12,4)$
over 8,494,200 restrictions; $P_{\mathrm{cert4}} \le e \cdot P_4 = o(P_K)$ by the
mass dominance chain; $P_{\mathrm{blk4}} \le e/(n - 2d - 3)$.
The chi-hypothesis stays alive exactly when $d^2 \log k = o(n)$: the boundary is
degree-independent through degree 4.
The degree-$\le 4$ completion inventory is exactly: free rows (cost $\Theta(n)$),
degree-2 stars ($n-1$), degree-3 stars ($n-2$), degree-4 stars ($n-3$), and alias
pairs (per query, configuration-invariant, zero information); no other class
appears.
$\mathrm{post}_4$ peaks at $1.084 \times q_{\mathrm{and\_exact}}$ at $(255,4)$, the
same finite-$n$ purity pattern as degree 3, vanishing as $\Theta(d^2/n^2)$.

Proof location.
deg4_theory.md sections 2, 3, 5, 6 (Theorem A, Theorem B (the degree-4 star lock),
Theorem C, Proposition M, REL-4, Theorem 3'', Corollary 3.3).

Verification status.
Written assembly; the $(8,4)$ classification is enumerated through witness algebra
(912,978 fixed-0 + 302,472 varying-valued $= \binom{75}{4}$); $\mathrm{post}_4$
digit-exact; the star-lock status decomposition verified exhaustively over all 90
restrictions at $(9,4)$; the same deep-zero-run residue as Theorem 3' is inherited.

Regime of validity.
$p = 2$, degree $\le 4$.

Label: PROVED (written assembly, with enumerated classification and posterior
checks; same flagged residue as 2.9).

### 2.11 Theorems 4 and 4b (the $K_j$ witness)

Statement.
Theorem 4 (unbounded budget): the $K_j$-tree's error is exactly
$$\mathrm{err}_K = \sum_{s\ \mathrm{odd}} \binom{2d}{s} 2^{2d(s-1)} \big/
2^{(2d+1)(2d-1)} = 2d \cdot 2^{1-4d}\,(1+o(1)),$$
which is $1028/2^{15} = 0.031372$ at $d = 2$ (success $0.9692$ at $(32,2)$ at
budget $\sim 4n$; measured $0.9698$ with 99% interval $[0.9665, 0.9728]$) and
$8 \cdot 2^{-15} = 2.44 \times 10^{-4}$ at $d = 4$.
Theorem 4b (budget $e$): a budget split achieves success at least
$(1 - e^{-\alpha e d/n})(1 - e^{-(1-\alpha)e(2d+1)/(2(n+1))})$, and at the optimal
split the exponent constant is $c_w = \rho/(1+\rho) = 0.55363$ at $d = 2$ and
$0.53589$ at $d = 3$, so $\mathrm{err} \le 2e^{-c_w x}$ with $x = ed/n$ (the
printed $(1-e^{-ed/(4n)})^2$ form undercharges the exponent by a factor $2.2$ at
$d = 2$).
ADDENDUM 9 correction (cap side): the matching cap term $2(1-e^{-ed/(4n)})$ is
invalid (a conjunction charged as a disjunction; violated by the adaptive optimum,
$0.55 > 0.31$ at $(96,3)$); the valid cap is $\chi(e) + (1-\chi(e))(q + A(e))$, and
the adaptive optimum's small-$x$ coefficient is $\rho x^2/2$, twice the printed
split's $\rho x^2/4$.

Proof location.
deg2_theory.md section 6 (Theorems 4 and 4b); gap_e_constants.md sections 4-5
(Theorems E3 and E4); proof_complexity.md ADDENDUM 9.

Verification status.
Written proofs; the failure count enumerated digit-exactly over all $2^{15}$
odd-row matrices at $(5,2)$; Monte Carlo at $(32,2)$ and $(48,4)$ inside 99%
intervals; the DP witness validated end-to-end (section 2.13).

Regime of validity.
$p = 2$, degree-1 queries; Theorem 4 unbounded, Theorem 4b at any budget $e \ge 2$.

Label: PROVED (written and enumerated).

### 2.12 The budgeted boundary $\mathrm{err}^*(d, d\log k) = k^{-\Theta(d^2/n)}$

Statement.
At degree $\le 2$, $p = 2$, with $e = d\log k$ and $x = d^2\log k/n$: the optimal
budgeted error is $\mathrm{err}^*(d, d\log k) = k^{-\Theta(d^2/n)}$.
Cap side: $\mathrm{success}(T) \le \chi(e) + (1-\chi(e))(q + A(e)) + o(1)$, so the
error is $\ge 1 - q - A(e) - \chi(e) - o(1)$ with $\chi(e)$ quadratic at leading
order.
Witness side: some degree-1 tree achieves error $\le 2e^{-c_w x}$.
The transition sits at $d^2 \sim n$, independent of $\log k$: for any fixed implied
constant $C$ the chi-hypothesis (error $\ge k^{-C}$) holds when $d^2 \le c\,C\,n$
and fails when $d^2 \ge C'\,C\,n$.
At degrees 3 and 4 the cap side is proved with the same boundary (Corollaries 3.2
and 3.3), and the degree-1 witness applies at every degree, so the two-sided
statement holds at degrees 2, 3, and 4.
At every prime $p$ the same boundary holds at degree $\le 2$
(odd_p_theory.md sections 5-6 and Corollary O6-d2), with better constants as $p$
grows.

Proof location.
deg2_theory.md section 8; sharpened constants in gap_e_constants.md sections 5 and
7; degree-3 and degree-4 corollaries in deg3_theory.md and deg4_theory.md; odd-$p$
mirror in odd_p_theory.md.

Verification status.
Written (both sides assembled from proved pieces); the constants are as in 2.11
and 2.13.

Regime of validity.
Both directions at degree $\le 2$; cap side at degrees 3 and 4; all $p$ at degree
$\le 2$.

Label: PROVED (written).

### 2.13 The GAP E bracket (the exact budgeted optimum, computed)

Statement.
The exact adaptive optimum of the budgeted degree-$\le 2$ game is bracketed:

| point | family-exact cap | DP model | measured best policy |
|---|---|---|---|
| (128,2), e=32 | 0.1864 | 0.1269 | 0.1264 [0.1242,0.1286] |
| (96,3), e=48 | 0.6803 | 0.5515 | 0.5499 [0.5466,0.5532] |
| (96,3), e=32 | 0.4850 | 0.3429 | 0.3422 [0.3379,0.3465] |

For comparison, the printed cap values were 0.3170, 0.9513, 0.6924, and the printed
Theorem 4b witness bound 0.0138, 0.0978, 0.0489; the best fixed-split tree measures
0.0706 at $(128,2)$.
The witness is the exact adaptive DP over states $(u,m,k,o,z)$ (Theorem E2, exact
in the certified family); the cap is Theorem E4; the residual gap is the
unharvested $(1-\chi)(q+A)$ mass (Conjecture E5, section 4).
The certification boundary at $(128,2)$ moves from $e = 58$ (printed cap,
computed) to $e \approx 80$ (sharpened cap, interpolated).
End-to-end validation: full enumeration at $(5,2)$, $e = 6$, all 983,040
configurations: realized $961024/983040 = 0.977604$ against the model $0.999330$
(delta $-0.0217$), with the DP policy still the best of every grid policy tried.

Proof location.
gap_e_constants.md sections 2-7 (Lemma E1, Theorems E2, E3, E4, the E6 sweep).

Verification status.
Cap side PROVED (written; the composition steps it reuses were discharged by
ADDENDUM 8).
Witness side: exact in-family (written DP) and MEASURED on the exact channel
(150,000 simulations per point; the model value sits inside the 99% band at all
three points); the $(5,2)$ check is enumerated.

Regime of validity.
$p = 2$, degree $\le 2$; the bracket constants are point values at the listed
$(n,d,e)$; the $e \approx 80$ boundary figure is interpolated, as its source marks.

Label: MEASURED (witness side) inside a PROVED bracket (cap side).

### 2.14 The odd-$p$ transfer (degree $\le 2$ at every characteristic)

Statement.
Every $p = 2$ closed form transfers by the single substitution "free-branch hit
mass $1/2 \to 1/p$": $q_p = (2d+1)2d/((2d+1)2d + p(n-2d))$, $\mathrm{post0}_p$,
$q_p^{\ne 0}$, the column posterior $\mathrm{colq}_p = 2d/(2d + p(n-2d))$,
$q_{\mathrm{and},p} = (M_1 + M_2)/(pM_0 + 2M_1 + M_2)$, and the row-scan
$\mathrm{post}_p(k)$ with weight $p^{-\min(t+1,\,2d-1)}$, still maximized at
$k = 0$.
A specific-value hit is weaker at odd $p$ and a nonzero hit is stronger (at
$(7,2)$, $p = 3$: $q_3^{\ne 0} = 40/49 = 0.8163$ vs $q_2 = 10/13 = 0.7692$ vs
$q_3 = 20/29 = 0.6897$).
The $K_j$-tree error at characteristic $p$ is exactly
$$\mathrm{err}_K(p) = p^{-(2d+1)(2d-1)} \sum_{s} \binom{2d}{s} p^{2d(s-1)},$$
the sum over $1 \le s \le 2d$ with $s \equiv 2d+1 \pmod p$; the dominant term is
$\binom{2d}{p-1}p^{1-2pd}$ for $p \le 2d$, and $\mathrm{err}_K(p) = 0$ exactly
when $p \ge 2d+1$ (the feasible set is empty).
The odd-$p$ budgeted cap (odd_p_theory.md's own "Theorem 3''" label) adds the
self-certification term $P_{\mathrm{sc}} \le ef(p-2)/p$ and keeps the boundary:
$\mathrm{err}^*(d, d\log k) = k^{-\Theta(d^2/n)}$ at every $p$, with aliveness
exactly when $d^2 \log k = o(n)$.
Reference values: $486/3^{15} = 3.387 \times 10^{-5}$ at $(p,d) = (3,2)$ against
$1028/2^{15}$ at $(2,2)$; exact zero at $(5,2)$, at $(3,1)$, and at $(5,1)$.

Proof location.
odd_p_theory.md sections 2, 4, 5, 6 (the substitution rule, Theorems P1, P1c,
P2'', 4'', 4b'', Lemma REL-p, the cap, Corollary O6-d2).

Verification status.
Written proofs (the odd-$p$ row-lock argument via the 2-torsion obstruction; the
failure-table count); machine-checked digit-exact against restriction enumeration
at $(7,2)$ (11,760 restrictions), $(8,2)$ (211,680), $(9,2)$ (3,810,240) at
$p = 3$; DP versus closed form at seven $(p,d)$ points; $p = 2$ regressions
reproduce the corpus numbers digit-exactly.

Regime of validity.
Degree $\le 2$ at every prime $p$; degree $\ge 3$ at odd $p$ is not covered
(section 4, O6); the general-$p$ column relation is spec-derived, not separately
machine-verified (channel_spec.md section 2.3).

Label: PROVED (written and machine-checked).

### 2.15 Theorem R (the err-form route; conditional)

Statement.
Fix the prime $p$, the constant $\ell \ge 2$, and the route constant $C \ge 1$.
Assume:
(A) every $(d_0, E)$-tree $T'$ with labels in $[n+1] \times [n]$ satisfies
$\mathrm{err}(T') \ge k^{-C}$, where err is the printed section 5 quantity over
$\omega \in \Omega(n,d_0)$, with $d_0 = \lceil (2+\log k)(h^*+1)^{c_d \ell}
\rceil$, $h^*$ the least integer with $e^{h^*/p} \ge 2(k^{c_S+C})^2$, and
$E = \lceil h^* + \log k^{c_S+C} \rceil + c_{44} d_0 \log n$;
(B1) $k(n) \ge n^3/2$;
(B2) $2 \le d_0 \le n/2$.
Then $\neg\mathrm{PHP}_n$ admits no $F_\ell(\mathrm{MOD}_p)$-refutation with $k$
steps.
The premise is exactly O2, the all-degrees budgeted err-floor, in its
design-sampled $(P_2)$ form; the printed Theorem 6.1(3), its Span conjunct, and
uniform path sampling appear nowhere in the proof.
Every hypothesis maps 1:1 to a corpus open problem; the sole mathematical premise
is O2.

Proof location.
err_form_route.md sections 3-4 (assembly lemmas: Lemma P, ENS padding; Lemma M,
solution monotonicity), with the chi_transfer.md Theorem 4 constant-direction
correction it supersedes recorded in chi_transfer.md's closing CORRECTION note.

Verification status.
Written, self-contained; every printed ingredient is quoted verbatim against the
fetched source (arXiv:2609.35927v2, pinned by content hash in bibliography.md);
no machine step.

Regime of validity.
Conditional, for every fixed $C$; the premise is open (section 4).
Slices of the premise at degrees 2, 3, and 4 are in hand (sections 2.8-2.10),
which does not feed the growing $d_0$.

Label: PROVED (written conditional proof; premise open).

### 2.16 Lemma CLS at general $d$ (the degree-2 relation inventory)

Statement.
Lemma CLS (lemma_m.md section 3.3's naming) in its two halves, current final form.
(i) Every diagonal degree-2 column (every matching-2 column) varies at general
$d$, and is marginally fair by the balance lemma: the matching hierarchy of
section 2.2 with base = the completion lemma cor:coin and step = the star-row
argument (cls_cnt.md section 2).
(ii) The algebraic core Q-A: the determined relations of degree $\le 2$ are
generated exactly by the inventoried families, in dimension form
$(V \oplus \langle e_0\rangle) \cap S_{\le 2} = V_{\le 2} \oplus \langle e_0\rangle$
with $V_{\le 2} = \mathrm{span}\{Q_i,\ Q_i x_{ab},\ b_{ij},\ C,\ H\}$
(cls_cnt.md section 3.1).
The route is a d-uniform degree-truncated Buchberger argument: every
S-polynomial of a generator pair with lcm-degree $\le 2$ reduces to zero within
degree $\le 2$, via the master identities M1, M2, M3, I1, M5 (universal ring
identities at every $d \ge 2$; cls_cnt.md section 3.3).
Together with the covering theorem (every support of a nonzero element of the
varying-coordinate projection contains a full row, a full star, a DS, a UU, an
OFF, or a catch-all-class support; cls_cnt.md section 4.2) this is the repaired
block-free identification of section 2.3 at general $d$.

Proof location.
cls_cnt.md sections 2-4; ADDENDUM 11.

Verification status.
The master identities are machine-checked at all position instances of the
$5 \times 4$ and $7 \times 6$ rectangles, and the generic sweep checks every
lcm-$\le 2$ pair mechanically (465 and 1225 S-polynomials).
The dimension identity is machine-verified exactly at $(4,2)$
($\dim(V \cap S_{\le 2}) = 165$) and at $(6,3)$ with degree-3 shifts present
($\dim = 511$; rank off $S_{\le 2}$ 11,599).
Engine caveat of record: the sweep's engine lemma (Lemma TB, cls_cnt.md section
3.2) is FALSE as stated (section 3); the $t = 2$ conclusion is re-proved by the
repaired completion engine (degree-capped Buchberger completion with
machine-enforced span neutrality) at $5 \times 4$ and $7 \times 6$, and is
separately anchored by the exact $(6,3)$ dimension computation (cls_cnt.md
closing correction note; inv3.md section 3.2).
The replacement engine-validity lemma (genuine multivariate-division/Groebner
theory for the dehomogenized problem) is the named open repair (inv3.md
DOWNGRADE block; GUIDANCE.md priority 1); the classification Lemma L-CLASS is
open and absorbed by the catch-all.

Regime of validity.
Unconditional at $d \le 3$ (the machine anchors, including the $(6,3)$ exact
dimension check).
The general-$d$ form carries the cor:coin base caveat (section 2.2) and the
engine-validity caveat above; the five-family inventory supersedes the
three-family inventory the lemma's statement originally accompanied (section
2.3).

Label: PROVED (written d-uniform argument, machine-checked identities and exact
dimension anchors; unconditional at $d \le 3$; the general-$d$ engine lemma is a
named open repair).

### 2.17 Lemma CNT (the completion count at general $d$)

Statement.
The probability that a budget-$e$ window contains the support of any relation of
the five-family inventory obeys $\varepsilon_{full}(e,n,d) = (1 + o(1))\,
\varepsilon_{headline}$ at every fixed $d \ge 2$ with $e = o(n)$, where
$\varepsilon_{headline} = \frac{A}{2}\big[(e/n)^{2d} + (2e/(n-1))^{2d-1}\big]$
and $A = (2d+1)/(n+1)$ (cls_cnt.md section 5.1).
The enlarged inventory (DS, UU, OFF, catch-all) contributes only dominated
$\Delta$ terms, absorbed by the multiplicative $(1 + o(1))$.
The headline form is tight: a deliberate star probe matches it up to factorial
slack and a deliberate DS probe matches $\Delta_{DS}$ (cls_cnt.md section 5.2).
Non-adaptive: PROVED over the full inventory.
Adaptive (Proposition CNT-A): $P[E_{full}] \le \varepsilon_{full}(e,n,d)\,
\exp(2ed/n) + O(e/n)$; B1 (the per-answer classification) is proved, B2 (the
distortion product) is reduced and closes in regime for any polynomial loss, so
in the regime $d^2 \log k = o(n)$ the distortion is $1 + o(1)$ and the
non-adaptive bound is the operative adaptive form.
The minimum varying-support size over the whole inventory is $2d$, achieved only
by rows and degree-2 stars, so at $e < 2d$ no event can fire and the transfer is
exact.

Proof location.
cls_cnt.md sections 5.1-5.3 (the bound, tightness, Proposition CNT-A, lemmas B1
and B2); the degree-$k$ extension in all_degrees.md sections 2.2 and 2.4.

Verification status.
Written proof; the $\Delta$-dominance table machine-checked at six printed
points (at $(128,2)$, $e = 32$: headline $2.6 \times 10^{-3}$ against all
$\Delta$ terms $\le 2 \times 10^{-7}$).

Regime of validity.
$p = 2$, degree $\le 2$ (degree-$k$ form in all_degrees.md), general $d$,
$e = o(n)$; the adaptive form in regime modulo B2; the exact adaptive constant
at the boundary $d^2 = \Theta(n)$ is open and the headline form is operative
there, exactly as for Lemma REL.

Label: PROVED (written; non-adaptive over the full inventory, headline tight;
adaptive in-regime modulo named lemma B2).

### 2.18 Theorem 3 at general $d$ in regime (the degree-2 slice of O2, upgraded)

Statement.
Theorem 3 (section 2.8) stands at general $d$: its step (6) is closed at general
$d$ by sections 2.16 and 2.17, so at $p = 2$, general $d$, budget $e = o(n)$
with $d^2 \log k = o(n)$, every adaptive degree-$\le 2$ tree satisfies the same
cap and the same sharpened certificate form
$$\mathrm{success}(T) \le \chi(e) + (1 - \chi(e))\,(q_2^* + A(e))\,(1 + O(e/n) + o(1)),$$
with $q_2^* = \max(q,\ q_{\mathrm{and\_exact}},\ q_{\mathrm{mix}})$
(all_degrees.md section 3.1).
No constant shifts: $q$, $q_{\mathrm{and\_exact}}$, $q_{\mathrm{mix}}$, the
regime line $c(c-1) \ge 2d^2(4d^2 - 1)$, and $\chi(e)$ are
inventory-independent (the posteriors are computed on block-free windows and
the covering theorem preserves the fresh-bit identification on them); the
$o(1)$ now absorbs $\varepsilon_{full}$ instead of the three-family
$\varepsilon$, still $o(1)$ in regime.
MIXTURE-d caveat in the regime line (all_degrees.md section 5.2 item 2, updated
by ADDENDUM 12): the cap family covers monomial queries plus linear forms, and
arbitrary $\mathbb{F}_2$ mixtures are covered only at $d \le 3$ (sections 2.8
and 2.19); O2's literal quantifier at $d \ge 4$ therefore retains the MIXTURE-d
scope gap.

Proof location.
all_degrees.md section 3.1, on cls_cnt.md sections 3, 5, and 6 and the degree-2
machinery of section 2.8 unchanged.

Verification status.
Written assembly; the consumed lemmas are sections 2.16 and 2.17; the
constant-invariance check is cls_cnt.md section 6 and all_degrees.md section
3.1.

Regime of validity.
$p = 2$, degree $\le 2$, general $d$, $e = o(n)$, $d^2 \log k = o(n)$, modulo
the three named caveats (the cor:coin base; B2 in-regime; L-CLASS absorbed by
the catch-all); unconditional at $d \le 3$; this is the strongest all-$d$ slice
of O2 and it is new with the newest wave.

Label: PROVED (written assembly at general $d$ in regime, with the named
caveats; unconditional at $d \le 3$).

### 2.19 Theorem M3-D (MIXTURE-3; MIXTURE-d closed at $d \le 3$)

Statement.
Every adaptive tree of budget $e$ using arbitrary $\mathbb{F}_2^{\le 3}$ queries
(the full printed degree-$\le 3$ class; normal form: a constant, singles,
non-degenerate diagonals, matching triples) satisfies
$$\mathrm{success}(T) \le \min\big(1,\ q_3^{\mathrm{mix}}(n,d) +
P_{\mathrm{adj,mix3}}(e) + P_K(e) + P_{\mathrm{wedge}}(e) + P_Z(e) +
P_{\mathrm{blk3}}(e) + O(e/n) + o(1)\big),$$
with $q_3^{\mathrm{mix}} = q_3^* + \epsilon_3$, $\epsilon_3 > 0$ at every
measured point and finite-$n$ only: $+0.0169$ absolute at $(15,3)$, $+0.0048$ at
$(31,3)$, $+5.2 \times 10^{-5}$ at $(63,3)$, and
$\mathrm{max}/\mathrm{post}_3 = 1.000000$ by $(1023,3)$ (mixture3.md Theorem
M3-A).
The maximizers are monomial-star mixtures through the output pair (the degree-2
star-3M family through $n \sim 31$, disjoint triple-stars beyond).
Mechanism: the killed-branch self-exclusion of Theorem M-A extends verbatim
(Theorem M3-1; the killed-branch answer-1 mass is exactly 0 for every
through-output configuration, machine-checked); no new single-query certificates
(Theorem M3-B, 0 of 1,474 enumerated configurations); the degree-3 mixture Z
form folds a covered certificate at equal budget (Proposition M3-E).
Aliveness (Corollary M3-D1): error $\ge k^{-O(1)}$ exactly when
$d^2 \log k = o(n)$, the same condition as the covered class.
Budgeted verdict (measured): at $(15,3)$ no mixture strategy beats the covered
champions at any tested budget; the dominant covered champion is the $K_j$
column parity queried as one linear-form query per column (0.986 at budget 30),
and the $(7,3)$ mixture win at budget 10 is the $c = 1$ degeneracy, gone by
budget 30.
Consequence: the MIXTURE-d scope gap is closed at $d \in \{2, 3\}$ with
constant-only repairs and is open at $d \ge 4$ (mixture3.md section 10; ADDENDUM
12).

Proof location.
mixture3.md sections 1-7 and 9-10 (Theorems M3-1, M3-2, M3-A, M3-B, Proposition
M3-E, Theorem M3-D, Corollary M3-D1); ADDENDUM 12.

Verification status.
Written assembly with exactly the modulo set of Theorem 3' plus two marked
inherited pieces (the rate-weighted elevation sup is measured at degree 2 and
not separately re-measured at degree 3; the two-query mixture certificate
classification beyond the folded families is conjectured); dual-engine
validation digit-exact (4,648 queries x 2 answers over all 56 restrictions at
$(7,3)$, 0 mismatches) and sampled at $(15,3)$ within 5-sigma; exact rational
grid over twelve $(n,d)$ points.

Regime of validity.
$p = 2$, degree $\le 3$, $e = o(n)$; the scan is support-$\le 3$ exhaustive with
sampled wider families, and dominance beyond support 3 is conjectured (the
per-$\rho$ law first leaves $\{0, 1/2\}$ at support 4, mixture3.md section
2.2).

Label: PROVED (written assembly; one measured constant inside the mixture term;
marked pieces as listed).

### 2.20 Theorem 3''' (the degree-5 budgeted cap; assembly at the machine points)

Statement.
Every adaptive tree of budget $e$ over degree-$\le 5$ monomial queries and
linear forms satisfies
$$\mathrm{success}(T) \le \min(1,\ q_5^* + P_{\mathrm{adj}} + P_K +
P_{\mathrm{cert5}} + P_{\mathrm{blk5}} + o(1)),$$
with $q_5^* = \max(q,\ q_{\mathrm{and\_exact}},\ \mathrm{post}_3,\
\mathrm{post}_4,\ \mathrm{post}_5)$, $P_{\mathrm{cert5}} \le e \cdot P_5 =
o(P_K)$, and $P_{\mathrm{blk5}} \le e/(n - 2d - 4)$ (deg5_theory.md section
6.1).
The mass chain $P_{k+1} < P_k$ is now proved at general $k$ (Proposition M5,
strict event inclusion), upgrading the deg4 measured chain.
$\mathrm{post}_5 = (b_0 + 4b_1 + 6b_2 + 4b_3)/(2b_5 + b_0 + 5b_1 + 10b_2 +
10b_3 + 5b_4)$ is digit-exact at $(11,5)$ ($46/47$), $(12,5)$ ($703/733$),
$(13,5)$ ($18362/19517$, 624,624 restrictions); all single-pass posteriors
through $k = 5$ share the leading form $2d^2/n$ (Conjecture NAL proved for
$k \le 5$); the finite-$n$ purity lift peaks at $1.1297 \times
q_{\mathrm{and\_exact}}$ at $(255,5)$ and vanishes as $\Theta(d^2/n^2)$.
The degree-5 classification (fixed-0 line-pair, alias with the six-pattern
reduction system, matching-5 varying by Theorem A at $k = 5$) is proved, with
the partition identity $125{,}446{,}882 + 21{,}356{,}390 = 146{,}803{,}272 =
\binom{114}{5}$ exact at $(10,5)$, and a sparse degree-$\le 3$ sweep at $(10,5)$
(234,136 columns; 100,156 determined, all inventoried) verifying the partition
by sweep for degree $\le 3$ at $d = 5$, the first sweep beyond $d \le 3$.
The chi-hypothesis stays alive exactly when $d^2 \log k = o(n)$: the boundary is
degree-independent through degree 5; measured cap at $(4095,5)$, $e = 80$:
0.0816, alive.
General-$d$ status NOT upgraded: the cap form is stated and its constants are
inventory-independent, but the proof at general $d$ consumes INV(5); REL-5's "no
other class" is exactly the open SPARSE-d/INV-d lemma, and the completion engine
whose $t = 3$ closure at $d = 4$ would have fed INV(3) is downgraded (section 3;
section 2.21).

Proof location.
deg5_theory.md sections 2-6 (Lemmas W5 and A5, Theorem A at $k = 5$, Theorem B5,
REL-5, Theorem C5, Proposition M5, Theorem 3''', Corollary 3.4); general-$d$
status per all_degrees.md section 3.2.

Verification status.
Written assembly with the two inherited JDP composition flags; registered run
chi_deg5_check.py (21 s, all pass): the Theorem-A base at the $(10,5)$ slice,
alias and star witnesses, the sparse sweep, digit-exact posteriors, the mass
chain at ten grid points, and the F1-certain search at $(11,5)$ (unexplained 0).

Regime of validity.
$p = 2$, degree $\le 5$; an assembly at the machine points and a printed form at
general $d$ modulo INV(5).

Label: PROVED (written assembly with machine-checked and enumerated pieces at
$d = 5$); the general-$d$ form is INFERRED (premise INV(5) open).

### 2.21 Theorem 3-gen (the all-degrees budgeted cap; conditional) and the INV(d) premise

Statement.
Fix $p = 2$, $d \ge 2$, $k \ge 2$ with $\log k \ge 1$, and budget $e = d\log k$.
Assume INV(d) (inventory completeness through degree $d$: the Q-A identity
$(V \oplus \langle e_0\rangle) \cap S_{\le t} = V_{\le t} \oplus \langle
e_0\rangle$ at every $t \le d$, plus the covering of every support by a full
row, a degree-$j$ star, a DS, a UU, an OFF, or a catch-all support;
all_degrees.md section 4.1) and B2.
Then every adaptive tree of budget $e$ whose queries are degree-$\le d$
monomials or linear forms satisfies the explicit cap of Theorem 3-gen (with
$q_d^* = \max(q,\ q_{\mathrm{and\_exact}},\ \mathrm{post}_3, \ldots,
\mathrm{post}_d)$ and the degree-$d$ completion bound $\varepsilon^{(d)}$), and
if $d^2 \log k = o(n)$ then $\mathrm{err}(T) \ge 1/2 - o_d(1) \ge k^{-O(1)}$;
with the degree-1 witness the two-sided form $\mathrm{err}^*(d, d\log k) =
k^{-\Theta(d^2/n)}$ holds at every fixed $d$ granting INV(d) (all_degrees.md
sections 4.2-4.3).
Premise status: INV(2) is PROVED at general $d$ (sections 2.16 and 2.17); at
$d = 3$ the $t = 3$ layer is a tautology ($V = V_{\le 3}$) and step (6a) is
closed by the $(6,3)$ full sweep, independent of the downgraded engine; INV(d)
for $d \ge 4$ is OPEN at every $t \ge 3$ layer.
The one closure claimed beyond the sweeps (INV(3)(i) at $d = 4$, via the
degree-truncated completion engine) is DOWNGRADED to engine output, unverified
(section 3; inv3.md DOWNGRADE block), so nothing downstream of it is established:
Theorem 3-gen's premise is OPEN at $t \ge 3$, and inv3.md's tightened premise
table ("INV(4) has only its $t = 4$ layer open") is not consumed.
Everything downstream of the downgraded INV(3) is therefore INFERRED at best:
the all-degrees assembly is proved as a conditional, and its condition is the
corpus's single mathematical gap (all_degrees.md section 5.2 item 1).

Proof location.
all_degrees.md sections 4.1-4.3 (the assembly, every step labeled) and section 5
(the final O2 status); premise downgrade per inv3.md and GUIDANCE.md priority 1.

Verification status.
Written assembly with each step labeled (transfer; certificate-free leaves;
certificate charge; completion charge; assembly; regime arithmetic; witness
side), each proved modulo its named lemma; the premise is the open content,
machine-verified at the swept points ($(6,3)$ full; $(8,4)$ and $(10,5)$
degree-$\le 2$; $(10,5)$ degree-$\le 3$).

Regime of validity.
$p = 2$, every fixed $d$ granting INV(d); unconditional at $d = 2$ modulo the
standing cor:coin caveat and B2; conditional at every $d \ge 3$ in the $t \ge 3$
layers.

Label: PROVED (written assembly at $d = 2$); INFERRED at general $d$ (the
premise INV(d) is open at $t \ge 3$).

## 3. Retracted and superseded statements

- Theorem T's artifact law (the two-phase tree's error exactly $2^{-(2d+1)}$,
  "phase 2 never fails given certification"): a coin-model simulator artifact; the
  literal-law error is $5 \cdot 2^{-(2d+1)}(1+o(1))$, the mechanism is dead on the
  true pipeline ($Q_i$ answers 0 on every pigeon), and the tree is dominated by
  Theorem 4.
  Correction record: cert_floor.md "Correction to Theorem T's record";
  proof_complexity.md correction block; channel_spec.md section 6 item 5.
- Proposition D (the non-adaptive cap at all query degrees, success
  $\le (s+1)f + o(1)$): false as stated; the rc counting tree is non-adaptive with
  exact success 0.9067 at $(64,2)$ against the cap 0.625; the surviving form covers
  the variable/monomial non-adaptive class only.
  Correction record: proof_complexity.md correction block, "Proposition D: FALSE AS
  STATED"; ADDENDUM 2 item 5.
- The $2^{-\Theta(d)}$ certification-floor conjecture (with Theorem T's optimality):
  false; the exact unbounded coin-channel floor is $2^{-\Theta(d^2)}$ (Theorem F)
  and the true-pipeline optimum is 0 (Theorem 5).
  Correction record: cert_floor.md "Scope and outcome"; open_problems.md O4.
- Reading B of Lemma B.1 (the literal "any pair $p$ not in $S$" quantifier):
  falsified at 15/35 grid points (the shared-coordinate answer-1 lift); repaired to
  the disjoint-pair reading, and Lemma B.1's step (2) negative-association instance
  retracted as false (exact counterexample, covariance $+19/1008$ at the in-regime
  point $(8,1)$); the proof is re-based on Lemmas D1 and D3.
  Correction record: proof_complexity.md REPAIR NOTE and ADDENDUM 8;
  thmB_stress.md; jdp_demod.md Proposition D4.
- The Pi-form cap (the printed certificate term $2(1-e^{-ed/(4n)})$ and
  split-product cap forms): invalid as a cap term (a conjunction charged as a
  disjunction; violated by the adaptive optimum, $0.55 > 0.31$ at $(96,3)$); the
  valid cap is $\chi + (1-\chi)(q+A)$.
  Correction record: proof_complexity.md ADDENDUM 9; gap_e_constants.md Theorem E3.
- The "printed Theorem 6.1(3) is false as printed" over-claim: retracted; (3) is a
  hypothesis about the paper's own constructed tree, not a paper claim, so it
  cannot be false as printed; what stands is the corpus's INFERENCE that under the
  universal-quantifier reading a trivial row-sum tree violates (3), a reading gap
  pending expert confirmation.
  Correction record: proof_complexity.md ADDENDUM 4 and its DOWNGRADE note;
  chi_transfer.md section 5 item 2; channel_spec.md section 6 item 9.
- The confidence figure ("P != NP, about 93% confidence"): a subjective prior, not
  derived from this corpus; removed everywhere.
  Correction record: GUIDANCE.md item 1; GOAL.md section 1; LOG.md 2026-10-04
  (the clues.md position statement downgraded).
- Lemma TB (the truncated-Buchberger reduction lemma, cls_cnt.md section 3.2: if
  every S-polynomial of a pair whose leading-monomial lcm has degree $\le t$
  reduces to zero within degree $\le t$, then $I \cap S_{\le t} = W_t$): FALSE as
  stated.
  Counterexample: $G = \{x^2,\ xy + 1\}$ over $\mathbb{F}_2[x,y]$, $t = 2$: the
  only pair has lcm-degree $3 > 2$, so the hypothesis is vacuous, yet
  $1 \in I \cap S_{\le 2}$ and $1 \notin W_2$ (the xy-coefficient argument proves
  the negation).
  The $t = 2$ CONCLUSION of the cls-cnt record survives: re-proved by the repaired
  completion engine at $5 \times 4$ and $7 \times 6$, and separately confirmed by
  the exact dimension computation at $(6,3)$ (sections 2.16 and 2.17).
  Correction record: cls_cnt.md section 3.2 correction block and its closing
  correction note; inv3.md sections 2.3-2.4; ADDENDUM 13; GUIDANCE.md priority 2.
- The INV(3) $t = 3$, $d = 4$ closure (inv3.md's "INV(3)(i) PROVED at $d = 4$
  [MV]" via the degree-truncated Buchberger completion engine): DOWNGRADED to
  engine output, unverified.
  Reviewer-verified defects: the engine never examines pairs with lcm-degree
  $> t$, whose S-polynomials can have degree $\le t$ (so the exotics that would
  refute the claim are invisible to it); the verification pass can time out
  mid-scan and still report closure; "all pairs" is overstated; and the "four
  independent configurations" are conjugate or overlapping (orders A and C by
  variable relabeling; G and G' span the same $W_t$).
  Nothing downstream is consumed (section 2.21); the $t = 2$ conclusion survives
  independently.
  Correction record: inv3.md DOWNGRADE block (2026-10-04); GUIDANCE.md priority 1.

## 4. Open problems (current forms)

- O2, the all-degrees budgeted err-floor (the open core).
  Is there a constant $C$ such that every budgeted adaptive tree ($e = d\log k$
  queries, degree $\le d$ over $\mathbb{F}_2$) in the $\Omega(n,d)$ pipeline at
  $p = 2$ errs with probability $\ge k^{-C}$?
  The cap side is assembled at every fixed degree granting INV(d) (Theorem 3-gen,
  section 2.21): degrees 2 through 5 are proved at their degrees (Theorems 3, 3',
  3'', 3'''; the same $d^2 \sim n$ boundary through degree 5), degree 2 stands at
  general $d$ in regime (section 2.18), and under INV(d) the boundary is
  degree-independent at every $d$.
  The open core, in order (all_degrees.md section 5.2): (i) INV-d at $t \ge 3$,
  the single mathematical gap (the $t = 3$ engine closure at $d = 4$ is
  downgraded, section 3; the honest next target is a correct engine lemma or an
  independently audited computation at a feasible rectangle); (ii) MIXTURE-d at
  $d \ge 4$ (closed at $d \le 3$, section 2.19); (iii) the boundary constant at
  $d^2 = \Theta(n)$; (iv) intermediate budgets $e = \Theta(n)$ (deg2_theory.md
  open item 3); (v) the exponent constants (Conjecture E5 below).
  Sub-items: the multi-class deep-zero-run composition (deg3_theory.md open
  item 3) and the standing small items (the cor:coin base; NAL at $k \ge 6$; the
  degree-$\ge 3$ write-out of the B1/B2 bookkeeping).
  Failure mode of record, restated on support sizes (cls_cnt.md correction 5;
  all_degrees.md section 3.2): a relation class whose minimal support is small
  ($\Theta(d)$) and transcript-identifiable and not a supersupport of an
  inventoried configuration; the deg4 forward note's "no sub-$\Theta(n)$
  completion cost" is false in form (the DS/UU supports are $\Theta(d)$) and
  harmless in regime, and the induction tracks support sizes, not query costs.
- Lemma CLS and Lemma CNT (the general-$d$ degree-2 transfer): CLOSED in regime
  (sections 2.16 and 2.17; this entry supersedes their former open listing here).
  CLS: every diagonal degree-2 column varies at general $d$, and Q-A holds with
  the machine anchors at $(4,2)$ and $(6,3)$; the general-$d$ engine lemma is the
  named open repair (section 3).
  CNT: the headline form is tight, the non-adaptive bound is proved over the full
  five-family inventory, and the adaptive case is closed in regime modulo B2.
  Residuals, folded into O2's open core: Lemma L-CLASS (the minimal-support
  classification beyond the five families, harmless for counting), B2's exact
  form, and the boundary constant at $d^2 = \Theta(n)$.
  Naming note: odd_p_theory.md uses "Lemma CNT" for its nonzero-count law; the two
  are unrelated.
- O6 at degree $\ge 3$, odd $p$.
  Degree $\le 2$ is settled at every $p$ (section 2.14).
  Open: the odd-$p$ degree-3 recompute (the $(6,3)$ kernel classification over
  $\mathbb{F}_p$; the tuple-based GF($p$) machinery does not reach that scale),
  with the degree-3 template (star sum rules, wedge/Z, posteriors under
  $1/2 \to 1/p$) conjectured to transfer; and the odd-$p$ analogue of the
  degree-$\ge 5$ quantifier (odd_p_theory.md section 9).
- Conjecture E5 (the residual mass).
  $\mathrm{success}^*(e) = W_{dp}(e) + o((1-\chi(e))\,q)$: no tree realizes
  materially more of the $(1-\chi)(q+A)$ mass than the certified-family fallback.
  Falsifiable: at $(128,2)$, $e = 32$, an adaptive degree-$\le 2$ tree above
  $0.135$ refutes it, and above $0.20$ refutes the sharpened cap itself
  (gap_e_constants.md sections 8 and 10).
- The chi-transfer quantifier question (INFERENCE, pending expert confirmation).
  Whether Theorem 6.1's hypothesis (3) quantifies over all budgeted trees (the
  corpus's reading, forced by the reduction logic, under which a trivial row-sum
  tree gives $\chi = k^{-\Theta(d)}$ with $\mathrm{err} \ge 1/2$; chi_transfer.md
  Theorem 3) or only over the paper's own constructed tree (the literal grammar).
  Under either reading the route of record is Theorem R with premise O2; the
  question decides only how the printed conditional is described.
  The instrument is note_to_author.md, a draft reading-check question; sending it
  is the owner's reserved decision.

## 5. What would change this picture

- A new determined-relation class with sub-$\Theta(n)$ completion cost at some
  degree $\ge 5$ would break the per-degree cap induction and reopen O2's boundary.
- A value-determined diagonal degree-2 column at some $d$, or an exotic relation on
  an alias-aware block-free window, would falsify Lemma CLS and force a
  recomputation of the degree-2 constants there.
- An adaptive tree whose completion probability exceeds $\varepsilon_{full}(e,n,d)\,
  e^{2ed/n} + O(e/n)$ over the five-family inventory would falsify Proposition
  CNT-A or lemma B2 (cls_cnt.md section 5.3).
- A window at $(4,2)$ or $(6,3)$ whose true law deviates from fresh-bit and whose
  support contains none of the five families would falsify the covering theorem
  and with it INV-2 (searchable now by minimal-codeword enumeration of
  $\overline{V}$, dimensions 166 and 512).
- A $\ge 3$-star cancellation chain whose minimal support is small ($\Theta(d)$)
  and transcript-identifiable and not a supersupport of any pair configuration
  would create a sub-$\Theta(n)$ completion mechanism and break
  $P_{\mathrm{blk}}$ at that degree: the corpus's named O2 failure mode, located
  inside INV-d (all_degrees.md section 5.3).
- A degree-$\ge 4$ mixture tree beating the monomial-class cap at a measured point
  would show MIXTURE-d bites and reopen the scope item with content (closed at
  $d \le 3$, section 2.19).
- An $F_p$ audit finding $L(Q_i^\rho) \ne 0$ at any pigeon or any $p$ would
  collapse the characteristic-uniform channel law and force O6's redevelopment from
  scratch.
- An adaptive degree-$\le 2$ tree at $(128,2)$, $e = 32$, exceeding success $0.1864$
  would falsify the sharpened cap; exceeding $0.135$ would falsify Conjecture E5.
- A budgeted tree with error $< k^{-C}$ at $d^2 \gg n$ (equivalently, the $(64,4)$
  versus $(64,8)$ success cliff failing to appear) would break the $d^2 \sim n$
  boundary.
- A determined matching-$k$ column at any $(2d,d)$ would contradict Theorem A's
  base and the balance lemma.
- Expert confirmation that (3) is not universally quantified would retire the
  ADDENDUM 4 violation reading (the route of record is unaffected either way).
- An author correction to Definition 4.3's $g^\rho$ clause or the vanishing
  condition would dissolve the channel frame every result here is phrased on.
- A super-polynomial AC0[2]-Frege lower bound, or a budgeted tree with success
  $\ge 1 - k^{-O(1)}$ at $d = (\log k)^{O(\ell)} \le \sqrt{n}$, would close O2 from
  opposite sides and empty the corpus's open core.

## 6. Consolidation note

This pass folds the newest wave (all_degrees.md, cls_cnt.md, inv3.md,
mixture3.md, deg5_theory.md) into sections 2, 4, and 5, and adds the two
retractions of section 3; nothing was repaired silently.
No live inconsistency between sources was found; the one sequencing artifact is
that all_degrees.md's MIXTURE-d line (written before mixture3.md) says the
mixture class is covered only at $d = 2$, superseded by the dated ADDENDUM 12
and stated here in the resolved form (closed at $d \le 3$, section 2.19).
Every number above was taken from regeneration_2026-10-04.md or from the cited
source document.
Editorial notes, not inconsistencies: the labels "Theorem B" (the proof_complexity.md
cap versus the deg4_theory.md star-lock theorem), "Theorem R" (the cert_floor.md
parity tree versus the err_form_route.md route theorem), "Theorem 3''" (the
deg4_theory.md cap versus the odd_p_theory.md cap), and "Lemma CNT" (the lemma_m.md
completion count versus the odd_p_theory.md nonzero-count law) each name two
distinct objects; this file disambiguates by citation.
The newest wave adds "Theorem 3'''" (the deg5_theory.md cap, a third distinct
object in that family) and makes "Lemma CNT" name the cls_cnt.md completion count
of section 2.17, still distinct from odd_p_theory.md's law.
One channel-scope item not listed in section 3 because it is proved on its own
channel: cert_floor.md Theorem R (the rows-and-columns parity tree) is proved for
the coin channel and has no true-pipeline existence (its $Q_i$ half answers 0
determinedly there); its surviving half is Theorem 4 (deg2_theory.md section 10
item 3).
Maintenance: sections 2.16-2.21 were added together with their PROVED_CLAIMS and
REQUIRED_CLAIMS entries in proved_registry.py in the same change; when a result
lands or dies, update this file together with docs/theorem_map.md, so the one
current statement and the map stay in sync.
