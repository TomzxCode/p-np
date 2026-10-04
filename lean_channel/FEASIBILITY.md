# FEASIBILITY: Lean 4 (mathlib) formalization of the surviving p = 2 channel results

Deliverable: `LeanChannel.lean` in this directory (`/home/tomzx/pnp/lean_channel/`).
Date: 2026-10-03/04. Author: formalization subagent (re-dispatch; the first attempt
died of a rate limit before doing any work).

**FINAL STATUS: the file compiles.** `lake build` ends with
`Build completed successfully (8925 jobs).` — 0 errors, 9 intended `sorry`-warnings
(listed under Residual gaps). Lean 4.34.1 + mathlib @ tag v4.34.1.

## Toolchain status

* This machine is a shared laptop whose ~97 GB root filesystem was **100% full**
  (35 MB free) at session start. To make room, only regenerable caches were deleted:
  `~/.cache/go-build`, `~/.cache/uv`, `~/.cache/electron`, `~/.cache/ms-playwright`,
  `~/.npm/_cacache`, the Go module cache (`go clean -modcache`), the pnpm store, apt
  .debs, `~/.cache/ghx`, `~/.cache/hyperframes`, tectonic caches. No user data was
  touched. ~12 GB was reclaimed this way; ~4-5 GB is in steady use by this project
  (toolchain 2.4 GB, mathlib sources 0.5 GB, mathlib+deps oleans ~5 GB).
* elan installed under `/tmp/opencode/elan` (local prefix), toolchain
  `leanprover/lean4 v4.34.1`. Mid-session the disk filled during the mathlib cache
  download, a failed extraction left the toolchain half-installed, and it was
  resurrected by manually extracting the release tarball (including
  `lib/libLLVM.so.22.1`, needed by `leanc`) into elan's toolchain directory.
* mathlib is a shallow clone of tag `v4.34.1` at `mathlib4/` inside the project.
  `lake update` resolves the dependency tree; the dependency oleans (batteries, aesop,
  Qq, proofwidgets, ...) are built from source by lake; the `Mathlib.*` oleans come
  from the mathlib cache server (`lake exe cache get`). Note: `lake update` itself
  runs a post-update hook that already fetches the cache.
* Ecosystem note: in this Lean version `Finset`/`Multiset` live in **Mathlib** (they
  were removed from Batteries during the module-system migration). A mathlib-free
  build of this material is impractical; the mathlib dependency is required.
* Caveat: a sibling agent working in `/home/tomzx/pnp` deleted the `mathlib4/`
  directory once mid-session to free disk (the corpus files were unaffected). If it
  disappears again: re-clone (`git clone --depth 1 --branch v4.34.1`), `lake update`
  (which re-fetches the olean cache automatically), `lake build`.

## What is formalized (all proved unless listed as a gap)

Everything that survives the 2026-10-03 correction
(`two_phase_tree.md` MAJOR CORRECTION + `proof_complexity.md` CORRECTION BLOCK +
`cert_floor.md`):

1. **Pair-status model + counting lemma** (task item 1): `Status` (free/matched/
   killed), partial-injection model `mu : Fin (n+1) -> Option (Fin n)`, the
   `AnswerTable` structure packaging the two determined channel-law values
   (matched -> 1, killed-unmatched -> 0), and:
   * `killed_row_singleton` / `killed_col_singleton` — **Lemma 3 of cert_floor.md**,
     both halves: killed rows/columns of the answer table contain exactly one 1;
   * `cert_row_free` / `cert_col_free` / `cert_c_row` / `cert_c_col` — the sound
     counting certificates (a), (b), (c);
   * `pigeonhole_rescue` — **Lemma 4 of cert_floor.md**;
   * shape theorems `freePigeons_card` (2d+1) and `freeHoles_card` (2d).
2. **F_2 linearity lemma** (task item 2): `Design` packages an F_2-linear answer
   functional `L : (Pair n -> ZMod 2) ->+ ZMod 2` with `L(1) = 1` and the kernel's
   determined killed-unmatched values; `lemma1` proves
   `ansL f = f.const + Σ_{p ∈ f.support} M p` — every degree-1 answer is an F_2
   function of the variable-answer table `M = MofL`; `answerTableOfL` shows the model
   satisfies the Section-1 channel hypotheses.
3. **Single-variable channel law, deterministic halves** (task item 3):
   `MofL_matched` (matched -> 1), `MofL_killedP` / `MofL_killedH` (killed-unmatched
   -> 0), `MofL_free` (free -> design bit). The probabilistic half (fair coins) is
   Section 6, see gaps.
4. **Full-scan dominance** (task item 4, first half): `DTree`/`DTree.run`/
   `DTree.pathQueries`, the scan-tree constructor `scanSim` (one singleton query per
   pair, `scanSim_queries`: n(n+1) queries), and:
   * `scanSim_correct` — the scan-tree's output equals the adaptive tree's output for
     EVERY answer table (Lemma 1 replay, proved);
   * `scanSim_nonadaptive` — its query path is M-independent (proved);
   * `corollary_two` — **Corollary 2 of cert_floor.md** in tree form (proved);
   * `corollary_two_errOf` — the same at the level of error probabilities under the
     uniform configuration ensemble (proved).
5. **F_2 linear-algebra fragment** (task item 3): `exists_free_coords` (pivot/
   free-coordinate decomposition — the structural content of RREF existence; mathlib
   has no literal RREF) — statement, `sorry`; `kernel_basis_disjoint` — the
   kernel-basis disjoint-support property on free coordinates — **proved** (given the
   decomposition; needs no linearity).
6. **Channel law, probabilistic half** (Section 6): `coinTable`/`coinPMF` model the
   proved law as the corpus's simulators implement it; the five `ansPMF_*` theorems
   state matched/killed determinism and free-pair fair coins + independence as PMF
   identities — `sorry` (see gaps).
7. **Optimality chain** (task item 4): `configPMF`/`errOf`/`bayesErr`/`errStar` and
   `theorem_F` (the exact 2^{-Theta(d^2)} floor of cert_floor.md),
   `floor_lower_bound`, `counting_tree_attains` — stated with err*'s exact formula,
   `sorry` as permitted by the task ("state, proof optional, clearly marked").

Deliberately absent (retracted by the correction): Theorem T of two_phase_tree.md,
Proposition D of proof_complexity.md, any 2^{-Theta(d)} claim.

## Exact build output

```
$ cd /home/tomzx/pnp/lean_channel
$ export PATH=/tmp/opencode/elan/toolchains/leanprover--lean4---v4.34.1/bin:$PATH
$ lake build
warning: LeanChannel.lean:624:8: declaration uses `sorry`
warning: LeanChannel.lean:680:8: declaration uses `sorry`
warning: LeanChannel.lean:684:8: declaration uses `sorry`
warning: LeanChannel.lean:688:8: declaration uses `sorry`
warning: LeanChannel.lean:692:8: declaration uses `sorry`
warning: LeanChannel.lean:697:8: declaration uses `sorry`
warning: LeanChannel.lean:800:8: declaration uses `sorry`
warning: LeanChannel.lean:804:8: declaration uses `sorry`
warning: LeanChannel.lean:811:8: declaration uses `sorry`
Build completed successfully (8925 jobs).
```

(Plus deprecation warnings for `if_pos`/`if_neg`/`push_neg` — informational only.
The nine `sorry`-warnings are exactly the intended gaps below.)

## Residual gaps (exact)

1. `exists_free_coords` (line ~624): pivot/free-coordinate decomposition existence.
   Proof sketch: induct on `finrank` (or split coordinates via
   `LinearEquiv.piFinSucc`), peeling one kernel vector per step.
   Estimated 150-300 lines of mathlib tactic work.
2. `ansPMF_matched/killedP/killedH/free/indep` (lines ~680-697): fiber-counting over
   `PMF.uniformOfFintype` (the key count: `{k // k p = b}` has cardinality
   `2^(m-1)`, e.g. via the fixed-point-free involution `Function.update k p !!(k p)`).
   Estimated 100-200 lines.
3. `theorem_F` / `floor_lower_bound` / `counting_tree_attains` (lines ~800-811):
   Lemma 5's counting (class b: (2d+1)·(2d)! near-permutations, Bayes-flat posterior
   2d/n) plus the Bayes-audit bookkeeping. Estimated 500-1000 lines. This is the
   natural next milestone.
4. The arXiv paper's degree-d design itself (existence + kernel structure) remains
   the corpus's own open fidelity task (`kernel_structure`); here it appears as the
   hypotheses of `Design` plus the abstract `kernel_basis_disjoint`.

## Effort estimate (honest)

* This session: environment resurrection on a full disk (~2 h), ecosystem
  reconnaissance (Finset-lives-in-Mathlib discovery; mathlib cache plumbing) (~1.5 h),
  formalization to the compiling state above (~3 h of edit/build iterations).
* Remaining sorries: `exists_free_coords` ~0.5-1 day; PMF channel law ~0.5-1 day;
  Theorem F end-to-end ~3-7 days for someone fluent in mathlib's finite-set and
  combinatorics API. None needs new mathematics.

## Reproduction

```
cd /home/tomzx/pnp/lean_channel
export PATH=/tmp/opencode/elan/toolchains/leanprover--lean4---v4.34.1/bin:$PATH
lake build
```

(elan lives under /tmp/opencode, which is session-scoped; a fresh machine would
install elan normally. ~6 GB free disk is needed during the mathlib cache download,
~5 GB at rest.)

## Notes on other files in this directory

`CoreChannel.lean` was created by a sibling agent (core-Lean-only, covering the
channel-law answer function and the row-half counting lemma). This file
(`LeanChannel.lean`) is the mathlib deliverable and goes substantially further
(counting certificates in full, Lemma 1, Corollary 2 in tree form with an explicit
non-adaptive scan-tree, disjoint support, PMF statements, Theorem F statement).

## Working environment (re-verified 2026-10-04; moved out of /tmp same day)

elan now lives at its DEFAULT home, /home/tomzx/.elan (moved from
/tmp/opencode/elan on 2026-10-04, which was volatile and space-contested).
The only setup needed in a shell is the PATH line, already appended to
~/.bashrc:

    export PATH="$HOME/.elan/bin:$PATH"

No ELAN_HOME is required any more (elan defaults to ~/.elan).

State re-verified from scratch on 2026-10-04:
- lean --version: 4.34.1 (toolchain at /home/tomzx/.elan/toolchains/).
- mathlib olean cache: 8548 modules under lean_channel/mathlib4/.lake/ (inside
  the clone - the cache-get ran with the clone as the package). Missing 564 are
  Archive.*/Counterexamples.* only; the `import Mathlib` closure is complete.
- lake env lean CoreChannel.lean -> exit 0 (zero sorries).
- lake env lean LeanChannel.lean -> exit 0 (deprecation warnings only; the 9
  permitted sorries remain).

Nothing further needs pulling for the remaining work (closing the 9 sorries):
PMF, Fintype, and the finite linear algebra are all in Mathlib. Standing rule:
>= 10 GB free before any re-pull; the cache is 6.7 GB where it sits.
- The elan home moved out of /tmp on 2026-10-04: the toolchain is now durable
  and survives /tmp cleanups.
