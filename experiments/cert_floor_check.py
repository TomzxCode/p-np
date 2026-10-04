#!/usr/bin/env python3
"""cert_floor_check.py

Certification-floor audit for adaptive degree-1 trees in the Omega(n,d) pipeline
of arXiv:2609.35927 at p = 2.

Channel law (proved, taken as given):
  after rho there are 2d+1 free pigeons D and 2d free holes R among n+1 / n;
  a single-variable query x_ij returns a fresh fair coin if (i,j) in D x R,
  deterministically 1 if (i,j) is matched, deterministically 0 otherwise;
  an affine-linear query returns its constant plus the XOR of the single-variable
  answers on its support (Lemma 1 in cert_floor.md: L is linear, L(1) = 1).

Strategies audited (all deterministic given the pipeline; degree-1 queries only;
fallback label is the fixed pair (0,0)):

  thmT_literal        two-phase tree of Theorem T with the LITERAL phase-1 query
                      Q_i = 1 + sum_j x_ij (answer 1 iff the free-row XOR is 0)
  thmT_literal_retry  same, retrying over all certified pigeons
  qi_full_row_scan    certify ALL pigeons via Q_i, then full-row scans with retry
                      (independent code path; identical decisions to literal_retry)
  rc_parity           row+column parity certificates (Q_i and K_j scans, direct
                      I x J output, rescue scans on single-sided failure)
  rc_nonadaptive      same parity certificates, fixed scan, output only if BOTH
                      sides certified (purely non-adaptive)
  scan_all_counting   query every variable once; COUNT certificates: a row or
                      column showing any number of 1s other than exactly one
                      certifies freeness (killed rows/columns have exactly one 1)
  scan_all_shuffled   same tree with randomized query order (robustness check)
  scan_all_first1     query every variable once and output the first answer-1
                      pair (the naive scan-all baseline)
  thmT_published      the corpus implementation of phase 1 (certifies on free-row
                      XOR = 1, see chi_two_phase.py line 50); this is NOT the
                      answer law of any degree-1 query; audited only to show it
                      reproduces the corpus numbers
  thmT_published_retry

Cross-checks:
  - closed-form predictions for every strategy,
  - exact enumeration over all free-region coin matrices at canonical
    (n,d) = (4,1) and (5,2) (--no-exact2 skips the 2^20 pass).

EXACT FLOOR THEOREM checked here (see cert_floor.md):
  err* = (1 - 2d/n) * (2d+1) * (2d)! / 2^((2d+1)*2d)
  is the optimal error of EVERY adaptive degree-1 tree (no query budget), and
  scan_all_counting achieves it exactly.

Run: python3 cert_floor_check.py [--no-exact2] [--sims N]
"""
from __future__ import annotations

import itertools
import math
import random
import sys

FB = (0, 0)  # fixed fallback label for every tree


# --------------------------------------------------------------------------
# pipeline
# --------------------------------------------------------------------------

class Pipeline:
    """One draw of (rho, coins) under the literal p=2 answer law."""

    def __init__(self, n: int, d: int, rng: random.Random | None = None,
                 coin_rows: tuple[int, ...] | None = None,
                 canonical: bool = False,
                 rho=None, D=None, R=None):
        self.n = n
        self.d = d
        if rho is not None:
            self.rho = rho
            self.D = list(D)
            self.R = list(R)
        elif canonical:
            # killed pigeons 0..n-2d-1 -> killed holes 0..n-2d-1 (rho(i) = i)
            self.rho = {i: i for i in range(n - 2 * d)}
            self.D = list(range(n - 2 * d, n + 1))
            self.R = list(range(n - 2 * d, n))
        else:
            assert rng is not None
            assigned_p = rng.sample(range(n + 1), n - 2 * d)
            assigned_h = rng.sample(range(n), n - 2 * d)
            self.rho = dict(zip(assigned_p, assigned_h))
            self.D = sorted(set(range(n + 1)) - set(assigned_p))
            self.R = sorted(set(range(n)) - set(assigned_h))
        # coin table: one 2d-bit integer per free pigeon (columns in R order)
        if coin_rows is None:
            assert rng is not None
            coin_rows = tuple(rng.getrandbits(2 * d) for _ in self.D)
        self.coin_rows = coin_rows
        self._D_index = {i: t for t, i in enumerate(self.D)}
        self._R_index = {j: t for t, j in enumerate(self.R)}

    def free(self, i: int, j: int) -> bool:
        return i in self._D_index and j in self._R_index

    def answer(self, i: int, j: int) -> int:
        if i in self.rho:
            return 1 if self.rho[i] == j else 0
        t = self._R_index.get(j)
        if t is None:
            return 0
        return (self.coin_rows[self._D_index[i]] >> t) & 1

    def q_row(self, i: int) -> int:
        """Literal degree-1 query Q_i = 1 + sum_j x_ij."""
        acc = 1
        for j in range(self.n):
            acc ^= self.answer(i, j)
        return acc

    def q_col(self, j: int) -> int:
        """Literal degree-1 query K_j = 1 + sum_i x_ij."""
        acc = 1
        for i in range(self.n + 1):
            acc ^= self.answer(i, j)
        return acc


# --------------------------------------------------------------------------
# strategies: each returns (success, reached_fallback)
# --------------------------------------------------------------------------

def thmT_literal(p: Pipeline) -> tuple[int, int]:
    istar = None
    for i in range(p.n + 1):
        if p.q_row(i) == 1:
            istar = i
            break
    if istar is None:
        return (1 if p.free(*FB) else 0), 1
    for j in range(p.n):
        if p.answer(istar, j) == 1:
            return (1 if p.free(istar, j) else 0), 0
    return (1 if p.free(*FB) else 0), 1


def thmT_literal_retry(p: Pipeline) -> tuple[int, int]:
    certified = [i for i in range(p.n + 1) if p.q_row(i) == 1]
    for i in certified:
        for j in range(p.n):
            if p.answer(i, j) == 1:
                return (1 if p.free(i, j) else 0), 0
    return (1 if p.free(*FB) else 0), 1


def qi_full_row_scan(p: Pipeline) -> tuple[int, int]:
    certified = [i for i in range(p.n + 1) if p.q_row(i) == 1]
    for i in certified:
        row_ones = [j for j in range(p.n) if p.answer(i, j) == 1]
        if row_ones:
            return (1 if p.free(i, row_ones[0]) else 0), 0
    return (1 if p.free(*FB) else 0), 1


def rc_parity(p: Pipeline) -> tuple[int, int]:
    I = [i for i in range(p.n + 1) if p.q_row(i) == 1]
    J = [j for j in range(p.n) if p.q_col(j) == 1]
    if I and J:
        return (1 if p.free(I[0], J[0]) else 0), 0
    if not I and J:          # all free rows odd: some free column must be even
        for j in J:
            for i in range(p.n + 1):
                if p.answer(i, j) == 1:
                    return (1 if p.free(i, j) else 0), 0
        return (1 if p.free(*FB) else 0), 1  # unreachable (parity constraint)
    if I and not J:          # all free columns odd: some free row must be even
        for i in I:
            for j in range(p.n):
                if p.answer(i, j) == 1:
                    return (1 if p.free(i, j) else 0), 0
        return (1 if p.free(*FB) else 0), 1  # unreachable (parity constraint)
    return (1 if p.free(*FB) else 0), 1      # unreachable


def rc_nonadaptive(p: Pipeline) -> tuple[int, int]:
    I = [i for i in range(p.n + 1) if p.q_row(i) == 1]
    J = [j for j in range(p.n) if p.q_col(j) == 1]
    if I and J:
        return (1 if p.free(I[0], J[0]) else 0), 0
    return (1 if p.free(*FB) else 0), 1


def counting_output(p: Pipeline, order=None) -> tuple[int, int]:
    """Output pair of scan_all_counting (kept separate for the Bayes audit)."""
    pairs = order if order is not None else [
        (i, j) for i in range(p.n + 1) for j in range(p.n)
    ]
    cnt_p = [0] * (p.n + 1)
    cnt_h = [0] * p.n
    row_ones = [[] for _ in range(p.n + 1)]
    col_ones = [[] for _ in range(p.n)]
    for (i, j) in pairs:
        if p.answer(i, j) == 1:
            cnt_p[i] += 1
            cnt_h[j] += 1
            row_ones[i].append(j)
            col_ones[j].append(i)
    certP = [i for i in range(p.n + 1) if cnt_p[i] != 1]
    certH = [j for j in range(p.n) if cnt_h[j] != 1]
    if certP and certH:
        return (certP[0], certH[0])
    if not certP:
        for j in range(p.n):
            if cnt_h[j] >= 2:
                return (col_ones[j][0], j)
        return FB
    if not certH:
        for i in certP:
            if cnt_p[i] >= 2:
                return (i, row_ones[i][0])
        return (certP[0], FB[1])
    return FB


def scan_all_counting(p: Pipeline, order=None) -> tuple[int, int]:
    out = counting_output(p, order=order)
    return (1 if p.free(*out) else 0), 0


def scan_all_first1(p: Pipeline) -> tuple[int, int]:
    for i in range(p.n + 1):
        for j in range(p.n):
            if p.answer(i, j) == 1:
                return (1 if p.free(i, j) else 0), 0
    return (1 if p.free(*FB) else 0), 1


def _flip_law_q_row(p: Pipeline, i: int) -> int:
    """Corpus implementation's phase-1 law (chi_two_phase.py line 50): killed
    pigeons answer 0, free pigeons certify on XOR(row bits) = 1. Not the
    answer law of any degree-1 query (the literal Q_i certifies on XOR = 0);
    audit only, to show it reproduces the corpus numbers."""
    if i in p.rho:
        return 0
    acc = 0
    for j in p.R:
        acc ^= p.answer(i, j)
    return 1 if acc == 1 else 0


def thmT_published(p: Pipeline) -> tuple[int, int]:
    for i in range(p.n + 1):
        if _flip_law_q_row(p, i) == 1:
            for j in range(p.n):
                if p.answer(i, j) == 1:
                    return (1 if p.free(i, j) else 0), 0
            return (1 if p.free(*FB) else 0), 1  # unreachable in this law
    return (1 if p.free(*FB) else 0), 1


def thmT_published_retry(p: Pipeline) -> tuple[int, int]:
    certified = [i for i in range(p.n + 1) if _flip_law_q_row(p, i) == 1]
    for i in certified:
        for j in range(p.n):
            if p.answer(i, j) == 1:
                return (1 if p.free(i, j) else 0), 0
    return (1 if p.free(*FB) else 0), 1


STRATEGIES = [
    ("thmT_literal", thmT_literal),
    ("thmT_literal_retry", thmT_literal_retry),
    ("qi_full_row_scan", qi_full_row_scan),
    ("rc_parity", rc_parity),
    ("rc_nonadaptive", rc_nonadaptive),
    ("scan_all_counting", scan_all_counting),
    ("scan_all_first1", scan_all_first1),
    ("thmT_published", thmT_published),
    ("thmT_published_retry", thmT_published_retry),
]


# --------------------------------------------------------------------------
# closed-form predictions (include the f-term of the (0,0) fallback)
# --------------------------------------------------------------------------

def f_base(n: int, d: int) -> float:
    return (2 * d + 1) * 2 * d / ((n + 1) * n)


def rc_fail_exact(d: int) -> float:
    """P[F1 u F2] for the rc_parity rescue tree, uniform coin matrix."""
    tot = 0
    for b in range(1, 2 * d + 1, 2):        # F1: rows all odd, even cols zero
        tot += math.comb(2 * d, b) * 2 ** (2 * d * (2 * d - b - 1))
    for a in range(1, 2 * d + 2, 2):        # F2: cols all odd, even rows zero
        tot += math.comb(2 * d + 1, a) * 2 ** ((2 * d - a) * (2 * d - 1))
    return tot / 2 ** ((2 * d + 1) * 2 * d)


def floor_exact(n: int, d: int) -> float:
    """The exact optimal error of every adaptive degree-1 tree (cert_floor.md)."""
    return (1 - 2.0 * d / n) * (2 * d + 1) * math.factorial(2 * d) \
        / 2 ** ((2 * d + 1) * 2 * d)


def predictions(n: int, d: int) -> dict[str, float]:
    f = f_base(n, d)
    m1 = 2.0 ** -(2 * d + 1)
    m2 = 2.0 ** (1 - 2 * d)
    out = {}
    out["thmT_literal"] = (1 - m1) * (1 - m2) + (m1 + (1 - m1) * m2) * f
    out["thmT_literal_retry"] = 1 - ((1 + m2) / 2) ** (2 * d + 1) * (1 - f)
    out["qi_full_row_scan"] = out["thmT_literal_retry"]
    out["rc_parity"] = 1 - rc_fail_exact(d) * (1 - f)
    out["rc_nonadaptive"] = 1 - (m1 + 2.0 ** (-2 * d)) * (1 - f)
    out["scan_all_counting"] = 1 - floor_exact(n, d)
    out["scan_all_first1"] = float("nan")    # no simple closed form
    out["thmT_published"] = 1 - m1 * (1 - f)
    out["thmT_published_retry"] = 1 - m1 * (1 - f)
    return out


# --------------------------------------------------------------------------
# exact enumeration over the free-region coin matrix (canonical Z)
# --------------------------------------------------------------------------

PAR1 = [bin(x).count("1") & 1 for x in range(64)]
CNT = [bin(x).count("1") for x in range(64)]


def exact_enumeration(n: int, d: int) -> dict[str, float]:
    """Exact success over all coin matrices with canonical Z (fallback label
    (0,0) is matched there, so 'strict' = no fallback luck). exact = strict +
    f * P[reach fallback], comparable to the Monte Carlo runs over random Z."""
    width = 2 * d
    nfp = 2 * d + 1
    f = f_base(n, d)
    names = ["thmT_literal", "thmT_literal_retry", "rc_parity", "rc_nonadaptive",
             "scan_all_counting"]
    succ = {k: 0 for k in names}
    fbmass = {k: 0 for k in names}
    total = 2 ** (nfp * width)
    for rows in itertools.product(range(1 << width), repeat=nfp):
        # thmT_literal: first free pigeon with even parity, then its row
        istar = None
        for t, r in enumerate(rows):
            if PAR1[r] == 0:
                istar = t
                break
        if istar is None or rows[istar] == 0:
            fbmass["thmT_literal"] += 1
        else:
            succ["thmT_literal"] += 1
        # thmT_literal_retry: fail iff every even-parity row is all-zero
        fail = all((PAR1[r] == 1) or (r == 0) for r in rows)
        succ["thmT_literal_retry"] += 0 if fail else 1
        fbmass["thmT_literal_retry"] += 1 if fail else 0
        # column aggregates
        col_par = [0] * width
        col_cnt = [0] * width
        for r in rows:
            for b in range(width):
                if (r >> b) & 1:
                    col_par[b] ^= 1
                    col_cnt[b] += 1
        # rc_parity
        I = [t for t, r in enumerate(rows) if PAR1[r] == 0]
        J = [b for b in range(width) if col_par[b] == 0]
        ok = 0
        fb = 0
        if I and J:
            ok = 1
        elif not I and J:
            ok = 1 if any(col_cnt[b] >= 1 for b in J) else 0
            fb = 0 if ok else 1
        elif I and not J:
            ok = 1 if any(rows[t] != 0 for t in I) else 0
            fb = 0 if ok else 1
        else:
            fb = 1
        succ["rc_parity"] += ok
        fbmass["rc_parity"] += fb
        # rc_nonadaptive
        if I and J:
            succ["rc_nonadaptive"] += 1
        else:
            fbmass["rc_nonadaptive"] += 1
        # scan_all_counting
        row_cnt = [CNT[r] for r in rows]
        certP = [t for t in range(nfp) if row_cnt[t] != 1]
        certH = [b for b in range(width) if col_cnt[b] != 1]
        ok = 0
        fb = 0
        if certP and certH:
            ok = 1
        elif not certP:
            # pigeonhole: some column has >= 2 ones; its first one is free
            ok = 1 if any(c >= 2 for c in col_cnt) else 0
            fb = 0 if ok else 1
        elif not certH:
            ok = 1 if any(row_cnt[t] >= 2 for t in certP) else 0
            # class b (all rows <= 1): the Bayes guess (zero-row, killed hole 0)
            # fails under canonical Z, exactly as the flat 2d/n posterior says
            fb = 0
        else:
            fb = 1
        succ["scan_all_counting"] += ok
        fbmass["scan_all_counting"] += fb
    out = {}
    for k in names:
        out[k + "_strict"] = succ[k] / total
        out[k + "_fbmass"] = fbmass[k] / total
        out[k] = succ[k] / total + f * fbmass[k] / total
    return out


# --------------------------------------------------------------------------
# Bayes audit: is scan_all_counting optimal on EVERY answer table M?
# --------------------------------------------------------------------------

def bayes_audit_exhaustive(n: int, d: int) -> None:
    """Enumerate ALL configurations (D, R, mu, coins), group by answer table M,
    and verify on every M-class:
      (a) the counting tree's output pair achieves exactly the maximum pair
          posterior (Bayes-optimality, per class);
      (b) the pooled Bayes error E_M[1 - max posterior] equals floor_exact.
    """
    from itertools import combinations, permutations
    assert (n, d) == (4, 1), "exhaustive audit sized for (4,1)"
    classes = {}
    for D in combinations(range(n + 1), 2 * d + 1):
        for R in combinations(range(n), 2 * d):
            kp = [i for i in range(n + 1) if i not in D]
            kh = [j for j in range(n) if j not in R]
            for mu in permutations(kh):
                rho = dict(zip(kp, mu))
                for bits in range(2 ** ((2 * d + 1) * 2 * d)):
                    coin_rows = tuple(
                        (bits >> (2 * d * t)) & (2 ** (2 * d) - 1)
                        for t in range(2 * d + 1)
                    )
                    p = Pipeline(n, d, rho=dict(rho), D=list(D), R=list(R),
                                 coin_rows=coin_rows)
                    M = tuple(p.answer(i, j) for i in range(n + 1)
                              for j in range(n))
                    out = counting_output(p)
                    ok = 1 if p.free(*out) else 0
                    ent = classes.get(M)
                    if ent is None:
                        ent = {"n": 0, "pair": {}, "ok": 0}
                        classes[M] = ent
                    ent["n"] += 1
                    ent["ok"] += ok
                    for i in D:
                        for j in R:
                            ent["pair"][(i, j)] = ent["pair"].get((i, j), 0) + 1
    err_num = 0
    total = 0
    worst_gap = 0
    multi = 0
    for ent in classes.values():
        best = max(ent["pair"].values())
        if ent["n"] > 1:
            multi += 1
        worst_gap = max(worst_gap, abs(ent["ok"] - best))
        err_num += ent["n"] - best
        total += ent["n"]
    bayes = err_num / total
    pred = floor_exact(n, d)
    print(f"[BAYES] (4,1) exhaustive: {total} configs, {len(classes)} M-classes")
    print(f"  counting tree vs Bayes on every class: max |tree - best pair| "
          f"= {worst_gap:.0f} configs (0 = optimal everywhere)")
    print(f"  E_M[1 - max posterior] = {bayes:.6f}  vs  floor_exact = {pred:.6f}"
          f"  -> {'MATCH' if abs(bayes - pred) < 1e-9 else 'MISMATCH'}")


def bayes_audit_sampled(n: int, d: int, samples: int, seed: int) -> None:
    """Sampled version for (5,2): same per-class optimality check."""
    rng = random.Random(seed)
    classes = {}
    for _ in range(samples):
        p = Pipeline(n, d, rng)
        M = tuple(p.answer(i, j) for i in range(n + 1) for j in range(n))
        out = counting_output(p)
        ok = 1 if p.free(*out) else 0
        ent = classes.get(M)
        if ent is None:
            ent = {"n": 0, "pair": {}, "ok": 0}
            classes[M] = ent
        ent["n"] += 1
        ent["ok"] += ok
        for i in p.D:
            for j in p.R:
                ent["pair"][(i, j)] = ent["pair"].get((i, j), 0) + 1
    err_num = 0
    total = 0
    worst_gap = 0
    witnesses = []
    for M, ent in classes.items():
        best = max(ent["pair"].values())
        gap = ent["ok"] - best
        if gap != 0:
            # Theorem F: any gap must come from class b (all columns exactly
            # one 1, every row at most one 1), where all pair posteriors are
            # flat at 2d/n and small samples fluctuate. Verify that.
            n1 = n + 1
            row_cnt = [sum(M[i1 * n + j1] for j1 in range(n)) for i1 in range(n1)]
            col_cnt = [sum(M[i1 * n + j1] for i1 in range(n1)) for j1 in range(n)]
            is_b = all(c == 1 for c in col_cnt) and all(c <= 1 for c in row_cnt)
            witnesses.append((gap, is_b))
        worst_gap = max(worst_gap, abs(gap))
        err_num += ent["n"] - best
        total += ent["n"]
    bayes = err_num / total
    pred = floor_exact(n, d)
    print(f"[BAYES] (5,2) sampled ({samples} configs): "
          f"{len(classes)} distinct M-classes")
    print(f"  per-class max |tree - best pair| = {worst_gap} "
          f"(single-config classes give 0 by construction; multi-config "
          f"classes test optimality)")
    if witnesses:
        print(f"  {len(witnesses)} gapped class(es); all class-b: "
              f"{all(isb for _, isb in witnesses)} "
              f"(gaps {[g for g, _ in witnesses]}); a nonzero gap on a "
              f"NON-class-b table would refute Theorem F")
    print(f"  E_M[1 - max posterior] ~= {bayes:.3e}  vs  floor_exact = "
          f"{pred:.3e}")


# --------------------------------------------------------------------------
# Monte Carlo
# --------------------------------------------------------------------------

def mc_point(n: int, d: int, sims: int, seed: int) -> dict[str, float]:
    rng = random.Random(seed)
    acc = {name: 0 for name, _ in STRATEGIES}
    for _ in range(sims):
        p = Pipeline(n, d, rng)
        for name, fn in STRATEGIES:
            acc[name] += fn(p)[0]
    return {name: acc[name] / sims for name, _ in STRATEGIES}


def mc_point_counting_shuffled(n: int, d: int, sims: int, seed: int) -> float:
    rng = random.Random(seed)
    s = 0
    for _ in range(sims):
        p = Pipeline(n, d, rng)
        pairs = [(i, j) for i in range(p.n + 1) for j in range(p.n)]
        rng.shuffle(pairs)
        s += scan_all_counting(p, order=pairs)[0]
    return s / sims


# --------------------------------------------------------------------------
# main
# --------------------------------------------------------------------------

def main() -> None:
    args = sys.argv[1:]
    exact2 = "--no-exact2" not in args
    sims_override = None
    if "--sims" in args:
        sims_override = int(args[args.index("--sims") + 1])

    print("certification-floor audit, Omega(n,d) pipeline at p=2")
    print("channel law: single variable: free -> fair coin, matched -> 1, else 0;")
    print("             affine-linear query = constant + XOR of single answers")
    print("fallback label (0,0) for every tree; f = (2d+1)*2d/((n+1)*n)")
    print()

    points = [(32, 2, sims_override or 2000), (64, 2, sims_override or 1500),
              (64, 4, sims_override or 800)]
    seeds = {32: 271828, 64: 141421}
    for (n, d, sims) in points:
        print(f"[MC] n={n} d={d} sims={sims}")
        res = mc_point(n, d, sims, seeds[n])
        sh = mc_point_counting_shuffled(n, d, sims, seeds[n] + 7)
        preds = predictions(n, d)
        bench = 1 - 2.0 ** -(2 * d + 1)
        print(f"  {'strategy':<22} {'measured':>9} {'pred':>10} "
              f"{'bench':>8} {'beats bench':>12}")
        for name, _ in STRATEGIES:
            val = res[name]
            pred = preds.get(name, float("nan"))
            se = (max(val, 1e-12) * (1 - min(val, 1 - 1e-12)) / sims) ** 0.5
            beats = "YES" if val > bench + 2.9 * se else "no"
            print(f"  {name:<22} {val:>9.4f} {pred:>10.4f} {bench:>8.4f} {beats:>12}")
        print(f"  {'scan_all_shuffled':<22} {sh:>9.4f} {res['scan_all_counting']:>10.4f}"
              f"   (shuffled vs fixed order, must agree within noise)")
        print(f"  exact floor err* = {floor_exact(n, d):.3e} -> optimal success "
              f"{1 - floor_exact(n, d):.7f}")
        print(f"  benchmark 1 - 2^-(2d+1) = {bench:.7f}")
        print()

    print("[BAYES] exhaustive Bayes audit: is scan_all_counting optimal on")
    print("        every answer table M? (ground truth for the floor theorem)")
    bayes_audit_exhaustive(4, 1)
    bayes_audit_sampled(5, 2, sims_override or 200000, 7777)
    print()
    print("[EXACT] enumeration over all free-region coin matrices, canonical Z")
    print("        (fallback (0,0) is matched under canonical Z: 'strict' has no")
    print("         fallback luck; 'exact' adds f * P[reach fallback] ~ MC)")
    res1 = exact_enumeration(4, 1)
    print(f"  (n,d)=(4,1): {2 ** 6} matrices")
    for k in ["thmT_literal", "thmT_literal_retry", "rc_parity", "rc_nonadaptive",
              "scan_all_counting"]:
        print(f"    {k:<22} exact={res1[k]:.6f} (strict {res1[k+'_strict']:.6f}, "
              f"fb {res1[k+'_fbmass']:.4f})")
    print(f"    scan_all_counting closed form: strict "
          f"{1 - (2 * 1 + 1) * math.factorial(2 * 1) / 2 ** ((2 * 1 + 1) * 2 * 1):.6f}, "
          f"random-Z {1 - floor_exact(4, 1):.6f}")
    if exact2:
        res2 = exact_enumeration(5, 2)
        print(f"  (n,d)=(5,2): {2 ** 20} matrices")
        for k in ["thmT_literal", "thmT_literal_retry", "rc_parity", "rc_nonadaptive",
                  "scan_all_counting"]:
            print(f"    {k:<22} exact={res2[k]:.7f} (strict {res2[k+'_strict']:.7f}, "
                  f"fb {res2[k+'_fbmass']:.4f})")
        print(f"    scan_all_counting closed form: strict "
              f"{1 - (2 * 2 + 1) * math.factorial(2 * 2) / 2 ** ((2 * 2 + 1) * 2 * 2):.7f}, "
              f"random-Z {1 - floor_exact(5, 2):.7f}")
    print()
    print("summary: scan_all_counting is optimal by the exact floor theorem;")
    print(f"err* at (32,2) = {floor_exact(32, 2):.3e} << 2^-5 = {2**-5:.3e};")
    print(f"err* at (64,4) = {floor_exact(64, 4):.3e} << 2^-9 = {2**-9:.3e}.")
    print("The 2^{-Theta(d)} certification-floor conjecture and Theorem T's")
    print("optimality within the degree-1 family are both FALSE.")


if __name__ == "__main__":
    main()
