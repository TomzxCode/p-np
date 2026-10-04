"""Verification of odd_p_theory.md: the odd-prime (F_p) Omega(n,d) answer
channel, certificate inventory, per-hit posteriors, the K_j-tree error law,
and the budgeted cap at p > 2.  [docstring continued at end of file]"""
from __future__ import annotations
# Full docstring (raw string, kept after imports to avoid escape warnings):
# odd-p-theory agent script (2026-10-04). Channel: the TRUE pipeline at
# characteristic p (uniform designs of the restricted canonical system over
# F_p). Structural driver (PROVED in odd_p_theory.md): the row axiom
# Q_i = 1 - sum_j x_ij is an EQUALITY over F_p, so free-row design values are
# locked to sum = 1 at EVERY p (the p > 2 form of the p = 2 XOR = 1 lock),
# while injectivity stays an INEQUALITY (collision monomials), so columns are
# unconstrained. Row-sum queries are therefore dead at every p; column
# queries and the value-based certificates carry the channel.
#
# Self-contained GF(p) sparse linear algebra (the corpus toolkit
# razborov_check.py / kernel_structure.py is GF(2)-bitmask based);
# monomials() is imported from razborov_check.py (characteristic-independent
# variable indexing: variable (i, j), 0-based, = i * nfr + j).
#
# Scale facts: kernel work lives at the restricted systems (2,1) and (4,2)
# (degree <= 2); the (6,3) degree-3 build over F_p is out of reach for
# tuple-based GF(p) elimination and is flagged in odd_p_theory.md, not run.
# Outer pipeline work: (7,2) exhaustive (11760 restrictions, exact projected
# design cosets), (8,2) status-level exact (211680), (15,2) Monte Carlo on
# the proved closed forms.
#
# Verified clauses:
#   V0. builds at (2,1),(4,2) for p in {2,3,5}: 1 not in V; rank V; dim Des;
#       p = 2 regressions (corpus tables 165/65 and 3/3). NEW: rank and
#       dim Des are IDENTICAL at p = 2, 3, 5 ((4,2): 165/65).
#   V1. channel law at (4,2), p in {2,3,5}: the single-table law (product of
#       per-row sum-1 hyperplanes, exact projected-kernel dimension + sampled
#       row sums); a full free row = exactly the p^(2d-1) hyperplane points;
#       row-incomplete windows jointly uniform over F_p^T; the star sum rule
#       over F_p (single-variable base g); the alias law ans(x^2) = ans(x);
#       the nonzero-count law on a full free row.
#   V2. certificate soundness at outer (7,2), exhaustive over all 11760
#       restrictions with exact projected-design cosets: self-certification
#       (answer in F_p minus {0,1}), adjacency (two nonzeros co-row or
#       co-column), Z ({ans(x_p) != 1, ans(m) != 0}), K_j (killed columns
#       determined 0; free columns uniform, K_j uniform), wedge (two
#       nonzeros through a pigeon); exact per-attempt rates at p = 2, 3.
#   V3. posteriors: q_p, post0_p, q_p^neq0, colq_p (K_j = 0), q_and_p:
#       closed forms digit-exact vs restriction enumeration ((7,2) design+
#       status level, (8,2)/(9,2) status level); row-scan post_p(k) closed
#       form vs exact per-rho coset enumeration at (7,2); (15,2) Monte Carlo.
#   V4. K_j-tree: exact failure-count DP over the single-table law vs the
#       closed form sum over s = 2d+1 (mod p) of C(2d,s) p^(2d(s-1)) at
#       (d = 1,2; p = 2,3,5) and (d = 3; p = 2); p = 2, d = 2 regression:
#       1028/2^15 (deg2_theory Theorem 4).
#   V5. budgeted cap terms at e = d log2 k for (31,2),(63,2),(127,2) at
#       p = 2,3; aliveness verdict (d^2 log k = o(n)).
#   V6. p = 2 regressions: q(32,2) = 5/19 = 0.263158; q_and_exact(32,2) vs
#       the printed independent-masses form (deg2_theory item 6).
#
# Run: python3 chi_odd_p_check.py [--smoke]

from __future__ import annotations

import math
import random
import sys
import time
from collections import defaultdict
from fractions import Fraction
from itertools import combinations, permutations, product

from razborov_check import monomials

T0 = time.perf_counter()
SMOKE = "--smoke" in sys.argv
TIME_LIMIT = 780.0
BUILDS: dict = {}


def elapsed() -> float:
    return time.perf_counter() - T0


# ------------------------------------------------------------ GF(p) machinery

def shift_p(h: dict, g: tuple, p: int) -> dict:
    """Multiply polynomial h (dict mono-tuple -> coeff) by monomial g."""
    out: dict = {}

    def merge(a: tuple, b: tuple) -> tuple:
        res = []
        i = j = 0
        while i < len(a) and j < len(b):
            if a[i] <= b[j]:
                res.append(a[i])
                i += 1
            else:
                res.append(b[j])
                j += 1
        res.extend(a[i:])
        res.extend(b[j:])
        return tuple(res)

    for t, c in h.items():
        nt = merge(t, g)
        nc = (out.get(nt, 0) + c) % p
        if nc:
            out[nt] = nc
        else:
            out.pop(nt, None)
    return out


def system_polys_p(nfr: int, p: int) -> list[dict]:
    """Restricted canonical system rows as {mono-tuple: coeff} over F_p:
    collisions, two-holes, Q_i = 1 - sum_j x_ij, Boolean x^2 - x."""
    nr = nfr + 1

    def v(i: int, j: int) -> int:
        return i * nfr + j

    polys = []
    for j in range(nfr):
        for i1 in range(nr):
            for i2 in range(i1 + 1, nr):
                polys.append({tuple(sorted((v(i1, j), v(i2, j)))): 1})
    for i in range(nr):
        for j1 in range(nfr):
            for j2 in range(j1 + 1, nfr):
                polys.append({tuple(sorted((v(i, j1), v(i, j2)))): 1})
    for i in range(nr):
        poly = {(): 1}
        for j in range(nfr):
            poly[(v(i, j),)] = p - 1
        polys.append(poly)
    for i in range(nr):
        for j in range(nfr):
            a = v(i, j)
            polys.append({(a, a): 1, (a,): p - 1})
    return polys


def vrows_sparse(nfr: int, d: int, p: int) -> list[dict]:
    """All restricted-system rows g*h with deg(g*h) <= d, as sparse column
    dicts {col: coeff} (cols = indices into monomials(nfr, d))."""
    monos = monomials(nfr, d)
    mi = {t: i for i, t in enumerate(monos)}
    out = []
    seen = set()
    for h in system_polys_p(nfr, p):
        dh = max(len(t) for t in h)
        for g in monos:
            if len(g) + dh > d:
                continue
            prod = shift_p(h, g, p)
            if not prod:
                continue
            key = tuple(sorted(prod.items()))
            if key in seen:
                continue
            seen.add(key)
            out.append({mi[t]: c for t, c in prod.items()})
    return out


def rref_aug(rows: list, p: int) -> dict:
    """Reduced row echelon of (sparse dict, rhs) rows.
    Returns {pivot_col: (row_dict, rhs)} with unit pivots."""
    ech: dict = {}
    for d0, rhs0 in rows:
        d = {c: v % p for c, v in d0.items() if v % p}
        rhs = rhs0 % p
        while d:
            c = max(d)
            if c in ech:
                f = d[c]
                row, rr = ech[c]
                for cc, v in row.items():
                    nv = (d.get(cc, 0) - f * v) % p
                    if nv:
                        d[cc] = nv
                    else:
                        d.pop(cc, None)
                rhs = (rhs - f * rr) % p
            else:
                inv = pow(d[c], p - 2, p)
                d = {cc: (v * inv) % p for cc, v in d.items()}
                ech[c] = (d, rhs)
                break
        if not d and rhs % p:
            raise ValueError("inconsistent augmented row (1 in V?)")
    return ech


def reduce_vec(d0: dict, ech: dict, p: int) -> dict:
    """Residual of a sparse vector against an RREF; {} iff in the span."""
    d = {c: v % p for c, v in d0.items() if v % p}
    while d:
        c = max(d)
        if c not in ech:
            return d
        f = d[c]
        row = ech[c][0]
        for cc, v in row.items():
            nv = (d.get(cc, 0) - f * v) % p
            if nv:
                d[cc] = nv
            else:
                d.pop(cc, None)
    return d


def particular_backsub(ech: dict, p: int) -> dict:
    """Particular solution by back-substitution.

    The one-pass echelon is TRIANGULAR (each pivot row's lead is its max
    column, other entries at smaller columns), not reduced: the naive
    Lstar = {pivot: rhs} readout is wrong once a pivot row carries an
    earlier pivot column. Process pivots in increasing column order with
    free variables set to 0."""
    Lstar: dict = {}
    for c in sorted(ech):
        row, rr = ech[c]
        val = rr
        for cc, v in row.items():
            if cc in Lstar:
                val -= v * Lstar[cc]
        Lstar[c] = val % p
    return Lstar


def kernel_basis(ech: dict, ncols: int, p: int) -> list[dict]:
    """One homogeneous kernel vector per non-pivot column, by
    back-substitution (triangular echelon: see particular_backsub)."""
    basis = []
    for fc in range(ncols):
        if fc in ech:
            continue
        y = {fc: 1}
        for c in sorted(ech):
            row, _ = ech[c]
            val = 0
            for cc, v in row.items():
                if cc in y:
                    val -= v * y[cc]
            if val % p:
                y[c] = val % p
        basis.append(y)
    return basis


def build_system(nfr: int, d: int, p: int) -> dict:
    """Design coset machinery for the restricted canonical (nfr, d) at p."""
    key = (p, nfr, d)
    if key in BUILDS:
        return BUILDS[key]
    monos = monomials(nfr, d)
    mi = {t: i for i, t in enumerate(monos)}
    ncols = len(monos)
    rows = vrows_sparse(nfr, d, p)
    ech_hom = rref_aug([(r, 0) for r in rows], p)
    one_in_V = (reduce_vec({0: 1}, ech_hom, p) == {})
    ech_a = rref_aug([(r, 0) for r in rows] + [({0: 1}, 1)], p)
    Lstar = particular_backsub(ech_a, p)
    kb = kernel_basis(ech_a, ncols, p)
    # self-verification: Lstar kills every V row with L(1) = 1, and kernel
    # vectors are orthogonal to every V row (guards the whole pipeline)
    assert Lstar.get(0, 0) == 1, "L(1) != 1"
    for r in rows:
        assert sum(c * Lstar.get(col, 0) for col, c in r.items()) % p == 0, \
            "Lstar violates a V row"
    for k in kb[:8]:
        for r in rows[:40]:
            assert sum(c * k.get(col, 0) for col, c in r.items()) % p == 0, \
                "kernel vector violates a V row"
    S = dict(monos=monos, mi=mi, ncols=ncols, rank=len(ech_hom),
             one_in_V=one_in_V, Lstar=Lstar, kb=kb, ech_hom=ech_hom)
    BUILDS[key] = S
    return S


def project(v: dict, T: list) -> tuple:
    return tuple(v.get(c, 0) for c in T)


def proj_basis(kb: list[dict], T: list, p: int) -> list[tuple]:
    """Independent basis of the projected homogeneous kernel pi_T(K)
    (the exact projected design law over F_p; deg3 machinery, F_p form)."""
    piv: dict = {}
    for k in kb:
        w = [k.get(c, 0) for c in T]
        while any(w):
            lead = next(i for i, x in enumerate(w) if x)
            if lead in piv:
                f = w[lead]
                pv = piv[lead]
                w = [(a - f * b) % p for a, b in zip(w, pv)]
            else:
                inv = pow(w[lead], p - 2, p)
                w = [x * inv % p for x in w]
                piv[lead] = w
                break
    return [piv[i] for i in sorted(piv)]


def coset_points(Ls: tuple, pb: list, p: int, cap: int = 36288) -> list | None:
    """All elements of Ls + span(pb), each exactly once (None if too big)."""
    n = len(pb)
    if p ** n > cap:
        return None
    pts = []
    for coeffs in product(range(p), repeat=n):
        pt = list(Ls)
        for b, k in zip(coeffs, pb):
            if b:
                for i in range(len(Ls)):
                    pt[i] = (pt[i] + b * k[i]) % p
        pts.append(tuple(pt))
    return pts


def coset_sample(Ls: tuple, pb: list, p: int, nsam: int, rng: random.Random):
    for _ in range(nsam):
        pt = list(Ls)
        for k in pb:
            b = rng.randrange(p)
            if b:
                for i in range(len(Ls)):
                    pt[i] = (pt[i] + b * k[i]) % p
        yield tuple(pt)


# ------------------------------------------------- restriction machinery

def rhos(n: int, d: int):
    """All restrictions leaving 2d free holes, as dicts."""
    c = n - 2 * d
    for A in combinations(range(n + 1), c):
        for B in permutations(range(n), c):
            yield dict(zip(A, B))


def count_rhos(n: int, d: int) -> int:
    c = n - 2 * d
    return math.comb(n + 1, c) * math.comb(n, c) * math.factorial(c)


def statuses(rho: dict, pair) -> str:
    i, j = pair
    if rho.get(i, -1) == j:
        return "M"
    if i not in rho and j not in rho.values():
        return "F"
    return "K"


def canon_map(rho: dict, d: int) -> dict:
    n = len(rho) + 2 * d
    D = sorted(set(range(n + 1)) - set(rho))
    R = sorted(set(range(n)) - set(rho.values()))
    return {(i, j): pi * (2 * d) + hj
            for pi, i in enumerate(D) for hj, j in enumerate(R)}


def spec_of(sysd: dict, rho: dict, cm: dict, q) -> tuple:
    """Answer spec of monomial query q (tuple of pairs): ('c', const | None)
    or ('b', col). None const = the answer is the constant, value given.
    NOTE: cm yields canonical VARIABLE indices; monomial COLUMNS go through
    mi[(var, ...)] (column 0 is e_0, singles start at column 1)."""
    st = [statuses(rho, pr) for pr in q]
    if "K" in st:
        return ("c", 0)
    ft = sorted(cm[pr] for pr, s in zip(q, st) if s == "F")
    if not ft:
        return ("c", 1)
    return ("b", sysd["mi"][tuple(ft)])


def col_single(sysd: dict, cm: dict, pair) -> int:
    """Monomial COLUMN of the single variable at a canonical pair."""
    return sysd["mi"][(cm[pair],)]


def spec_const(spec) -> int | None:
    return spec[1] if spec[0] == "c" else None


# ------------------------------------------------------------------- V0

def v0() -> dict:
    print("[V0] builds: 1 not in V; rank V; dim Des  [exact]")
    ok = True
    expect = {(2, (2, 1)): (3, 3), (2, (4, 2)): (165, 65)}
    for p in (2, 3, 5):
        for (nfr, d) in ((2, 1), (4, 2)):
            t0 = time.perf_counter()
            S = build_system(nfr, d, p)
            dim_des = S["ncols"] - S["rank"] - 1
            note = ""
            if (p, (nfr, d)) in expect:
                rk, dd = expect[(p, (nfr, d))]
                good = (S["rank"] == rk and dim_des == dd
                        and not S["one_in_V"])
                note = f" (corpus p=2: rank {rk}, dim {dd}) " \
                       f"{'PASS' if good else 'FAIL'}"
                ok &= good
            print(f"  p={p} ({nfr},{d}): 1 in V: {S['one_in_V']} (want "
                  f"False); rank {S['rank']}, ncols {S['ncols']}, "
                  f"dim Des {dim_des}{note}  [{time.perf_counter()-t0:.1f}s]")
            ok &= (not S["one_in_V"])
    print(f"  -> {'PASS' if ok else 'FAIL'}")
    return BUILDS


# ------------------------------------------------------------------- V1

def v1(p_list=(2, 3, 5)) -> None:
    print("\n[V1] channel law at restricted (4,2): row lock, hyperplane row, "
          "row-incomplete uniformity, star rule, alias, nonzero counts")
    allok = True
    for p in p_list:
        S = build_system(4, 2, p)
        mi, kb, Ls_full = S["mi"], S["kb"], S["Lstar"]
        d = 2
        ok = True
        # (a) single-table law: T = e_0 + all 20 singles
        singles = [(i, j) for i in range(5) for j in range(4)]
        T = [0] + [mi[(i * 4 + j,)] for (i, j) in singles]
        pb = proj_basis(kb, T, p)
        ok &= (len(pb) == 20 - 5)
        Ls = project(Ls_full, T)
        rs = [sum(Ls[1 + i * 4 + j] for j in range(4)) % p for i in range(5)]
        ok &= all(r == 1 for r in rs)
        rsb = all(sum(v[1 + i * 4 + j] for j in range(4)) % p == 0
                  for v in pb for i in range(5))
        ok &= rsb
        rng = random.Random(20261004 + p)
        nsam = 300 if SMOKE else 3000
        bad = sum(1 for pt in coset_sample(Ls, pb, p, nsam, rng)
                  if any(sum(pt[1 + i * 4 + j] for j in range(4)) % p != 1
                         for i in range(5)))
        oka = (len(pb) == 15 and all(r == 1 for r in rs) and rsb
               and bad == 0)
        ok &= oka
        print(f"  p={p} (a) single-table: kernel dim {len(pb)} "
              f"(theorem 15); Lstar row sums {rs} (theorem all 1); "
              f"basis row sums 0: {rsb}; {nsam-bad}/{nsam} sampled designs "
              f"with all row sums 1 -> {'PASS' if oka else 'FAIL'}")
        # (b) full free row = the p^3 hyperplane points, each once
        T = [0] + [mi[(j,)] for j in range(4)]
        pb = proj_basis(kb, T, p)
        okb = (len(pb) == 3)
        pts = coset_points(project(Ls_full, T), pb, p)
        okb &= (pts is not None and len(pts) == p ** 3)
        okb &= all(pt[0] == 1 for pt in pts)
        hyp = {tuple(pt[1:]) for pt in pts}
        okb &= (len(hyp) == p ** 3
                and all(sum(t) % p == 1 for t in hyp))
        ok &= okb
        print(f"  p={p} (b) full free row: {len(pts)} coset points "
              f"(theorem p^3 = {p**3}), all distinct sum-1 patterns, "
              f"L(1)=1 in all: {'PASS' if okb else 'FAIL'}")
        # (c) row-incomplete window: answers jointly uniform over F_p^T
        T = [0] + [mi[(0 * 4 + j,)] for j in range(3)] \
              + [mi[(1 * 4 + j,)] for j in range(3)] \
              + [mi[(2 * 4 + j,)] for j in range(3)] \
              + [mi[(3 * 4 + j,)] for j in range(2)] \
              + [mi[(4 * 4 + j,)] for j in range(2)]
        pb = proj_basis(kb, T, p)
        okc = (len(pb) == len(T) - 1)
        ok &= okc
        print(f"  p={p} (c) row-incomplete window ({len(T)-1} cells): "
              f"projected kernel dim {len(pb)} (theorem {len(T)-1}: "
              f"answers jointly uniform F_p^{'{}'.format(len(T)-1)}): "
              f"{'PASS' if okc else 'FAIL'}")
        # (d) star sum rule over F_p: g = x_21, probe pigeon 0, fresh j in {0,2,3}
        g = mi[(2 * 4 + 1,)]
        terms = [mi[tuple(sorted((0 * 4 + j, 2 * 4 + 1)))] for j in (0, 2, 3)]
        T = [0, g] + terms
        # star row: Q_0.g + (collision x_01 x_21) = g - sum_{j != 1} x_0j x_21
        Q0 = {(): 1}
        for j in range(4):
            Q0[(0 * 4 + j,)] = (Q0.get((0 * 4 + j,), 0) + p - 1) % p
        star = shift_p(Q0, (2 * 4 + 1,), p)
        coll_key = tuple(sorted((0 * 4 + 1, 2 * 4 + 1)))
        star[coll_key] = (star.get(coll_key, 0) + 1) % p
        star = {mi[t]: v for t, v in star.items() if v}
        inV_star = (reduce_vec(star, S["ech_hom"], p) == {})
        coll = reduce_vec({mi[coll_key]: 1}, S["ech_hom"], p) == {}
        pb = proj_basis(kb, T, p)
        okd = (inV_star and coll and len(pb) == 3)
        pts = coset_points(project(Ls_full, T), pb, p)
        viol = 0
        if pts:
            for pt in pts:
                lhs = sum(pt[2 + k] for k in range(3)) % p
                viol += (lhs != pt[1])
            okd &= (viol == 0 and len(set(pts)) == p ** 3)
        ok &= okd
        print(f"  p={p} (d) star: Q_0.x21 + x_01x_21 in V: {inV_star}; "
              f"collision x_01x_21 in V: {coll}; kernel dim {len(pb)} "
              f"(theorem 3); sum-rule violations {viol} (theorem 0); "
              f"coset {0 if pts is None else len(set(pts))} "
              f"(theorem {p**3}) -> {'PASS' if okd else 'FAIL'}")
        # (e) alias: ans(x^2) = ans(x) in every design
        a = mi[(0,)]
        T = [0, a, mi[(0, 0)]]
        pb = proj_basis(kb, T, p)
        okE = (len(pb) == 1)
        pts = coset_points(project(Ls_full, T), pb, p)
        okE &= all(pt[2] == pt[1] for pt in pts)
        ok &= okE
        print(f"  p={p} (e) alias x^2 = x: kernel dim {len(pb)} (theorem 1); "
              f"ans(x^2)=ans(x) in {len(pts)}/{len(pts)} coset points: "
              f"{'PASS' if okE else 'FAIL'}")
        # (f) nonzero-count law on a full free row (p = 3)
        if p == 3:
            from collections import Counter
            Trow = [0] + [mi[(j,)] for j in range(4)]
            pbrow = proj_basis(kb, Trow, p)
            ptsrow = coset_points(project(Ls_full, Trow), pbrow, p)
            cnt = Counter(sum(1 for x in pt[1:] if x) for pt in ptsrow)
            good = True
            for c in range(1, 5):
                pred = math.comb(4, c) * ((p - 1) ** c - (-1) ** c) // p
                good &= (cnt.get(c, 0) == pred)
            ok &= good
            print(f"  p={p} (f) nonzero-count law on the full row: counts "
                  f"{dict(sorted(cnt.items()))} vs formula "
                  f"{{c: C(4,c)((p-1)^c-(-1)^c)/p}} "
                  f"{{1:4, 2:6, 3:12, 4:5}} -> {'PASS' if good else 'FAIL'}")
        allok &= ok
    print(f"  [V1] -> {'PASS' if allok else 'FAIL'}")


# ------------------------------------------------------------------- V2

def v2(p_list=(2, 3)) -> None:
    print("\n[V2] certificate soundness + exact rates at outer (7,2), "
          "exhaustive over all restrictions")
    n, d = 7, 2
    n_rho = count_rhos(n, d)
    print(f"  restrictions: {n_rho}")
    for p in p_list:
        S = build_system(4, 2, p)
        mi, kb, Lsf = S["mi"], S["kb"], S["Lstar"]
        rng = random.Random(777 + p)
        rho_list = list(rhos(n, d))
        if SMOKE:
            rho_list = rho_list[::10]
        viol = defaultdict(int)
        rate_z = Fraction(0)
        rate_wedge = Fraction(0)
        rate_kcert = Fraction(0)
        n_rho = 0
        t0 = time.perf_counter()
        for rho in rho_list:
            n_rho += 1
            cm = canon_map(rho, d)

            def coset(specs):
                T = sorted({0} | {s[1] for s in specs if s[0] == "b"})
                pb = proj_basis(kb, T, p)
                Ls = project(Lsf, T)
                pts = coset_points(Ls, pb, p)
                pos = {c: i for i, c in enumerate(T)}
                return pts, pos

            def values(pt, specs, pos):
                out = []
                for kind, val in specs:
                    out.append(val if kind == "c" else pt[pos[val]])
                return out

            # (i) self-certification: F cell -> uniform F_p; M/K -> in {0,1}
            for (i, j) in [(a, b) for a in (2, 3, 4) for b in (2, 3, 4)]:
                st = statuses(rho, (i, j))
                if st == "F":
                    pts, pos = coset([("b", col_single(S, cm, (i, j)))])
                    vals = {pt[pos[col_single(S, cm, (i, j))]] for pt in pts}
                    if vals != set(range(p)):
                        viol["selfcert"] += 1
                # M -> 1, K -> 0: structural (spec consts), no coset needed
            # (ii) adjacency: two nonzeros co-row / co-column
            for c1, c2 in [((3, 1), (3, 3)), ((1, 2), (4, 2))]:
                specs = [spec_of(S, rho, cm, (c,)) for c in (c1, c2)]
                pts, pos = coset(specs)
                for pt in pts:
                    v1_, v2_ = values(pt, specs, pos)
                    if v1_ % p and v2_ % p:
                        if (statuses(rho, c1) != "F"
                                or statuses(rho, c2) != "F"):
                            viol["adjacency"] += 1
            # (iii) Z: {ans(x_p) != 1, ans(m) != 0}, p in m
            pair0, m0 = (3, 3), ((3, 3), (2, 2))
            specs = [spec_of(S, rho, cm, (pair0,)), spec_of(S, rho, cm, m0)]
            pts, pos = coset(specs)
            cnt_z = 0
            for pt in pts:
                sv, mv = values(pt, specs, pos)
                if sv % p != 1 and mv % p != 0:
                    cnt_z += 1
                    if statuses(rho, pair0) != "F":
                        viol["Z"] += 1
            rate_z += Fraction(cnt_z, len(pts))
            # (iv) K_j: killed column determined 0; free column uniform
            j = 2
            if j in rho.values():
                i0 = [i for i in rho if rho[i] == j][0]
                for i in range(n + 1):
                    st_i = statuses(rho, (i, j))
                    # killed column: cell i0 matched (answers 1), every
                    # other cell killed-unmatched (answers 0); none free
                    if st_i == "F" or (st_i == "M") != (i == i0):
                        viol["K_killed"] += 1
                rate_kcert += Fraction(0)
            else:
                cells = [col_single(S, cm, (i, j))
                         for i in sorted(set(range(n + 1)) - set(rho))]
                T = [0] + cells
                pb = proj_basis(kb, T, p)
                pts = coset_points(project(Lsf, T), pb, p)
                kvals = defaultdict(int)
                for pt in pts:
                    kv = (1 - sum(pt[1:])) % p
                    kvals[kv] += 1
                if len(set(pts)) != p ** (2 * d + 1) or \
                        any(c != p ** (2 * d) for c in kvals.values()):
                    viol["K_free"] += 1
                rate_kcert += Fraction(sum(c for kv, c in kvals.items()
                                           if kv != 0), len(pts))
            # (v) wedge: two nonzeros on x_pj.m through pigeon 4
            pv = 4
            gq = ((2, 2),)
            probes = [(pv, 3), (pv, 4)]
            st_g = statuses(rho, (2, 2))
            gspec = spec_of(S, rho, cm, gq)
            terms = []
            for (i, jj) in probes:
                st_pj = statuses(rho, (i, jj))
                if "K" in [st_g] or st_pj == "K" or st_g == "K":
                    terms.append(("c", 0))
                elif st_pj == "M":
                    terms.append(gspec)
                else:
                    ftg = [] if st_g == "M" else [cm[(2, 2)]]
                    col = mi[tuple(sorted(ftg + [cm[(i, jj)]]))]
                    terms.append(("b", col))
            pts, pos = coset(terms)
            cnt_w = 0
            for pt in pts:
                tv = values(pt, terms, pos)
                n1 = sum(1 for x in tv if x % p)
                if n1 >= 2:
                    cnt_w += 1
                    if pv in rho:
                        viol["wedge"] += 1
            rate_wedge += Fraction(cnt_w, len(pts))
        rZ = rate_z / n_rho
        rW = rate_wedge / n_rho
        rK = rate_kcert / n_rho
        f = Fraction((2 * d + 1) * 2 * d, (n + 1) * n)
        print(f"  p={p}: {n_rho} restrictions  [{time.perf_counter()-t0:.0f}s]")
        print(f"    violations: {dict(viol)} (theorem: all 0) -> "
              f"{'PASS' if not viol else 'FAIL'}")
        rK_closed = Fraction(2 * d * (p - 1), n * p)
        print(f"    exact per-attempt rates: Z {float(rZ):.6f}; "
              f"wedge(deg-1 base) {float(rW):.6f}; "
              f"K_j != 0 {float(rK):.6f} (closed (2d/n)(p-1)/p = "
              f"{float(rK_closed):.6f})")
        BUILDS.setdefault("rates", {})[p] = dict(Z=rZ, W=rW, K=rK, f=f)


# ------------------------------------------------------------------- V3

def q_p(n, d, p):
    return Fraction((2 * d + 1) * 2 * d, (2 * d + 1) * 2 * d + p * (n - 2 * d))


def post0_p(n, d, p):
    return Fraction((2 * d + 1) * 2 * d,
                    (2 * d + 1) * 2 * d + p * (n * n - 4 * d * d))


def qneq_p(n, d, p):
    return Fraction((p - 1) * (2 * d + 1) * 2 * d,
                    (p - 1) * (2 * d + 1) * 2 * d + p * (n - 2 * d))


def colq_p(n, d, p):
    return Fraction(2 * d, 2 * d + p * (n - 2 * d))


def qand_p(n, d, p):
    """Two-pair status Bayes for a diagonal, exact hypergeometric counts
    (labeled: M1 = pair 1 matched, pair 2 free). p = 2: deg2_theory value."""
    c = n - 2 * d
    C, F = math.comb, math.factorial
    M0 = C(n - 1, c - 2) * C(n - 2, c - 2) * F(c - 2) if c >= 2 else 0
    M1 = C(n - 1, c - 1) * C(n - 2, c - 1) * F(c - 1) if c >= 1 else 0
    M2 = C(n - 1, c) * C(n - 2, c) * F(c)
    return Fraction(M1 + M2, p * M0 + 2 * M1 + M2)


def fb_p(k, n, d, p):
    C = math.comb
    tot = 0
    for t in range(0, min(k, 2 * d - 1) + 1):
        if 2 * d - 1 - t > n - k - 1 or t > k:
            continue
        tot += C(k, t) * C(n - k - 1, 2 * d - 1 - t) \
            * Fraction(1, p ** min(t + 1, 2 * d - 1))
    return Fraction(tot, C(n, 2 * d))


def post_scan_p(k, n, d, p):
    """Row-scan posterior after k zeros then a 1 (Theorem 2'' form)."""
    A = Fraction(2 * d + 1, n + 1)
    m = Fraction(n - 2 * d, (n + 1) * n)
    FB = fb_p(k, n, d, p)
    return A * FB / (A * FB + m)


def v3() -> None:
    print("\n[V3] per-hit posteriors at odd p: closed forms vs exact "
          "restriction enumeration")
    p = 3
    ok = True
    # (a) status-level closed forms, exact enumeration
    for (n, d) in [(7, 2), (8, 2)] + ([(9, 2)] if not SMOKE else []):
        num1 = den1 = num0 = den0 = numn = denn = numc = denc = \
            numa = dena = Fraction(0)
        pr = 0
        for rho in rhos(n, d):
            pr += 1
            # single pair (0, 0)
            st = statuses(rho, (0, 0))
            pa = {"M": Fraction(1), "F": Fraction(1, p),
                  "K": Fraction(0)}[st]
            den1 += pa
            num1 += pa if st == "F" else 0
            pz = {"M": Fraction(0), "F": Fraction(1, p),
                  "K": Fraction(1)}[st]
            den0 += pz
            num0 += pz if st == "F" else 0
            pn = {"M": Fraction(1), "F": Fraction(p - 1, p),
                  "K": Fraction(0)}[st]
            denn += pn
            numn += pn if st == "F" else 0
            # K_j = 0 at column j = 0
            if 0 in rho.values():
                pk0 = Fraction(1)
                freej = 0
            else:
                pk0 = Fraction(1, p)
                freej = 1
            denc += pk0
            numc += pk0 * freej
            # diagonal ans = 1, pairs (0,0),(1,1)
            sts = [statuses(rho, q) for q in ((0, 0), (1, 1))]
            pa2 = Fraction(0) if "K" in sts else \
                (Fraction(1) if sts == ["M", "M"] else Fraction(1, p))
            dena += pa2
            numa += pa2 if sts[0] == "F" else 0
        checks = [
            ("q_p(1)", num1 / den1, q_p(n, d, p)),
            ("post0", num0 / den0, post0_p(n, d, p)),
            ("q_p(!=0)", numn / denn, qneq_p(n, d, p)),
            ("colq(K=0)", numc / denc, colq_p(n, d, p)),
            ("q_and_p", numa / dena, qand_p(n, d, p)),
        ]
        for (lbl, enumv, closed) in checks:
            good = (enumv == closed)
            ok &= good
            print(f"  ({n},{d}) p={p} {lbl}: enumeration {enumv} = "
                  f"{float(enumv):.6f}; closed {closed} -> "
                  f"{'PASS (digit-exact)' if good else 'FAIL'}  "
                  f"[{pr} rhos]")
    # (b) design-level at (7,2): row-scan post_p(k) and K_j posterior
    n, d = 7, 2
    S = build_system(4, 2, p)
    mi, kb, Lsf = S["mi"], S["kb"], S["Lstar"]
    row_i = 3
    for k in (0, 1, 2):
        num = den = Fraction(0)
        for rho in rhos(n, d):
            cm = canon_map(rho, d)
            obs = [(row_i, j) for j in range(k + 1)]
            sts = [statuses(rho, q) for q in obs]
            if "M" in sts[:-1]:
                continue
            free_c = sorted(col_single(S, cm, q)
                            for q, s in zip(obs, sts) if s == "F")
            if sts[-1] == "M":
                T = [0] + free_c
                pb = proj_basis(kb, T, p)
                pts = coset_points(project(Lsf, T), pb, p)
                cnt = sum(1 for pt in pts
                          if all(pt[1 + t] == 0
                                 for t in range(len(free_c))))
            elif sts[-1] == "F":
                T = [0] + free_c
                pb = proj_basis(kb, T, p)
                pts = coset_points(project(Lsf, T), pb, p)
                cnt = sum(1 for pt in pts
                          if all(pt[1 + t] == 0 for t in range(len(free_c) - 1))
                          and pt[1 + len(free_c) - 1] == 1)
            else:
                cnt = 0
            if cnt:
                w = Fraction(cnt, len(pts))
                den += w
                num += w if sts[-1] == "F" else 0
        enumv = num / den
        closed = post_scan_p(k, n, d, p)
        good = (enumv == closed)
        ok &= good
        print(f"  (7,2) p={p} post_scan(k={k}): enumeration {enumv} = "
              f"{float(enumv):.6f}; closed {closed} = {float(closed):.6f} "
              f"-> {'PASS (digit-exact)' if good else 'FAIL'}")
    # (c) (15,2) Monte Carlo on the proved per-rho forms
    n, d = 15, 2
    rng = random.Random(20261004)
    nsim = 4000 if SMOKE else 60000
    num = den = 0.0
    for _ in range(nsim):
        c = n - 2 * d
        A = rng.sample(range(n + 1), c)
        B = rng.sample(range(n), c)
        rho = dict(zip(A, B))
        # row 3 scan, k = 1: cell (3,0) answers 0, cell (3,1) answers 1
        s0 = statuses(rho, (3, 0))
        if s0 == "M":
            continue
        w0 = Fraction(1, p) if s0 == "F" else Fraction(1)
        s1 = statuses(rho, (3, 1))
        if s1 == "K":
            continue
        w1 = Fraction(1) if s1 == "M" else Fraction(1, p)
        w = w0 * w1
        den += float(w)
        num += float(w) * (s1 == "F")
    est = num / den
    closed = float(post_scan_p(1, n, d, p))
    print(f"  (15,2) p={p} post_scan(k=1) Monte Carlo ({nsim} rhos): "
          f"estimate {est:.5f}; closed {closed:.5f} "
          f"(differs by {abs(est-closed):.5f}; "
          f"{'consistent' if abs(est-closed) < 0.01 else 'CHECK'})")
    print(f"  [V3] -> {'PASS' if ok else 'FAIL'}")


# ------------------------------------------------------------------- V4

def ktree_closed(p: int, d: int) -> int:
    nfr = 2 * d
    return sum(math.comb(nfr, s) * p ** (nfr * (s - 1))
               for s in range(1, nfr + 1) if s % p == (nfr + 1) % p)


def ktree_dp(p: int, d: int) -> tuple:
    """Exact failure count of the K_j-tree over all single tables
    (product of per-row sum-1 hyperplanes), by DP over rows with states
    (column sum, column-nonzero flag)."""
    nfr = 2 * d
    pats = [t for t in product(range(p), repeat=nfr) if sum(t) % p == 1]
    state0 = tuple((0, 0) for _ in range(nfr))
    dp = {state0: 1}
    for _ in range(nfr + 1):
        ndp = defaultdict(int)
        for st, cnt in dp.items():
            for pat in pats:
                ns = tuple(((st[j][0] + pat[j]) % p,
                            st[j][1] or pat[j] != 0) for j in range(nfr))
                ndp[ns] += cnt
        dp = ndp
    fail = sum(cnt for st, cnt in dp.items()
               if all((not f) or (s == 1) for (s, f) in st))
    total = sum(dp.values())
    return fail, total


def v4() -> None:
    print("\n[V4] K_j-tree exact failure law: DP vs closed form "
          "sum_{s = 2d+1 (mod p)} C(2d,s) p^(2d(s-1)) / p^((2d+1)(2d-1))")
    ok = True
    grid = [(2, 1), (3, 1), (5, 1), (2, 2), (3, 2), (2, 3)]
    if not SMOKE:
        grid.append((5, 2))
    for (p, d) in grid:
        t0 = time.perf_counter()
        fail, total = ktree_dp(p, d)
        closed = ktree_closed(p, d)
        want_total = p ** ((2 * d + 1) * (2 * d - 1))
        good = (fail == closed and total == want_total)
        ok &= good
        note = ""
        if (p, d) == (2, 2):
            note = " (corpus: 1028/2^15 = 0.031372)"
        print(f"  p={p} d={d}: DP fail {fail} / {total} "
              f"(total {'=' if total == want_total else '!'}="
              f" p^{'%d' % ((2*d+1)*(2*d-1))}); closed {closed}; "
              f"err = {float(Fraction(fail, total)):.6g}"
              f"{note}  [{time.perf_counter()-t0:.0f}s] -> "
              f"{'PASS' if good else 'FAIL'}")
    # dominant-term asymptotics at the cap points
    for (p, d) in [(2, 2), (3, 2), (3, 3), (2, 4), (3, 4)]:
        nfr = 2 * d
        s_list = [s for s in range(1, nfr + 1) if s % p == (nfr + 1) % p]
        terms = {s: math.comb(nfr, s) * p ** (nfr * (s - 1)) for s in s_list}
        s_d = max(terms, key=lambda s: terms[s])
        tot = p ** ((2 * d + 1) * (2 * d - 1))
        print(f"  p={p} d={d}: feasible s (mod-p class of {nfr+1}) "
              f"{s_list}; dominant s = {s_d}; dominant term = "
              f"{float(Fraction(terms[s_d], tot)):.3e} of all tables; "
              f"C(2d,p-1) p^(1-2dp) = "
              f"{math.comb(nfr, p-1) * p ** (1 - 2 * p * d):.3e}")
    print(f"  [V4] -> {'PASS' if ok else 'FAIL'}")


# ------------------------------------------------------------------- V5

def v5() -> None:
    print("\n[V5] Theorem 3'' cap terms and Theorem 4'' budgeted witness at "
          "e = d log2(k), degree <= 2 trees")
    for (n, d) in [(31, 2), (63, 2), (127, 2), (255, 2), (1023, 2)]:
        for p in (2, 3):
            c = n - 2 * d
            f = Fraction((2 * d + 1) * 2 * d, (n + 1) * n)
            m = Fraction(c, (n + 1) * n)
            qp = q_p(n, d, p)
            qap = qand_p(n, d, p)
            qstar = max(qp, qap)
            h1 = (p - 1) * f / p + m
            # witness: budgeted K_j-tree, optimal alpha ~ 1/2 split
            c1 = Fraction(2 * d * (p - 1), n * p)
            c2 = Fraction((2 * d + 1) * (p - 1), (n + 1) * p)
            for logk in (16, 64):
                e = d * logk
                p_sc = min(1.0, float(e) * float(f) * (p - 2) / p)
                p_adj = min(1.0, float(e) * float(h1)) * \
                    min(1.0, float(e) * float(qneq_p(n, d, p))
                        * (2 * d - 1) * (p - 1) / (p * (n - 1)))
                p_k = min(1.0, 2.0 * float(e) ** 2 * d * d
                          * (p - 1) ** 2 / (p * p * n * n))
                p_blk = min(1.0, float(e) / max(c - 2, 1))
                cap = min(1.0, float(qstar) + p_sc + p_adj + p_k + p_blk)
                wit = (1 - math.exp(-float(e * c1) / 2)) ** 2
                alive = "ALIVE" if d * d * logk < 0.1 * n else "stressed"
                print(f"  ({n:4d},{d}) p={p} logk={logk:2d}: q*_p = "
                      f"{float(qstar):.4f}  P_sc = {p_sc:.4f}  "
                      f"P_adj = {p_adj:.4f}  P_K = {p_k:.4f}  "
                      f"P_blk = {p_blk:.4f}  cap = {cap:.4f}  "
                      f"witness >= {wit:.4f} "
                      f"[d^2 log k = {d*d*logk}, n = {n}: {alive}]")


# ------------------------------------------------------------------- V6

def qand_printed_p(n, d, p):
    """The printed independent-status-masses q_and generalized to p:
    P(ans=1) = m^2 + (2fm + f^2 p_diag)/p, P(ans=1 and pair 1 free) =
    (fm + f^2 p_diag)/p; at p = 2 this is deg2_theory item 6's 0.2765."""
    f = Fraction((2 * d + 1) * 2 * d, (n + 1) * n)
    m = Fraction(n - 2 * d, (n + 1) * n)
    G = (2 * d + 1) * 2 * d
    p_diag = Fraction(math.comb(G, 2) - (2 * d + 1) * math.comb(2 * d, 2)
                      - math.comb(2 * d + 1, 2) * 2 * d, math.comb(G, 2))
    return Fraction(f * m + f * f * p_diag,
                    p * m * m + 2 * f * m + f * f * p_diag)


def v6() -> None:
    print("\n[V6] p = 2 regressions")
    q = q_p(32, 2, 2)
    ok1 = (q == Fraction(5, 19))
    print(f"  q(32,2) p=2: {q} = {float(q):.6f} (deg2_theory 5/19 = "
          f"0.263158) -> {'PASS' if ok1 else 'FAIL'}")
    qa = qand_p(32, 2, 2)
    qp_printed = qand_printed_p(32, 2, 2)
    ok2 = abs(float(qa) - float(qp_printed)) < 3e-3
    print(f"  q_and_exact(32,2) p=2: {qa} = {float(qa):.6f}; printed "
          f"independent-masses form {float(qp_printed):.6f} "
          f"(deg2_theory item 6: 0.2765); gap "
          f"{abs(float(qa)-float(qp_printed)):.4f} (deg3 finding: "
          f"< 0.002-ish at all tested points) -> "
          f"{'PASS' if ok2 else 'FAIL'}")
    print(f"  [V6] -> {'PASS' if ok1 and ok2 else 'FAIL'}")


# ----------------------------------------------------------------- main

def main() -> None:
    print("chi_odd_p_check: verification of odd_p_theory.md on the TRUE "
          "pipeline channel at characteristic p\n")
    v0()
    print(f"  [t = {elapsed():.0f} s]")
    v1()
    print(f"  [t = {elapsed():.0f} s]")
    v2()
    print(f"  [t = {elapsed():.0f} s]")
    v3()
    print(f"  [t = {elapsed():.0f} s]")
    v4()
    print(f"  [t = {elapsed():.0f} s]")
    v5()
    v6()
    print(f"\n[done in {elapsed():.0f} s]")


if __name__ == "__main__":
    main()
