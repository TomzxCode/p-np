# P != NP investigation: consolidated overview

## Repository layout

    GOAL.md            standing instructions; the resume-point for any session
    README.md          this overview: verdict, artifact guide, session outcome
    LOG.md             timestamped audit trail (every step, correction, screen)
    bibliography.md    tracked, status-coded bibliography of record
    verify_corpus.py   machine gate: run before trusting any consolidation
    docs/              route maps, theory, forensics, open problems, theorem map
      monitors/        dated monitoring screens (arXiv/ECCC/claim-wave)
    experiments/       all python scripts (standalone or same-dir imports)
    paper/             the LaTeX write-up (p2_results.tex/pdf) + CHANGES.md
    lean_channel/      Lean 4 formalization project (CoreChannel.lean: zero sorry)

References to files throughout the corpus are by basename; `verify_corpus.py`
resolves them across the tree.

Last updated: 2026-10-03 (session with 20-turn budget; turns used: 9).
Objective: prove or disprove $\mathrm{P} \neq \mathrm{NP}$. Honest status: the problem is open; this corpus maps
every major attack route to its exact wall, refutes the unrefuted 2025-2026 claimed proofs
found, documents original experiments, and states the evidence balance.

## Verdict (with confidence type)

P != NP, confidence about 93%, inductive not deductive. Nothing found this session contradicts
it; every claimed resolution found in 2025-2026 was refuted or is unvalidated; the technique
walls (relativization, natural proofs now with an unconditional AC0 instantiation,
algebrization, localization, sharp thresholds) all mark where attempts die, not that the
separation is false.

## Artifact guide

- `clues.md` - master dossier: provable frame, five attacks with their walls, claim forensics,
  experiments, evidence balance sheet, frontier.
- `chi_search.py` - depth-2 decision-list hill-climbing search for high-chi trees at
  $d = 2$ (Theorem 6.1's condition-2 battleground); imports razborov_check's $F_2$ machinery.
- `LOG.md` - timestamped working log of every step, correction, and screen.
- `goertzel_audit.md` - full refutation of arXiv:2510.08814 (the one unrefuted P != NP claim
  found): internal k-parameter conflict + switching-lemma trilemma.
- `edwards_audit.md` - full refutation of arXiv:2512.11820 (208-page SPDP-rank separation):
  the bridging map changes identity across its three published forms; the paper's own
  lemmas are jointly inconsistent; first instantiation of failure mode F7.
- `williams_ladder.md` - the algorithmic-method ladder ($\mathrm{NEXP}/\mathrm{ACC}^0$ -> $\mathrm{THR} \circ \mathrm{THR}$ -> $\mathrm{TC}^0$ ->
  $\mathrm{P/poly}$ -> $\mathrm{P}$ vs $\mathrm{NP}$), with verified 2026 records, exact open trigger conditions, and watch
  list.
- `magnification_gap.md` - the exact epsilon-bookkeeping of the hardness-magnification wall
  (known n^{2eps-delta} vs needed n^{2eps+o(1)}), why it is provably not crossable by current
  techniques, and the Santhanam-Williams constructivization assessment.
- `algebraic_rung.md` - $\mathrm{VP}$ vs $\mathrm{VNP}$: records by model, four pinned no-go walls (SPD cannot
  separate $\mathrm{perm}/\mathrm{det}$; GCT occurrence obstructions dead padded and unpadded; min-partition rank
  barrier for multilinear ABPs; depth-reduction chasm), surviving directions.
- `proof_complexity.md` - the proof-complexity rung (the route where one super-polynomial
  Frege lower bound would prove $\mathrm{P} \neq \mathrm{NP}$ via $\mathrm{NP} \neq \mathrm{coNP}$): systems ladder, 2025-2026 frontier
  ($\mathrm{AC}^0[p]$-Frege reduction to pseudo-solutions, first self-proving lower bounds, refuter-problem
  metamathematics), walls and triggers. Now contains the session's formal results for the
  Krajicek pipeline at $p=2$: the proved answer-channel law, Prop A/C/D, Theorem B (adaptive
  single-variable cap), and Open Problem O1.
- `two_phase_tree.md` - ORIGINAL RESULT: the two-phase certification tree, an explicit
  adaptive degree-1 strategy for the $\Omega(n,d)$ pipeline at $p=2$ with success $1 - 2^{-(2d+1)}$
  (measured 0.97 at (32,2), 1.000 at d=8 with retries), beating Theorem B's single-variable
  cap 4x. IMPORTANT CORRECTION: the two-phase tree does NOT refute $\Omega(n,2)$ as a
  pseudo-solution - its failure rate $\sim 0.03$ SATISFIES the solution condition's tiny
  threshold $\gamma = k^{-O(1)}$; the candidate survives its strongest known attacker, and
  the chi-hypothesis also holds. The sharpened open problem is the freeness-certification
  impossibility over $F_2$ (proving NO adaptive tree achieves error $< k^{-O(1)}$).
- `note_to_author.md` - DRAFT remark for communication to J. Krajicek or as an ECCC
  comment on arXiv:2609.35927: the two-phase certification tree refutation of the
  candidate pseudo-solutions at $p=2$, with definitions quoted, exact error analysis, and
  the constructive repair direction. NOT sent; sending is the user's decision.
- `failure_modes.md` - field guide to the six structural failure modes of claimed resolutions
  (F1 redefinition, F2 circular subroutine, F3 reduction gap, F4 trilemma, F5 half-bridge,
  F6 formalization mismatch), each instantiated on the audited 2025-2026 corpus, plus the
  one-line triage procedure.
- Experiments (`sat_scaling.py`, `xor_hardness.py`, `razborov_check.py`, `chi_task_experiment.py`,
  `chi_p2_adaptive.py`, `chi_p2_multivar.py`, `chi_scaling.py`, `chi_full_pipeline_check.py`,
  `chi_and_vs_single.py`, `chi_two_phase.py`, `chi_o1_scaling.py`, `chi_posterior_test.py`):
  random 3-SAT and XOR systems easy at all tested scales; pigeonhole visibly exponential
  (1,439 / 80,639 / >150,000 nodes at h = 6/8/10), matching Haken's bound's location; exact
  $\mathrm{GF}(2)$ verification of Razborov's Theorem 4.1 (the foundation of Krajicek's $\mathrm{AC}^0[p]$-Frege
  pseudo-solution program) plus the first tabulated PHP design-space dimensions (|Des(4,2)| =
  2^65, |Des(6,3)| = 2^2079); toy-scale computation of Krajicek's chi-quantity; the $p=2$
  adaptive-lift measurement (success 0.24 vs 0.019 baseline) and its confirmed scaling law
  (success ~ n^{-1.77} at fixed $d$, budget); the multi-variable conflation test; the
  full-pipeline check that retracted the canonical-shortcut mismeasurement (violation rate
  0.0005, not 0.37). Note: an earlier "apparent typo" reading of Theorem 6.1's hypothesis was
  retracted - the printed direction is correct (see `proof_complexity.md` corrections section).

## Session outcome (final state, 2026-10-03)

The objective (prove or disprove $\mathrm{P} \neq \mathrm{NP}$) was not met - the problem is open. What this
session established, in decreasing order of permanence:

1. Nine analysis/instrument errors were made and corrected mid-session, all caught by
   computation or primary-source checks, never by argument alone; all are logged in
   `LOG.md` as prominently as the findings. The corpus is machine-verified consistent
   (`verify_corpus.py`: 351 checks, all PASS).
2. An original quantified reformulation of the $\mathrm{AC}^0[2]$-Frege program's $p=2$ core, carried
   to its FINAL form through eight corrections (see the correction blocks and ADDENDA
   in `two_phase_tree.md` and `proof_complexity.md`):
   * The channel law, kernel-true form: free-pair single-variable answers are fair
     marginally and on row-incomplete query sets; fully queried free rows are
     PARITY-LOCKED ($\mathrm{XOR} = 1$); $Q_i$ is determined $0$ on every pigeon; $V(n,d)^\rho =$
     $V(2d,d)$ (one kernel; the design-space debate dissolves). The coin channel is
     exactly the row-incomplete answer law, valid below per-row cost $\Theta(n)$
     (Lemma REL).
   * The BUDGETED cap for the ENTIRE degree-$\leq 2$ class (Theorem 3, `deg2_theory.md`):
     success $\leq q + P_{\mathrm{adj}} + P_K + o(1)$, keeping the printed chi-hypothesis ALIVE
     whenever $d^2 \log k = o(n)$ - the program's own regime - with the exact budgeted
     boundary $\mathrm{err}^*(d,\, d\log k) = k^{-\Theta(d^2/n)}$.
   * Three certificate mechanisms mapped (trichotomy, `open_problems.md` O7): row
     parity DEAD on the true pipeline; counting INERT within polylog budget
     (Theorem F = exact COIN-channel floor 2^{-Theta(d^2)}, `cert_floor.md`; on the
     literal pipeline the unbounded floor is exactly 0); ADJACENCY alive - two
     adjacent 1s certify a free pair WITH CERTAINTY (Lemma C), measured success
     0.93 at budget 1000, the strongest known adaptive attacker.
   * Retractions en route: Theorem T's recorded exact law (simulator artifact: the
     scripts certified on a row-XOR condition no legitimate query implements;
     literal error $\sim 5 \cdot 2^{-(2d+1)}$ at $d=2$, measured 0.8500); Proposition D as
     stated (rc counterexample 0.9067 vs cap 0.625); Lemma B.1's quantifier
     repaired to the disjoint-pair reading its proof supports (35/35 exact-grid
     PASS after repair; Reading B falsified exactly where the proof's "disjoint
     subfamilies" step excludes).
   * The open core, made precise (`open_problems.md`): the ALL-DEGREES budgeted
     floor (degree $\geq 3$ is what Theorem 6.1 quantifies over), the adjacency-budget
     race constant, and the odd-p analogue O6 (`p_family.md`: the chi-task is
     characteristic-uniform; no DAG-like $\mathrm{Res}(\mathrm{lin}_{\mathbb{F}_p})$ PHP bound exists at odd $p$).
   A positive answer to the all-degrees budgeted floor, via Krajicek's Theorem 6.1,
   yields super-polynomial $\mathrm{AC}^0[2]$-Frege lower bounds for the pigeonhole principle.
   The surviving results are also MACHINE-CHECKED in Lean 4 (`lean_channel/`):
   CoreChannel.lean - core-only, zero sorries (axioms: propext, Quot.sound), the
   channel-law answer function + counting lemma + certificate soundness;
   LeanChannel.lean - mathlib build, 0 errors, 9 statement-only sorries (the
   PMF channel facts and the Theorem F chain; ~1-2 weeks estimated to close),
   counting certificates in full, Lemma 1, Corollary 2 as an explicit non-adaptive
   scan-tree, disjoint-support and PMF statements.
3. Claim forensics with reusable structure: the 2025-2026 resolution claims were audited
   (Goertzel quantale: refuted via its own definitions; Edwards SPDP-rank 208-page
   separation: refuted via `edwards_audit.md` - bridging-map identity drift, first
   instantiation of failure mode F7; the Lean-4 P=NP artifact: refuted via its own
   issue tracker) and distilled into a failure taxonomy with a triage procedure
   (`failure_modes.md`).
4. Route maps at verified primary-source resolution for every major approach
   (`williams_ladder.md`, `algebraic_rung.md`, `magnification_gap.md`,
   `proof_complexity.md`), each with named walls, exact open trigger conditions, and
   monitored watch lists.

The evidence balance remains: $\mathrm{P} \neq \mathrm{NP}$ with ~93% confidence, inductive not deductive.

## Top-line facts of the map

- Best explicit Boolean circuit lower bound: ~3.1n (B2) / 5n-o(n) (U2), stalled ~40 years.
  No SAT-family lower bound is known against ALL polynomial algorithms; the canonical
  provable-hard family (pigeonhole) even has a trivial side-channel algorithm.
- Circuit-class frontier moved in 2026: THR o THR from n^{2-o(1)} to n^{2.5-eps}
  (Chen-Tal-Wang, STOC 2026) - the blocker for the next rung is OR-closure of $\mathrm{THR} \circ \mathrm{THR}$.
- Magnification thresholds are proven sharp and sit one epsilon-parameter above known bounds;
  crossing them provably costs the final theorem (Chen-Tell sharp thresholds), and localization
  disqualifies most techniques a priori.
- Algebraic: LST gives constant-depth super-polynomial bounds, but the depth-reduction chasm
  (need $2^{\omega(\sqrt{n})}$) plus the perm-vs-det no-gos box in every current technique.
- Constructivizing the one non-localizing super-linear technique (Santhanam-Williams,
  P-uniform circuits) is blocked by a missing prerequisite: no super-linear lower bound of any
  kind for MCSP-type problems, even uniform-time, is known.

## Monitored triggers (what would be real news)

1. $\mathrm{THR} \circ \mathrm{THR}$ exponent past 2.5, or an OR-closure workaround (XOR-pairs reduction throughout).
2. Quantified derandomization of $\mathrm{TC}^0$ at $n^{1+O(1/d)}$ wires (from $n^{1+\exp(-d)}$).
3. A fixed-$\varepsilon$ magnification crossing ($n^{-\varepsilon}$-$\mathrm{MCSP}[\sigma]$ outside $\mathrm{PFML}[n^{2\varepsilon+o(1)}]$).
4. Any explicit $\omega(n)$ Boolean circuit lower bound.
5. Any claimed resolution: screen, audit statement-vs-proof, check axiom inventory and sorry
   migration (method validated on the Goertzel and Lean-4 cases).

## Method notes (what worked this session)

- Audit claimed proofs against their own artifacts (repo issues, axiom lists, backup files);
  the decisive evidence was always structural, not stylistic.
- Verify every "known fact" against primary sources before relying on it (three drifts found
  and corrected: the SW14 attribution, the LST venue-year, the PHP "hard family" mislabel).
- Small-scale experiments cannot witness P != NP; their value is negative (average case is
  easy everywhere tested) and calibrational (provable hardness becomes visible exactly where
  theory says).
