# The Ladder: what a genuine P != NP proof must climb (state verified 2026-10-03)

Companion to `clues.md` section 7. Every statement below was checked against the primary
source (venue page, ECCC, or arXiv) in this session unless marked otherwise.

## The rungs, weakest to strongest conclusion

- R1 (done, 2010): NEXP is not in ACC^0 (Williams, via a $2^n/2^{n^\epsilon}$ SAT algorithm for ACC
  circuits). Extended 2018 to NEXP not in $\mathrm{ACC}^0 \circ \mathrm{THR}$ (Murray-Williams).
- R2 (frontier, open): NEXP is not in TC^0. Best depth-2 result: Chen-Tal-Wang (STOC 2026,
  ECCC TR26-039): some $f$ in $\mathrm{E}^{\mathrm{NP}}$ needs n^{2.5-eps}-size THR o THR circuits, any $\epsilon > 0$.
  First superquadratic bound; previous record $n^{2-o(1)}$ (Tamaki 2016; Alman-Chan-Williams
  FOCS 2016). The engine is again Williams' method: a $2^{n - n^{\Omega(\epsilon)}}$-time algorithm
  estimating the acceptance probability of an XOR of two $\mathrm{THR} \circ \mathrm{THR}$ circuits.
- R3 (open): NP is not in $\mathrm{SIZE}[n^k]$ for all fixed $k$. Nothing beyond linear for any NP problem
  in general circuits; explicit general-circuit lower bounds sit at 3.1n - o(n) over the basis
  B2 and 5n - o(n) over U2 (Lachish-Iwama; Iwama-Morimae).
- R4 (the goal): $\mathrm{P} \ne \mathrm{NP}$. R3 implies it; nothing weaker known implies it.

## The precise open conditions that would trigger each next rung

1. To get NEXP not in TC^0, any one of:
   a. Quantified derandomization improvement: derandomize TC^0 circuits with $n^{1+O(1/d)}$
      wires (Chen-Tell 2019 achieved $n^{1+\exp(-d)}$; their paper proves the improvement to
      $n^{1+O(1/d)}$ in time $2^{n^{\exp(-d)}}$ would yield standard derandomization of TC^0 and
      hence NEXP not in TC^0).
   b. k-SAT in $2^{n(1 - 1/k^{1/\omega(\log\log k)})}$ time (Murray-Williams framework; current
      record algorithms run in $2^{n(1 - 1/O(k))}$: PPSZ family, biased-PPSZ 2019, improved
      analyses 2022-2024; general 3-SAT randomized $\sim 1.307^n$, deterministic $1.32793^n$, 2018).
   c. A CAPP (acceptance-probability estimation) algorithm for $\mathrm{THR} \circ \mathrm{THR}$ at $2^n/n^{\omega(1)}$.
      The known blocker is structural, not algorithmic: the Williams reduction needs the class
      closed under OR (the Chen-Tal-Wang breakthrough computes the XOR of two circuits, and
      "we do not know how to convert a large OR of THR o THR circuits into an equivalent THR o
      THR circuit" - documented verbatim in the ToC journal version of the THR-evaluation
      work). This OR-closure gap is the single most concrete technical obstacle on R2.
2. To get NP not in P/poly via magnification (the alternative route that bypasses natural
   proofs): prove $n^{-\epsilon}$-$\mathrm{MCSP}[\sigma]$ is not in $\mathrm{PFML}[n^{2\epsilon+o(1)}]$ for some $\epsilon > 0$ and
   $\sigma \le 2^{n^{o(1)}}$ (Chen-McKay-...-2025 "Simple general magnification", Theorem 9).
   Known: $\mathrm{MCSP}[2^{\sqrt{\ell}}]$ is not in $\mathrm{PFML}[n^{2-\delta}]$ for every $\delta > 0$ (Hirahara-
   Santhanam; pseudorandom restrictions), and the 2025 thresholds are proven sharp. The gap
   to the magnification threshold is a single $\epsilon$-parameter in the exponent: $n^{2-\delta}$ for
   all $\delta$ is known, $n^{2\epsilon+o(1)}$ for one fixed $\epsilon$ is needed.
   Also open and "almost known": $\mathrm{P} \ne \mathrm{NP}^{\text{xor-P}}$ would follow from $n^{-\epsilon}$-$\mathrm{MCSP}[\sigma]$ not
   in $\mathrm{P}$-uniform-$\mathrm{SIZE}[n^{1+\epsilon+o(1)}]$ (same paper, Theorem 11), given Santhanam-Williams'
   $\mathrm{P}$ not in $\mathrm{P}$-uniform-$\mathrm{SIZE}[n^c]$.
3. To get R3 directly: any $\omega(n)$ explicit lower bound over B2 (45-year stall at $3.1n$).

## Barriers each attempt must dodge (updated this session)

- Natural proofs (Razborov-Rudich, conditional on PRGs): now with an unconditional
  instantiation for AC0 - arXiv:2606.12631 (June 2026) builds an unconditional depth-$d$ PRF of
  size $2^{n^{O(1/d)}}$ fooling AC0 distinguishers (localized Trevisan-Xue) and proves no
  poly-size constant-depth natural property can show $2^{n^{7/(d-5)}}$ lower bounds at depth $d$,
  with the self-referential twist that the Switching Lemma proves the Switching Lemma cannot
  prove more. For TC^0 the conditional barrier stands (DDH/LWE-based PRFs in TC^0), and the
  exact-complexity results of 2021 show restriction-based methods provably cannot improve the
  known $n^{1+\Omega(c^{-d})}$ wire bounds.
- Relativization and algebrization: unchanged; both directions have oracle worlds.
- Localization: many techniques survive small-fan-in oracle gates (so they cannot prove the
  magnification thresholds); Santhanam-Williams and the 2025 distinguisher method are the
  known non-localizing exceptions.
- The audit trilemma (new here): any framework that (i) applies to all poly-time deciders,
  (ii) converts them to a locality-style normal form, and (iii) preserves success through the
  conversion, is inconsistent on $\mathrm{P} = \mathrm{NP}$ algorithms - exact domination, locality, and per-block
  small-advantage cannot all hold (Goertzel arXiv:2510.08814 is the case study; see
  `goertzel_audit.md`). This is the distributional analogue of why Razborov-Rudich blocks
  natural proofs: lower-bound arguments must exploit something global about the hard function,
  not a normal form of arbitrary efficient computation.

## Fresh 2026 signal: machine-assisted lower-bound proofs are real

arXiv:2609.38677 ("Top-Down Lower Bounds for All Depths", Sept 2026) completes the top-down
program for parity at every constant depth ($\exp(\epsilon_d n^{1/(d-1)})$ bounds, tight up to
constants) and explicitly documents a human-machine collaboration: the human identified that
a strengthened "light patterns lemma" would suffice; the machine found the proof (a reverse-
hypercontractive inequality route, later simplified to a "harmonic mean transform"). Contrast
with the solo-AI-celebrity P vs NP attempts that died in this session's audits. The workable
division of labor appears to be: human picks the invariant, machine searches lemma space.

## Anatomy of the frontier result (added 2026-10-03): why THR o THR is stuck at polynomial

Verified from the ECCC TR26-039 abstract, the group's earlier ToC journal paper, and an
elementary closure check.

- The result: some $f$ in $\mathrm{E}^{\mathrm{NP}}$ requires $n^{2.5-\epsilon}$-size $\mathrm{THR} \circ \mathrm{THR}$ circuits for every $\epsilon > 0$
  (first superquadratic; previous record $n^{2-o(1)}$, Tamaki 2016 and Alman-Chan-Williams
  FOCS 2016). Engine: a $2^{n - n^{\Omega(\epsilon)}}$-time algorithm estimating the acceptance
  probability of an XOR of TWO $n^{2.5-\epsilon}$-size $\mathrm{THR} \circ \mathrm{THR}$ circuits, plugged into Williams'
  algorithmic method.
- Why the classical theorem templates do not apply: the Williams reductions (and the ToC
  paper's Theorem 2.10: a $2^{n - n^\epsilon}$ counting-SAT algorithm for C-circuits gives NEXP no
  quasi-polynomial C-circuits) require the class to be "typical": closed under composition,
  unbounded-fan-in AND, OR, and NOT. $\mathrm{THR} \circ \mathrm{THR}$ provably fails this at the top gate. The
  elementary core: $(x_1 \land x_2) \lor (x_3 \land x_4)$ is not a threshold function of $(x_1, \dots, x_4)$, so
  even the OR of two LTFs is not in general an LTF; merging two top gates into one fails the
  same way. For ACC, by contrast, OR/AND/XOR composed with ACC stay in ACC, which is exactly
  why Williams' 2010 argument went through there. The ToC paper states the consequence
  verbatim: "We do not know how to convert a large OR of THR o THR circuits into an
  equivalent THR o THR circuit, even assuming NEXP has small THR o THR circuits."
- The CTW26 workaround: the reduction is arranged so that only the XOR of TWO circuits'
  acceptance probabilities is ever needed, and the new estimation algorithm handles that
  structure directly, avoiding the OR-merge.
- The exact remaining gap: the estimation algorithm's runtime degrades with target size $s$
  ($s = n^{2.5-\epsilon}$ against $2^{n - n^{\Omega(\epsilon)}}$). Quasi-polynomial $\mathrm{THR} \circ \mathrm{THR}$ lower bounds
  would need estimation with $2^n/\mathrm{poly}$-type loss for $s = n^{\omega(1)}$; no such trade-off is
  known, and each constant improvement in the s-exponent has historically cost a new
  estimation algorithm ($2 \to 2-o(1)$ took a decade; $2-o(1) \to 2.5-\epsilon$ took another).
- Watch triggers for the next rung: any paper pushing 2.5 toward 3 or beyond, any removal of
  the size-dependence in the estimation runtime, and any OR/AND-closure workaround for
  threshold circuits (equivalently: a Williams-style reduction needing only XOR-pairs).

## What to watch (falsifiable triggers)

1. Any paper titled or implying "NEXP not in TC0" or "super-polynomial THR o THR"; short of
   that, any improvement of the $n^{2.5-\epsilon}$ $\mathrm{THR} \circ \mathrm{THR}$ exponent ($2.5 \to 3 \to \cdots$) or of the
   estimation trade-off $2^{n - n^{\Omega(\epsilon)}}$ at larger sizes.
2. Quantified derandomization of TC^0 pushed from $n^{1+\exp(-d)}$ to $n^{1+O(1/d)}$ wires.
3. Any OR-closure result for $\mathrm{THR} \circ \mathrm{THR}$ (converting OR of circuits to one circuit of the class),
   or a Williams-style reduction needing only XOR-pairs throughout.
4. Any crossing of the magnification threshold: a fixed $\epsilon$ with $n^{-\epsilon}$-$\mathrm{MCSP}[\sigma]$ not in
   $\mathrm{PFML}[n^{2\epsilon}]$ for subexponential $\sigma$, or any explicit $\omega(n)$ B2-circuit lower bound.
5. k-SAT progress beyond $2^{n(1-1/O(k))}$ for growing $k$ (the Super-SETH regime where circuit
   consequences kick in).


## Screen (2026-10-03, frontiers monitor; full detail in `monitor_frontiers_2026-10-03.md`)

Verdict: NO trigger fired, NO named wall weakened.
- Chen-Tal-Wang $n^{2.5-\epsilon}$ $\mathrm{THR} \circ \mathrm{THR}$: formally published STOC 2026, zero citations, no
  successor exponent step. The wire-record line (Dev Nag, ECCC TR26-167, near-cubic wires
  for $\mathrm{SYM} \circ \mathrm{THR}$ / $\mathrm{THR} \circ \mathrm{THR}$, successor at $n^{7/2}$ wires) transfers to only $\sim n^2/\log$ gates
  (a wire bound is an $s(n+1)$ relaxation of the gate bound), so it does not approach the
  gate record: NEW CONTEXT, not a movement.
- Ren-Williams (ECCC TR26-118, FOCS 2026): $\mathrm{E}^{\mathrm{prMA}}/1$ requires $2^n/n$-size circuits,
  near-maximum via iterative win-win + Avoid-to-lower-bounds. NEW CONTEXT: largest-scale
  general-circuit bound for a strengthened class; no NP or $\mathrm{THR} \circ \mathrm{THR}$ consequence.
- Constructive gate elimination (Carmosino-Dang-Jackman, arXiv:2604.23958, 2602.17942):
  refuters extracted from Li-Yang-type $3.1n-o(n)$ bounds; the 45-year B2 stall intact but
  the constructivity currency the CJSW program needs now exists at the bottom rung.
- Hirahara-Ilango (FOCS 2025): conditional MCSP NP-hardness (NIWI/coNP/$\mathrm{P}^{\mathrm{NP}}$-poly
  assumptions); the magnification constructivization prerequisite (an UNCONDITIONAL
  MCSP-type lower bound) remains unmet.
- Toolbox: TR26-208 exponential correlation bounds for polynomials vs low-degree $F_2$
  polynomials (PRG seeds for the estimation engine). Negative screens: quantified
  derandomization of TC^0, OR-closure for $\mathrm{THR} \circ \mathrm{THR}$, k-SAT Super-SETH: all NO CHANGE.
