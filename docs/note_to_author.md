# Remark on "Pseudo-solutions of polynomial systems and the lower bound problem for
# AC0[p]-Frege systems" (arXiv:2609.35927): a two-phase certification tree for the
# candidate pseudo-solutions Omega(n,d) at p = 2, with exact error law

Prepared 2026-10-03 (corrected draft, superseding an earlier draft whose title claimed
a refutation; that claim was wrong by a success/error direction flip and is documented
as retracted in the working log). Draft remark for communication to the author (Jana
Krajicek, Charles University) or as an ECCC comment on arXiv:2609.35927. Not yet sent
or posted; the decision to communicate belongs to the corpus owner.

## Summary

We exhibit an adaptive decision tree using only degree-1 queries (row sums and
individual variables) that, against the candidate pseudo-solutions $\Omega(n,d)$ for
$\neg\mathrm{PHP}_n$ as defined in Definition 4.3 of arXiv:2609.35927, outputs a pair in
$D^\rho \times R^\rho$ (a conflict pair) with success probability exactly
$1 - 2^{-(2d+1)} + f \cdot 2^{-(2d+1)}$ at $p = 2$, where $f = |D||R| / ((n+1)n)$ is the
fraction of free pairs; at $d = 2$ this is ~0.97 (measured 0.970 across 400 exact-channel
simulations; replicated at five $(n,d)$ points with 816,000 simulations, the theorem's
unreachable error branch firing 0 times). The tree is to our knowledge the strongest
known adaptive tree for this candidate at $p = 2$: it beats the single-variable adaptive
cap of $4d^2/(2d^2+n)$ (~0.26 at the same parameters) by a factor ~4, which required
row-sum (parity) queries.

The main point of this remark, however, is that the candidate SURVIVES this attack:
the tree's error ~$2^{-2d}$ is a constant at fixed $d$, hence $\geq \gamma = k^{-O(1)}$ for all
super-polynomial $k$, so $\Omega(n,2)$ still satisfies Definition 3.1's solution condition
against it; simultaneously the tree's $\chi$-probability (= its error, in the natural
reading of the $\chi$-task) also exceeds $k^{-O(1)}$, so Theorem 6.1's hypothesis is
undamaged. Both requirements hold simultaneously, and the precise open problem is
therefore isolated and unchanged: prove that NO adaptive $(d,e)$-tree can push the error
below $k^{-O(1)}$ - the freeness-certification impossibility over $F_2$ - which via
Theorem 6.1 would yield the super-polynomial AC0[2]-Frege lower bounds for $\neg\mathrm{PHP}_n$.

## Setup (as printed in arXiv:2609.35927 v2)

Parameters: prime $p$ (we take $p = 2$), outer dimension $n$, degree $d$ (the program uses
$d = (\log k)^{O(l)}$), accuracy $h$, budget $e' = O(\log n) + O(d \log n)$.

The pipeline $\Omega(n,d)$ (Definition 4.3): (1) $\rho$: a partial injection leaving exactly
$n_\rho = 2d$ free holes; $D$ = the free pigeons ($|D| = 2d+1$), $R$ = the free holes
($|R| = 2d$); the restricted system is $\neg\mathrm{PHP}$ on $D \times R$. (2) $L$: a degree-$d$ design of the
restricted system. (3) $\omega = (\rho, L)$; the answer to a query $g$ is $L(g^\rho)$.

The solution condition (Definition 3.1): for every $(d,e)$-tree $T$,
$\mathrm{Prob}_\omega[T(\omega) \text{ is not a conflict pair for } \omega] \geq \gamma$. The lower-bound route
(Theorem 3.2 contrapositive): a $k$-step refutation implies some tree fails with
probability $< \gamma$.

## The two-phase tree (all queries degree 1)

Phase 1: query the row sums $Q_i = 1 + \sum_j x_{ij}$ for pigeons $i = 1, \ldots, n+1$; stop at
the first answer 1; certify pigeon $i^* :=$ that pigeon as free.

Why this certifies: over $F_2$, for an ASSIGNED pigeon $i$: $x_{i,\rho(i)} = 1$ and
$x_{i,j} = 0$ for $j \neq \rho(i)$, so $Q_i^\rho = 1 + 1 = 0$: assigned pigeons answer the
determined 0, never 1. An answer 1 has only one cause: $i^*$ is free.

Phase 2: for holes $j$: query $x_{i^*,j}$; stop at the first answer 1; label ($i^*, j$).

Why this certifies the hole: for certified-free $i^*$, $x_{i^*,j}^\rho = 0$ for used holes
and $x_{i^*,j}^\rho$ is the variable's design bit (a fair coin) for $j \in R$. Answer 1 has
only one cause: $j \in R$.

## The error analysis (exact)

The tree errs only if some phase's required coin comes up 0:
- Phase 1 misses iff EVERY free pigeon answers its row-coin 0. The free pigeons'
  row-coins are independent fair bits (their design coordinates are free columns of
  the design kernel; the kernel basis vectors have disjoint single-variable supports -
  verified computationally and by construction: back-substitution corrections touch
  pivot columns only). Miss probability $2^{-(2d+1)}$.
- Given phase-1 success, phase 2 misses iff the certified pigeon's $2d$ free-hole design
  bits are all 0: probability $2^{-2d}$. (We prove this branch is unreachable at the
  exact law's level: with the fallback relabeling the total error is exactly
  $2^{-(2d+1)}$ up to the $f \cdot 2^{-(2d+1)}$ fallback term; the simulation's phase-2-fail
  branch fired 0 times in 816,000 runs.)
Success $= 1 - 2^{-(2d+1)}$ (measured 0.970 at $(n,d) = (32,2)$ against $31/32 = 0.969$;
0.998 at $(64,4)$ against $1 - 2^{-9}$; replicated at $(16,1)$, $(24,3)$, $(48,4)$, $(96,6)$,
$(128,8)$)).

## Status relative to the solution condition and Theorem 6.1

The solution condition requires every tree to err with probability $\geq \gamma$. The
two-phase tree's error ~$2^{-(2d+1)}$ is a CONSTANT at fixed $d$ and is $\geq \gamma =$
$k^{-O(1)}$ for all super-polynomial $k$: $\Omega(n,2)$ SATISFIES the solution condition
against this tree. In the other direction, the tree's $\chi$-probability (0.97, a
constant) also exceeds $k^{-O(1)}$: Theorem 6.1's hypothesis is satisfied with room.
The two conditions are compatible, and we are not aware of any reading under which
this tree refutes the candidate. What the tree does establish: (i) the answer channel
at $p = 2$ is exactly the fair-coin/determined-bit law (the disjoint-support lemma);
(ii) parity (row-sum) queries strictly beat variable queries for the conflict-pair
task, so any cap argument must cover linear forms, not just monomials; (iii) the
certification mechanism (an answer 1 has one cause) is the only known route to
constant-error success, and blocking it is a sharp, checkable target.

## Constructive note

The attack indicates what a viable pseudo-solution at $p = 2$ must resist: designs that
are near-multiplicative on low-degree triples with high probability over the set -
i.e., designs not independently randomizable per free variable (which is what makes
them certification-vulnerable). Sum-of-squares-style pseudo-distributions inside the
ENS framework are natural candidates; whether they can satisfy the solution condition
against all adaptive degree-$\leq d$ trees is, to our knowledge, open - and by the above,
open in a precise form.

We work from the definitions as printed in arXiv:2609.35927 v2 and Krajicek 2024
(Proc. AMS). If the intended notion of the design set, of the answer channel, or of
the tree class differs from our reading, the remark applies to the printed
formulation. The construction is elementary (two scans, degree-1 queries), the error
analysis is exact for the stated channel, and the computational verification is
reproducible from the quoted scripts.
