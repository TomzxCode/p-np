# Kernel-level fidelity check of the Omega(n,d) answer channel at p = 2
# (printed OUTER reading of Definition 4.3, arXiv:2609.35927)

Verification-agent report, 2026-10-03. Script: `kernel_structure.py` (standalone; imports
`razborov_check.py` for the corpus's gf2 machinery). Points: outer (n,d) in
{(7,1), (15,2), (31,3)}, restricted systems (2d,d) = {(2,1), (4,2), (6,3)}.
Sample sizes: 100,000 uniform design samples per tested law per point (plus exact
enumeration at (2,1) and full-kernel 2,000-sample cross-checks at (2,1)/(4,2)).
Fixed seeds; the run reproduces digit-for-digit.

This is the re-dispatch with the UPDATED brief: the corpus adopted the PRINTED OUTER
reading of Definition 4.3 ("L vanishing on V(n,d)^rho as printed",
proof_complexity.md "Design-space readings"; paper/p2_results.tex def:pipeline), and the
task is the kernel-level check under that reading, plus the key question of whether the
coin-channel simulators sample a strict superset of the legal designs. It supersedes the
earlier canonical-reading pass, whose kernel findings this check confirms and relocates:
they were never artifacts of the canonical reading, because (Finding 1) there is only one
kernel.

## 1. What was reconstructed (constraints imposed, and why)

The pipeline (proof_complexity.md, quoting Def 4.3): rho is a partial injection leaving
exactly n_rho = 2d free holes (2d+1 free pigeons D, 2d free holes R); L is a degree-d
design (linear, L(1) = 1, "vanishing on V(n,d)^rho") of the restricted system; the answer
to a query g is omega(g) = L(g^rho). The corpus's paper (def:pipeline, items 2-3, the
adopted outer reading) specifies V(n,d)^rho as "span of the restrictions of the outer
degree-<=d consequences" and g^rho as the substitution x_ij -> 1 if rho(i) = j, -> 0 if i
is assigned and j != rho(i), x_ij untouched on D x R.

Constraint set imposed by `kernel_structure.py`:

  (i)  L kills every restriction (g.h)^rho, where h runs over the outer system -PHP_n
       (razborov_check.system_polys), g runs over outer monomials with
       deg(g.h) <= d, and restriction is applied term-by-term;
  (ii) L(e_0) = 1 for designs; kernel vectors are the homogeneous variant L(e_0) = 0.

Two reading gaps had to be closed before (i) is well defined, and both resolutions are
forced by the corpus's own commitments (documented in the script docstring):

- The printed g^rho clause does not cover the pair (free pigeon, matched hole). Any
  completion leaving those variables symbolic would make killed-unmatched answers
  undetermined design values, contradicting the corpus's channel law
  ("killed-unmatched -> 0 determined": cert_floor.md Lemma 3 proof, chi_p2_adaptive.py,
  chi_two_phase.py). The zeroing completion is therefore the only one consistent with the
  corpus; it is imposed.

- rho is fixed to the canonical restriction (pigeon i -> hole i for i < n - 2d, 0-based;
  the "canonical Z" of cert_floor.md). All rho with the same free sizes give isomorphic
  systems, and the answer channel factors through the isomorphism class.

Generator rows for V(n,d)^rho are built THROUGH THE OUTER ROUTE only (outer polynomials,
outer shifts, then restriction - with the row set collapsed over distinct restrictions
and distinct images, exact because (h.g)^rho = h^rho . g^rho), never by copying the
canonical construction. The canonical list (razborov_check-style at (2d,d)) is built
independently and the two spans are compared by rank plus containment in both directions.

## 2. Finding 1 (script F1, structural): V(n,d)^rho = V(2d,d). The two readings coincide

Measured at all three points (exact gf2 elimination; "containment" = every generator of
one list reduces to 0 against the other list's echelon, both ways):

| outer (n,d) | restricted (2d,d) | rows (outer route) | rank V(n,d)^rho | rank V(2d,d) | containment | dim S | dim Des | corpus table      |
|-------------|-------------------|--------------------|-----------------|--------------|-------------|-------|---------|-------------------|
| (7,1)       | (2,1)             | 3                  | 3               | 3            | both ways   | 7     | 3       | - (formula value) |
| (15,2)      | (4,2)             | 195                | 165             | 165          | both ways   | 231   | 65      | 165 / 65 MATCH    |
| (31,3)      | (6,3)             | 18361              | 12110           | 12110        | both ways   | 14190 | 2079    | 12110 / 2079 MATCH |

Reason (verified term-by-term in the construction): every restricted outer generator is a
canonical generator shift or 0 - an assigned pigeon's Q_i restricts to the ZERO
polynomial (1 + 1 = 0), and killed Booleans, collisions, and two-hole monomials restrict
to 0 - and deg(h^rho) = deg(h) whenever h^rho != 0, so the shift ranges coincide exactly.

CONSEQUENCE. The design-space debate (proof_complexity.md correction block, "Design-space
readings"; two_phase_tree.md correction item (e)) DISSOLVES at kernel level: there is no
kernel-level difference between "L vanishing on V(n,d)^rho" and "L in canonical
Des(2d,d)". The corpus's adoption of the outer reading is answer-channel-neutral: the
operative constraint is the printed vanishing condition itself, and under it the free
rows carry a FORCED parity (next section). Note this also resolves the writeup agent's
"reversed tree wins with probability 1" scare in the corpus's own favor: under the
zeroing semantics, Q_i^rho = 0 for ASSIGNED pigeons too (the paper's rigidity
proposition (a) computes Q_i^rho = Q^c + 1 only by treating assigned-row variables as
symbolic, which the zeroing semantics excludes), so no reading of the printed definition
produces a reversed certificate; row queries simply carry no information
(proof_complexity.md ADDENDUM finding 3, "no trivial win", confirmed at kernel level).

## 3. Finding 2 (script F2/F3): the exact answer law under the printed reading

Degree-1 column classification (pivot = answer design-determined; every degree-1 column
classified; the augmentation row pins e_0):

| restricted | degree-1 columns | pivot | free     | parity pivots                       |
|------------|------------------|-------|----------|-------------------------------------|
| (2,1)      | 6                | 3     | 3 = 3x1  | one per free row, at its last hole  |
| (4,2)      | 20               | 5     | 15 = 5x3 | one per free row, at its last hole  |
| (6,3)      | 42               | 7     | 35 = 7x5 | one per free row, at its last hole  |

Each pivot single is parity-determined: L(x_rowpivot) = 1 + XOR(the other 2d-1 design
values of its row); kernel vectors carry EVEN row parities; designs carry ODD row
parities (rigidity). Empirical laws (100,000 uniform design samples each; PASS = |z| < 4):

| test                                                    | (2,1)      | (4,2)       | (6,3)       |
|---------------------------------------------------------|------------|-------------|-------------|
| C1 L(1) = 1                                             | 100000/100000 | 100000/100000 | 100000/100000 |
| C2 marginal fairness, free pairs (max chi2 z)           | 0.74       | 1.87        | 1.79        |
| C3 pairwise independence, window pairs (max z)          | 0.88       | 1.38        | 1.22        |
| C4 joint i.i.d., row-incomplete window (z over 2^k pats)| -0.38      | -2.01       | -0.18       |
| C5 FULL free row: P(row XOR = 1)                        | 1.0000     | 1.0000      | 1.0000      |
| C5 patterns occurring on a full free row                | 2 of 4     | 8 of 16     | 32 of 64    |
| C6 P(Q_i = 1), free pigeons (coin channel claims 1/2)   | 0.0000     | 0.0000      | 0.0000      |
| C6 P(Q_i = 1), killed pigeons                           | 0 (structural) | 0       | 0           |

Plus: matched -> 1 and killed-unmatched -> 0 hold by the restriction semantics (x^rho in
{0,1}, L(1) = 1); F_2-linearity holds by construction (Lemma 1 of cert_floor.md); at
(2,1) the full design space was enumerated (8/8 designs: all free-row parities = 1) and
at (2,1)/(4,2) a 2,000-sample full-kernel check reproduced the projected law with 0
violations; the projected sampling basis was verified against the full kernel basis by
span equality on every tested coordinate set.

Verdict on the channel law, exact form:

- free pairs: marginally fair ALWAYS, and jointly i.i.d. fair on any query set that
  misses at least one cell of each free row (the completion structure,
  p2_results.tex lem:completion / cor:coin);
- a FULLY queried free row is locked to parity 1: only 2^(2d-1) of the 2^(2d) answer
  patterns occur, XOR = 1 in 100,000/100,000 samples (the coin channel predicts 1/2);
- the row-sum certificate Q_i = 1 + XOR(row answers) is DETERMINED 0 on every pigeon,
  free ones included: L kills Q_i^rho in V(n,d)^rho, since Q_i is an outer generator.
  The parity-certificate basis of the two-phase tree is therefore refuted at kernel
  level. This upgrades proof_complexity.md ADDENDUM finding 3 (measured 0/2000) to a
  theorem-level statement and matches p2_results.tex prop:rigidity (b).

So the brief's context sentence is exact with one qualification: single-variable answers
are i.i.d. fair coins on free pairs ON ROW-INCOMPLETE QUERY SETS; the qualified law is
precisely cor:coin's statement with its E_full event.

## 4. Finding 3 (script F4): the disjoint-support lemma

- (2,1): TRUE. The RREF kernel basis (one vector per free column) has pairwise-disjoint
  single-variable supports: each free single carries {itself, its row's parity pivot},
  and rows are disjoint.
- (4,2), (6,3): FALSE for the RREF basis: the (2d-1) free singles of one row all carry
  the row's parity pivot (15 overlapping pairs at (4,2)).
- Stronger: at d >= 2 NO basis of the kernel (nor of its single-variable projection,
  which is the even-parity subspace) can have pairwise-disjoint single-variable supports:
  within a row of 2d coordinates, 2d-1 even-weight disjointly supported vectors need
  total weight >= 2(2d-1) > 2d.
- The channel-law conclusion does not need the lemma: it rests on completion (Section 3,
  C4), which holds at every d. The note_to_author.md phrase "back-substitution
  corrections touch pivot columns only" is correct but insufficient for disjointness -
  pivot columns include the parity pivots, which are single-variable columns.

## 5. Finding 4 (script F5, THE KEY QUESTION): the coin channel DROPS constraints

VERDICT: YES. The coin-channel simulators (chi_two_phase.py, chi_two_phase_retry.py,
chi_thmT_verify.py, cert_floor_check.py, chi_o1_scaling.py, chi_p2_multivar.py,
chi_and_vs_single.py, and the "iid" channel of chi_and_chain.py) sample i.i.d. fair row
bits. Their samples are a STRICT SUPERSET of the legal outer-reading designs.

Dropped constraints, completely characterized at the degrees the corpus uses:

1. Degree 1: the 2d+1 free-row parity constraints (XOR of each free row's answers = 1).
   Legal fraction of coin samples, measured vs 2^-(2d+1):

   | point  | legal fraction (measured) | 2^-(2d+1) |
   |--------|---------------------------|-----------|
   | (2,1)  | 0.12587 (12587/100000)    | 0.12500   |
   | (4,2)  | 0.03051 (3051/100000)     | 0.03125   |
   | (6,3)  | 0.00793 (793/100000)      | 0.00781   |

2. Degree 2: the simulators' product semantics (answer = product of the factor answers)
   violate three design identities, each verified at 100,000 samples with zero
   violations on the design side:

   | quantity                                   | design law          | coin channel   |
   |--------------------------------------------|---------------------|----------------|
   | same-hole product of two free pairs        | determined 0        | 1 w.p. 1/4     |
   | same-pigeon product of two free pairs      | determined 0        | 1 w.p. 1/4     |
   | XOR_j L(x_rj . x_cd) (Q-shift sum rule)    | = L(x_cd) always    | holds w.p. 1/2 |
   | diagonal product (distinct row and column) | fresh fair bit, independent of its two singles (P[= product] = 1/2) | = product, always |

   The square law L(x^2) = L(x) is the one degree-2 identity the product semantics gets
   right (ans(x)^2 = ans(x)); measured 0 mismatches in 100,000 design samples at (4,2)
   and (6,3).

   (The determinations hold because the collision and two-hole monomials lie in V(n,d)^rho
   themselves, and the square law and sum rule are the Boolean and Q-shift rows.) The B5
   classification of ALL degree-2 columns (exact, from the augmented echelon):

   | restricted | same-hole  | same-pigeon | square  | diagonal            |
   |------------|------------|-------------|---------|---------------------|
   | (4,2)      | 40/40 pivot| 30/30 pivot | 20/20 pivot | 70/120 pivot, 50 free |
   | (6,3)      | 126/126 pivot | 105/105 pivot | 42/42 pivot | 231/630 pivot, 399 free |

   (The pivot diagonals are parity-determined through the Q-shift sum rules; both
   diagonal classes answer marginally fair bits independent of their component singles,
   which is what C7 measures.)

Do the dropped constraints change any answer distribution the corpus's theorems use?

- Single-variable answers: NO, up to E_full. Total variation between the coin law and
  the design law is EXACTLY 0 on every row-incomplete query set (completion structure;
  C4 confirms at all three points) and on every marginal; it is EXACTLY 1/2 on a fully
  queried free row (C5). The event's probability is bounded by cor:coin's union bound
  (n+1) C(e,2d) / C(n,2d), printed in the script output: small in the super-polynomial
  regime at the larger points (4.4e-05 at (31,3), budget e ~ d n^(1/4)) and weak at toy
  sizes - the exact TV statements (0, and 1/2 on full rows) are the operative facts.
  Hence Theorem B, Props A/C/D, the Bayes posteriors, and the completion lemma are
  KERNEL-FAITHFUL.
- Row-sum parities: YES, completely. Coin: Q_i is a fair coin on free pigeons. Designs:
  Q_i = 0 on every pigeon (TV = 1/2). The two-phase parity certificate (Theorem T's
  mechanism, chi_two_phase.py phase 1, note_to_author.md's certification argument) is a
  COIN-MODEL-ONLY object. This is the kernel-level confirmation of the corpus's own
  adjudication (p2_results.tex prop:rigidity: "under neither reading does any pigeon
  answer Q_i = 1"; ADDENDUM finding 3).
- Degree-2 AND-query laws: YES. The AND no-lift posterior identity (thm:and) is derived
  under the product semantics; the pipeline's AND channel differs (table above), so its
  pipeline transfer is NOT covered by this check and would need a design-space redo.

Related consequence for the counting certificates (cert_floor.md Theorem F; script F7):
under the design law a fully scanned free row has an ODD count of 1s, with P(count = c) =
C(2d,c)/2^(2d-1) on odd c (count 1 with probability 2d/2^(2d-1), TWICE the coin model's
2d/2^(2d)); killed rows still show exactly one 1. The counting mechanism survives, but
Theorem F's constant is a coin-model number.

## 6. Finding 5 (script F6, control): the only kernel that realizes the coin law violates the print

The outer-design kernel {L : L kills the UNRESTRICTED outer V(n,d), L(1) = 1}, with
omega(g) = L(g^rho) read in the outer space, masks every row parity in the never-queried
killed-pair design values: its free-pair answers are i.i.d. fair EVEN on full rows, and
P(Q_i = 1 | free) = 1/2 (measured 0.4962 at (7,1), 0.5004 at (15,2); full-row joint
uniformity PASS). But it satisfies the printed vanishing condition only by accident:
Q_i^rho lies in V(n,d)^rho and the printed condition demands L(Q_i^rho) = 0 for every
design, while only ~1/2 of the sampled outer designs kill it (50382/100000 and
49962/100000). So no design space satisfying Definition 4.3 as printed realizes the coin
law. The coin channel is exactly the design space's row-incomplete single-variable
answer law - which is the precise content of the corpus's own cor:coin with its E_full
clause. The fidelity question is closed in that form.

## 7. Honesty section: what is underdetermined or misstated where

- The printed g^rho definition does not cover (free pigeon, matched hole). The zeroing
  completion is forced by the corpus's own killed-unmatched law (Section 1); under any
  other completion the corpus's channel law fails, so the check has no freedom here.
- The paper's rigidity proposition (a) ("canonical reading: Q_i answers 1 on assigned
  pigeons") is inconsistent with the zeroing restriction semantics: with killed-unmatched
  variables zeroed, Q_i^rho = 0 for assigned pigeons under BOTH readings, and the answer
  is 0 in both cases. The "reversed certificate" scenario does not exist at kernel level
  (ADDENDUM finding 3's "no trivial win" confirmed).
- razborov_check.py's in_span sorts pivot VECTORS by bit_length, which equals leading
  column + 1 and is therefore injective across pivots: the sort is a correct descending
  column order and no hazard exists there. (A genuinely wrong variant is to sort pivot
  COLUMN INDICES by bit_length, where ties within one power-of-2 bucket let a larger
  pivot's row re-set a cleared lower bit; kernel_structure.py's first draft had exactly
  that bug and its reduce_mod now sorts by column value. Recorded as a gf2-toolkit
  gotcha.) No corpus file was edited per the task constraints.
- The brief's item 3(b) expectation ("Q_i = 1 with probability exactly 1/2 on free
  pigeons") is the coin-channel law, and it FAILS at kernel level under the printed
  reading (measured 0.0000 everywhere). The test was run as specified and the failure is
  a finding, not a script defect: it is the kernel-level form of the corpus's own
  rigidity proposition and ADDENDUM finding 3.
- Scope: the degree-2 statements above cover the structures the corpus's AND-line uses
  (same-hole, same-pigeon, square, diagonal, Q-shift sum rules) plus the full pivot/free
  classification of all degree-2 columns; a complete joint law over ALL degree-2
  coordinates was sampled in full at (4,2) (whole-kernel sampling) and via exact
  projected laws at (6,3). Degree-3 coordinates at (6,3) were classified only in count.

## 8. Reproduction

  cd /home/tomzx/pnp && python3 kernel_structure.py

Runtime ~2 minutes total ((7,1) 0.6 s, (15,2) 1.7 s, (31,3) ~88 s, controls ~10 s;
100,000 samples per law). Seeds: RNG_SEED = 20261003 with per-point/per-test offsets;
all randomness is in the design sampling and the coin comparison; every exact
construction (ranks, containments, classifications, projected bases) is deterministic
and internally cross-checked (projected bases vs full kernel basis by span equality;
particular solution and kernel vectors verified against every generator row; the
1-not-in-V consistency check runs inside every echelon).

## 9. Bottom line for the corpus

1. There is ONE design space: V(n,d)^rho = V(2d,d). The outer/canonical distinction
   should be retired from the corpus's framing; the operative object is the printed
   vanishing condition, and it forces the row parities.
2. The exact channel law under that reading: free pairs answer i.i.d. fair bits on
   row-incomplete query sets (marginally fair always); full free rows are parity-locked;
   Q_i = 0 on every pigeon; matched -> 1; killed-unmatched -> 0; L(1) = 1.
3. The coin-channel simulators over-sample: they drop the row parities (legal fraction
   2^-(2d+1)) and, at degree 2, three product identities. Their single-variable results
   are faithful off E_full; their row-sum and product results are coin-model-only.
4. Kernel-faithful corpus results: Theorem B, Props A/C/D, the Bayes posteriors, the
   completion lemma, the counting-certificate mechanism (with a corrected odd-count
   distribution), the adjacency certificate (it consumes only rho-determined structure).
   Coin-model-only: the two-phase parity certificate, Theorem T's law, Theorem F's
   constant, the AND no-lift identity's pipeline transfer.
