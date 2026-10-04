# Bibliography of record (tracked 2026-10-04)

Every reference the corpus engages, with verification status. Status codes:
[V] = verified against the primary source this session (fetch or API record);
[L] = recorded from the literature/monitoring, not independently opened;
[R] = refuted by this corpus's audit; [I] = internal (this session's own
deliverables). Each entry lists where it is used in the corpus. Corrections to
this file should update the `correct-as-of` date per entry.

## 1. The engaged program

- [V] J. Krajicek, "Pseudo-solutions of polynomial systems and the lower bound
  problem for AC0[p]-Frege systems", arXiv:2609.35927 (v1 Sep 2026; v2 30 Sep 2026,
  spelling-only). THE engaged paper: Def 3.1, Def 4.3, Lemmas 4.4/5.1/5.2, Thms
  2.2/3.2/3.3, 6.1; the chi-task. Note (chi_transfer.md): printed Theorem 6.1(3) is
  false as printed; the err-form route is the live replacement. Used in:
  proof_complexity.md, two_phase_tree.md, chi_transfer.md, note_to_author.md,
  paper/. correct-as-of: 2026-10-04.
- [L] J. Krajicek, Proc. AMS (2024) - the predecessor; Problem 4.4; Defs 3.1/3.2
  quoted as printed in 2609.35927. Used in: proof_complexity.md, chi_transfer.md.
- [V] T. Braun, "Lower bounds for bit pigeonhole principles in unrestricted
  resolution over parities", arXiv:2609.23015 (v1 19 Sep 2026; Lean 4-formalized;
  AI-assisted development). The unrestricted Res(+o+) BPHP bound; zero citations
  as of 2026-10-04; first in-text follow-up is Pang (below). Used in:
  proof_complexity.md, williams_ladder.md context. correct-as-of: 2026-10-04.
- [V] arXiv:2610.00837 (Pang), "A Degree-Size Relation for Resolution over
  Polynomials" - credits Braun's "common-multiplier idea"; first in-text Braun
  follow-up. Used in: proof_complexity.md (algebraic proof systems).

## 2. This session's original deliverables [I]

- proof_complexity.md (+ ADDENDA 1-4), two_phase_tree.md (MAJOR CORRECTION),
  cert_floor.md (Theorem F, Lemmas 1-5), deg2_theory.md (Theorems 1-5, Lemma REL,
  Sec 8), deg3_theory.md (pending agent), and_chain.md (Lemma C),
  kernel_structure.md (V(n,d)^rho = V(2d,d); parity-locking), thmB_stress.md
  (Lemma B.1 repair), chi_transfer.md (printed-(3) falsification; err-form route),
  chi_and_chain.py, chi_deg2_theory_check.py, chi_two_phase*.py, razborov_check.py,
  kernel_structure.py, verify_corpus.py, theorem_map.md, open_problems.md,
  goertzel_audit.md, edwards_audit.md, failure_modes.md, p_family.md, paper/
  (p2_results.tex/pdf, FINAL). All ASCII math; every number run-backed.

## 3. Claim-wave items audited or triaged

- [R] B. Goertzel, quantale "P != NP", arXiv:2510.08814 (v1 9 Oct 2025; v2
  22 Apr 2026, title softened to "route"). REFUTED: internal k-parameter conflict +
  switching trilemma (goertzel_audit.md); pith.science machine-review REJECT
  converges (note: its author rebuttal is machine-simulated; Goertzel silent).
  correct-as-of: 2026-10-04.
- [R] D.J. Edwards, "Observer-Theoretic Separation via SPDP Rank...", arXiv:2512.11820
  (v1 30 Nov 2025 - v5 8 Jan 2026, 208 pp). REFUTED: bridging-map identity drift
  (F7), self-refutation (Lemmas 204+224+124), quantitative collapse
  (edwards_audit.md). Companion toolkit: arXiv:2512.20729 (no bound claimed).
- [L] Arthanari, Lean-4 "P = NP" via pedigree polytope, arXiv:2606.03194 - traced
  to `proves True` via the repo's tracker. Used in: failure_modes.md.
- [L] McCallum, "PA proves P != NP", arXiv:2005.10080 (v15, 12 Feb 2026; 15
  versions/6 yr). [L] Gao Ming, arXiv:2203.05022 (v12, 5 Aug 2026). [L]
  arXiv:2604.07406 (NP-definition-defect). [L] arXiv:2602.00134 / Zenodo 20713602
  (Six Birds, conditional). [L] AASC P=NP Zenodo (Jun 2026, Lean-spine). [L]
  AETERNA/Prodromov GCT+entropy (Sep 2026). [L] academia.edu "ZFC proof" (Jan
  2026). [L] Ramezanian, arXiv:2609.10864 (self-described non-resolution). All in:
  failure_modes.md, monitor_2026-10-03b.md.

## 4. Proof-complexity frontier (the Res(+o+)/AC0[p] lane)

- [V] ECCC TR26-007 (2 Jan 2026) Alekseev-Gaevoy, "New Polynomial-Depth Res(+o+)
  Lower Bounds" (CBPHP). [V] ECCC TR26-018 (12 Feb 2026) Itsykson-Podolskii-
  Shekhovtsov, "Resolution Width Lifts to Near-Quadratic-Depth Res(+o+) Size".
- [V] arXiv:2511.20023 / TR25-118 (25 Nov 2025) Byramji-Impagliazzo, bounded-depth
  Res(+o+) BPHP bounds - Braun's direct predecessor.
- [V] ECCC TR26-055 Davis-Robere, Res(log) self-proving lower bounds.
- [V] arXiv:2609.23228 / TR26-196 Li-Ren-Zhong, demi-bits generator.
- [L] arXiv:2509.16824 Lu-Santhanam-Tzameret, AC0[p]-Frege DNF lower bound (ITCS
  2026). [L] arXiv:2608.08760 Weak Rank Principle. [L] TR26-078 tree-like semantic
  bounded-line-size. [L] TR26-225/TR26-226 (3-4 Oct 2026; out of lane, screened).
- Classics [L]: Haken 1985 (resolution PHP); Ajtai 1994; Beame et al. 1996
  (AC0-Frege PHP); Segerlind-Buss-Impagliazzo (Res(k)); Itsykson-Sokolov 2017
  (Res(lin_2)); Part-Tzameret (tree-like Res(lin_Fp), all characteristics);
  Khaniki (ToCL 2022; odd-p fragments); Garlik-Kolodziejczyk 2018 (PK_d^c(+)
  separation); Maciel-Nguyen-Pitassi 2013; Krajicek 1997 (PK_d^c(+)); Ben-Sasson-
  Wigderson 2001 (width-size). Used in: proof_complexity.md, p_family.md.

## 5. Algorithmic lower bounds and magnification

- [V] ECCC TR26-039 / STOC 2026 Chen-Tal-Wang, THR o THR n^{2.5-eps} (the ladder
  anchor; zero citations as of 2026-10-03). [V] ECCC TR26-167 Dev Nag, near-cubic
  WIRE bounds (LLM-authorship episode: Goldreich on record; quote-conditional Lean).
- [V] ECCC TR26-118 / FOCS 2026 Ren-Williams, 2^n/n for E^{prMA}/1. [L] FOCS 2025
  Hirahara-Ilango, conditional MCSP NP-hardness. [V] arXiv:2604.23958 +
  arXiv:2602.17942 Carmosino-Dang-Jackman, constructive gate elimination. [V]
  arXiv:2609.38677 / TR26-221 Korten, top-down lower bounds (human-machine
  collaboration). [V] ECCC TR26-208 exponential correlation bounds (toolbox).
- [V] arXiv:2503.24061 Atserias-Muller, general magnification (sharp wall; zero
  citations). [V] arXiv:2604.25251 Atserias-Muller, Godel incompleteness to
  consistency. [L] TR25-045 Carmosino-Grosser (VAPC vs V1); TR26-043 Kush
  min-partition barrier; TR26-176 Carmosino-Juvekar. Used in: williams_ladder.md,
  magnification_gap.md.

## 6. Algebraic complexity

- [V] ECCC TR26-218 Kumar-Volk, Omega(n^2) determinantal complexity (supersedes an
  AI-written claim). [L] arXiv:2604.22006 / FOCS 2026 Raz, non-commutative
  n^{1.5}. [V] arXiv:2607.15848 / TR26-138 Narayanan, sumset-expansion elusive
  functions (resolves GMO). [L] arXiv:2606.25121 Burgisser (BSM => VP != VNP);
  arXiv:2512.01227 Rossman-Zhu (SoS => VNC^1 != VNP); arXiv:2502.02442 Orzel et al.
  (cost of a Boolean sum); FOCS 2026 Forbes (depth-3 small characteristic);
  arXiv:1609.02103 ELSW SPD no-go. Used in: algebraic_rung.md.

## 7. Methodological classics cited in the proofs

- [L] Joag-Dev and Proschan (1983), Annals of Statistics 11(1):286-295 - negative
  association. Used in: proof_complexity.md (Lemma B.1), paper/.
- [L] Dubhashi and Ranjan (1998), Random Structures and Algorithms 13(2):99-124 -
  negative association (venue corrected from an earlier note's "Algorithmica").
  Used in: proof_complexity.md, paper/.
- [L] Cook-Reckhow (1979) - proof-system polynomial boundedness iff NP = coNP.
  [L] Baker-Gill-Solovay (1975) - relativization. [L] Razborov-Rudich (1997) -
  natural proofs. [L] Aaronson-Wigderson (2008) - algebrization. [L] Tardos
  (1988) - strongly polynomial LP (cited inside the corpus's M3P notes). Used in:
  clues.md, paper/, failure_modes.md.

## Maintenance rule

New references enter via monitoring deliverables (monitor_*.md) and are promoted
here when the corpus engages them substantively (audited, proved-against, or
load-bearing in a proof). Every promotion carries a status code and a
correct-as-of date; corrections update the entry in place and note the change in
LOG.md.
