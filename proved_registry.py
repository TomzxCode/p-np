#!/usr/bin/env python3
"""proved_registry.py - the machine-checkable PROVED registry for the corpus.

GOAL.md section 3 requires every PROVED label to trace to a written
line-by-line proof or a machine-checked statement of the same proposition,
and GUIDANCE item 5 records that the discipline should be enforced
mechanically. This module is that enforcement's data half: one tuple per
PROVED claim in docs/current_results.md section 2 (the single current
statement of the corpus), each naming the proof document, an anchor
substring that exists in that document, and the verification kind.

corpus_lint.py check 8 imports this module and verifies on every lint run:
  - every proof_anchor_substring is present (whitespace-normalized) in its
    proof document;
  - every claim has a corresponding line in docs/current_results.md
    (matched on claim_id, or on the claim statement's first 40 characters,
    whitespace-normalized);
  - the section-2 entry headers of docs/current_results.md are exactly the
    REQUIRED_CLAIMS mirror below, and each has a registry entry.

Maintenance rule (mirrors docs/current_results.md section 6): when a result
lands or dies, update docs/current_results.md, PROVED_CLAIMS, and
REQUIRED_CLAIMS in the same change, so the one current statement and this
registry stay in sync. The lint fails otherwise.

verification_kind is the LEAD kind named first in the entry's Label line in
docs/current_results.md; entries whose proof mixes kinds (written proof,
machine check, enumeration) record the lead kind and name the mix in the
short statement. A registry entry asserts that a proof EXISTS at the anchor;
it is bookkeeping, not mathematical validation (GOAL.md section 4).
"""

from __future__ import annotations

WRITTEN_PROOF = "written_proof"
MACHINE_CHECKED = "machine_checked"
ENUMERATED = "enumerated"

VERIFICATION_KINDS = (WRITTEN_PROOF, MACHINE_CHECKED, ENUMERATED)

# (claim_id, short_statement, proof_document, proof_anchor_substring,
#  verification_kind)
#
# proof_document resolves by basename in the corpus tree (all live in docs/).
# Each anchor was verified present in its document at registration time;
# corpus_lint.py check 8 re-verifies it on every run.
PROVED_CLAIMS: list[tuple[str, str, str, str, str]] = [
    (
        "CR-2.1",
        r"The channel law and its locks (kernel-true, every $p$) - determined"
        r" answers per query class, independence and uniformity windows, and"
        r" the four locks (channel_spec.md tables 5.1-5.3).",
        "channel_spec.md",
        "Determinism table (exact on every status configuration",
        MACHINE_CHECKED,
    ),
    (
        "CR-2.2",
        r"Theorem A (the matching hierarchy, all $d$) - every matching-$k$"
        r" column is design-varying and answers a fair coin at $p = 2$; no"
        r" matching column is ever determined.",
        "deg4_theory.md",
        "Theorem A (matching hierarchy)",
        WRITTEN_PROOF,
    ),
    (
        "CR-2.3",
        r"Lemma M (transcript-level transfer) and the fresh-bit identification"
        r" - the TV bound eps(e,n,d) with the improved constants, exact on"
        r" alias-aware block-free windows (supersedes deg2_theory.md Lemma"
        r" REL).",
        "lemma_m.md",
        r"Lemma M. Fix $(n,d)$",
        WRITTEN_PROOF,
    ),
    (
        "CR-2.4",
        r"Propositions A and C (the single-variable non-adaptive theory) -"
        r" fixed-label exactness and the non-adaptive single-variable cap.",
        "proof_complexity.md",
        "Formal statements: the provable p=2 cap",
        WRITTEN_PROOF,
    ),
    (
        "CR-2.5",
        r"Theorem B (the adaptive single-variable budgeted cap) - success at"
        r" most max(2d^2/(2d^2+n), f/2) + O(e/n) + o(1); coupling Lemma B.1"
        r" on the disjoint-pair quantifier, re-based on Lemmas D1 and D3.",
        "proof_complexity.md",
        "Theorem B (adaptive single-variable cap, PROVED)",
        WRITTEN_PROOF,
    ),
    (
        "CR-2.6",
        r"Theorem F (the exact coin-channel floor) and the true-pipeline"
        r" unbounded optimum - err* = 2^{-Theta(d^2)} on the stipulated coin"
        r" channel; success exactly 1 on the true pipeline at every p.",
        "cert_floor.md",
        "Theorem F (exact certification floor) - PROVED",
        WRITTEN_PROOF,
    ),
    (
        "CR-2.7",
        r"The certain-certificate inventory, with rates - adjacency, wedge, Z,"
        r" K_j column channel, self-certification (p > 2), counting, full"
        r" scan; mechanisms written-proved, rates MEASURED.",
        "deg2_theory.md",
        "Theorem 1 (adjacency certification",
        WRITTEN_PROOF,
    ),
    (
        "CR-2.8",
        r"Theorem 3 (the degree-2 budgeted cap; full printed class) - the"
        r" q_2* cap over arbitrary F_2 mixtures with the chi(e) certificate"
        r" form (ADDENDUM 9 correction; GAP D discharged, GAP B' closed).",
        "deg2_theory.md",
        "Theorem 3 (budgeted cap, true channel",
        WRITTEN_PROOF,
    ),
    (
        "CR-2.9",
        r"Theorem 3' (the degree-3 budgeted cap) - the q_3* cap with the same"
        r" d^2 log k = o(n) boundary as degree 2.",
        "deg3_theory.md",
        "Theorem 3' (budgeted cap, true channel",
        WRITTEN_PROOF,
    ),
    (
        "CR-2.10",
        r"Theorem 3'' (the degree-4 budgeted cap) - the q_4* cap; the boundary"
        r" is degree-independent through degree 4.",
        "deg4_theory.md",
        "Corollary 3.3 (chi-hypothesis at degree",
        WRITTEN_PROOF,
    ),
    (
        "CR-2.11",
        r"Theorems 4 and 4b (the $K_j$ witness) - the exact K_j-tree error and"
        r" the budgeted split witness (cap side corrected per ADDENDUM 9).",
        "deg2_theory.md",
        "Theorem 4b (budgeted form)",
        WRITTEN_PROOF,
    ),
    (
        "CR-2.12",
        r"The budgeted boundary $\mathrm{err}^*(d, d\log k) ="
        r" k^{-\Theta(d^2/n)}$ - two-sided at degrees 2, 3, 4 (p = 2) and at"
        r" degree <= 2 at every prime p; the transition sits at d^2 ~ n.",
        "deg2_theory.md",
        "The budgeted certification boundary at p = 2 (both directions)",
        WRITTEN_PROOF,
    ),
    (
        "CR-2.13",
        r"The GAP E bracket (the exact budgeted optimum, computed) - cap side"
        r" PROVED (written); witness side exact-in-family DP, MEASURED at"
        r" three (n,d,e) points.",
        "gap_e_constants.md",
        "Theorem E4 (the sharpened bracket)",
        WRITTEN_PROOF,
    ),
    (
        "CR-2.14",
        r"The odd-$p$ transfer (degree $\le 2$ at every characteristic) - the"
        r" 1/2 -> 1/p substitution rule, the exact err_K(p), and the odd-p"
        r" cap keeping the d^2 log k = o(n) boundary.",
        "odd_p_theory.md",
        r"The substitution rule (why every $p = 2$ form transfers)",
        WRITTEN_PROOF,
    ),
    (
        "CR-2.15",
        r"Theorem R (the err-form route; conditional) - no F_l(MOD_p)"
        r"-refutation with k steps given premise (A) = O2; written"
        r" conditional proof, premise open.",
        "err_form_route.md",
        "Theorem R (err-form route)",
        WRITTEN_PROOF,
    ),
    (
        "CR-2.16",
        r"Lemma CLS at general $d$ (the degree-2 relation inventory) - diagonal"
        r" variation via Theorem A plus the Q-A dimension identity by the"
        r" d-uniform degree-truncated Buchberger argument with master identities"
        r" M1-M5, I1; the general-d engine lemma (Lemma TB) is a named open"
        r" repair; unconditional at d <= 3.",
        "cls_cnt.md",
        "CLS(ii) core: the degree-2 slice of the relation space",
        WRITTEN_PROOF,
    ),
    (
        "CR-2.17",
        r"Lemma CNT (the completion count at general $d$) - the headline form"
        r" tight, the non-adaptive bound proved over the full five-family"
        r" inventory, the adaptive case closed in regime modulo B2 (Proposition"
        r" CNT-A).",
        "cls_cnt.md",
        "Proposition CNT-A",
        WRITTEN_PROOF,
    ),
    (
        "CR-2.18",
        r"Theorem 3 at general $d$ in regime (the degree-2 slice of O2,"
        r" upgraded) - the section 2.8 cap and certificate form at general d"
        r" with d^2 log k = o(n), modulo cor:coin base, B2, and L-CLASS"
        r" absorbed; the MIXTURE-d scope caveat stated in the regime line.",
        "all_degrees.md",
        "Theorem 3's step (6) is closed at general",
        WRITTEN_PROOF,
    ),
    (
        "CR-2.19",
        r"Theorem M3-D (MIXTURE-3; MIXTURE-d closed at $d \le 3$) - the full"
        r" printed degree-<=3 class covered with the constant repaired to"
        r" q3_mix (finite-n lift only) and the same aliveness condition.",
        "mixture3.md",
        "Theorem M3-D (repaired Theorem 3' over the FULL printed degree-",
        WRITTEN_PROOF,
    ),
    (
        "CR-2.20",
        r"Theorem 3''' (the degree-5 budgeted cap; assembly at the machine"
        r" points) - the q_5* cap with Proposition M5's general-k mass chain;"
        r" the general-d status is NOT upgraded (consumes INV(5)).",
        "deg5_theory.md",
        "Theorem 3''' (budgeted cap, true channel",
        WRITTEN_PROOF,
    ),
    (
        "CR-2.21",
        r"Theorem 3-gen (the all-degrees budgeted cap; conditional) and the"
        r" INV(d) premise - the all-degrees assembly proved at d = 2 and"
        r" INFERRED at general d: the premise INV(d) is open at every t >= 3"
        r" layer, the inv3 t=3/d=4 closure being downgraded engine output.",
        "all_degrees.md",
        "Theorem 3-gen (all-degrees budgeted cap)",
        WRITTEN_PROOF,
    ),
]

# (section number, entry title) mirroring the section-2 entry headers of
# docs/current_results.md one-for-one. corpus_lint.py check 8 parses those
# headers and requires exact set-and-title parity with this list.
REQUIRED_CLAIMS: list[tuple[str, str]] = [
    ("2.1", r"The channel law and its locks (kernel-true, every $p$)"),
    ("2.2", r"Theorem A (the matching hierarchy, all $d$)"),
    ("2.3", r"Lemma M (transcript-level transfer) and the fresh-bit identification"),
    ("2.4", r"Propositions A and C (the single-variable non-adaptive theory)"),
    ("2.5", r"Theorem B (the adaptive single-variable budgeted cap)"),
    ("2.6", r"Theorem F (the exact coin-channel floor) and the true-pipeline unbounded optimum"),
    ("2.7", r"The certain-certificate inventory, with rates"),
    ("2.8", r"Theorem 3 (the degree-2 budgeted cap; full printed class)"),
    ("2.9", r"Theorem 3' (the degree-3 budgeted cap)"),
    ("2.10", r"Theorem 3'' (the degree-4 budgeted cap)"),
    ("2.11", r"Theorems 4 and 4b (the $K_j$ witness)"),
    ("2.12", r"The budgeted boundary $\mathrm{err}^*(d, d\log k) = k^{-\Theta(d^2/n)}$"),
    ("2.13", r"The GAP E bracket (the exact budgeted optimum, computed)"),
    ("2.14", r"The odd-$p$ transfer (degree $\le 2$ at every characteristic)"),
    ("2.15", r"Theorem R (the err-form route; conditional)"),
    ("2.16", r"Lemma CLS at general $d$ (the degree-2 relation inventory)"),
    ("2.17", r"Lemma CNT (the completion count at general $d$)"),
    ("2.18", r"Theorem 3 at general $d$ in regime (the degree-2 slice of O2, upgraded)"),
    ("2.19", r"Theorem M3-D (MIXTURE-3; MIXTURE-d closed at $d \le 3$)"),
    ("2.20", r"Theorem 3''' (the degree-5 budgeted cap; assembly at the machine points)"),
    ("2.21", r"Theorem 3-gen (the all-degrees budgeted cap; conditional) and the INV(d) premise"),
]
