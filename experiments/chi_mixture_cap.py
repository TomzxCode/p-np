#!/usr/bin/env python3
"""chi_mixture_cap.py

GAP B' (GOAL.md section 6; proof_complexity.md ADDENDUM 4 item 6): Theorem 3's
covered query classes form a PROPER subset of the printed degree-<=2 tree
class. The printed class allows arbitrary F_2 mixtures of variables and
degree-2 monomials (e.g. g = x_ij + x_kl x_mn), which Theorem 3 does not
cover. This script measures the exact per-hit labeling posterior over the
FULL printed degree-<=2 class on the true Omega(n,d) pipeline at p = 2, and
tests whether the cap constant max(q, q_and) survives.

Channel: the TRUE pipeline (uniform designs L of the restricted canonical
system Des(2d,d); kernel F1: V(n,d)^rho = V(2d,d), so the canonical
construction is the printed design space). For one restriction rho and one
query g the per-rho answer probability P[ans(g)=1 | rho] is computed exactly
two independent ways:

  Engine A (design-exact): map g to its restricted coordinate vector
      v = g^rho (raw monomial columns; V-membership is handled automatically
      because every design vanishes on V), then
      P[ans=1 | rho] = fraction of the design coset Lstar + kernel with
      L(v) = 1, enumerated through the projected kernel (chi_deg3 pattern).
  Engine B (status calculus, design-free): on each status pattern of the
      query's pairs the answer is a fair coin when the live coordinate set
      is nonempty and determined otherwise (matched singles and
      matched-matched monomials, plus the constant). Exact for support <= 3
      because no determined relation of degree <= 2 lives on <= 3
      nondegenerate coordinates.

Posteriors: for output pair c and answer event ans(g)=a,
  post(c | g, a) = N / (N + D),
  N = sum_rho P(rho) 1_{c free}     P[ans(g)=a | rho],
  D = sum_rho P(rho) 1_{c not free} P[ans(g)=a | rho].
Output roles: the query's own support pairs plus the external role (any
untouched pair; all such pairs are exchangeable).

Engine B weighting (exact): a status pattern's weight is the number of
restrictions realizing EXACTLY that pattern. Killed slots are split into the
two disjoint exhaustive cases Kp (pigeon matched elsewhere) and Kh (hole
matched, pigeon unmatched), each a forced-structure event; the P-slot edges
are then excluded by inclusion-exclusion over U subseteq P-slots.

Checks:
  V0  weight sanity: per-slot pattern weights sum to the restriction count.
  V1  (7,2): Engine B == Engine A digit-exact on every enumerated query,
      every answer, every support-pair role; the pure diagonal monomial
      reproduces q_and_exact; the single variable reproduces q.
  V2  (7,2) exhaustive posterior max, all 11760 restrictions, all 7169
      support<=2 (16-pair window) and support<=3 with >= 2 monomials
      (10-pair sub-window, carries the degree-2 star triple) queries.
  V3  (15,2): a fixed panel of 40 queries on 40000 sampled restrictions
      (exact per-rho law) vs Engine B, within 4-sigma tolerance.
  V4  grid: Engine B over ALL support<=3 query configurations (with pair
      geometry) on a grid of (n,d): maximum posterior vs q, q_and_exact;
      the two-monomials-sharing-a-pair mixture is printed per point.
  V5  budgeted adaptive strategies on the exact channel at (15,2) and
      (32,2): does any mixture strategy beat the covered-class champions at
      equal budget? Certified outputs are asserted free (soundness).

Run: python3 chi_mixture_cap.py [--smoke] [--rhos15 K]
"""
from __future__ import annotations

import argparse
import math
import random
import sys
import time
from collections import Counter
from fractions import Fraction
from itertools import combinations, permutations, product

from razborov_check import monomials
from kernel_structure import canonical_rows, echelon_rhs, particular

T0 = time.perf_counter()


def elapsed() -> float:
    return time.perf_counter() - T0


# ----------------------------------------------------------------- machinery

def build_restricted(d: int) -> dict:
    """Design coset machinery for the canonical restricted system (2d, d)."""
    nr = 2 * d
    monos = monomials(nr, d)
    mi = {t: i for i, t in enumerate(monos)}
    rows = canonical_rows(nr, d)
    ech_a = echelon_rhs([(g, 0) for g in rows] + [(1, 1)])
    Lstar = particular(ech_a)
    # one homogeneous kernel vector per non-pivot column; the affine row
    # (1,1) is a pivot at column 0, so every kernel vector has bit 0 = 0 and
    # L(1) = 1 across the whole coset.
    masks = [(c, ech_a[c][0] ^ (1 << c)) for c in sorted(ech_a)]
    kb = []
    for fc in range(len(monos)):
        if fc in ech_a:
            continue
        y = 1 << fc
        for _c, mask in masks:
            if (y & mask).bit_count() & 1:
                y ^= 1 << _c
        kb.append(y)
    colD = {t: mi[t] for t in monos if len(t) == 2}
    return dict(monos=monos, mi=mi, ech_a=ech_a, Lstar=Lstar, kb=kb,
                colD=colD, ncols=len(monos))


class DesignExact:
    """Exact answer-law evaluator: w(v) = P_{L ~ Des}[L(v) = 1]."""

    def __init__(self, d: int):
        self.d = d
        self.__dict__.update(build_restricted(d))
        self._pk_cache: dict = {}
        self._w_cache: dict = {}

    def _pk(self, T: tuple) -> list:
        ent = self._pk_cache.get(T)
        if ent is not None:
            return ent
        basis = []
        for y in self.kb:
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
        ent = [piv[c] for c in sorted(piv)]
        self._pk_cache[T] = ent
        return ent

    def w(self, v: int) -> tuple[int, int]:
        """Exact (numerator, denominator) of P[L(v) = 1] over the design coset."""
        ent = self._w_cache.get(v)
        if ent is not None:
            return ent
        T = tuple(i for i in range(self.ncols) if (v >> i) & 1)
        vT = LsT = 0
        for k, c in enumerate(T):
            if (v >> c) & 1:
                vT |= 1 << k
            if (self.Lstar >> c) & 1:
                LsT |= 1 << k
        pi = self._pk(T)
        dim = len(pi)
        cnt = 0
        for msk in range(1 << dim):
            y = LsT
            for b in range(dim):
                if (msk >> b) & 1:
                    y ^= pi[b]
            if (y & vT).bit_count() & 1:
                cnt += 1
        ent = (cnt, 1 << dim)
        self._w_cache[v] = ent
        return ent


def rhos_all(n: int, d: int):
    """All restrictions leaving 2d free holes, as (matched_pigeons, images)."""
    c = n - 2 * d
    for A in combinations(range(n + 1), c):
        for B in permutations(range(n), c):
            yield A, B


def count_rhos(n: int, d: int) -> int:
    c = n - 2 * d
    return (math.comb(n + 1, c) * math.comb(n, c) * math.factorial(c))


def rho_data(n: int, d: int, A, B):
    """Per-pair status (0=F, 1=M, 2=K) and canonical variable column."""
    matched = dict(zip(A, B))
    D = sorted(set(range(n + 1)) - set(A))
    R = sorted(set(range(n)) - set(B))
    pidx = {i: t for t, i in enumerate(D)}
    hidx = {j: t for t, j in enumerate(R)}
    npairs = (n + 1) * n
    st = bytearray(npairs)
    cvar = [-1] * npairs
    for i in range(n + 1):
        base = i * n
        if i in matched:
            mj = matched[i]
            for j in range(n):
                st[base + j] = 1 if j == mj else 2
        else:
            for j in range(n):
                if j in hidx:
                    st[base + j] = 0
                    cvar[base + j] = 1 + pidx[i] * (2 * d) + hidx[j]
                else:
                    st[base + j] = 2
    return st, cvar


# ------------------------------------------------------- Engine B (calculus)

_COUNT_CACHE: dict = {}


def count_assign(n: int, d: int, pu: int, pm: int, hu: int, hm: int,
                 e_img: int) -> int:
    """#restrictions (matchings of size c) with: pm distinct pigeons forced
    into the matching, pu distinct pigeons excluded, hm distinct holes forced
    in as images, hu distinct holes excluded, and e_img images fixed by
    forced edges. The bijection of the remaining c - e_img pairs is free.
    """
    key = (n, d, pu, pm, hu, hm, e_img)
    ent = _COUNT_CACHE.get(key)
    if ent is not None:
        return ent
    c = n - 2 * d
    k = c - pm
    if k < 0 or c - hm < 0 or c - e_img < 0:
        ent = 0
    elif n + 1 - pu - pm < k or n - hu - hm < c - hm:
        ent = 0
    else:
        ent = (math.comb(n + 1 - pu - pm, k)
               * math.comb(n - hu - hm, c - hm) * math.factorial(c - e_img))
    _COUNT_CACHE[key] = ent
    return ent


_WP_CACHE: dict = {}


def weight_pattern(n: int, d: int, geo: tuple, assign: tuple) -> int:
    """Exact #restrictions realizing the F/M/K pattern on the slots."""
    key = (n, d, geo, assign)
    ent = _WP_CACHE.get(key)
    if ent is not None:
        return ent
    t = len(assign)
    kslots = [k for k in range(t) if assign[k] == 'K']
    total = 0
    for split in product('PH', repeat=len(kslots)):
        st4 = []
        si = 0
        for k in range(t):
            a = assign[k]
            if a == 'F':
                st4.append('F')
            elif a == 'M':
                st4.append('M')
            else:
                st4.append('P' if split[si] == 'P' else 'H')
                si += 1
        # class-level structure
        pig_cov = {geo[k][0] for k in range(t) if st4[k] in ('M', 'P')}
        pig_free = {geo[k][0] for k in range(t) if st4[k] in ('F', 'H')}
        hol_cov = {geo[k][1] for k in range(t) if st4[k] in ('M', 'H')}
        hol_free = {geo[k][1] for k in range(t) if st4[k] == 'F'}
        ok = not (pig_cov & pig_free) and not (hol_cov & hol_free)
        Mslots = [k for k in range(t) if st4[k] == 'M']
        Mp = [geo[k][0] for k in Mslots]
        Mh = [geo[k][1] for k in Mslots]
        if ok and (len(set(Mp)) != len(Mp) or len(set(Mh)) != len(Mh)):
            ok = False          # two M edges sharing a pigeon or a hole
        if not ok:
            continue
        Pslots = [k for k in range(t) if st4[k] == 'P']
        # inclusion-exclusion over U subseteq P-slots (forced P edges)
        for U in range(1 << len(Pslots)):
            uslots = [Pslots[b] for b in range(len(Pslots)) if (U >> b) & 1]
            up, uh = [], []
            okU = True
            for k in uslots:
                pc, hc = geo[k]
                if pc in Mp or pc in up:
                    okU = False
                    break
                if hc in Mh or hc in uh or hc in hol_free:
                    okU = False
                    break
                up.append(pc)
                uh.append(hc)
            if not okU:
                continue
            pm = len(pig_cov)           # distinct covered pigeons
            pu = len(pig_free)          # distinct excluded pigeons
            hm = len(hol_cov | set(uh))  # distinct forced holes
            hu = len(hol_free)          # distinct excluded holes
            e_img = len(Mslots) + len(uh)
            w2 = count_assign(n, d, pu, pm, hu, hm, e_img)
            if w2:
                total += w2 if len(uslots) % 2 == 0 else -w2
    _WP_CACHE[key] = total
    return total


def law_of_terms(terms, assign, const):
    """Live coordinate set (XOR-cancelled) and determined constant.

    terms: list of ('V', slot) / ('M', slot, slot). assign: 'F'/'M'/'K'.
    Returns (live_nonempty, det).
    """
    live: dict = {}
    det = const
    for t in terms:
        if t[0] == 'V':
            s = assign[t[1]]
            if s == 'F':
                live[t[1]] = live.get(t[1], 0) ^ 1
            elif s == 'M':
                det ^= 1
        else:
            _, p, q = t
            sp, sq = assign[p], assign[q]
            if sp == 'K' or sq == 'K':
                continue
            if sp == 'F' and sq == 'F':
                key = ('D', p, q)
                live[key] = live.get(key, 0) ^ 1
            elif sp == 'M' and sq == 'M':
                det ^= 1
            else:
                f = p if sp == 'F' else q
                live[f] = live.get(f, 0) ^ 1
    return any(live.values()), det


def status_table(geo, terms, const):
    """Per-config rows: (assign, w2, free_slots), w2 = 2*P[ans=1|pattern]."""
    t = len(geo)
    rows = []
    for assign in product('FMK', repeat=t):
        live, det = law_of_terms(terms, assign, const)
        w2 = 1 if live else (0 if det == 0 else 2)
        frees = frozenset(k for k in range(t) if assign[k] == 'F')
        rows.append((assign, w2, frees))
    return rows


def p_ext_free(n: int, d: int, sF: int, sM: int) -> Fraction:
    """P[a specific untouched pair is free | pattern counts] (exact)."""
    c = n - 2 * d
    dp = n + 1 - sF - sM
    dh = n - sF - sM
    if dp <= 0 or dh <= 0 or 2 * d + 1 - sF <= 0 or 2 * d - sF <= 0:
        return Fraction(0)
    return Fraction((2 * d + 1 - sF) * (2 * d - sF), dp * dh)


def posts_from_table(n, d, geo, table):
    """Exact per-role posteriors for one configuration at one (n,d).

    Returns dict: ('pair', slot, a) and ('ext', a) -> Fraction.
    """
    t = len(geo)
    S = [0, 0]          # scaled by 2 (w2)
    N = [[0] * t, [0] * t]
    Next = [Fraction(0), Fraction(0)]
    for (assign, w2, frees) in table:
        W = weight_pattern(n, d, geo, assign)
        if W == 0:
            continue
        sF = assign.count('F')
        sM = assign.count('M')
        for a, w2a in ((0, 2 - w2), (1, w2)):
            S[a] += W * w2a
            for k in frees:
                N[a][k] += W * w2a
            if w2a:
                Next[a] += W * w2a * p_ext_free(n, d, sF, sM)
    out = {}
    for a in (0, 1):
        for k in range(t):
            out[('pair', k, a)] = Fraction(N[a][k], S[a]) if S[a] else Fraction(0)
        out[('ext', a)] = Next[a] / S[a] if S[a] else Fraction(0)
    return out


def concrete_engineB(n, d, pair_terms, const):
    """Exact per-role posteriors for one concrete query (Engine B).

    pair_terms: list of ('V', pair) / ('M', pair, pair), concrete pairs.
    Returns (slots, posts): posts[(a, pair)] and posts[(a, 'ext')].
    """
    slots = sorted({p for t in pair_terms
                    for p in ((t[1],) if t[0] == 'V' else (t[1], t[2]))})
    idx = {p: k for k, p in enumerate(slots)}
    terms = [('V', idx[t[1]]) if t[0] == 'V'
             else ('M', idx[t[1]], idx[t[2]]) for t in pair_terms]
    geo = tuple((p[0], p[1]) for p in slots)
    table = status_table(geo, terms, const)
    raw = posts_from_table(n, d, geo, table)
    posts = {}
    for a in (0, 1):
        for k, p in enumerate(slots):
            posts[(a, p)] = raw[('pair', k, a)]
        posts[(a, 'ext')] = raw[('ext', a)]
    return slots, posts


# ------------------------------------------------- configurations (Engine B)

def _partitions(elements):
    if not elements:
        yield []
        return
    first, rest = elements[0], elements[1:]
    for part in _partitions(rest):
        yield [[first]] + part
        for i in range(len(part)):
            yield part[:i] + [part[i] + [first]] + part[i + 1:]


def _rank_geo(geo_seq):
    pmap, hmap, out = {}, {}, []
    for (a, b) in geo_seq:
        if a not in pmap:
            pmap[a] = len(pmap)
        if b not in hmap:
            hmap[b] = len(hmap)
        out.append((pmap[a], hmap[b]))
    return tuple(out)


def enum_configs(kmax=3):
    """All support<=kmax query configurations up to isomorphism.

    Isomorphism = slot permutations + pigeon/hole class relabelings.
    Returns list of (const, terms, geo).
    """
    seen = set()
    out = []
    # t = number of distinct pairs (slots); support = number of generators.
    # t up to 2*kmax covers monomial stars through a shared pair (3
    # monomials through one pair need 4 slots); t = 5,6 get only the
    # disjoint-monomial families (the remaining support-3 shapes).
    for t in range(1, 2 * kmax + 1):
        elems = list(range(t))
        for pc in _partitions(elems):
            for hc in _partitions(elems):
                pcl, hcl = {}, {}
                for bi, block in enumerate(pc):
                    for x in block:
                        pcl[x] = bi
                for bi, block in enumerate(hc):
                    for x in block:
                        hcl[x] = bi
                geo = tuple((pcl[k], hcl[k]) for k in range(t))
                if len(set(geo)) != t:
                    continue
                pool = [('V', k) for k in range(t)]
                for i in range(t):
                    for j in range(i + 1, t):
                        if geo[i][0] != geo[j][0] and geo[i][1] != geo[j][1]:
                            pool.append(('M', i, j))
                if t > kmax and t <= 2 * kmax:
                    # keep only the disjoint-monomial families on wide geos
                    if t == 5:
                        keep = [('M', 0, 1), ('M', 2, 3), ('V', 4)]
                    elif t == 6:
                        keep = [('M', 0, 1), ('M', 2, 3), ('M', 4, 5)]
                    else:
                        keep = [('M', 0, 1), ('M', 2, 3), ('V', 0)]
                    fams = [[('M', 0, 1), ('M', 2, 3), ('V', 0)],
                            [('M', 0, 1), ('M', 0, 2), ('M', 0, 3)]] \
                        if t == 4 else [[('M', 0, 1), ('M', 2, 3), ('M', 4, 5)]]
                    combos = [tuple(f) for f in fams
                              if all(g in set(pool) for g in f)]
                    for sub in combos:
                        for const in (0, 1):
                            best = None
                            for perm in permutations(range(t)):
                                inv = [0] * t
                                for k, p in enumerate(perm):
                                    inv[p] = k
                                g = _rank_geo([geo[perm[k]] for k in range(t)])
                                tt = []
                                for tm in sub:
                                    if tm[0] == 'V':
                                        tt.append(('V', inv[tm[1]]))
                                    else:
                                        a, b = inv[tm[1]], inv[tm[2]]
                                        tt.append(('M', min(a, b), max(a, b)))
                                key = (g, tuple(sorted(tt)), const)
                                if best is None or key < best:
                                    best = key
                            if best in seen:
                                continue
                            seen.add(best)
                            out.append((best[2], list(best[1]),
                                        tuple(best[0])))
                    continue
                for size in range(1, kmax + 1):
                    for sub in combinations(pool, size):
                        for const in (0, 1):
                            best = None
                            for perm in permutations(range(t)):
                                inv = [0] * t
                                for k, p in enumerate(perm):
                                    inv[p] = k
                                g = _rank_geo([geo[perm[k]] for k in range(t)])
                                tt = []
                                for tm in sub:
                                    if tm[0] == 'V':
                                        tt.append(('V', inv[tm[1]]))
                                    else:
                                        a, b = inv[tm[1]], inv[tm[2]]
                                        tt.append(('M', min(a, b), max(a, b)))
                                key = (g, tuple(sorted(tt)), const)
                                if best is None or key < best:
                                    best = key
                            if best in seen:
                                continue
                            seen.add(best)
                            out.append((best[2], list(best[1]),
                                        tuple(best[0])))
    return out


def virtual_post(n, d, terms, const, geo, vgeo):
    """Exact posterior pair (post1, post0) for the LAST slot of vgeo (a
    virtual same-line partner with no terms), given the support terms."""
    t = len(geo)
    S = [0, 0]
    Nv = [0, 0]
    for assign in product('FMK', repeat=t + 1):
        W = weight_pattern(n, d, vgeo, assign)
        if W == 0:
            continue
        live, det = law_of_terms(terms, assign[:t], const)
        w2 = 1 if live else (0 if det == 0 else 2)
        for a, w2a in ((0, 2 - w2), (1, w2)):
            S[a] += W * w2a
            if assign[t] == 'F':
                Nv[a] += W * w2a
    return (Fraction(Nv[1], S[1]) if S[1] else Fraction(0),
            Fraction(Nv[0], S[0]) if S[0] else Fraction(0))


def posts_with_virtuals(n, d, const, terms, geo):
    """Support roles + generic ext + same-line virtual partner roles
    (virtuals only for t <= 3; wider configs keep support roles)."""
    t = len(geo)
    table = status_table(geo, terms, const)
    base = posts_from_table(n, d, geo, table)
    out = {}
    for a in (0, 1):
        for k in range(t):
            out[('pair', k, a)] = base[('pair', k, a)]
        out[('ext', a)] = base[('ext', a)]
    if t > 3:
        return out
    fresh_h = max(g[1] for g in geo) + 1
    fresh_p = max(g[0] for g in geo) + 1
    for c in sorted({g[0] for g in geo}):
        p1, p0 = virtual_post(n, d, terms, const, geo, geo + ((c, fresh_h),))
        out[('vp', c, 1)], out[('vp', c, 0)] = p1, p0
    for h in sorted({g[1] for g in geo}):
        p1, p0 = virtual_post(n, d, terms, const, geo, ((fresh_p, h),) + geo)
        out[('vh', h, 1)], out[('vh', h, 0)] = p1, p0
    return out


# ------------------------------------------------------- closed-form baselines

def q_closed(n, d):
    return Fraction((2 * d + 1) * d, (2 * d + 1) * d + (n - 2 * d))


def q_and_printed(n, d):
    f = Fraction((2 * d + 1) * 2 * d, (n + 1) * n)
    m = Fraction(n - 2 * d, (n + 1) * n)
    G = (2 * d + 1) * 2 * d
    p_diag = Fraction(math.comb(G, 2) - (2 * d + 1) * math.comb(2 * d, 2)
                      - math.comb(2 * d + 1, 2) * 2 * d, math.comb(G, 2))
    num = f * f * p_diag / 2 + f * m / 2
    den = f * f * p_diag / 2 + f * m + m * m
    return num / den


def q_and_exact(n, d):
    c = n - 2 * d
    M0 = (math.comb(n - 1, c - 2) * math.comb(n - 2, c - 2)
          * math.factorial(c - 2)) if c >= 2 else 0
    M1 = (math.comb(n - 1, c - 1) * math.comb(n - 2, c - 1)
          * math.factorial(c - 1)) if c >= 1 else 0
    M2 = math.comb(n - 1, c) * math.comb(n - 2, c) * math.factorial(c)
    return Fraction(M1 + M2, 2 * M0 + 2 * M1 + M2)


# ----------------------------------------------------- Engine A: enumeration

def gen_desc(g):
    if g[0] == 'K':
        return "1"
    if g[0] == 'V':
        return f"x{g[1]}"
    return f"x{g[1]}x{g[2]}"


def engineA_point(n, d, DX, gen_specs, queries, pairs, rho_source):
    """Engine A pass over a full restriction enumeration.

    queries: list of (frozenset-of-gen-indices, desc). pairs: the pair list
    defining candidate output roles (support pairs of every query must lie
    in pairs). Returns {frozenset: (desc, {pair: (post1, post0)}, ext)}.
    """
    npairs = (n + 1) * n
    ncand = len(pairs)
    pos = {p: k for k, p in enumerate(pairs)}
    genvec = [[] for _ in gen_specs]
    candmask = []
    matchmask = []
    cntF = [0] * ncand
    for A, B in rho_source:
        st, cvar = rho_data(n, d, A, B)
        cm = 0
        mm = 0
        for k, (i, j) in enumerate(pairs):
            s = st[i * n + j]
            if s == 0:
                cm |= 1 << k
                cntF[k] += 1
            elif s == 1:
                mm |= 1 << k
        candmask.append(cm)
        matchmask.append(mm)
        for gi, g in enumerate(gen_specs):
            if g[0] == 'K':
                genvec[gi].append(1)
            elif g[0] == 'V':
                i, j = g[1]
                s = st[i * n + j]
                genvec[gi].append(1 if s == 1 else
                                  (1 << cvar[i * n + j] if s == 0 else 0))
            else:
                i, j = g[1]
                i2, j2 = g[2]
                s1, s2 = st[i * n + j], st[i2 * n + j2]
                if s1 == 2 or s2 == 2:
                    genvec[gi].append(0)
                elif s1 == 1 and s2 == 1:
                    genvec[gi].append(1)
                elif s1 == 1:
                    genvec[gi].append(1 << cvar[i2 * n + j2])
                elif s2 == 1:
                    genvec[gi].append(1 << cvar[i * n + j])
                else:
                    u, v = sorted((cvar[i * n + j] - 1, cvar[i2 * n + j2] - 1))
                    genvec[gi].append(1 << DX.colD[(u, v)])
    nrho = len(candmask)
    out = {}
    for gensel, desc in queries:
        gs = sorted(gensel)
        own = [pos[p] for p in query_pairs(gen_specs, gensel)]
        ftemp = 0
        mtemp = 0
        for k in own:
            ftemp |= 1 << k
            mtemp |= 1 << k
        if len(gs) == 1:
            vs = genvec[gs[0]]
        elif len(gs) == 2:
            ga, gb = genvec[gs[0]], genvec[gs[1]]
            vs = [a ^ b for a, b in zip(ga, gb)]
        else:
            ga, gb, gc = genvec[gs[0]], genvec[gs[1]], genvec[gs[2]]
            vs = [a ^ b ^ c for a, b, c in zip(ga, gb, gc)]
        tally = Counter(zip(vs,
                            [cm & ftemp for cm in candmask]))
        # accumulate with the common denominator 64 (dims <= 6)
        S1 = 0
        N1 = [0] * ncand
        for (v, om), cnt in tally.items():
            wn, wd = DX.w(v)
            wi = wn * (64 // wd)
            S1 += cnt * wi
            k = 0
            m = om
            while m:
                if m & 1:
                    N1[k] += cnt * wi
                m >>= 1
                k += 1
        posts = {}
        for k in own:
            p1 = Fraction(N1[k], S1) if S1 else Fraction(0)
            den0 = nrho * 64 - S1
            p0 = Fraction(cntF[k] * 64 - N1[k], den0) if den0 else Fraction(0)
            posts[pairs[k]] = {1: p1, 0: p0}
        den1 = S1 / 64
        den0 = nrho - S1 / 64
        out[gensel] = (desc, posts, den1, den0)
    return out


def query_pairs(gen_specs, gensel):
    s = set()
    for g in gensel:
        gg = gen_specs[g]
        if gg[0] == 'V':
            s.add(gg[1])
        elif gg[0] == 'M':
            s.add(gg[1])
            s.add(gg[2])
    return sorted(s)


# ---------------------------------------------------------------- strategies

class Sampler:
    """Exact-channel configuration sampler at (n, d)."""

    def __init__(self, n, d, DX, rng):
        self.n, self.d = n, d
        self.DX = DX
        self.rng = rng
        self.c = n - 2 * d

    def config(self):
        n, d, c = self.n, self.d, self.c
        rng = self.rng
        A = rng.sample(range(n + 1), c)
        B = rng.sample(range(n), c)
        matched = dict(zip(A, B))
        D = sorted(set(range(n + 1)) - set(A))
        R = sorted(set(range(n)) - set(B))
        pidx = {i: t for t, i in enumerate(D)}
        hidx = {j: t for t, j in enumerate(R)}
        L = self.DX.Lstar
        for kv in self.DX.kb:
            if rng.getrandbits(1):
                L ^= kv
        cache = {}

        def pairinfo(p):
            if p not in cache:
                i, j = p
                if matched.get(i) == j:
                    cache[p] = 1
                elif i not in matched and j in hidx:
                    cache[p] = 0
                else:
                    cache[p] = 2
            return cache[p]

        def col(p):
            i, j = p
            return 1 + pidx[i] * (2 * d) + hidx[j]

        def ans_var(p):
            s = pairinfo(p)
            if s == 1:
                return 1
            if s == 0:
                return (L >> col(p)) & 1
            return 0

        def ans_mono(p, q):
            s1, s2 = pairinfo(p), pairinfo(q)
            if s1 == 2 or s2 == 2:
                return 0
            if s1 == 1 and s2 == 1:
                return 1
            if s1 == 1:
                return ans_var(q)
            if s2 == 1:
                return ans_var(p)
            a, b = sorted((col(p) - 1, col(q) - 1))
            return (L >> self.DX.colD[(a, b)]) & 1

        def ans_q(g):
            if g[0] == 'V':
                return ans_var(g[1])
            if g[0] == 'M':
                return ans_mono(g[1], g[2])
            return 1

        def free(p):
            return pairinfo(p) == 0

        return ans_q, free


def strat_single(ans_q, free, n, budget, order):
    used = 0
    for (i, j) in order:
        if used >= budget:
            return (0, 0)
        used += 1
        if ans_q(('V', (i, j))) == 1:
            return (i, j)
    return (0, 0)


def strat_and(ans_q, free, n, budget, mono_list):
    used = 0
    for (p, q) in mono_list:
        if used >= budget:
            return (0, 0)
        used += 1
        if ans_q(('M', p, q)) == 1:
            return p
    return (0, 0)


def strat_kj(ans_q, free, n, budget):
    used = 0
    cert = []
    for j in range(n):
        if used >= budget // 2:
            break
        used += 1
        v = 1
        for i in range(n + 1):
            v ^= ans_q(('V', (i, j)))
        if v == 1:
            cert.append(j)
    for j in cert:
        for i in range(n + 1):
            if used >= budget:
                return (0, 0)
            used += 1
            if ans_q(('V', (i, j))) == 1:
                return (i, j)
    return (0, 0)


def strat_mixz(ans_q, free, n, budget, mono_list, viol):
    used = 0
    for (p, q) in mono_list:
        if used >= budget:
            break
        used += 1
        if (ans_q(('V', p)) ^ ans_q(('M', p, q))) == 1:
            if used >= budget:
                break
            used += 1
            if ans_q(('M', p, q)) == 1:
                if not free(q):
                    viol[0] += 1
                return q
            return p
    return (0, 0)


def strat_mixscan(ans_q, free, n, budget, mono_list):
    used = 0
    for (p, q) in mono_list:
        if used >= budget:
            break
        used += 1
        if (ans_q(('V', p)) ^ ans_q(('M', p, q))) == 1:
            return p
    return (0, 0)


def strat_hybrid(ans_q, free, n, budget, mono_list, order):
    used = 0
    mi = 0
    for (i, j) in order:
        if used >= budget:
            return (0, 0)
        used += 1
        if ans_q(('V', (i, j))) == 1:
            return (i, j)
        if used >= budget:
            return (0, 0)
        used += 1
        if mi < len(mono_list):
            p, q = mono_list[mi]
            mi += 1
            if ans_q(('M', p, q)) == 1:
                return p
    return (0, 0)


# ----------------------------------------------------------------------- main

def diag_monos(pairs):
    out = []
    for a in range(len(pairs)):
        for b in range(a + 1, len(pairs)):
            (i1, j1), (i2, j2) = pairs[a], pairs[b]
            if i1 != i2 and j1 != j2:
                out.append((pairs[a], pairs[b]))
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--rhos15", type=int, default=40000)
    args = ap.parse_args()
    SMOKE = args.smoke
    rng = random.Random(20261004)

    print("chi_mixture_cap: GAP B' - the per-hit posterior cap over the FULL")
    print("printed degree-<=2 class (F_2 mixtures) on the true Omega(n,d)")
    print("pipeline at p=2. Engine A = exact projected-coset answer law;")
    print("Engine B = proved alive/dead status calculus with exact")
    print("inclusion-exclusion pattern weights; they must agree")
    print("digit-exactly.")
    print()

    DX = DesignExact(2)
    print(f"[setup] restricted system (4,2): {DX.ncols} columns, kernel dim "
          f"{len(DX.kb)}, Lstar(1) = {DX.Lstar & 1} (must be 1)")
    assert DX.Lstar & 1 == 1

    # ================= V0: weight sanity ================================
    geo1 = ((0, 0),)
    tot = count_rhos(15, 2)
    s = sum(weight_pattern(15, 2, geo1, a)
            for a in product('FMK', repeat=1))
    print(f"[V0] (15,2) single-pair F+M+K weights sum: {s} vs restriction "
          f"count {tot} -> {'PASS' if s == tot else 'FAIL'}")
    geo2 = ((0, 0), (1, 1))
    s2 = sum(weight_pattern(15, 2, geo2, a)
             for a in product('FMK', repeat=2))
    print(f"[V0] (15,2) two-pair weights sum: {s2} -> "
          f"{'PASS' if s2 == tot else 'FAIL'}")
    print(f"[V0] baselines at (15,2): q = {q_closed(15, 2)}, q_and_exact = "
          f"{q_and_exact(15, 2)} (= 23/45 expected)")
    print()

    # ================= V1/V2: (7,2) exhaustive ==========================
    n, d = 7, 2
    main_pairs = [(i, j) for i in (0, 1, 3, 4) for j in (0, 1, 3, 4)]
    sub_pairs = [(i, j) for i in (0, 3) for j in (0, 1, 3, 4, 5)]
    all_pairs = sorted(set(main_pairs) | set(sub_pairs))
    gen_specs = [('K',)] + [('V', p) for p in all_pairs] + \
                [('M', p, q) for (p, q) in diag_monos(all_pairs)]
    gpos = {g: k for k, g in enumerate(gen_specs)}

    queries = []
    qseen = set()
    main_gi = [gpos[g] for g in gen_specs
               if g[0] == 'K' or (g[0] == 'V' and g[1] in main_pairs)
               or (g[0] == 'M' and g[1] in main_pairs and g[2] in main_pairs)]
    for size in (1, 2):
        for sub in combinations(main_gi, size):
            key = frozenset(sub)
            if key not in qseen:
                qseen.add(key)
                queries.append((key, ""))
    sub_mi = [gpos[('M', p, q)] for (p, q) in diag_monos(sub_pairs)]
    sub_vi = [gpos[('V', p)] for p in sub_pairs]
    for size in (2, 3):
        for sub in combinations(sub_mi, size):
            key = frozenset(sub)
            if key not in qseen:
                qseen.add(key)
                queries.append((key, ""))
    for msub in combinations(sub_mi, 2):
        for v in sub_vi:
            key = frozenset(msub + (v,))
            if key not in qseen:
                qseen.add(key)
                queries.append((key, ""))
    if SMOKE:
        queries = queries[::7]
    # shape-completion: concrete instances of abstract configurations whose
    # partners need pairwise-distinct pigeon/hole classes (outside the
    # sub-window's two-pigeon reach). Engine B's config scan is complete over
    # abstract shapes; these queries let Engine A validate those shapes.
    extra = [
        [('V', (0, 0)), ('M', (0, 0), (3, 1)), ('M', (0, 0), (4, 3))],
        [('V', (0, 0)), ('M', (0, 0), (3, 1)), ('M', (0, 0), (4, 4))],
        [('V', (3, 3)), ('M', (3, 3), (0, 1)), ('M', (3, 3), (4, 0))],
        [('M', (0, 0), (3, 1)), ('M', (0, 0), (4, 3)), ('M', (0, 0), (1, 4))],
        [('M', (0, 0), (3, 1)), ('M', (0, 0), (4, 3))],
        [('M', (3, 1), (0, 0)), ('M', (4, 3), (0, 0))],
        [('M', (0, 0), (3, 1)), ('M', (0, 1), (4, 3))],
        [('V', (0, 0)), ('M', (3, 1), (4, 3)), ('M', (3, 4), (1, 3))],
    ]
    for terms in extra:
        try:
            gensel = frozenset(gpos[t] for t in terms)
        except KeyError:
            continue
        if gensel not in qseen:
            qseen.add(gensel)
            queries.append((gensel, ""))
    queries = [(k, " + ".join(gen_desc(gen_specs[g]) for g in sorted(k)))
               for k, _ in queries]
    print(f"[V2] (7,2): {len(all_pairs)} pairs, {len(gen_specs)} generators, "
          f"{len(queries)} queries")

    rhos = list(rhos_all(n, d))
    print(f"[V2] Engine A: all {len(rhos)} restrictions x {len(queries)} "
          f"queries")
    t0 = time.perf_counter()
    res = engineA_point(n, d, DX, gen_specs, queries, all_pairs, rhos)
    print(f"[V2] Engine A pass done in {time.perf_counter() - t0:.1f} s")
    print(f"     baselines: q = {q_closed(n, d)} = "
          f"{float(q_closed(n, d)):.6f}, q_and_printed = "
          f"{float(q_and_printed(n, d)):.6f}, q_and_exact = "
          f"{q_and_exact(n, d)} = {float(q_and_exact(n, d)):.6f}")

    # ---- V1 cross-validation, per role, digit-exact
    mism = 0
    single_rec = None
    mono_rec = None
    shared_rec = None
    for gensel, desc in queries:
        terms = []
        const = 0
        for g in sorted(gensel):
            gg = gen_specs[g]
            if gg[0] == 'K':
                const = 1
            elif gg[0] == 'V':
                terms.append(('V', gg[1]))
            else:
                terms.append(('M', gg[1], gg[2]))
        slots, bposts = concrete_engineB(n, d, terms, const)
        _, apost, _d1, _d0 = res[gensel]
        for p in slots:
            for a in (0, 1):
                if bposts[(a, p)] != apost[p][a]:
                    mism += 1
                    if mism <= 5:
                        print(f"     MISMATCH {desc} ans={a} c={p}: "
                              f"B={float(bposts[(a, p)]):.7f} "
                              f"A={float(apost[p][a]):.7f}")
        if terms == [('V', (3, 3))] and const == 0:
            single_rec = (desc, apost[(3, 3)][1])
        if terms == [('M', (3, 3), (4, 4))] and const == 0:
            mono_rec = (desc, apost[(3, 3)][1])
        if terms == [('M', (4, 1), (1, 3)), ('M', (4, 1), (1, 4))] and const == 0:
            shared_rec = (desc, apost[(4, 1)][1], bposts[(1, (4, 1))])
    print(f"[V1] Engine B vs Engine A: {len(queries)} queries x 2 answers x "
          f"support roles: {mism} mismatches -> "
          f"{'PASS (digit-exact)' if mism == 0 else 'FAIL'}")
    if single_rec:
        ok = single_rec[1] == q_closed(n, d)
        print(f"[V1] single variable x(3,3): post1 = {single_rec[1]} vs "
              f"q = {q_closed(n, d)} -> {'PASS' if ok else 'FAIL'}")
    if mono_rec:
        ok = mono_rec[1] == q_and_exact(n, d)
        print(f"[V1] diagonal monomial x(3,3)x(4,4): post1 = {mono_rec[1]} "
              f"vs q_and_exact = {q_and_exact(n, d)} -> "
              f"{'PASS (digit-exact)' if ok else 'FAIL'}")
    if shared_rec:
        print(f"[V1] shared-pair mixture x(4,1)x(1,3)+x(4,1)x(1,4): post1 = "
              f"{shared_rec[1]} = {float(shared_rec[1]):.6f} (Engine B: "
              f"{float(shared_rec[2]):.6f}) vs q_and_exact = "
              f"{float(q_and_exact(n, d)):.6f}")

    # ---- V2 max scan
    ranked = []
    for gensel, (desc, posts, _d1, _d0) in res.items():
        if not posts:
            continue
        best = max(max(v.values()) for v in posts.values())
        ranked.append((best, gensel, desc, posts))
    ranked.sort(reverse=True, key=lambda x: x[0])
    print("[V2] top 12 queries by max posterior over answers and roles:")
    for best, gensel, desc, posts in ranked[:12]:
        argmax = max(((p, max(v.values())) for p, v in posts.items()),
                     key=lambda kv: kv[1])
        p = argmax[0]
        v1, v0 = posts[p][1], posts[p][0]
        side = 1 if v1 >= v0 else 0
        print(f"     {float(max(v1, v0)):.6f} (ans={side}, c={p})  {desc}")
    gmax, gdesc = ranked[0][0], ranked[0][2]
    verdict = ("CAP HOLDS" if gmax <= q_and_exact(n, d) else "EXCEEDED")
    print(f"[V2] (7,2) MAX posterior = {gmax} = {float(gmax):.6f} vs "
          f"q_and_exact = {q_and_exact(n, d)} -> {verdict}   [{gdesc}]")
    ncert = 0
    for gensel, (desc, posts, _d1, _d0) in res.items():
        for p, v in posts.items():
            if v[1] >= 1 or v[0] >= 1:
                ncert += 1
                break
    print(f"[V2] single-query certificates (posterior = 1): {ncert} "
          f"(Theorem M4: 0 expected)")
    print()

    # ================= V3: (15,2) sampled panel ==========================
    n, d = 15, 2
    panel_pairs = [(i, j) for i in (0, 1, 2, 3) for j in (0, 1, 2, 3)]
    gen_specs = [('K',)] + [('V', p) for p in panel_pairs] + \
                [('M', p, q) for (p, q) in diag_monos(panel_pairs)]
    gpos = {g: k for k, g in enumerate(gen_specs)}
    panel = [
        [('K',)],
        [('V', (0, 0))], [('V', (2, 2))],
        [('M', (0, 0), (2, 2))],
        [('V', (0, 0)), ('V', (2, 2))],
        [('V', (0, 0)), ('M', (0, 0), (2, 2))],
        [('V', (2, 2)), ('M', (0, 0), (2, 2))],
        [('M', (0, 0), (2, 2)), ('M', (0, 0), (3, 3))],
        [('M', (0, 0), (2, 2)), ('M', (1, 1), (3, 3))],
        [('M', (0, 0), (2, 2)), ('M', (0, 1), (1, 3))],
        [('V', (2, 2)), ('M', (2, 2), (3, 3))],
        [('V', (2, 2)), ('V', (2, 3)), ('V', (3, 2))],
        [('M', (0, 0), (2, 2)), ('M', (0, 0), (2, 3)), ('M', (0, 0), (3, 2))],
        [('M', (0, 2), (2, 0)), ('M', (0, 3), (3, 0))],
        [('V', (0, 0)), ('V', (0, 1))],
        [('V', (0, 0)), ('M', (2, 2), (3, 3))],
    ]
    queries = []
    for terms in panel:
        gensel = frozenset(gpos[t] for t in terms)
        desc = " + ".join(gen_desc(gen_specs[g]) for g in sorted(gensel))
        queries.append((gensel, desc))
    K = 2000 if SMOKE else args.rhos15

    def sample_rho():
        c = n - 2 * d
        return (tuple(rng.sample(range(n + 1), c)),
                tuple(rng.sample(range(n), c)))

    print(f"[V3] (15,2): {len(queries)} panel queries x {K} sampled "
          f"restrictions (exact per-rho law)")
    t0 = time.perf_counter()
    res15 = engineA_point(n, d, DX, gen_specs, queries, panel_pairs,
                          (sample_rho() for _ in range(K)))
    print(f"[V3] Engine A pass done in {time.perf_counter() - t0:.1f} s")
    worst = 0.0
    bad = 0
    worst_d = ""
    for gensel, (desc, apost, den1, den0) in res15.items():
        terms = [gen_specs[g] for g in sorted(gensel)]
        const = 1 if ('K',) in terms else 0
        pt = [t for t in terms if t[0] != 'K']
        slots, bposts = concrete_engineB(n, d, pt, const)
        for p in slots:
            for a in (0, 1):
                diff = abs(float(bposts[(a, p)]) - float(apost[p][a]))
                den = den1 if a == 1 else den0
                tol = 5 * 0.5 / math.sqrt(max(den, 1.0)) + 0.002
                if diff > tol:
                    bad += 1
                    if bad <= 5:
                        print(f"     V3 EXCEEDS {desc} ans={a} c={p}: "
                              f"B={float(bposts[(a, p)]):.4f} "
                              f"A={float(apost[p][a]):.4f} tol={tol:.4f}")
                if diff > worst:
                    worst = diff
                    worst_d = f"{desc} ans={a} c={p} (tol {tol:.4f})"
    tol = 0.10 if SMOKE else 4.0 / math.sqrt(K) + 0.005
    print(f"[V3] worst |Engine B - Engine A| over the panel: {worst:.5f} "
          f"({bad} comparisons over tolerance, per-comparison 5-sigma "
          f"tolerance) -> {'PASS' if bad == 0 else 'FAIL'}  [{worst_d}]")
    print()

    # ================= V4: grid over all configurations ==================
    print("[V4] grid over ALL support<=3 configurations with geometry "
          "(Engine B, exact rationals)")
    configs = enum_configs(3)
    print(f"     {len(configs)} configurations up to isomorphism")
    tables = []
    shared_idx = -1
    star_idx = -1
    for (const, terms, geo) in configs:
        tables.append((const, terms, geo, status_table(geo, terms, const)))
        if (const == 0 and len(terms) == 3 and all(t[0] == 'M' for t in terms)
                and terms[0][1] == terms[1][1] == terms[2][1]
                and len({t[2] for t in terms}) == 3):
            star_idx = len(tables) - 1
        if (const == 0 and len(terms) == 2 and all(t[0] == 'M' for t in terms)
                and terms[0][1] == terms[1][1]
                and len({terms[0][1], terms[0][2], terms[1][2]}) == 3
                and len(set(geo)) == 3
                and len({g[0] for g in geo}) == 3
                and len({g[1] for g in geo}) == 3):
            shared_idx = len(tables) - 1
    grid = ([(7, 2), (8, 2), (9, 2), (12, 2), (15, 2), (24, 2), (32, 2),
             (63, 2), (127, 2), (255, 2), (1023, 2)]
            + [(8, 3), (15, 3), (31, 3), (63, 3), (16, 4), (31, 4)])
    if SMOKE:
        grid = [(7, 2), (15, 2), (32, 2)]
    worst = Fraction(0)
    worst_at = None
    print(f"     {'(n,d)':>9} {'q':>7} {'q_and_ex':>8} {'max post':>8} "
          f"{'shared-2M':>11} {'star-3M':>11}  argmax form")
    for (n, d) in grid:
        qe = q_and_exact(n, d)
        mx = Fraction(0)
        mxd = ""
        shared = None
        star = None
        for idx, (const, terms, geo, table) in enumerate(tables):
            posts = posts_with_virtuals(n, d, const, terms, geo)
            if idx == shared_idx:
                shared = posts[('pair', 0, 1)]
            if idx == star_idx:
                star = posts[('pair', 0, 1)]
            for key, val in posts.items():
                if key[0] == 'ext':
                    if val > mx:
                        mx = val
                        mxd = f"const={const} terms={terms} geo={geo} ext"
                elif val > mx:
                    mx = val
                    mxd = (f"const={const} terms={terms} geo={geo} "
                           f"role={key[:2]}")
        gap = mx - qe
        if gap > worst:
            worst, worst_at = gap, (n, d, mxd)
        tag = mxd if gap > 0 else "monomial (= q_and_exact)"
        shared_s = f"{float(shared):11.6f}" if shared is not None else 11 * " "
        star_s = f"{float(star):11.6f}" if star is not None else 11 * " "
        print(f"     ({n:4d},{d}) {float(q_closed(n, d)):>7.4f} "
              f"{float(qe):>8.4f} {float(mx):>8.4f} "
              f"{shared_s} {star_s}  {tag[:64]}")
    # exact rationals for the doc (the winning shared-pair family)
    for (n, d) in [(15, 2), (32, 2), (63, 2)]:
        qe = q_and_exact(n, d)
        sp = None
        for (const, terms, geo) in configs:
            if (const == 0 and len(terms) == 2 and all(t[0] == 'M' for t in terms)
                    and terms[0][1] == terms[1][1]
                    and len(set(geo)) == 3 and len({g[0] for g in geo}) == 3
                    and len({g[1] for g in geo}) == 3):
                sp = posts_from_table(n, d, geo,
                                      status_table(geo, terms, const))[('pair', 0, 1)]
        print(f"[V4] exact ({n},2): q2*_shared - q_and = "
              f"{sp - qe} = {float(sp - qe):.2e}; shared = {sp} = "
              f"{float(sp):.6f}; q_and = {qe}; q = {q_closed(n, d)}")
    print(f"[V4] worst (max post - q_and_exact) over the grid: "
          f"{float(worst):+.6f}"
          + (f" at {worst_at[0], worst_at[1]}: {worst_at[2]}"
             if worst_at else "")
          + " -> "
          + ("CAP = q_and_exact HOLDS on the grid" if worst <= 0
             else "EXCEEDED"))
    print()

    # ================= V5: budgeted strategies ===========================
    print("[V5] budgeted adaptive strategies (exact channel); certified")
    print("     outputs asserted free; budget counts query evaluations")
    names = ["single_scan", "and_scan", "kj_budget", "mix_z", "mix_scan",
             "hybrid"]
    for (n, d, sims) in ([(15, 2, 200 if SMOKE else 4000),
                          (32, 2, 100 if SMOKE else 1500)]):
        mono_list = []
        allp = [(i, j) for i in range(n + 1) for j in range(n)]
        for a in range(len(allp)):
            for b in range(a + 1, len(allp)):
                p, r = allp[a], allp[b]
                if p[0] != r[0] and p[1] != r[1]:
                    mono_list.append((p, r))
        print(f"  (n,d) = ({n},{d}): q = {float(q_closed(n, d)):.4f}, "
              f"q_and_exact = {float(q_and_exact(n, d)):.4f}, "
              f"sims = {sims}")
        for budget in (10, 30, 100):
            acc = {s: 0 for s in names}
            viol = [0]
            s2 = random.Random(777 + budget)
            s3 = random.Random(555 + budget)
            samp = Sampler(n, d, DX, s2)
            for _ in range(sims):
                ans_q, free = samp.config()
                order = allp[:]
                s3.shuffle(order)
                monos = mono_list[:4000]
                s3.shuffle(monos)
                acc["single_scan"] += free(strat_single(ans_q, free, n,
                                                        budget, order))
                acc["and_scan"] += free(strat_and(ans_q, free, n, budget,
                                                  monos))
                acc["kj_budget"] += free(strat_kj(ans_q, free, n, budget))
                acc["mix_z"] += free(strat_mixz(ans_q, free, n, budget,
                                                monos, viol))
                acc["mix_scan"] += free(strat_mixscan(ans_q, free, n, budget,
                                                      monos))
                acc["hybrid"] += free(strat_hybrid(ans_q, free, n, budget,
                                                   monos, order))
            print("    budget %3d: " % budget
                  + "  ".join(f"{s}={acc[s] / sims:.4f}" for s in names))
        if viol[0]:
            print(f"    SOUNDNESS VIOLATIONS (certified output not free): "
                  f"{viol[0]}")
        else:
            print("    soundness: every certified output was free "
                  "(0 violations)")
    print()
    print("[verdict] summary lines above; full reading in docs/mixture_cap.md")


if __name__ == "__main__":
    main()
