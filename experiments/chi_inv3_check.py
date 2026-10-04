#!/usr/bin/env python3
"""chi_inv3_check.py -- machine checks for docs/inv3.md (INV(3): the t=3
degree-truncated Buchberger over the enlarged five-family inventory).

Self-contained GF(2).  Rectangle = np pigeons x nh holes; cell id v = p*nh + h;
monomials are sorted tuples of cell ids (multisets); a polynomial is a frozenset
of monomials (coefficients in F_2, so XOR = addition).

Parts:
  I  master identities, ALL position instances at 5x4 and 7x6:
     t=2 set : M1, M2, M3, M5, I1                       (cls_cnt.md sect. 3.3)
     t=3 set : N1  (alias-Q S-poly closure at degree 3)
               N2  (star-cross closure: x_z * I1, degree 3)
               SH  (single-cell shifts of M1/M2/M3/I1 into degree-3 room)
  D  dimension identities:
     (4,2): dim V_<=2 = 165; e0 not in V_<=2                        [t=2 anchor]
     (6,3): rank V_<=3 = 12110; dim Des = 2079; e0 not in V;
            dim(V cap S_<=2) = 511 by the exact rank formula
            dim(V cap S_<=2) = rank V - rank(V restricted off S_<=2);
            the t=3 slice at d = 3 is the tautology V = V_<=3.
  B  the t-truncated BUCHBERGER COMPLETION engine (the corrected instrument;
     docs/inv3.md sect. 3): add fully-reduced S-polynomial residues as new
     generators, each verified (a) to lie in W_t = span{m*h : h in G,
     deg(mh) <= t} and (b) to have ALL its <=t shifts inside W_t (machine-
     enforced span neutrality).  Termination: each added generator's head is
     divisible by no earlier head, so heads grow strictly inside the finite
     monomial set of degree <= t.  On termination every S-poly of G* with
     lcm-degree <= t reduces to zero within degree <= t, so Lemma TB
     (cls_cnt.md sect. 3.2) legitimately gives I cap S_<=t = span{m*g*} = W_t:
     the truncated identity PROVED at the rectangle.  A failed verification is
     an EXOTIC relation and a DISPROOF candidate.
     Run at t=2 (re-anchor; repairs the engine of the t=2 record) and t=3,
     rectangles 5x4, 7x6, 9x8, generator variants G (corpus: Q,b,C,H,ST) and
     G' (reduced stars RS replace ST), monomial orders A (pigeon-lex) and
     C (reversed pigeon-lex).
  E  the (8,4) instrument: the deg-4 rows of V(8,4) project onto the S_<=3
     coordinates as UNIT VECTORS ONLY (monoidal-decomposition proposition,
     docs/inv3.md sect. 3.4), so the projection question collapses to which
     degree-3 unit vectors e_m lie in V_<=3; measured against the 9x8
     degree-<=3 echelon (which part B also needs).

Run:  python3 experiments/chi_inv3_check.py [--fast]
      --fast skips the 9x8 completion round and part E.
"""
import sys, math, time
from collections import Counter, defaultdict
from itertools import combinations_with_replacement

sys.setrecursionlimit(100000)

PASS = 0
FAIL = 0
FAST = "--fast" in sys.argv

def check(name, ok, info=""):
    global PASS, FAIL
    PASS += int(bool(ok)); FAIL += int(not ok)
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f"  {info}" if info else ""), flush=True)

def note(msg):
    print("      " + msg, flush=True)

# ---------------------------------------------------------------------------
# polynomial machinery
# ---------------------------------------------------------------------------

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

def mlcm(m1, m2):
    c1, c2 = Counter(m1), Counter(m2)
    out = []
    for k in sorted(set(m1) | set(m2)):
        out.extend([k] * max(c1.get(k, 0), c2.get(k, 0)))
    return tuple(out)

def mquo(big, small):
    cb, cs = Counter(big), Counter(small)
    rem = []
    for k in cb:
        rem.extend([k] * (cb[k] - cs.get(k, 0)))
    return tuple(sorted(rem))

def submultisets(m):
    cnt = Counter(m)
    cells = list(cnt)
    def rec(i, acc):
        if i == len(cells):
            yield tuple(acc); return
        c = cells[i]
        for k in range(cnt[c] + 1):
            acc.extend([c] * k)
            yield from rec(i + 1, acc)
            if k: del acc[len(acc) - k:]
    yield from rec(0, [])

def echelon(rows):
    piv = {}
    for vv in rows:
        while vv:
            h = vv.bit_length() - 1
            q = piv.get(h)
            if q is None:
                piv[h] = vv; break
            vv ^= q
    return piv

def in_span(vv, piv):
    while vv:
        h = vv.bit_length() - 1
        q = piv.get(h)
        if q is None: return False
        vv ^= q
    return True

# ---------------------------------------------------------------------------
# generators of the restricted system on np x nh
# ---------------------------------------------------------------------------

def build_gens(np_, nh, variant):
    def v(p, h): return p * nh + h
    def Q(i): return frozenset({()} | {(v(i, t),) for t in range(nh)})
    def B(x): return frozenset({(x, x), (x,)})
    def C(i1, i2, j): return frozenset({tuple(sorted((v(i1, j), v(i2, j))))})
    def H(i, j1, j2): return frozenset({tuple(sorted((v(i, j1), v(i, j2))))})
    def ST(r, c, d):
        return frozenset({(v(c, d),)} |
                         {tuple(sorted((v(c, d), v(r, t)))) for t in range(nh)})
    def RS(r, c, d):  # reduced star = ST(r,c,d) + C(r,c,d); M5: Q_r x_cd = C + RS
        return frozenset({(v(c, d),)} |
                         {tuple(sorted((v(c, d), v(r, t)))) for t in range(nh) if t != d})
    gens = []
    for i in range(np_): gens.append((f"Q{i}", Q(i)))
    for x in range(np_ * nh): gens.append((f"b{x}", B(x)))
    for i1 in range(np_):
        for i2 in range(i1 + 1, np_):
            for j in range(nh): gens.append((f"C{i1}.{i2}.{j}", C(i1, i2, j)))
    for i in range(np_):
        for j1 in range(nh):
            for j2 in range(j1 + 1, nh): gens.append((f"H{i}.{j1}.{j2}", H(i, j1, j2)))
    if variant in ("G", "G+"):
        for r in range(np_):
            for c in range(np_):
                for d in range(nh): gens.append((f"ST{r}.{c}.{d}", ST(r, c, d)))
    if variant in ("G+", "G'"):
        # reduced stars RS(r,c,d) = ST(r,c,d) + C(r,c,d) are ideal elements
        # only for r != c (C needs distinct pigeons); the c = r rows stay as
        # unreduced ST(r,r,d) = Q_r x_rd, which is always an ideal element
        for r in range(np_):
            for c in range(np_):
                for d in range(nh):
                    if c == r:
                        if variant == "G'":
                            gens.append((f"ST{r}.{c}.{d}", ST(r, c, d)))
                        continue
                    gens.append((f"RS{r}.{c}.{d}", RS(r, c, d)))
    seen = set(); out = []
    for nm, g in gens:
        if g not in seen:
            seen.add(g); out.append((nm, g))
    return out

def order_key(kind, np_, nh):
    N = np_ * nh
    if kind == "A":   # pigeon-primary lex
        return lambda m: (len(m), tuple(sorted(m, reverse=True)))
    if kind == "B":   # hole-primary lex
        return lambda m: (len(m), tuple(sorted(((c % nh, c // nh) for c in m),
                                               reverse=True)))
    if kind == "C":   # reversed cell order, pigeon-primary
        return lambda m: (len(m), tuple(sorted((N - 1 - c for c in m), reverse=True)))
    raise ValueError(kind)

# ---------------------------------------------------------------------------
# rows of the degree-<= cap truncation over the degree-<= cap coordinates
# ---------------------------------------------------------------------------

def rect_monomials(np_, nh, cap):
    monos = [()]
    for k in range(1, cap + 1):
        monos.extend(combinations_with_replacement(range(np_ * nh), k))
    return monos

def rect_rows(np_, nh, cap, monos, midx):
    gens = build_gens(np_, nh, "G")
    out = []
    for nm, g in gens:
        dg = max(len(t) for t in g)
        for m in monos:
            if len(m) + dg <= cap:
                vv = 0
                for t in g:
                    vv |= 1 << midx[tuple(sorted(m + t))]
                out.append(vv)
    return out

def dedupe(rows):
    return list(dict.fromkeys(rows))

# ---------------------------------------------------------------------------
# Part I: master identities
# ---------------------------------------------------------------------------

def part_I(np_, nh, tag):
    t0 = time.time()
    def v(p, h): return p * nh + h
    def Q(i): return frozenset({()} | {(v(i, t),) for t in range(nh)})
    def B(x): return frozenset({(x, x), (x,)})
    def C(i1, i2, j): return frozenset({tuple(sorted((v(i1, j), v(i2, j))))})
    def H(i, j1, j2): return frozenset({tuple(sorted((v(i, j1), v(i, j2))))})
    def RS(r, c, d):
        return frozenset({(v(c, d),)} |
                         {tuple(sorted((v(c, d), v(r, t)))) for t in range(nh) if t != d})
    ZERO = frozenset()
    cells = [v(p, h) for p in range(np_) for h in range(nh)]
    eta = nh - 1  # head hole of every Q_p under order A

    ok = True
    for i in range(np_):
        for ip in range(np_):
            if ip == i: continue
            for j in range(nh):
                ok &= (padd(pmul({(v(ip, j),)}, Q(i)), padd(C(i, ip, j), RS(i, ip, j)))
                       == ZERO)
    check(f"{tag} M1 all instances", ok)

    ok = True
    for i in range(np_):
        for j in range(nh):
            for jp in range(nh):
                if j == jp: continue
                acc = padd(pmul({(v(i, jp),)}, Q(i)), H(i, j, jp))
                acc = padd(acc, B(v(i, jp)))
                for t in range(nh):
                    if t not in (j, jp): acc = padd(acc, H(i, t, jp))
                ok &= (acc == ZERO)
    check(f"{tag} M2 all instances", ok)

    ok = True
    for i in range(np_):
        for j in range(nh):
            acc = padd(pmul({(v(i, j),)}, Q(i)), B(v(i, j)))
            for t in range(nh):
                if t != j: acc = padd(acc, H(i, t, j))
            ok &= (acc == ZERO)
    check(f"{tag} M3 all instances", ok)

    ok = True
    for r in range(np_):
        for c in range(np_):
            for d in range(nh):
                ok &= (pmul(Q(r), {(v(c, d),)}) == padd(C(r, c, d), RS(r, c, d)))
    check(f"{tag} M5 all instances", ok)

    def I1_lhs(i, ip, j, jp):
        return padd(pmul({(v(ip, jp),)}, Q(i)), pmul({(v(i, j),)}, Q(ip)))
    def I1_rhs(i, ip, j, jp):
        return padd(RS(i, ip, jp), padd(RS(ip, i, j),
                    padd(C(i, ip, jp), C(i, ip, j))))
    ok = True
    for i in range(np_):
        for ip in range(np_):
            if ip == i: continue
            for j in range(nh):
                for jp in range(nh):
                    if j == jp: continue
                    ok &= (I1_lhs(i, ip, j, jp) == I1_rhs(i, ip, j, jp))
    check(f"{tag} I1 all instances", ok)

    # N1: x_ab^2 Q_p + s_p b_ab + b_ab = b_ab * sum_{j != eta} x_pj + x_ab Q_p
    ok = True; n_n1 = 0
    for p in range(np_):
        Qp = Q(p)
        for ab in cells:
            if ab == v(p, eta): continue
            n_n1 += 1
            lhs = padd(pmul({(ab, ab)}, Qp),
                       padd(pmul({(v(p, eta),)}, B(ab)), B(ab)))
            tail = frozenset({(v(p, t),) for t in range(nh) if t != eta})
            rhs = padd(pmul(B(ab), tail), pmul({(ab,)}, Qp))
            ok &= (lhs == rhs)
    check(f"{tag} N1 (alias-Q closure) all {n_n1} instances", ok)

    # N2: x_z * I1(p, r) at j = j' = eta, for every cell z and p != r
    ok = True; n_n2 = 0
    for p in range(np_):
        for r in range(np_):
            if r == p: continue
            lhs = padd(pmul({(v(r, eta),)}, Q(p)), pmul({(v(p, eta),)}, Q(r)))
            rhs = padd(RS(p, r, eta), padd(RS(r, p, eta),
                       padd(C(p, r, eta), C(p, r, eta))))
            ok &= (lhs == rhs)
            for z in cells:
                n_n2 += 1
                ok &= (pmul({(z,)}, lhs) == pmul({(z,)}, rhs))
    check(f"{tag} N2 (x_z * I1 star-cross, degree 3) all {n_n2} shift instances", ok)

    # SH: single-cell shifts of M1/M2/M3/I1 into degree-3 room
    ok = True; n_sh = 0
    inst = []
    for i in range(np_):
        for ip in range(np_):
            if ip == i: continue
            for j in range(nh):
                inst.append((padd(pmul({(v(ip, j),)}, Q(i)),
                                  padd(C(i, ip, j), RS(i, ip, j))), ZERO))
    for i in range(np_):
        for j in range(nh):
            for jp in range(nh):
                if j == jp: continue
                acc = padd(pmul({(v(i, jp),)}, Q(i)), H(i, j, jp))
                acc = padd(acc, B(v(i, jp)))
                for t in range(nh):
                    if t not in (j, jp): acc = padd(acc, H(i, t, jp))
                inst.append((acc, ZERO))
    for i in range(np_):
        for j in range(nh):
            acc = padd(pmul({(v(i, j),)}, Q(i)), B(v(i, j)))
            for t in range(nh):
                if t != j: acc = padd(acc, H(i, t, j))
            inst.append((acc, ZERO))
    for i in range(np_):
        for ip in range(np_):
            if ip == i: continue
            for j in range(nh):
                for jp in range(nh):
                    if j == jp: continue
                    inst.append((I1_lhs(i, ip, j, jp), I1_rhs(i, ip, j, jp)))
    for z in cells:
        for lhs, rhs in inst:
            n_sh += 1
            ok &= (pmul({(z,)}, lhs) == pmul({(z,)}, rhs))
    check(f"{tag} SH (single-cell shifts of M1/M2/M3/I1) all {n_sh} instances", ok)
    note(f"({tag}) part I done in {time.time()-t0:.1f}s")

# ---------------------------------------------------------------------------
# Part B: the truncated Buchberger completion engine
# ---------------------------------------------------------------------------

def nf_full(state, gens, heads, by_head, key):
    """full division within the degree cap (states only ever contain monomials
    of degree <= t): kill any monomial divisible by some head; each kill adds
    only strictly smaller monomials, so this terminates."""
    state = set(state)
    while True:
        hit = None
        for T in sorted(state, key=key, reverse=True):
            for D in submultisets(T):
                lst = by_head.get(D)
                if lst:
                    hit = (T, lst[0], mquo(T, D))
                    break
            if hit: break
        if hit is None:
            return frozenset(state)
        T, gi, m = hit
        for u in gens[gi]:
            mm = tuple(sorted(m + u))
            if mm in state: state.remove(mm)
            else: state.add(mm)
        if not state:
            return frozenset(state)

def gb_complete(np_, nh, t, variant, kind, wt_piv, midx, tag,
                time_cap=420.0, max_added=5000, scope="target"):
    """One-shot pair queue (standard incremental Buchberger): each pair is
    processed once; a zero-reduction stays a zero-reduction as the set grows,
    so an empty queue certifies the TB hypothesis for the final G*."""
    from collections import deque
    t0 = time.time()
    key = order_key(kind, np_, nh)
    gens = [g for _, g in build_gens(np_, nh, variant)]
    heads = [max(g, key=key) for g in gens]
    by_head = defaultdict(list)
    for i, h in enumerate(heads): by_head[h].append(i)
    base = len(gens)
    gset = set(gens)

    def vec_of(p):
        vv = 0
        for m in p: vv |= 1 << midx[m]
        return vv

    shift_monos_cache = {}
    def verify_neutral(R):
        if not in_span(vec_of(R), wt_piv):
            return "R not in W_t"
        dg = max(len(m) for m in R)
        sms = shift_monos_cache.get(dg)
        if sms is None:
            sms = [m for m in midx if len(m) <= t - dg]
            shift_monos_cache[dg] = sms
        for m in sms:
            sh = frozenset(tuple(sorted(m + u)) for u in R)
            if not in_span(vec_of(sh), wt_piv):
                return f"shift {m} not in W_t"
        return None

    def lcm_ok(i, j):
        hi, hj = heads[i], heads[j]
        if len(set(hi) | set(hj)) > t: return False
        return len(mlcm(hi, hj)) <= t

    queue = deque()
    inq = set()
    for i in range(base):
        for j in range(i + 1, base):
            if lcm_ok(i, j):
                queue.append((i, j)); inq.add((i, j))

    exotic = None
    added = 0
    add_types = []
    added_degs = []
    processed = 0
    passes = 0

    def process_queue():
        nonlocal processed, added, exotic
        while queue:
            if time.time() - t0 > time_cap or added > max_added:
                return False
            i, j = queue.popleft()
            inq.discard((i, j))
            processed += 1
            if processed % 25000 == 0:
                note(f"  ... {tag} t={t} [{variant}/{kind}]: {processed} pairs, "
                     f"{added} added, {len(queue)} queued, {time.time()-t0:.0f}s")
            hi, hj = heads[i], heads[j]
            L = mlcm(hi, hj)
            if len(L) > t: continue
            S = padd(pmul(gens[i], {mquo(L, hi)}), pmul(gens[j], {mquo(L, hj)}))
            if not S: continue
            R = nf_full(S, gens, heads, by_head, key)
            if R:
                if add_if_neutral(R, f"pair ({i},{j})") is False:
                    return False
        return True

    def add_if_neutral(R, src):
        nonlocal added, exotic
        why = verify_neutral(R)
        if why is not None:
            exotic = (src, sorted(R), why)
            return False
        gens.append(R); gset.add(R)
        heads.append(max(R, key=key))
        by_head[heads[-1]].append(len(gens) - 1)
        n = len(gens) - 1
        for k in range(n):
            if lcm_ok(k, n) and (k, n) not in inq:
                queue.append((k, n)); inq.add((k, n))
        added += 1
        added_degs.append(max(len(m) for m in R))
        if added <= 12:
            add_types.append((src, sorted(R)))
        return True

    while True:
        passes += 1
        if not process_queue():
            break
        # verification pass over ALL pairs of the final set: the one-shot queue
        # is certified only after a full pass finds every S-poly reducing to 0
        bad = []
        n = len(gens)
        for i in range(n):
            if exotic is not None or time.time() - t0 > time_cap:
                break
            hi = heads[i]; shi = set(hi)
            for j in range(i + 1, n):
                if len(shi | set(heads[j])) > t: continue
                if len(mlcm(hi, heads[j])) > t: continue
                S = padd(pmul(gens[i], {mquo(mlcm(hi, heads[j]), hi)}),
                         pmul(gens[j], {mquo(mlcm(hi, heads[j]), heads[j])}))
                if not S: continue
                R = nf_full(S, gens, heads, by_head, key)
                if R:
                    bad.append((i, j, R))
        if exotic is not None:
            break
        if not bad:
            break
        for (i, j, R) in bad:
            if add_if_neutral(R, f"verify ({i},{j})") is False:
                break
        if exotic is not None or passes >= 6:
            break
        for i in range(base, len(gens)):
            for j in range(i):
                if lcm_ok(j, i) and (j, i) not in inq:
                    queue.append((j, i)); inq.add((j, i))

    ok = (exotic is None) and (not queue)
    degs = Counter(added_degs)
    status = ("completion closed: I cap S_<=t = W_t PROVED at this rectangle"
              if ok else
              ("EXOTIC RELATION (disproof candidate)" if exotic else
               f"INCOMPLETE (cap; {len(queue)} pairs unprocessed)"))
    info = (f"{base}+{added} gens ({dict(sorted(degs.items()))} by degree), "
            f"{processed} pairs processed, {passes} pass(es); {status}; "
            f"{time.time()-t0:.1f}s")
    if scope == "target":
        check(f"{tag} t={t} completion [{variant}, order {kind}]", ok, info)
    else:
        note(f"[diagnostic] {tag} t={t} completion [{variant}, order {kind}]: {info}")
        print(f"[{'PASS' if ok else 'INFO'}] (diagnostic, outside INV(3) scope: "
              f"d = {nh // 2} < t = {t}) {tag} t={t} [{variant}/{kind}] {info}",
              flush=True)
    for k, (src, R) in enumerate(add_types):
        note(f"  added[{k}] from {src}: {R}")
    if exotic:
        note(f"  EXOTIC: {exotic}")
    return ok

# ---------------------------------------------------------------------------
# Part D: dimension anchors
# ---------------------------------------------------------------------------

def part_D():
    # ---- (4,2)
    np_, nh = 5, 4
    monos = rect_monomials(np_, nh, 2)
    midx = {t: k for k, t in enumerate(monos)}
    piv = echelon(dedupe(rect_rows(np_, nh, 2, monos, midx)))
    check("(4,2) dim V_<=2 = 165", len(piv) == 165, f"rank {len(piv)}")
    check("(4,2) e0 not in V_<=2", not in_span(1, piv))
    monos54 = rect_monomials(np_, nh, 3)
    midx54 = {t: k for k, t in enumerate(monos54)}
    t0 = time.time()
    piv54 = echelon(dedupe(rect_rows(np_, nh, 3, monos54, midx54)))
    note(f"5x4 degree-<=3 echelon: rank {len(piv54)} of {len(monos54)} coords, "
         f"{time.time()-t0:.1f}s")

    # ---- (6,3)
    np_, nh = 7, 6
    monos3 = rect_monomials(np_, nh, 3)
    midx3 = {t: k for k, t in enumerate(monos3)}
    t0 = time.time()
    rows3 = dedupe(rect_rows(np_, nh, 3, monos3, midx3))
    piv3 = echelon(rows3)
    check("(6,3) rank V_<=3 = 12110", len(piv3) == 12110,
          f"rank {len(piv3)}, {time.time()-t0:.1f}s")
    check("(6,3) dim Des = 2079", len(monos3) - len(piv3) - 1 == 2079,
          f"dim Des {len(monos3) - len(piv3) - 1}")
    check("(6,3) e0 not in V", not in_span(1, piv3))
    n2 = 1 + np_ * nh + math.comb(np_ * nh + 1, 2)
    rank_high = len(echelon([vv >> n2 for vv in rows3]))
    dim_cap2 = len(piv3) - rank_high
    monos2 = rect_monomials(np_, nh, 2)
    midx2 = {t: k for k, t in enumerate(monos2)}
    piv2 = echelon(dedupe(rect_rows(np_, nh, 2, monos2, midx2)))
    check("(6,3) Q-A(2) re-anchor: dim(V cap S_<=2) = dim V_<=2 = 511",
          dim_cap2 == len(piv2) == 511,
          f"dim cap {dim_cap2}, dim V_<=2 {len(piv2)}")
    note("(6,3) t=3 slice is the tautology dim(V cap S_<=3) = dim V_<=3 at d = 3")
    return piv54, midx54, piv3, monos3, midx3

# ---------------------------------------------------------------------------
# Part E: the (8,4) instrument
# ---------------------------------------------------------------------------

def part_E(monos8, midx8, piv8):
    t0 = time.time()
    deg3 = [m for m in monos8 if len(m) == 3]
    nlines = 0
    nfails = 0
    nfails_diag = 0
    ndiag = 0
    for m in deg3:
        linepair = False
        for a in range(3):
            for b in range(a + 1, 3):
                ca, cb = m[a], m[b]
                if ca == cb: continue
                if (ca // 8 == cb // 8) or (ca % 8 == cb % 8):
                    linepair = True
        ok = in_span(1 << midx8[m], piv8)
        if linepair:
            nlines += 1
            if not ok: nfails += 1
        else:
            ndiag += 1
            if not ok: nfails_diag += 1
    note(f"(8,4) degree-3 monomials: {len(deg3)}; line-pair class {nlines} "
         f"(unit vectors outside V_<=3: {nfails}); diagonal/alias class {ndiag} "
         f"(outside V_<=3: {nfails_diag})")
    check("(8,4) every line-pair degree-3 unit vector lies in V_<=3", nfails == 0,
          f"{nlines} line-pair monomials tested")
    check("(8,4) some diagonal/alias degree-3 unit vectors lie outside V_<=3 "
          "(Theorem A consistency: matching-3 columns vary)", nfails_diag > 0,
          f"{nfails_diag} of {ndiag} outside V_<=3")
    # e0 clause at (8,4): e0 not in pi_{S_<=3}(V_<=4) implies e0 not in V(8,4)
    # (e0 in V_<=4 => e0 = pi(e0) in pi(V_<=4)); pi_{S_<=3}(V_<=4) = V_<=3 +
    # span{e_m : m deg 3} by the monoidal decomposition, so membership of e0 in
    # that span is decidable on the S_<=3 echelon alone.
    piv8b = dict(piv8)
    for m in deg3:
        v = 1 << midx8[m]
        while v:
            h = v.bit_length() - 1
            q = piv8b.get(h)
            if q is None:
                piv8b[h] = v; break
            v ^= q
    check("(4,2)/(6,3)/(8,4) e0 not in V_<=3 (9x8 echelon)",
          not in_span(1, piv8))
    # e0 IN pi_{S_<=3}(V_<=4) is expected when true: it witnesses the degree-3
    # OFF-analogue structure (V_<=3 contains elements e0 + pure-degree-3, the
    # degree-3 analogue of OFF = Sigma_off + e0 in V_<=2).  It does NOT bear on
    # the e0 clause of INV(3)(i), which is e0 not in V(8,4) and follows from
    # designs existing (paper Theorem 4.1, every (n,d)); the direct echelon
    # over S_<=4 is the known deg4 wall.
    check("(8,4) e0 membership in pi_{S_<=3}(V_<=4) decided (OFF-analogue probe)",
          True, f"e0 in pi(V_<=4): {in_span(1, piv8b)}")
    note(f"part E done in {time.time()-t0:.1f}s")

# ---------------------------------------------------------------------------

def main():
    t00 = time.time()
    print("== chi_inv3_check: INV(3), the t=3 degree-truncated Buchberger ==")
    print(f"--fast={FAST}")

    print("== Part I: master identities ==", flush=True)
    part_I(5, 4, "5x4")
    part_I(7, 6, "7x6")

    print("== Part D: dimension anchors ==", flush=True)
    piv54, midx54, piv63, monos63, midx63 = part_D()

    print("== Part B: truncated Buchberger completion ==", flush=True)
    # t=2 re-anchor (engine repair for the t=2 record)
    monos54_2 = rect_monomials(5, 4, 2)
    midx54_2 = {t: k for k, t in enumerate(monos54_2)}
    piv54_2 = echelon(dedupe(rect_rows(5, 4, 2, monos54_2, midx54_2)))
    gb_complete(5, 4, 2, "G", "A", piv54_2, midx54_2, "5x4")
    gb_complete(7, 6, 2, "G", "A", echelon(dedupe(rect_rows(7, 6, 2,
                 rect_monomials(7, 6, 2),
                 {t: k for k, t in enumerate(rect_monomials(7, 6, 2))}))),
                {t: k for k, t in enumerate(rect_monomials(7, 6, 2))}, "7x6")
    # t=3, the INV(3) target
    for kind in ("A", "C"):
        for variant in ("G", "G'"):
            gb_complete(7, 6, 3, variant, kind, piv63, midx63, "7x6")
    # 5x4 at t=3 is OUTSIDE INV(3) scope (d = 2 < t = 3); run as a diagnostic:
    # it exhibits an explicit exotic degree-3 relation of the 4-hole system.
    for kind in ("A", "C"):
        for variant in ("G", "G'"):
            gb_complete(5, 4, 3, variant, kind, piv54, midx54, "5x4",
                        scope="diagnostic", time_cap=120.0)

    if not FAST:
        print("== Part B (9x8) + Part E: the (8,4) system ==", flush=True)
        t0 = time.time()
        monos8 = rect_monomials(9, 8, 3)
        midx8 = {t: k for k, t in enumerate(monos8)}
        rows8 = dedupe(rect_rows(9, 8, 3, monos8, midx8))
        piv8 = echelon(rows8)
        note(f"9x8 degree-<=3 echelon: {len(rows8)} rows, rank {len(piv8)} "
             f"of {len(monos8)} coords, {time.time()-t0:.1f}s")
        check("(8,4) dim V_<=3 (9x8 echelon) computed, rank <= coords",
              len(piv8) <= len(monos8), f"rank {len(piv8)}")
        for kind in ("A", "C"):
            for variant in ("G", "G'"):
                gb_complete(9, 8, 3, variant, kind, piv8, midx8, "9x8",
                            time_cap=600.0)
        print("== Part E: (8,4) monoidal-decomposition instrument ==", flush=True)
        part_E(monos8, midx8, piv8)

    print(f"\n== summary: {PASS} PASS / {FAIL} FAIL, {time.time()-t00:.1f}s total ==")
    return 0 if FAIL == 0 else 1

if __name__ == "__main__":
    sys.exit(main())
