# P ?= NP: Clue Dossier

Date: 2026-10-03
Companion files: `LOG.md` (working log), `sat_scaling.py` (experiments).

## 1. Verdict

P versus NP is open as of October 2026. I did not prove or disprove it.
No one has: every claimed resolution found in this investigation was either refuted within days
or has no community validation. What follows is the attempted proof log, the walls each attempt
hits, fresh forensics on the 2025-2026 claims, two experiments, and the resulting evidence
balance sheet. My position, stated up front: P != NP with about 93% confidence, where the
confidence is empirical and not a proof.

## 2. The frame everyone must work in (what is actually provable today)

- Cook-Levin: SAT is NP-complete, so $\mathrm{P} = \mathrm{NP}$ iff $\mathrm{SAT} \in \mathrm{P}$ iff every NP problem has poly circuits
  (nonuniform version: $\mathrm{NP} \subseteq \mathrm{P/poly}$).
- Time hierarchies: P is properly inside EXPTIME and NP is properly inside NEXP.
  Separating deterministic classes by diagonalization works; nondeterminism is exactly what
  breaks the argument.
- Ladner: if $\mathrm{P} \neq \mathrm{NP}$ then intermediate problems exist. Mahaney: no sparse NP-hard sets under
  many-one reductions unless $\mathrm{P} = \mathrm{NP}$.
- Karp-Lipton: $\mathrm{NP} \subseteq \mathrm{P/poly}$ collapses PH to its second level. So $\mathrm{SAT} \notin \mathrm{P/poly}$ would
  immediately give $\mathrm{P} \neq \mathrm{NP}$, but that lower bound is itself open.
- Kannan: for every fixed $k$, $\Sigma_2^{\mathrm{P}}$ contains functions requiring circuit size $n^k$.
- Best unconditional "class" separations of the relevant kind: $\mathrm{NEXP} \notin \mathrm{ACC}^0$
  (Williams, 2010) and $\mathrm{NEXP} \notin \mathrm{ACC}^0 \circ \mathrm{THR}$ (Murray-Williams, 2018).
  Even $\mathrm{NEXP} \notin \mathrm{TC}^0$ (depth-2 threshold circuits!) is open.
- Best explicit general Boolean circuit lower bound: about $3.1n$ gates (Find 1984, Iwama-Lachish
  2002 line). Shannon counting shows almost all functions need about $2^n/n$ gates.
  The entire difficulty of P vs NP lives in the explicit-versus-random gap.
- Algebraic circuits: Limaye-Srinivasan-Tavenas (FOCS 2021) proved the first super-polynomial
  lower bounds for all constant-depth algebraic circuits. This is the one notable crack of
  daylight in decades, and it is still constant depth.
- Proof complexity: resolution (Haken 1985) and constant-depth Frege (Ajtai and others) have
  exponential lower bounds; Frege and extended Frege are open.
  $\mathrm{NP} \neq \mathrm{coNP}$ implies $\mathrm{P} \neq \mathrm{NP}$; a p-bounded propositional proof system exists iff $\mathrm{NP} = \mathrm{coNP}$.
- The three named barriers any proof must dodge:
  1. Relativization (Baker-Gill-Solovay 1975): oracle A exists with $\mathrm{P}^A = \mathrm{NP}^A$ (A PSPACE-complete)
     and oracle B with $\mathrm{P}^B \neq \mathrm{NP}^B$. Any relativizing argument proves both, hence neither.
  2. Natural proofs (Razborov-Rudich 1994): a property of Boolean functions that is
     poly-time-checkable on truth tables, large, and useful for lower bounds against P/poly
     would break pseudorandom generators. Conditioned on PRGs (essentially AES), no such proof
     of $\mathrm{SAT} \notin \mathrm{P/poly}$ can exist.
  3. Algebrization (Aaronson-Wigderson 2008): extends relativization to arithmetization-based
     techniques. Both $\mathrm{P} = \mathrm{NP}$ and $\mathrm{P} \neq \mathrm{NP}$ have algebrizing "proofs" relative to suitable oracles.
- There are oracles with $\mathrm{P}^A \neq \mathrm{NP}^A$ yet $\mathrm{NP}^A \subseteq \mathrm{P}^A/\mathrm{poly}$, so P vs NP and the circuit
  lower bound route are genuinely different questions relative to oracles. Any proof of the
  latter must be non-black-box in a strong sense.

## 3. Attack log: five attempts and the wall each one hits

### Attack 1: Diagonalization (try to build a language in NP outside P)
Idea: enumerate polynomial-time machines with clocks and diagonalize.
What breaks: deciding the diagonal language for NP needs witnesses of unbounded structure, and
the resulting argument relativizes. Baker-Gill-Solovay supplies oracle worlds with $\mathrm{P}^A = \mathrm{NP}^A$,
so the argument cannot work in the unrelativized world either.
Verdict: dead on arrival, and instructive: the time hierarchy proves $\mathrm{P} \neq \mathrm{EXPTIME}$ by the same
machinery, so the missing ingredient is specifically nondeterminism.

### Attack 2: Effective counting (circuit lower bound via a checkable property)
Idea: Shannon's counting argument shows hard functions exist; make the hard property
constructive so it applies to SAT's truth tables.
What breaks: checkable + large + useful is exactly the natural-proofs template, blocked by
Razborov-Rudich assuming PRGs. Quantitatively it is also hopeless: the record explicit lower
bound is $3.1n$, and the target is super-polynomial.
Verdict: dead for now; only properties outside the natural template (e.g., Williams' $\mathrm{ACC}^0$
argument, which uses the class's own structure) have ever worked.

### Attack 3: Algebraic route (permanent vs determinant, GCT)
Idea: VP vs VNP is the algebraic P vs NP; prove perm needs super-poly algebraic circuits.
Status: alive but far, and now fully mapped at the walls (see `algebraic_rung.md`): LST 2021
(JACM 2025) delivered constant-depth bounds, but the Tavenas depth-reduction chasm means
constant-depth bounds below $2^{\omega(\sqrt{n})}$ can never reach VP vs VNP; the shifted-partial-
derivative technique behind all depth-4 records provably cannot separate perm from det; GCT's
occurrence obstructions are no-go'd in both the padded and padding-free formulations; the
symmetric world is fully separated ($\mathrm{symVF} < \mathrm{symVS} < \mathrm{symVP}$, STOC 2026) but the symmetry
restriction is exactly what general circuits escape.
Verdict: alive via multiplicity obstructions, debordering, and unknown techniques; every named
sub-route now has a documented wall.

### Attack 4: Proof complexity (separate Frege, get NP != coNP)
Idea: exhibit tautologies needing super-poly Frege proofs; NP != coNP follows, hence P != NP.
What breaks: even $\mathrm{NC}^1$-Frege lower bounds are open; the known techniques hit natural proofs
again at the truth-table level.
Verdict: open; pigeonhole is settled only for resolution and constant-depth Frege.

### Attack 5: Find the algorithm (argue the P = NP side)
Idea: heuristics keep improving; maybe $\mathrm{SAT} \in \mathrm{P}$ with a big constant.
What breaks: the experiments below show average-case ease, but planted and random structure is
not worst case; the entire fine-grained complexity web (SETH, no $(2-\epsilon)^n$ for CNF-SAT,
 hardness magnification) is coherent only under worst-case hardness. $\mathrm{P} = \mathrm{NP}$ would also imply
$\mathrm{PH} = \mathrm{P}$ (trivially, $\mathrm{P}^{\mathrm{NP}} = \mathrm{P}$) and would kill one-way functions, hence all of modern cryptography.
Verdict: no trace of such an algorithm after 55 years; every near miss was withdrawn or refuted.

## 4. Forensics on claimed resolutions found this session (2025-2026)

- Arthanari, "Lean 4 machine-verified proof of P = NP" (arXiv:2606.03194, Jun 2026). REFUTED.
  The repo's own issue #1, opened one day after submission: the main theorem proves `True`,
  not $\mathrm{P} = \mathrm{NP}$. The chain from M3P to $\mathrm{P} = \mathrm{NP}$ rests on six axioms including Cook's and Karp's
  theorems as assumptions; the necessity half of the membership characterization sits in a
  backup file with 16 sorries. "Zero sorries in the main chain" was technically true and
  completely misleading. Community consensus formed within 24 hours.
- Ke Xu and Guangyan Zhou, $\mathrm{P} \neq \mathrm{NP}$ (Frontiers of Computer Science, 2025). Multiple independent
  flaw reports; no accepted defense; journal attached expert comments instead of certifying it.
- Deng, $\mathrm{P} = \mathrm{NP}$ via SDP for degree-4-bounded 3-coloring (2024). Refuted: conflates subgraphs
  with induced subgraphs.
- Petros, $\mathrm{P} \neq \mathrm{NP}$ via self-referential CNF (SSRN 2025). Claims to defeat all three barriers
  simultaneously; no community uptake; classic red flag pattern.
- Edwards, "Observer-Theoretic Separation via SPDP Rank" (arXiv:2512.11820, v1 Nov 2025 -
  v5 Jan 2026, 208 pages). REFUTED by session audit; full writeup in `edwards_audit.md`.
  The bridging extraction map exists in three published forms naming three different
  output polynomials (Lemma 7/205/206); the paper's own Lemmas 204+224+124 are jointly
  inconsistent (its instrumented solver must contain an $n^{\Theta(\log n)}$-rank sheet,
  falsifying its own P-side bound); one side of every reading collapses quantitatively.
  First instantiation of failure mode F7 (protean surrogate / definition drift). Fairness:
  its rank-bookkeeping theorems (94/128/236/280) are correct-looking on their own terms.
- "Weakness quantale" $\mathrm{P} \neq \mathrm{NP}$ (arXiv:2510.08814, Ben Goertzel; v1 Oct 2025, v2 22 Apr 2026).
  REFUTED by session audit; full writeup in `goertzel_audit.md`. Two quote-anchored findings.
  (1) Internal parameter conflict: Sections 3.1, 3.6 and 7.4 fix the VV parity matrix at
  $k = c_1 \log m$ (matching the $O(\log m)$ per-bit label budget of Definition 2.10), but Lemma 2.12's
  $\Omega(1/m)$ isolation bound needs $k$ uniform over $\{0, \ldots, m-1\}$, i.e. $\Theta(m)$ rows for instances with
  $2^{\Theta(m)}$ solutions. With $k = c_1 \log m$ the uniqueness event has double-exponentially small
  probability, so the ensemble is not efficiently samplable; with $k = \Theta(m)$ every downstream
  $O(\log m)$ input budget collapses (Def 2.10, Thm 4.2, Lemma 2.15, A.4).
  (2) Trilemma in the switching lemma (Theorem 4.2): exact success domination, per-bit locality
  on a constant fraction of blocks, and Lemma 2.15's small advantage for $O(\log m)$-input functions
  are jointly inconsistent when P is the $\mathrm{P} = \mathrm{NP}$ solver: symmetrization of the solver returns the
  witness bit exactly on every block (Lemma 4.3's measure preservation), and by the paper's own
  neutrality lemma that bit is not a function of the local view. The argument must apply to that
  decoder, so no repair within this framework proves $\mathrm{P} \neq \mathrm{NP}$.
- Topological argument that $\mathrm{P} = \mathrm{NP}$ implies $\#\mathrm{P} = \mathrm{FP}$ (arXiv:2603.22211, Mar 2026). Its advertised
  novelty, $\mathrm{P} = \mathrm{NP}$ implies $\mathrm{PH} = \mathrm{P}$, is folklore ($\mathrm{P}^{\mathrm{NP}} = \mathrm{P}$). The empirical shattering measurements
  are fine; the exhaustive dichotomy step ("local information is provably useless") is where it
  should fail. Not a separation proof in any case.
- Historical base rate: Deolalikar 2010 (rejected within days), Blum 2017 (withdrawn).
  The claim rate itself is a clue: outsiders can produce candidate arguments, so the problem is
  not remote; it is exactly tuned to resist the arguments humans produce.

## 5. Experiments (sat_scaling.py, xor_hardness.py)

Setup: naive DPLL with unit propagation, pure literal elimination, max-occurrence branching.
Node cap per instance; medians over multiple instances per size.

- Random 3-SAT at clause ratio 4.26 (threshold region): median nodes 7-15, flat through $n=26$;
  max 57. Typical instances fall in microseconds.
- Random 3-XOR systems, planted, over-determined, Tseitin-encoded: at every density $\alpha$ in
  1.2..3.2 and $n$ up to 80, GF(2) elimination shows unsat cores of only 8-34 rows, and the truly
  unsatisfiable instances are refuted in 7-31 nodes at $n \leq 32$. A correction to the first run of
  this experiment: I had labeled this family "the regime where resolution is provably
  exponential", and that was wrong at these parameters. Random triples at feasible n do not
  deliver the expansion that Ben-Sasson-Wigderson hardness needs; cores stay small, and unit
  propagation effectively performs the linear algebra.
- Pigeonhole $\mathrm{PHP}^{h}_{h+1}$: 1439 nodes at h=6 (42 variables), 80639 nodes at h=8 (72
  variables), and above the 150000-node cap at h=10 (110 variables): a measured growth factor
  of $56\times$ per +2 pigeons and still super-linear beyond the cap. The blowup appears exactly
  where Haken's resolution lower bound predicts.

Clues from the three-family contrast:
1. The average-case/worst-case split is the entire content of P vs NP. Heuristics demolish
   random structure at every scale tested, in every random family, at every density.
2. Every exponential lower bound we can exhibit is against a restricted model (here:
   resolution/DPLL), and the canonical such family admits a trivial polynomial side-channel
   algorithm: to decide a PHP instance, count pigeons and holes. This is the precise shape of
   the open problem: no family of SAT instances is known where all polynomial-time algorithms
   provably fail. Exhibiting one would require an explicit function lower bound beyond $\sim 3.1n$,
   which has not moved in about 40 years.
3. Feasible-scale experiments cannot witness $\mathrm{P} \neq \mathrm{NP}$: provable hardness (PHP) becomes visible
   only where theory says to look, and no experiment can rule out an unrestricted-model
   algorithm. Proofs are the only known way forward.

## 6. Evidence balance sheet

For $\mathrm{P} \neq \mathrm{NP}$:
- 55 years with zero polynomial algorithms for any NP-complete problem, despite enormous effort
  and money (worst-case crypto has strong incentives).
- Circuit complexity progress is glacial: $3.1n$ for explicit functions; $\mathrm{NEXP} \notin \mathrm{ACC}^0$ took
  until 2010 and needed the algorithmic method; $\mathrm{TC}^0$ remains out of reach.
- Every oracle world we can build consistent with our techniques allows separation; the barriers
  tell us why: our techniques are too weak, not the separation false.
- Existence of one-way functions (the empirical success of cryptography) implies $\mathrm{P} \neq \mathrm{NP}$.
- Fine-grained complexity (SETH and hundreds of conditional results) is a self-consistent web
  only under hardness; a single $\mathrm{P} = \mathrm{NP}$ collapse would demolish it.
- Expert consensus: in the most recent published poll (Gasarch 2019) about 88% of
  complexity theorists chose $\mathrm{P} \neq \mathrm{NP}$.

For P = NP:
- Complexity theory has produced shocking collapses before ($\mathrm{IP} = \mathrm{PSPACE}$, $\mathrm{MIP} = \mathrm{NEXP}$, PCP),
  so "obviously different" is not a proof.
- Random and average-case instances are easy in practice (confirmed by experiment above);
  if the world's SAT instances were all like these, $\mathrm{P} = \mathrm{NP}$ would barely matter practically.
  No one, however, has ever exhibited a worst-case polynomial algorithm even for parity or
  structured-tail instances.
That second list is short, and none of it is evidence of equality; it is only evidence that
intuitions fail.

## 7. The live frontier (where the next genuine clue will come from)

1. Williams' algorithmic method: any $2^n / n^{\omega(1)}$ Circuit-SAT analysis algorithm for
   NEXP-computable functions gives $\mathrm{NEXP} \notin \mathrm{P/poly}$. Slightly faster k-SAT, Max-IP, or LWS
   algorithms would already push past $\mathrm{ACC}^0 \circ \mathrm{THR}$ toward $\mathrm{TC}^0$. This is the single most
   concrete ladder.
2. Any super-linear explicit lower bound for general circuits (the $3.1n$ stall has held for
   about 40 years).
3. Hardness magnification: proving $n^{1+\epsilon}$ lower bounds for MCSP-like or sufficiently sparse
   NP problems would imply $\mathrm{NEXP} \notin \mathrm{P/poly}$. The 2025 general magnification results put
   thresholds within a hair of known lower bounds, so this frontier may move first.
4. Algebraic: extend LST-style bounds beyond constant depth; perm vs det; GCT obstructions
   past the known low-degree failures.
5. Proof complexity: any super-polynomial Frege lower bound would unlock the $\mathrm{NP} \neq \mathrm{coNP}$ route.
6. Meta-computational complexity: lower bounds for MCSP are candidates to bypass natural
   proofs, since the property is about computation rather than combinatorics.
7. Independence meta-results: some weak theories cannot prove certain lower-bound statements;
   the claim "P != NP is provable in PA" (arXiv:2005.10080) remains unvalidated. Where the
   statement sits between provable and independent is itself an open clue surface.

Update (verified 2026-10-03, details and sources in `williams_ladder.md`):
- Chen-Tal-Wang (STOC 2026, ECCC TR26-039): first superquadratic $\mathrm{THR} \circ \mathrm{THR}$ lower bounds,
  $n^{2.5-\epsilon}$ for a function in $\mathrm{E}^{\mathrm{NP}}$, via Williams' method (acceptance-probability estimation
  in $2^{n - n^{\Omega(\epsilon)}}$). The known blocker for the next rung is OR-closure: no one knows
  how to convert an OR of $\mathrm{THR} \circ \mathrm{THR}$ circuits into one $\mathrm{THR} \circ \mathrm{THR}$ circuit.
- Top-down lower bounds completed for all constant depths (arXiv:2609.38677): parity needs
  $\exp(\epsilon_d n^{1/(d-1)})$ size at depth $d$; notable as an explicit human+machine collaboration.
- Unconditional natural-proofs barrier for AC0 (arXiv:2606.12631): the Switching Lemma itself
  proves AC0-natural properties cannot exceed the Switching-Lemma frontier.
- Magnification thresholds are proven sharp (arXiv:2503.24061, 2025) and sit just above known
  bounds: $\mathrm{MCSP}[2^{\sqrt{\ell}}] \notin \mathrm{PFML}[n^{2-\delta}]$ for all $\delta$ is known; one fixed-eps
  crossing would give $\mathrm{NP} \notin \mathrm{P/poly}$. The exact epsilon bookkeeping of this wall, why it is
  provably not crossable by the current technique family (sharpness + Chen-Tell sharp
  thresholds + the localization barrier of Corollary 23), and the ranked candidate directions
  are in `magnification_gap.md`.

## 8. Answer to the question

Not provable or disprovable with current mathematics. The five attacks above each terminate at
a named wall (relativization, natural proofs, algebrization, open proof-complexity frontiers),
and the empirical route confirms hardness only asymptotically, which experiments cannot see.
The rational working conclusion, consistent with everything gathered here: $\mathrm{P} \neq \mathrm{NP}$.
The confidence is inductive, the way most of mathematics believed Fermat's Last Theorem for
350 years before a proof arrived. The clues that would change my mind, in order of likelihood:
a $\mathrm{TC}^0$-level lower bound via Williams' program, an MCSP magnification threshold crossing, or a
genuinely poly-time algorithm for a structured-tail family that resists all reductions.
