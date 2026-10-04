"""Verification of deg2_theory.md: true-channel facts, per-leaf posterior
formulas, the K_j column-parity tree's exact law, and the budgeted cap.

deg2-theory agent script (2026-10-03). Channel: the TRUE Omega(n,d) pipeline at
p = 2 - uniform designs of the restricted canonical system (the design coset,
NOT chi_p2_adaptive.build()'s e_0 + kernel coset; see kernel_structure.py).
Verified clauses:
  V1. true-channel structure facts at canonical (2,1) [exhaustive, 8 designs]
      and (4,2) [sampled]: row parities forced 1; L(Q_i) = 0; K_j answers 1 on
      exactly the even free columns; the diagonal coordinate d(00;11) is fair
      and jointly uniform with its component singles x_00, x_11 (all 8
      patterns occur); same-line degree-2 coordinates answer 0.
  V2. Theorem 2 (deg2_theory.md): post(0) = q; post(k) closed form at
      k = 1, 5, 15; post_full = (2d+1)2d/((2d+1)2d + (n-2d))  [Monte Carlo,
      Clopper-Pearson 99% intervals, chi_thmT_verify.py machinery pattern].
  V3. Theorem 4: K_j-tree exact error law
        err_K = sum_{s odd} C(2d,s) 2^{2d(s-1)} / 2^{(2d+1)(2d-1)}
      at (32,2) and (48,4) [Monte Carlo] plus digit-exact enumeration over all
      2^15 odd-row canonical matrices at the (5,2) scale.
  V4. Theorem 5: full single-variable scan certifies with probability 1
      (zero failures at (32,2)).
  V5. Theorem 4b: budgeted K_j-tree at B in {10,30,100,300,1000} vs its split
      prediction; also vs the single-scan baseline (first-hit labeling).
  V6. the analytic chain constant h1 (1 - (1 - q(2d-1)/(2(n-1)))^6) vs
      and_chain.md's measured 0.0018-0.0026 at (32,2).

Run: python3 chi_deg2_theory_check.py [--smoke]
"""
from __future__ import annotations

import math
import random
import sys
from itertools import product

from razborov_check import gf2_rank, monomials, shift, system_polys, to_vec

ALPHA = 0.01  # two-sided 99% Clopper-Pearson


# ---------- true-design space construction (independent, canonical route) ----------
# New-kernel_structure.py F1: the outer-reading and canonical constraint sets
# coincide (V(n,d)^rho = V(2d,d) exactly), so the canonical construction below
# is the printed-definition design space.

def design_space(d: int):
    """Design coset {L : L kills V(2d,d), L(1)=1} as particular + kernel basis."""
    n = 2 * d
    monos = monomials(n, d)
    mi = {t: i for i, t in enumerate(monos)}
    rows = []
    for f in system_polys(n):
        df = max(len(t) for t in f)
        for h in monos:
            if len(h) + df <= d:
                rows.append(to_vec(shift(f, h), mi))
    e0 = 1 << mi[()]
    rows.append(e0)  # impose L(1) = 0 on the kernel; designs = particular + K
    piv = {}
    for v in rows:
        while v:
            hbit = v.bit_length() - 1
            if hbit in piv:
                v ^= piv[hbit]
            else:
                piv[hbit] = v
                break
    # particular solution with L(1) = 1 (e0 row's rhs)
    Lp = 0
    for c in sorted(piv):
        p = piv[c]
        mask = p & ~(1 << c)
        rhs = 1 if c == mi[()] else 0
        if (bin(Lp & mask).count("1") & 1) ^ rhs:
            Lp |= 1 << c
    # self-check: Lp kills every V row and has L(1) = 1
    for v in rows[:-1]:
        assert (bin(Lp & v).count("1") & 1) == 0, "particular design fails V"
    assert (Lp >> mi[()]) & 1 == 1
    # kernel basis: one vector per free column
    kb = []
    for fc in range(len(monos)):
        if fc in piv:
            continue
        y = 1 << fc
        for c in sorted(piv):
            mask = piv[c] & ~(1 << c)
            if bin(y & mask).count("1") & 1:
                y |= 1 << c
        kb.append(y)
    # project onto the single-variable coordinates
    single = [mi[(v,)] for v in range((n + 1) * n)]
    proj = []
    for y in kb:
        v = 0
        for k, c in enumerate(single):
            if (y >> c) & 1:
                v |= 1 << k
        proj.append(v)
    red = {}
    for v in proj:
        while v:
            hbit = v.bit_length() - 1
            if hbit in red:
                v ^= red[hbit]
            else:
                red[hbit] = v
                break
    red_rows = [red[c] for c in sorted(red)]
    Lp_mask = 0
    for k, c in enumerate(single):
        if (Lp >> c) & 1:
            Lp_mask |= 1 << k
    return dict(n=n, d=d, kb=kb, Lp=Lp, mono_index=mi,
                red_rows=red_rows, Lp_mask=Lp_mask)


# ---------- exact binomial CP intervals ----------

def binom_cdf(k: int, n: int, p: float) -> float:
    """P[X <= k], X ~ Bin(n,p) = 1 - sum_{i=k+1..n} pmf(i).

    Exact: starts at the mode (no underflow) and recurses both directions.
    """
    if k < 0:
        return 0.0
    if k >= n:
        return 1.0
    if p <= 0.0:
        return 1.0
    if p >= 1.0:
        return 0.0
    q = 1.0 - p
    sd = math.sqrt(n * p * q)
    if k + 1 < n * p - 300.0 * sd:
        return 0.0
    if k + 1 > n * p + 300.0 * sd:
        return 1.0
    m = min(n, int(n * p))
    lc = (math.lgamma(n + 1) - math.lgamma(m + 1) - math.lgamma(n - m + 1)
          + m * math.log(p) + (n - m) * math.log(q))
    pmf = math.exp(lc)
    if k + 1 > m:
        # tail starts above the mode: recurse upward from k+1
        lc = (math.lgamma(n + 1) - math.lgamma(k + 2) - math.lgamma(n - k)
              + (k + 1) * math.log(p) + (n - k - 1) * math.log(q))
        t = math.exp(lc)
        s_right = 0.0
        i = k + 1
        while i <= n and t > 0.0:
            s_right += t
            i += 1
            if i <= n:
                t *= (n - i + 1) / i * (p / q)
        return min(1.0, max(0.0, 1.0 - s_right))
    # right part: sum_{i=m..n}
    s_right = 0.0
    t = pmf
    i = m
    while i <= n and t > 0.0:
        s_right += t
        i += 1
        if i <= n:
            t *= (n - i + 1) / i * (p / q)
    # left part: sum_{i=k+1..m-1}
    s_left = 0.0
    t = pmf
    i = m
    while i - 1 >= k + 1 and t > 0.0:
        t *= i / (n - i + 1) * (q / p)
        i -= 1
        s_left += t
    return min(1.0, max(0.0, 1.0 - (s_left + s_right)))


def cp_ci(k: int, n: int, alpha: float = ALPHA) -> tuple[float, float]:
    if k <= 0:
        lo = 0.0
    else:
        glo, ghi = 0.0, 1.0
        for _ in range(80):
            mid = 0.5 * (glo + ghi)
            if 1.0 - binom_cdf(k - 1, n, mid) > alpha / 2:
                ghi = mid
            else:
                glo = mid
        lo = 0.5 * (glo + ghi)
    if k >= n:
        hi = 1.0
    else:
        glo, ghi = 0.0, 1.0
        for _ in range(80):
            mid = 0.5 * (glo + ghi)
            if binom_cdf(k, n, mid) > alpha / 2:
                glo = mid
            else:
                ghi = mid
        hi = 0.5 * (glo + ghi)
    return lo, hi


def _self_test() -> None:
    lo, hi = cp_ci(0, 10, 0.05)
    assert lo == 0.0 and abs(hi - 0.30850) < 5e-4, (lo, hi)
    lo, hi = cp_ci(10, 10, 0.05)
    assert hi == 1.0 and abs(lo - 0.69150) < 5e-4, (lo, hi)
    lo, hi = cp_ci(97, 100, 0.05)
    assert lo < 0.97 < hi, (lo, hi)
    assert abs(binom_cdf(50, 100, 0.5) - 0.5397946) < 1e-6
    assert abs(binom_cdf(10, 10, 0.5) - 1.0) < 1e-12


# ---------- true-design channel at the restricted canonical system ----------

CH: dict = {}


def channel_setup(d: int) -> dict:
    """Design coset machinery + projected single-coordinate sampler, (2d, d)."""
    return design_space(d)


def sample_design_restriction(ch: dict, rng: random.Random) -> int:
    v = ch["Lp_mask"]
    for row in ch["red_rows"]:
        if rng.random() < 0.5:
            v ^= row
    return v


def v1_structure() -> None:
    print("[V1] true-channel structure facts (design coset, not e_0+kernel)")
    # (2,1): exhaustive, 8 designs
    ch = CH[(2, 1)]
    n, mi = ch["n"], ch["mono_index"]
    ok_par = ok_q = True
    for mask in range(1 << len(ch["kb"])):
        L = ch["Lp"]
        for b in range(len(ch["kb"])):
            if (mask >> b) & 1:
                L ^= ch["kb"][b]
        for i in range(n + 1):
            row = [(L >> mi[(i * n + j,)]) & 1 for j in range(n)]
            ok_par &= (sum(row) % 2 == 1)
            ok_q &= ((1 + sum(row)) % 2 == 0)
    print(f"  (2,1) exhaustive 8 designs: row parity 1 everywhere: {ok_par}; "
          f"L(Q_i) = 0 everywhere: {ok_q} -> "
          f"{'PASS' if ok_par and ok_q else 'FAIL'}")
    # (4,2): sampled; the restriction carries ONLY the (n+1)n single
    # coordinates (bit k = canonical single k = (k // n, k % n))
    ch = CH[(4, 2)]
    n, d = ch["n"], ch["d"]
    rng = random.Random(20261003)
    nsam = 40 if "--smoke" in sys.argv else 4000
    bad = dict(par=0, q=0, kj=0)
    for _ in range(nsam):
        L = sample_design_restriction(ch, rng)
        rows = [[(L >> (i * n + j)) & 1 for j in range(n)]
                for i in range(n + 1)]
        if any(sum(r) % 2 != 1 for r in rows):
            bad["par"] += 1
        if any((1 + sum(r)) % 2 != 0 for r in rows):
            bad["q"] += 1
        for j in range(n):
            col = [rows[i][j] for i in range(n + 1)]
            if ((1 + sum(col)) % 2 == 1) != (sum(col) % 2 == 0):
                bad["kj"] += 1
    allbad = bad["par"] + bad["q"] + bad["kj"]
    print(f"  (4,2) sampled {nsam} designs: parity violations {bad['par']}, "
          f"L(Q_i) violations {bad['q']}, K_j-law violations {bad['kj']} -> "
          f"{'PASS' if allbad == 0 else 'FAIL'}")
    # degree-2 facts on a separate singles+diagonals projection
    monos_full = monomials(n, d)
    mi_full = {t: i for i, t in enumerate(monos_full)}
    diag = [mi_full[t] for t in monos_full
            if len(t) == 2 and t[0] // n != t[1] // n
            and t[0] % n != t[1] % n]
    single = [mi_full[(v,)] for v in range((n + 1) * n)]
    coords = single + diag
    cpos = {c: k for k, c in enumerate(coords)}
    proj = []
    for y in ch["kb"]:
        v = 0
        for k, c in enumerate(coords):
            if (y >> c) & 1:
                v |= 1 << k
        proj.append(v)
    red = {}
    for v in proj:
        while v:
            hbit = v.bit_length() - 1
            if hbit in red:
                v ^= red[hbit]
            else:
                red[hbit] = v
                break
    red_rows = [red[c] for c in sorted(red)]
    Lp_mask = 0
    for k, c in enumerate(coords):
        if (ch["Lp"] >> c) & 1:
            Lp_mask |= 1 << k

    def samp():
        v = Lp_mask
        for row in red_rows:
            if rng.random() < 0.5:
                v ^= row
        return v

    da = cpos[mi_full[tuple(sorted((0 * n + 0, 1 * n + 1)))]]
    xa = cpos[mi_full[(0 * n + 0,)]]
    xb = cpos[mi_full[(1 * n + 1,)]]
    # same-line products are pivot (determined 0): check on FULL design vectors
    sp_f = mi_full[tuple(sorted((0 * n + 0, 0 * n + 1)))]
    sh_f = mi_full[tuple(sorted((0 * n + 0, 1 * n + 0)))]
    counts8 = [0] * 8
    bad_line = 0
    diag_ones = diag_tot = 0
    for _ in range(nsam):
        v = samp()
        ksub = 0
        for b in range(len(ch["kb"])):
            if rng.random() < 0.5:
                ksub |= 1 << b
        Lfull = ch["Lp"]
        for b in range(len(ch["kb"])):
            if (ksub >> b) & 1:
                Lfull ^= ch["kb"][b]
        if (Lfull >> sp_f) & 1:
            bad_line += 1
        if (Lfull >> sh_f) & 1:
            bad_line += 1
        av, bv, dv = (v >> xa) & 1, (v >> xb) & 1, (v >> da) & 1
        counts8[av * 4 + bv * 2 + dv] += 1
        for c in diag:
            diag_tot += 1
            diag_ones += (v >> cpos[c]) & 1
    all8 = all(c > 0 for c in counts8)
    exp8 = nsam / 8.0
    ok8 = all8 and all(abs(c - exp8) < 4 * math.sqrt(exp8) for c in counts8)
    dmarg = diag_ones / max(diag_tot, 1)
    okm = abs(dmarg - 0.5) < 4 * math.sqrt(0.25 / max(diag_tot, 1))
    print(f"  (4,2) same-line degree-2 products answering 1: {bad_line} "
          f"(theorem: 0) -> {'PASS' if bad_line == 0 else 'FAIL'}")
    print(f"  (4,2) {{d(00;11), x_00, x_11}} pattern counts: {counts8} -> "
          f"all 8 present within 4 sigma: {'PASS' if ok8 else 'FAIL'} "
          f"(independence)")
    print(f"  (4,2) diagonal-coordinate marginal: {dmarg:.4f} over {diag_tot} "
          f"reads (fair: 0.5) -> {'PASS' if okm else 'FAIL'}")


# ---------- outer pipeline Monte Carlo ----------

def make_channel(n: int, d: int, rng: random.Random):
    """One sampled (rho, design restriction); returns ans, ansK, free, D, R."""
    ch = CH[(2 * d, d)]
    Lres = sample_design_restriction(ch, rng)
    ap = rng.sample(range(n + 1), n - 2 * d)
    ah = rng.sample(range(n), n - 2 * d)
    rho = dict(zip(ap, ah))
    D = sorted(set(range(n + 1)) - set(ap))
    R = sorted(set(range(n)) - set(ah))
    rho_inv = set(rho.values())
    canon = {(i, j): pi * (2 * d) + hj
             for pi, i in enumerate(D) for hj, j in enumerate(R)}
    free = {(i, j) for i in D for j in R}

    def ans(pair):
        i, j = pair
        if i in rho:
            return 1 if rho[i] == j else 0
        if j in rho_inv:
            return 0
        return (Lres >> canon[(i, j)]) & 1

    def ansK(j):
        if j not in rho_inv:
            x = 0
            for i in D:
                x ^= (Lres >> canon[(i, j)]) & 1
            return 1 ^ x  # 1 + XOR over the 2d+1 free-pigeon bits
        return 0
    return ans, ansK, free, D, R


def v2_posteriors(n: int, d: int, n_sim: int, rng: random.Random) -> None:
    print(f"\n[V2] Theorem 2 per-leaf posteriors at ({n},{d})")
    A = (2 * d + 1) / (n + 1)
    m = (n - 2 * d) / ((n + 1) * n)

    def FB(k):
        tot = 0.0
        cn = math.comb(n, 2 * d)
        for t in range(0, min(k, 2 * d - 1) + 1):
            w = 2.0 ** (-min(t + 1, 2 * d - 1))
            tot += (math.comb(k, t) * math.comb(n - k - 1, 2 * d - 1 - t)
                    * w / cn)
        return tot

    q = (2 * d + 1) * d / ((2 * d + 1) * d + (n - 2 * d))
    rho2a = ((2 * d + 1) * 2 * d * 2.0 ** (1 - 2 * d)
             / ((2 * d + 1) * 2 * d * 2.0 ** (1 - 2 * d) + (n - 2 * d)))
    print(f"  closed forms: q = post(0) = {q:.6f}; post_full = rho_2a = "
          f"{rho2a:.6f}")
    ks = [1, 5, 15] if d >= 2 else [1]
    pred = {0: q}
    pred.update({k: A * FB(k) / (A * FB(k) + m) for k in ks})
    hits = {k: [0, 0] for k in ks + [0]}
    full = [0, 0]
    for _ in range(n_sim):
        ans, _, free, D, R = make_channel(n, d, rng)
        i = rng.randrange(n + 1)
        order = list(range(n))
        rng.shuffle(order)
        first = None
        for pos, j in enumerate(order):
            if ans((i, j)) == 1:
                first = (pos, j)
                break
        if first is not None:
            k, j = first
            if k in hits:
                hits[k][0] += 1
                hits[k][1] += int((i, j) in free)
            if k == n - 1:
                full[0] += 1
                full[1] += int((i, j) in free)
    verdict = "PASS"
    for k in sorted(hits):
        tot, fre = hits[k]
        if tot < 5:
            print(f"  post({k}): only {tot} strata; skipped")
            continue
        lo, hi = cp_ci(fre, tot)
        p = pred[k]
        ok = lo <= p <= hi
        verdict = verdict if ok else "FAIL"
        print(f"  post({k}): {fre}/{tot} = {fre / tot:.4f} "
              f"[{lo:.4f},{hi:.4f}] vs {p:.6f} -> {'PASS' if ok else 'FAIL'}")
    if full[0] >= 5:
        lo, hi = cp_ci(full[1], full[0])
        ok = lo <= rho2a <= hi
        verdict = verdict if ok else "FAIL"
        print(f"  post_full: {full[1]}/{full[0]} = {full[1] / full[0]:.4f} "
              f"[{lo:.4f},{hi:.4f}] vs {rho2a:.6f} -> "
              f"{'PASS' if ok else 'FAIL'}")
    else:
        print(f"  post_full: only {full[0]} strata (rare at this n); skipped")
    print(f"  [V2] overall: {verdict}")


def err_K_exact(d: int) -> float:
    num = sum(math.comb(2 * d, s) * 2 ** (2 * d * (s - 1))
              for s in range(1, 2 * d, 2))
    return num / 2.0 ** ((2 * d + 1) * (2 * d - 1))


def make_channel_struct(n: int, d: int, rng: random.Random):
    """Structural sampler: exact single-coordinate law (uniform odd rows),
    justified by the design-space theorems (new kernel_structure.py F2/F3:
    row parity is the ONLY single-coordinate constraint). Used for points
    whose full design space is too large to build exactly ((48,4) etc.)."""
    ap = rng.sample(range(n + 1), n - 2 * d)
    ah = rng.sample(range(n), n - 2 * d)
    rho = dict(zip(ap, ah))
    D = sorted(set(range(n + 1)) - set(ap))
    R = sorted(set(range(n)) - set(ah))
    rho_inv = set(rho.values())
    Rset = set(R)
    row_bits = {}
    for i in D:
        bits = [rng.randrange(2) for _ in range(2 * d)]
        if sum(bits) % 2 == 0:
            bits[0] ^= 1  # uniform odd pattern
        for hj, j in enumerate(R):
            row_bits[(i, j)] = bits[hj]

    def ans(pair):
        i, j = pair
        if i in rho:
            return 1 if rho[i] == j else 0
        if j in rho_inv:
            return 0
        return row_bits[(i, j)]

    def ansK(j):
        if j in Rset:
            x = 0
            for i in D:
                x ^= ans((i, j))
            return 1 ^ x
        return 0
    free = {(i, j) for i in D for j in R}
    return ans, ansK, free, D, R


def v3_ktree(n: int, d: int, n_sim: int, rng: random.Random,
             structural: bool = False) -> None:
    print(f"\n[V3] Theorem 4 K_j-tree (full budget) at ({n},{d})"
          f"{' [structural sampler]' if structural else ''}")
    maker = make_channel_struct if structural else make_channel
    ek = err_K_exact(d)
    f = (2 * d + 1) * 2 * d / ((n + 1) * n)
    pred = 1 - (1 - f) * ek
    succ = 0
    for _ in range(n_sim):
        ans, ansK, free, D, R = maker(n, d, rng)
        out = None
        for j in range(n):
            if ansK(j) == 1:
                for i in range(n + 1):
                    if ans((i, j)) == 1:
                        out = (i, j)
                        break
            if out:
                break
        if out is None:
            out = (rng.randrange(n + 1), rng.randrange(n))
        succ += int(out in free)
    lo, hi = cp_ci(succ, n_sim)
    ok = lo <= pred <= hi
    print(f"  success {succ}/{n_sim} = {succ / n_sim:.6f} [{lo:.6f},{hi:.6f}] "
          f"vs pred 1-(1-f)err_K = {pred:.6f} (err_K = {ek:.3e}) -> "
          f"{'PASS' if ok else 'FAIL'}")


def v3_enum() -> None:
    print("\n[V3b] exact enumeration at canonical (5,2): all 2^15 odd-row "
          "5x4 matrices")
    cnt = tot = 0
    odd = [p for p in product(range(2), repeat=4) if sum(p) % 2 == 1]
    for rows in product(odd, repeat=5):
        tot += 1
        cols = [sum(r[j] for r in rows) for j in range(4)]
        if all(c % 2 == 1 or c == 0 for c in cols):
            cnt += 1
    pred_cnt = round(err_K_exact(2) * 2 ** 15)
    ok = cnt == pred_cnt
    print(f"  fail matrices {cnt}/{tot} = {cnt / tot:.6f}; formula count "
          f"= {pred_cnt} -> {'PASS (digit-exact)' if ok else 'FAIL'}")


def v4_fullscan(n: int, d: int, n_sim: int, rng: random.Random) -> None:
    print(f"\n[V4] Theorem 5 full-scan certainty at ({n},{d})")
    fails = 0
    for _ in range(n_sim):
        ans, _, free, D, R = make_channel(n, d, rng)
        colcnt = [0] * n
        rowcnt = [0] * (n + 1)
        for i in range(n + 1):
            for j in range(n):
                if ans((i, j)) == 1:
                    rowcnt[i] += 1
                    colcnt[j] += 1
        found = any(c >= 2 for c in rowcnt) or any(c >= 2 for c in colcnt)
        if not found:
            fails += 1
    print(f"  {n_sim} full scans: certificate-absent failures = {fails} "
          f"(theorem: 0) -> {'PASS' if fails == 0 else 'FAIL'}")


def v5_budgeted(n: int, d: int, budgets, n_sim: int,
                rng: random.Random) -> None:
    print(f"\n[V5] Theorem 4b budgeted K_j-tree vs single baseline at ({n},{d})")
    q = (2 * d + 1) * d / ((2 * d + 1) * d + (n - 2 * d))
    h1 = ((2 * d + 1) * d + (n - 2 * d)) / ((n + 1) * n)
    f = (2 * d + 1) * 2 * d / ((n + 1) * n)
    print(f"  single-scan cap reference: q = {q:.4f}; h1 = {h1:.4f}")
    allpairs = [(i, j) for i in range(n + 1) for j in range(n)]
    for B in budgets:
        succ = succ_single = 0
        for _ in range(n_sim):
            ans, ansK, free, D, R = make_channel(n, d, rng)
            ncols = min(B // 2, n)
            cols = rng.sample(range(n), ncols)
            cert = [j for j in cols if ansK(j) == 1]
            out = None
            budget = B - ncols
            for j in cert:
                for i in range(n + 1):
                    if budget <= 0:
                        break
                    budget -= 1
                    if ans((i, j)) == 1:
                        out = (i, j)
                        break
                if out or budget <= 0:
                    break
            if out is None:
                out = (rng.randrange(n + 1), rng.randrange(n))
            succ += int(out in free)
            pairs = rng.sample(allpairs, min(B, len(allpairs)))
            hit = next((p for p in pairs if ans(p) == 1), None)
            if hit is None:
                hit = (rng.randrange(n + 1), rng.randrange(n))
            succ_single += int(hit in free)
        # split prediction: alpha = y/(x+y), x = Bd/n, y = B(2d+1)/(2(n+1)),
        # capped by the pure-tree full-budget ceiling 1-(1-f)err_K
        x = B * d / n
        y = B * (2 * d + 1) / (2.0 * (n + 1))
        a = y / (x + y) if x + y > 0 else 0.5
        ceiling = 1 - (1 - f) * err_K_exact(d)
        pred = min(ceiling,
                   (1 - math.exp(-a * x)) * (1 - math.exp(-(1 - a) * y))
                   + f * math.exp(-a * x) * math.exp(-(1 - a) * y))
        se = math.sqrt(max(pred * (1 - pred), 1e-12) / n_sim)
        ok = succ / n_sim >= pred - 3 * se  # Theorem 4b is a LOWER bound
        lo, hi = cp_ci(succ, n_sim)
        print(f"  B={B:>5}: K-tree {succ / n_sim:.4f} [{lo:.4f},{hi:.4f}] vs "
              f"split pred {pred:.4f} (ceiling {ceiling:.4f}) -> "
              f"{'PASS' if ok else 'FAIL'}; "
              f"single {succ_single / n_sim:.4f}; K>single: "
              f"{'YES' if succ > succ_single else 'no'}")


def v6_chain_constant(n: int, d: int) -> None:
    q = (2 * d + 1) * d / ((2 * d + 1) * d + (n - 2 * d))
    h1 = ((2 * d + 1) * d + (n - 2 * d)) / ((n + 1) * n)
    k = 6
    c = h1 * (1 - (1 - q * (2 * d - 1) / (2 * (n - 1))) ** k)
    print(f"\n[V6] analytic chain constant at ({n},{d}), k = {k}: "
          f"h1 (1-(1-q(2d-1)/(2(n-1)))^k) = {c:.5f} per query "
          f"(and_chain measured -ln(1-cert)/B = 0.0018-0.0026)")


def main() -> None:
    smoke = "--smoke" in sys.argv
    _self_test()
    global CH
    CH[(2, 1)] = channel_setup(1)
    CH[(4, 2)] = channel_setup(2)
    print("chi_deg2_theory_check: verification of deg2_theory.md on the TRUE "
          "pipeline channel\n")
    v1_structure()
    rng = random.Random(271828)
    if smoke:
        print("\n[smoke mode: reduced simulation counts]")
        v2_posteriors(32, 2, 30000, rng)
        v3_ktree(32, 2, 3000, rng)
        v3_enum()
        v4_fullscan(32, 2, 500, random.Random(5))
        v5_budgeted(32, 2, [30, 100], 2000, rng)
        v6_chain_constant(32, 2)
        return
    v2_posteriors(32, 2, 300000, rng)
    v3_ktree(32, 2, 20000, rng)
    v3_ktree(48, 4, 40000, rng, structural=True)
    v3_enum()
    v4_fullscan(32, 2, 5000, random.Random(5))
    v5_budgeted(32, 2, [10, 30, 100, 300, 1000], 20000, rng)
    v6_chain_constant(32, 2)


if __name__ == "__main__":
    main()
