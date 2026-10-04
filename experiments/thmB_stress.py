#!/usr/bin/env python3
# ---------------------------------------------------------------------------
# thmB_stress.py
#
# Independent numerical stress-test of Lemma B.1 of proof_complexity.md
# (the coupling step in the proof of Theorem B, the adaptive single-variable
# cap). Standard citations there: Joag-Dev & Proschan 1983, Dubhashi & Ranjan
# 1998. This script writes nothing but stdout; corpus files are untouched.
#
# INEQUALITY UNDER TEST (reconstructed from Lemma B.1 + its proof step (4),
# with the constants the proof uses):
#
#   Model: rho uniform over partial injections with n_rho = 2d:
#     D = free pigeons, a uniform (2d+1)-subset of {1..n+1},
#     R = free holes,   a uniform 2d-subset   of {1..n},   independent of D,
#     a uniform bijection between the remaining pigeons and holes.
#     F = D x R = free pairs.  Single-variable answer channel (exact law,
#     per queried pair q = (a,b), B_q an independent fair design bit):
#       ans(x_ab) = 1  iff  ([a in D and b in R] and B_q = 1) or (match(a) = b)
#     Pair statuses (the corpus's "killed-unmatched -> 0" case splits into two
#     genuinely different statuses, both with answer 0):
#       F  : pair free (a in D, b in R): answers the fair bit,
#       M  : killed-matched (match(a) = b): answers 1,
#       X1 : pigeon killed, matched to another hole c != b: answers 0,
#       X2 : pigeon free but its hole killed by another pigeon: answers 0.
#
#   Reading A (depletion constant of proof step (4), the reading the NA
#   argument supports): for any transcript event E determined by the answers
#   on a queried set S of e pairs (distinct pigeons, distinct holes), and any
#   pair p whose BOTH coordinates are outside S:
#
#       P[ p in F | E ]  <=  f_e := ((2d+1)/(n+1-e)) * (2d/(n-e))       (A)
#
#   Direction: upper bound.  f_e/f = ((n+1)n)/((n+1-e)(n-e)) = 1 + O(e/n)
#   is the hypergeometric depletion factor (the O(e/n) of Lemma B.1).
#
#   Reading B (the lemma's literal quantifier "any pair p not in S", which
#   allows p to SHARE one coordinate with a queried pair): the same constant
#   (A) is tested at p1 = (a_1, j) and p2 = (i, b_1) with i, j fresh.
#
#   The lemma's difference form, |P[p in F|transcript] - P[p in F|own-answer-
#   class]| = O(e/n), is scored as: for unqueried p the own-answer class is
#   trivial, so the claim is max_E |P[F_p|E] - f| = O(e/n); reported as the
#   empirical constant C* = max_E |P[F_p|E] - f| * n / e.
#
# Method: exact enumeration of the model by status atoms (status of pair 1
# plus counts of the other e-1 positions), each atom's probability and
# conditional freeness value known in closed form, so P[F_p|E] is computed
# EXACTLY in rational arithmetic. On top of that, an exact rejection-free
# CONDITIONAL sampler (samples j, R, images, D, bits directly given E) drives
# the required Monte Carlo estimates with 99% CIs. Instrument validation:
#   V1 closed-form per-pair status law vs direct prior sampling,
#   V2 normalization identity (atom weights over ALL status vectors sum to
#      the model's total outcome count),
#   V3 brute-force status-vector enumerator vs count-vector table,
#   V4 rejection MC vs conditional MC vs exact posteriors,
#   V5 e=1 closed-form analytic posteriors vs exact enumeration.
# ---------------------------------------------------------------------------

import math
import random
import time
from bisect import bisect_right
from fractions import Fraction
from math import comb, factorial, sqrt

Z99 = 2.5758293035489004  # two-sided 99% normal quantile

# status codes
F1, F0, MM, X1, X2 = 0, 1, 2, 3, 4

# exact_posteriors tuple indices
I_PE, I_P0, I_P1, I_P2 = 0, 1, 2, 3
# mc_run tuple indices
M_P0, M_P1, M_P2 = 0, 1, 2


def perm(n, k):
    if k < 0 or n < 0 or k > n:
        return 0
    return factorial(n) // factorial(n - k)


def image_R_factor(n, d, e, kf, em, x1):
    """Joint count of (R, X1-images) given the atom's counts.

    R: 2d-subset containing b_F (kf holes), avoiding b_M (em) and b_X2.
    Images: injective map c_t for each X1 pigeon t, with c_t outside
    R, outside b_M, and c_t != its own b_t.  If j of the X1 holes are in R,
    those j rows have no extra forbidden column, while the other x1-j rows
    each forbid one distinct column outside R; by inclusion-exclusion

        img(j)  = Sum_{i=0}^{x1-j} (-1)^i C(x1-j, i) perm(n-2d-em-i, x1-i)

    (rows with b_t in R may use any of the M = n-2d-em columns of
    holes \\ (R u b_M); rows with b_t outside R lose exactly their own).
    So

        # (R, images) = Sum_j C(x1, j) C(n-e, 2d-kf-j) img(j).

    Two consequences used elsewhere:
      - each specific R with the given j has exactly img(j) completions, so
        the conditional law of R given the atom is img(j)-weighted within
        the atom (NOT uniform over j);
      - the fresh-hole membership factor follows by weighting the same
        terms with the fresh hole forced in (see hole_factor).
    """
    total = 0
    M = n - 2 * d - em
    for j in range(0, x1 + 1):
        if 2 * d - kf - j < 0:
            break
        img = 0
        for i in range(0, x1 - j + 1):
            img += ((-1) ** i) * comb(x1 - j, i) * perm(M - i, x1 - i)
        total += comb(x1, j) * comb(n - e, 2 * d - kf - j) * img
    return total


def hole_factor(n, d, e, kf, em, x1):
    """P[ a fresh (unqueried) hole is in R | atom ] as an exact Fraction.

    R's conditional law given the atom is img(j)-weighted (see
    image_R_factor), so the fresh-hole membership is the img-weighted ratio

        [Sum_j C(x1,j) C(n-e-1, 2d-kf-1-j) img(j)]
        / [Sum_j C(x1,j) C(n-e,  2d-kf-j)   img(j)].

    For x1 = 0 this reduces to the plain hypergeometric (2d-kf)/(n-e).
    """
    M = n - 2 * d - em
    num = 0
    den = 0
    for j in range(0, x1 + 1):
        if 2 * d - kf - j < 0:
            break
        img = 0
        for i in range(0, x1 - j + 1):
            img += ((-1) ** i) * comb(x1 - j, i) * perm(M - i, x1 - i)
        if img == 0:
            continue
        den += comb(x1, j) * comb(n - e, 2 * d - kf - j) * img
        if 2 * d - kf - 1 - j >= 0:
            num += comb(x1, j) * comb(n - e - 1, 2 * d - kf - 1 - j) * img
    if den == 0:
        # no admissible R at all: the atom is impossible under this pattern
        return Fraction(0)
    return Fraction(num, den)


def shared_hole_factor(n, d, e, kf, em, x1):
    """P[ b_1 in R | atom ] when pair 1 has X1 status (b_1 is one of the x1
    X1-holes; c_1 != b_1 is required, so hole 1 is never pigeon 1's own
    image, but it CAN be in R).  img-weighted like hole_factor:

        [Sum_{j>=1} C(x1-1, j-1) C(n-e, 2d-kf-j) img(j)]
        / [Sum_j  C(x1, j)   C(n-e, 2d-kf-j) img(j)]
    """
    M = n - 2 * d - em
    num = 0
    den = 0
    for j in range(0, x1 + 1):
        if 2 * d - kf - j < 0:
            break
        img = 0
        for i in range(0, x1 - j + 1):
            img += ((-1) ** i) * comb(x1 - j, i) * perm(M - i, x1 - i)
        if img == 0:
            continue
        den += comb(x1, j) * comb(n - e, 2 * d - kf - j) * img
        if j >= 1:
            num += (comb(x1 - 1, j - 1)
                    * comb(n - e, 2 * d - kf - j) * img)
    return Fraction(num, den) if den else Fraction(0)


# ---------------------------------------------------------------------------
# Exact atom machinery.
#
# Queried pairs: q_t = (t+1, t+1), t = 0..e-1 (distinct pigeons, distinct
# holes; the worst case for the bound, since sharing coordinates between
# queried pairs can only reduce the number of depleted pools). Transcript
# event E_z = {the first z answers are 1, the remaining e-z answers are 0};
# by exchangeability over query positions, P[F_p|E] depends only on z.
#
# Atom = status s1 of pair 1 plus counts (cf1, cf0, cm, c1, c2) of
# F1/F0/M/X1/X2 among the other e-1 positions.  Closed forms (derived by
# counting (D, R, matching, bits) outcomes; each status vector leaves the
# e-kf non-free pairs' bits unconstrained, giving the 2^(e-kf) factor):
#
#   w(atom) = C(z1,cf1) C(z0,cf0) C(z0-cf0, c1)     [status placements;
#              leftover one-positions are forced to M, M cannot sit on a
#              zero-position]
#             * C(n+1-e, 2d+1-kf-x2)          [D count]
#             * image_R_factor(...)           [(R, images) count]
#             * (n-2d-em-x1)!                 [matching completions]
#             * 2^(e-kf)                      [free bit assignments]
#
#   P[fresh pigeon in D | atom] = (2d+1-kf-x2)/(n+1-e)
#   P[fresh hole   in R | atom] = hole_factor(kf,em,x1): the img(j)-weighted
#       ratio (plain hypergeometric (2d-kf)/(n-e) only when x1 = 0)
#
#   v0(atom) = ((2d+1-kf-x2)/(n+1-e)) * hole_factor(kf,em,x1)  [disjoint p0]
#   v1(atom) = hole_factor(kf,em,x1)  if s1 in {F1,F0,X2} else 0  [p1=(1,n)]
#   v2(atom) = ((2d+1-kf-x2)/(n+1-e)) * [1 if s1 in {F1,F0} else
#              shared_hole_factor(kf,em,x1) if s1 = X1 else 0]  [p2=(n+1,1)]
# ---------------------------------------------------------------------------

def atom_table(n, d, e, z):
    out = []
    rem = e - 1
    # position 0 answered 1 iff z >= 1: its status class is fixed by z.
    s1_opts = [F1, MM] if z >= 1 else [F0, X1, X2]
    z1 = z - 1 if z >= 1 else 0        # ones among the remaining e-1 spots
    z0 = rem - z1
    if z1 < 0 or z0 < 0:
        return out
    for s1 in s1_opts:
        for cf1 in range(z1 + 1):
            cm = z1 - cf1            # leftover one-positions are forced to M
            for cf0 in range(z0 + 1):
                for c1 in range(z0 - cf0 + 1):
                    c2 = z0 - cf0 - c1
                    kf = cf1 + cf0 + (1 if s1 in (F1, F0) else 0)
                    x2 = c2 + (1 if s1 == X2 else 0)
                    em = cm + (1 if s1 == MM else 0)
                    x1 = c1 + (1 if s1 == X1 else 0)
                    top = 2 * d + 1 - kf - x2      # D slots left
                    if top < 0 or top > n + 1 - e:
                        continue
                    if n - 2 * d - em - x1 < 0:
                        continue
                    jf = image_R_factor(n, d, e, kf, em, x1)
                    if jf <= 0:
                        continue
                    # M can only sit on a one-position and F0/X1/X2 only on a
                    # zero-position, so the assignment count is
                    # C(z1,cf1) C(z0,cf0) C(z0-cf0, c1).
                    w = (comb(z1, cf1) * comb(z0, cf0) * comb(z0 - cf0, c1))
                    w *= comb(n + 1 - e, top)
                    w *= jf
                    w *= factorial(n - 2 * d - em - x1)
                    w *= 2 ** (e - kf)
                    if w <= 0:
                        continue
                    hf = hole_factor(n, d, e, kf, em, x1)
                    pi = Fraction(2 * d + 1 - kf - x2, n + 1 - e)
                    v0 = pi * hf
                    v1 = hf if s1 in (F1, F0, X2) else Fraction(0)
                    if s1 in (F1, F0):
                        v2 = pi
                    elif s1 == X1:
                        v2 = pi * shared_hole_factor(n, d, e, kf, em, x1)
                    else:
                        v2 = Fraction(0)
                    out.append((w, v0, v1, v2, (s1, cf1, cf0, cm, c1, c2)))
    return out


def model_total(n, d, e):
    """Total count of (D, R, matching, e design bits) outcomes."""
    return (2 ** e) * comb(n + 1, 2 * d + 1) * comb(n, 2 * d) * factorial(n - 2 * d)


def exact_posteriors(n, d, e, z):
    """(P[E], P[F_p0|E], P[F_p1|E], P[F_p2|E]) exactly, as Fractions.

    p0 = (n+1, n): both coordinates unqueried (Reading A probe pair),
    p1 = (1, n): shares pigeon a_1 = 1 with queried pair 1 (Reading B),
    p2 = (n+1, 1): shares hole b_1 = 1 with queried pair 1 (Reading B).
    """
    tab = atom_table(n, d, e, z)
    W = sum(t[0] for t in tab)
    pE = Fraction(W, model_total(n, d, e))
    s0 = sum(t[0] * t[1] for t in tab)
    s1 = sum(t[0] * t[2] for t in tab)
    s2 = sum(t[0] * t[3] for t in tab)
    return pE, s0 / W, s1 / W, s2 / W


def float_posterior0(n, d, e, z):
    """Float-only P[F_p0|E] for the box scan."""
    tab = atom_table(n, d, e, z)
    W = float(sum(t[0] for t in tab))
    s0 = 0.0
    for t in tab:
        s0 += (t[0] / W) * float(t[1])
    return s0


def f_e(n, d, e):
    return Fraction((2 * d + 1) * (2 * d), (n + 1 - e) * (n - e))


def cap_thmB(n, d):
    """Theorem B's per-leaf cap: max(2d^2/(2d^2+n), f/2)."""
    f = Fraction((2 * d + 1) * (2 * d), (n + 1) * n)
    return max(Fraction(2 * d * d, 2 * d * d + n), f / 2)

# ---------------------------------------------------------------------------
# Exact conditional Monte Carlo sampler.
#
# Samples (j, R, D) directly from P[. | E_z]:
#   1. pick an atom with probability w/W (exact integer weights),
#   2. place the F statuses uniformly among consistent positions, split the
#      rest uniformly into M/X1/X2,
#   3. pick j = #X1-holes-in-R with weight
#      C(x1,j) C(n-e, 2d-kf-j) img(j)   (img as in image_R_factor),
#   4. draw R: j of the X1 holes plus a uniform sample of the unqueried holes
#      (R is uniform within its j-class),
#   5. draw D: forced pigeons (F and X2 positions) plus a uniform sample.
# The X1 images are not drawn: the probe pairs have both coordinates
# unqueried-or-fixed by E_z, so their freeness events depend only on (D, R),
# and the queried answers are already fixed by the event.  Every step
# reproduces the closed-form atom counts exactly, so the sampler is exact
# (rejection-free, unbiased).
# ---------------------------------------------------------------------------

def mc_run(n, d, e, z, trials, seed):
    rng = random.Random(seed)
    tab = atom_table(n, d, e, z)
    W = sum(t[0] for t in tab)

    # precompute per-atom data: cum weight, j-weights, derived sizes
    atoms = []
    cum = []
    acc = 0.0
    for t in tab:
        s1, cf1, cf0, cm, c1c, c2c = t[4]
        kf = cf1 + cf0 + (1 if s1 in (F1, F0) else 0)
        em = cm + (1 if s1 == MM else 0)
        x1 = c1c + (1 if s1 == X1 else 0)
        x2 = c2c + (1 if s1 == X2 else 0)
        M = n - 2 * d - em
        jw = []
        for j in range(0, x1 + 1):
            if 2 * d - kf - j < 0:
                break
            img = 0
            for i in range(0, x1 - j + 1):
                img += ((-1) ** i) * comb(x1 - j, i) * perm(M - i, x1 - i)
            jw.append(comb(x1, j) * comb(n - e, 2 * d - kf - j) * img)
        acc += t[0] / W
        cum.append(acc)
        atoms.append((s1, cf1, cf0, cm, c1c, c2c, kf, em, x1, x2, jw))
    cum[-1] = 1.0

    ones_rem = [t for t in range(1, e) if t < z]
    zeros_rem = [t for t in range(1, e) if t >= z]
    pigeonpool = list(range(e + 1, n + 2))   # unqueried pigeons, n+1-e
    holepool = list(range(e + 1, n + 1))     # unqueried holes,  n-e
    c0 = c1 = c2 = 0
    for _ in range(trials):
        i = bisect_right(cum, rng.random())
        if i >= len(atoms):
            i = len(atoms) - 1
        (s1, cf1, cf0, cm, c1c, c2c, kf, em, x1, x2, jw) = atoms[i]
        # leftover one-positions are forced to M; F1 among ones, F0/X1/X2
        # split the zero-positions
        f1s = rng.sample(ones_rem, cf1) if cf1 else []
        used_ones = set(f1s)
        m_pos = [t for t in ones_rem if t not in used_ones]
        f0s = rng.sample(zeros_rem, cf0) if cf0 else []
        used_zeros = set(f0s)
        remzeros = [t for t in zeros_rem if t not in used_zeros]
        x1s = set(rng.sample(remzeros, c1c)) if c1c else set()
        x2s = {t for t in remzeros if t not in x1s}

        # step 3: j = number of X1 holes that land in R
        jw_tot = sum(jw)
        jr = rng.random() * jw_tot
        accj = 0.0
        j = 0
        for jj, wj in enumerate(jw):
            accj += wj
            if jr <= accj:
                j = jj
                break

        # step 4: R = b_F (forced) + j of the X1 holes + uniform unqueried;
        # position 0's hole joins the X1-hole pool when s1 == X1
        forcedR = {t + 1 for t in f1s}
        forcedR.update(t + 1 for t in f0s)
        if s1 in (F1, F0):
            forcedR.add(1)
        x1l = [t + 1 for t in x1s]
        if s1 == X1:
            x1l.append(1)
        RinX1 = set(rng.sample(x1l, j)) if j else set()
        top2 = 2 * d - kf - j
        R = set(forcedR)
        R |= RinX1
        if top2:
            R.update(rng.sample(holepool, top2))

        # step 5: D = forced (F and X2 pigeons) + uniform unqueried
        forcedD = {t + 1 for t in f1s}
        forcedD.update(t + 1 for t in f0s)
        forcedD.update(t + 1 for t in x2s)
        if s1 in (F1, F0, X2):
            forcedD.add(1)
        top = 2 * d + 1 - len(forcedD)
        D = set(forcedD)
        if top:
            D.update(rng.sample(pigeonpool, top))

        if (n + 1) in D and n in R:
            c0 += 1
        if 1 in D and n in R:
            c1 += 1
        if (n + 1) in D and 1 in R:
            c2 += 1
    return c0 / trials, c1 / trials, c2 / trials, trials


# ---------------------------------------------------------------------------
# Direct prior sampler (validation instrument): sample (D, R, matching, bits)
# from the model, compute the answers, keep trials matching E_z.
# ---------------------------------------------------------------------------

def prior_run(n, d, e, z, trials, seed, tally=False):
    rng = random.Random(seed)
    pigeons = list(range(1, n + 2))
    holes = list(range(1, n + 1))
    matches = 0
    hits = 0
    stat = [0, 0, 0, 0]  # F, M, X1, X2 counts for pair 1
    for _ in range(trials):
        D = set(rng.sample(pigeons, 2 * d + 1))
        R = set(rng.sample(holes, 2 * d))
        nonD = [i for i in pigeons if i not in D]
        nonR = [h for h in holes if h not in R]
        img = rng.sample(nonR, len(nonR))
        matched = dict(zip(nonD, img))
        a1, b1 = 1, 1
        if a1 in D and b1 in R:
            s = 0
        elif matched.get(a1) == b1:
            s = 1
        elif a1 not in D:
            s = 2   # X1: pigeon killed, matched elsewhere
        else:
            s = 3   # X2: pigeon free, hole killed by another pigeon
        if tally:
            stat[s] += 1
        answers = []
        for t in range(e):
            a = t + 1
            b = t + 1
            if a in D and b in R:
                answers.append(1 if rng.random() < 0.5 else 0)
            elif matched.get(a) == b:
                answers.append(1)
            else:
                answers.append(0)
        if answers == [1] * z + [0] * (e - z):
            matches += 1
            if (n + 1) in D and n in R:
                hits += 1
    return hits, matches, trials, stat


# ---------------------------------------------------------------------------
# Brute-force status-vector enumerator (independent check of atom_table).
# ---------------------------------------------------------------------------

def brute_posterior0(n, d, e, z):
    from itertools import product
    W = 0
    s0 = Fraction(0)
    for st in product(range(5), repeat=e):
        ok = True
        for t in range(e):
            if (st[t] in (F1, MM)) != (t < z):
                ok = False
                break
        if not ok:
            continue
        kf = sum(1 for s in st if s in (F1, F0))
        em = sum(1 for s in st if s == MM)
        x1 = sum(1 for s in st if s == X1)
        x2 = sum(1 for s in st if s == X2)
        top = 2 * d + 1 - kf - x2
        if top < 0 or top > n + 1 - e:
            continue
        if n - 2 * d - em - x1 < 0:
            continue
        w = (comb(n + 1 - e, top) * image_R_factor(n, d, e, kf, em, x1)
             * factorial(n - 2 * d - em - x1) * 2 ** (e - kf))
        W += w
        s0 += (w * Fraction(2 * d + 1 - kf - x2, n + 1 - e)
               * hole_factor(n, d, e, kf, em, x1))
    return (s0 / W) if W else None


def brute_normalization(n, d, e):
    """Atom-weight sum over ALL status vectors must equal the model total."""
    from itertools import product
    W = 0
    for st in product(range(5), repeat=e):
        kf = sum(1 for s in st if s in (F1, F0))
        em = sum(1 for s in st if s == MM)
        x1 = sum(1 for s in st if s == X1)
        x2 = sum(1 for s in st if s == X2)
        top = 2 * d + 1 - kf - x2
        if top < 0 or top > n + 1 - e:
            continue
        if n - 2 * d - em - x1 < 0:
            continue
        W += (comb(n + 1 - e, top) * image_R_factor(n, d, e, kf, em, x1)
              * factorial(n - 2 * d - em - x1) * 2 ** (e - kf))
    return W


def ci99(phat, N):
    return Z99 * sqrt(phat * (1.0 - phat) / N)


def status_law(n, d):
    f = Fraction((2 * d + 1) * (2 * d), (n + 1) * n)
    m = Fraction(n - 2 * d, (n + 1) * n)
    x2 = Fraction((2 * d + 1) * (n - 2 * d), (n + 1) * n)
    return (f, m, Fraction(1) - f - m - x2, x2)  # F, M, X1, X2


def analytic_e1(n, d, z, probe):
    """Closed-form e=1 posteriors for V5 (independent of the atom machinery).

    probe 0: p0 fresh pair; probe 1: p1 shares pigeon; probe 2: p2 shares hole.
    Atoms: z=1: F1 (weight f/2) and M (weight m);
           z=0: F0 (f/2), X1 (P[X1]), X2 (P[X2]).
    Fresh-pigeon factor pi (D's law is image-independent):
      F (kf=1): pi = (2d+1-1)/(n+1-1) = 2d/n
      M:        pi = (2d+1)/n
      X1:       pi = (2d+1)/n
      X2:       pi = 2d/n (the X2 pigeon is in D, consuming a slot)
    Fresh-hole factor rh: R's conditional law given the atom is img(j)-
    weighted (see hole_factor / shared_hole_factor, reused here; their
    exactness is established by the exhaustive per-outcome check).
    Probe values: probe 0 = pi * rh (both coordinates fresh);
    probe 1 = [a_1 in D | atom] * rh, where the shared pigeon 1 is in D
    exactly for F/X2 atoms;
    probe 2 = [b_1 in R | atom] * pi, where b_1 is in R certainly for F
    atoms, with probability shared_hole_factor for X1 atoms, and never for
    M/X2 atoms.  The atom WEIGHTS here come from the per-pair answer law
    (f/2 fair-coin, m matched, and the two answer-0 leftovers), an
    independent derivation from the atom table.
    """
    f = Fraction((2 * d + 1) * (2 * d), (n + 1) * n)
    m = Fraction(n - 2 * d, (n + 1) * n)
    x2p = Fraction((2 * d + 1) * (n - 2 * d), (n + 1) * n)
    x1p = Fraction(1) - f - m - x2p
    if z == 1:
        atoms = [(f / 2, "F1"), (m, "M")]
    else:
        atoms = [(f / 2, "F0"), (x1p, "X1"), (x2p, "X2")]

    def pi_of(st):
        if st in ("F1", "F0"):
            return Fraction(2 * d, n)
        if st in ("M", "X1"):
            return Fraction(2 * d + 1, n)
        return Fraction(2 * d, n)  # X2

    num = Fraction(0)
    den = Fraction(0)
    for (wt, st) in atoms:
        den += wt
        pi = pi_of(st)
        if st in ("F1", "F0"):
            kf, em, x1 = 1, 0, 0
        elif st == "M":
            kf, em, x1 = 0, 1, 0
        elif st == "X1":
            kf, em, x1 = 0, 0, 1
        else:
            kf, em, x1 = 0, 0, 0
        rh = hole_factor(n, d, e=1, kf=kf, em=em, x1=x1)
        if probe == 0:
            num += wt * pi * rh
        elif probe == 1:
            if st in ("F1", "F0", "X2"):     # shared pigeon 1 in D
                num += wt * rh
        else:                                # probe 2
            if st in ("F1", "F0"):           # shared hole 1 in R for sure
                num += wt * pi
            elif st == "X1":                 # b_1 in R with prob sh
                sh = shared_hole_factor(n, d, e=1, kf=kf, em=em, x1=x1)
                num += wt * pi * sh
    return num / den

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

GRID = [(8, 1), (12, 2), (16, 4), (24, 6), (32, 8), (40, 12), (8, 3)]
TRIALS = 200_000
TRIALS_BUMP = 1_000_000


def e_list(n, d):
    emax = n - 2 * d - 1
    if emax < 1:
        emax = 1
    es = {x for x in [1, 2, 4, 8, 12, emax] if 1 <= x <= emax}
    if 1 <= n - 2 * d <= 13:
        es.add(n - 2 * d)   # the boundary e = n-2d (degenerate: f_e = 1)
    return sorted(es)


def seed_for(n, d, e, z, tag):
    return (n * 1_000_003 + d * 10_007 + e * 101 + z * 7 + tag * 7919) % (2 ** 31)


def main():
    t0 = time.time()
    print("=" * 110)
    print("thmB_stress: numerical stress-test of Lemma B.1 (proof_complexity.md)")
    print()
    print("Inequality tested (Reading A, the proof's step-(4) depletion constant):")
    print("   P[ p in F | E ] <= f_e := ((2d+1)/(n+1-e)) * (2d/(n-e)),")
    print("for any transcript event E on e queried pairs (answers on S) and any pair")
    print("p with BOTH coordinates unqueried. Direction: upper bound (LHS-RHS <= 0).")
    print("Reading B (literal 'any pair not in S', p sharing a coordinate with S):")
    print("same constant tested at p1 = (a_1, j) and p2 = (i, b_1), i, j fresh.")
    print("Difference form scored as C* = max_E |P[F_p|E] - f| * n / e.")
    print("=" * 110)

    # ---------------- validation ----------------
    print("\nINSTRUMENT VALIDATION")
    n, d = 32, 2
    th = status_law(n, d)
    _, _, _, stat = prior_run(n, d, e=1, z=1, trials=400_000, seed=123,
                              tally=True)
    emp = [c / 400_000 for c in stat]
    names = ["F ", "M ", "X1", "X2"]
    for k in range(4):
        se = sqrt(emp[k] * (1 - emp[k]) / 400_000)
        zsc = (emp[k] - float(th[k])) / se if se > 0 else 0.0
        print("  V1 status law (n=32,d=2) %-2s exact %.6f  prior-MC %.6f  z=%+.2f"
              % (names[k], float(th[k]), emp[k], zsc))

    n, d, e = 8, 1, 3
    tot = brute_normalization(n, d, e)
    ref = model_total(n, d, e)
    print("  V2 normalization (n=8,d=1,e=3): atom-sum %d vs model total %d -> %s"
          % (tot, ref, "OK" if tot == ref else "MISMATCH"))
    tot2 = brute_normalization(9, 3, 3)
    ref2 = model_total(9, 3, 3)
    print("  V2 normalization (n=9,d=3,e=3): atom-sum %d vs model total %d -> %s"
          % (tot2, ref2, "OK" if tot2 == ref2 else "MISMATCH"))

    ok3 = True
    for (nb, db, eb, zb) in [(8, 1, 3, 1), (8, 1, 3, 0), (12, 2, 2, 1),
                             (16, 4, 3, 2), (8, 3, 1, 1)]:
        pb = brute_posterior0(nb, db, eb, zb)
        pe = exact_posteriors(nb, db, eb, zb)[I_P0]
        same = (pb == pe)
        ok3 &= same
        print("  V3 brute vs count-table P[F_p0|E] (n=%d,d=%d,e=%d,z=%d): %s vs %s -> %s"
              % (nb, db, eb, zb, pb, pe, "OK" if same else "MISMATCH"))

    ok5 = True
    for (nb, db, zb) in [(32, 2, 0), (32, 2, 1), (8, 1, 0), (8, 1, 1),
                         (40, 12, 1)]:
        for probe in (0, 1, 2):
            pa = analytic_e1(nb, db, zb, probe)
            pe = exact_posteriors(nb, db, 1, zb)[1 + probe]
            same = (pa == pe)
            ok5 &= same
            if not same:
                print("  V5 ANALYTIC MISMATCH (n=%d,d=%d,z=%d,probe=%d): %s vs %s"
                      % (nb, db, zb, probe, pa, pe))
    print("  V5 e=1 analytic vs exact enumeration (5 points x 3 probes): %s"
          % ("ALL OK" if ok5 else "MISMATCH"))

    ok4 = True
    for (nb, db, eb, zb) in [(8, 1, 2, 1), (8, 1, 2, 0), (16, 4, 2, 0)]:
        pe = exact_posteriors(nb, db, eb, zb)[I_P0]
        hits, matches, trials, _ = prior_run(nb, db, eb, zb, trials=400_000,
                                             seed=999 + zb)
        if matches == 0:
            print("  V4 rejection run had zero matches, skipped")
            ok4 = False
            continue
        rej = hits / matches
        se_rej = 2.576 * sqrt(rej * (1 - rej) / matches)
        mc0, _, _, N = mc_run(nb, db, eb, zb, TRIALS, seed_for(nb, db, eb, zb, 0))
        h_mc = ci99(mc0, N)
        inside = (float(pe) - se_rej <= mc0 + h_mc) and (mc0 - h_mc <= float(pe) + se_rej)
        ok4 &= inside
        print("  V4 (n=%d,d=%d,e=%d,z=%d): exact %.6f | rejection-MC %.6f +- %.6f"
              " (P[E]~%.5f, %d matches) | conditional-MC %.6f +- %.6f -> %s"
              % (nb, db, eb, zb, float(pe), rej, se_rej, matches / trials,
                 matches, mc0, h_mc, "OK" if inside else "MISMATCH"))
    v_ok = ok3 and ok4 and ok5
    print("  validation verdict: %s"
          % ("ALL OK" if v_ok else "FAILURE: investigate before trusting results"))

    # ---------------- main grid: compute exact per-z once, reuse everywhere --
    grid_data = []   # (n, d, e, zdata)
    for (n, d) in GRID:
        for e in e_list(n, d):
            zdata = [exact_posteriors(n, d, e, z) for z in range(0, e + 1)]
            grid_data.append((n, d, e, zdata))

    # ---------------- TABLE 1: Reading A ----------------
    print("\n" + "=" * 110)
    print("TABLE 1: Reading A, p0 = (n+1, n), both coordinates unqueried.")
    print("margin = P[F_p0|E*] - f_e (LHS - RHS); PASS iff upper 99% CI < 0.")
    print("E* = worst transcript pattern; exact search over all 2^e patterns,")
    print("reduced by exchangeability to the count z of 1s.")
    print("=" * 110)
    print("%-9s %2s %-9s | %-8s %-8s | %-9s %-24s %-7s | %-10s %-22s %-11s %7s"
          % ("n,d,e", "z*", "P[E*]", "f", "f_e", "P_exact",
             "P_MC +- CI99", "z-sc", "mrg_exact", "mrg_MC +- CI99",
             "verdict", "trials"))
    all_rows = []
    for (n, d, e, zdata) in grid_data:
        fe = f_e(n, d, e)
        f0 = f_e(n, d, 0)
        worst = None
        for (z, row) in enumerate(zdata):
            gap = row[I_P0] - fe
            if worst is None or gap > worst[0]:
                worst = (gap, z)
        gap, zstar = worst
        pex = zdata[zstar][I_P0]
        pE = zdata[zstar][I_PE]
        trials = TRIALS
        mc0, _, _, N = mc_run(n, d, e, zstar, trials, seed_for(n, d, e, zstar, 0))
        h = ci99(mc0, N)
        if abs(float(gap)) < 4 * h:      # near-tie: bump trials
            trials = TRIALS_BUMP
            mc0, _, _, N = mc_run(n, d, e, zstar, trials,
                                  seed_for(n, d, e, zstar, 1))
            h = ci99(mc0, N)
        se = h / Z99
        zsc = (mc0 - float(pex)) / se if se > 0 else 0.0
        mrg_mc = mc0 - float(fe)
        if float(gap) >= 0:
            verdict = "FAIL(exact)"
        elif mrg_mc + h < 0:
            verdict = "PASS"
        elif mrg_mc - h > 0:
            verdict = "FAIL"
        else:
            verdict = "TIE"
        print("%-9s %2d %-9.3e | %-8.6f %-8.6f | %-9.6f %.6f +-%.6f %-+7.2f | "
              "%-10.3e %+.6f +-%.6f %-11s %7d"
              % ("%d,%d,%d" % (n, d, e), zstar, float(pE), float(f0), float(fe),
                 float(pex), mc0, h, zsc, float(gap), mrg_mc, h, verdict, N))
        all_rows.append((n, d, e, zstar, fe, zdata))

    # ---------------- TABLE 2: Reading B probes ----------------
    print("\n" + "=" * 110)
    print("TABLE 2: Reading B probes, p sharing ONE coordinate with queried pair 1.")
    print("Same depletion constant f_e. gap = P[F_p|E*] - f_e, exact (rational).")
    print("E* per probe = its own worst pattern. cap = max(2d^2/(2d^2+n), f/2)")
    print("= Theorem B's per-leaf cap, for context.")
    print("=" * 110)
    print("%-9s | %-26s | %-26s | %-8s | %s"
          % ("n,d,e", "p1=(1,n): gap / z* / verdict",
             "p2=(n+1,1): gap / z* / verdict", "cap", "max probe <= cap?"))
    probe_rows = []
    for (n, d, e, zdata) in grid_data:
        fe = f_e(n, d, e)
        cap = cap_thmB(n, d)
        res = []
        maxprobe = Fraction(0)
        for idx in (I_P1, I_P2):
            best = None
            for (z, row) in enumerate(zdata):
                g = row[idx] - fe
                if best is None or g > best[0]:
                    best = (g, z, row[idx])
            res.append(best)
            if best[2] > maxprobe:
                maxprobe = best[2]
        (g1, z1, v1), (g2, z2, v2) = res
        vd1 = "FAIL" if g1 > 0 else ("TIE" if g1 == 0 else "PASS")
        vd2 = "FAIL" if g2 > 0 else ("TIE" if g2 == 0 else "PASS")
        under = "yes" if maxprobe <= cap else "NO"
        print("%-9s | %+9.6f z=%-2d %-5s | %+9.6f z=%-2d %-5s | %-8.4f | %s"
              % ("%d,%d,%d" % (n, d, e), float(g1), z1, vd1,
                 float(g2), z2, vd2, float(cap), under))
        probe_rows.append((n, d, e, z1, z2, fe, vd1, vd2))

    print("\nMC confirmation of probe rows with exact FAIL/TIE"
          " (200k trials, 99% CI):")
    any_conf = False
    for (n, d, e, z1, z2, fe, vd1, vd2) in probe_rows:
        parts = []
        for (z, midx, vd, pname) in ((z1, M_P1, vd1, "p1"),
                                     (z2, M_P2, vd2, "p2")):
            if vd == "PASS":
                continue
            m = mc_run(n, d, e, z, TRIALS, seed_for(n, d, e, z, 5 + midx))[midx]
            h = ci99(m, TRIALS)
            mrg = m - float(fe)
            v = ("PASS" if mrg + h < 0 else "FAIL" if mrg - h > 0 else "TIE")
            parts.append("%s z=%d MC gap %+.6f +-%.6f (%s; exact %s)"
                         % (pname, z, mrg, h, v, vd))
        if parts:
            any_conf = True
            print("  (%d,%d,%d): %s" % (n, d, e, "; ".join(parts)))
    if not any_conf:
        print("  (none needed)")

    # ---------------- TABLE 3: difference form ----------------
    print("\n" + "=" * 110)
    print("TABLE 3: Lemma B.1's difference form |P[F_p|E] - P[F_p|own]| = O(e/n)")
    print("(unqueried p: own class is trivial). C* = max_z |P[F_p0|E_z] - f| * n/e;")
    print("the claim needs C* bounded uniformly in the parameters.")
    print("=" * 110)
    print("%-9s %-12s %-8s %s" % ("n,d,e", "max_z|P-f|", "C*", "worst z"))
    cmax = 0.0
    cmax_at = None
    for (n, d, e, zstar, fe, zdata) in all_rows:
        f0 = f_e(n, d, 0)
        mx = Fraction(0)
        wz = 0
        for (z, row) in enumerate(zdata):
            dev = abs(row[I_P0] - f0)
            if dev > mx:
                mx = dev
                wz = z
        cs = float(mx) * n / e
        if cs > cmax:
            cmax = cs
            cmax_at = (n, d, e)
        print("%-9s %-12.3e %-8.4f %d" % ("%d,%d,%d" % (n, d, e), float(mx), cs, wz))
    print("  max C* = %.4f at (n=%d, d=%d, e=%d)" % (cmax, *cmax_at))

    # ---------------- worst-case box scan ----------------
    print("\n" + "=" * 110)
    print("BOX SCAN: exact float scan for the minimal-margin (tightest) point.")
    print("argmax over z restricted to {0, e}; the grid above checks on %d points"
          % len(all_rows))
    print("that the worst z is always 0 or e. gap = P[F_p0|E*] - f_e; ranking by")
    print("gap descending (least negative = tightest = closest to violation).")
    print("=" * 110)
    results = []
    for n in range(8, 49, 4):
        dmax = min(14, (n - 1) // 2)
        for d in range(1, dmax + 1):
            emax = n - 2 * d - 1
            if emax < 1:
                continue
            es = sorted({x for x in [1, 2, 4, 8, 12, emax] if 1 <= x <= emax})
            for e in es:
                fev = float(f_e(n, d, e))
                best = None
                for z in (0, e):
                    p0 = float_posterior0(n, d, e, z)
                    gap = p0 - fev
                    if best is None or gap > best[0]:
                        best = (gap, z, p0)
                results.append((best[0], n, d, e, best[1], best[2], fev))
    results.sort(reverse=True)
    print("top 8 tightest points:")
    for (gap, n, d, e, z, p0, fev) in results[:8]:
        print("  (n=%2d, d=%2d, e=%2d, z=%2d): P=%.6f f_e=%.6f gap=%+.3e (rel %+.5f)"
              % (n, d, e, z, p0, fev, gap, gap / fev))
    gw, nw, dw, ew, zw, _, few = results[0]
    print("\nglobal tightest point: (n=%d, d=%d, e=%d, z=%d)" % (nw, dw, ew, zw))
    pex = exact_posteriors(nw, dw, ew, zw)[I_P0]
    feX = f_e(nw, dw, ew)
    gapx = pex - feX
    trials = 1_000_000
    mcX = mc_run(nw, dw, ew, zw, trials, seed_for(nw, dw, ew, zw, 42))[M_P0]
    hX = ci99(mcX, trials)
    print("  exact:  P[F_p0|E*] = %.8f  f_e = %.8f  gap = %+.3e  -> %s"
          % (float(pex), float(feX), float(gapx),
             "PASS" if gapx < 0 else "FAIL"))
    print("  MC 1M:  P[F_p0|E*] = %.6f +- %.6f  gap = %+.6f  -> %s"
          % (mcX, hX, mcX - float(feX),
             "PASS" if mcX + hX < float(feX) else "TIE/FAIL"))

    # ---------------- summary ----------------
    print("\n" + "=" * 110)
    print("SUMMARY")
    failsA = [(n, d, e) for (n, d, e, zstar, fe, zdata) in all_rows
              if max(row[I_P0] - fe for row in zdata) > 0]
    tiesA = [(n, d, e) for (n, d, e, zstar, fe, zdata) in all_rows
             if max(row[I_P0] - fe for row in zdata) == 0]
    print("Reading A (coordinate-disjoint p): %d grid points; exact FAILs: %s;"
          " exact TIEs: %s"
          % (len(all_rows), failsA or "none", tiesA or "none"))
    failsB1 = [(n, d, e) for (n, d, e, z1, z2, fe, vd1, vd2) in probe_rows
               if vd1 != "PASS"]
    failsB2 = [(n, d, e) for (n, d, e, z1, z2, fe, vd1, vd2) in probe_rows
               if vd2 != "PASS"]
    print("Reading B shared-pigeon probe p1: exact FAIL/TIE at %d/%d points %s"
          % (len(failsB1), len(probe_rows), failsB1 or ""))
    print("Reading B shared-hole probe p2:   exact FAIL/TIE at %d/%d points %s"
          % (len(failsB2), len(probe_rows), failsB2 or ""))
    print("Empirical O(e/n) constant (difference form, disjoint p):"
          " max C* = %.4f" % cmax)
    print("Total MC trials run: see per-row counts; standard %dk, bumped rows %dk."
          % (TRIALS // 1000, TRIALS_BUMP // 1000))
    print("Total runtime %.1f s" % (time.time() - t0))


if __name__ == "__main__":
    main()
