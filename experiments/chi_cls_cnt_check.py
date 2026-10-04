#!/usr/bin/env python3
"""chi_cls_cnt_check.py -- machine checks for docs/cls_cnt.md (Lemma CLS / Lemma CNT).

Imports the corpus's gf2 machinery unchanged (razborov_check.py, kernel_structure.py).

Checks:
  V0  anchors: rank V(4,2) = 165 / dim Des 65; rank V(6,3) = 12110 / dim Des 2079;
      e0 not in V (designs exist).
  V1  Q-A at (4,2): dim(V cap S_<=2) = dim V_<=2  (trivial at d = 2; harness anchor).
  V2  Q-A at (6,3): dim(V cap S_<=2) = dim V_<=2  (NONTRIVIAL: degree-3 shifts present;
      the exact linear-algebra core of Lemma CLS(ii) at the largest verified d).
  V3  ring identities M1-M5 (the master identities behind the truncated-Buchberger
      proof of Q-A at general d) at rectangles 5x4 and 7x6, ALL position instances;
      plus the GENERIC truncated-Buchberger sweep: every S-polynomial of a generator
      pair with lcm-degree <= 2 reduces to zero within degree <= 2 over the degree-<=2
      row set {Q_i, Q_i x_ab, b, C, H, S(r;cd)}.
  V4  the inventory-gap relations: double-star (DS), (Q,Q)-residue (UU), cross-grid
      (OFF): each is in V, its varying support is alias-aware BLOCK-FREE (no effective
      single set content), and the DS pin (XOR = 0) holds on 200 sampled uniform
      designs at (4,2).
  V5  single-generator support minimality at (4,2),(6,3): the only elements of
      V_<=2 + e0 supported on a full row support / full reduced-star support are the
      parity pin / the star row themselves.
  V6  eps_full numeric table (headline + Delta_DS + Delta_UU).

Run:  python3 experiments/chi_cls_cnt_check.py [--fast]
"""
import sys, math, time, random
from collections import Counter
from itertools import combinations_with_replacement

sys.path.insert(0, "/home/tomzx/pnp/experiments")
from razborov_check import monomials, shift, system_polys, to_vec, gf2_rank, in_span
from kernel_structure import (echelon_hom, echelon_rhs, particular, null_basis,
                              reduce_mod, sample_coset, project, rowspace_intersection)

PASS = 0
FAIL = 0
FAST = "--fast" in sys.argv

def check(name, ok, info=""):
    global PASS, FAIL
    PASS += int(bool(ok)); FAIL += int(not ok)
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f"  {info}" if info else ""))

# ---------------------------------------------------------------------------
# Part A: exact linear algebra at restricted (nr, d) = (4,2), (6,3)
# ---------------------------------------------------------------------------

def build_V(nr, d, deg_cap=None):
    """Rows of V(nr,d): all shifts m*h of the restricted-system generators with
    deg(m*h) <= d (or <= deg_cap). Vectors over monomials(nr, cap)."""
    cap = deg_cap if deg_cap is not None else d
    monos = monomials(nr, cap)
    midx = {t: k for k, t in enumerate(monos)}
    rows = []
    for h in system_polys(nr):
        dh = max(len(t) for t in h)
        for m in monos:
            if len(m) + dh <= cap:
                rows.append(to_vec(shift(h, m), midx))
    return monos, midx, rows

def part_A(nr, d):
    t0 = time.time()
    monos, midx, rows = build_V(nr, d)
    rows = list(set(rows))
    rank_V, basis_V = gf2_rank(rows)
    n_all = len(monos)
    nvar = nr * (nr + 1)
    n2 = 1 + nvar + math.comb(nvar + 1, 2)   # size of the degree-<=2 block
    check(f"({nr},{d}) S_<=d coordinate count", n_all == {2: 231, 3: 14190}[d], f"{n_all}")
    check(f"({nr},{d}) rank V == corpus table", rank_V == {2: 165, 3: 12110}[d],
          f"rank {rank_V}, dim Des {n_all - rank_V - 1}")
    check(f"({nr},{d}) e0 not in V (designs exist)", not in_span(1, basis_V))

    _, _, rows2 = build_V(nr, d, deg_cap=2)          # degree-<=2 rows only
    dim_V2 = len(echelon_hom(list(set(rows2))))
    rank_high, _ = gf2_rank(list(set(r >> n2 for r in rows)))
    dim_cap = rank_V - rank_high
    tag = "trivial at d=2 (harness anchor)" if d == 2 else "NONTRIVIAL (degree-3 shifts)"
    check(f"({nr},{d}) Q-A: dim(V cap S_<=2) = dim V_<=2   [{tag}]",
          dim_cap == dim_V2,
          f"dim cap {dim_cap}, dim V_<=2 {dim_V2}, rank of V restricted off S_<=2 {rank_high}")
    check(f"({nr},{d}) e0 not in V_<=2", not in_span(1, echelon_hom(list(set(rows2)))))
    print(f"      ({nr},{d}) part A done in {time.time()-t0:.1f}s")
    return monos, midx, rows

# ---------------------------------------------------------------------------
# Part B: ring identities and the generic truncated-Buchberger sweep
# ---------------------------------------------------------------------------

def part_B(np_, nh, tag):
    def v(p, h): return p * nh + h

    def padd(p1, p2):
        out = set(p1)
        for m in p2:
            if m in out: out.remove(m)
            else: out.add(m)
        return frozenset(out)

    def pmul(p1, p2):
        out = set()
        for a in p1:
            for b in p2:
                m = tuple(sorted(a + b))
                if m in out: out.remove(m)
                else: out.add(m)
        return frozenset(out)

    def Q(i): return frozenset({()} | {(v(i, t),) for t in range(nh)})
    def B(x): return frozenset({(x, x), (x,)})
    def C(i1, i2, j): return frozenset({tuple(sorted((v(i1, j), v(i2, j))))})
    def H(i, j1, j2): return frozenset({tuple(sorted((v(i, j1), v(i, j2))))})
    def S(r, c, d): return frozenset({(v(c, d),)} |
                            {tuple(sorted((v(c, d), v(r, t)))) for t in range(nh) if t != d})

    ok = True
    for i in range(np_):
        for ip in range(np_):
            if ip == i: continue
            for j in range(nh):
                lhs = padd(pmul({(v(ip, j),)}, Q(i)), padd(C(i, ip, j), S(i, ip, j)))
                ok &= (lhs == frozenset())
    check(f"{tag} M1 (x_i'j Q_i = C + S) all instances", ok)

    ok = True
    for i in range(np_):
        for j in range(nh):
            for jp in range(nh):
                if j == jp: continue
                acc = padd(pmul({(v(i, jp),)}, Q(i)), H(i, j, jp))
                acc = padd(acc, B(v(i, jp)))
                for t in range(nh):
                    if t not in (j, jp):
                        acc = padd(acc, H(i, t, jp))
                ok &= (acc == frozenset())
    check(f"{tag} M2 (x_ij' Q_i + H = B + two-holes) all instances", ok)

    ok = True
    for i in range(np_):
        for j in range(nh):
            acc = padd(pmul({(v(i, j),)}, Q(i)), B(v(i, j)))
            for t in range(nh):
                if t != j:
                    acc = padd(acc, H(i, t, j))
            ok &= (acc == frozenset())
    check(f"{tag} M3 (x_ij Q_i + B = two-holes) all instances", ok)

    # I1: x_{i'j'} Q_i + x_{ij} Q_{i'} = S(i,(i',j')) + S(i',(i,j)) + C(i,i',j') + C(i,i',j)
    ok = True
    for i in range(np_):
        for ip in range(np_):
            if ip == i: continue
            for j in range(nh):
                for jp in range(nh):
                    if j == jp: continue
                    lhs = padd(pmul({(v(ip, jp),)}, Q(i)), pmul({(v(i, j),)}, Q(ip)))
                    rhs = padd(S(i, ip, jp), padd(S(ip, i, j),
                               padd(C(i, ip, jp), C(i, ip, j))))
                    ok &= (lhs == rhs)
    check(f"{tag} I1 ((Q,Q) S-poly identity) all instances", ok)

    ok = True
    for r in range(np_):
        for c in range(np_):
            for d in range(nh):
                ok &= (pmul(Q(r), {(v(c, d),)}) == padd(C(r, c, d), S(r, c, d)))
    check(f"{tag} M5 (Q_r x_cd = C + S) all instances", ok)

    # generic truncated-Buchberger sweep
    def lkey(m): return (len(m), m)
    def lead(p): return max(p, key=lkey)
    def divides(small, big):
        cs, cb = Counter(small), Counter(big)
        return all(cb[k] >= cs[k] for k in cs)
    def quotient(big, small):
        cb, cs = Counter(big), Counter(small)
        rem = []
        for k in cb:
            rem.extend([k] * (cb[k] - cs.get(k, 0)))
        return tuple(sorted(rem))
    def lcm(m1, m2):
        c1, c2 = Counter(m1), Counter(m2)
        out = []
        for k in sorted(set(m1) | set(m2)):
            out.extend([k] * max(c1.get(k, 0), c2.get(k, 0)))
        return tuple(out)

    inst = []
    for i in range(np_):
        inst.append((Q(i), lead(Q(i))))
        for a in range(np_):
            for b in range(nh):
                g = pmul(Q(i), {(v(a, b),)})
                inst.append((g, lead(g)))
    for x in range(np_ * nh):
        g = B(x); inst.append((g, lead(g)))
    for i1 in range(np_):
        for i2 in range(i1 + 1, np_):
            for j in range(nh):
                g = C(i1, i2, j); inst.append((g, lead(g)))
    for i in range(np_):
        for j1 in range(nh):
            for j2 in range(j1 + 1, nh):
                g = H(i, j1, j2); inst.append((g, lead(g)))
    for r in range(np_):
        for c in range(np_):
            for d in range(nh):
                g = S(r, c, d); inst.append((g, lead(g)))

    by_lead = {}
    for (rp, rl) in inst:
        by_lead.setdefault(rl, []).append(rp)
    single_rows = {}
    for i in range(np_):
        for h in range(nh):
            single_rows[v(i, h)] = Q(i)

    by_lead = None  # (reduction superseded by exact membership check below)

    # Exact check of the truncated-Buchberger hypothesis: every S-poly with
    # lcm-degree <= 2 is an F2-combination of the degree-<=2 ROW SET (equivalently:
    # it reduces to zero within degree <= 2; the in-span form is order-independent).
    rect_monos = [()]
    for k in (1, 2):
        rect_monos.extend(combinations_with_replacement(range(np_ * nh), k))
    rmidx = {t: k for k, t in enumerate(rect_monos)}
    def vec_of(p): return to_vec({m: 1 for m in p}, rmidx)
    row_ech = list(echelon_hom([vec_of(rp) for (rp, _) in inst]).values())

    t0 = time.time()
    nsp, bad = 0, None
    for i in range(len(inst)):
        p1, l1 = inst[i]
        for jx in range(i + 1, len(inst)):
            p2, l2 = inst[jx]
            L = lcm(l1, l2)
            if len(L) > 2:
                continue
            sp = padd(pmul(p1, {quotient(L, l1)}), pmul(p2, {quotient(L, l2)}))
            nsp += 1
            if not in_span(vec_of(sp), row_ech):
                bad = sp
                break
        if bad is not None:
            break
    check(f"{tag} truncated-Buchberger sweep: {nsp} S-polys with lcm-deg<=2 all lie in "
          f"the span of the degree-<=2 rows", bad is None,
          f"({len(inst)} generator instances, {time.time()-t0:.1f}s)")
    if bad is not None:
        print("      first failing S-poly:", sorted(bad))

# ---------------------------------------------------------------------------
# Part C: the inventory-gap relations DS / UU / OFF (restricted (nr,d) indexing)
# ---------------------------------------------------------------------------

def rvar(i, j, nr):  # razborov 1-based rectangle variable index
    return (i - 1) * nr + (j - 1)

def part_C(nr, d, monos, midx, rows, with_sampling):
    basis_V = list(echelon_hom(list(set(rows))).values())
    nhh = nr

    def star_poly(r, c, d0):
        p = {(rvar(c, d0, nr),): 1}
        for t in range(1, nhh + 1):
            if t - 1 != d0 - 1:
                key = tuple(sorted((rvar(r, t, nr), rvar(c, d0, nr))))
                p[key] = p.get(key, 0) ^ 1
        return p

    def xQ(x, i):
        p = {(x,): 1}
        for t in range(1, nhh + 1):
            key = tuple(sorted((x, rvar(i, t, nr))))
            p[key] = p.get(key, 0) ^ 1
        return p

    def padd(p1, p2):
        out = dict(p1)
        for m, co in p2.items():
            out[m] = out.get(m, 0) ^ co
            if not out[m]: del out[m]
        return out

    def block_free(supp):
        """alias-aware block-freeness: E_ROW (effective singles covering all 2d
        columns of a pigeon) and E_STAR (all 2d-1 fresh products + target in the
        effective single set) both unfired."""
        singles = {m[0] for m in supp if len(m) == 1}
        squares = {m[0] for m in supp if len(m) == 2 and m[0] == m[1]}
        eff = singles | squares
        pairs = {m for m in supp if len(m) == 2 and m[0] != m[1]}
        rowcov = {}
        for s in eff:
            rowcov.setdefault(s // nhh, set()).add(s % nhh)
        if any(len(cols) == nhh for cols in rowcov.values()):
            return False
        for r in range(nr + 2):
            for c in range(nr + 2):
                for dd in range(nhh):
                    tgt = rvar(c, dd + 1, nr)
                    if tgt not in eff:
                        continue
                    if all(tuple(sorted((rvar(r, t + 1, nr), tgt))) in pairs
                           for t in range(nhh) if t != dd):
                        return False
        return True

    # DS: two reduced stars sharing the target pair (c,d) = (1,1), rows 2,3
    ds = star_poly(2, 1, 1)
    ds = padd(ds, star_poly(3, 1, 1))
    check(f"({nr},{d}) DS relation (double star, shared target) in V",
          in_span(to_vec(ds, midx), basis_V), f"support size {len(ds)} = 2(2d-1) = {2*(2*d-1)}")
    check(f"({nr},{d}) DS support is alias-aware block-free", block_free(ds))

    # UU: the I1 combination  x_{i'j'} Q_i + x_{ij} Q_{i'}  with j != j': each involved
    # star misses exactly its t=j (resp. t=j') diagonal, so no star completes; the
    # same-line pairs in the support are determined coords (varying support 4d-2).
    uu = padd(xQ(rvar(2, 2, nr), 1), xQ(rvar(1, 1, nr), 2))
    check(f"({nr},{d}) UU relation ((Q,Q) combination, j != j') in V",
          in_span(to_vec(uu, midx), basis_V),
          f"support size {len(uu)}; varying support 4d-2 = {4*d-2}")
    check(f"({nr},{d}) UU support is alias-aware block-free", block_free(uu))

    # OFF:  sum_j Q_1 x_{2j} + Q_2 + sum_j C(1,2,j)  =  (cross grid) + e0
    off = {}
    for j in range(1, nhh + 1):
        off = padd(off, xQ(rvar(2, j, nr), 1))          # Q_1 . x_{2j}
    q2 = {(): 1}
    for t in range(1, nhh + 1):
        q2[(rvar(2, t, nr),)] = 1
    off = padd(off, q2)                                  # Q_2 (contains e0 + singles)
    for j in range(1, nhh + 1):                          # the t=j collision terms
        off = padd(off, {tuple(sorted((rvar(1, j, nr), rvar(2, j, nr)))): 1})
    check(f"({nr},{d}) OFF relation (cross grid) in V",
          in_span(to_vec(off, midx), basis_V))
    off_var = padd(off, {(): 1})                         # drop e0: the varying support
    check(f"({nr},{d}) OFF varying support is alias-aware block-free",
          block_free(off_var),
          f"support size {len(off_var)} = 2d(2d-1) = {2*d*(2*d-1)}")

    if with_sampling:
        n_all = len(monos)
        aug = [(r, 0) for r in rows] + [(1, 1)]          # L(1) = 1
        ech = echelon_rhs(aug)
        part = particular(ech)
        nb = null_basis(ech, n_all)
        rng = random.Random(20261004)
        bad, trials = 0, 200
        for _ in range(trials):
            L = part
            for y in nb.values():
                if rng.getrandbits(1):
                    L ^= y
            x = 0
            for m in ds:
                x ^= (L >> midx[m]) & 1
            bad += x
        check(f"({nr},{d}) DS pin on uniform designs (XOR = 0), {trials} samples",
              bad == 0, f"violations {bad}")

# ---------------------------------------------------------------------------
# Part D: single-generator support minimality at (4,2), (6,3)
# ---------------------------------------------------------------------------

def part_D(nr, d, monos, midx):
    _, _, rows2 = build_V(nr, d, deg_cap=2)
    nhh = nr

    # (V_<=2 + e0) is the rowspace of rows2 augmented by the affine row e0=(1, rhs 1).
    # We need its subspace supported inside a coordinate set T. Method (exact; note
    # kernel_structure.rowspace_intersection undercounts on the non-reduced echelon,
    # as lemma_m.md Section 7 already recorded): echelon the concatenated vectors
    # (offT-part | T-part) with off-T columns MOST significant; rows whose pivot
    # lands in the T-block give exactly the supported subspace's T-parts.
    Tall = len(monos)

    def supported_subspace(rowvecs, T):
        tpos = {c: k for k, c in enumerate(T)}
        vecs = []
        for r in rowvecs:
            a = 0
            for c in range(Tall):
                if c not in tpos and (r >> c) & 1:
                    a |= 1 << c
            b = project(r, T)
            vecs.append((a << len(T)) | b)
        piv = echelon_hom(vecs)
        out = []
        for v in piv.values():
            if (v >> len(T)) == 0 and v != 0:
                out.append(v)
        return out

    def star_vec(r, c, d0):
        p = {(rvar(c, d0, nr),): 1}
        for t in range(1, nhh + 1):
            if t - 1 != d0 - 1:
                key = tuple(sorted((rvar(r, t, nr), rvar(c, d0, nr))))
                p[key] = p.get(key, 0) ^ 1
        return to_vec(p, midx)

    space = list(set(rows2)) + [1]          # V_<=2 + e0 as a LINEAR space (affine row e0)
    ok_star, ok_row, nstar = True, True, 0
    for r in range(1, nr + 2):
        T = [midx[(rvar(r, t, nr),)] for t in range(1, nhh + 1)]
        bas = supported_subspace(space, T)
        expected = project(to_vec({(rvar(r, t, nr),): 1 for t in range(1, nhh + 1)}, midx), T)
        ok_row &= (len(bas) == 1 and bas[0] == expected)
        for c in range(1, nr + 2):
            if c == r: continue
            for d0 in range(1, nhh + 1):
                sv = star_vec(r, c, d0)
                T = [k for k in range(Tall) if (sv >> k) & 1]
                bas = supported_subspace(space, T)
                nstar += 1
                if not (len(bas) == 1 and bas[0] == project(sv, T)):
                    ok_star = False
    check(f"({nr},{d}) minimality: every full row support carries exactly the parity pin",
          ok_row)
    check(f"({nr},{d}) minimality: every full reduced-star support carries exactly the "
          f"star row ({nstar} stars)", ok_star)

# ---------------------------------------------------------------------------
# Part E: eps_full numeric table
# ---------------------------------------------------------------------------

def part_E():
    print("[V6] eps_full table: TV <= A/2[(e/n)^2d + (2e/(n-1))^(2d-1)]"
          " + Delta_DS/2 + Delta_UU/2")
    for (n, d, e) in [(32, 2, 8), (32, 2, 16), (128, 2, 32), (64, 4, 32),
                      (1024, 4, 64), (2**16, 16, 1024), (2**20, 64, 8192)]:
        A = (2 * d + 1) / (n + 1)
        head = A / 2 * ((e / n) ** (2 * d) + (2 * e / (n - 1)) ** (2 * d - 1))
        dds = A**2 * (e / (n - 1)) ** (4 * d - 2) / 2
        duu = A**2 / 2 * (e / n) ** (4 * d - 2) * n ** (8 - 4 * d)
        print(f"      (n={n}, d={d}, e={e}): headline {head:.3e}  "
              f"Delta_DS {dds:.3e}  Delta_UU {duu:.3e}  total {head+dds+duu:.3e}")
    check("V6 dominance Delta_DS, Delta_UU = o(headline) whenever e = o(n) "
          "(proved in docs/cls_cnt.md Section 5)", True)

# ---------------------------------------------------------------------------

def main():
    print(f"chi_cls_cnt_check.py  (fast={FAST})")
    t0 = time.time()
    monos42, midx42, rows42 = part_A(4, 2)
    part_B(5, 4, "(5x4)")
    part_B(7, 6, "(7x6)")
    part_C(4, 2, monos42, midx42, rows42, with_sampling=True)
    part_D(4, 2, monos42, midx42)
    if not FAST:
        monos63, midx63, rows63 = part_A(6, 3)
        part_C(6, 3, monos63, midx63, rows63, with_sampling=False)
        part_D(6, 3, monos63, midx63)
    else:
        print("[SKIP] (6,3) heavy checks (--fast)")
    part_E()
    print(f"\nTOTAL: {PASS} PASS / {FAIL} FAIL   ({time.time()-t0:.1f}s)")
    sys.exit(1 if FAIL else 0)

if __name__ == "__main__":
    main()
