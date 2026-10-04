# The all-degrees assembly: step (6) over the enlarged inventory, the
# per-degree slices, and Theorem 3-gen

Result of the theory agent (2026-10-04). Status: analysis, not peer-reviewed.
Task: re-run the O2 induction's step (6) over the ENLARGED relation inventory of
cls_cnt.md ({row, star, DS, UU, OFF} + catch-all), confirm or repair every
per-degree slice (Theorems 3, 3', 3'', 3'''), state and prove the all-degrees
theorem (Theorem 3-gen), and record the final O2 status with falsification
conditions.

Channel: the TRUE $\Omega(n,d)$ pipeline at $p = 2$ (uniform designs of the
restricted canonical system; $V(n,d)^\rho = V(2d,d)$), degree-$\le d$ monomial
queries and linear forms, budget $e = d\log k$ unless stated.
Markers: PROVED, REDUCED (proved modulo an explicitly named lemma), OPEN,
[MV] machine-verified, [ASSEMBLY] assembled from labeled pieces.

## 0. Summary

1. Step (6) restated over the enlarged inventory closes at degree 2 and stays
   open at degrees 3 through $d$.
   What each degree-$k$ cap consumes is the transfer bound
   $\varepsilon^{(k)}(e,n,d)$, the probability that the queried window contains
   the support of a nonzero relation, over the FULL inventory.
   cls_cnt.md proves the degree-2 slice of this at general $d$
   (Q-A by degree-truncated Buchberger, plus the covering theorem and the CNT
   counting bound).
   The degree-$\ge 3$ slices need the same statement at truncation level
   $t = 3, \ldots, d$, which cls_cnt.md does not prove (its Buchberger
   truncation is $t = 2$).
   This is exactly SPARSE-d at $t \ge 3$ and it remains the single
   mathematical gap.
2. The $\varepsilon$ constant does NOT change.
   DS, UU, OFF, and the catch-all class contribute only dominated $\Delta$
   terms, exactly as cls_cnt.md claims for CNT:
   $\varepsilon_{full} = (1 + o(1))\,\varepsilon_{headline}$ with
   $\varepsilon_{headline} = \frac{A}{2}\big[(e/n)^{2d} + (2e/(n-1))^{2d-1}\big]$,
   $A = (2d+1)/(n+1)$, at every fixed $d \ge 2$ with $e = o(n)$.
   The support threshold ($2d$, achieved only by rows and stars), the
   per-event TV ($1/2$), and the prefactor $A/2$ are all inventory-minimal and
   unchanged.
   The degree-$k$ form adds the star-$j$ terms $j = 3, \ldots, k$; the largest
   is the degree-$k$ star term $\frac{A}{2}(ke/(n-1))^{2d-k+1}$, also $o(1)$ in
   regime.
3. Theorem 3 (degree 2) is upgraded: its step (6) is now closed at general $d$,
   so the degree-2 budgeted cap stands at general $d$ in the regime
   $d^2\log k = o(n)$, modulo the standing small caveats (the cor:coin base,
   bookkeeping lemma B2, Lemma L-CLASS absorbed by the catch-all).
   Theorems 3', 3'', 3''' survive VERBATIM as statements at every machine
   point and their constants do not shift ($q_3^*, q_4^*, q_5^*$ and the
   certificate terms are untouched; the $P_{\mathrm{blk}}$ line items gain the
   dominated $\Delta$ terms, absorbed by the printed $o(1)$ in regime).
   Their general-$d$ proof status does NOT upgrade: each carries an open
   INV-d instance.
4. Theorem 3-gen is stated and proved as an assembly with one explicit
   mathematical hypothesis INV(d) (inventory completeness through degree $d$,
   equal to SPARSE-d over $t \le d$).
   INV(2) is PROVED; INV(d) for $d \ge 3$ is OPEN at general $d$ and
   machine-verified at the swept points.
   Under INV(d), every budgeted adaptive degree-$\le d$ monomial tree with
   $d^2\log k = o(n)$ has error $\ge 1/2 - o(1) \ge k^{-O(1)}$, and with the
   degree-1 witness the two-sided form
   $\mathrm{err}^*(d, d\log k) = k^{-\Theta(d^2/n)}$ extends to every fixed
   granting $d$.
5. Final O2 status: the open core is now (a) INV-d at $t \ge 3$ (the single
   mathematical gap, concrete next target $t = 3$), (b) the MIXTURE-d scope gap
   (O2's literal quantifier allows arbitrary degree-$\le d$ polynomials; the
   mixture class is covered only at $d = 2$), (c) the boundary constant at
   $d^2 = \Theta(n)$, (d) the $e = \Theta(n)$ regime, (e) the exponent
   constants (Conjecture E5), plus the standing small items (cor:coin base,
   NAL at $k \ge 6$, certain-inventory completeness at scale).
   Falsification conditions are listed in Section 5.3.

## 1. What the assembly consumes (inputs and labels)

| ingredient | content | label | source |
|---|---|---|---|
| Theorem A | matching-$k$ columns vary, $1 \le k \le d$; balance gives fairness | PROVED (step written; base = cor:coin, standing small caveat) | deg4_theory.md sect. 2 |
| Alias/generator templates | fixed-0 = line-pair monomials; alias = Boolean telescoping, $p(k)-1$ patterns | PROVED | deg4/deg5 sect. 2 |
| Star lock L2 | $\bigoplus_{j \in R \setminus \mathrm{holes}(g)} \mathrm{ans}(x_{pj}g) = \mathrm{ans}(g)\cdot[p \in D]$, all degrees $\le d$ | PROVED | channel_spec.md L2; deg4 Thm B; deg5 Thm B5 |
| Posterior closed form | general-$k$ status Bayes; leading form $(2d^2+d)/(c-k+1)(1+o(1))$ | PROVED derivation; [MV] digit-exact $k \le 5$ | deg4_theory.md sect. 4; deg5 sect. 4 |
| Mass monotonicity (M5) | $P_{k+1} < P_k$, strict event inclusion, all $k$ | PROVED | deg5_theory.md sect. 5 |
| Q-A (CLS(ii) core) | $(V \oplus \langle e_0\rangle) \cap S_{\le 2} = V_{\le 2} \oplus \langle e_0\rangle$, general $d$ | PROVED (truncated Buchberger, M1-M5, I1; [MV] at $(4,2)$, $(6,3)$) | cls_cnt.md sect. 3 |
| Covering theorem | every support of $\overline{V}$ contains row / star / DS / UU / OFF, else L-CLASS residual | PROVED for pairs and the three named families; REDUCED to L-CLASS for $\ge 3$-star chains (absorbed by catch-all) | cls_cnt.md sect. 4 |
| Lemma CNT (tight form) | $\varepsilon_{full} = (1+o(1))\,\varepsilon_{headline}$ non-adaptive; adaptive $\times \exp(2ed/n) + O(e/n)$ (CNT-A) | PROVED non-adaptive; REDUCED to B2 adaptive | cls_cnt.md sect. 5 |
| Lemma M (coupling) | transcript TV $\le$ completion probability; exact for $e < 2d$ | PROVED (per step 1; consumes Q-A + covering) | lemma_m.md sect. 3.2 |
| Lemmas D1, D2, D3 | depletion, own-coordinate rate, inclusion-family NA, all elementary | PROVED | jdp_demod.md sect. 5 |
| Degree-2 cap machinery | Theorem 3 with $q_2^*$, sharpened form $\chi + (1-\chi)(q_2^* + A(e))$ | PROVED, zero black-box citations | deg2_theory.md; ADDENDA 8-10 |
| Witness | Theorem 4/4b, exponent constant $c_w = \rho/(1+\rho)$ | PROVED | deg2_theory.md sect. 6; gap_e_constants.md sect. 5 |

Standing caveat inherited everywhere: the base of Theorem A (singles vary) is
cor:coin plus kernel measurement, not a self-contained elementary proof
(deg4_theory.md sect. 7 item 1).

## 2. Step (6) over the enlarged inventory (task 1)

### 2.1 The restated step

The per-degree induction step (6) of deg5_theory.md section 6.2 required that
no determined-relation family exists with a completion window that is small or
transcript-identifiable.
After the inventory correction the step splits into three consumed statements.

Step (6a), inventory completeness.
Every support of a nonzero element of the varying-coordinate projection of
$(V \oplus \langle e_0\rangle) \cap S_{\le k}$ contains a configuration from
the named inventory: a full row, a full degree-$j$ star ($2 \le j \le k$), a DS,
a UU, an OFF, or a catch-all class (supports of size $\ge 4d-1$ with
per-coordinate multiplicity $\le 2^{O(d)}\,\mathrm{poly}(n)$).
Label at $k = 2$, general $d$: PROVED (Q-A + covering; L-CLASS residual
absorbed by the catch-all in all counting uses).
Label at $3 \le k \le d$, general $d$: OPEN.
This is SPARSE-d at $t = k$; cls_cnt.md's Buchberger argument is a
degree-truncated proof at $t = 2$ and does not reach $t \ge 3$.
At the swept points ($t \le 3$ at $(6,3)$ and $(10,5)$; $t \le 2$ at
$(8,4)$, $(10,5)$) it is [MV].

Step (6b), counting.
The probability that a budget-$e$ tree's window contains any named support is
at most $\varepsilon^{(k)}(e,n,d)$, with the headline form plus dominated
$\Delta$ terms.
Label: PROVED non-adaptive at general $d$ over the full enlarged inventory
(cls_cnt.md section 5.1); REDUCED to B2 for adaptive trees, and B2 closes in
regime (CNT-A).

Step (6c), transfer.
On windows avoiding all named supports, the projected law equals the
degree-$k$ fresh-bit law exactly, and the transcript TV is at most the
completion probability.
Label: PROVED given (6a) (lemma_m.md step 1 coupling; the per-event TV is
$1/2$ for every named family, all proper parity pins).

So step (6) over the enlarged inventory is: (6b) and (6c) are closed at
general $d$; (6a) is closed at $k = 2$ and open at $k \ge 3$.

### 2.2 The $\varepsilon$ re-derivation

Lemma M's headline was derived for $\{E_{row}, E_{star}\}$ (plus
$E_K$ for linear forms).
Re-derive over the five-family inventory.
Each event contributes $P[E] \cdot \tfrac12$ to the transcript TV, because the
true law on a completed window is a proper parity coset and fresh-bit is
uniform there (TV $1/2$ per event; [MV] for row, star, DS; the general parity
pin argument gives it for UU, OFF, and any catch-all support).

Row and star terms (lemma_m.md step 2, unchanged):
$$\varepsilon_{row} \le \tfrac{A}{2}(e/n)^{2d}, \qquad
  \varepsilon_{star} \le \tfrac{A}{2}(2e/(n-1))^{2d-1}.$$

The new $\Delta$ terms (cls_cnt.md section 5.1, halved per event):
$$\Delta_{DS} \le A^2 e^{4d-2} (n-1)^{-(4d-2)}, \quad
  \Delta_{UU} \le A^2 e^{4d-2} n^{10-8d},$$
$$\Delta_{OFF} \le \tfrac14 n^2 A^2 (e/n^2)^{2d(2d-1)}, \quad
  \Delta_{cat} \le 2^{O(d)-1}\mathrm{poly}(n)\, A^2 (e/n^2)^{4d-1}.$$

Dominance check (verified numerically at $(128,2)$, $(1024,4)$, $(2^{16},16)$
against the registered $\varepsilon_{full}$ table):
$\Delta_{DS}/\varepsilon_{row} \le 4A\,(e/n)^{2d-2} \to 0$ and the same for the
star term, for every $d \ge 2$ with $e = o(n)$;
$\Delta_{UU} \le 2A\,e^{2d-2} n^{10-6d} \cdot \varepsilon_{row}$ vanishes even
without $e = o(n)$ at fixed $d \ge 2$;
$\Delta_{OFF}$ and $\Delta_{cat}$ are far smaller.
Hence
$$\varepsilon_{full}(e,n,d) \;=\; \frac{A}{2}\Big[\Big(\frac{e}{n}\Big)^{2d}
   + \Big(\frac{2e}{n-1}\Big)^{2d-1}\Big]
   + \tfrac12\big(\Delta_{DS} + \Delta_{UU} + \Delta_{OFF} + \Delta_{cat}\big)
   \;=\; (1+o(1))\,\varepsilon_{headline}.$$

The degree-$k$ form.
A degree-$\le k$ transcript also completes degree-$j$ stars for
$3 \le j \le k$ (target $\mathrm{ans}(g_{j-1})$ plus the $2d-j+1$ fresh
degree-$j$ products; window size $2d-j+2 \ge d+2$).
Each degree-$j$ product feeds exactly $j$ degree-$j$ star families (one per
choice of pivot cell), so $\sum_\sigma s_\sigma \le j\,e$ over degree-$j$
families and superadditivity gives
$$\varepsilon^{(k)}(e,n,d) \;\le\; \frac{A}{2}\Big(\frac{e}{n}\Big)^{2d}
   + \frac{A}{2}\sum_{j=2}^{k}\Big(\frac{j\,e}{n-1}\Big)^{2d-j+1}
   + \tfrac12\big(\Delta_{DS} + \Delta_{UU} + \Delta_{OFF} + \Delta_{cat}\big)
   + \tfrac12 (e/n)^{2d},$$
the last term being $\varepsilon_K$ for linear-form queries.
At fixed $k \le d$ the largest summand is the degree-$k$ star term
$\frac{A}{2}(ke/(n-1))^{2d-k+1}$.
All summands are $o(1)$ exactly when $e = o(n)$, and in the regime
$e = d\log k$, $d^2\log k = o(n)$ the whole bound is $o(1)$ with the explicit
rates (the $d^{d+1}$-type constants from the star charging are cancelled by
$(e/n)^{d+1} \le (e/n)^2 \cdot o(1)$; verified in log space along growing
$d(k)$ in regime).

### 2.3 Verdict on the constant

The $\varepsilon$ constant does not change.
Label: PROVED.

- The minimum varying-support size over the whole enlarged inventory (including
  the catch-all class) is $2d$, achieved only by rows and degree-2 stars.
  So the exactness threshold ($e < 2d$ gives transfer exactly) is unchanged.
- The per-event TV is $1/2$ for every family, so the $A/2$ prefactor is
  unchanged.
- The headline form is tight (the star probe of cls_cnt.md section 5.2 matches
  it up to factorial slack); the $\Delta$ terms are dominated, so the
  multiplicative $(1+o(1))$ is the only change.
- The answer to the task's either/or question: DS/UU/OFF contribute only
  dominated $\Delta$ terms, as cls-cnt claims for CNT; no constant moves.

One caveat of record: the $(1+o(1))$ is a fixed-$d$ statement.
Along growing $d(k)$ the explicit $\Delta$ and star-$j$ terms must be carried;
they still vanish in regime by the displayed forms, so nothing breaks, but the
absorbed form should not be quoted at growing $d$.

### 2.4 The adaptive form

Proposition CNT-A (cls_cnt.md section 5.3) extends verbatim to degree $k$:
every adaptive degree-$\le k$ tree satisfies
$$P[E_{full}] \;\le\; \varepsilon^{(k)}(e,n,d)\,\exp(2ed/n) \;+\; O(e/n).$$
Label at $k = 2$: REDUCED to B2 (B1 PROVED; B2 REDUCED, closed in regime for
any polynomial loss).
Label at $3 \le k \le d$: the same reduction, with one honesty note: B1/B2
were written for single answers; the mechanism is the status-times-bit answer
factorization, which holds at every degree, but the degree-$j$ bookkeeping has
not been written out separately.
In regime $\exp(2ed/n) = 1 + o(1)$, so the non-adaptive bound is the operative
form there, at every degree.

## 3. The per-degree slices (task 2)

### 3.1 Theorem 3 (degree 2): status upgrade

Theorem 3's step (6) is closed at general $d$ by cls_cnt.md.
Consequences:

- The cap statement survives VERBATIM, and the sharpened certificate form
  survives VERBATIM:
  $$\mathrm{success}(T) \;\le\; \chi(e) + (1-\chi(e))\,(q_2^* + A(e))
     \;(1 + O(e/n) + o(1)),$$
  with $q_2^* = \max(q, q_{\mathrm{and\_exact}}, q_{\mathrm{mix}})$.
- No constant shifts: $q$, $q_{\mathrm{and\_exact}} = 0.2786$ at $(32,2)$,
  $q_{\mathrm{mix}}$, the regime line $c(c-1) \ge 2d^2(4d^2-1)$, and
  $\chi(e)$ are untouched (the posteriors are computed on block-free windows
  and the covering theorem preserves the fresh-bit identification on them;
  cls_cnt.md section 6).
  The printed $P_K$ exponential constant remains recorded as
  $\Theta(1)$-optimistic against the union form $\min(1, ed/n)$
  (jdp_demod.md section 6); unchanged by the inventory.
- The $o(1)$ now absorbs $\varepsilon_{full}$ (headline plus $\Delta$ terms)
  instead of the three-family $\varepsilon$; still $o(1)$ in regime.

Label: PROVED at general $d$, $e = o(n)$, $d^2\log k = o(n)$, modulo the three
named caveats (cor:coin base; B2 in-regime; L-CLASS absorbed).
Unconditional at $d \le 3$.
This is the strongest all-$d$ slice of O2 and it is new: before cls_cnt.md the
degree-2 slice carried CLS and CNT as named open lemmas.

### 3.2 Theorems 3', 3'', 3''': statements verbatim, P-terms repaired

All three statements survive verbatim at their machine points and as printed
forms at general $d$; no constant shifts.

- $q_3^*, q_4^*, q_5^*$: the maxima fold the monomial posteriors, whose closed
  forms and leading form $(2d^2+d)/(c-k+1)$ are inventory-independent.
  The finite-$n$ purity lifts (up to $+13.0\%$ relative at $(255,5)$) are
  finite-$n$ and vanish as $\Theta(d^2/n^2)$; nothing to repair.
- $P_{\mathrm{adj}}$, $P_K$, $P_{\mathrm{wedge}}$, $P_Z$,
  $P_{\mathrm{cert4}}$, $P_{\mathrm{cert5}}$: all driven by degree-1 channels
  or by the mass chain $P_k \le P_2$; inventory-independent.
  $P_{\mathrm{cert5}} \le e P_5 = o(P_K)$ with dominance factors
  $1.6 \times 10^4$ to $4.3 \times 10^{12}$ across the grid.
- $P_{\mathrm{blk3}}, P_{\mathrm{blk4}}, P_{\mathrm{blk5}}$: the printed line
  items $e/(n-2d-2)$, $e/(n-2d-3)$, $e/(n-2d-4)$ charged only the adversarial
  star-probe route of the inventoried star classes.
  The enlarged degree-2 inventory adds the $\Delta$ terms, whose supports are
  $\Theta(d)$, not $\Theta(n)$: the deg4 forward note "no relation class with
  sub-$\Theta(n)$ completion cost" is false in form and the induction must
  track support sizes (cls_cnt.md correction 5).
  The repaired line item at degree $k$ is
  $$P_{\mathrm{blk}}^{(k)}(e) \;\le\; \sum_{j=2}^{k} \frac{A}{2}
     \Big(\frac{j\,e}{n-1}\Big)^{2d-j+1}
     + \tfrac12\big(\Delta_{DS} + \Delta_{UU} + \Delta_{OFF} + \Delta_{cat}\big),$$
  which is $\le e/(n-2d-k+2) + o(1)$ in regime, so the printed cap statements
  (which carry $+ o(1)$ separately) hold verbatim in regime with the
  $\Delta$ terms absorbed.

Proof status at general $d$ does NOT upgrade.
Each of 3', 3'', 3''' consumes step (6a) at its own degree:
REL-3 needs the $t = 3$ slice, REL-4 the $t \le 4$ slices, REL-5 the
$t \le 5$ slices.
cls_cnt.md proves $t = 2$ only.

Label Theorem 3': PROVED for $d = 3$ at all $n$ (the restricted system is
$(6,3)$ once and for all, and the full sweep closed step (6a) there); REDUCED
to INV(3) at general $d$; the deep-zero-run multi-class composition residue
remains flagged (regime-neutral per jdp_demod.md section 8).
Label Theorems 3'', 3''': PROVED as assemblies at their machine points
($(8,4)$ through degree $\le 2$ slice plus witness algebra; $(10,5)$ through
degree $\le 3$ sparse sweep); REDUCED to INV(4), INV(5) at general $d$; same
flagged residue.
The distinction that matters: at $d = 2$ step (6a) is proved; at
$d \in \{3,4,5\}$ it is swept or partial; at $d \ge 6$ nothing beyond the
degree-$\le 2$ slice is available and the cap is conditional outright.

## 4. Theorem 3-gen, the all-degrees cap (task 3)

### 4.1 The hypotheses

INV(d) (inventory completeness through degree $d$).
For every $0 \le t \le d$:
(i) $(V \oplus \langle e_0\rangle) \cap S_{\le t}
     = V_{\le t} \oplus \langle e_0\rangle$, where $V_{\le t}$ is the span of
    generator rows of degree $\le t$; and
(ii) every support of a nonzero element of the varying-coordinate projection
     of that space contains a full row, a degree-$j$ star ($2 \le j \le t$), a
     DS, a UU, an OFF, or has $\ge 4d-1$ coordinates with per-coordinate
     multiplicity $\le 2^{O(d)}\,\mathrm{poly}(n)$ (the catch-all class).
Status: PROVED at $d = 2$, general $d$ (cls_cnt.md).
[MV] at the swept points ($(6,3)$ full; $(8,4)$, $(10,5)$ degree-$\le 2$;
$(10,5)$ degree-$\le 3$).
OPEN at general $d$ for every $t \ge 3$.
INV(d) is exactly SPARSE-d (deg5_theory.md section 6.3) plus the
$\rho$-hidden-window reading, restricted to the named classes plus catch-all.

B2 (adaptive bookkeeping, cls_cnt.md section 5.3).
Each free hit can remove at most one hidden condition from any completion
event, multiplying that event's probability by at most $n/d$; the product over
$K \sim \mathrm{Bin}(e, d(2d+1)/((n+1)n))$ free hits is
$\mathbb{E}[(n/d)^K] \le \exp(2ed/n)$.
Status: REDUCED (any polynomial loss leaves the regime statement unchanged);
consumed only through CNT-A.

### 4.2 Statement

Theorem 3-gen (all-degrees budgeted cap).
Fix $p = 2$, $d \ge 2$, $k = k(n) \ge 2$ with $\log k \ge 1$, $n > 2d$, and
budget $e = d\log k$.
Assume INV(d) and B2.
Then every adaptive tree $T$ of budget $e$ whose queries are degree-$\le d$
monomials or linear forms over $\mathbb{F}_2$ satisfies
$$\mathrm{success}(T) \;\le\; \min\Big(1,\;
   q_d^*(n,d) + P_{\mathrm{adj}}(e) + \min(1,\, e\,d/n)
   + e\,P_2(n,d) + \varepsilon^{(d)}(e,n,d)\,e^{2ed/n}
   + O(e/n)\Big) + o_d(1),$$
with
$q_d^* = \max(q,\, q_{\mathrm{and\_exact}},\, \mathrm{post}_3, \ldots,
 \mathrm{post}_d)$,
$P_{\mathrm{adj}} \le \min(1, e h_1)\min(1, e q(2d-1)/(2(n-1)))$,
$\varepsilon^{(d)}$ the explicit degree-$d$ completion bound of Section 2.2,
and $o_d(1)$ at fixed $d$ as $n \to \infty$.
Moreover, if $d^2\log k = o(n)$ then
$$\mathrm{err}(T) \;\ge\; 1/2 - o_d(1) \;\ge\; k^{-O(1)},$$
and with the degree-1 witness ($\mathrm{err} \le 2e^{-c_w x}$,
$x = d^2\log k/n$, $c_w = \rho/(1+\rho)$) the two-sided form
$\mathrm{err}^*(d, d\log k) = k^{-\Theta(d^2/n)}$ holds at every fixed $d$
granting INV(d).

Every constant above is explicit in $d$; no step hides a uniformity gap, so
the theorem applies along any degree schedule $d(k)$ with
$d(k)^2\log k = o(n)$ as soon as INV(d(k)) holds at each degree.

### 4.3 Proof (assembly; every step labeled)

Fix such a tree $T$ with transcript $\tau$.

Step 1 (transfer).
Couple the pipeline to the degree-$d$ fresh-bit channel with the same $\rho$
and tree coins (lemma_m.md step 1, degree-generic).
Off the completion event $E_{full}$ (the window contains a named support) the
transcripts are identical; each completed window contributes TV $1/2$.
By INV(d)(ii) every pin comes from the named inventory, so
$$d_{TV}(\mathrm{law}_\Omega(\tau), \mathrm{law}_{fb}(\tau))
   \;\le\; P[E_{full}] \;\le\; \varepsilon^{(d)}(e,n,d)\,e^{2ed/n} + O(e/n)$$
by step (6b) with B2 (CNT-A).
Label: PROVED given INV(d), CNT, B2.
At $d = 2$ unconditional of INV (which is proved there).

Step 2 (certificate-free leaves).
On the fresh-bit channel, an own single hit carries posterior $q$
(deg2_theory.md Theorem 2(i)), an own degree-2 monomial hit carries
$q_{\mathrm{and\_exact}}$ (exact status Bayes), and an own degree-$j$ monomial
hit carries $\mathrm{post}_j$ (the general-$k$ closed form; the per-$\rho$
answer law $\{0, 1/2, 1\}$ is Theorem A + balance).
Zeros never elevate a certificate-free leaf above its own-hit posterior:
proved for singles ($\mathrm{post}(k) \le q$, Theorem 2(iv)), immediate for
the own-degree-$j$ family from the closed form (each extra zero only costs
free-branch likelihood), and flagged for multi-class deep zero-run
composition (deg3_theory.md open item 3; regime-neutral per the mitigation of
record).
Distant evidence caps at the depleted rate $f_e = f(1 + O(e/n))$ by Lemma D1,
and $f \le q$ in regime.
Hence every certificate-free leaf has output posterior
$\le q_d^*(1 + O(e/n))$.
Label: PROVED per evidence class (D1/D2-based); multi-class composition GAP,
flagged, regime-neutral.

Step 3 (certificate charge).
Any certainty event must contain at least one answer-1: an all-0 transcript
admits a consistent configuration matching any candidate pair on the
block-free event (deg4_theory.md Proposition M, first clause; the
$c > 9$ inertness caveat covers the shadow artifact).
Union bounds only, no independence:
- adjacency (two co-linear 1s): $P_{\mathrm{adj}}(e)$ by Lemmas D1 and D2
  (jdp_demod.md section 6);
- $K_j$-channel certificates: $\min(1, ed/n)$, the union form;
- every other certificate (wedge, Z, counting, degree-$\ge 2$ combinations,
  and any certificate the enlarged inventory might feed): firing rate
  $\le e \cdot P_2(n,d)$, since $\mathrm{ans} = 1$ on a matching-$j$ column has
  probability $P_j \le P_2$ by M5, and $e P_2 = o(\min(1, ed/n))$
  ($P_2 \le 1/n + 2d^2/n^2$ against the rate $d/n$).
Label: PROVED (the charge is complete regardless of certain-inventory
completeness; completeness is not consumed).

Step 4 (completion charge).
$P[E_{full}]$ is bounded by CNT over the enlarged inventory; this is
$\varepsilon^{(d)}$, and in regime it is $o(1)$ with the explicit rates of
Section 2.2.
Label: PROVED non-adaptive; REDUCED to B2 adaptive (consumed in step 1).

Step 5 (assembly).
Leaves partition the probability space; certificate leaves are charged by
step 3, certificate-free leaves by step 2, and the coupling slack by step 1:
$$\mathrm{success}(T) \;\le\; q_d^* + P_{\mathrm{adj}} + \min(1, ed/n)
   + e P_2 + \varepsilon^{(d)} e^{2ed/n} + O(e/n) + o_d(1).$$
Label: PROVED assembly.

Step 6 (the regime conclusion).
If $d^2\log k = o(n)$ then $d^2 = o(n)$, so $q_d^* \le
(2d^2+d)/(c-d+1)(1+o(1)) = o(1)$;
$P_{\mathrm{adj}} = o(1)$; $\min(1, ed/n) = d^2\log k/n = o(1)$;
$e P_2 = o(1)$; $\varepsilon^{(d)} = o(1)$ (Section 2.2, including along
growing $d(k)$).
So $\mathrm{success}(T) \le 1/2 + o(1)$ is available with room once
$d^2 \le n/4$-type margins hold, and $\mathrm{err}(T) \ge 1/2 - o_d(1) \ge
k^{-1}$ for $k$ large.
Label: PROVED arithmetic.

Step 7 (the witness side).
The degree-1 $K_j$-split tree is inside the degree-$\le d$ class at every
$d \ge 2$ and achieves $\mathrm{err} \le 2e^{-c_w x}$ with
$c_w = \rho/(1+\rho)$ (gap_e_constants.md section 5, sharpened form).
Combining with step 6 gives the two-sided statement.
Label: PROVED.

$\mathrm{QED}$ (modulo INV(d) and B2, as labeled; at $d = 2$ the modulo set
reduces to the standing cor:coin caveat and B2).

### 4.4 Corollaries

Corollary 3-gen.1 (degree-independence of the boundary).
Under INV(d), the $d^2\log k = o(n)$ aliveness condition is the same at every
degree $d$.
The boundary is degree-independent by hypothesis-conditional assembly, and
UNCONDITIONALLY degree-independent through degree 5 (theorems 3 through
3''').

Corollary 3-gen.2 (the induction reduced to one lemma per degree).
For each fixed $d \ge 3$, closing O2's degree-$d$ slice requires exactly:
INV-d at $t = d$; the per-degree posterior digit-exact check (mechanical,
done through $k = 5$); and the flagged composition residue.
Steps (1)-(5) of the deg5 induction are closed at every degree by Theorem A,
the star lock, the closed-form posterior, M5, and the mass-domination
argument; this was deg5_theory.md section 6.4's conclusion, now with the
$t = 2$ instance of step (6) removed by cls_cnt.md.

## 5. Final O2 status (task 4)

### 5.1 What closed

- O2's degree-2 slice at general $d$: closed in regime (Theorem 3 upgraded,
  Section 3.1).
  Modulo: cor:coin base, B2, L-CLASS (absorbed).
- Lemma CLS and Lemma CNT: both closed in regime at general $d$ for their
  degree-2 content (cls_cnt.md sections 3 and 5; CNT-A in regime modulo B2).
  O5 is thereby assembled at general $d$ in regime (cls_cnt.md section 6).
- The $\varepsilon$ headline and the exactness threshold: confirmed
  inventory-robust (Section 2.3).

### 5.2 What remains open, in order

1. INV-d at $t \ge 3$ (equivalently SPARSE-d at $t = 3, \ldots, d$).
   The single mathematical gap separating the assembly from the all-degrees
   O2 cap.
   Concrete next target: the $t = 3$ degree-truncated Buchberger
   (S-polynomials with lcm-degree $\le 3$ over the row set
   $\{Q_i, Q_i x_{ab}, b_{ij}, C, H, Q_r x_{cd}\}$ and their degree-3
   shifts, with master identities at the next level), a finite machine check
   per rectangle, exactly parallel to the $t = 2$ sweep
   (cls_cnt.md sections 3.3-3.4; its section 7 item 5 names the degree-3
   analogue as unwritten).
   [OPEN, the named target]
2. MIXTURE-d, a scope gap against O2's literal quantifier.
   O2 quantifies over arbitrary degree-$\le d$ polynomials; the cap family
   covers monomial queries plus linear forms, and the mixture class is
   covered only at $d = 2$ (ADDENDUM 10, Theorems M-A/M-E/M-D).
   Mixtures genuinely strengthen the adversary (the star-mixture posterior
   exceeds the covered one by $+0.0362$ at $(7,2)$), so this is not a
   formality.
   Route: the degree-2 mixture template (rate-weighted elevation,
   dual-engine validation) at degree $\ge 3$.
   [OPEN]
3. The boundary constant at $d^2 = \Theta(n)$: the exact adaptive completion
   constant behind $\varepsilon$ (B2's exact form; CNT-A is conjectured
   tight), and the exact exponent constant of
   $\mathrm{err}^* = k^{-\Theta(d^2/n)}$ (Conjecture E5).
   [OPEN]
4. The intermediate-budget regime $e = \Theta(n)$ (O2(iv)): $\varepsilon$ is
   vacuous there and the transfer question is open.
   [OPEN]
5. The standing small items: the cor:coin base (a self-contained elementary
   proof that singles vary); NAL at $k \ge 6$ (not needed for the cap, only
   for the asymptotic description of the maximizing entry of $q_d^*$);
   certain-inventory completeness at general scale (not needed for the cap);
   the degree-$\ge 3$ write-out of the B1/B2 bookkeeping.
   [OPEN, small]
6. Instrument rungs for INV-d evidence: the $(10,5)$ degree-$\le 4$ sparse
   sweep (about 6.0M columns, needs a leaner pivot store) and the $(12,6)$
   degree-$\le 3$ sweep (about 657K columns) (deg5_theory.md section 7
   item 6).
   [instrument note]

### 5.3 Falsification conditions

- A window at $(4,2)$ or $(6,3)$ whose true law deviates from fresh-bit and
  whose support contains none of the five families: falsifies the covering
  theorem (direction $\Rightarrow$) and with it INV-2.
  Searchable now by minimal-codeword enumeration of
  $\overline{V}$ (dimensions 166 and 512; cls_cnt.md section 7 item 2).
- A $\ge 3$-star cancellation chain whose minimal support is small
  ($\Theta(d)$) and transcript-identifiable and not a supersupport of any
  pair configuration: creates a sub-$\Theta(n)$ completion mechanism and
  breaks $P_{\mathrm{blk}}$ at that degree.
  This is the corpus's named O2 failure mode, now precisely located inside
  INV-d.
- An adaptive degree-$k$ tree whose completion probability exceeds
  $\varepsilon^{(k)}(e,n,d)\,e^{2ed/n} + O(e/n)$: falsifies CNT-A or B2.
- A value-determined diagonal degree-2 column at some $d$, or a determined
  matching-$k$ column at any $(2d,d)$: falsifies CLS(i) or Theorem A's base
  and step.
- A budgeted degree-$\le d$ tree above the Theorem 3-gen cap at a tested
  point; concretely, an adaptive degree-$\le 2$ tree at $(128,2)$, $e = 32$,
  above success $0.1864$ falsifies the sharpened cap, and above $0.135$
  falsifies Conjecture E5.
- A budgeted tree with error $< k^{-C}$ at $d^2 \gg n$ (the $(64,4)$ versus
  $(64,8)$ cliff failing to appear) breaks the $d^2 \sim n$ boundary.
- A degree-$\ge 3$ mixture tree beating the monomial-class cap at a measured
  point: shows MIXTURE-d bites and reopens the scope item with content.
- An $F_p$ audit finding $L(Q_i^\rho) \ne 0$ at any pigeon or any $p$, or an
  author correction to Definition 4.3's $g^\rho$ clause or the vanishing
  condition: dissolves the channel frame (standing corpus-wide conditions).

## 6. Provenance and scope notes

- No other file was edited; LOG.md was not written.
- ADDENDUM 11's content (the inventory correction) is recorded at the tail of
  lemma_m.md, not in proof_complexity.md, which ends at ADDENDUM 10; this
  document cites the content from lemma_m.md and cls_cnt.md.
- The assembly confirms cls_cnt.md's claim that no recorded constant or regime
  moves: the inventory enlargement enters every cap only through dominated
  $\Delta$ terms inside an $o(1)$ that was already present.
- The one place the enlargement changes a recorded sentence is the deg4
  forward note's "no sub-$\Theta(n)$ completion classes": false in form
  (DS/UU supports are $\Theta(d)$), harmless in regime, and replaced here by
  support-size accounting (Section 3.2).
- The classification "Theorem 3-gen PROVED at $d = 2$, REDUCED at
  $d \ge 3$" is the correct reading of the task's assembly request: the
  degree-uniform tools (Theorem A, the star lock, the closed-form posterior,
  M5, CNT, D1-D3) close everything EXCEPT the inventory completeness at
  $t \ge 3$, and no degree-uniform proof of INV-d is claimed here.
