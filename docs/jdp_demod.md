# jdp_demod: de-modularizing the JDP steps (GAP D discharge, 2026-10-04)

Result of the rigor agent (GAP D brief). Status: analysis, not peer-reviewed.
Scope: every negative-association / JDP / coupling citation in
`deg2_theory.md` Theorem 3's proof and its supporting lemmas, plus the
inheritance chain into `proof_complexity.md` Lemma B.1 and
`deg3_theory.md` Theorem 3'. Deliverable rule respected: no other corpus
file was edited and no LOG.md entry was written.
Marker conventions: PROVED (proof in this file), MEASURED (executed exact
computation, Section 10), UNVERIFIED (could not check against the primary
source this session), OPEN (not discharged).

## 1. Verdict in brief

1. PROVED: the two modulo-JDP steps of Theorem 3 are discharged by an
   elementary status-atom conditioning argument (Lemmas D1 and D2 below).
   No negative association is needed anywhere in Theorem 3's proof.
2. PROVED: the corpus's existing NA usage for the freeness families
   $\{P_i\}$, $\{H_j\}$ and their union is a genuine classical instance,
   and a self-contained page proof is provided (Lemma D3), so Lemma B.1's
   step (1) no longer needs its citation either.
3. FINDING (correction-class): Lemma B.1's step (2) citation is misapplied
   and the claimed instance is FALSE: the pair-product family
   $F_q = P_i H_j$ is NOT negatively associated. MEASURED counterexample
   inside the model's parameter regime, exact covariance $+19/1008 > 0$ at
   $(n,d) = (8,1)$. The corpus's own Reading B falsification
   (thmB_stress.md, 15/35 FAILs) is the numerical shadow of this false
   instance. The step is not needed and is replaced.
4. PROVED: Theorem 3 restated with zero black-box citations (Section 6);
   Corollary 3.1 and the Section 8 boundary are unchanged.
5. deg3_theory.md Theorem 3': the distant-evidence half of its JDP flag
   transfers and is discharged; the multi-class deep-zero-run half remains
   OPEN (it was already open independently of JDP as deg3 open item 3).
6. UNVERIFIED: the internal Joag-Dev-Proschan theorem numbers quoted by
   Lemma B.1 ("Section 3.n", "Theorem 8", "Theorem 10"). Project Euclid
   and JSTOR are access-blocked this session; only the abstract is
   quote-anchored. Nothing in the discharged proofs relies on those
   numbers.
7. FINDING (citation anchor): the Dubhashi-Ranjan citation in Lemma B.1
   step (1) is a mis-anchor. The full BRICS report text of that paper
   contains no without-replacement content; its occupancy theorem is for
   i.i.d. throwing (multinomial-type counts), a different experiment.

## 2. The audit

Every NA / JDP / coupling citation in the Theorem 3 orbit, with line
references and verdicts.

| # | Location | Claim at that location | Cited source | Verdict |
|---|----------|------------------------|--------------|---------|
| A1 | deg2_theory.md:28-29 | header marker: "modulo JDP" marks the step resting on "the same negative-association citation standard the corpus's Lemma B.1 already accepts" | Lemma B.1 | discharged here (Sections 5-6) |
| A2 | deg2_theory.md:238-243 | each subsequent same-line query answers 1 with conditional probability at most $q(2d-1)/(2(n-1))$; the past's hit elevates row-freeness posterior to at most $q$ | Theorem 2(iv) + implicit NA composition | discharged: exact at the coin channel (MEASURED), upper bound on the true channel (MEASURED); coupling written out as Lemma D2 |
| A3 | deg2_theory.md:256-260 | "the multi-row composition is modulo JDP, the same citation status as Lemma B.1" | JDP via Lemma B.1 | discharged: Lemma D1 + D2; no NA needed |
| A4 | deg2_theory.md:266-269 | "distant evidence only depresses (exact one-distant-hit computation, NA composition modulo JDP)" | JDP via Lemma B.1 | discharged: Lemma D1; phrasing corrected, see Finding F4 |
| A5 | deg2_theory.md:270-271 | the $O(e/n)$ term is "the finite-population depletion of Lemma B.1, valid on the product channel" | Lemma B.1 steps (1)-(4) | discharged: Lemma D1 gives the explicit form $f_e$ and the difference constant |
| A6 | deg2_theory.md:271-272 | QED marker: "two modulo-JDP steps marked, both inherited from the corpus's existing standard" | Lemma B.1 | both steps now proved, marker can be dropped |
| A7 | deg2_theory.md:440-442 | open item 4: the modulo-JDP composition steps, "not yet machine-checked" | - | closed as stated: proved here, and the exact values cross-check thmB_stress digit-for-digit (MEASURED) |
| A8 | proof_complexity.md:320-333 | step (1): $\{P_i\}$, $\{H_j\}$ are the canonical without-replacement NA families (JDP "Section 3.n and Theorem 8"; D-R "for the occupancy form"); joint family NA by JDP closure ("their Theorem 10") | JDP 1983, D-R 1998 | instance genuine; elementary proof supplied (Lemma D3); JDP numbering UNVERIFIED; D-R anchor misapplied (Finding F2) |
| A9 | proof_complexity.md:334-338 | step (2): $\{F_q\} = \{P_i H_j\}$ over all pairs is NA by JDP closure "products of NA random variables over disjoint subfamilies are NA" (their Theorem 10) | JDP 1983 | FALSE as stated: the factor subfamilies are not disjoint across members, and $\{F_q\}$ is not NA (Proposition D4, MEASURED) |
| A10 | proof_complexity.md:339-346 | step (3): NA closure under "coordinate-wise functions of disjoint indicator supports" licenses conditioning on the transcript | NA closure properties | replaced: answer events factor through the status atom (Lemma D1), no closure lemma needed |
| A11 | proof_complexity.md:347-354 | step (4): "the standard finite-population (hypergeometric) depletion" giving $f_e$ | elementary | proved: Lemma D1 with explicit constant; MEASURED at (8,1) |
| A12 | deg3_theory.md:73, 330-337, 346 | Theorem 3': "MULTI-evidence composition (deep zero-runs across classes, distant evidence) ... carried modulo the same JDP negative-association citation standard" | JDP via deg2 Theorem 3 | distant-evidence half discharged (Section 8); deep-zero-run multi-class half OPEN (independent of JDP) |

Items verified clean (no NA, no coupling citation, no action needed):

- Theorem 1 (deg2_theory.md:97-110): deterministic adjacency
  certification from F1 and the killed row/column structure of F2.
- Theorem 2 (deg2_theory.md:138-198): exact one-row Bayes with
  hypergeometric masses and parity weights. Its part (iv) monotonicity is
  elementary for $k \le n-2d$ and numerically verified on the tail
  (deg2_theory.md:170-172, 425-427): that residual tail proof is a
  pre-existing open item, not a JDP item, and is untouched here.
- Lemma REL (deg2_theory.md:207-231): hypergeometric union bound plus the
  [MV] row-incomplete independence facts. This lemma is what licenses the
  answer factorization used by Lemma D1 below.
- The F2/F5 channel facts and Theorem 4's count (exact enumeration).
- Corollary 3.1 (deg2_theory.md:282-295) and Section 8: arithmetic on top
  of Theorem 3; they inherit the discharge.

## 3. Primary-source status of the two citations

### 3.1 Joag-Dev and Proschan 1983

What is quote-anchored this session (abstract fetched via the MathDoc
mirror at dml.mathdoc.fr/item/1176346079 and the Project Euclid landing
page; full text is subscriber-only and was NOT reachable):

- The NA definition: disjoint subsets $A_1, A_2$, all nondecreasing $f, g$,
  $\mathrm{Cov}[f(X_i, i \in A_1), g(X_j, j \in A_2)] \le 0$.
- "Especially useful is the property that nondecreasing functions of
  mutually exclusive subsets of NA random variables are NA."
- The NA distribution list: "(a) multinomial, (b) convolution of unlike
  multinomials, (c) multivariate hypergeometric, (d) Dirichlet, and (e)
  Dirichlet compound multinomial", plus "Negative association is shown to
  arise in situations where the probability measure is permutation
  invariant" and "Applications of this are considered for sampling
  without replacement".
- Independently, Dubhashi-Ranjan's Remark 14 (full text, fetched) states
  that Joag-Dev and Proschan prove the multinomial NA "at their
  $\S$3.1(a)", which confirms JDP's examples use a 3.x numbering and
  corroborates the format of Lemma B.1's "Section 3.n" reference.

What remains UNVERIFIED: the internal theorem numbers "Theorem 8" and
"Theorem 10" as quoted in proof_complexity.md:324-332, 336-337. No claim
in this deliverable uses them.

### 3.2 Dubhashi and Ranjan 1998

The full BRICS report version (BRICS-RS-96-25, 30 pages, fetched and
converted to text this session; the journal version is Random Structures
and Algorithms 13(2), 99-124, and numbering may differ) contains:

- Proposition 7: (1) the union of two mutually independent NA families is
  NA; (2) nondecreasing (or all nonincreasing) functions on disjoint
  index sets of an NA family are NA.
- Lemma 8 (Zero-One Lemma): 0/1 variables with $\sum_i X_i = 1$ a.s. are NA.
- Proposition 11: the full occupancy indicator vector $(B_{i,j})$ is NA.
- Theorem 13: the occupancy numbers $B_1, \ldots, B_n$ of $m$ balls thrown
  independently into $n$ bins are NA.
- Remark 14: attributes the multinomial case to JDP.

Finding F2 (mis-anchor): the report text contains no occurrence of
"without replacement", "permutation", "hypergeometric", or "capacity".
Its experiment is i.i.d. throwing; its variables are unbounded counts.
The corpus's families $\{P_i\}$, $\{H_j\}$ are 0/1 inclusion indicators
of a without-replacement sample (sum fixed at $2d+1$ resp. $2d$), which
is a different experiment, and the Zero-One Lemma as printed covers only
the sum-equals-one case. So proof_complexity.md:326-327's "see also
Dubhashi & Ranjan ... for the occupancy form" does not cover the
instance; the correct anchor is JDP alone (whose abstract names sampling
without replacement and the multivariate hypergeometric), or better the
self-contained Lemma D3 below, which needs no citation at all.

## 4. Findings

F1 (discharge, PROVED): both flagged steps of Theorem 3 reduce to
conditioning on the transcript-determined status atom. The channel law on
row-incomplete sets (F2, Lemma REL) factors answers as status times
independent fair bits, which makes the conditioning argument four lines
long and citation-free. See Section 5.

F2 (mis-anchor, verified against the fetched D-R full text): see
Section 3.2.

F3 (false instance, correction-class, MEASURED): Lemma B.1 step (2)'s
family $\{F_q = P_i H_j\}$ is not NA. The cited closure hypothesis
("disjoint subfamilies") fails because the pairs $(i,j)$ and $(i,j')$
share the factor $P_i$, and the conclusion itself is false: at
$(n,d) = (8,1)$ (in-regime: $2d^2 + 3d = 5 \le 8$), with $q_a = (1,1)$,
$q_b = (1,2)$, $q_c = (2,1)$, $f = F_{q_a}$, $g = F_{q_b} + F_{q_c}$
(both nondecreasing, the pair sets $\{q_a\}$ and $\{q_b, q_c\}$
disjoint):
$$E[fg] - E[f]E[g] = \frac{19}{1008} > 0.$$
Exact values: $E[fg] = 11/336$, $E[f]E[g] = 1/72$ (MEASURED by exhaustive
enumeration of all $1{,}693{,}440$ outcomes; closed form below). Also
$+26/735$ at $(6,1)$. General closed form for the tested functional,
with $A = E[P_i]$ (one pigeon), $\gamma = E[P_i P_{i'}]$ (two distinct
pigeons), $h = E[H_j]$ (one hole), $c = E[H_j H_{j'}]$ (two distinct
holes):
$$E[fg] = A\,c + \gamma\,h, \qquad E[f]\,E[g] = 2A^2h^2, \qquad
E[fg] - E[f]E[g] = A\,c + \gamma\,h - 2A^2h^2,$$
using independence of the pigeon and hole families and idempotence of
indicators. The positive terms $Ac$ and $\gamma h$ compete with
$2A^2h^2$, so the sign is regime-dependent a priori; at both tested
in-regime points the covariance is positive. At $(8,1)$:
$A = 1/3$, $\gamma = 1/12$, $h = 1/4$, $c = 1/28$ give
$1/84 + 1/48 - 1/72 = 19/1008$. The citation defect is independent of
the sign in any case, because the closure hypothesis fails regardless
(the factor subfamilies overlap).
Consequence: the Reading B failures of thmB_stress.md (15/35 grid points,
shared-coordinate lift) are exactly what NA of $\{F_q\}$ would have
forbidden; the corpus's numerical finding and the citation defect are the
same fact seen twice. Reading A survives untouched (it never used
$\{F_q\}$-NA; see F5).

F4 (statement sharpening): deg2_theory.md:269's "distant evidence only
depresses" is not literally true. At $(8,1)$, $e=1$, the all-zero
transcript leaves a fresh pair's freeness EXACTLY at $f = 1/12$
(MEASURED, Section 10), neither depressed nor elevated, and atoms with
many assigned queried pigeons lift fresh freeness up to the depleted rate
$f_e > f$. The correct statement is Lemma D1: fresh-pair freeness is
capped at the depleted base rate $f_e = f(1 + O(e/n))$, which is what
Theorem 3's assembly actually uses.

F5 (cross-validation, MEASURED): the exact values produced by the atom
computation of Lemma D1 reproduce thmB_stress.md's instrument
digit-for-digit at the overlapping points: $(8,1,1)$ worst pattern value
$1/12 = 0.083333$ (their Table 1 row 1) and $(8,1,2)$ worst value
$2/23 = 0.086957$ with $z^* = 2$ (their Table 1 row 2), plus the
$(8,1,2)$, $z=0$ ground truth $86/1031 = 0.083414$ (their validation
item 4). Two independently written instruments now agree on the exact
rationals.

## 5. The replacement toolkit (self-contained, zero citations)

Standing model (the status layer of the $\Omega(n,d)$ pipeline at
$p = 2$, deg2_theory.md Section 1 and thmB_stress.md Section 1):
$\rho = (D, R, \mu)$ with $D$ a uniform $(2d+1)$-subset of the $n+1$
pigeons, $R$ a uniform $2d$-subset of the $n$ holes, independent, and
$\mu$ a uniform bijection from the assigned pigeons to the assigned
holes. Pair status: free ($i \in D \wedge j \in R$), matched
($\mu(i) = j$, which forces $i \notin D, j \notin R$), killed-unmatched
otherwise. Marginals: $f = \frac{(2d+1)2d}{(n+1)n}$ (free),
$m = \frac{n-2d}{(n+1)n}$ (matched; note $E[\mu(i)=j] = P[i \notin D]
\cdot P[j \notin R] \cdot \frac{1}{n-2d} = m$), $A = \frac{2d+1}{n+1}$,
$q = \frac{f/2}{f/2 + m}$, $h_1 = f/2 + m$.

Standing answer law (the block-free event of Lemma REL, [MV]-backed):
answers on the queried set factor as status times design bits; the bits
of distinct free rows are independent fair coins; killed-unmatched
answers 0 and matched answers 1 determinedly. A transcript event $E$ is
therefore a rectangle: a status atom $s$ (the status of every touched
pair) times a bit prescription on the free touched pairs, and the bits
are independent of $\rho$.

Notation: for a transcript event $E$ with touched-pair set $S$,
$|S| = e$, let $e_p$ = distinct pigeons touched, $e_h$ = distinct holes
touched (both $\le e$), and
$$f_e := \frac{2d+1}{n+1-e} \cdot \frac{2d}{n-e}.$$

### Lemma D1 (atom conditioning; the depletion bound). PROVED

On the block-free event, for any transcript event $E$ determined by the
answers on $S$ and any pair $p$ with both coordinates outside $S$:
$$P[p \in F \mid E] \le f_e, \qquad\text{hence}\qquad
|P[p \in F \mid E] - f| \le f \cdot \frac{12\,e}{n}
\ \ \text{for } e \le n/2.$$

Proof. Let $s$ be the status atom of $S$ and $b$ the bit prescription;
$E = \{s\} \cap \{b\}$ up to a union over atoms sharing the realized
answer pattern, and it suffices to bound each atom term. Given $s$: the
touched pigeons contain $f_p$ free pigeons and the touched holes contain
$f_h$ free holes, so the residual law is again of the same form with
fresh parameters: $D$ restricted to the untouched pigeons is uniform of
size $2d+1-f_p$ (so a fresh pigeon is free with probability
$\frac{2d+1-f_p}{n+1-e_p}$), likewise $R$ gives
$\frac{2d-f_h}{n-e_h}$, and the two are independent, while $\mu$ does not
enter freeness. Since $p$'s freeness is $p$-pigeon free times $p$-hole
free,
$$P[p \in F \mid s, b] = \frac{2d+1-f_p}{n+1-e_p}\cdot\frac{2d-f_h}{n-e_h}
\le \frac{2d+1}{n+1-e}\cdot\frac{2d}{n-e} = f_e,$$
using $f_p, f_h \ge 0$ and $e_p, e_h \le e$. The bits are independent of
$\rho$, so conditioning on $b$ changes nothing, and averaging over the
posterior atom distribution preserves the bound. For the difference form:
$\frac{f_e}{f} - 1 = \frac{e(2n+1-e)}{(n+1-e)(n-e)} \le \frac{12e}{n}$
for $e \le n/2$. QED.

This is exactly thmB_stress.md's Reading A inequality, now proved instead
of tested. The constant 12 is crude; their measured $C^* \le 0.43$ shows
the true constant is far smaller.

### Lemma D2 (own-coordinate conditioning; the adjacency rate). PROVED

Let $i$ be a pigeon and $E$ any answer event on a touched set $S$. Then:

(i) If no coordinate of row $i$ is touched:
$$P[i \in D \mid E] \le \frac{2d+1}{n+1-e_p} \le q\left(1 + \frac{2e}{n}\right).$$

(ii) In general (row $i$ possibly touched, e.g. zeros then the first
hit): $P[i \in D \mid E] \le q\,(1 + O((d+e)/n))$, and in-regime
($d \le \sqrt{n}$) this is $q(1 + O(e/n) + o(1))$, absorbable into
Theorem 3's $O(e/n) + o(1)$ bookkeeping.

(iii) Consequently, for a fresh column $j'$ and a known free column $j$
of row $i$:
$$P[\mathrm{ans}(i,j') = 1 \mid E,\ i \in D \text{ at rate } q] \le
q \cdot \frac{2d-1}{2(n-1)}\left(1 + O\!\left(\frac{e}{n}\right)\right),$$
and on the true channel the middle factor is an over-estimate: the
row-parity tax only suppresses (MEASURED: the conditional drops to
exactly $0$ at $(8,1)$ where the two queries complete the row).

Proof. (i) Condition on the status atom of the touched pairs outside
pigeon $i$: by the residual-law computation of Lemma D1,
$P[i \in D \mid s] = \frac{2d+1-f_p}{n+1-e_p} \le \frac{2d+1}{n+1-e_p}$;
average over atoms. For the second inequality:
$\frac{2d+1}{n+1-e_p} \le A\frac{n+1}{n+1-e_p}$, and $A \le q$
identically, since $q - A \ge 0 \iff (n-2d)(d-1) \ge 0$.
(ii) Condition on the full status atom $a$ of all touched pairs
(off-row pairs and row-i pairs together) plus the bit prescription, and
write the posterior as the atom-weighted sum
$P[i \in D \mid E] = \sum_a P[a \mid E]\,P[i \in D \mid a]$.
Two cases, by the hit structure of $E_{\mathrm{own}}$.
Hit case ($E_{\mathrm{own}}$ = zeros then one 1 at $(i,j)$): the
consistent atoms split into the free branch (row-i pair free, bit 1)
and the matched branch ($\mu(i) = j$); the free:matched odds at fixed
off-row content is exactly the Theorem 2 likelihood ratio, and every
off-row completion-count factor penalizes the free branch relative to
the matched branch: i consumes one free-pigeon slot
($\binom{n-e_p^o}{2d-f_p^o}$ vs $\binom{n-e_p^o}{2d+1-f_p^o}$, ratio
$\le 1$) and $j$ consumes one free-hole slot
($\binom{n-e_h^o-1}{2d-1-f_h^o}$ vs $\binom{n-e_h^o-1}{2d-f_h^o}$,
ratio $\le 1$). Relative to the marginal (no off-row content), each
ratio-of-ratios is a pool perturbation bounded by
$1 + O((d+e)/n)$: pigeon side
$\frac{(2d+1-f_p^o)(n-2d)}{(2d+1)(n-e_p^o-2d+f_p^o)}$, hole side
$\frac{(2d-f_h^o)(n-1-2d)}{2d\,(n-e_h^o-2d+f_h^o)}$, both $\le 1 +
O((d+e)/n)$ for $n \ge 4d$. So
$O' \le O\,(1+O((d+e)/n))$ with $O$ the Theorem 2 odds
$\le q/(1-q)$, and the algebra identity
$\frac{(1+\varepsilon)q}{(1-q)+(1+\varepsilon)q} \le q(1+3\varepsilon)$
(valid unconditionally: it reduces to
$0 \le 2\varepsilon + \varepsilon q(1+3\varepsilon)$) finishes.
Zeros case: identical, with the matched branch replaced by the
killed-unmatched branch ($\mu(i)$ outside the queried columns), whose
residual slots again dominate the free branch's
(the free branch additionally pays the parity bit-weights
$2^{-r} \le 1$ on the $r$ zero-columns forced into $R$). The exact
identity behind the pigeon-side perturbation is verified in Section 10,
row D. QED.

(iii) Given the
atom, a fresh hole is free with probability
$\frac{2d-1-f_h'}{n-1-e_h} \le \frac{2d-1}{n-1}\cdot\frac{n-1}{n-1-e_h}$,
and the free-row bit is a fair coin on the block-free event; multiply
by the part-(ii) bound on $P[i \in D \mid E]$. QED.

The one-slot identity behind (iii)'s constants was verified exactly:
at $(8,1)$, for the atom $\{(2,2)\text{ free}, (3,3)\text{ matched}\}$
on queried pigeons $\{2,3\}$, conditioning on $1 \in D$ shifts the atom
probability by exactly $\frac{(n+1)(2d+1-f_p)}{(2d+1)(n+1-e_p)} = 6/7$
(MEASURED, matches the formula).

### Lemma D3 (the inclusion families are NA, elementarily). PROVED

Let $A_0$ be a uniform $k$-subset of $[N]$ and $I_i = 1[i \in A_0]$. Then
$\{I_i\}_{i \le N}$ is negatively associated. Consequently, if $D$ and
$R$ are independent without-replacement samples, the joint family
$\{P_i\} \cup \{H_j\}$ is NA.

Proof. Fix disjoint $S, T \subseteq [N]$ and nondecreasing $f, g$; write
$t = \sum_{i \in S} I_i$, $u = \sum_{j \in T} I_j$. Three elementary
facts. (F1) Given $(t, u)$, the two restrictions are independent and
uniform on their level sets (a uniform subset conditioned on cell counts
is uniform within cells, independently across cells). (F2)
$a(t) := E[f \mid t]$ is nondecreasing: delete a uniform element from a
uniform $(t+1)$-subset to obtain a uniform $t$-subset, and use
pointwise monotonicity of $f$. (F3) Given $t$, $u$ is hypergeometric
with $k - t$ draws; $c(t) := E[g \mid u \sim \mathrm{Hyp}(N - |S|, |T|,
k-t)]$ is nonincreasing in $t$: to couple $t_1 < t_2$, draw the larger
$k - t_1$ and discard $t_2 - t_1$ uniformly, which stochastically
dominates. Then
$E[fg] = E[a(t)\,c(t)]$ by F1, and with $t, t'$ i.i.d. copies,
$(a(t) - a(t'))(c(t) - c(t')) \le 0$ pointwise; expanding and taking
expectations gives $E[a(t)c(t)] \le E[a(t)]E[c(t)] = E[f]E[g]$.
For the union family: condition on the entire $H$-family; the
conditional expectations $\phi = E[f \mid H]$ and $\psi = E[g \mid H]$
are nondecreasing in their pigeon coordinates (monotone integrand, common
dominating measure), so NA of $\{P_i\}$ gives
$E[fg \mid H] \le \phi\,\psi$, and $\phi, \psi$ are nondecreasing
functions of disjoint hole blocks, so NA of $\{H_j\}$ finishes. QED.

This proves Lemma B.1's step (1) without any citation, and it is the
same proof route D-R use for their Theorem 13 (counts instead of
indicators), so the corpus's intuition was right; only the anchor was
off.

### Proposition D4 (the pair-product family is not NA). PROVED + MEASURED

In the model above with $(n,d) = (8,1)$, the family
$\{F_q = P_i H_j\}_{q \in [n+1] \times [n]}$ is not negatively
associated: for $f = F_{(1,1)}$, $g = F_{(1,2)} + F_{(2,1)}$,
$E[fg] - E[f]E[g] = 19/1008 > 0$ (exact, exhaustive enumeration; closed
form in Finding F3; also $26/735 > 0$ at $(6,1)$). QED (counterexample).

Remark. No closure theorem can cover this step: the "disjoint
subfamilies" hypothesis fails structurally, since $(i,j)$ and $(i,j')$
share the factor $P_i$. Lemma B.1's step (2) should be recorded as
withdrawn, with steps (3)-(4) replaced by Lemma D1. Nothing downstream
changes: the corpus's applications use only the depletion conclusion
(Reading A), which D1 proves.

## 6. Theorem 3 de-modularized (zero black-box citations)

Statement (unchanged from deg2_theory.md:245-249): every adaptive tree of
budget $e$ in the full degree-$\le 2$ class satisfies
$$\mathrm{success}(T) \le \min\big(1,\ q + P_{\mathrm{adj}}(e) + P_K(e) + O(e/n) + o(1)\big),$$
with the $o(1)$ absorbing the block-completion probability of Lemma REL.

Proof, with every coupling written out. Fix a tree $T$ and decompose its
leaves.

Certificate leaves, adjacency accounting ($P_{\mathrm{adj}}$).
A leaf is adjacency-certified when its transcript contains two
answer-1s on a common row or column (Theorem 1, deterministic). Let
$(i,j)$ be the first hit: the union bound over the $\le e$ queried
singles gives $P[\text{first hit}] \le e\,h_1$, each single answering 1
with marginal probability exactly $h_1 = f/2 + m$ (free pairs are fair
coins, matched pairs answer 1, killed-unmatched answer 0; no independence
needed for a union bound). Conditional on the past (all answers before
the adjacency probe, certificate-free so far): by Lemma D2(ii) the
row-freeness posterior is at most $q(1 + O((d+e)/n))$, where the own-row
part (zeros, then the hit) is exactly Theorem 2's computation and the
off-row part enters only through the pool-perturbation factors of
Lemma D2(ii)'s proof. Given row $i$ free with hit column $j \in
R$, a fresh same-line query $(i, j')$ answers 1 only if $j' \in R$
(hypergeometric factor $\frac{2d-1}{n-1}$, shifted by at most
$\frac{n-1}{n-1-e_h}$ by Lemma D2(iii)) and its free-row coin is 1
(probability $\le 1/2$ on the block-free event; strictly less on the
true channel, where the parity tax applies, MEASURED $0$ at $(8,1)$).
Union over the $\le e$ probes:
$$P_{\mathrm{adj}}(e) \le \min(1, e h_1)\,\min\!\left(1, e\,q\frac{2d-1}{2(n-1)}\right)\left(1 + O\!\left(\tfrac{e}{n}\right)\right),$$
with the final factor absorbed by the theorem's $O(e/n)$ term. This
discharges the flag at deg2_theory.md:256-260.

Certificate leaves, column-parity accounting ($P_K$).
A certificate needs a $K_j$ answer-1 (marginal probability exactly
$d/n$: $j \in R$ w.p. $2d/n$, then the column parity of its $2d+1$ free
bits, a fair coin, F5) and a 1-entry found by scanning that column
(per-query marginal $\frac{2d+1}{2(n+1)} = A/2$ on a fresh pigeon;
depletion only raises later rates, so $A(1+O(e/n))/2$ caps each). Both
stages are union-bounded over their query counts $t_1 + t_2 = e$:
$$P_K(e) \le \min\big(1,\ t_1 d/n,\ t_2 A(1+O(e/n))/2\big)\ \le\ \min(1,\ ed/n).$$
No independence or NA is used (union bounds only). Three constant-level
notes, none affecting the cap: the printed exponential form
$2(1 - \exp(-ed/4n)) \sim ed/(2n)$ is smaller than the union form's
$ed/n$ by a $\Theta(1)$ factor, and its exponential form does not follow
from marginals plus union bounds; conditioning on $\rho$ the $K_j$
answers are independent, which gives $P[\ge 1\text{ cert}] \le
1 - 2^{-2dt_1/n}$ (Jensen, since $E|J_0 \cap R| = 2dt_1/n$), whose
small-$x$ constant $2\ln 2$ still exceeds the union form's $1$; the
optimal split of the union form gives $\sim 2ed/(3n)$; and Corollary
3.1 only uses $P_K \to 0$ linearized, so the bookkeeping constant is
immaterial. This resolves the $P_K$ line of
deg2_theory.md:236-237 in elementary form, with the printed exponential
constant recorded as $\Theta(1)$-optimistic.

Certificate-free leaves.
On the block-free event (Lemma REL, [MV]: the likelihood factors), let
$\ell$ be a certificate-free leaf with output pair $p$. Split the
transcript into own evidence (queries touching $p$'s row or column) and
distant evidence. Own evidence is covered by the exact one-coordinate
laws: an own hit gives $q$ (Theorem 2(i)); an own row scan gives
$\mathrm{post}(k) \le q$ with equality only at $k = 0$ (Theorem 2(iv),
elementary for $k \le n-2d$, tail numerically verified, pre-existing
caveat); an own column scan gives at most $q$ (deg2_theory.md Section 3,
symmetric formulas). Distant evidence: Lemma D1 caps the output pair's
freeness at $f_e = f(1 + O(e/n))$, and $f \le q$ in-regime: $f \le q$
is equivalent to $4d^3 - 2d^2 + 2dn \le n^2 + n$, whose left side is at
most $n^2$ (from $2d^2 \le n$, so $d \le \sqrt{n/2}$ and
$4d^3 \le \sqrt{2}\,n^{3/2} \le n^2$ for $n \ge 2$, while
$-2d^2 + 2dn \ge 0$), so distant evidence leaves the leaf posterior at
most
$\max(q, f_e)(1 + O(e/n)) = q(1 + O(e/n))$. This is the corrected form
of the "distant evidence only depresses" step: not literal depression,
but a cap at the depleted base rate (Finding F4, MEASURED at $(8,1)$
where the all-zero transcript leaves a fresh pair exactly at $f$).
Block completion: charged to $p_{\mathrm{block}}(e) = o(1)$ by Lemma
REL's union bound. Summing over leaves (the reach events partition the
probability space) gives the stated cap. Zero citations remain.
QED

Corollary 3.1 and the Section 8 boundary are unchanged: they use only
$q \le 1/2$ in-regime, $1 - e^{-x} \le x$, and the $d^2 \log k = o(n)$
arithmetic already in deg2_theory.md:282-295, 385-400.

## 7. Lemma B.1 repaired proof of record (for proof_complexity.md, not edited here)

Lemma B.1 (Reading A, repaired quantifier: $p$ with both coordinates
outside the queried set) is now proved as follows, with the four old
steps replaced:

1. (replaces old steps (1)-(3)) By the answer factorization on the
   row-incomplete channel, every transcript event $E$ is a status atom
   times a bit prescription; conditioning on $E$ is conditioning on the
   atom. Lemma D1 then gives
   $P[p \in F \mid E] \le f_e$, and the difference form gives the
   lemma's $O(e/n)$ with explicit constant 12 (crude; the measured
   corpus constant is $\le 0.43$).
2. (replaces old step (4)) The depletion count is Lemma D1's residual
   hypergeometric computation; nothing else is used.
3. The NA citations of old step (1) become decorative: Lemma D3 proves
   the inclusion-family NA elementarily if it is wanted for other uses,
   and the D-R anchor is dropped (Finding F2).
4. Old steps (2)-(3) are withdrawn: the family $\{F_q\}$ is not NA
   (Proposition D4), and the closure hypothesis fails structurally.

Reading B (shared-coordinate $p$) remains falsified, as it must: the
shared-coordinate lift is positive association of the $\{F_q\}$ family
(Finding F3), so no repair of the quantifier was ever going to rescue
the literal statement. The corpus's 2026-10-03 quantifier repair was the
correct fix.

## 8. deg3_theory.md Theorem 3': what transfers

Theorem 3' (deg3_theory.md:319-337) flags one inherited gap: the
"MULTI-evidence composition (deep zero-runs across classes, distant
evidence) is carried modulo the same JDP negative-association citation
standard". Dissection:

Transfers and is discharged (PROVED):

- The answer law at degree $\le 3$ factors as status times design bits
  on windows carrying no complete star, no full row, and no alias pair
  (deg3_theory.md:142-145, the star lemma's consequences, [MV]-backed,
  plus the balance lemma at lines 126-130). This is the same
  factorization Lemma D1 consumes, with the touched-pair set now
  counting each monomial's component pairs, so Lemma D1 transfers
  verbatim with $e$ = touched pairs: distant evidence caps a fresh
  pair's freeness at $f_e = \frac{(2d+1)2d}{(n+1-e)(n-e)}
  = \frac{4d^2}{n^2}(1 + O(e/n)) \le q\,(1 + O(e/n))$.
- The certificate terms $P_{\mathrm{adj}}, P_K, P_{\mathrm{wedge}},
  P_Z, P_{\mathrm{blk3}}$ are marginal-rate and union-bound
  computations (F5, Lemma S3, Lemma Z, Lemma REL-3): already
  citation-free, no NA anywhere.
- The distant-evidence half of the flag is thereby closed: the
  certificate-free leaf posterior is at most
  $\max(q_3^*, f_e)(1 + O(e/n)) = q_3^*(1 + O(e/n))$, since
  $q_3^* \ge q \ge f$ in-regime.

Does not transfer, remains OPEN:

- The multi-class deep-zero-run composition: whether the posterior of a
  pair under continued zero-answers spread across several evidence
  classes (own singles, own diagonals, own triples) stays at the
  own-class cap. Each class in isolation is exact (Theorem 2 for
  singles, $q_{\mathrm{and\_exact}}$ status Bayes, Theorem P3), and
  deg3_theory.md:374-377 already records this as open item 3
  independently of JDP. Lemma D1 does not close it: D1 bounds distant
  freeness by the depleted base rate, not by the class posteriors, and
  own-coordinate multi-class scans are own evidence, outside D1's
  hypothesis. Label: OPEN.
- Mitigation of record: the cap's conclusion does not depend on it. Any
  elevation on certificate-free leaves is bounded by the D1 route
  through the own-evidence decomposition plus $f_e$, and elevation to
  certainty is a certificate event, charged to the inventory terms. So
  Corollary 3.2's regime statement ($d^2 \log k = o(n)$) is unaffected;
  its "[PROVED modulo the two JDP steps]" marker at
  deg3_theory.md:346 can drop to PROVED for the distant-evidence step,
  with the zero-run residue tracked as deg3 open item 3.

## 9. Recommended repairs for the orchestrator (no file edited by this agent)

1. proof_complexity.md Lemma B.1: replace steps (2)-(3) by Lemma D1
   (withdraw the $\{F_q\}$-NA citation; record Proposition D4 as the
   reason), replace the step (1) citations by Lemma D3 or keep them as
   decorative with the JDP numbering marked UNVERIFIED, and drop the
   D-R anchor (Finding F2).
2. deg2_theory.md:269: reword "distant evidence only depresses" to
   "distant evidence caps at the depleted base rate $f_e$ (Lemma D1)".
3. deg2_theory.md:271-272 and 440-442: the two modulo-JDP markers can be
   retired (discharged); open item 4 can be closed with a pointer to
   this file.
4. deg3_theory.md:336 and 346: split the flag: distant evidence
   discharged; deep-zero-run multi-class composition remains open item
   3 (pre-existing).
5. deg2_theory.md:237 and 275: the printed $P_K$ bound
   $2(1 - \exp(-ed/4n))$ is $\Theta(1)$-optimistic relative to what
   marginals plus union bounds give ($\min(1, ed/n)$, optimal split
   $\sim 2ed/(3n)$); the cap and Corollary 3.1 are unaffected since they
   only linearize, but the printed constant should carry a bookkeeping
   note or be replaced by the union form.
6. Library access to Joag-Dev-Proschan 1983 full text would let a later
   session verify the internal theorem numbers ("Theorem 8", "Theorem
   10") and, if they are wrong, correct the historical citation strings;
   no mathematical claim depends on this.

## 10. Verification (executed run)

Script: /tmp/opencode/jdp_demod_check.py (outside the corpus per the
deliverable rule; exact Fraction arithmetic over the uniform outcome
space, no sampling). Runtime several minutes, dominated by the (8,1)
enumerations of all $C(9,3)C(8,2)6! = 1{,}693{,}440$ outcomes. Output,
verbatim:

    A (6,1): Cov(F_(1,1), F_(1,2)+F_(2,1)) = 26/735  (E[fg]=8/105, E[f]E[g]=2/49)  NA-FAILS=True
    A (8,1): Cov(F_(1,1), F_(1,2)+F_(2,1)) = 19/1008  (E[fg]=11/336, E[f]E[g]=1/72)  NA-FAILS=True
    B P-family (6,1): E[fg]-E[f]E[g] = -24/245  NA-ok=True
    B H-family (6,1): E[fg]-E[f]E[g] = -1/45  NA-ok=True
    B joint    (6,1): E[fg]-E[f]E[g] = -8/245  NA-ok=True
    B P-family (8,1): E[fg]-E[f]E[g] = -5/63  NA-ok=True
    B H-family (8,1): E[fg]-E[f]E[g] = -1/112  NA-ok=True
    B joint    (8,1): E[fg]-E[f]E[g] = -1/63  NA-ok=True
    C (8,1) e=1 pattern z=0: P[F_p|E] = 1/12 = 0.083333  f_e = 3/28 = 0.107143  PASS=True
    C (8,1) e=1 pattern z=1: P[F_p|E] = 1/12 = 0.083333  f_e = 3/28 = 0.107143  PASS=True
    C (8,1) e=2 pattern z=0: P[F_p|E] = 86/1031 = 0.083414  f_e = 1/7 = 0.142857  PASS=True
    C (8,1) e=2 pattern z=1: P[F_p|E] = 12/145 = 0.082759  f_e = 1/7 = 0.142857  PASS=True
    C (8,1) e=2 pattern z=2: P[F_p|E] = 2/23 = 0.086957  f_e = 1/7 = 0.142857  PASS=True
    D (8,1): P[atom|P1]/P[atom] = 6/7  formula (n+1)(2d+1-fp)/((2d+1)(n+1-e_p)) = 6/7  MATCH=True
    E (8,1) coin [row completed (2d=2)]: P[ans12=1|ans11=1] = 1/42 = 0.023810  q(2d-1)/(2(n-1)) = 1/42 = 0.023810  within=True
    E (8,1) true [row completed (2d=2)]: P[ans12=1|ans11=1] = 0 = 0.000000  q(2d-1)/(2(n-1)) = 1/42 = 0.023810  within=True
    E (8,2) coin [row incomplete (2d=4)]: P[ans12=1|ans11=1] = 15/98 = 0.153061  q(2d-1)/(2(n-1)) = 15/98 = 0.153061  within=True
    E (8,2) true [row incomplete (2d=4)]: P[ans12=1|ans11=1] = 15/98 = 0.153061  q(2d-1)/(2(n-1)) = 15/98 = 0.153061  within=True
    F (6,1) brute force (100800 outcome-design cells): P[ans12=1|ans11=1] = 0 = 0.000000

Reading of the rows:

- A: Proposition D4's counterexample, exact, at two in-regime points.
- B: Lemma D3 spot checks (the full lemma is proved, not just tested).
- C: Lemma D1's bound at every answer pattern; the values $1/12$,
  $2/23$, $86/1031$ reproduce thmB_stress.md's independently computed
  exact values at $(8,1,1)$ and $(8,1,2)$ digit-for-digit.
- D: the one-slot identity behind Lemma D2(iii)'s constants.
- E: the adjacency conditional equals the printed rate
  $q(2d-1)/(2(n-1))$ exactly at the coin channel, and the true channel
  never exceeds it (parity lock forces an exact $0$ at $(8,1)$); at
  $(8,2)$ the row is incomplete and coin equals true, as Lemma REL
  predicts.
- F: full brute force over outcomes times designs (each free pigeon
  carrying its own odd-parity vector) confirms the true-channel value
  at $(6,1)$.

## 11. One-paragraph verdict for the orchestrator

GAP D is discharged. Theorem 3's two modulo-JDP steps did not need
negative association: on the corpus's own row-incomplete channel
law, answers factor into status atoms times independent bits, and both
steps follow from four lines of conditioning on those atoms (Lemmas D1
and D2), with the depletion constant explicit and the numerics matching
thmB_stress exactly. The audit's substantive yield is one correction-class
finding: Lemma B.1's step (2) cited a closure theorem whose hypothesis
fails, and the claimed family is in fact not negatively associated
(exact counterexample $+19/1008$ at in-regime parameters), which is the
same fact as the corpus's Reading B falsification seen from the
citation side; the repair is already aligned with what thmB_stress
recommended. What survives of the NA apparatus is the classical
inclusion-family result, now proved elementarily in the corpus (Lemma
D3) so that no citation carries the proof; the D-R anchor should be dropped
(mis-anchored to an i.i.d. occupancy paper), and the JDP internal
theorem numbers are marked UNVERIFIED, with nothing resting on
them. Theorem 3 and Corollary 3.1 stand with zero black-box steps; Theorem
3' loses its distant-evidence flag and keeps only its pre-existing
zero-run open item.
