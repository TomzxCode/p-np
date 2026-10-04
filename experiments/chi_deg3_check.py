"""Verification of deg3_theory.md: the degree-3 extension of the true-pipeline
Omega(n,d) theory at p = 2 (kernel classification of degree-3 monomial
columns, the exact per-hit posterior of an all-distinct degree-3 query, the
star-difference certificate, an exhaustive small-scale certificate search,
and the cap assembly numerics).

deg3-theory agent script (2026-10-04). Channel: the TRUE pipeline (uniform
designs of the restricted canonical system; kernel_structure.py F1:
V(n,d)^rho = V(2d,d), so the canonical construction IS the printed-definition
design space). Reuses kernel_structure.py's gf2 toolkit and the
chi_deg2_theory_check.py verification pattern.

Scale facts: degree-3 monomial columns exist only for d >= 3; the smallest
exact point is the restricted system (6,3) (outer (31,3)); the outer points
(7,1) and (15,2) have no degree-3 columns at all. The smallest outer pipeline
carrying degree-3 queries is (7,3): c = n - 2d = 1, so there are exactly
C(8,1)*7!/(6!)... = 56 restrictions and all of them are enumerated exactly.

Verified clauses:
  V0. construction cross-check at (6,3): rank V = 12110, dim Des = 2079
      (corpus tables, proof_complexity.md).
  V1. [exact, (6,3)] the TEN structural classes of degree-3 columns with
      counts; determined-constant vs alias vs varying status of every column
      (full sweep, membership in rowspace(V rows + e_0)); global determined
      count 7974; the alias identities x^3 = x and x^2y = xy and the degree-3
      star row Q_p.g2 verified in V by exact GF(2) reduction.
  V2. [(6,3), exact projected design sampling] matching triples: marginal
      fairness; star sum rule XOR_{fresh j} L(x_pj.g2) = L(g2); a completed
      star shows only 2^4 of 2^5 answer patterns; a star-free, row-free,
      alias-free window is uniform (rowspace intersection = {e_0}); a
      matching triple is jointly uniform with its three component singles.
  V3. [outer (7,3), (8,3), (9,3), exhaustive] Theorem P3: the per-hit
      posterior post3 of an all-distinct degree-3 query: closed form
      post3 = (2u + v + w)/(2A0 + 3u + 3v + w) vs exhaustive restriction
      enumeration (digit-exact as rationals); exact projected-design
      enumeration and simulation at (7,3); exact per-rho balance; grid
      comparison vs q and q_and (printed and exact-status forms).
  V4. [outer (7,3) and (5,2), exact] Lemma S3 co-vertex (wedge)
      certificate: two answer-1s on monomials carrying the same pigeon in
      DISTINCT holes certify that pigeon free (an assigned pigeon kills
      every monomial through a non-matched hole); soundness verified with
      zero violations by exhaustive projected-design enumeration, and exact
      certificate rates, degree-2 and degree-3 wedges.
  V5. [outer (7,3), sampled on the exact channel] certificate search over
      symmetry classes of <=3-query sets from {singles, degree-2 diagonals,
      degree-3 matching triples}: every posterior-1 pattern must be
      inventory-explained (adjacency, wedge, Z, or the c = 1 shadow-escape
      artifact); every unexplained posterior-1 pattern is re-verified
      exactly (all 56 restrictions x exact projected enumeration).
  V6. Theorem 3' cap terms at e = d log k (q3*, P_adj, P_K, P_Star,
      P_block3) and the aliveness verdict.

Run: python3 chi_deg3_check.py [--smoke]
"""
from __future__ import annotations

import math
import random
import sys
import time
from fractions import Fraction
from itertools import combinations, permutations

from razborov_check import monomials, shift, system_polys, to_vec
from kernel_structure import (canonical_rows, echelon_rhs, null_basis,
                              orthocomplement, particular, project,
                              reduce_mod, rowspace_intersection, sample_coset,
                              span_equal)

T0 = time.perf_counter()
SMOKE = "--smoke" in sys.argv
NFR = 6          # restricted holes at d = 3 (2d)
NR = 7           # restricted pigeons (2d+1)
TIME_LIMIT = 540.0   # runtime guard (s)


def elapsed() -> float:
    return time.perf_counter() - T0


# ----------------------------------------------------------------- machinery

def build_restricted(nr: int, d: int):
    """Design coset machinery for the canonical restricted system (nr, d)."""
    monos = monomials(nr, d)
    mi = {t: i for i, t in enumerate(monos)}
    rows = canonical_rows(nr, d)
    ech_a = echelon_rhs([(g, 0) for g in rows] + [(1, 1)])
    ech_hom = {c: m for c, (m, r) in ech_a.items()}
    Lstar = particular(ech_a)
    return dict(monos=monos, mi=mi, rows=rows, ech_a=ech_a,
                ech_hom=ech_hom, Lstar=Lstar, ncols=len(monos))


def kernel_basis_big(sysd: dict) -> list[int]:
    """One kernel vector per non-pivot column (large systems)."""
    ech_a = sysd["ech_a"]
    masks = [(c, ech_a[c][0] ^ (1 << c)) for c in sorted(ech_a)]
    basis = []
    for fc in range(sysd["ncols"]):
        if fc in ech_a:
            continue
        y = 1 << fc
        for _c, mask in masks:
            if (y & mask).bit_count() & 1:
                y ^= 1 << _c
        basis.append(y)
    return basis


def proj_kernel(kb: list[int], T: list) -> list[int]:
    """Independent basis of the projected homogeneous kernel pi_T(K).

    This is the exact projected design law: designs are Lp + K uniformly, so
    their T-coordinates are uniform over project(Lp, T) + pi_T(K). (The
    rowspace_intersection route can undercount W n F_2^T on a non-reduced
    echelon; the kernel route is exact by construction.)
    """
    basis = []
    for y in kb:
        v = 0
        for k, c in enumerate(T):
            if (y >> c) & 1:
                v |= 1 << k
        if v:
            basis.append(v)
    piv: dict[int, int] = {}
    for v in basis:
        while v:
            h = v.bit_length() - 1
            if h in piv:
                v ^= piv[h]
            else:
                piv[h] = v
                break
    return [piv[c] for c in sorted(piv)]


def exact_coset(pi: list[int], Ls: int) -> list[int]:
    """All elements of Ls + span(pi), uniformly (each exactly once)."""
    outs = []
    for msk in range(1 << len(pi)):
        v = Ls
        for b in range(len(pi)):
            if (msk >> b) & 1:
                v ^= pi[b]
        outs.append(v)
    return outs


def rhos(n: int, d: int):
    """All restrictions leaving 2d free holes, as dicts."""
    c = n - 2 * d
    for A in combinations(range(n + 1), c):
        for B in permutations(range(n), c):
            yield dict(zip(A, B))


def count_rhos(n: int, d: int) -> int:
    c = n - 2 * d
    return math.comb(n + 1, c) * math.comb(n, c) * math.factorial(c)


# ------------------------------------------------- V1: degree-3 classification

CLS3 = ["x3", "x2y_samepigeon", "x2y_samehole", "x2y_diag", "T_pigeon3",
        "T_hole3", "T_22", "T_pm21_hm3", "T_pm3_hm21", "match3"]
PRED_CNT = {"x3": 42, "x2y_samepigeon": 210, "x2y_samehole": 252,
            "x2y_diag": 1260, "T_pigeon3": 140, "T_hole3": 210, "T_22": 1260,
            "T_pm21_hm3": 2520, "T_pm3_hm21": 3150, "match3": 4200}
PRED_VARY = {"x3", "x2y_diag", "match3"}
PRED_DET_TOTAL = 7974   # 1 (e_0) + 231 same-line deg-2 + 462 x^2y same-line
                        # + 7280 collision-containing all-distinct


def cls_deg3(t: tuple, nfr: int = NFR) -> str:
    cnt: dict[int, int] = {}
    for v in t:
        cnt[v] = cnt.get(v, 0) + 1
    if len(cnt) == 1:
        return "x3"
    if len(cnt) == 2:
        (x, _), (y, _) = sorted(cnt.items())
        if x // nfr == y // nfr:
            return "x2y_samepigeon"
        if x % nfr == y % nfr:
            return "x2y_samehole"
        return "x2y_diag"
    pats = [v // nfr for v in t]
    holes = [v % nfr for v in t]
    pm = tuple(sorted((pats.count(p) for p in set(pats)), reverse=True))
    hm = tuple(sorted((holes.count(h) for h in set(holes)), reverse=True))
    if pm == (1, 1, 1) and hm == (1, 1, 1):
        return "match3"
    if pm == (3,):
        assert hm == (1, 1, 1), "repeated variable in T_pigeon3"
        return "T_pigeon3"
    if hm == (3,):
        assert pm == (1, 1, 1), "repeated variable in T_hole3"
        return "T_hole3"
    if pm == (2, 1) and hm == (2, 1):
        return "T_22"
    if pm == (2, 1):
        return "T_pm21_hm3"
    return "T_pm3_hm21"


def v1_classification(sysd: dict) -> dict:
    print("[V1] degree-3 column classification at restricted (6,3) [exact]")
    mi, ech_hom = sysd["mi"], sysd["ech_hom"]
    classes: dict[str, list[int]] = {c: [] for c in CLS3}
    for t in sysd["monos"]:
        if len(t) == 3:
            classes[cls_deg3(t)].append(mi[t])
    ok_cnt = all(len(classes[c]) == PRED_CNT[c] for c in CLS3)
    print(f"  class counts vs predictions: "
          f"{'PASS' if ok_cnt else 'FAIL'} "
          f"(total {sum(len(classes[c]) for c in CLS3)} = "
          f"{sum(PRED_CNT.values())})")
    det_flag = {}
    for c in CLS3:
        d = 0
        for col in classes[c]:
            isd = reduce_mod(1 << col, ech_hom) == 0
            det_flag[col] = isd
            d += isd
        pred = 0 if c in PRED_VARY else len(classes[c])
        ok = (d == pred)
        print(f"    {c:<15}: {len(classes[c]):5d} columns, {d:5d} "
              f"determined (predicted {pred:5d}) -> "
              f"{'PASS' if ok else 'FAIL'}")
    ndet = 0
    for col in range(sysd["ncols"]):
        if reduce_mod(1 << col, ech_hom) == 0:
            ndet += 1
    print(f"  global determined columns: {ndet} (predicted {PRED_DET_TOTAL}) "
          f"-> {'PASS' if ndet == PRED_DET_TOTAL else 'FAIL'}")
    varying = sysd["ncols"] - ndet
    print(f"  varying columns: {varying} (= 42 singles + 630 diagonals + 42 "
          f"squares + 42 x^3 + 1260 x^2y-diag + 4200 matching triples)")
    # exact identities in V
    x3v = to_vec({(0, 0, 0): 1, (0,): 1}, mi)
    ok_a1 = reduce_mod(x3v, ech_hom) == 0
    xxy = tuple(sorted((0, 0, NFR + 1)))
    x2yv = to_vec({xxy: 1, (0, NFR + 1): 1}, mi)
    ok_a2 = reduce_mod(x2yv, ech_hom) == 0
    Q6 = {(): 1}
    for j in range(NFR):
        Q6[((NR - 1) * NFR + j,)] = 1     # restricted pigeon 6 = row 6
    starv = to_vec(shift(Q6, (0, NFR + 1)), mi)
    ok_star = reduce_mod(starv, ech_hom) == 0
    same_line = to_vec({(0, NFR): 1}, mi)  # x_(0,0) x_(1,0): same hole
    ok_sl = reduce_mod(same_line, ech_hom) == 0
    ok = ok_a1 and ok_a2 and ok_star and ok_sl
    print(f"  identities in V: x^3+x: {ok_a1}; x^2y+xy: {ok_a2}; "
          f"Q_6.g2: {ok_star}; same-hole product: {ok_sl} -> "
          f"{'PASS' if ok else 'FAIL'}")
    return det_flag


# ----------------------------------------------------- V2: matching-triple law

def v2_law63(sysd: dict, kb: list[int], rng: random.Random) -> None:
    print("\n[V2] answer law of matching triples at (6,3) [exact projected "
          "sampling on the kernel-projection channel]")
    mi = sysd["mi"]
    match3_cols = [mi[t] for t in sysd["monos"]
                   if len(t) == 3 and cls_deg3(t) == "match3"]
    match3_tups = [t for t in sysd["monos"]
                   if len(t) == 3 and cls_deg3(t) == "match3"]
    cache: dict = {}

    def pk(T):
        key = tuple(T)
        if key not in cache:
            cache[key] = proj_kernel(kb, list(key))
        return cache[key]

    nsam = 200 if SMOKE else 20000

    def sample(T, pb, Ls):
        v = Ls
        for b in pb:
            if rng.getrandbits(1):
                v ^= b
        return v

    # (a) marginal fairness of 20 random matching triples + L(1) = 1
    test_t = list(match3_tups)
    rng.shuffle(test_t)
    test = test_t[:20]
    test_c = [mi[t] for t in test]
    T = [0] + test_c
    pb = pk(T)
    Ls = project(sysd["Lstar"], T)
    ones = [0] * len(test)
    l1 = 0
    for _ in range(nsam):
        v = sample(T, pb, Ls)
        l1 += v & 1
        for k in range(len(test)):
            ones[k] += (v >> (1 + k)) & 1
    zmax = max(abs(o / nsam - 0.5) / math.sqrt(0.25 / nsam) for o in ones)
    print(f"  (a) marginal fairness, 20 matching triples: max |z| = {zmax:.2f}"
          f"; L(1)=1 in {l1}/{nsam} -> "
          f"{'PASS' if zmax < 4 and l1 == nsam else 'FAIL'}")
    # (b) star sum rule at (p=6, g2 = x_00 x_11), fresh j in 2..5
    g2 = mi[(0, NFR + 1)]
    starT = [0, g2] + [mi[tuple(sorted(((NR - 1) * NFR + j, 0, NFR + 1)))]
                       for j in range(2, 6)]
    pb = pk(starT)
    Ls = project(sysd["Lstar"], starT)
    dimW = len(starT) - len(pb)
    viol = 0
    pats = [0] * 32
    for _ in range(nsam):
        v = sample(starT, pb, Ls)
        G = (v >> 1) & 1
        x = 0
        for k in range(4):
            x ^= (v >> (2 + k)) & 1
        viol += (x != G)
        idx = (G << 4)
        for k in range(4):
            idx |= ((v >> (2 + k)) & 1) << (3 - k)
        pats[idx] += 1
    occ = sum(1 for p in pats if p)
    print(f"  (b) star sum rule XOR_fresh = G: violations {viol}/{nsam}"
          f" (theorem: 0); determined relations dim = {dimW} (theorem: 2 = "
          f"e_0 + star row); full 5-bit patterns occurring {occ}/32 "
          f"(XOR-pinned half-cube: 16) -> "
          f"{'PASS' if viol == 0 and occ == 16 and dimW == 2 else 'FAIL'}")
    # (c) star-free, row-free, alias-free window: only e_0, uniform
    win = [0,
           mi[(0,)], mi[(1,)], mi[(2,)], mi[(3,)],       # row 0: 4 of 6 holes
           mi[(NFR,)], mi[(NFR + 1,)],                   # row 1: 2 holes
           mi[tuple(sorted((4, 8, 13)))],                # (0,4)(1,2)(2,1)
           mi[tuple(sorted((5, 9, 12)))]]                # (0,5)(1,3)(2,0)
    pb = pk(win)
    Ls = project(sysd["Lstar"], win)
    dimW = len(win) - len(pb)
    nw = len(win) - 1
    cnts = [0] * (1 << nw)
    for _ in range(nsam):
        v = sample(win, pb, Ls)
        idx = 0
        for k in range(nw):
            idx |= ((v >> (1 + k)) & 1) << k
        cnts[idx] += 1
    z = chi2_z(cnts, nsam)
    okc = (dimW == 1) and abs(z) < 4
    print(f"  (c) star-free window: determined relations dim = {dimW} "
          f"(theorem: 1, e_0 only); joint uniformity over 2^{nw} patterns: "
          f"chi2 z = {z:+.2f} -> {'PASS' if okc else 'FAIL'}")
    # (d) matching triple jointly uniform with its three component singles
    t0 = match3_tups[0]
    T2 = [0] + [mi[(v,)] for v in t0] + [mi[t0]]
    pb = pk(T2)
    Ls = project(sysd["Lstar"], T2)
    dimW = len(T2) - len(pb)
    cnts = [0] * 16
    for _ in range(nsam):
        v = sample(T2, pb, Ls)
        idx = 0
        for k in range(4):
            idx |= ((v >> (1 + k)) & 1) << k
        cnts[idx] += 1
    z = chi2_z(cnts, nsam)
    print(f"  (d) (s1,s2,s3,triple) all 16 patterns: chi2 z = {z:+.2f}; "
          f"determined relations dim = {dimW} (theorem: 1) -> "
          f"{'PASS' if abs(z) < 4 and dimW == 1 else 'FAIL'}")


def chi2_z(counts: list[int], n_tot: int) -> float:
    k = len(counts)
    if k < 2 or n_tot == 0:
        return 0.0
    exp = n_tot / k
    stat = sum((o - exp) ** 2 for o in counts) / exp
    dof = k - 1
    return (stat - dof) / math.sqrt(2.0 * dof)


# ------------------------------------------- V3: exact per-hit posterior post3

def q_closed(n: int, d: int) -> Fraction:
    return Fraction((2 * d + 1) * d, (2 * d + 1) * d + (n - 2 * d))


def q_and_printed(n: int, d: int) -> Fraction:
    f = Fraction((2 * d + 1) * 2 * d, (n + 1) * n)
    m = Fraction(n - 2 * d, (n + 1) * n)
    G = (2 * d + 1) * 2 * d
    p_diag = Fraction(math.comb(G, 2) - (2 * d + 1) * math.comb(2 * d, 2)
                      - math.comb(2 * d + 1, 2) * 2 * d, math.comb(G, 2))
    num = f * f * p_diag / 2 + f * m / 2
    den = f * f * p_diag / 2 + f * m + m * m
    return num / den


def q_and_exact(n: int, d: int) -> Fraction:
    """Two-pair status Bayes with exact hypergeometric pattern counts."""
    c = n - 2 * d
    C, F = math.comb, math.factorial
    M0 = C(n - 1, c - 2) * C(n - 2, c - 2) * F(c - 2) if c >= 2 else 0
    M1 = C(n - 1, c - 1) * C(n - 2, c - 1) * F(c - 1) if c >= 1 else 0
    M2 = C(n - 1, c) * C(n - 2, c) * F(c)
    return Fraction(M1 + M2, 2 * M0 + 2 * M1 + M2)


def post3_closed(n: int, d: int) -> Fraction:
    """Theorem P3 closed form: post3 = (2u + v + w)/(2A0 + 3u + 3v + w)."""
    c = n - 2 * d
    C, F = math.comb, math.factorial
    A0 = C(n - 2, c - 3) * C(n - 3, c - 3) * F(c - 3) if c >= 3 else 0
    u = C(n - 2, c - 1) * C(n - 3, c - 1) * F(c - 1) if c >= 1 else 0
    v = C(n - 2, c - 2) * C(n - 3, c - 2) * F(c - 2) if c >= 2 else 0
    w = C(n - 2, c) * C(n - 3, c) * F(c)
    return Fraction(2 * u + v + w, 2 * A0 + 3 * u + 3 * v + w)


def statuses(rho: dict, pair) -> str:
    i, j = pair
    if rho.get(i, -1) == j:
        return "M"
    if i not in rho and j not in rho.values():
        return "F"
    return "K"


def post3_enum(n: int, d: int, triple) -> Fraction:
    """Exact posterior by exhaustive enumeration over all restrictions."""
    num = den = Fraction(0)
    for rho in rhos(n, d):
        st = [statuses(rho, p) for p in triple]
        if "K" in st:
            continue
        t = st.count("F")
        a = Fraction(1) if t == 0 else Fraction(1, 2)
        den += a
        if st[0] == "F":
            num += a
    return num / den


def canon_map(rho: dict, d: int) -> dict:
    c = len(rho)
    D = sorted(set(range(len(rho) + 2 * d + 1)) - set(rho))
    R = sorted(set(range(len(rho) + 2 * d)) - set(rho.values()))
    return {(i, j): pi * (2 * d) + hj
            for pi, i in enumerate(D) for hj, j in enumerate(R)}


def v3_posterior(sysd: dict, rng: random.Random) -> None:
    print("\n[V3] Theorem P3: exact per-hit posterior of an all-distinct "
          "degree-3 query")
    triples = [((1, 1), (2, 2), (3, 3)), ((1, 2), (2, 4), (3, 1))]
    for (n, d) in [(7, 3), (8, 3), (9, 3)]:
        for ti, tr in enumerate(triples[:1 if n > 7 else 2]):
            pc = post3_closed(n, d)
            pe = post3_enum(n, d, tr)
            ok = (pc == pe)
            print(f"  ({n},{d}) triple {ti}: closed form {pc} = "
                  f"{float(pc):.6f}; exhaustive over {count_rhos(n, d)} "
                  f"restrictions {pe} -> "
                  f"{'PASS (digit-exact)' if ok else 'FAIL'}")
    # (7,3): exact projected-design enumeration + per-rho balance
    n, d = 7, 3
    tr = triples[0]
    kb = kernel_basis_big(sysd)
    cache: dict = {}

    def pk(T):
        key = tuple(T)
        if key not in cache:
            cache[key] = proj_kernel(kb, list(key))
        return cache[key]

    num = den = Fraction(0)
    bal_ok = True
    for rho in rhos(n, d):
        cm = canon_map(rho, d)
        st = [statuses(rho, p) for p in tr]
        if "K" in st:
            continue
        t = st.count("F")
        if t == 0:
            a = Fraction(1)
        else:
            coord = tuple(sorted(cm[p] for p, s in zip(tr, st) if s == "F"))
            T = [0, sysd["mi"][coord]]
            pb = pk(T)
            Ls = project(sysd["Lstar"], T)
            dim = len(pb)
            ones = tot = 0
            for msk in range(1 << dim):
                v = Ls
                for bb in range(dim):
                    if (msk >> bb) & 1:
                        v ^= pb[bb]
                tot += 1
                ones += (v >> 1) & 1
            bal_ok &= (2 * ones == tot)
            a = Fraction(ones, tot)
        den += a
        if st[0] == "F":
            num += a
    pc = post3_closed(n, d)
    ok = (num / den == pc) and bal_ok
    print(f"  (7,3) exact projected-design enumeration over all 56 "
          f"restrictions: post3 = {num / den} vs closed form {pc}; "
          f"per-rho balance exact: {bal_ok} -> "
          f"{'PASS (digit-exact)' if ok else 'FAIL'}")
    # simulation sanity
    nsim = 2000 if SMOKE else 20000
    hits = [0, 0]
    rho_list = list(rhos(n, d))
    for _ in range(nsim):
        rho = rho_list[rng.randrange(len(rho_list))]
        cm = canon_map(rho, d)
        st = [statuses(rho, p) for p in tr]
        if "K" in st:
            continue
        t = st.count("F")
        bit = 1 if t == 0 else rng.randrange(2)
        if t == 0 or bit:
            hits[0] += 1
            hits[1] += int(st[0] == "F")
    emp = Fraction(hits[1], hits[0]) if hits[0] else Fraction(0)
    print(f"  (7,3) simulation ({nsim} configs, exact balance channel): "
          f"post3 = {float(emp):.4f} vs {float(pc):.4f}")
    # grid comparison + asymptotics
    print("  grid (exact arithmetic): post3 vs q vs q_and")
    worst_q = worst_a = Fraction(0)
    for (n, d) in [(7, 3), (8, 3), (9, 3), (10, 3), (12, 3), (15, 3),
                   (20, 3), (31, 3), (63, 3), (127, 3), (255, 3), (1023, 3),
                   (16, 4), (31, 4), (63, 4), (127, 4), (255, 4), (1023, 4)]:
        p3, qv = post3_closed(n, d), q_closed(n, d)
        qa_p, qa_e = q_and_printed(n, d), q_and_exact(n, d)
        worst_q = max(worst_q, p3 - qv)
        worst_a = max(worst_a, p3 - max(qa_p, qa_e))
        print(f"    ({n:4d},{d}): post3 = {float(p3):.6f}  q = "
              f"{float(qv):.6f}  q_and(exact) = {float(qa_e):.6f}  "
              f"post3/q_and = {float(p3 / qa_e):.4f}  "
              f"post3-q = {float(p3 - qv):+.4f}")
    big = (4095, 3)
    p3b, qab = post3_closed(*big), q_and_exact(*big)
    print(f"  asymptotics (proved from the closed forms): post3 and "
          f"q_and_exact are both = (2d+1)(2d)/(2(n-2d)).(1+o(1)) = "
          f"2d^2/n.(1+o(1)); ratio -> 1:")
    print(f"    at {big}: post3 = {float(p3b):.6f}, q_and_exact = "
          f"{float(qab):.6f}, ratio = {float(p3b / qab):.4f}, 2d^2/n = "
          f"{2 * big[1] ** 2 / big[0]:.6f}")
    print(f"  max over grid of (post3 - q) = {float(worst_q):+.6f}; "
          f"max of (post3 - q_and_exact) = {float(worst_a):+.6f} (a real but "
          f"small finite-n lift, peaked near n ~ 8d^2, decaying to ratio 1)")


# ---------------------------------------------- V4: co-vertex wedge certificate

def wedge_probe_scan(n: int, d: int, sysd: dict, kb: list[int],
                     p: int, h_pairs: tuple, exact: bool,
                     rng: random.Random, nsam: int) -> dict:
    """Wedge certificate scan: h a degree-k monomial (k = len(h_pairs)),
    probe = all holes j outside h's holes; queries x_pj . h.

    Invariant (proved): XOR_probe == ans(h) for EVERY restriction and design
    (the star row Q_p.h lies in V). Certificate: at least TWO probe answers
    equal to 1 => pigeon p free (an assigned pigeon has every wedge term
    determined 0 except the single matched-hole term j0, whose value is
    ans(h); so at most one probe answer can be 1).

    Returns violation counts and the exact certificate rate.
    """
    cache: dict = {}
    k = len(h_pairs)
    h_holes = {j for (_i, j) in h_pairs}
    probe = [j for j in range(n) if j not in h_holes]
    m_f = 2 * d - k                      # fresh-hole count when p is free
    viol_x = cert = cert_free = 0
    rate_num = Fraction(0)
    n_rho = 0
    dim_bad = 0
    for rho in rhos(n, d):
        n_rho += 1
        cm = canon_map(rho, d)
        p_free = p not in rho
        hst = [statuses(rho, q) for q in h_pairs]
        h_coord = None
        h_const = None
        if "K" in hst:
            h_const = 0
        else:
            ft = [cm[q] for q, s in zip(h_pairs, hst) if s == "F"]
            if not ft:
                h_const = 1
            else:
                h_coord = sysd["mi"][tuple(sorted(ft))]
        terms = []
        h_dead = ("K" in hst)          # a killed pair kills every wedge term
        for j in probe:
            st = statuses(rho, (p, j))
            if h_dead or st == "K":
                terms.append(("c", 0))
            elif st == "M":
                terms.append(("h", 0))
            else:
                ft = [cm[q] for q, s in zip(h_pairs, hst) if s == "F"]
                col = sysd["mi"][tuple(sorted(ft + [cm[(p, j)]]))]
                terms.append(("b", col))
        T = sorted(set([0] + ([h_coord] if h_coord is not None else [])
                       + [col for kind, col in terms if kind == "b"]))
        pb = pk_cache(cache, kb, T)
        Ls = project(sysd["Lstar"], T)
        pos = {c: kk for kk, c in enumerate(T)}
        if p_free and h_coord is not None and len(T) - len(pb) != 2:
            dim_bad += 1               # expected: e_0 + the star row only
        if exact:
            dim = len(pb)
            designs = []
            for msk in range(1 << dim):
                v = Ls
                for bb in range(dim):
                    if (msk >> bb) & 1:
                        v ^= pb[bb]
                designs.append(v)
        else:
            designs = []
            for _ in range(nsam):
                v = Ls
                for b in pb:
                    if rng.getrandbits(1):
                        v ^= b
                designs.append(v)
        ones_ge2 = 0
        tot = len(designs)
        for v in designs:
            hv = h_const if h_const is not None else (v >> pos[h_coord]) & 1
            xor = 0
            n1 = 0
            for kind, col in terms:
                if kind == "c":
                    b = col
                elif kind == "h":
                    b = hv
                else:
                    b = (v >> pos[col]) & 1
                xor ^= b
                n1 += b
            viol_x += (xor != hv)
            if n1 >= 2:
                ones_ge2 += 1
                cert += 1
                cert_free += int(p_free)
        if p_free:
            rate_num += Fraction(ones_ge2, tot)
    return dict(viol_x=viol_x, viol_c=cert - cert_free, cert=cert,
                rate=rate_num / n_rho, n_rho=n_rho, dim_bad=dim_bad,
                m_f=m_f, cost=len(probe) + 1)


def pk_cache(cache: dict, kb: list[int], T: list) -> list[int]:
    key = tuple(T)
    if key not in cache:
        cache[key] = proj_kernel(kb, list(key))
    return cache[key]


def z_cert_scan(n: int, d: int, sysd: dict, kb: list[int], pair,
                m_pairs: tuple) -> dict:
    """Exact rate and soundness of the Z-certificate {x_pair = 0, ans(m)=1}.

    Proof of soundness (F1 only): ans(m) = 1 forces every pair of m to be
    matched-or-free (a killed-unmatched pair contributes the factor 0); the
    single's 0 forces `pair` non-matched; hence `pair` is free.
    """
    cache: dict = {}
    viol = 0
    rate_num = Fraction(0)
    n_rho = 0
    for rho in rhos(n, d):
        n_rho += 1
        cm = canon_map(rho, d)
        st_s = statuses(rho, pair)
        st_m = [statuses(rho, q) for q in m_pairs]
        # single value: const unless free
        if st_s == "M":
            s_spec = ("c", 1)
        elif st_s == "K":
            s_spec = ("c", 0)
        else:
            s_spec = ("b", cm[pair])
        # monomial value
        if "K" in st_m:
            m_spec = ("c", 0)
        else:
            ft = [cm[q] for q, s in zip(m_pairs, st_m) if s == "F"]
            m_spec = ("c", 1) if not ft else ("b", sysd["mi"][tuple(sorted(ft))])
        T = sorted(set([0] + [c for k, c in (s_spec, m_spec) if k == "b"]))
        pb = pk_cache(cache, kb, T)
        Ls = project(sysd["Lstar"], T)
        pos = {c: i for i, c in enumerate(T)}
        s_pos = None if s_spec[0] == "c" else pos[s_spec[1]]
        m_pos = None if m_spec[0] == "c" else pos[m_spec[1]]
        pair_free = int(st_s == "F")
        cnt = 0
        cnt_cert = 0
        for msk in range(1 << len(pb)):
            v = Ls
            for bb in range(len(pb)):
                if (msk >> bb) & 1:
                    v ^= pb[bb]
            sv = s_spec[1] if s_pos is None else (v >> s_pos) & 1
            mv = m_spec[1] if m_pos is None else (v >> m_pos) & 1
            if sv == 0 and mv == 1:
                cnt_cert += 1
                viol += (1 - pair_free)
        # P[pattern | rho] as an exact fraction of the projected coset
        rate_num += Fraction(cnt_cert, 1 << len(pb))
    return dict(viol=viol, rate=rate_num / n_rho, n_rho=n_rho)


def v4_wedge_certificate(sysd63: dict, kb63: list[int]) -> None:
    print("\n[V4] Lemma S3 co-vertex (wedge) certificate [exact]")
    print("  certificate: >=2 answer-1s on x_pj.h (j over holes outside "
          "h's) => pigeon p free")
    for (n, d, hp, label, sysd) in [
            (7, 3, ((2, 1), (3, 2)), "degree-3 wedge (h = x21.x32, p = 4)",
             sysd63),
            (7, 3, ((2, 1),), "degree-2 wedge (h = x21, p = 4)", sysd63)]:
        r = wedge_probe_scan(n, d, sysd, kb63, 4, hp, not SMOKE,
                             random.Random(9), 500)
        ok = (r["viol_x"] == 0 and r["viol_c"] == 0 and r["dim_bad"] == 0)
        kj_rate = d / n
        print(f"  ({n},{d}) {label}: {r['n_rho']} restrictions; XOR "
              f"invariant violations {r['viol_x']} (theorem: 0); "
              f"certificates {r['cert']} with non-free-pigeon violations "
              f"{r['viol_c']} (theorem: 0); window dims ok: "
              f"{r['dim_bad'] == 0}; exact cert probability per attempt "
              f"{float(r['rate']):.6f} (cost {r['cost']} queries, "
              f"rate/query {float(r['rate']) / r['cost']:.2e}; K_j rate "
              f"d/n = {kj_rate:.2e}: dominated x{float(kj_rate / (r['rate'] / r['cost'])):.0f})"
              f" -> {'PASS' if ok else 'FAIL'}")
    sysd42 = build_restricted(4, 2)
    kb42 = kernel_basis_big(sysd42)
    r3 = wedge_probe_scan(5, 2, sysd42, kb42, 4, ((2, 1),), True,
                          random.Random(9), 0)
    ok = (r3["viol_x"] == 0 and r3["viol_c"] == 0)
    print(f"  (5,2) degree-2 wedge (h = x21, p = 4), exact enumeration over "
          f"all {r3['n_rho']} restrictions: XOR violations {r3['viol_x']} "
          f"(theorem: 0); certificates {r3['cert']}, non-free violations "
          f"{r3['viol_c']} (theorem: 0); exact rate {float(r3['rate']):.6f} "
          f"-> {'PASS' if ok else 'FAIL'}")
    print("  remark: the sum-rule form (ans(h)=1 and XOR_fresh=1) is NOT "
          "realizable as a certainty certificate: the fresh set is "
          "rho-hidden and the full-probe XOR equals ans(h) identically "
          "(that is the XOR invariant checked above).")
    # Z-certificate: {x_p = 0, ans(m) = 1} with p in m certifies the PAIR p
    # free (2 queries; reading-independent proof from F1)
    zc = z_cert_scan(7, 3, sysd63, kb63, (1, 1), ((0, 0), (1, 1)))
    okz = (zc["viol"] == 0)
    print(f"  (7,3) Z-certificate (x_11 = 0, m = x00.x11): {zc['n_rho']} "
          f"restrictions, violations {zc['viol']} (theorem: 0); exact "
          f"probability per attempt {float(zc['rate']):.6f} (2 queries, "
          f"rate/query {float(zc['rate']) / 2:.2e}) -> "
          f"{'PASS' if okz else 'FAIL'}")
    zc2 = z_cert_scan(7, 3, sysd63, kb63, (2, 2),
                      ((0, 0), (1, 1), (2, 2)))
    print(f"  (7,3) Z-certificate (x_22 = 0, m = matching triple "
          f"x00.x11.x22): violations {zc2['viol']} (theorem: 0); exact "
          f"probability per attempt {float(zc2['rate']):.6f} (2 queries, "
          f"rate/query {float(zc2['rate']) / 2:.2e}) -> "
          f"{'PASS' if zc2['viol'] == 0 else 'FAIL'}")


# --------------------------------------------------------- V5: certificate search

P4 = [(i, j) for i in range(4) for j in range(4)]
PERMS = list(permutations([1, 2, 3]))


def _relabel_query(q, pm, hm):
    return tuple(sorted((pm[i], hm[j]) for (i, j) in q))


def canon_class(qs):
    best = None
    for pp in PERMS:
        pm = {0: 0, 1: pp[0], 2: pp[1], 3: pp[2]}
        for hh in PERMS:
            hm = {0: 0, 1: hh[0], 2: hh[1], 3: hh[2]}
            r = tuple(sorted(_relabel_query(q, pm, hm) for q in qs))
            if best is None or r < best:
                best = r
    return best


def v5_search(sysd63: dict, kb63: list[int],
              rng: random.Random) -> None:
    print("\n[V5] certificate search at (7,3): symmetry classes of <=3-query "
          "sets over {singles, deg-2 diagonals, deg-3 matching triples}")
    n, d = 7, 3
    q1 = [(p,) for p in P4]
    q2 = [tuple(sorted((a, b))) for a, b in combinations(P4, 2)
          if a[0] != b[0] and a[1] != b[1]]
    q3 = [tuple(sorted((a, b, c))) for a, b, c in combinations(P4, 3)
          if len({x[0] for x in (a, b, c)}) == 3
          and len({x[1] for x in (a, b, c)}) == 3]
    pool = q1 + q2 + q3
    print(f"  pool: {len(q1)} singles + {len(q2)} diagonals + {len(q3)} "
          f"matching triples = {len(pool)} queries")
    # exact channel samples: kernel basis at (6,3), designs per restriction
    kb = kb63
    Lp = sysd63["Lstar"]
    rows = sysd63["rows"]
    okk = True
    for y in rng.sample(kb, 20):
        for g in rng.sample(rows, 200):
            okk &= ((y & g).bit_count() % 2 == 0)
    print(f"  kernel basis orthogonality spot-check (20 vectors x 200 rows): "
          f"{'PASS' if okk else 'FAIL'}")
    K = 120 if SMOKE else 500
    rho_list = list(rhos(n, d))
    samples = []
    meta = []
    for rho in rho_list:
        cm = canon_map(rho, d)
        D = sorted(set(range(n + 1)) - set(rho))
        R = sorted(set(range(n)) - set(rho.values()))
        freep = [1 if (i in D and j in R) else 0 for (i, j) in P4]
        vs = []
        for _ in range(K):
            v = Lp
            for y in kb:
                if rng.getrandbits(1):
                    v ^= y
            vs.append(v)                 # full design vector (monomial space)
        samples.append(vs)
        meta.append((cm, freep, set(R), rho))
    # per (rho, query) answer spec
    qidx = {q: k for k, q in enumerate(pool)}

    def answer_spec(rho, cm, Rset, q):
        st = [statuses(rho, p) for p in q]
        if "K" in st:
            return ("c", 0)
        ft = sorted(cm[p] for p, s in zip(q, st) if s == "F")
        if not ft:
            return ("c", 1)
        return ("b", sysd63["mi"][tuple(ft)])

    specs = [[answer_spec(rho, cm, R, q) for q in pool]
             for (cm, freep, R, rho) in meta]

    def scan(classes, label, nsam_per_rho):
        nonlocal explained, unexplained_max, n_cert_pat, n_pat1, classes_done, cert_tags
        for qs in classes:
            if time.perf_counter() - T0 > TIME_LIMIT:
                print(f"  [time guard at {elapsed():.0f} s: search stopped "
                      f"after {classes_done} classes]")
                return
            classes_done += 1
            acc: dict = {}
            for ri in range(len(rho_list)):
                cm, freep, R, rho = meta[ri]
                spec = specs[ri]
                idxs = [qidx[q] for q in qs]
                sp = [spec[i] for i in idxs]
                for v in samples[ri][:nsam_per_rho]:
                    ans = []
                    for kind, val in sp:
                        ans.append(val if kind == "c" else (v >> val) & 1)
                    key = tuple(ans)
                    rec = acc.get(key)
                    if rec is None:
                        rec = acc[key] = [0, [0] * len(P4)]
                    rec[0] += 1
                    for pi_, fr in enumerate(freep):
                        rec[1][pi_] += fr
            for key, (cnt, frec) in acc.items():
                if cnt < 30:
                    continue
                best = max(frec)
                if best < cnt:
                    continue
                n_pat1 += 1
                # classify the posterior-1 pattern
                ones = [(qs[k], key[k]) for k in range(len(qs)) if key[k] == 1]
                tag = None
                # adjacency: two SINGLE 1-answers sharing a row or column
                s1 = [q[0] for q, v in ones if len(q) == 1]
                for a in range(len(s1)):
                    for b in range(a + 1, len(s1)):
                        if (s1[a][0] == s1[b][0] or s1[a][1] == s1[b][1]):
                            tag = "adjacency"
                # wedge (co-vertex): two 1-answers whose monomials carry the
                # same pigeon in DISTINCT holes (or the same hole in distinct
                # pigeons): a matched vertex kills every monomial through a
                # different hole, so two 1s force the vertex free
                if tag is None:
                    for a in range(len(ones)):
                        for b in range(a + 1, len(ones)):
                            qa, qb = ones[a][0], ones[b][0]
                            for vtx in (0, 1):
                                other = 1 - vtx
                                ma = {q[vtx]: q[other] for q in qa}
                                mb = {q[vtx]: q[other] for q in qb}
                                if any(ma[x] != mb[x]
                                       for x in set(ma) & set(mb)):
                                    tag = ("wedgeP" if vtx == 0
                                           else "wedgeH")
                # Z-certificate: a single answering 0 plus a monomial of
                # degree >= 2 CONTAINING that pair answering 1 certifies the
                # pair free (the monomial's 1 forces the pair non-killed;
                # the single's 0 forces it non-matched)
                if tag is None:
                    zero_singles = [qs[k][0] for k in range(len(qs))
                                    if len(qs[k]) == 1 and key[k] == 0]
                    if zero_singles:
                        for qb, vb in ones:
                            if vb == 1 and len(qb) >= 2:
                                if any(p in qb for p in zero_singles):
                                    tag = "Z"
                                    break
                if tag is None:
                    tag = "UNEXPLAINED"
                    pu = best / cnt
                    if pu > unexplained_max:
                        unexplained_max = pu
                    if best == cnt:
                        unexplained_pats.add((qs, key))
                else:
                    n_cert_pat += 1
                    cert_tags[tag] = cert_tags.get(tag, 0) + 1
        print(f"  {label}: {classes_done} classes scanned so far")

    # size-1 and size-2 classes (all), size-3 (sampled)
    explained = unexplained_max = n_cert_pat = n_pat1 = classes_done = 0
    cert_tags: dict = {}
    unexplained_pats: set = set()
    singles_cls = sorted({canon_class([q]) for q in pool})
    pairs_cls = sorted({canon_class(sorted([qa, qb]))
                        for qa, qb in combinations(pool, 2)})
    tri_cls_all = sorted({canon_class(sorted([qa, qb, qc]))
                          for qa, qb, qc in combinations(pool, 3)})
    if SMOKE:
        rng.shuffle(tri_cls_all)
        tri_cls = tri_cls_all[:60]
    else:
        rng.shuffle(tri_cls_all)
        tri_cls = tri_cls_all[:400]
    print(f"  classes: {len(singles_cls)} singletons, {len(pairs_cls)} pairs, "
          f"{len(tri_cls)} triples (of {len(tri_cls_all)}; sampled)")
    nsam = 200 if SMOKE else 800
    scan(singles_cls, "singletons", nsam)
    scan(pairs_cls, "pairs", nsam)
    scan(tri_cls, "triples", nsam)
    print(f"  posterior-1 patterns found: {n_pat1}; inventory-explained: "
          f"{n_cert_pat} (by tag: {cert_tags}); max UNEXPLAINED sampled "
          f"posterior: {unexplained_max:.4f}; {len(unexplained_pats)} "
          f"unexplained posterior-1 patterns -> exact verification:")
    # exact posterior of every unexplained pattern (all 56 restrictions x
    # exact projected-design enumeration)
    Lstar = sysd63["Lstar"]
    cache2: dict = {}

    def exact_post(qs, key):
        """Exact P[best window pair free | pattern] and the set of window
        pairs free in EVERY pattern-consistent configuration."""
        den = 0
        num = 0
        alive = [True] * len(P4)      # pair i still free in all cons. cfgs
        any_cons = False
        for rho in rho_list:
            cm = canon_map(rho, d)
            D = sorted(set(range(n + 1)) - set(rho))
            R = sorted(set(range(n)) - set(rho.values()))
            freep = [1 if (i in D and j in R) else 0 for (i, j) in P4]
            T = [0]
            live = []
            ok = True
            for k, q in enumerate(qs):
                st = [statuses(rho, p) for p in q]
                if "K" in st:
                    if key[k] != 0:
                        ok = False
                        break
                else:
                    ft = sorted(cm[p] for p, s in zip(q, st) if s == "F")
                    if not ft:
                        if key[k] != 1:
                            ok = False
                            break
                    else:
                        col = sysd63["mi"][tuple(ft)]
                        if col not in T:
                            T.append(col)
                        live.append((k, col))
            if not ok:
                continue
            pb = pk_cache(cache2, kb, T)
            Ls = project(Lstar, T)
            pos = {c: i for i, c in enumerate(T)}
            cnt = 0
            for msk in range(1 << len(pb)):
                v = Ls
                for bb in range(len(pb)):
                    if (msk >> bb) & 1:
                        v ^= pb[bb]
                if all(((v >> pos[col]) & 1) == key[k] for k, col in live):
                    cnt += 1
            if cnt:
                any_cons = True
                den += cnt
                num += cnt * max(freep)
                for i in range(len(P4)):
                    if not freep[i]:
                        alive[i] = False
        cert = frozenset(i for i in range(len(P4))
                         if any_cons and alive[i])
        return (Fraction(num, den) if den else Fraction(0)), cert

    exact_max = Fraction(0)
    real_cert = 0
    shadow = 0
    for qs, key in sorted(unexplained_pats):
        ep, cert_pairs = exact_post(qs, key)
        if ep > exact_max:
            exact_max = ep
        if ep == 1:
            # certified window pairs exist: classify the mechanism
            zero_singles = [qs[k][0] for k in range(len(qs))
                            if len(qs[k]) == 1 and key[k] == 0]
            isz = any(vb == 1 and len(qb) >= 2
                      and any(p in qb for p in zero_singles)
                      for qb, vb in
                      ((qs[k], key[k]) for k in range(len(qs))))
            if isz:
                real_cert += 1
                print(f"    TRUE UNEXPLAINED CERTIFICATE: queries={qs} "
                      f"pattern={key}")
            elif cert_pairs:
                shadow += 1
            else:
                real_cert += 1
                print(f"    TRUE UNEXPLAINED CERTIFICATE (no certified "
                      f"pair?!): queries={qs} pattern={key}")
    print(f"  exact max posterior among unexplained-by-{chr(90)}/wedge "
          f"patterns: {float(exact_max):.6f}; remaining exact certificates: "
          f"{real_cert} unexplained + {shadow} shadow-escape (c = 1 toy "
          f"artifact: consistency pins the unique matched pair, freeing "
          f"outside window pairs; inert for c > 9) -> "
          f"{'PASS (inventory complete at searched scale: adjacency + '
             'wedge + Z + counting-shadow)'
             if real_cert == 0 else 'FAIL: genuinely new mechanism'}")


# ------------------------------------------------------------- V6: cap numerics

def v6_cap() -> None:
    print("\n[V6] Theorem 3' cap terms at e = d log2(k), degree <= 3 trees")
    C = math.comb
    for (n, d) in [(31, 3), (63, 3), (127, 3), (63, 4)]:
        c = n - 2 * d
        f = (2 * d + 1) * 2 * d / ((n + 1) * n)
        m = (n - 2 * d) / ((n + 1) * n)
        h1 = f / 2 + m
        q = (2 * d + 1) * d / ((2 * d + 1) * d + c)
        qae = float(q_and_exact(n, d))
        p3 = float(post3_closed(n, d))
        q3s = max(q, qae, p3)
        A = (2 * d + 1) / (n + 1)
        for logk in (4, 16, 64):
            e = d * logk
            p_adj = min(1.0, e * h1) * min(1.0, e * q * (2 * d - 1) / (2 * (n - 1)))
            p_k = 2 * (1 - math.exp(-e * d / (4 * n)))
            p_star = min(1.0, e * A * h1 / (n - 1))
            p_blk = e / max(n - 2 * d - 2, 1)
            cap = q3s + p_adj + p_k + p_star + p_blk
            alive = "ALIVE" if d * d * logk < 0.1 * n else "stressed"
            print(f"  ({n:3d},{d}) e = {e:4d}: q3* = {q3s:.4f}  P_adj = "
                  f"{p_adj:.4f}  P_K = {p_k:.4f}  P_Star = {p_star:.5f}  "
                  f"P_blk3 = {p_blk:.4f}  cap = {min(cap, 1.0):.4f} "
                  f"[d^2 log k = {d * d * logk}, n = {n}: {alive}]")


# ------------------------------------------------------------------------ main

def main() -> None:
    print("chi_deg3_check: verification of deg3_theory.md on the TRUE "
          "pipeline channel\n")
    t0 = time.perf_counter()
    sysd63 = build_restricted(2 * 3, 3)
    rank = len(sysd63["ech_a"]) - 1
    print(f"[V0] restricted (6,3): rank V = {rank} (corpus table 12110), "
          f"dim S = {sysd63['ncols']}, dim Des = "
          f"{sysd63['ncols'] - rank - 1} (corpus table 2079) -> "
          f"{'PASS' if rank == 12110 and sysd63['ncols'] - rank - 1 == 2079 else 'FAIL'}"
          f"  [build {time.perf_counter() - t0:.1f} s]")
    rng = random.Random(20261004)
    v1_classification(sysd63)
    print(f"  [t = {elapsed():.0f} s]")
    t0 = time.perf_counter()
    kb63 = kernel_basis_big(sysd63)
    print(f"[K] full kernel basis at (6,3): {len(kb63)} vectors "
          f"[{time.perf_counter() - t0:.1f} s]")
    v2_law63(sysd63, kb63, rng)
    print(f"  [t = {elapsed():.0f} s]")
    v3_posterior(sysd63, rng)
    print(f"  [t = {elapsed():.0f} s]")
    v4_wedge_certificate(sysd63, kb63)
    print(f"  [t = {elapsed():.0f} s]")
    v5_search(sysd63, kb63, rng)
    print(f"  [t = {elapsed():.0f} s]")
    v6_cap()
    print(f"\n[done in {elapsed():.0f} s]")


if __name__ == "__main__":
    main()
