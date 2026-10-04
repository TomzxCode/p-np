# The p > 2 map: AC0[p]-Frege and Res(lin_p) beyond characteristic 2 (mapped 2026-10-03)

Purpose: map the known state of AC0[p]-Frege and Res(lin_p)-type systems for p != 2, the
pigeonhole lower-bound landscape per characteristic, and whether the corpus's p = 2
certification phenomenon (the Krajicek chi-task pipeline of arXiv:2609.35927, see
`proof_complexity.md` and `two_phase_tree.md`) has a p > 2 analogue worth formalizing as
Open Problem O6. Method: websearch + webfetch of primary sources (arXiv abstracts and
HTML full texts, ECCC reports, LIPIcs/Springer pages) on 2026-10-03; the full HTML text
of arXiv:2609.35927v2 was read for question 3. No corpus files were edited; LOG.md was
not touched. Everything below is literature mapping except where marked ANALYSIS (the
p > 2 channel derivations in section 4, which extend this corpus's proved p = 2 results
and are flagged as not yet computationally verified).

## 1. Q1: AC0[p]-Frege lower bounds: the strongest known statements, per characteristic (2026-10-03)

The headline fact is characteristic-uniform: for the FULL AC0[p]-Frege system there is no
super-polynomial lower bound on any explicit tautology family, for ANY prime p, tree-like
or DAG-like. Krajicek states the problem for a fixed arbitrary prime p and calls it a
problem that "runs through proof complexity over thirty years" (arXiv:2609.35927v2,
Introduction, https://arxiv.org/html/2609.35927v2). At p = 2 the same status is stated in
Garlik-Kolodziejczyk, "Some subsystems of constant-depth Frege with parity" (Ann. Pure
Appl. Logic, 2018; PDF: https://www.mimuw.edu.pl/~lak/jansparity.pdf, slides:
https://www.dcs.warwick.ac.uk/~igorcarb/events/oxford-complexity-day/slides/Michal.pdf):
their three subsystems are precisely "subsystems of AC0[2]-Frege ... for which exponential
lower bounds are known", implying the full system has none. The frontier's own framing of
the objective is p-general: Braun's companion whitepaper states the project's "main
objective is a superpolynomial lower bound for ordinary PHP in every fixed-depth
AC0[p]-Frege system. That objective remains open" (scope note of arXiv:2609.23015,
whitepaper: https://raw.githubusercontent.com/kbr-/math-research/3979e0cc0a75dde9b845df7ec8869d033dfcd8d4/publications/bit-php-resolution-over-parities/whitepaper.pdf).

Known lower bounds BELOW the full system (the subsystem ladder, all at p = 2 unless noted):

- AC0-Frege plus counting AXIOMS: exponential lower bounds for PHP in AC0-Frege with
  parity (Count_2) axioms, Beame-Riis, "More on the relative strength of counting
  principles", DIMACS Series 39 (1997/98) 13-35, doi 10.1090/dimacs/039/02 (as cited for
  this exact statement by Garlik-Kolodziejczyk 2018); Count_q independence from Count_p
  for distinct primes by polynomial-size constant-depth Frege proofs, Ajtai, STOC 1994,
  doi 10.1145/195058.195207, with the exponential versions and the composite-q extension
  in Beame-Impagliazzo-Krajicek-Pitassi-Pudlak, "Lower bounds on Hilbert's Nullstellensatz
  and propositional proofs", Proc. LMS (3) 73 (1996) 1-26 (referred from the bibliography
  of arXiv:2609.35927, ref [2]). Generalizing to every characteristic p: counting mod q
  for gcd(p, q) = 1 is hard in the mod-p-axioms subsystem, so this rung has known bounds
  at EVERY p, but always for the wrong-principle (axiom) version, not for gates.
- Krajicek's PK_d^c(MOD_p)-type systems (p = 2): exponential lower bounds for PHP in
  tree-like PK^c_d(+) and for Count_3 in dag-like PK^c_d(+) (Krajicek 1997, "Lower bounds
  for a proof system with an exponential speed-up over constant-depth Frege systems and
  over polynomial calculus", STACS 1997, doi 10.1007/bfb0029951; as summarized in
  Garlik-Kolodziejczyk 2018). Garlik-Kolodziejczyk then SEPARATED these subsystems from
  the full system: dag-like PK^O(1)_O(1)(+) is superpolynomially weaker than AC0[2]-Frege
  on De Morgan formulas (adapting Impagliazzo-Segerlind, "Counting axioms do not
  polynomially simulate counting gates", FOCS 2001, doi 10.1109/sfcs.2001.959894), and
  tree-like PK^O(1)_O(1)(+) is quasipolynomially but not polynomially equivalent to
  AC0-Frege with parity axioms; their open problem: a superquasipolynomial separation
  between AC0[2]-Frege and a subsystem containing AC0-Frege with parity axioms on
  parity-free formulas (Garlik-Kolodziejczyk 2018). So the entire known ladder sits
  strictly below AC0[2]-Frege.
- Conditional tree-like bounds with modular connectives: exponential lower bounds for
  tree-like PK*[r] with constant-depth cuts, under plausible ACC0[r] circuit hardness
  assumptions, with PHP-based hard families, and the note that size-s constant-depth
  PK*[r] proofs of PHP(f) imply size-s ACC0[r]-Frege proofs of PHP; Maciel-Nguyen-Pitassi,
  "Lifting lower bounds for tree-like proofs", Computational Complexity 23 (2013) 585-636,
  doi 10.1007/s00037-013-0064-x (conditional separation between different moduli included).
  This is the strongest tree-like-with-modular-connectives statement known, and it is
  conditional at every modulus.
- The one UNCONDITIONAL lower bound touching the full system at any p: Lu-Santhanam-
  Tzameret, "AC0[p]-Frege Cannot Efficiently Prove that Constant-Depth Algebraic Circuit
  Lower Bounds are Hard" (arXiv:2509.16824, Sept 2025; ITCS 2026 per `proof_complexity.md`):
  a family of explicit DNFs expressing that constant-depth algebraic circuit lower bounds
  (Limaye-Srinivasan-Tavenas J.ACM 2025; Forbes CCC 2024) are hard for constant-depth
  algebraic proofs "does not admit polynomial-size propositional AC0[p]-Frege proofs
  infinitely often", unconditionally; the tautology status of the DNFs is open, so the
  result shows the family is either a hard tautology for AC0[p]-Frege or not a tautology
  (https://arxiv.org/abs/2509.16824). This is the closest thing to an AC0[p]-Frege lower
  bound on an explicit family, and the abstract is stated for AC0[p]-Frege without
  restricting p.

Frontier summary per p (verified 2026-10-03): identical at every prime p. No lower bound
of any super-polynomial strength is known for the full system at any characteristic, nor
any exponential bound even tree-like; the canonical hard candidate is PHP at every p; the
pseudo-solution reduction (Krajicek Proc. AMS 152(11) 2024, pp. 4881-4892, and
arXiv:2609.35927) is the only live programmatic route and is characteristic-uniform (see
section 3). The 2026 Res(+) breakthrough does not lift: "For nested extension axioms, as
they arise from AC0[p]-Frege proofs, we know of no corresponding removal step", and "the
AC0[p]-Frege lower-bound problem remains open" (arXiv:2609.23015, HTML v2,
https://arxiv.org/abs/2609.23015). Reading: the odd-p case of the full problem has
received strictly less attention than p = 2 but is exactly as open, and no structural
obstruction peculiar to odd p appears anywhere in the literature mapped here.

## 2. Q2: Res(lin_p): known lower bounds by characteristic, and the PHP/BPHP status (2026-10-03)

Definitions and lineage. Res(lin_R) operates with disjunctions of linear equations over a
ring R with Boolean variables: introduced over Z by Raz-Tzameret 2008 ("Resolution over
linear equations and multilinear proofs",
https://www.sciencedirect.com/science/article/pii/S0168007208000614); its characteristic-
two version Res(+) (clauses of affine equations over F_2) by Itsykson-Sokolov ("Resolution
over linear equations modulo two", Ann. Pure Appl. Logic 171(1), 2020, doi
10.1016/j.apal.2019.102722; earlier version "Lower bounds for splittings by linear
combinations", https://logic.pdmi.ras.ru/~dmitrits/papers/splitting.pdf); the general
ring/field theory by Part-Tzameret ("Resolution with Counting: Dag-Like Lower Bounds and
Different Moduli", ECCC TR18-117, ITCS 2020, Computational Complexity 30:8, 2021, doi
10.1007/s00037-020-00202-x, arXiv:1806.09383). Res(+) sits immediately below AC0[2]-Frege
on the corpus's ladder; Res(lin_Fp) is its analogue at characteristic p, and no
super-polynomial lower bound for unrestricted DAG-like Res(lin_R) over any FINITE field
was known before 2026 (Part-Tzameret 2021: the system "captures a 'minimal' extension of
resolution with counting gates for which no super-polynomial lower bounds are known").

The p = 2 lane (complete restricted ladder, 2010-2026):

- Tree-like: exponential lower bounds for 2-fold Tseitin and an elementary exponential
  bound for unary PHP linear splitting trees (Itsykson-Sokolov, splitting paper above);
  PHP_n^m tree-like size >= 2^{n-1} and tight space >= n-1 via Prover-Delayer games on
  "extensible formulas" (Gryaznov-Ovcharov-Riazanov, ACM ToCT 16(3), 2024, 15:1-15:15,
  doi 10.1145/3675415, arXiv:2404.08370); the tree-like cluster also includes CMSS23
  (Chattopadhyay-Mande-Sanyal-Sherif) and Beame-Koroth per the related-work list of
  ECCC TR25-118 (https://eccc.weizmann.ac.il/report/2025/118/download). Tree-like Res(lin_2)
  is exponentially weaker than general Res(lin_2) (Itsykson-Sokolov, per the account in
  Bhattacharya-Chattopadhyay-Dvorak, CCC 2024, doi 10.4230/LIPIcs.CCC.2024.23).
- Regular fragments: regular (top-regular) Res(+) introduced via read-once linear branching
  programs (Gryaznov-Pudlak-Talebanfard, CCC 2022, per Braun's [GPT22] and the CCC 2024
  paper's [10]); the first super-polynomial fragment bound: regular Res(+) refutations of
  BPHP_n^{n+1} have size >= 2^{Omega(n^{1/3}/log n)}, also yielding the strongly-read-once
  LBP lower bound resolving the GPT22 open question, plus tree-like weak BPHP >=
  2^{Omega(n)} and a width-Omega(n) bound for unrestricted DAG-like Res(+)
  (Efremenko-Garlik-Itsykson, ECCC TR23-187, STOC 2024, SICOMP 54(4):887-915, 2025,
  https://eccc.weizmann.ac.il/report/2023/187/); bottom-regular Res(+) separated
  exponentially from general Res(+) (Bhattacharya-Chattopadhyay-Dvorak, CCC 2024, arXiv:
  2402.04364).
- Bounded-depth DAG-like: the first bounds applying to general (non-regular) Res(+) are
  size-depth tradeoffs: exponential size or depth Omega(n log log N) (Alekseev-Itsykson,
  STOC 2025, pp. 584-595, doi 10.1145/3717823.3718150), depth pushed to Omega(N log N)
  (Efremenko-Itsykson, cited in TR25-118), supercritical size-depth tradeoffs
  (Chattopadhyay-Dvorak, CCC 2025, doi 10.4230/LIPIcs.CCC.2025.24; Itsykson-Knop, ITCS
  2026, doi 10.4230/LIPIcs.ITCS.2026.81); for PHP-type formulas specifically:
  BPHP_m_n proofs of depth D need size exp(Omega(n^3/D^2)), hence exponential size below
  depth O(n^{1.5-eps}) (Byramji-Impagliazzo, ECCC TR25-118, 2025), extended to
  BPHP_n^{n+1} at depth N^{2-eps}, t-collision BPHP at depth N^{2-1/t-eps}, and a lifting
  theorem with constant-size gadgets (Byramji-Impagliazzo, arXiv:2511.20023, the expanded
  posting of the same line, https://arxiv.org/abs/2511.20023; a merged STOC 2026 paper
  [BCBI26] per Braun's account); resolution-width lifts give depth Omega(w^2/log S) and
  size Omega(w^2), including polynomial-size formulas easy for resolution but needing
  superpolynomial-size Res(+) refutations below depth o(n^2/log^4 n) (Itsykson-Podolskii-
  Shekhovtsov, ECCC TR26-018, CCC 2026, doi 10.4230/LIPIcs.CCC.2026.13); polynomial-depth
  bounds for constrained BPHP (Alekseev-Gaevoy, ECCC TR26-007, partly conditional).
- UNRESTRICTED DAG-like: BPHP_n^{n+1} (n = 2^l holes, n+1 pigeons) needs more than
  exp(n/(32768 l^2)) = 2^{Omega(n/log^2 n)} clauses for l >= 32, no regularity or depth
  restriction, i.e. 2^{L^{1/3-o(1)}} for the formula size L = Theta(n^3 log n), Lean 4-
  formalized, with an explicit statement that the theorem "concerns Res(+) only", "does
  not address unary PHP in Res(+)", and that the extension-variable method gives no
  removal step for the nested extension axioms of AC0[p]-Frege (Braun, arXiv:2609.23015).
  This is the bound already catalogued in `proof_complexity.md` lines 10-18.

The odd-p (general finite field F_q) lane:

- Tree-like, every field: exponential lower bounds for tree-like Res(lin_F) refutations
  of the pigeonhole principle for EVERY field F; for Tseitin mod q in tree-like
  Res(lin_Fp) for every pair of distinct primes p != q (2^{Omega(dn)} on d-regular
  expanders); random k-CNFs exponential for tree-like Res(lin_Fp) for every prime p;
  via a size-width relation for tree-like Res(lin_F) over every field plus translation to
  polynomial calculus over F (Part-Tzameret 2021, Corollaries 45-47 and Theorem 43-44).
  Khaniki extends the tree-like bounds to Res*_F(PC_d) for d up to sublinear: Tseitin mod
  q (char(F) != q), random k-CNFs, PHP, and Counting mod q (ECCC TR20-034, ACM ToCL
  23(3), 2022, https://eccc.weizmann.ac.il/report/2020/034/).
- DAG-like over finite fields: the first nontrivial bounds of any kind are Khaniki's
  ALMOST QUADRATIC bounds for DAG-like Res(PC_d/F), d = 1 included, over every finite
  field F, for Tseitin mod q (char(F) != q) and random k-CNFs; caveat noted at the
  frontier: "the rules considered there differ from the formulation of Res(+) used here"
  (Khaniki TR20-034/ToCL 2022; the caveat quoted in Braun arXiv:2609.23015). Then Part's
  ECC-based bounds, restricted to char >= 5: for (s,r)-robust vector subset-sum instances
  (rowspace of A an error-correcting code of distance >= s), 2^{Omega(r)} size lower
  bounds for a DAG-like FRAGMENT (BinRegDags_Fq); tree-like Res(lin_Fq) and LinTrees_Fq
  size >= 2^{Omega(((q+1) ln q)^{-1/3} d^{1/5})} for every instance whose matrix generates
  a code of distance d, for every finite field F_q with q = q(n); random instances are
  (n/3, Omega((n/(q+1) ln q)^{1/3}))-robust and algebraic geometry codes give explicit
  instances (Fedor Part, "Lower Bounds for Subset Sum in Resolution with Modular
  Counting", arXiv:2202.08214, v1 2022, v3 2026, https://arxiv.org/abs/2202.08214).
- UNRESTRICTED DAG-like Res(lin_Fp) lower bounds for PHP or BPHP at ANY p, including
  depth-restricted or regular versions: NONE known for odd p. The odd-p lane is two to
  three restriction-levels behind p = 2 (no analogue of the bottom-regular, bounded-depth,
  or unrestricted BPHP bounds exists in any odd characteristic).

PHP/BPHP lower bounds in Res(lin_p), the precise table (2026-10-03):

- p = 2, bit encoding (BPHP): known at every restriction level, tree-like (TR23-187),
  regular (2^{Omega(n^{1/3}/log n)}, TR23-187), bounded depth (TR25-118, arXiv:2511.20023),
  and unrestricted (Braun 2^{Omega(n/log^2 n)}, arXiv:2609.23015). DONE.
- p = 2, unary encoding (the standard PHP_n that arXiv:2609.35927 itself uses): tree-like
  known (Itsykson-Sokolov; GOR24 2^{n-1}); UNRESTRICTED DAG-like OPEN (Braun explicitly
  disclaims unary PHP). So even at p = 2 the unrestricted DAG-like status of the paper's
  own system is open.
- odd p, unary PHP: tree-like known for every field (Part-Tzameret 2021); DAG-like: NO
  lower bound of any kind known, and no polynomial-size upper bound either (the
  Raz-Tzameret polynomial-size PHP refutations over char-0 rings do not transfer to
  finite fields; Part-Tzameret Theorem 15 covers char 0 only).
- odd p, BPHP: no results found at any level (the bit-encoding instance has not been
  studied at odd characteristic).

Instance-space split by characteristic (structural, cited): the canonical coNP-complete
language of 0-1-unsatisfiable linear systems (LinSys_Fq) is coNP-complete for
char >= 5 and in P for char 2 and 3 (Part-Tzameret 2021, Theorem 5, for char 0 and
p >= 5; extended to all characteristics except 2 and 3 by Gryaznov, "Notes on Resolution
over Linear Equations", CSR 2019, doi 10.1007/978-3-030-19955-5_15, as recorded in
arXiv:2202.08214). Consequence: at odd p >= 5 the Res(lin_Fp) lower-bound program has a
second hard-instance source (LinSys instances hard unless P = NP) that the p = 2 and
p = 3 programs lack; there the hard instances must be CNFs with genuinely non-linear
structure. Reading for the corpus: odd p >= 5 is structurally DIFFERENT from p = 2 in the
Res(lin) lane (more target instances, and the counting is not parity-collapse), yet
empirically no harder - still no unrestricted DAG-like bound anywhere.

## 3. Q3: is the Krajicek chi-task p-specific? (2026-10-03, full text of arXiv:2609.35927v2)

No. The paper is stated for a fixed arbitrary prime throughout, and it never
specializes to p = 2 or discusses any characteristic-specific behavior. Verified from the
HTML full text (https://arxiv.org/html/2609.35927v2):

- Conventions (before Section 1): "we fix an arbitrary prime p for the rest of the paper".
- Definition 3.1 ((d, e, gamma)-solutions), Theorem 3.2 (no (d, h + log S, S^{-1})-solution
  when e^{h/p} >= 2 S^2, i.e. h = O(p log S) = O(log S) at fixed p), and Theorem 3.3
  (a ((log k)^{O(l)}, O(log k), k^{-O(1)})-solution rules out k-step F_l(MOD_p)-refutations)
  are all stated over F_p with constants depending "only on FF and p".
- Definition 4.3 (the candidate Omega(n,d)) fixes n_rho = 2d at EVERY p, with L a degree-d
  design over F_p; Corollary 4.2 rests on Theorem 4.1, Razborov's PC degree theorem, which
  holds over every field (Razborov, Computational Complexity 7(4), 1998; Braun's account
  in arXiv:2609.23015: "Razborov's theorem [Raz98] that polynomial calculus refutations of
  the pigeonhole principle need degree n/2+1 over every field").
- Lemma 4.4 (reduction of tree conflict-finding to labeling a free pair, via a binary
  search for a conflict pair with a variable monomial) is characteristic-uniform.
- Lemma 5.1 / 5.2 define Error(rho) = Sum_P chi(P,rho) p^{-dim^rho(P)} and reduce the
  solution condition to Prob_{rho,P}[chi(P,rho) = 1] at general p.
- Theorem 6.1 concludes at general p: the chi-hypothesis for all (d, e')-trees with
  d = (log k)^{O(l)}, e' = O(log n) + O(d log n) implies no k-step F_l(MOD_p)-refutation
  of -PHP_n. The closing conjecture ("It appears possible that the hypothesis in the
  theorem holds for k(n) = 2^{n^delta}, for sufficiently small delta > 0, even with the
  bound in (3) being Omega(1)") carries no p-qualification. The Section 7 UENS-vs-TC0-
  Frege remark is likewise p-uniform.
- The only p-dependences in the paper are mechanical: query trees are p-ary; the accuracy
  condition contains 1/p; the path probabilities carry p^{-dim}; the target system is
  F_l(MOD_p). There is no remark on p = 2 anywhere, no analysis of the answer channel at
  any characteristic, and no discussion of search-tree strategy at any p: the paper
  reduces everything to the probability task and stops.

Two bibliographic precision notes for the corpus. (1) Theorem 3.3 is NEW in
arXiv:2609.35927: the paper says of it that it "was not stated and proved [in Krajicek
2024] formally so we do it now"; the 2024 paper contains the reduction (Theorem 3.2) and
the explanation after its Theorem 5.2. (2) The corpus's char-2 focus is a SPECIALIZATION
chosen by this corpus (because the answer channel collapses to coins-vs-determined bits
at p = 2, enabling the exact channel law of `two_phase_tree.md`), not a restriction of
the program: Theorem 6.1 would deliver AC0[p]-Frege bounds at ANY fixed p from the same
chi-task, so an odd-p solution of the probability task would immediately give the first
super-polynomial AC0[p]-Frege lower bound in that odd characteristic.

## 4. Q4: what replaces the fair coin at p > 2, and does determined-certification survive? (2026-10-03)

This section is ANALYSIS: it extends this corpus's proved p = 2 results (the channel law
and Theorem T in `two_phase_tree.md`) to general p by inspection of the definitions of
arXiv:2609.35927. It has not been verified by computation this session; the harness
(chi_two_phase.py) needs only the p-ary channel substitution to check it.

The channel law at general p. Under Omega(n,d) at characteristic p, with L uniform in
Des(n,d)^rho (Corollary 4.2 of the paper), a query g answers L(g^rho). By the same
disjoint-support/kernel-basis reasoning the corpus used at p = 2 (linear algebra, no
characteristic dependence): killed-unmatched variables restrict to 0, so the answer is
L(0) = 0 (determined); killed-matched variables restrict to 1, so the answer is L(1) = 1
(determined); free variables answer uniformly in F_p. So the p = 2 fair coin generalizes
to a fair p-SIDED DIE on the free region: for a single-variable query on a free pair the
answer is uniform over F_p, and answers outside {0, 1} (probability (p-2)/p per query to
a free pair) certify freeness DIRECTLY. This matches the corpus's query-race note at
`proof_complexity.md` lines 205-209.

Certification survives, and in a cleaner form. Query the paper's own axiom polynomial
Q_i = 1 - Sum_j x_ij (the pigeon axiom, Section 1 of arXiv:2609.35927). An assigned
pigeon (rho(i) = j) has Q_i^rho = 1 - 1 = 0 DETERMINEDLY at every p; a free pigeon has
Q_i^rho = -Sum_{j in R} b_ij, a sum of 2d free-row design bits, which is uniform in F_p
(any single uniform coordinate suffices). Hence at general p the two-phase certification
tree generalizes verbatim, with hit probability (p-1)/p replacing 1/2:

  Proposed Theorem T_p (ANALYSIS, unverified by computation). At characteristic p, the
  tree that (phase 1) scans rows Q_i until the first NONZERO answer, then (phase 2) scans
  the certified row's free-hole variables x_{i*,j} until the first NONZERO answer, labels
  a CERTIFIED-FREE pair with success 1 - (1/p)^{2d+1} + fallback terms, error
  p^{-(2d+1)}. Phase 2 never fails given certification: a nonzero row sum implies some
  free design bit in the row is nonzero, and the scan finds one deterministically (killed
  holes answer 0 always). At p = 2 this is exactly Theorem T (error 2^{-(2d+1)},
  measured 0.97 at (32,2), replicated in `thmT_verify.md`).

So the determined-certification phenomenon ("answer certifies freeness because assigned
objects cannot produce it") exists at ALL characteristics; what is genuinely p = 2-
specific is that the determined set {0, 1} covers the whole alphabet, so at p = 2 NO
single-variable answer ever certifies and freeness leaks only through linear combinations
(row sums), whereas at p > 2 single variables already leak (answers in {2, ..., p-1}).
The two phases coincide at p = 2 (nonzero = 1) and separate for p > 2.

Do the new p > 2 channels break the chi-hypothesis? In the program's intended regime,
no, and for a characteristic-uniform reason: the binding constraint is the free-pair
density f = (2d+1)2d/((n+1)n) ~ 4d^2/n^2, not the answer alphabet. A scan of e' = d log k
single variables certifies with probability <= e' * f * (p-2)/p ~ 4d^3 log k/n^2, capped
below 1 - k^{-O(1)} whenever d << n^{2/3}/(log k)^{1/3}, the same transition this corpus's
Proposition D proved for the non-adaptive class at p = 2 (success <= (s+1) f, with the
exact transition at d > Theta(n^{2/3}/(log k)^{1/3}), `proof_complexity.md` lines 446-453;
that proof is characteristic-uniform since it only counts free mass). Per-hit posteriors
are higher at p > 2 (more answer values are self-certifying), but hit probability is
still f. And the p-generalized certification tree errs with probability p^{-Theta(d)},
a CONSTANT, which is >= k^{-O(1)} = 2^{-O(log k)} for all d = (log k)^{omega(1)}: the
chi-hypothesis of Theorem 6.1 survives its strongest known attacker at every
characteristic, exactly as at p = 2 (`two_phase_tree.md`, implications 1-3).

One more structural difference, from the Res(lin_Fp) literature rather than the chi-task:
at p >= 5 the natural hard-instance family LinSys_Fp is coNP-complete, while at p = 2, 3
it is in P (section 2, citations there). The chi-task is insensitive to this split (the
system -PHP_n is CNF-derived at every p), but the adjacent Res(lin_p) lane at odd p >= 5
can target an instance class with built-in worst-case hardness, which the p = 2 lane
cannot. Also note p = 3 is the smallest characteristic where the direct single-variable
certification channel exists at all ((p-2)/p = 1/3), making it the natural first target
for any computational study of the p > 2 chi-task.

## 5. Verdict: Open Problem O6, the p > 2 analogue (2026-10-03)

Verdict: YES, there is an unmapped open problem worth formalizing, and it is arguably the
better sibling: the reduction chain of arXiv:2609.35927 is proved at every characteristic,
the design foundation (Razborov) holds at every characteristic, the p > 2 case has a
certification tree just as p = 2 does (section 4), and NOTHING in the literature treats
the chi-task at p != 2 (the paper stops at the probability task; no follow-up exists, cf.
`monitor_2026-10-03b.md` section 1: zero citations). Meanwhile the adjacent frontier at
odd p is strictly less crowded than at p = 2: the Res(lin_Fp) PHP/BPHP program has no
regular, no bounded-depth, and no unrestricted bound at any odd p (section 2).

O6 (formal statement). Fix an odd prime p (or any fixed prime p >= 3). Let Omega(n,d) be
Definition 4.3 of arXiv:2609.35927 at characteristic p (restrictions with n_rho = 2d free
holes, uniform degree-d designs L of the restricted system). Determine whether:

  for every (d, e')-tree T' with d = (log k)^{O(l)} and e' = O(log n) + O(d log n),
  Prob_{rho,P}[chi(P, rho) = 1] >= k^{-O(1)} for all n >> 1,

with rho uniform over restrictions and P a uniform root-to-leaf path (the hypothesis of
Theorem 6.1 there, stated for the fixed arbitrary prime p). Equivalently: no shallow
low-degree p-ary query tree certifies a free pair with probability 1 - k^{-O(1)} - the
freeness-certification impossibility over F_p. A positive answer at any k(n) >= n^{omega(1)}
(a fortiori k(n) = 2^{n^delta}), combined with the paper's Theorem 6.1 and the
BIKPRS96/BKZ ENS equivalence (Buss-Impagliazzo-Krajicek-Pudlak-Razborov-Sgall,
Computational Complexity 6(3), 1996/97, pp. 256-298), yields k-step lower bounds for
F_l(MOD_p)-Frege refutations of -PHP_n: the FIRST super-polynomial lower bound for the
full AC0[p]-Frege system at ANY characteristic, and the first lower bound of any kind for
odd-p AC0[p]-Frege proofs of the pigeonhole principle. A negative answer (a tree with
error < k^{-O(1)}) refutes Omega(n,d) as a pseudo-solution at that p and redirects the
program, exactly as in the p = 2 statement of Open Problem O1 (`proof_complexity.md`).

Why O6 is a distinct problem, not a corollary of O1. The proof tools are
characteristic-specific in both directions. Any p = 2 impossibility proof must use the
0/1-determinedness of killed answers, which fails at p > 2 (free answers range over F_p,
and 1 - 1/p of free answers are self-certifying for single variables). Conversely, the
p = 2 posterior audit (the exact per-pair Bayes computation giving posterior
2d^2/(2d^2+n), `proof_complexity.md` lines 266-295) has no direct analogue: answers are
p-valued, so the event algebra of the single-variable class must be redone (the p > 2
version should be EASIER - more answers are informative - but nothing is proved).
The characteristic-uniform parts already in place: the reduction chain (the paper's own
text, section 3 above), the design theorem (Razborov, every field), the non-adaptive cap
arithmetic (free-density counting), and the certification tree's existence (section 4).

What is open inside O6, in order: (1) the channel-law audit at p > 2 - verify uniformity
and independence of free-region design values over F_p computationally with the existing
harness (substitute the p-ary channel in chi_two_phase.py; check Proposed Theorem T_p's
error p^{-(2d+1)} at toy scale, p = 3 and p = 5); (2) the single-variable posterior audit
at p > 2; (3) the common core of O1 and O6: the all-degrees adaptive quantifier, open at
every characteristic.

Watch triggers (add to the rung's list): any paper analyzing Omega(n,d) or the chi-task
at p != 2; any odd-p Res(lin_Fp) PHP or BPHP lower bound at regular, bounded-depth, or
unrestricted level (the odd-p analogue of the TR23-187 / TR25-118 / Braun sequence); any
verification or refutation of Proposed Theorem T_p; any claimed tree achieving error
< k^{-O(1)} against Omega(n,d) at any characteristic.
