# The Magnification Gap: exact bookkeeping (verified 2026-10-03)

Source: arXiv:2503.24061 "Simple general magnification of circuit lower bounds" (2025), read
from the full PDF text saved this session. All theorem numbers below are that paper's.

## The one-sentence situation

The known unconditional lower bound for the relevant gap problem sits at exponent 2*eps - delta
for every delta > 0, and the magnification theorem needs exponent 2*eps + o(1) for one fixed
eps > 0: the entire open distance is the single step from "strictly below 2*eps" to "at 2*eps".

## The bookkeeping, precisely

- Theorem 9 (the magnification engine): NP is not contained in FML[n^c] for every c if there
  exist eps > 0 and a 2^{n^{o(1)}}-sparse problem Q in NP such that either
  (a) n^{-eps}-Q is not in FML[n^{1 + 2 eps + o(1)}], or
  (b) n^{-eps}-Q is not in PFML[n^{2 eps + o(1)}].
  Here n^{-eps}-Q is the gap relaxation of Q with more NO instances (it equals Q when
  eps(n) <= 1/n, and smaller eps means a harder problem).
- Theorem 10 (what is currently known): for every pair 0 < eps, delta <= 1,
  n^{-eps}-MCSP[2^sqrt(ell)] is NOT in PFML[n^{2 eps - delta}].
  (Hirahara-Santhanam's n^{2-delta} bound for MCSP[2^sqrt(ell)], gap-refined by the same
  pseudorandom-restriction technique; the 2025 paper redoes it one-sided for convenience.)
- Related magnifications in the same paper: Theorem 25 (crossing the threshold for MCSP[sigma]
  gives XOR-P not in NC1) and Theorems 11/27 (crossing the uniform-version threshold gives
  P != NP^{xor-P}; the threshold is "almost known" because Santhanam-Williams proved
  P is not in P-uniform-SIZE[n^c] for every c).

So for each fixed eps the known exponent is 2 eps - delta for all delta > 0, and the hypothesis
of Theorem 9(b) needs 2 eps + o(1) for some eps. The gap is the boundary case delta = 0.

## Why this wall is not an accident

1. The 2025 paper proves its own thresholds sharp: "we find it remarkable that the magnification
   threshold Theorem 9(b) obtained by our generic method turns out to be sharp." The
   distinguisher/compression method cannot be tuned past 2 eps.
2. Chen-Tell sharp-threshold results (FOCS 2020) make the wall two-sided: for the
   MCSP[(log N)^c] variants they prove that an n^{2+eps} lower bound (any eps > 0) already
   implies NP has no n^k-size formulas for all k and #SAT has no log-depth circuits. In this
   regime the last delta costs exactly as much as the final theorem, provably. The gap is not
   a margin waiting for a stronger analysis of the same technique.
3. The localization barrier blocks the obvious routes: Corollary 23 of the 2025 paper shows
   every 2^{n^{o(1)}}-sparse problem has probabilistic formula circuits of size n^{2 + o(1)}
   WITH small-fan-in oracle gates. Hence any lower-bound technique that still works in the
   presence of such oracle gates (which is what "localizing" means) can never prove the
   magnification thresholds. Known non-localizing exceptions: Santhanam-Williams'
   P-uniform argument (whose proof is non-constructive; their stated open problem is to make
   it exhibit an explicit hard problem in P) and the 2025 distinguisher method itself.

## The precise open target, then

Unconditional target (non-uniform): exhibit ANY 2^{n^{o(1)}}-sparse problem Q in NP and a
fixed eps > 0 with n^{-eps}-Q not in PFML[n^{2 eps + o(1)}].
- Inventory check (from the paper): no explicit 2^{n^{o(1)}}-sparse problem is known outside
  FML[n^2]; the best sparse-case bounds sit at PFML[n^{2-delta}] (Theorem 10 above).
- The required technique must be non-localizing, must handle probabilistic formulas with
  two-sided or one-sided error, and must beat the sharpness of the distinguisher method.
Uniform cousin (arguably closer to P vs NP itself): n^{-eps}-MCSP[sigma] not in
P-uniform-SIZE[n^{1 + eps + o(1)}] for some eps and sigma <= 2^{o(ell)} (Theorem 27), against
the Santhanam-Williams lower bound P not in P-uniform-SIZE[n^c] which is known but
non-constructive and does not cover MCSP variants.

## Candidate directions, ranked by fit to the constraints

1. Constructivize Santhanam-Williams: their P-uniform lower bound is the only known technique
   that is simultaneously super-linear, non-localizing, and proven; the full assessment is the
   next section (short version: the port to MCSP-type problems is blocked by an unmet
   prerequisite - no super-linear lower bound of any kind for MCSP-type problems is known).
2. Compression/antichecker route (Allender-Koucky lineage, strengthened by the Lipton-Young
   antichecker construction used in the proof-complexity magnification): the 2025 paper notes
   the antichecker proof does not obviously localize; pushing it from almost-formulas to
   probabilistic formulas at sparse problems is open.
3. Kt/meta-complexity variants (MKtP gap problems): the Oliveira-Pich-Santhanam FOCS 2019
   program shows EXP not in NC1 from MKtP gap bounds at N^{2+eps}/N^{3+eps} in restricted
   models where known bounds are N^{3-o(1)} (average-case, explicit problems); here too the
   known exponents press against the needed ones from below.

## Constructivization assessment: Santhanam-Williams (added 2026-10-03)

Source: Santhanam-Williams, "On Medium-Uniformity and Circuit Lower Bounds" (CCC 2013;
Computational Complexity 23, 2014), read via the full PDFs of that paper, its CCC 2017
follow-up ("Easiness Amplification and Uniform Circuit Lower Bounds"), and the bounded-
arithmetic follow-up (Krajicek-Oliveira 2017). Correcting one slip in `williams_ladder.md`
context: the result is from CCC 2013/CC 2014, not FOCS 2021.

The theorem: for every k, P is not contained in P-uniform SIZE(n^k); i.e., there is L in P
whose n^k-size circuits cannot be generated in polynomial time.

The mechanism (indirect diagonalization):
1. Proposition 1: DTIME(n^{d+1}) is not in DTIME(n^d)/n (time hierarchy against sublinear
   advice, proved by the trick of using the input itself as its own advice).
2. Assume P is in P-uniform SIZE(n^k). Take any L in P. Its direct connection language L_dc
   is in P, so it also gets n^k circuits (the assumption is applied a second time, to L_dc).
3. Pad the direct-connection tuples into a succinct language L_succ of length n^{1/(3k)}
   (the padding exponent is what balances the two applications).
4. Net effect: every L in P is simulated in DTIME(n^{2k+2})/O(n^{1/2} log n), contradicting
   Proposition 1. The hard language is the advice-hierarchy language: pure contradiction
   artifact.

Documented drawbacks (stated verbatim in the CCC 2017 follow-up):
- "Extreme non-constructivity": no particular problem in P is known to exhibit the lower
  bound; the proof does not even give an explicit time exponent for such a problem.
- "It relativizes, which implies that there are hard barriers to what it can possibly prove.
  In particular, we cannot expect to prove results like P not in SIZE[O(n)] via such
  techniques."

What the magnification threshold needs (Theorem 27 of arXiv:2503.24061):
n^{-eps}-MCSP[sigma] not in P-uniform-SIZE[n^{1+eps+o(1)}] for one fixed eps and
sigma <= 2^{o(ell)}, which would give P != NP^{xor-P}.

The porting blocker, made precise this turn: SW14's argument is problem-agnostic in its
hypothesis (arbitrary L in P gets simulated) but its conclusion is existence-only; the hard
language is constructed from the advice-hierarchy. To replace it by MCSP, one must first
show that MCSP (or the gap variant) cannot be simulated in DTIME(n^{1+o(1)}) with o(n)
advice - and NO super-linear time lower bound of any kind is known for MCSP today (its
uniform time complexity is wide open: it could in principle be n^{1.01} for all we know).
So constructivization decomposes into two open problems, each at frontier level:
(1) any super-linear (time or circuit) lower bound for a natural meta-computational problem
    in P, and
(2) a version of the two-application uniformity trick whose surviving hard language is that
    specific problem rather than a hierarchy artifact.

Signs of life around it:
- Krajicek-Oliveira 2017 formalized the SW14 argument in bounded arithmetic (PV) and showed
  the natural-problem versions resist their method: "it is not clear how to establish
  [them] using only the soundness of PV"; the non-constructivity is intrinsic there too.
- The constructivization question now has its own literature with both signs: Chen-Jin-
  Santhanam-Williams (TheoretiCS 2024) show constructivizing many known separations would
  imply breakthrough lower bounds, and that some separations cannot be constructivized at
  all; Carmosino-Grosser (ECCC TR25-045, 2025) generalize to Student-Teacher refutation games
  and prove, e.g., that a P-Student-Teacher constructive separation of Palindromes from
  one-tape nondeterministic n^{1+eps} time would imply NP not in SIZE[n^k] for all k, and
  that certain high-Kolmogorov-complexity generation protocols provably do not exist. Net
  effect on this route: constructivization is quantifiably potent (each success implies
  breakthroughs) and provably blocked in several regimes - the wall is bidirectional.
- Carmosino-Krajicek-Koloupis-Oliveira 2021 (LEARN-uniform circuits) strengthened SW14 to
  learners with equivalence queries via a "query elimination" lemma and a "compressible
  counterexample" hierarchy theorem - an explicit-witness mechanism that partially answers
  the constructivity complaint, though still for artificially defined languages.
- The CCC 2017 easiness-amplification paper gives the best candidate natural problem: the
  Circuit-Composition problem (in TISP[n^{1+eps}, O~(n)]), conjectured to need super-linear
  circuits even non-uniformly, with proven consequences in both directions (Lemma 4: if it
  has nearly-linear circuits then every TISP[n^k, O~(n)] problem does). They also proved
  TIME[n^{1+eps}] is not in LOGSPACE-uniform SIZE[O(n)] by a non-relativizing argument -
  the one breach of the relativization barrier in this neighborhood - and recorded the
  equivalences P not in SIZE[O(n)] iff P not in P^{Sigma2P}-uniform SIZE[O(n)].

Updated judgment for the ladder: Theorem 11/27 of the 2025 magnification paper is
"almost known" in the sense that the target class (P-uniform circuits) admits proven
super-linear separations; but the known technique's hard language is a hierarchy artifact,
its proof relativizes, and the natural-problem prerequisite (any super-linear lower bound
for MCSP-type problems, even uniform-time) is itself open. The single most valuable concrete
problem on this route is the Circuit-Composition problem's P-uniform (ideally non-uniform)
super-linear lower bound, which by easiness amplification would radiate consequences across
TISP and, via the 2025 magnification theorems, toward the P vs NP frontier.


## Screening note (2026 claims, this session)

No magnification-adjacent breakthrough found. A September 2026 screen of new P vs NP claims
surfaced only: an LLM self-audit framework ("Trisduction Engine", certified on philarchive,
self-described as non-deductive and explicitly "not a proof"), a graph-based P = NP preprint
now at Zenodo v7 after 7 versions since January 2026 (its "local infeasibility trimming" step
would have to decide whether partial certificates extend to accepting ones, which is the
original problem), a claimed "upgrade" of monotone CLIQUE lower bounds to deterministic
computation (Preprints.org; lifting monotone bounds past Razborov-Rudich is precisely the
blocked move), and two meta-records that explicitly claim nothing. Details in LOG.md.

## Screen (2026-10-03, frontiers monitor; full detail in `monitor_frontiers_2026-10-03.md`)

Verdict: the sharp 2eps wall and the constructivization porting blocker are UNTOUCHED.
- Atserias-Muller magnification paper (arXiv:2503.24061): zero OpenAlex citations; no
  follow-up crosses or relaxes the Theorem 9(b)/10 boundary.
- New context only: Atserias-Muller, "From Godel incompleteness to the consistency of
  circuit lower bounds" (arXiv:2604.25251) magnifies PROOF-hardness in bounded arithmetic,
  not circuit lower bounds (does not touch PFML thresholds); Carmosino-Juvekar parallel
  Kolmogorov complexity (TR26-176); Hsieh-Jain-Li-Mathialagan padding-via-certification
  (FOCS 2026). TISP/Circuit-Composition: zero arXiv activity; the self-declared most
  valuable concrete problem remains open.
- Venue note: Korten's top-down lower bounds (in-corpus arXiv:2609.38677) now ECCC
  TR26-221.
