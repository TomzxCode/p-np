# Audit: arXiv:2510.08814 "P != NP: A Non-Relativizing Proof via Quantale Weakness and
# Geometric Complexity" (Ben Goertzel; v1 Oct 2025, v2 22 Apr 2026)

Auditor: this session, 2026-10-03, from the arXiv HTML v1 full text (saved locally).
Verdict: the proof fails. Two independent, quote-anchored findings below. This is a session
audit, not peer review; both findings are stated so a defender can address them directly.

## The argument's skeleton (as the paper states it)

M0: ensemble $D_m$ = masked random 3-CNF + VV isolation, conditioned on unique satisfiability,
"efficiently samplable"; weakness measure $K^{\mathrm{poly}}$.
M1: per-bit unpredictability: for sign-invariant views, $\Pr[X_i = 1 \mid I] = 1/2$ (neutrality), and
restricted decoders (tiny ACC0 on $O(\log m)$ inputs) have per-block advantage $\le \varepsilon(m)$
(Lemma 2.15), plus template sparsification $m^{-\Omega(1)}$ per fixed local rule.
M2: Switching-by-Weakness (Theorem 4.2): for every poly-time decoder P of description length
$\le \delta t$, a short wrapper W makes $(P \circ W)$ (a) per-bit local (output bit = function of
$u = (z, a_i, b)$, $|u| = O(\log m)$) on a $\gamma$-fraction of blocks, and (b) dominating P's success
up to $m^{-\Omega(1)}$ slack.
M3: success $\le (1/2 + \varepsilon)^{\gamma t} = 2^{-\Omega(t)}$ for every such decoder; Compression-from-
Success gives $K^{\mathrm{poly}}(\text{witness tuple}) \ge \eta t$ whp.
Clash: under $P = NP$ a constant-length solver gives $K^{\mathrm{poly}} \le O(1)$. Contradiction, hence $P \neq NP$.

## Finding 1: the isolation parameter k is internally inconsistent (kills M0)

- Definition 2.10 (VV labels): $a_i := A e_i \in \{0,1\}^k$, and "($a_i$, $b$); their total length is
  $O(\log m)$ per block." So the paper's working regime has $k = O(\log m)$.
- Section 3.1: "Fix clause density $\alpha > 0$ and integers $m \ge 1$ and $k = c_1 \log m$."
- Section 3.6 parameters: "VV parameters: $k = c_1 \log m$, $\delta = m^{-c_2}$."
- Section 7.4 (consolidated): "VV layer: $k = c_1 \log m$ ...; isolation succeeds with $\Omega(1/m)$
  probability and we condition on uniqueness."
- Lemma 2.12: isolation probability $\ge c/m$ holds for "$k \in \{0,1,\ldots,m-1\}$ chosen uniformly", and
  the proof sketch says "$k$ uniform in a logarithmic window around $\log_2 |S|$". For the ensemble's
  own instances (subcritical random 3-CNF with $S = 2^{\Theta(m)}$ solutions), $\log_2 |S| = \Theta(m)$,
  so the window sits at height $\Theta(m)$: $k$ must be $\Theta(m)$ w.h.p.

These cannot both hold. Quantitatively, with $k = c_1 \log m$ fixed rows and near-uniform $b$, a CNF
with $S = 2^{\beta m}$ solutions has expected constrained-solution count $S \cdot 2^{-k} =$
$2^{\Theta(m)}/\mathrm{poly}(m) \to \infty$, and the probability of exactly one solution is at most
$\approx \exp(-S \cdot 2^{-k})$, double-exponentially small. Consequences:
- With $k = c_1 \log m$: $\mathrm{Unq}(\Phi)$ has probability $\approx 0$, $D_m$ is NOT efficiently samplable, and Lemma
  2.12's "expected $O(m)$ trials" is false. The ensemble M0 does not exist as described.
- With $k = \Theta(m)$ (what isolation actually needs): the labels ($a_i$, $b$) are $\Theta(m)$ bits per
  bit, so Definition 2.10's $O(\log m)$ budget, Theorem 4.2's post-switch input size
  ($|u| = O(\log m)$, Section 4.3), Lemma 2.15's tiny-ACC0-on-$O(\log m)$-inputs hypothesis, the
  $m^{O(1)}$ chart count with $2^{O(k)}$ factor in A.4, and the neutrality/calibration accounting
  for label-dependent rules all fail simultaneously.
No choice of $k$ rescues M0 + M2 together.

## Finding 2: the switching lemma's locality and domination cannot both hold (kills M2)

Lemma 4.3 ("Symmetrization preserves success exactly") is correct: each symmetrized prediction
$\mathrm{BM}_\sigma(P(g_\sigma(\Phi)))$ has exactly P's success, by measure/promise preservation.
The A.1 sketch then claims the majority of these predictions "matches the Bayes rule on the
local $\sigma$-field for all but $o(t)$ blocks" and that "the overall success does not decrease by
more than $m^{-\Omega(1)}$" (Theorem 4.2's domination), concluding the output is per-bit local.

Apply this to the one decoder the argument must handle: the $P = NP$ solver.
- For it, $\mathrm{BM}_\sigma(P(g_\sigma(\Phi))) = X_i$ for every $\sigma$ (the solver solves the sign-flipped
  formula exactly and the back-map flips the bit back). The majority is $X_i$ exactly, on every
  block, with success 1: domination would hold.
- But Theorem 4.2's locality conclusion says this majority output is a function of the local
  view $u = (z, a_i, b)$ on a $\gamma$-fraction of blocks. By the paper's own M1 (neutrality +
  Lemma 2.15), no function of the $O(\log m)$-bit local view can predict $X_i$ with constant
  advantage, let alone certainty, on a constant fraction of blocks: a function of $u$ that equals
  $X_i$ on $\gamma t$ blocks has average advantage $\ge \gamma/2$, contradicting advantage $\le \varepsilon(m)$.
So for P = the solver, exact domination and locality are jointly impossible; the Chernoff and
Hoeffding steps in A.1 only ever bound accuracy of the majority, they never produce locality.
The same collapse hits the ERM wrapper: ERM distills P into the best local rule, whose quality
is exactly what M1 caps, so the distilled comparator cannot dominate a solver with success 1.

## Proposition 1 (the trilemma, formal; added 2026-10-03)

Setting: $(\Phi, X)$ with $X = X(\Phi)$ a function of $\Phi$; $D$ any distribution on $\Phi$; $V$ any function
of $\Phi$ with $|V(\Phi)| = O(\log m)$ bits (the local view). Call a randomized procedure Q
"V-determined with failure $\delta$" if, over seeds fixed to good values (deterministically),
$Q(\Phi) = X(\Phi)$ for all but a $\delta$-fraction of $D$; call it "V-local" if its output is a
deterministic function of $V(\Phi)$.

Claim: if there exists a program P and wrapper W such that $Q = P \circ W$ is simultaneously
(1) V-determined with failure $\delta$, (2) V-local, and (3) every deterministic function $h$ of
$V(\Phi)$ satisfies $\Pr_D[h(V(\Phi)) = X(\Phi)] \le 1/2 + \varepsilon$, then $\varepsilon \ge 1/2 - \delta$.

Proof. By (1) and (2), the function $h^* := \Phi \mapsto Q(\Phi)$ (seeds fixed) is a deterministic
function of $V(\Phi)$ with $\Pr_D[h^*(V(\Phi)) = X(\Phi)] \ge 1 - \delta$. But (3) applied to $h^*$ gives
$\Pr \le 1/2 + \varepsilon$. Hence $1 - \delta \le 1/2 + \varepsilon$. QED.

Consequence for arXiv:2510.08814: their Lemma 2.15 is exactly condition (3) with
$\varepsilon(m) \to 0$, and their domination requirement is condition (1) with $\delta = m^{-\Omega(1)}$
$\to 0$. The proposition shows conditions (1)+(2)+(3) cannot hold jointly for any P that
solves the instance - in particular for the $P = NP$ solver their self-reduction step must
apply to - no matter how the wrapper is constructed, because once the wrapper's seeds are
fixed, "success domination" and "locality" force the inequality. This upgrades Finding 2
from an analysis to a statement: their Theorem 4.2's locality conclusion and domination
requirement are jointly inconsistent with their own Lemma 2.15 whenever P succeeds with
probability $1 - o(1)$. The only escape is denying that the switching normal form produces a
deterministic function of the local view - which is precisely the locality claim itself.

Scope note: this is a two-line pigeonhole once the definitions are set; its value is
removing the possibility that a probabilistic subtlety in the wrapper circumvents Finding 2.
The nontrivial question remains where exactly the paper's Lemma 4.3-to-Theorem 4.2 step
breaks, and the proposition localizes that: it must be the locality conclusion, since the
other two conditions are what their lemmas explicitly supply.


## What would have to change

- Isolation and label budget must be made consistent: either give up efficient samplability
  (and rebuild all compression arguments for promise-only ensembles) or give up the
  $O(\log m)$ local input budget (and rebuild M1/M2 for $\Theta(m)$-bit views, where nothing
  obstructs a local rule from reading enough to solve the block).
- The switching step needs a genuine locality-producing mechanism, not accuracy bounds.
  As stated, symmetrization is accuracy-preserving only.

## References (arXiv HTML v1 section anchors)

- Def 2.10 (labels, $O(\log m)$); Lemma 2.12 + sketch ($k \in \{0,\ldots,m-1\}$); Remark 2.13 (promise);
- Sec 3.1 ($k = c_1 \log m$; Def 3.3); Sec 3.6 (parameters); Lemma 3.6 (involution, $b \mapsto b \oplus a_i$);
- Thm 4.2 / Lemma 4.3 (switching, symmetrization); Sec 4.3 ($|u| = O(\log m)$, ERM);
- Lemma 2.15 (restricted advantage); Sec 6.3-6.4 (small success, constants);
- Sec 7.4 (consolidated parameters); A.1 (majority/Bayes step); A.4 ($2^{O(k)}$ pattern count).

## Addendum (2026-10-03, monitor pass 2)

Independent external convergence: pith.science (a machine-review service) lists the paper
with a REJECT verdict and a referee/author exchange (precision, 2026-10-04 monitor: the
exchange is pith's machine-SIMULATED author rebuttal; Goertzel himself has not responded) (https://pith.science/paper/2510.08814).
Its objections — the normalization theorem "invoked but neither formally stated nor proved",
no construction or sampling procedure for the ensemble Y, Compression-from-Success asserted
without supporting lemmas — are abstract-level statements of this audit's F5/F4 findings,
reached independently. No new technical content; no academic commentary or citations found
(OpenAlex cited_by_count = 0). Also recorded: v1's title said "Proof", v2's says "Route".
Version history corrected above: v2 is dated 22 Apr 2026 (an earlier note here and in
clues.md said Aug 2026; the arXiv submission history is authoritative).
