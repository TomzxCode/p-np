# The algebraic rung: VP vs VNP (verified 2026-10-03)

Companion to `clues.md` attack 3 and `williams_ladder.md`. All items checked against
primary sources surfaced this session (venue pages or arXiv).

## Why it matters for P vs NP

- Valiant: a super-polynomial lower bound for the permanent over general algebraic circuits
  gives $\mathrm{VP} \neq \mathrm{VNP}$, the algebraic shadow of P vs NP. Proving it is not known to imply
  $\mathrm{P} \neq \mathrm{NP}$, but it is the natural intermediate separation, and every depth-reduction result
  transfers the difficulty to bounded-depth models whose lower-bound technology is much
  better developed (and, per below, still short).
- Characteristic subtlety (a clue in itself): over GF(2), determinant equals permanent
  (signs vanish), so the flagship perm-vs-det formulation is vacuous in characteristic 2 -
  the Boolean-relevant case must be phrased via other polynomials (e.g., iterated matrix
  multiplication), and low-characteristic versions of the depth-4 lower bounds required
  separate work.

## Lower-bound record by model

- General arithmetic circuits, explicit polynomials: about $\Omega(N \log N)$ (Baur-Strassen
  lineage) - a decades-old record, the algebraic twin of the Boolean 3.1n stall.
- Monotone arithmetic circuits: exponential for explicit (clique-type) polynomials - again,
  monotone separations are provable while general ones are not.
- Homogeneous depth 3: exponential (Nisan-Wigderson 1995).
- Homogeneous depth 4: $n^{\Omega(\log\log n)}$ unrestricted (Kumar-Saraf, via bounded-support
  shifted partial derivatives + random restrictions); exponential under bounded bottom or
  top fan-in (Gupta-Kamath-Kayal-Saptharishi 2013; Kayal-Saha-Saptharishi 2013).
- Every constant depth (Limaye-Srinivasan-Tavenas, FOCS 2021; journal JACM 72(4), 2025):
  super-polynomial for an explicit polynomial (iterated matrix multiplication type); extended
  to fields of every characteristic (Forbes, 2024) - removing the earlier characteristic-0
  caveat. The one general-model crack of the past decade, still bounded depth.
- Symmetric algebraic circuits: the permanent provably has no polynomial-size symmetric
  circuits while the determinant does (Dawar-Wilsenach, ICALP 2020); extended to a full
  symmetric theory in 2026: symVF strictly inside symVS strictly inside symVP, unconditional
  (Dwivedi-Pago-Seppelt, STOC 2026, via homomorphism-polynomial characterizations and
  model-theoretic homomorphism indistinguishability). A complete separated universe - under a
  symmetry restriction that general circuits do not obey.

## The walls (no-go results, each verified this session)

1. The shifted-partial-derivative method - the technique behind all depth-4 records - cannot
   separate the permanent from the determinant: for the padded permanent against the GL-orbit
   closure of the determinant with $n > 2m^2 + 2m$, the SPD ranks of degenerations of $\mathrm{det}_n$
   always dominate (arXiv:1609.02103, four case analyses using Macaulay's theorem on ideal
   growth). The best lower-bound technology is provably insufficient for the flagship question.
2. GCT occurrence obstructions are impossible in the padded det-vs-perm orbit-closure setting:
   Ikenmeyer-Panova (FOCS 2016) killed the Kronecker-coefficient route; Buedguesser-Ikenmeyer-
   Panova (JAMS 2019, "No occurrence obstructions in geometric complexity theory") killed the
   full occurrence-obstruction strategy - every representation occurring in the padded
   permanent's coordinate ring also occurs in the determinant's (and the proof used only
   padding, not the permanent).
3. The padding dilemma: padding is what makes the stabilizers reductive (GCT needs it), but
   all no-go results exploit padding. Removing padding via the homogeneous reformulation
   (determinant replaced by the trace of a variable matrix power, after Nisan 1991) changes
   the representation theory so much that occurrence obstructions cannot prove even
   superlinear lower bounds in that model (third no-go). The original GCT obstruction plan is
   squeezed between two impossibility results that trade on the same variable.
4. Depth-reduction chasm: Tavenas' depth reduction ($2^{O(\sqrt{d \log d \log(ns)})}$) means
   constant-depth lower bounds below $2^{\omega(\sqrt{n})}$ can never yield $\mathrm{VP} \neq \mathrm{VNP}$. The
   depth-4 record for permanent-type polynomials is $2^{\Omega(\sqrt{n})}$ in top-fan-in-type
   measures - sitting exactly at the chasm, with wall 1 forbidding the crossing by SPD tools.
4b. Multilinear ABP barrier (Kush, ECCC TR26-043, April 2026): the min-partition rank method -
    the only technique behind known multilinear lower bounds - provably cannot prove
    superpolynomial lower bounds against multilinear algebraic branching programs: there
    exists a full-rank multilinear polynomial computable by a polynomial-size mABP. This
    resolves the Fabris-Limaye-Srinivasan-Yehudayoff question on 1-balanced-chain set systems
    ($N(n) = n^{O(1)}$) and adds a fourth named technique-wall in the algebraic world, matching
    the SPD and GCT no-gos above.
5. Algebraic natural proofs (Forbes-Shpilka-Tenger; Grochow): proof systems whose separating
   objects lie in VNP cannot prove lower bounds under standard crypto assumptions - the
   algebraic twin of Razborov-Rudich, restricting the meta-language of candidate proofs.

## Surviving directions (activity 2025-2026, verified)

- Multiplicity obstructions: the surviving GCT tool (occurrence = multiplicity $> 0$ vs
  multiplicity comparison). Ikenmeyer-Kandasamy (STOC 2020) implemented the first separation
  via symmetries of both polynomials; the 2025 product-plus-power work (Journal of Symbolic
  Computation 2025) extends it with an explicit infinite family of multiplicity obstructions
  and deborders Kumar's model. Still far from det-vs-perm.
- Debordering: active survey-level program (October 2025); central open question $\overline{\mathrm{VP}} = \mathrm{VP}$
  (is VP closed under approximation?), with major consequences in either resolution.
- Algorithmic invariant theory: orbit-closure intersection in randomized polynomial time for
  tensor actions with constant third factor (CCC 2026, via polynomial degree bounds and
  succinct invariant encodings); counterweights: exponential lower bounds on generator degrees
  for the full 3-tensor action (9 copies) and exponentially small weight margins
  (Franks-Reichenbach) breaking optimization-based null-cone algorithms.
- Symmetric theory: the 2026 STOC work above; lesson - symmetry is what makes lower bounds
  provable, and general circuits defeat every invariant-based method so far.

## Verdict for the dossier

The algebraic route is alive but fully mapped at the walls: the general-model record is
logarithmic ($\Omega(N \log N)$), the bounded-depth breakthrough (LST) cannot reach VP vs VNP
through the depth-reduction chasm, the flagship technique (SPD) is provably insufficient for
perm-vs-det, and GCT's original obstruction plans are no-go'd from two directions. What
remains genuinely open: multiplicity obstructions beyond toy separations, debordering, and
any technique that is neither SPD nor occurrence-based. The Boolean lesson stands: symmetry
and monotonicity enable separations; their absence is the entire difficulty.

## arXiv sweep additions (this session, 2025-2026, verified to abstract level)

- Debordering: "Debordering Closure Results in Determinantal and Pfaffian Ideals"
  (arXiv:2511.16492, Nov 2025) extends the Andrews-Forbes STOC 2022 determinantal-ideal
  program - the constructive-invariant-theory side of debordering keeps moving.
- GCT applied beyond det-vs-perm: "Geometric Complexity Theory and Graph Isomorphism"
  (arXiv:2606.26244, June 2026) uses GCT ideas as a playground for separating graph
 .property orbit closures - consistent with the map: GCT techniques live in restricted,
  symmetry-rich settings.
- Completeness/hardness landscape: "Planar Perfect Matching Counting is as Hard as
  Determinants" (arXiv:2606.03975, June 2026) extends the Valiant/holant completeness picture
  (planar PM counting is determinantal-complexity complete).
- Restricted-model lower bounds: "Tropical Circuits with Scalar Multiplication Gates"
  (arXiv:2607.11540, July 2026) - exponential lower bounds for max-+-scalar circuits on
  spanning trees and bipartite matchings; "A Lower Bound for Read-Once Parity Branching
  Programs" (arXiv:2607.05944, July 2026) - $\widetilde{\Omega}(n^2)$, improved from $n^{1.5}$, via
  reduction to algebraic circuits. Monotone/tropical separations continue to be provable;
  general ones do not.
- Upper-bound progress: GCD in constant depth over any characteristic (arXiv:2506.23220,
  2025, extending Andrews-Wigderson); deterministic subexponential factorization of
  constant-depth algebraic circuits (arXiv:2504.08063); the $3 \times 3$ matrix multiplication record
  dropped to 22 multiplications over the integers (arXiv:2610.01639, Oct 2026) - base-case
  progress relevant to exponent targets.
- roABP structure: non-closure under factoring (arXiv:2509.10725, Sept 2025).
- Technique barrier addition (recorded in the walls section as 4b): Kush's min-partition-rank
  barrier (ECCC TR26-043). Related MCSP-adjacent hardness landscape updates: partial MBPSP is
  ETH-hard (arXiv:2407.04632), MCSP* XOR-extension tractability (arXiv:2511.16903), explicit
  truth-table-perturbation circuit-size bound (arXiv:2603.09379), and SoS degree lower bounds
  for MCSP (arXiv:2311.12994: degree $\Omega(s^{1-\epsilon})$ to prove no size-s circuits exist).


## Screen (2026-10-03, frontiers monitor; full detail in `monitor_frontiers_2026-10-03.md`)

Verdict: every named algebraic wall stands (SPD no-go, GCT no-gos, padding dilemma,
depth-reduction chasm, Kush mABP barrier, algebraic natural proofs). Movement was
restricted-model records and implication arrows:
- Kumar-Volk (ECCC TR26-218): power-sum determinantal complexity $\Omega(n^2)$ over $\mathbb{C}$,
  unconditional, explicitly superseding Sheshadri's AI-written claim of the same bound.
  First human-verified superlinear dc bound for an explicit family; a machine-assisted-
  proof ledger datum (human proof retiring an AI proof).
- Raz (FOCS 2026): $\Omega(n^{1.5})$ product gates, non-commutative circuits (degree $n$).
  Narayanan (arXiv:2607.15848 / TR26-138): sumset-expansion elusive functions, resolving
  the GMO open problem, quadratically improving Raz's depth-record. Both restricted-model;
  VP vs VNP untouched.
- Implication arrows: Burgisser (arXiv:2606.25121) BSM intractability $\Rightarrow \mathrm{VP}^0 \neq \mathrm{VNP}^0$;
  Rossman-Zhu (arXiv:2512.01227) SoS lower bounds $\Rightarrow \mathrm{VNC}^1 \neq \mathrm{VNP}$ (conditional targets).
  Orzel et al. (arXiv:2502.02442): the "cost of a Boolean sum" property separates $\mathrm{perm}$
  from $\mathrm{det}$ (sharpens why VNP-completeness fails for $\mathrm{det}$). Forbes (FOCS 2026): exponential
  depth-3 bounds in small characteristic (closes a recorded low-characteristic caveat).
- GCT: no occurrence obstructions constructed, no new det-vs-perm rank bounds; only
  Grochow-Urisman v2 (cycle-index multiplicity characterization) and plethysm-in-#BQP.
  Consistent with the map: GCT lives in symmetry-rich restricted settings.
- Flag for the claim-wave ledger: Edwards arXiv:2512.20729 (SPDP rank/codimension toolkit,
  no lower bound) is the companion of arXiv:2512.11820 under audit; the ELSW SPD no-go is
  not engaged.
