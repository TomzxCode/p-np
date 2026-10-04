# Failure-mode taxonomy of claimed P vs NP resolutions (2025-2026 corpus)

Added 2026-10-03. Derived entirely from this session's verified audits (see `clues.md`
section 4, `goertzel_audit.md`, and LOG.md). Purpose: a field guide that classifies each
claim by the structural reason it fails, so future claims can be triaged in minutes. The
taxonomy was distilled from the corpus, then applied back to it.

## The six failure modes

F1. Redefinition of the target. The author proves a statement about a nonstandard surrogate
    (restricted computation model, redefined class, "non-brute-force computation") while the
    title claims the standard problem. Detection: check what the main theorem quantifies
    over, before reading any proof.
F2. Circular subroutine. The algorithm's key step decides extensibility/consistency of
    partial objects, which is equivalent to the original problem. Detection: locate the one
    step where exponential search is avoided and ask what oracle it secretly uses.
F3. Reduction gap. A true-looking bridge between two theorems is asserted but the bridging
    reduction does not exist in the required direction or strength (e.g., decision-to-counting
    extraction, membership-vs-separation, subgraph-vs-induced-subgraph). Detection: state the
    bridge as a standalone reduction and check it against known equivalences.
F4. Trilemma violation (formalized this session, Proposition 1 in `goertzel_audit.md`):
    frameworks that simultaneously require success-domination, locality of the transformed
    algorithm, and a small-advantage bound for all local functions are inconsistent on any
    P = NP algorithm. Detection: identify the framework's three legs and check the inequality
    $\varepsilon \geq 1/2 - \delta$.
F5. Unproved characterization (half-bridge). A decision procedure needs a characterization
    proved in both directions; only one direction is proved and the other sits in a backup
    file, an axiom, or "ongoing work". Detection: enumerate which lemmas are axioms and which
    direction of each iff is proved.
F6. Formalization mismatch. A machine-checked artifact (Lean/Coq) verifies statements that
    are not the famous claim: the main theorem proves True, or assumes the bridge as axioms,
    or formalizes a bespoke predicate named after the claim. Detection: read the theorem
    statement and the axiom inventory first; "zero sorries" is about the chain, not the
    destination.
F7 (PROPOSED, 2026-10-03, first instantiation Edwards). Protean surrogate / definition
    drift. A load-bearing quantity has multiple inequivalent definitions and the
    separation chain requires a different one at each use site, so no single object
    satisfies both sides of the bridge. Detection: for each bridging lemma, pin down
    WHICH definition of the central object it uses and check the same pinning survives
    to the next use site. Borderline-foldable into F5 (the drift is a half-bridge's
    survival mechanism); kept separate pending a second instantiation. First case:
    Edwards arXiv:2512.11820, where the extraction map's output is the full sheet in
    Lemma 7/Theorem 223, the activated sheet in Lemma 205, and selector-wired in
    Lemma 206 - see `edwards_audit.md`.

## Instantiations on the 2025-2026 corpus (all audited this session)

- Arthanari, Lean 4 "P = NP" (arXiv:2606.03194, Jun 2026): F5 + F6. The M3P-in-P chain leans
  on a necessity direction left with 16 sorries in Backup; the P = NP chain imports Cook and
  Karp as axioms; repo issue #1 (one day after posting, 8 upvotes) shows the main theorem
  proves True. Community refutation within 24 hours.
- Goertzel, weakness-quantale "P != NP" (arXiv:2510.08814): F4, twice. (1) VV isolation to
  uniqueness needs $\Theta(n)$ hash rows (their Lemma 2.12) while the local normal form is
  granted $O(\log m)$ label bits (their Definition 2.10, Sections 3.1/3.6/7.4): the ensemble is
  not efficiently samplable in the stated regime. (2) Proposition 1: their Lemma 2.15
  ($\varepsilon \to 0$), Lemma 4.3 (exact domination) and the Theorem 4.2 locality conclusion are
  jointly inconsistent on the P = NP solver. See `goertzel_audit.md`.
- Topology paper "P = NP implies #P = FP" (arXiv:2603.22211): F3 + F4 shape. The advertised
  novel implication (row 5) needs the bridge "the P = NP decider computes a #P-hard
  function"; a satisfiability DECIDER computes a decision, and extracting #P-hardness from an
  NP decision oracle would require $\mathrm{\#P} \subseteq \mathrm{FP}^{\mathrm{NP}}$-type strength, which is neither known
  nor supplied. The exhaustive dichotomy (local-info useless / global invariant #P-hard) is a
  locality normal form with the middle option - computing the decision itself - left out;
  structurally, leg (2) of Proposition 1 is missing. (Analysis is abstract-level; the
  Theorems 45/47 dichotomy was not read in full.)
- Graph-based deterministic framework for NP (arXiv:2508.13166 / Zenodo v3-v7, Jan-Jul 2026):
  F2. "Local infeasibility trimming" of the computation graph must decide whether partial
  certificate-extensions reach an accepting certificate, which is the original NP problem;
  polynomial edge-count claims do not remove the need for that global decision. Version churn
  (7 versions in 6 months) with no community uptake.
- Xu-Zhou, P != NP (Frontiers of Computer Science 2025): F1. Diagonalizes over
  "non-brute-force computation", a nonstandard surrogate; multiple public flaw reports, no
  accepted defense; the journal appended expert comments rather than certifying the proof.
- Deng, P = NP via SDP for 3-coloring (2024): F3. Conflates subgraphs with induced subgraphs;
  the claimed D-graph lifting is false. (Refuted by others; verified structure matches.)
- Petros, self-referential CNF (SSRN 2025): F1-adjacent plus unsupported barrier-dodging:
  claims to defeat relativization, naturalization, and algebrization simultaneously; the
  construction is a diagonalization, which is exactly the technique the Baker-Gill-Solovay
  oracle worlds block; no community uptake.
- Trisduction/GOL certification (philarchive, 2026): not a proof by its own text
  (self-described non-deductive "epistemic warrant" from an LLM audit pipeline); included
  only to date the claim wave.
- Historical controls (pre-2025, for the base rate): Deolalikar 2010 (rejected in days),
  Blum 2017 (withdrawn), and a long tail of F1/F2 claims - the taxonomy's categories are
  stable across 15 years.

## Claim-wave screen b, 2026-10-03 (monitor pass 2; full details in `monitor_2026-10-03b.md`)

Six new items triaged (one-line failure-mode calls; none audited in depth yet):
- Edwards, arXiv:2512.11820 (v1 Nov 2025 - v5 Jan 2026, 208 pages): FULLY AUDITED (see
  `edwards_audit.md`): REFUTED. F1 + F5 confirmed, plus F4-shape (the paper's Lemmas
  204 + 224 + 124 are jointly inconsistent: its own instrumented solver must contain a
  sheet of rank $n^{\Theta(\log n)}$, falsifying its own universal P-side bound) and F3
  (switching-lemma restriction applied on one side only). F7 (protean surrogate) first
  instantiation: the extraction map's output changes identity across Lemma 7 / 205 / 206.
  P != NP via SPDP-rank / contextual-entanglement-width surrogates joined by a
  "rank-monotone extraction map"; formalization "future work" (honest, so F6 does not
  fire). Fairness: Theorems 94/128/236/280 are correct-looking rank bookkeeping on
  engineered encodings.
- arXiv:2604.07406 (Apr 2026): F1-adjacent. Claims the standard verifier definition of NP
  is unsatisfiable (a well-posedness attack, not a separation).
- "Six Birds" conditional P != NP (Zenodo 20713602, mirror of arXiv:2602.00134): F5 by its
  own text (conditional on one unproved axiom-level hypothesis).
- AASC "P = NP" (Zenodo, Jun 2026): F1 + F6, Lean appendix verifying a local spine, not
  the claim (the Arthanari pattern; rare P=NP direction).
- AETERNA/Prodromov GCT+entropy claim (Zenodo, Sep 2026): F3 (asserts exactly the GCT
  multiplicity obstructions whose construction is the open problem) + F1.
- "ZFC proof" (academia.edu, Jan 2026): F1 + Petros-pattern barrier-dodging
  (self-reference is what oracle worlds block); no uptake.
- Churn: McCallum arXiv:2005.10080 now at v15 (Feb 2026); Gao Ming arXiv:2203.05022 at v12
  (Aug 2026). Ramezanian arXiv:2609.10864 noted only (self-described non-resolution).
- New tripwire: pith.science maintains machine-review verdicts for P-vs-NP submissions
  (early-commentary signal alongside OpenAlex citation counts).
- Machine-assisted-proof ledger additions (frontiers screen, same day): ECCC TR26-167
  (Dev Nag, near-cubic wire bounds) carries an on-record board comment (Goldreich) judging
  the v1 text "entirely generated by LLMs without much human effort"; the author's v2
  re-attributes the core to Chen-Tal-Wang ("a change of accounting, not of architecture")
  and supplies a quote-conditional Lean derivation, not independent verification. The
  counter-datum: Kumar-Volk TR26-218 unconditionally prove the $\Omega(n^2)$ determinantal-
  complexity bound, explicitly superseding an AI-written claim of it. Net reading:
  machine fluency is not machine proof; verification ownership stays human.
- Companion paper flag: Edwards arXiv:2512.20729 (SPDP rank/codimension framework, no
  lower bound claimed) is the toolkit companion of arXiv:2512.11820 under audit.

## The one-line field guide

Before reading any proof: (1) quote the main theorem statement, (2) quote the axiom inventory,
(3) find the single step that avoids exponential search and ask what it assumes, (4) if a
framework transforms arbitrary algorithms into a normal form, check Proposition 1's inequality.
Every claim in the 2025-2026 corpus fails at least one of these checks, and the majority fail
at step (1).

## Base-rate note

Six independent claimed resolutions found in 2025-2026, zero surviving scrutiny (one refuted
here, one by its own repo within 24 hours, the rest pre-refuted or non-viable). The claim rate
itself is the strongest informal clue available: it shows the problem is accessible enough to
generate candidate arguments constantly, while every candidate dies at a structural checkpoint
the corpus above makes explicit.
