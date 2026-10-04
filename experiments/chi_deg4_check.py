"""Verification of deg4_theory.md: the degree-4 extension of the true-pipeline
Omega(n,d) theory at p = 2.

deg4-theory agent script (2026-10-04). Channel: the TRUE pipeline (uniform
designs of the restricted canonical system; kernel_structure.py F1). Scale
fact that drives the design: the restricted system at d = 4 is (8,4) = 9
pigeons x 8 holes = 72 variables, |S(8,4)| = 1,282,975 monomial columns, so
the degree-3 full-sweep echelon instrument is infeasible (167-180 GB). The
degree-4 work therefore runs on four exact instruments:
  (a) a degree-<=2 slice echelon at (8,4) (2,701 columns, exact),
  (b) witness algebra: membership in V by EXPLICIT generator-row sums,
      machine-checked (no echelon needed),
  (c) the matching-hierarchy theorem (star induction, proved in the doc):
      its base (singles never determined) and its step (star rows) are both
      machine-checked here,
  (d) F1-level (restriction-status) exhaustive enumeration on the outer
      pipeline: exact because the per-rho answer law is {0, 1/2, 1}
      once the matching-hierarchy theorem holds.

Verified clauses:
  V0. machinery anchor: rank V(4,2) = 165, dim S = 231, dim Des = 65 (corpus
      table); degree-<=2 slice at (8,4): singles never value-determined
      (0/72 fixed), squares alias to their single (x^2 + x in W, residue =
      the single), same-line products fixed 0 (540/540), all 2016 diagonals
      (= all matching2 columns) vary (hierarchy, exact at d = 4).
  V1. witness algebra at (8,4): x^4+x^2, x^4+x, x^3y+xy, x^2y^2+xy,
      x^2yz+xyz, the degree-3 aliases, and the degree-4 star rows Q_p.g3:
      each an explicit sum of legal generator rows (restricted-grid system
      polys, deg <= 4); structural form of the star rows asserted.
  V2. star-rule status decomposition at outer (9,4) over all 90
      restrictions: fresh-set form, the [p free] indicator, and the
      injectivity automatism (rho(p) in g3.holes => ans(g3) = 0).
  V3. Theorem C: post4 closed form vs exhaustive restriction enumeration,
      digit-exact as rationals at outer (9,4) [90], (10,4) [4,950],
      (11,4) [217,800], (12,4) [8,494,200]; two matching4 triples at (9,4);
      grid vs post3 / q_and_exact / q; leading form
      post_k = (2d^2+d)/(c-k+1) (1+o(1)); ratio -> 1 (no lift, no demotion).
  V4. answer-1 masses P_k of matching-k monomials (exact fractions);
      dominance chain P4 < P3 < P2 < P1 = h1 at every grid point; P4 vs the
      K_j rate d/n (dominance factors).
  V5. F1-level exhaustive certificate search at outer (9,4): ALL symmetry
      classes of 1- and 2-query sets over {singles, matching2, matching3,
      matching4} in a 4x4 window (208 queries; constant-0 and alias queries
      excluded with proved reasons) plus a sampled 3-query sweep; every
      F1-certain pattern must be explained by {wedge (any degree, incl.
      adjacency), Z (any degree), c = 1 shadow-pin}. F1-certainty =>
      certainty is proved (soundness direction); the converse rests on the
      (7,3) exact completeness of deg3_theory.md.
  V6. Theorem 3'' cap terms at e = d log2(k) and the aliveness verdicts
      (q4*, P_adj, P_K, P_cert4, P_blk4; boundary d^2 log k vs n).

Run: python3 chi_deg4_check.py [--smoke]
"""
from __future__ import annotations

import math
import random
import sys
import time
from fractions import Fraction
from itertools import combinations, permutations, combinations_with_replacement

from razborov_check import shift
from kernel_structure import echelon_rhs, reduce_mod

T0 = time.perf_counter()
SMOKE = "--smoke" in sys.argv
TIME_LIMIT = 600.0


def elapsed() -> float:
    return time.perf_counter() - T0


# ------------------------------------------------------- restricted grid (8,4)

NR = 9          # restricted pigeons (2d+1, d = 4)
NFR = 8         # restricted holes (2d)
NV = NR * NFR   # 72 variables


def vid(i: int, j: int) -> int:
    """Restricted variable index of cell (pigeon i, hole j), 0-based."""
    return i * NFR + j


def grid_system(holes: int, pigeons: int) -> list[dict[tuple[int, ...], int]]:
    """-PHP generator polynomials on a holes x pigeons grid (variable index
    (i-1)*holes + (j-1), 1-based cells; mirror of razborov_check.system_polys)."""
    def v(i, j):
        return (i - 1) * holes + (j - 1)
    polys: list[dict[tuple[int, ...], int]] = []
    for j in range(1, holes + 1):
        for i1 in range(1, pigeons + 1):
            for i2 in range(i1 + 1, pigeons + 1):
                a, b = sorted((v(i1, j), v(i2, j)))
                polys.append({(a, b): 1})
    for i in range(1, pigeons + 1):
        for j1 in range(1, holes + 1):
            for j2 in range(j1 + 1, holes + 1):
                a, b = sorted((v(i, j1), v(i, j2)))
                polys.append({(a, b): 1})
    for i in range(1, pigeons + 1):
        poly = {(): 1}
        for j in range(1, holes + 1):
            poly[(v(i, j),)] = 1
        polys.append(poly)
    for i in range(1, pigeons + 1):
        for j in range(1, holes + 1):
            a = v(i, j)
            polys.append({(a, a): 1, (a,): 1})
    return polys


def sys4() -> list[dict[tuple[int, ...], int]]:
    """Restricted-grid system polys with 0-based var index i*NFR + j."""
    return grid_system(NFR, NR)


def line_pair(t: tuple[int, ...]) -> bool:
    """Monomial tuple contains two cells sharing a pigeon or a hole."""
    cells = [divmod(v, NFR) for v in t]
    for a in range(len(cells)):
        for b in range(a + 1, len(cells)):
            if cells[a][0] == cells[b][0] or cells[a][1] == cells[b][1]:
                return True
    return False


def is_matching(t: tuple[int, ...]) -> bool:
    cells = [divmod(v, NFR) for v in t]
    return (len(set(c[0] for c in cells)) == len(cells)
            and len(set(c[1] for c in cells)) == len(cells))


# ------------------------------------------------- V0: anchor + (8,4) <=2 slice

def v0_anchor_and_slice() -> None:
    print("[V0] machinery anchor at (4,2) + degree-<=2 slice at (8,4) [exact]")
    # anchor: corpus table rank V(4,2) = 165, dim S = 231, dim Des = 65
    holes, pigeons, d = 4, 5, 2
    nv = holes * pigeons
    monos = [tuple()] + [t for k in (1, 2)
                         for t in combinations_with_replacement(range(nv), k)]
    mi = {t: i for i, t in enumerate(monos)}
    vecs = []
    for g in grid_system(holes, pigeons):
        gd = max((len(t) for t in g), default=0)
        for k in range(0, d - gd + 1):
            for m in combinations_with_replacement(range(nv), k):
                p = shift(g, m)
                v = 0
                for t in p:
                    v ^= 1 << mi[t]
                vecs.append(v)
    ech_a = echelon_rhs([(v, 0) for v in vecs] + [(1, 1)])
    rank = len(ech_a) - 1
    ncols = len(monos)
    ok = rank == 165 and ncols == 231 and ncols - rank - 1 == 65
    print(f"  (4,2): rank V = {rank} (165), dim S = {ncols} (231), "
          f"dim Des = {ncols - rank - 1} (65) -> {'PASS' if ok else 'FAIL'}")

    # degree-<=2 slice at (8,4): 2701 columns
    monos2 = [tuple()] + [t for k in (1, 2)
                          for t in combinations_with_replacement(range(NV), k)]
    mi2 = {t: i for i, t in enumerate(monos2)}
    gens8 = sys4()
    rows2 = []
    for g in gens8:
        gd = max((len(t) for t in g), default=0)
        for k in range(0, 2 - gd + 1):
            for m in combinations_with_replacement(range(NV), k):
                rows2.append(shift(g, m))
    vecs2 = []
    for p in rows2:
        v = 0
        for t in p:
            v ^= 1 << mi2[t]
        vecs2.append(v)
    ech2 = echelon_rhs([(v, 0) for v in vecs2] + [(1, 1)])
    echh = {c: m for c, (m, r) in ech2.items()}
    print(f"  (8,4) deg<=2 slice: {len(vecs2)} generator rows, {len(monos2)} "
          f"columns, echelon pivots {len(ech2)} [t = {elapsed():.0f} s]")

    # singles: never value-determined (theorem base: cor:coin + this slice);
    # the 9 Q_i rows project to 9 independent single-column relations
    det_s = 0
    for i in range(NR):
        for j in range(NFR):
            if reduce_mod(1 << mi2[(vid(i, j),)], echh) == 0:
                det_s += 1
    sproj = []
    for i in range(NR):                 # the 9 Q_i rows: e_0 + 8 singles
        v = 0
        for j in range(NFR):
            v ^= 1 << mi2[(vid(i, j),)]
        sproj.append(v)
    piv: dict = {}
    for v in sproj:
        while v:
            h = v.bit_length() - 1
            if h in piv:
                v ^= piv[h]
            else:
                piv[h] = v
                break
    ok = det_s == 0 and len(piv) == NR
    print(f"  singles: value-determined {det_s}/72 (theorem base: 0); rank of "
          f"the 9 Q_i-row projections onto singles = {len(piv)} (9 row-parity "
          f"relations) -> {'PASS' if ok else 'FAIL'}")
    ok0 = reduce_mod(1 << 0, echh) == 0
    print(f"  e_0 determined: {ok0} -> {'PASS' if ok0 else 'FAIL'}")
    # squares: alias to their single: e_sq + e_x in W for all 72
    bad = 0
    for i in range(NR):
        for j in range(NFR):
            vec = ((1 << mi2[(vid(i, j), vid(i, j))])
                   ^ (1 << mi2[(vid(i, j),)]))
            if reduce_mod(vec, echh) != 0:
                bad += 1
    print(f"  squares alias x^2 = x (e_sq + e_x in W): mismatches {bad}/72 "
          f"-> {'PASS' if bad == 0 else 'FAIL'}")
    # same-line degree-2 (distinct cells): fixed 0
    sl = sl_det = 0
    for t in monos2:
        if len(t) == 2 and t[0] != t[1] and line_pair(t):
            sl += 1
            if reduce_mod(1 << mi2[t], echh) == 0:
                sl_det += 1
    print(f"  same-line products fixed 0: {sl_det}/{sl} (540 expected) -> "
          f"{'PASS' if sl == sl_det == 540 else 'FAIL'}")
    # diagonals (= all matching2 columns): every one varies
    diag = diag_fixed = 0
    for t in monos2:
        if len(t) == 2 and not line_pair(t):
            diag += 1
            if reduce_mod(1 << mi2[t], echh) == 0:
                diag_fixed += 1
    ok = diag == 2016 and diag_fixed == 0
    print(f"  diagonals: {diag} (2016), value-fixed {diag_fixed} "
          f"(matching-hierarchy theorem: 0) -> {'PASS' if ok else 'FAIL'}")


# ----------------------------------------------------- V1: witness algebra

def v1_witnesses() -> None:
    print("\n[V1] degree-4 alias and star witnesses at (8,4) [explicit "
          "generator-row sums, machine-checked]")
    gens = sys4()
    x, y, z = vid(0, 0), vid(1, 1), vid(2, 2)
    boolx = {(x, x): 1, (x,): 1}
    booly = {(y, y): 1, (y,): 1}

    checks = []
    # each witness is a list of (system-poly, monomial) shifts; the machine
    # check asserts every shift row is a legal V-row and the sum == target
    t = {(x, x): 1, (x,): 1}
    checks.append(("x^2 + x", t, [(t, ())]))
    t = {(x, x, x, x): 1, (x, x): 1}
    checks.append(("x^4 + x^2", t, [(boolx, (x, x)), (boolx, (x,))]))
    t = {(x, x, x, x): 1, (x,): 1}
    checks.append(("x^4 + x", t, [(boolx, (x, x)), (boolx, (x,)), (boolx, ())]))
    t = {(x, x, x, y): 1, (x, y): 1}
    checks.append(("x^3y + xy", t, [(boolx, (x, y)), (boolx, (y,))]))
    t = {(x, x, y, y): 1, (x, y): 1}
    checks.append(("x^2y^2 + xy", t, [(boolx, (y, y)), (booly, (x,))]))
    t = {(x, x, y, z): 1, (x, y, z): 1}
    checks.append(("x^2yz + xyz", t, [(boolx, (y, z))]))
    t = {(x, x, x): 1, (x,): 1}
    checks.append(("x^3 + x", t, [(boolx, (x,)), (boolx, ())]))
    t = {(x, x, y): 1, (x, y): 1}
    checks.append(("x^2y + xy", t, [(boolx, (y,))]))

    allok = True
    for name, target, wit in checks:
        rows = [shift(g, m) for (g, m) in wit]
        s: dict = {}
        for r in rows:
            for tt, c in r.items():
                s[tt] = s.get(tt, 0) ^ c
        s = {tt: c for tt, c in s.items() if c}
        legal = (all(g in gens for (g, _m) in wit)
                 and all(max((len(tt) for tt in r), default=0) <= 4
                         for r in rows))
        ok = (s == target) and legal
        allok &= ok
        print(f"  {name:<14}: witness sum {'==' if s == target else '!='} "
              f"target, all {len(wit)} rows legal generator shifts "
              f"(deg<=4) -> {'PASS' if ok else 'FAIL'}")
    g3 = (vid(1, 1), vid(2, 2), vid(3, 3))
    for p in (0, 4):
        expect: dict = {tuple(sorted(g3)): 1}
        for j in range(NFR):
            key = tuple(sorted((vid(p, j),) + g3))
            expect[key] = expect.get(key, 0) ^ 1
        expect = {t: c for t, c in expect.items() if c}
        qp = {(): 1}
        for j in range(NFR):
            qp[(vid(p, j),)] = 1
        got = shift(qp, g3)
        legal = (qp in gens) and max(len(tt) for tt in got) <= 4
        ok = (got == expect) and legal
        allok &= ok
        print(f"  Q_{p}.g3 star row: structural form + generator membership "
              f"-> {'PASS' if ok else 'FAIL'}")
    print(f"  witness block -> {'PASS' if allok else 'FAIL'}")


# ------------------------------- V2: star-rule status decomposition at (9,4)

def rhos(n: int, d: int):
    c = n - 2 * d
    for A in combinations(range(n + 1), c):
        for B in permutations(range(n), c):
            yield dict(zip(A, B))


def count_rhos(n: int, d: int) -> int:
    c = n - 2 * d
    return math.comb(n + 1, c) * math.comb(n, c) * math.factorial(c)


def status(rho: dict, pair) -> str:
    i, j = pair
    if rho.get(i, -1) == j:
        return "M"
    if i not in rho and j not in rho.values():
        return "F"
    return "K"


def v2_star_decomposition() -> None:
    print("\n[V2] degree-4 star status decomposition at outer (9,4), all 90 "
          "restrictions [exact]")
    n, d = 9, 4
    g3 = ((5, 5), (6, 6), (7, 7))
    p = 4
    g3_holes = {h for (_i, h) in g3}
    bad_fresh = bad_auto = bad_ind = bad_live = n_free = n_assigned = 0
    for rho in rhos(n, d):
        R = set(range(n)) - set(rho.values())
        if p not in rho:
            n_free += 1
            for j in range(n):
                mono = tuple(sorted((vid0(n, p, j),) + tuple(
                    vid0(n, i, h) for (i, h) in g3)))
                live_fresh = (j not in g3_holes and j in R)
                if live_fresh:
                    # live term: monomial is a matching4 (no line pair) and
                    # the pair (p, j) is free
                    if line_pair_t(mono, n) or status(rho, (p, j)) != "F":
                        bad_live += 1
                elif j in g3_holes:
                    # same-hole collision factor: monomial determined 0
                    if not line_pair_t(mono, n):
                        bad_live += 1
                else:
                    # killed hole outside g3: pair (p, j) killed-unmatched
                    if status(rho, (p, j)) != "K":
                        bad_fresh += 1
        else:
            n_assigned += 1
            if any(status(rho, (p, j)) != "K"
                   for j in R if j not in g3_holes):
                bad_ind += 1
            if rho[p] in g3_holes:
                i_other = next(i for (i, h) in g3 if h == rho[p])
                if status(rho, (i_other, rho[p])) != "K":
                    bad_auto += 1
    ok = (bad_fresh == 0 and bad_auto == 0 and bad_ind == 0 and bad_live == 0)
    print(f"  free pigeons {n_free}, assigned {n_assigned}; live-term "
          f"structural errors {bad_live}; killed-elsewhere errors "
          f"{bad_fresh}; fresh-terms-killed errors {bad_ind}; injectivity "
          f"automatism errors {bad_auto} -> {'PASS' if ok else 'FAIL'}")


def vid0(n: int, i: int, j: int) -> int:
    """Outer 0-based variable index (pair id) for cell (i, j); only used as
    a cell identifier for line-pair tests."""
    return i * n + j


def line_pair_t(t: tuple, n: int) -> bool:
    cells = [divmod(v, n) for v in t]
    for a in range(len(cells)):
        for b in range(a + 1, len(cells)):
            if cells[a][0] == cells[b][0] or cells[a][1] == cells[b][1]:
                return True
    return False


# --------------------------------------------- V3: post4 closed form + checks

def bsub(n: int, d: int, k: int, m: int) -> int:
    """Configs with exactly the m specified T-pairs matched, rest of T free."""
    c = n - 2 * d
    if c - m < 0:
        return 0
    return (math.comb(n + 1 - k, c - m) * math.comb(n - k, c - m)
            * math.factorial(c - m))


def post_k(n: int, d: int, k: int) -> Fraction:
    """post_k = P[pair 1 free | ans(matching-k) = 1], per-subclass Bayes."""
    num = sum(math.comb(k - 1, m) * bsub(n, d, k, m) for m in range(0, k))
    den = 2 * bsub(n, d, k, k) + sum(math.comb(k, m) * bsub(n, d, k, m)
                                     for m in range(0, k))
    return Fraction(num, den)


def q_closed(n: int, d: int) -> Fraction:
    return Fraction((2 * d + 1) * d, (2 * d + 1) * d + (n - 2 * d))


def q_and_exact(n: int, d: int) -> Fraction:
    return post_k(n, d, 2)


def post4_enum(n: int, d: int, quad) -> Fraction:
    """Exact posterior by exhaustive enumeration over all restrictions.

    Per-rho answer probability: 1 if all four pairs matched (the restricted
    monomial collapses to the constant 1), 1/2 if no killed pair and at
    least one free pair (the free part is a matching_j column, varying +
    fair by the matching-hierarchy theorem and balance), 0 if any pair
    killed. Numerator/denominator carry a factor 2 to stay in integers.
    """
    num = den = 0
    c = n - 2 * d
    for A in combinations(range(n + 1), c):
        pos = {a: t for t, a in enumerate(A)}
        for B in permutations(range(n), c):
            m = 0
            p1m = False
            ok = True
            for t in range(4):
                i, j = quad[t]
                pi = pos.get(i, -1)
                if pi >= 0:
                    if B[pi] == j:
                        m += 1
                        if t == 0:
                            p1m = True
                    else:
                        ok = False
                        break
                elif j in B:
                    ok = False
                    break
            if not ok:
                continue
            den += 2 if m == 4 else 1
            if m <= 3 and not p1m:
                num += 1
    return Fraction(num, den)


def v3_post4() -> None:
    print("\n[V3] Theorem C: exact per-hit posterior of an all-distinct "
          "degree-4 query")
    quads = [((1, 1), (2, 2), (3, 3), (4, 4)),
             ((1, 2), (2, 4), (3, 1), (4, 3))]
    for (n, d) in [(9, 4), (10, 4), (11, 4), (12, 4)]:
        for qi, quad in enumerate(quads[:2 if n == 9 else 1]):
            pc = post_k(n, d, 4)
            pe = post4_enum(n, d, quad)
            ok = (pc == pe)
            print(f"  ({n},{d}) quad {qi}: closed form {pc} = "
                  f"{float(pc):.6f}; exhaustive over {count_rhos(n, d)} "
                  f"restrictions {pe} -> "
                  f"{'PASS (digit-exact)' if ok else 'FAIL'} "
                  f"[t = {elapsed():.0f} s]")
    print("  grid (exact arithmetic): post4 vs post3 vs q_and_exact vs q")
    for (n, d) in [(9, 4), (10, 4), (12, 4), (16, 4), (24, 4), (31, 4),
                   (63, 4), (127, 4), (255, 4), (1023, 4), (31, 5), (63, 5),
                   (127, 5), (1023, 5)]:
        p4, p3 = post_k(n, d, 4), post_k(n, d, 3)
        qa, qv = q_and_exact(n, d), q_closed(n, d)
        print(f"    ({n:5d},{d}): post4 = {float(p4):.6f}  post3 = "
              f"{float(p3):.6f}  q_and = {float(qa):.6f}  q = {float(qv):.6f}"
              f"  post4-post3 = {float(p4 - p3):+.2e}  "
              f"post4/q_and = {float(p4 / qa):.4f}")
    print("  leading form (proved from the closed forms): post_k = "
          "(2d^2+d)/(c-k+1) . (1+o(1)) for fixed d, c -> inf:")
    for (n, d) in [(1023, 4), (4095, 4), (16383, 4)]:
        c = n - 2 * d
        p4, p3 = post_k(n, d, 4), post_k(n, d, 3)
        r4 = float(p4) * (c - 3) / (2 * d * d + d)
        r3 = float(p3) * (c - 2) / (2 * d * d + d)
        print(f"    ({n:6d},{d}): post4.(c-3)/(2d^2+d) = {r4:.5f}, "
              f"post3.(c-2)/(2d^2+d) = {r3:.5f}, post4/post3 = "
              f"{float(p4 / p3):.6f} (-> 1)")


# ------------------------------------------------- V4: answer-1 masses P_k

def p_mass(n: int, d: int, k: int) -> Fraction:
    """P[ans(matching-k) = 1] = (Q_k + b_k/T)/2, Q_k the no-killed mass."""
    c = n - 2 * d
    T = math.comb(n + 1, c) * math.comb(n, c) * math.factorial(c)
    Q = sum(math.comb(k, m) * bsub(n, d, k, m) for m in range(0, k + 1))
    return Fraction(Q + bsub(n, d, k, k), 2 * T)


def v4_masses() -> None:
    print("\n[V4] answer-1 masses of matching-k monomials (exact) and "
          "dominance")
    allok = True
    for (n, d) in [(31, 4), (63, 4), (127, 4), (255, 4), (1023, 4),
                   (63, 5), (1023, 5)]:
        p1, p2, p3, p4 = (p_mass(n, d, k) for k in (1, 2, 3, 4))
        h1 = (Fraction((2 * d + 1) * d, (n + 1) * n)
              + Fraction(n - 2 * d, (n + 1) * n))
        ok = (p1 == h1) and (p4 < p3 < p2 < p1)
        allok &= ok
        kj = Fraction(d, n)
        print(f"  ({n:5d},{d}): P1 = {float(p1):.3e} P2 = {float(p2):.3e} "
              f"P3 = {float(p3):.3e} P4 = {float(p4):.3e}  chain "
              f"P4<P3<P2<P1=h1: {'OK' if ok else 'FAIL'};  "
              f"P4/K_j(d/n) = {float(p4 / kj):.2e}")
    print(f"  mass dominance block -> {'PASS' if allok else 'FAIL'}")


# ------------------------------------------ V5: F1-level certificate search

P4W = [(i, j) for i in range(4) for j in range(4)]
PERMS = list(permutations((1, 2, 3)))


def _relabel(q, pm, hm):
    # sort the CELLS of the query (pigeon, hole roles preserved per cell)
    return tuple(sorted((pm[a], hm[b]) for (a, b) in q))


def canon_class(qs):
    best = None
    for pp in PERMS:
        pm = {0: 0, 1: pp[0], 2: pp[1], 3: pp[2]}
        for hh in PERMS:
            hm = {0: 0, 1: hh[0], 2: hh[1], 3: hh[2]}
            r = tuple(sorted(_relabel(q, pm, hm) for q in qs))
            if best is None or r < best:
                best = r
    return best


def v5_search() -> None:
    print("\n[V5] F1-level certificate search at outer (9,4): symmetry "
          "classes of query sets over {singles, matching2, matching3, "
          "matching4}, 4x4 window")
    n, d = 9, 4
    q1 = [((i, j),) for (i, j) in P4W]
    q2 = [tuple(sorted((a, b))) for a, b in combinations(P4W, 2)
          if a[0] != b[0] and a[1] != b[1]]
    q3 = [tuple(sorted((a, b, c))) for a, b, c in combinations(P4W, 3)
          if len({x[0] for x in (a, b, c)}) == 3
          and len({x[1] for x in (a, b, c)}) == 3]
    q4 = [tuple(sorted((a, b, c, e))) for a, b, c, e in combinations(P4W, 4)
          if len({x[0] for x in (a, b, c, e)}) == 4
          and len({x[1] for x in (a, b, c, e)}) == 4]
    pool = q1 + q2 + q3 + q4
    qidx = {q: i for i, q in enumerate(pool)}
    print(f"  pool: {len(q1)} singles + {len(q2)} matching2 + {len(q3)} "
          f"matching3 + {len(q4)} matching4 = {len(pool)} queries "
          f"(constant-0 and alias queries excluded: determined / info-free)")
    rho_list = list(rhos(n, d))
    # per (rho, query) F1 spec: ('c',0) killed present; ('c',1) all matched;
    # else ('b',0): free part present, any coin value consistent at F1 level
    spec = []
    freep_masks = []
    for rho in rho_list:
        row = []
        fm = 0
        for pi, (i, j) in enumerate(P4W):
            if i not in rho and j not in rho.values():
                fm |= 1 << pi
        for q in pool:
            st = [status(rho, pair) for pair in q]
            if "K" in st:
                row.append(("c", 0))
            elif "F" not in st:
                row.append(("c", 1))
            else:
                row.append(("b", 0))
        spec.append(row)
        freep_masks.append(fm)
    print(f"  {len(rho_list)} restrictions enumerated; per-(rho,query) F1 "
          f"specs precomputed [t = {elapsed():.0f} s]")

    def scan(classes, label):
        n_certain = 0
        tags: dict = {}
        unexplained = []
        for qs in classes:
            idxs = [qidx[q] for q in qs]
            nq = len(qs)
            # per rho: determined-value mask + forced bits
            det_m = []
            det_v = []
            for ri in range(len(rho_list)):
                sp = spec[ri]
                dm = dv = 0
                for t, k in enumerate(idxs):
                    if sp[k][0] == "c":
                        dm |= 1 << t
                        if sp[k][1]:
                            dv |= 1 << t
                det_m.append(dm)
                det_v.append(dv)
            alive = {}          # keybits -> 16-bit alive mask
            for ri in range(len(rho_list)):
                dm, dv = det_m[ri], det_v[ri]
                fm = freep_masks[ri]
                for keybits in range(1 << nq):
                    if (keybits & dm) != dv:
                        continue
                    cur = alive.get(keybits, (1 << len(P4W)) - 1)
                    alive[keybits] = cur & fm
            for keybits, am in alive.items():
                if am == 0:
                    continue
                cert = [pi for pi in range(len(P4W)) if (am >> pi) & 1]
                n_certain += 1
                key = [(keybits >> t) & 1 for t in range(nq)]
                tag = classify(qs, key, cert, idxs, det_m, det_v)
                tags[tag] = tags.get(tag, 0) + 1
                if tag == "UNEXPLAINED":
                    unexplained.append((qs, tuple(key), cert))
        print(f"  {label}: {len(classes)} classes, F1-certain patterns "
              f"{n_certain}, tags {tags} [t = {elapsed():.0f} s]")
        return unexplained

    def classify(qs, key, cert, idxs, det_m, det_v):
        keybits = sum(b << t for t, b in enumerate(key))
        ones = [qs[t] for t in range(len(qs)) if key[t] == 1]
        certset = set(cert)
        covered = set()
        # wedge (any degree; adjacency = the single-variable case): two
        # 1-monomials sharing a pigeon in DISTINCT holes certify that pigeon
        # free; the shared-monomial cell pairs are certified as well.
        for a in range(len(ones)):
            for b in range(a + 1, len(ones)):
                qa, qb = ones[a], ones[b]
                for vtx in (0, 1):
                    other = 1 - vtx
                    ma = {q[vtx]: q[other] for q in qa}
                    mb = {q[vtx]: q[other] for q in qb}
                    for pv in set(ma) & set(mb):
                        if ma[pv] != mb[pv]:
                            for pi in range(len(P4W)):
                                if P4W[pi] in ((pv, ma[pv]), (pv, mb[pv])):
                                    covered.add(pi)
        # Z (any degree): 0-single + 1-monomial containing it => pair free
        for t in range(len(qs)):
            if key[t] == 0 and len(qs[t]) == 1:
                pair = qs[t][0]
                if any(key[u] == 1 and pair in qs[u] for u in range(len(qs))):
                    for pi in range(len(P4W)):
                        if P4W[pi] == pair:
                            covered.add(pi)
        if certset and certset <= covered:
            return "wedge/Z"
        # c = 1 shadow-pin: certified pairs avoid every consistent rho's
        # matched pigeons and matched holes
        mp, mh = set(), set()
        for ri in range(len(rho_list)):
            dm, dv = det_m[ri], det_v[ri]
            if (keybits & dm) == (dv & dm):
                rho = rho_list[ri]
                mp |= set(rho.keys())
                mh |= set(rho.values())
        if all((P4W[pi][0] not in mp and P4W[pi][1] not in mh)
               for pi in cert):
            return "shadow(c=1)"
        return "UNEXPLAINED"

    singles_cls = sorted({canon_class([q]) for q in pool})
    pairs_cls = sorted({canon_class(sorted([qa, qb]))
                        for qa, qb in combinations(pool, 2)})
    rng = random.Random(20261004)
    nraw = 1200 if SMOKE else 24000
    seen = set()
    tri_cls = set()
    for _ in range(nraw):
        t = tuple(sorted(rng.sample(range(len(pool)), 3)))
        if t in seen:
            continue
        seen.add(t)
        tri_cls.add(canon_class([pool[i] for i in t]))
    tri_cls = sorted(tri_cls)
    print(f"  classes: {len(singles_cls)} singletons, {len(pairs_cls)} pairs, "
          f"{len(tri_cls)} triples (sampled from {len(seen)} raw of "
          f"{math.comb(len(pool), 3)})")
    un = []
    un += scan(singles_cls, "singletons")
    un += scan(pairs_cls, "pairs")
    un += scan(tri_cls, "triples")
    for qs, key, cert in un[:10]:
        print(f"    UNEXPLAINED: queries={qs} key={key} cert={cert}")
    print(f"  inventory check: unexplained F1-certain patterns = {len(un)} "
          f"-> {'PASS (wedge/Z + shadow complete at searched scale)'
              if not un else 'FAIL: new mechanism candidates'}")
    print("  note: F1-certainty => certainty is proved (soundness); the "
          "converse (no design-luck certainty) rests on the (7,3) exact "
          "completeness result of deg3_theory.md Section 5.")


# ------------------------------------------------------- V6: cap numerics

def v6_cap() -> None:
    print("\n[V6] Theorem 3'' cap terms at e = d log2(k), degree <= 4 trees")
    for (n, d) in [(63, 4), (127, 4), (255, 4), (1023, 4), (4095, 4),
                   (63, 5), (127, 5), (1023, 5)]:
        c = n - 2 * d
        f = (2 * d + 1) * 2 * d / ((n + 1) * n)
        m = c / ((n + 1) * n)
        h1 = f / 2 + m
        q = (2 * d + 1) * d / ((2 * d + 1) * d + c)
        qa = float(q_and_exact(n, d))
        p3 = float(post_k(n, d, 3))
        p4 = float(post_k(n, d, 4))
        terms = {"q": q, "and": qa, "post3": p3, "post4": p4}
        q4name = max(terms, key=terms.get)
        q4 = terms[q4name]
        p4mass = float(p_mass(n, d, 4))
        for logk in (16, 64):
            e = d * logk
            p_adj = min(1.0, e * h1) * min(1.0, e * q * (2 * d - 1) / (2 * (n - 1)))
            p_k = 2 * (1 - math.exp(-e * d / (4 * n)))
            p_blk = e / max(n - 2 * d - 3, 1)
            p_c4 = min(1.0, e * p4mass)
            cap = q4 + p_adj + p_k + p_c4 + p_blk
            alive = "ALIVE" if d * d * logk < 0.1 * n else "stressed"
            print(f"  ({n:5d},{d}) e = {e:4d}: q4* = {q4:.4f} [= {q4name}]"
                  f"  P_adj = {p_adj:.4f}  P_K = {p_k:.4f} "
                  f" P_cert4 = {p_c4:.2e}  P_blk4 = {p_blk:.4f}  "
                  f"cap = {min(cap, 1.0):.4f} [d^2 log k = {d * d * logk}, "
                  f"n = {n}: {alive}]")


# ------------------------------------------------------------------------ main

def main() -> None:
    print("chi_deg4_check: verification of deg4_theory.md on the TRUE "
          "pipeline channel\n")
    v0_anchor_and_slice()
    print(f"  [t = {elapsed():.0f} s]")
    v1_witnesses()
    print(f"  [t = {elapsed():.0f} s]")
    v2_star_decomposition()
    print(f"  [t = {elapsed():.0f} s]")
    v3_post4()
    print(f"  [t = {elapsed():.0f} s]")
    v4_masses()
    print(f"  [t = {elapsed():.0f} s]")
    v5_search()
    print(f"  [t = {elapsed():.0f} s]")
    v6_cap()
    print(f"\n[done in {elapsed():.0f} s]")


if __name__ == "__main__":
    main()
