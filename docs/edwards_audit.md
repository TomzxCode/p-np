# Audit: arXiv:2512.11820 "Toward P != NP: An Observer-Theoretic Separation via SPDP Rank and a
# ZFC-Equivalent Foundation within the N-Frame Model" (Darren J. Edwards; v1 30 Nov 2025 through
# v5 8 Jan 2026, 208 pages)

Auditor: this session, 2026-10-03, from the arXiv HTML full texts of v1 and v5 (downloaded and
converted to plain text; quoted line-anchors below refer to that local text).
Verdict: the proof fails. The bridging extraction map is asserted, not proved, and its three
published forms identify three different polynomials; under every possible reading, one side of
the separation chain is false or the contradiction evaporates quantitatively.
Additionally, the paper's own P-side collapse theorem is refuted by its own NP-side lower bound
when both are applied to the machine the proof must compile (the instrumented solver).
Triage call (F1 + F5) confirmed; F4-shape and F3 also fire; F6 does not.

## What was fetched and what was not

- Abstract page: https://arxiv.org/abs/2512.11820 (full metadata, abstract, submission history).
- Full HTML of v5: https://arxiv.org/html/2512.11820v5 (5.6 MB, 12207 lines of plain text after
  pandoc conversion) and full HTML of v1: https://arxiv.org/html/2512.11820v1 (4.1 MB, 9050 lines).
- Not fetched: the PDF and TeX source (the HTML was complete and sufficient), and the intermediate
  v2/v3/v4 full texts (their dates and sizes are on the abstract page).
- Community uptake: none found. Semantic Scholar API returned HTTP 429, web search surfaced only
  aggregator mirrors (pubdb.com, arxiv.gg, academia.edu, exa.ai), and pith.science has no entry
  (404). No independent citation or referee discussion located as of 2026-10-03.

## The argument's skeleton (as the paper states it)

M0 (P-side compiler): Theorems 203/209 compile every M in DTIME(n^t) into a radius-1 SoS polynomial
P_{M,n} with "CEW(P_{M,n}) = O(log n)" and "Γ_{κ',ℓ'}(P_{M,n}) ≤ n^{O(1)}" at κ',ℓ' = Θ(log n)
(Width⇒Rank, Lemma 32).
M1 (instrumentation): Lemma 204 extends any 3SAT decider M to an instrumented M' that "prepends a
static clause-gadget sheet ... computing the coupled verifier polynomial
Q_Φ^×(x,z) = ∏_{C∈Φ}(1 − z_C · V_C(x)²)", claiming "Compilation preserves polylog CEW and
polynomial rank: Γ_{κ,ℓ}(P_{M',n}) ≤ n^{O(1)}" (stated without proof).
M2 (extraction): Lemma 7 / Lemma 205 / Theorem 223 produce an instance-uniform, rank-monotone map
T_Φ from P_{M',n} onto the clause sheet Q_Φ^×.
M3 (NP-side lower bound): Lemma 124 / Theorem 128 prove Γ(Q_Φ^×) ≥ binom(m,κ) = n^{Θ(log n)} for
sheets over m = Θ(n) disjoint clause blocks with free selector variables z.
Clash (Theorem 207, five steps): under P = NP a solver M_sol exists, so Γ(P_{M_sol',n}) ≤ n^{O(1)},
extraction gives Γ(Q_{Φ_n}^×) ≤ n^{O(1)}, the minor gives ≥ n^{Θ(log n)}, contradiction.
The main theorem is stated twice: Theorem 5 (Section 5, "single-statement form,
referee-auditable") and Theorem 207 (Section 39, "Global God Move ... ⇒ P ≠ NP", called the main
theorem in Section 2.2).

## The exact main theorem statement (task item 1)

Theorem 5 (SPDP separation in the compiled (blocked) model), Section 5, quoted:

"Fix (κ, ℓ) = Θ(log n) and the radius–1 block partition B induced by the uniform compiler
templates. ... Then the following three facts (proved in this manuscript) imply P ≠ NP:
1. (P-side compiled upper bound) For every deterministic machine M ∈ DTIME(n^c), the uniformly
   compiled family {P_{M,n}} satisfies Γ^B_{κ,ℓ}(P_{M,n}) ≤ n^{O(1)}.
2. (NP-side explicit compiled lower bound) There exists an explicit uniform 3SAT witness family
   {Φ_n} such that the associated coupled clause-sheet polynomials {Q^×_{Φ_n}} satisfy
   Γ^B_{κ,ℓ}(Q^×_{Φ_n}) ≥ n^{Θ(log n)}.
3. (Instance-uniform, witness-free extraction and rank monotonicity) For every instance Φ there is
   an instance-uniform map T_Φ (depending only on Φ, not on any witness) such that
   T_Φ(P_{M',N(Φ)}) = Q^×_Φ and Γ^B_{κ,ℓ}(T_Φ(p)) ≤ Γ^B_{κ,ℓ}(p) for all polynomials p.
Consequently, P ≠ NP."

Item (3) is the bridging step and is exactly where the proof fails; see Finding 1.

## The axiom/definition inventory (task item 2)

SPDP rank (Definition 65): "The SPDP matrix M_{κ,ℓ}(p) is the matrix with rows indexed by (S,m) ∈
𝒮_κ × 𝒯_ℓ and columns indexed by monomials in the standard monomial basis, where the (S,m)-th row
is the coefficient vector of m · ∂_S p ... Γ_{κ,ℓ}(p) := rank_F M_{κ,ℓ}(p)."
This is standard shifted-partial-derivative rank (Kayal-Saha style). The load-bearing variant is
the paper's bespoke blocked form: Γ^B_{κ,ℓ}(p) := rank(M^B_{κ,ℓ}(p)), a row/column restriction of
the unblocked matrix, so Γ^B ≤ Γ (Lemma 88, correct).

CEW (Definition 2, main text): "CEW^B_{κ,ℓ}(O; n) := Γ^B_{κ,ℓ}(Π^⋆[P_{O,n}])" where Π^⋆ is "the
fixed Global God-Move gauge (the universal projection/normal form)". So in the main definition,
CEW literally IS an SPDP rank after a gauge map.
CEW again (Definition 66, Appendix G.2): "CEW(p) is the minimal w such that after a universal
restriction ρ_⋆ (defined via deterministic switching lemma), the SPDP rank satisfies
Γ_{κ,ℓ}(p ↾ ρ_⋆) ≤ w". This is a different quantity (rank after a rank-destroying restriction,
minimized over restrictions).
CEW a third time (Remark 2): structural CEW (sCEW, "the maximum number of block interfaces crossed
by any local constraint window") vs algebraic CEW (aCEW, Definition 2), "coincide up to this
polynomial lifting" by assertion. The paper concedes the multiplicity at line 1684: "In some
appendix sections we introduce an alternative, purely algebraic notion of CEW ... This SPDP-based
CEW is used only as an equivalent characterisation of low-width behaviour." No equivalence is
proved anywhere.

N-Frame model (Definitions 1, 3, 4): an "N-Frame observer" is a tuple
O_n = (U_n, V_n, Z_n, 𝒯, B, Π^⋆) of interface/state/tag variables, a finite radius-1 template
library, a block partition, and the gauge Π^⋆. A "boundary-limited agent" is "(x, b, t)" with
polynomial budgets, wrapped in an "N-Frame envelope". The model's authority is entirely
self-referential: "In the N-Frame model, the term 'N' denotes natural selection acting over the
landscape of computational forms, while 'Frame' refers to the observer frame F = (S, R, I)"
(Section on motivation), and the citations for the model are [3] (the author, Frontiers in
Computational Neuroscience 2025, on "conscious observer-self agents") and [4] (the author's
forthcoming Palgrave book). Lemmas 1-2, which identify finite envelopes with poly-time computation,
are three-line sketches that never construct the compiled polynomial for an arbitrary "effective
inference/update process x"; Lemma 1 concludes "CEW(Env_n(x,b,t)) = O(b(n)^c) for some constant c
depending on the structure of T" without defining c or constructing the encoding.

"ZFC-equivalent foundation" (title phrase): the body never defines a foundation. The closest
content is Corollary 208: "All constructions above—sorting-network compiler, CEW accounting, SPDP
rank theory, and instance-uniform extraction—are finitely definable and verifiable within ZFC. No
additional axioms, randomness, or oracles are required." This is a claim of ZFC-definability, not a
foundation, and the Lean evidence is a to-do list: Appendix I instructs implementers to "Replace
the sketchy SPDProws/SPDPcols/SPDPMat with finite index sets". No machine-checked artifact exists
(the paper is honest about this: formalization "remains future work").

F1 check (does the normal form capture ALL polynomial-time algorithms, or only its own observers?).
Unusually for this corpus, the paper attempts the universal quantifier: Theorem 209 ("Universal
P→poly-SPDP bridge") states "Fix any deterministic Turing machine M ∈ DTIME(n^t) ... (v) (SPDP rank
bound) Γ_{κ',ℓ'}(P_{M,n}) ≤ n^{O(1)}", and Theorem 5 item (1) repeats it for every L ∈ P.
So the surrogate capture is claimed, not merely assumed. However, the capture theorem is refuted by
the paper's own NP-side construction (Finding 1, Reading A): the surrogate framework provably fails
on the instrumented solver M', which is itself a polynomial-time machine of the kind Theorem 209
quantifies over. The abstract's complementary direction, "unbounded CEW characterizes the class
NP", is never proved as a characterization; only one engineered witness family is shown high-rank.
So F1 fires in the corpus's standard sense: the theorem that would make the surrogate adequate is
false, and the class-level identification (CEW ⟺ P/NP) is a half-bridge.

## Finding 1: the bridging extraction is asserted, internally inconsistent, and quantitatively
insufficient (fatal; kills M2 and the composition)

The extraction map's three published forms disagree about its output object:

- Lemma 7 (Section on the God-Move): "Π_Φ(P_{M',N(Φ)}) = Q^×_Φ and Γ^B_{κ,ℓ}(Π_Φ(p)) ≤
  Γ^B_{κ,ℓ}(p). Moreover, Π_Φ is instance-uniform and witness-free." (output: the FULL sheet.)
- Lemma 205 (Section 38): "there exists a block-local transformation
  T_Φ = (basis) ∘ (affine relabel) ∘ (restriction) ∘ (projection) computable in poly(n) time from
  Φ alone, such that T_Φ(P_{M',|ρ(Φ)|}) = Q^×_{Φ,𝒮} ... where 𝒮 = 𝒮(n) is the activated clause-set
  from the God-Move projection." (output: the ACTIVATED sheet.)
- Theorem 223 (Section 40.7): "T_Φ(P_{M*,|ρ(Φ)|}) = Q^×_Φ" with proof sketch: "Pin administrative
  variables to compiler constants, then project to verifier columns. By Lemmas 219–221, each step
  is rank-nonincreasing. The resulting polynomial has the coupled verifier sheet form Q^×_Φ."
  (output: the FULL sheet again.)

The proof of Theorem 5 uses the full-sheet form: "By Item (3), there is an instance-uniform
extraction map T_{Φ_n} such that T_{Φ_n}(P_{M_sol,Φ_n}) = Q^×_{Φ_n}". But Lemma 205, the cited
source, delivers Q^×_{Φ,𝒮}. The rank-monotonicity half of item (3) is genuinely proved (Lemmas
33-36: restriction, submatrix, subadditivity, affine invariance; these proofs are fine). The
EQUALITY half is never proved; the cited "Monotonicity Lemmas (Section 16)" are exactly the lemmas
that give rank non-increase, i.e., the wrong half.

The equality is not merely unproved; each reading of the compiled polynomial makes one load-bearing
statement false:

Reading A (selectors free, Lemma 224): "P_{M',|x|}(u, z, v) = Q^×_Φ(u,z) + R_{M',Φ}(v), ... no
cross-constraints couple (u,z) and v." Then for every S ⊆ C_disj, ∂_{z(S)}P_{M',n} =
∂_{z(S)}Q^×_Φ (R does not involve z), so the binom(L,κ) diagonal minor of Lemma 124/Theorem 128
sits inside M_{κ,ℓ}(P_{M',n}), giving Γ(P_{M',n}) ≥ n^{Θ(log n)}. This contradicts Lemma 204's own
"Γ_{κ,ℓ}(P_{M',n}) ≤ n^{O(1)}" and Theorem 209's universal bound, both of which apply to M'
(the instrumented solver is a deterministic poly-time machine). The paper's P-side collapse theorem
is false for the paper's own machine.

Reading B (selectors wired, Lemma 206): "there exists a deterministic local wiring z = ζ(u,v) such
that P_{M',n}(u,v) = Q^×_Φ(u,z)|_{z=ζ(u,v)} + R_{M',Φ}(v)". Now the compiled polynomial has no
free selector variables at all. The operations of T_Φ (pin, project, relabel, basis change) only
delete or invertibly transform variables; none can resurrect the z-monomial structure that Lemma
124's off-diagonal vanishing argument requires. The equality T_Φ(P_{M',n}) = Q^×_Φ is unobtainable,
and the lower bound never transfers.

Reading C (activated sheet, Lemma 205 + Definition 7): "The Global God-Move selects an activated
clause-set 𝒮 = 𝒮(n) ⊆ Φ_n with |𝒮| = Θ(log n); all other clauses are deactivated (set z_C = 0)."
Then ∂_{z(S)} of the extracted object is identically zero unless S ⊆ 𝒮, so any identity minor has
size at most binom(Θ(log n), Θ(log n)) = n^{O(1)}. Independently, Q^×_{Φ,𝒮} is supported on O(log n)
clause blocks with degree O(log n) (Definition 38), so its SPDP rank is at most
(O(log n))^{O(log n)} = n^{O(log log n)}. Both bounds are far below the n^{Θ(log n)} the
contradiction needs: with the P-side bound n^{O(1)} the extracted rank n^{O(1)} violates nothing.
Definition 7's "Clarification" asserts the opposite without proof: "The identity-minor lower bound
(yielding rank n^{Θ(log n)}) exploits choices across all n clause blocks via the κ-derivative
construction, not just the Θ(log n) simultaneously activated clauses. The activation window
determines degree; the global block count determines rank." But Theorem 128's own proof indexes the
minor by derivatives with respect to the selector variables, and deactivated blocks contribute
identically zero rows. This sentence is where the proof has to work and does not.

Trilemma form (F4-shape): Lemma 204 (compiled instrumented machine has rank n^{O(1)}), Lemma 224
(compiled instrumented machine decomposes with the free-selector sheet as a summand), and Lemma 124
(free-selector sheet over Θ(n) blocks has rank n^{Θ(log n)}) are jointly inconsistent. All three
are load-bearing: Lemma 204/209 feed Theorem 207 step 3, Lemma 224 feeds Theorem 223's extraction,
Lemma 124/128 feed Theorem 207 step 5. No choice of readings rescues all three.

## Finding 2: the P-side and NP-side bounds are not evaluated on the same object (restriction
asymmetry; independent of Finding 1)

Section 8's spine theorem (Theorem 12) proves the P-side bound only after a restriction: Step 4
computes "Γ^B_{κ,ℓ}(P_M ↾ ρ^⋆) ≤ Σ_t Γ^B(P_{M,t}) ≤ poly(n)·(log n)^{O(1)} = n^{O(1)}", where ρ^⋆
is the "canonical restriction family" from a derandomized switching lemma. Step 5 states the NP-side
bound on the unrestricted object: "Compile Φ_n under the same compiler templates and block
partition B to obtain P_{Φ_n}. By the explicit minor lemma ... Γ^B_{κ,ℓ}(P_{Φ_n}) ≥ n^{Ω(log n)}."
No step applies ρ^⋆ to the NP side or transfers the lower bound through it. Since Lemma 33
("Restriction monotonicity": Γ(p ↾ ρ) ≤ Γ(p)) is one of the paper's own proved lemmas, a rank n^{Θ(log n)}
minor has no license to survive ρ^⋆; if ρ^⋆ is applied to both sides the gap closes to nothing, if
to neither the P-side bound is unavailable, if to only the P side the two inequalities are about
different polynomials. All four combinations fail to compose.

The post-restriction route the paper does attempt (Theorems 153/154) has the same defect in a
different place. Theorem 153: "There exists a computable map n ↦ s*_k(n) ∈ {0,1}^{O(log n)} such
that ... for every deterministic M ∈ DTIME(n^k), rk_{SPDP,ℓ}(confPoly(M,n) ↾ ρ*_{n,k}) ≤ n⁶."
Theorem 154 ("Uniform NP-side rank lower bound") claims the NP side survives the same restriction,
but its Step 2 augments the NP object before measuring: "Attach to Φ_x a Tseitin-style parity
scaffold ... For every clause occurrence we add a private literal (fresh variable)", and Step 5's
post-restriction rank comes entirely from this adjoined scaffold ("the mixed partials across
different lanes factor as a Khatri–Rao product ... the product rank is Γ ≥ (1+δ)^κ · N^{Ω(1)} = n^{Ω(log n)}").
The P-side bound of Theorem 153 is proved for the bare compiled machine confPoly(M,n); no theorem
covers scaffolded objects on the P side, and no theorem measures the NP language's ordinary encoding
without the scaffold. The "same (κ,ℓ) used on the P-side" rhetoric conceals that the two objects
differ by an expander scaffold whose sole function is to carry the lower bound.
The claim "For NP witnesses, the same ρ_⋆ leaves exponential order-ℓ SPDP rank (Theorem 17.2)"
(Sections 21.7 in v1, 35.7 in v5) rests on a dangling reference: "Theorem 17.2" is a section number
cited as a theorem, and Section 17.2 of v5 is titled "Locality and SPDP rows", not an NP restriction
lemma. Theorem 195's proof inherits this: "By Theorem 17.2 (NP restriction lemma), for every n there
is a witness w such that rk_{SPDP,ℓ}(jointPoly(V,n) ↾ ρ_⋆[w]) = 2^{Ω(n)}."

The paper also contains a complete SECOND separation chain built on these definitions, in v5
Sections 35.6-36 (v1 Sections 21.6-22.1, with theorems renumbered): "Recall CEW_ℓ(f) =
rk_{SPDP,ℓ}(p_f ↾ ρ_⋆)" then "Theorem 196 (Separation via CEW): P = {f | CEW_ℓ(f) ≤ n⁶} and
NP ⊇ {f | CEW_ℓ(f) ≥ 2^{Ω(n)}}. In particular, P ≠ NP", citing Theorem 191 (P-side n⁶) and
Theorem 195 (the dangling-reference NP side just quoted). This chain silently fixes the other
definition of CEW (Definition 66), uses different constants (n⁶, 2^{Ω(n)}) from the main chain
(n^{O(1)}, n^{Θ(log n)} at κ,ℓ = Θ(log n)), and its recap disclaimer ("This subsection is a recap
... not used in the logical derivation of Theorems 191–196") is self-contradictory since Theorem 196
IS a derivation of P ≠ NP. The two chains are never reconciled.

## Barrier-immunity claims (task item 4): by definition, by assertion, and disowned in scope

The abstract (arXiv metadata, all versions) claims: "(4) proofs of barrier immunity against
relativization, natural proofs, and algebrization." The barrier section itself (Section 43) opens
with: "Scope (not used in the separation chain). This section provides context relative to classical
barrier frameworks ... No statement in this section is used as a premise in the audit-layer proof of
the main separation theorem. A referee may safely skip this entire section." A second barrier
statement (Theorem 197, Section 36.1) is not marked non-load-bearing and proves barrier avoidance
against redefined barriers (see below).

Relativization, Theorem 235: "define the 'relativized' SPDP rank Γ^{(O)}_{κ,ℓ}(p) to be the rank of
the same shifted partial-derivative matrix M_{κ,ℓ}(p) computed over F (i.e., the definition does not
refer to oracle answers). Then Γ^{(O)}_{κ,ℓ}(p) = Γ_{κ,ℓ}(p) for all O." This is a tautology (the
relativized rank is defined to be the unrelativized rank), and the paper concedes the limit: "It
does not prove a separation P^{(O)} ≠ NP^{(O)}."
Algebrization is treated in three inequivalent ways in one document. First, Theorem 197 (v5 Section
36.1, "Barrier immunity") redefines the barrier as field-extension invariance: "(Non-algebrization.)
If k/F is any field extension with the same characteristic ... then rk_{SPDP,ℓ,k}(p_f ↾ ρ_⋆) =
rk_{SPDP,ℓ,F}(p_f ↾ ρ_⋆)" (strawman: Aaronson-Wigderson algebrization is about algebraic oracles,
not field extensions). Second, Proposition 238 (Section 43.3): "define p^{(A)}(x,Z) := p(x) (i.e.,
the oracle does not modify p). Then Γ_{κ,ℓ}(p^{(A)}) = Γ_{κ,ℓ}(p)" (a tautology: the oracle is
defined not to touch the polynomial). Third, Appendix L's Theorem 280 is honest: "There exists an
algebraic oracle A such that the following fails relative to A: (Compiled SPDP collapse)^A: every
M ∈ P^A compiles to Γ^B_{κ,ℓ}(p_{M,n}) ≤ n^{O(1)}", because the compiled polynomial of a single-query
machine "contains p_n as a restriction/projection" for a random truth-table oracle. And Remark 90:
"A formal non-algebrization theorem would require fixing a specific algebraic-oracle model and
verifying the entire argument there; we leave this as future work." The honest version (Theorem 280)
concedes that the collapse lemma is a statement about encodings and template libraries, not about
time-bounded computation as such.
Natural proofs, Theorem 236 (non-largeness of the high-SPDP-rank property, a counting argument) is
plausible and correctly scoped ("We mention this only as context"), but sits in the same
non-load-bearing section.
Net: barrier immunity is addressed by assertion and by definitions that make the compared quantities
identical, not by construction, and the paper's own scope note disclaims the section the abstract
advertises. The LaTeX abstract of v5 quietly downgraded "proof of barrier immunity" (v1) to
"structural analysis showing why the framework avoids ... preconditions", while the arXiv metadata
abstract still reads "proofs of barrier immunity".

## Version churn analysis, v1 to v5 (task item 5)

Submission history (abstract page): v1 Sun 30 Nov 2025 (2,880 KB), v2 Tue 16 Dec 2025 (2,883 KB),
v3 Sun 21 Dec 2025 (2,376 KB), v4 Sat 27 Dec 2025 (2,383 KB), v5 Thu 8 Jan 2026 (2,390 KB).
Five versions in 40 days, matching the corpus's high-churn pattern (McCallum v15, Gao v12).

- Title: identical across v1 and v5 (and hence presumably throughout).
- Size: v1 has 35 sections plus appendices A-I; v5 has 49 sections plus appendices A-N. About 3,100
  additional lines of plain text, almost all scaffolding ("How to Read" sections 1 and 3, the
  audit-first guide, Consolidation Theorem 215, invariance lemmas 219-221, the NC0 padding theorem
  115, barrier appendices L-M-N).
- Load-bearing spine unchanged: v1's Theorem 147 ("Global God Move ⇒ P ≠ NP") and v5's Theorem 207
  have the same five-step structure, same inequalities, same contradiction; the extraction lemma was
  asserted in v1 (Lemma 145: "T_Φ(P_{M',|ρ(Φ)|}) = Q_Φ") exactly as it is asserted in v5.
- The NP-side object changed materially: v1 extracted the ADDITIVE sheet Q_Φ; v5 extracts the
  COUPLED sheet Q^×_Φ, and v5's Remark 85 explains why: the additive form "cannot support identity
  minors due to vanishing cross-block partials (Remark 54)". The repair that forced four revisions
  was to make the hard family multiplicative in free selector variables, which is precisely what
  makes the composition with the P-side compiler impossible (Finding 1).
- Theorem renumbering between v1 and v5 (compilation Theorem 65 → 203/209, lower bound Theorem
  67 → 94/128, main theorem 147 → 207) indicates wholesale restructuring, so earlier citation-based
  checks do not carry over.
- The barrier material migrated from v1's Sections 28 and 32 ("Barrier Analysis", "Barriers
  Revisited") into v5's Section 43, retitled "Barrier Context (Non-Load-Bearing Meta-Discussion)",
  while the metadata abstract kept "proofs of barrier immunity"; v5 also added a second "Barrier
  immunity" statement (Theorem 197, Section 36.1) with a strawman definition of algebrization (see
  the barrier section below).
- The second separation chain (CEW-collapse, Theorem 136 in v1 Section 21.6 / Theorem 196 in v5
  Section 35.6) persists unchanged in structure across all versions, including the dangling
  "Theorem 17.2" citation.
- The paper's internal date line reads "August 24, 2026" in both v1 and v5 (never updated; ten
  months after the v1 submission date it contradicts).

## The single fatal step

The extraction equality of Theorem 5 item (3) / Lemma 7 / Lemma 205 / Theorem 223: the claim that a
pin-project-relabel map sends the compiled instrumented solver polynomial P_{M',N(Φ)} exactly onto
the clause sheet Q^×_Φ. Its rank-monotone half is proved; its equality half is asserted with a
proof sketch that cites only the monotone half, and the three published versions of the statement
disagree on the output object (full sheet, activated sheet, wired sheet). Under every consistent
reading, either Lemma 204/Theorem 209's P-side bound is false for M' (Reading A) or the equality is
false (Readings B and C), and in Reading C the surviving inequality gap is n^{O(1)} versus
n^{O(log log n)}: no contradiction.

## What would have to change

- A single fixed definition of the extracted object, and a proof that the compiler output of the
  instrumented solver contains it with free selector variables over Θ(n) blocks; then Lemma 204's
  rank preservation must be dropped, and the P-side bound re-derived without it (which would
  contradict Theorem 209's universal quantifier).
- Or: a rank lower bound for the ACTIVATED sheet (post-deactivation) of size super-polynomial,
  refuting the binom(|𝒮|,κ) counting bound above.
- Or: a proof that the NP-side minor survives the universal restriction ρ^⋆ (Lemma 155 attempts
  this for a different object; the main chain would have to cite and rely on it).
- Consistent single definitions of CEW across main text and appendix.

## What survives (fairness)

- Theorem 94: a clean, correct-looking identity: Γ_{κ,0}(perm_n) ≥ binom(n,κ) via private diagonal
  monomials. Easy and classical in spirit, but sound.
- Lemma 124 / Theorem 128: correct algebra showing the coupled sheet
  ∏_{C}(1 − z_C V_C(u_{B_C})²) over m = Θ(n) disjoint blocks has SPDP rank ≥ binom(m,κ) = n^{Θ(log n)}
  at κ = Θ(log n), over any field. A true statement about a bespoke encoding. Its complexity meaning
  is nil: the high rank is bought by free selector variables in the encoding, not by NP-hardness
  (the paper's own Theorem 280 makes exactly this point for oracle encodings).
- Theorem 236: the non-largeness counting bound for high shifted-partial-derivative rank at
  κ,ℓ = O(log n); a legitimate small observation about why such measures escape Razborov-Rudich.
- Theorem 280 (Appendix L): the honest and correct observation that the P-side collapse fails
  relative to a random algebraic oracle; it is the paper's most useful result and it refutes the
  universality of its own central lemma.
- Theorem 115's sketch (expander ball-packing giving a signed identity minor for Tseitin
  characteristic polynomials) is plausible classical combinatorics, stated for an ordinary partial
  derivative matrix and used only "to connect it to SPDP via the bridge".
None of this touches P vs NP; the correct content is rank bookkeeping on engineered polynomials
plus one meta-observation that undercuts the main lemma.

## Verdict and taxonomy mapping (task item 6)

- F5 fires (primary): the bridging iff is proved in one direction only (rank non-increase) while
  the needed direction (exact extraction equality) sits in a proof sketch citing the wrong lemmas.
  Quote anchors: Theorem 5 item (3), Lemma 7, Lemma 205, Theorem 223 with its "Pin administrative
  variables ... By Lemmas 219–221, each step is rank-nonincreasing" sketch.
- F4-shape fires: Lemma 204 + Lemma 224 + Lemma 124 are jointly inconsistent, the same
  domination/locality/advantage trilemma shape as Proposition 1 in `goertzel_audit.md`, transposed
  from switching lemmas to rank bookkeeping.
- F3 fires: the activated-to-full sheet bridge (Definition 7 "Clarification") and the
  restriction-to-unrestricted bridge (Theorem 12 Steps 4-5) do not exist in the cited direction or
  strength.
- F1 fires in the corpus's sense: the surrogate (compiled blocked SPDP rank) provably fails to
  capture the paper's own instrumented solver, and "unbounded CEW characterizes NP" is unproved;
  mitigated by the paper genuinely attempting the universal quantifier (Theorem 209), which is more
  than most corpus entries do.
- F6 does not fire: there is no fake formalization; the paper says formalization is future work and
  the Lean appendix is an explicit to-do skeleton.
- Community status: no independent citations, no machine-review entry, mirrors only.

## Base-rate comparison and a candidate new failure mode (task item 7)

The claim shows every corpus-typical feature (surrogate quantity, asserted bridge, version churn,
self-referential framework citing the author's own claimed Navier-Stokes proof [6], barrier claims
by assertion). One feature is not cleanly covered by F1-F6: load-bearing terms exist in two or more
inequivalent formal definitions in the same document, and the chain only reads as valid because each
use site silently takes a different instance. Observed here for:
- CEW: rank-under-gauge (Definition 2) vs minimum rank after restriction (Definition 66) vs
  interface width (Remark 2), equivalence merely asserted ("used only as an equivalent
  characterisation"), and the two separation chains each silently fixing a different one.
- The extraction target: full sheet (Lemma 7, Theorem 223) vs activated sheet (Lemma 205) vs wired
  sheet (Lemma 206), within three consecutive sections.
- Algebrization: field-extension invariance (Theorem 197) vs oracle-does-not-touch-p (Proposition
  238) vs genuine algebraic oracles (Theorem 280), in Sections 36, 43, and L respectively.
- The NP witness: the instance's own clause sheet (Theorem 128) vs the expander-scaffolded jointPoly
  (Theorems 154/195) vs "#3SAT" in the abstract.
F5 catches the resulting half-bridge, but not the mechanism that hides it.

Proposed new mode F7, "protean surrogate" (definition drift): a load-bearing quantity is given
multiple inequivalent formal definitions in one document, and the main argument's validity depends
on switching between them at specific steps, so that any single fixed reading renders some step
false. Detection: tabulate every definition of each load-bearing term, then check which instance
each use site requires; the claim fails if the instance is not constant along the proof chain.
Candidate borderline: this can be viewed as F5 with extra steps, and the corpus may prefer to fold
it in; the practical difference is that F7 is detectable before reading any proof, at the
definition-inventory stage (here three greps, for the CEW definitions, the extraction target, and
"algebriz", suffice).

## References

- Abstract page and submission history: https://arxiv.org/abs/2512.11820
- v5 full text: https://arxiv.org/html/2512.11820v5
- v1 full text: https://arxiv.org/html/2512.11820v1
- "NP resistance under the same ρ⋆" quoted directly from v1 Section 21.7 and v5 Section 35.7
  (identical text, theorems renumbered 136→196, 137→197). An intermediate-version mirror with
  Theorem 186/187/188 numbering is at https://www.academia.edu/145195720/
- Mirrors checked for uptake (none substantive): https://pubdb.com/paper/2512.11820 ,
  https://arxiv.gg/abs/2512.11820 , https://exa.ai/library/publication/mddq6rr91g5
- pith.science entry: none (404) as of 2026-10-03.
- Section/theorem anchors quoted above: Theorem 5 and item (3) (Section 5); Definitions 1-4 and
  Lemmas 1-2 (Section 4); Theorem 12 Steps 4-5 and Lemma 13 (Section 8); Lemma 32 (Section 9);
  Lemma 33 (Section 16); Theorem 94 (Section 18); Theorems 153-155 (Section 31); Theorem 197 and
  the second chain Theorems 191/195/196 (Sections 35.6-36.1); Definition 38 and Remark 54 (Section
  25); Lemma 124, Theorem 128, Remark 85 (Sections 26-27); line-1684 CEW disclaimer; Lemma 204-206
  (Sections 38-39); Theorem 207 and Corollary 208 (Section 39); Theorem 209, Theorem 223, Lemma
  224, Definitions 54-55 (Sections 40-41); Section 43 scope, Theorems 235-236, Proposition 238,
  Remark 90; Appendix G (Definitions 65-67), Appendix I (Lean skeleton), Appendix L (Theorem 280),
  Appendix M (Theorem 281); v1 Section 21.6-22.1 (Theorems 136-137) and v1 Lemma 145-146.
