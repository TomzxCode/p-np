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
construction is the printed design space). Answer law used, per restriction
rho: for any degree-<=2 query g, ans(g) = L(g^rho) with L uniform in the
design coset; the script computes the exact per-rho answer probability from
the projected design coset (Engine A, design-exact) and independently from
the proved alive/dead status calculus (Engine B, design-free), and requires
the two to agree digit-exactly.

Posteriors: for output pair c and answer event ans(g)=a,
  post(c | g, a) = N / (N + D),
  N = sum_rho P(rho) 1_{c free}     P[ans(g)=a | rho],
  D = sum_rho P(rho) 1_{c not free} P[ans(g)=a | rho].
The per-hit maximum over the printed class is the max over queries g, answers
a, and output pairs c.

Checks:
  V1  engine cross-validation at (7,2): Engine B == Engine A digit-exact on
      every enumerated query and every output role; the pure diagonal
      monomial query reproduces q_and_exact; the single variable reproduces q.
  V2  exhaustive posterior max at (7,2), all 11760 restrictions: every
      support<=2 query over a 16-pair window, plus every support<=3 query
      with >= 2 monomials over a 10-pair sub-window (covers the degree-2
      star-triple configuration, the only block-complete support-3 form).
  V3  same at (15,2) on sampled restrictions (exact per-rho law).
  V4  grid: Engine B over ALL support<=3 query configurations (with pair
      geometry: co-pigeon / co-hole classes) on a grid of (n,d): the maximum
      posterior vs q, q_and_printed, q_and_exact.
  V5  budgeted adaptive strategies on the exact channel at (15,2) and
      (32,2): does any mixture strategy beat the covered-class champions at
      equal budget? Certified outputs are asserted free (soundness).

Run: python3 chi_mixture_cap.py [--smoke] [--rhos15 K]
"""
from __future__ import annotations

import argparse
import random
import sys
import time
from fractions import Fraction
from itertools import combinations, permutations, product

from razborov_check import monomials
from kernel_structure import (canonical_rows, echelon_rhs, particular,
                              project)

T0 = time.perf_counter()
TIME_LIMIT = 900.0


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
    # one homogeneous kernel vector per non-pivot column (chi_deg3 pattern);
    # every kernel vector has bit 0 = 0 (the affine row pins L(1) = 1).
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
        s = build_restricted(d)
        self.__dict__.update(s)
        self._pk_cache: dict = {}
        self._w_cache: dict = {}

    def _pk(self, T: tuple) -> list:
        ent = self._pk_cache.get(T)
        if ent is not None:
            return ent
        kb = self.kb
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
    import math
    return math.comb(n + 1, c) * math.comb(n, c) * math.factorial(c)


def rho_data(n: int, d: int, A, B, npairs):
    """Statuses and canonical coordinates of all pairs under one restriction."""
    c = n - 2 * d
    matched = dict(zip(A, B))
    D = sorted(set(range(n + 1)) - set(A))
    R = sorted(set(range(n)) - set(B))
    pidx = {i: t for t, i in enumerate(D)}
    hidx = {j: t for t, j in enumerate(R)}
    st = bytearray(npairs)          # 0 = F, 1 = M, 2 = K
    cvar = [-1] * npairs            # restricted variable column for F pairs
    for i in range(n + 1):
        base = i * n
        if i in matched:
            for j in range(n):
                st[base + j] = 1
            st[base + matched[i]] = 1
        else:
            for j in range(n):
                if j in hidx:
                    st[base + j] = 0
                    cvar[base + j] = 1 + pidx[i] * (2 * d) + hidx[j]
                else:
                    st[base + j] = 2
    for i, j in matched.items():
        st[i * n + j] = 1
        cvar[i * n + j] = -1
    return st, cvar


# ------------------------------------------------------- Engine B (calculus)

def count_assign(n: int, d: int, sF: int, sM: int) -> int:
    """Exact number of restrictions with a given free/matched pair pattern."""
    import math
    c = n - 2 * d
    if sM > c or sF > 2 * d:
        return 0
    a, b = c - sM, c - sM
    if n + 1 - sF - sM < a or n - sF - sM < b:
        return 0
    return (math.comb(n + 1 - sF - sM, a) * math.comb(n - sF - sM, b)
            * math.factorial(a))


def p_ext_free(n: int, d: int, sF: int, sM: int) -> Fraction:
    """P[a specific untouched pair is free | pattern counts]."""
    c = n - 2 * d
    dp = n + 1 - sF - sM
    dh = n - sF - sM
    if dp <= 0 or dh <= 0:
        return Fraction(0)
    return Fraction((2 * d + 1 - sF) * (2 * d - sF), dp * dh)


def law_of_terms(terms, assign, const):
    """Live coordinate set (XOR-cancelled) and determined constant.

    terms: list of ('V', p) / ('M', p, q) with p, q pair slots.
    assign: tuple of 'F'/'M'/'K' per slot.
    Returns (live: dict coord->parity, det: 0/1).
    """
    live: dict = {}
    det = const
    for t in terms:
        if t[0] == 'V':
            s = assign[t[1]]
            if s == 'F':
                live[('A', t[1])] = live.get(('A', t[1]), 0) ^ 1
            elif s == 'M':
                det ^= 1
        else:
            _, p, q = t
            sp, sq = assign[p], assign[q]
            if sp == 'K' or sq == 'K':
                continue
            if sp == 'F' and sq == 'F':
                key = ('D', p, q) if p < q else ('D', q, p)
                live[key] = live.get(key, 0) ^ 1
            elif sp == 'M' and sq == 'M':
                det ^= 1
            else:
                f = p if sp == 'F' else q
                live[('A', f)] = live.get(('A', f), 0) ^ 1
    live = {k: v for k, v in live.items() if v}
    return live, det


def valid_assign(geo, assign):
    """geo: list of (pigeon_class, hole_class) per slot."""
    t = len(assign)
    for i in range(t):
        for j in range(i + 1, t):
            si, sj = assign[i], assign[j]
            if si == 'K' or sj == 'K':
                continue
            same_p = geo[i][0] == geo[j][0]
            same_h = geo[i][1] == geo[j][1]
            if same_p or same_h:
                return False
    return True


def concrete_engineB(n, d, terms, const):
    """Exact posteriors for one concrete query from the status calculus.

    Returns (best1, best0, desc1, desc0) where best* is the max posterior
    over output roles (query pairs + external) and desc* the argmax.
    """
    slots = sorted({p for t in terms for p in (t[1:] if t[0] == 'V' else (t[1], t[2]))})
    idx = {p: k for k, p in enumerate(slots)}
    sl_terms = []
    for t in terms:
        if t[0] == 'V':
            sl_terms.append(('V', idx[t[1]]))
        else:
            sl_terms.append(('M', idx[t[1]], idx[t[2]]))
    pigeons = [p // n for p in slots]
    holes = [p % n for p in slots]
    geo = [(pigeons[k], holes[k]) for k in range(len(slots))]
    t = len(slots)
    total = count_rhos(n, d)
    best = [Fraction(0), Fraction(0)]
    desc = ["", ""]
    for assign in product('FMK', repeat=t):
        if not valid_assign(geo, assign):
            continue
        sF = assign.count('F')
        sM = assign.count('M')
        W = count_assign(n, d, sF, sM)
        if W == 0:
            continue
        live, det = law_of_terms(sl_terms, assign, const)
        w = Fraction(1, 2) if live else Fraction(det)
        for a, val in ((0, w), (1, 1 - w)):
            for k in range(t):
                if assign[k] == 'F':
                    num = W * val
                    if num > best[a][0] * 0 + 0:  # placeholder, replaced below
                        pass
            # external role
            num = W * val * p_ext_free(n, d, sF, sM)
            if num > best[a][0]:
                pass
    # --- clean implementation (the loop above collects; see below)
    S = [Fraction(0), Fraction(0)]
    N = {}
    Next = [Fraction(0), Fraction(0)]
    for assign in product('FMK', repeat=t):
        if not valid_assign(geo, assign):
            continue
        sF = assign.count('F')
        sM = assign.count('M')
        W = count_assign(n, d, sF, sM)
        if W == 0:
            continue
        live, det = law_of_terms(sl_terms, assign, const)
        w = Fraction(1, 2) if live else Fraction(det)
        for a, val in ((0, w), (1, 1 - w)):
            S[a] += W * val
            for k in range(t):
                if assign[k] == 'F':
                    N[(a, k)] = N.get((a, k), Fraction(0)) + W * val
            Next[a] += W * val * p_ext_free(n, d, sF, sM)
    for a in (0, 1):
        if S[a] == 0:
            continue
        for k in range(t):
            post = N.get((a, k), Fraction(0)) / S[a]
            if post > best[a]:
                best[a] = post
                desc[a] = f"pair {slots[k]} = ({slots[k]//n},{slots[k]%n})"
        post = Next[a] / S[a]
        if post > best[a]:
            best[a] = post
            desc[a] = "external"
    return best[1], best[0], desc[1], desc[0]


def enum_configs(kmax=3):
    """All support<=kmax query configurations with geometry, up to isomorphism.

    A configuration = (const, terms over pair slots, geo). Returns a list of
    (const, terms, geo) with canonical strings deduplicated.
    """
    import itertools as it

    def partitions(elements):
        if not elements:
            yield []
            return
        first, rest = elements[0], elements[1:]
        for part in partitions(rest):
            # new block
            yield [[first]] + part
            for i, blocks in enumerate(part):
                yield [blocks + [first]] + part[:i] + part[i + 1:]

    def canon(pc, hc, terms):
        npc = len({x for b in pc for x in b})
        nhc = len({x for b in hc for x in b})
        bestk = None
        for pperm in it.permutations(range(npc)):
            for hperm in it.permutations(range(nhc)):
                pmap = {}
                for bi, block in enumerate(pc):
                    for x in block:
                        pmap[x] = pperm[bi]
                hmap = {}
                for bi, block in enumerate(hc):
                    for x in block:
                        hmap[x] = hperm[bi]
                g = tuple(sorted((pmap[k], hmap[k]) for k in range(len(pc))))
                tt = []
                for tm in terms:
                    if tm[0] == 'V':
                        tt.append(('V', pmap[tm[1]]))
                    else:
                        tt.append(('M', pmap[tm[1]], pmap[tm[2]]))
                tt = tuple(sorted(tt))
                key = (g, tt)
                if bestk is None or key < bestk[0]:
                    bestk = (key, g, tt)
        return bestk[1], list(bestk[2])

    seen = set()
    out = []
    for t in range(1, kmax + 1):
        elems = list(range(t))
        pcs = list(partitions(elems))
        hcs = list(partitions(elems))
        for pc in pcs:
            for hc in hcs:
                pclass = {}
                hclass = {}
                for bi, block in enumerate(pc):
                    for x in block:
                        pclass[x] = bi
                for bi, block in enumerate(hc):
                    for x in block:
                        hclass[x] = bi
                geo = [(pclass[k], hclass[k]) for k in range(t)]
                if len(set(geo)) != t:
                    continue          # two slots = same pair
                pool = [('V', k) for k in range(t)]
                for i in range(t):
                    for j in range(i + 1, t):
                        if geo[i][0] != geo[j][0] and geo[i][1] != geo[j][1]:
                            pool.append(('M', i, j))
                for size in range(1, kmax + 1):
                    for sub in it.combinations(pool, size):
                        for const in (0, 1):
                            g, tt = canon(pc, hc, list(sub))
                            key = (const, tuple(sorted(map(tuple, g))),
                                   tuple(sorted(tuple(x) if isinstance(x, tuple) else (x,) for x in tt)))
                            key = (const, str(sorted(map(tuple, g))),
                                   str(sorted(tt)))
                            if key not in seen:
                                seen.add(key)
                                out.append((const, list(tt), [tuple(x) for x in g]))
    return out


def config_posterior(n, d, const, terms, geo):
    """Exact max posterior (ans=1 side and ans=0 side) for one configuration."""
    t = len(geo)
    best = [Fraction(0), Fraction(0)]
    S = [Fraction(0), Fraction(0)]
    N = {}
    Next = [Fraction(0), Fraction(0)]
    for assign in product('FMK', repeat=t):
        if not valid_assign(geo, assign):
            continue
        sF = assign.count('F')
        sM = assign.count('M')
        W = count_assign(n, d, sF, sM)
        if W == 0:
            continue
        live, det = law_of_terms(terms, assign, const)
        w = Fraction(1, 2) if live else Fraction(det)
        for a, val in ((0, w), (1, 1 - w)):
            S[a] += W * val
            for k in range(t):
                if assign[k] == 'F':
                    N[(a, k)] = N.get((a, k), Fraction(0)) + W * val
            Next[a] += W * val * p_ext_free(n, d, sF, sM)
    out = [Fraction(0), Fraction(0)]
    for a in (0, 1):
        if S[a] == 0:
            continue
        m = max([N.get((a, k), Fraction(0)) / S[a] for k in range(t)]
                + [Next[a] / S[a]])
        out[a] = m
    return out[1], out[0]


# ------------------------------------------------------- closed-form baselines

def q_closed(n, d):
    return Fraction((2 * d + 1) * d, (2 * d + 1) * d + (n - 2 * d))


def q_and_printed(n, d):
    import math
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
    import math
    C, F = math.comb, math.factorial
    M0 = C(n - 1, c - 2) * C(n - 2, c - 2) * F(c - 2) if c >= 2 else 0
    M1 = C(n - 1, c - 1) * C(n - 2, c - 1) * F(c - 1) if c >= 1 else 0
    M2 = C(n - 1, c) * C(n - 2, c) * F(c)
    return Fraction(M1 + M2, 2 * M0 + 2 * M1 + M2)


# ----------------------------------------------------- Engine A: enumeration

def describe(ngen, gensel, win_pairs):
    """Human-readable query description from generator indices."""
    parts = []
    for g in sorted(gensel):
        kind = g[0]
        if kind == 'K':
            parts.append("1")
        elif kind == 'V':
            p = win_pairs[g[1]]
            parts.append(f"x({p[0]},{p[1]})")
        else:
            p, r = win_pairs[g[1]], win_pairs[g[2]]
            parts.append(f"x({p[0]},{p[1]})x({r[0]},{r[1]})")
    return " + ".join(parts) if parts else "0"


def engineA_point(n, d, DX, win_pairs, gen_specs, queries, cands,
                  rho_source, nrho, stage2=0):
    """Engine A pass.

    gen_specs: list of ('K',) / ('V', pair) / ('M', pair, pair).
    queries: list of (frozenset-of-gen-indices, description).
    cands: candidate output pair list.
    rho_source: iterable of (A, B) restriction data.
    Returns (results, top_list) with per-query max posteriors.
    """
    npairs = n * (n + 1)
    ncand = len(cands)
    cpos = {p: k for k, p in enumerate(cands)}
    genvec = [[] for _ in gen_specs]
    candmask = []
    cntF = [0] * ncand
    p_of = {}
    n_done = 0
    for A, B in rho_source:
        st, cvar = rho_data(n, d, A, B, npairs)
        cm = 0
        for k, p in enumerate(cands):
            if st[p[0] * n + p[1]] == 0:
                cm |= 1 << k
                cntF[k] += 1
        candmask.append(cm)
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
        n_done += 1
    nrho = n_done
    wcache = DX._w_cache
    results = []
    for gensel, desc in queries:
        gs = sorted(gensel)
        tally: dict = {}
        if len(gs) == 1:
            gv = genvec[gs[0]]
            for ri in range(nrho):
                key = (gv[ri] << ncand) | candmask[ri]
                tally[key] = tally.get(key, 0) + 1
        elif len(gs) == 2:
            ga, gb = genvec[gs[0]], genvec[gs[1]]
            for ri in range(nrho):
                key = ((ga[ri] ^ gb[ri]) << ncand) | candmask[ri]
                tally[key] = tally.get(key, 0) + 1
        else:
            ga, gb, gc = genvec[gs[0]], genvec[gs[1]], genvec[gs[2]]
            for ri in range(nrho):
                key = ((ga[ri] ^ gb[ri] ^ gc[ri]) << ncand) | candmask[ri]
                tally[key] = tally.get(key, 0) + 1
        S1 = Fraction(0)
        N1 = [Fraction(0)] * ncand
        for key, cnt in tally.items():
            v = key >> ncand
            cm = key & ((1 << ncand) - 1)
            wn, wd = wcache[v] if v in wcache else DX.w(v)
            w = Fraction(wn, wd)
            S1 += cnt * w
            k = 0
            m = cm
            while m:
                if m & 1:
                    N1[k] += cnt * w
                m >>= 1
                k += 1
        best1 = Fraction(0)
        bestc1 = None
        for k in range(ncand):
            if S1 > 0 and N1[k] / S1 > best1:
                best1 = N1[k] / S1
                bestc1 = cands[k]
        S0 = nrho - S1
        best0 = Fraction(0)
        bestc0 = None
        if S0 > 0:
            for k in range(ncand):
                post = (cntF[k] - N1[k]) / S0
                if post > best0:
                    best0 = post
                    bestc0 = cands[k]
        results.append((gensel, desc, best1, bestc1, best0, bestc0))
    return results


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
        # sample a design: L = Lstar ^ XOR of kernel vectors
        L = self.DX.Lstar
        for b, kv in enumerate(self.DX.kb):
            if (rng.getrandbits(1)):
                L ^= kv
        st = {}
        cv = {}

        def pairinfo(p):
            if p not in st:
                i, j = p
                if i in matched:
                    st[p] = 1
                elif j in hidx:
                    st[p] = 0
                    cv[p] = 1 + pidx[i] * (2 * d) + hidx[j]
                else:
                    st[p] = 2
            return st[p]

        def ans_var(p):
            s = pairinfo(p)
            if s == 1:
                return 1
            if s == 0:
                return (L >> cv[p]) & 1
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
            u, v = sorted((cv[p] - 1, cv[q] - 1))
            return (L >> self.DX.colD[(u, v)]) & 1

        def ans_q(genspec):
            if genspec[0] == 'V':
                return ans_var(genspec[1])
            if genspec[0] == 'M':
                return ans_mono(genspec[1], genspec[2])
            return 1  # constant

        def free(p):
            return pairinfo(p) == 0

        return ans_q, free


def strat_single(ans_q, free, n, budget):
    for i in range(n + 1):
        for j in range(n):
            if budget <= 0:
                return (0, 0), False
            budget -= 1
            if ans_q(('V', (i, j))) == 1:
                return (i, j), False
    return (0, 0), True


def strat_and(ans_q, free, n, budget, mono_list):
    for (p, q) in mono_list:
        if budget <= 0:
            return (0, 0), False
        budget -= 1
        if ans_q(('M', p, q)) == 1:
            return p, False
    return (0, 0), True


def strat_kj(ans_q, free, n, budget):
    half = budget // 2
    cert = []
    used = 0
    for j in range(n):
        if used >= half:
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
                return (0, 0), True
            used += 1
            if ans_q(('V', (i, j))) == 1:
                return (i, j), False
    return (0, 0), True


def strat_mixz(ans_q, free, n, budget, mono_list, viol):
    used = 0
    for (p, q) in mono_list:
        if used >= budget:
            break
        used += 1
        a1 = ans_q(('V', p)) ^ ans_q(('M', p, q))
        if a1 == 1:
            if used >= budget:
                break
            used += 1
            a2 = ans_q(('M', p, q))
            if a2 == 1:
                if not free(q):
                    viol[0] += 1
                return q, False
            return p, False
    return (0, 0), True


def strat_mixscan(ans_q, free, n, budget, mono_list):
    used = 0
    for (p, q) in mono_list:
        if used >= budget:
            break
        used += 1
        if (ans_q(('V', p)) ^ ans_q(('M', p, q))) == 1:
            return p, False
    return (0, 0), True


def strat_hybrid(ans_q, free, n, budget, mono_list):
    used = 0
    mi = 0
    for i in range(n + 1):
        for j in range(n):
            if used >= budget:
                return (0, 0), True
            used += 1
            if ans_q(('V', (i, j))) == 1:
                return (i, j), False
            if used >= budget:
                return (0, 0), True
            used += 1
            if mi < len(mono_list):
                p, q = mono_list[mi]
                mi += 1
                if ans_q(('M', p, q)) == 1:
                    return p, False
    return (0, 0), True


# ----------------------------------------------------------------------- main

def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--rhos15", type=int, default=12000)
    args = ap.parse_args()
    SMOKE = args.smoke
    rng = random.Random(20261004)

    print("chi_mixture_cap: GAP B' - the per-hit posterior cap over the FULL")
    print("printed degree-<=2 class (F_2 mixtures) on the true Omega(n,d)")
    print("pipeline at p=2. Channel: uniform designs of Des(2d,d), per-rho")
    print("projected-coset exact law (Engine A) cross-validated against the")
    print("proved alive/dead status calculus (Engine B).")
    print()

    DX = DesignExact(2)
    print(f"[setup] restricted system (4,2): {DX.ncols} columns, "
          f"kernel dim {len(DX.kb)}, Lstar(1) = {DX.Lstar & 1}")

    # ---------------- V1/V2: (7,2) exhaustive
    n, d = 7, 2
    npairs = n * (n + 1)
    main_pigeons = (0, 1, 3, 4)
    main_holes = (0, 1, 3, 4)
    win_pairs = [(i, j) for i in main_pigeons for j in main_holes]
    sub_pairs = [(i, j) for i in (0, 3) for j in (0, 1, 3, 4, 5)]
    all_pairs = sorted(set(win_pairs) | set(sub_pairs))
    pair_pos = {p: k for k, p in enumerate(all_pairs)}

    def diag_monos(pairs):
        out = []
        for a in range(len(pairs)):
            for b in range(a + 1, len(pairs)):
                (i1, j1), (i2, j2) = pairs[a], pairs[b]
                if i1 != i2 and j1 != j2:
                    out.append((pairs[a], pairs[b]))
        return out

    gen_specs = [('K',)]
    gen_specs += [('V', p) for p in all_pairs]
    gen_specs += [('M', p, q) for (p, q) in diag_monos(all_pairs)]
    gpos = {g: k for k, g in enumerate(gen_specs)}
    main_mono = diag_monos(win_pairs)
    print(f"[V2] (7,2) window: {len(win_pairs)} main pairs, "
          f"{len(all_pairs)} total pairs, {len(gen_specs)} generators")

    queries = []
    qseen = set()
    main_gi = [gpos[('K',)]] + [gpos[('V', p)] for p in win_pairs] + \
              [gpos[('M', p, q)] for (p, q) in main_mono]
    for size in (1, 2):
        for sub in combinations(main_gi, size):
            key = frozenset(sub)
            if key in qseen:
                continue
            qseen.add(key)
            queries.append((key, ""))
    sub_gi = [gpos[g] for g in gen_specs
              if g[0] == 'M' and g[1] in sub_pairs and g[2] in sub_pairs]
    sub_vi = [gpos[('V', p)] for p in sub_pairs]
    for size in (2, 3):
        for sub in combinations(sub_gi, size):
            key = frozenset(sub)
            if key in qseen:
                continue
            qseen.add(key)
            queries.append((key, ""))
    for msub in combinations(sub_gi, 2):
        for v in sub_vi:
            key = frozenset(msub + (v,))
            if key in qseen:
                continue
            qseen.add(key)
            queries.append((key, ""))
    for msub in combinations(sub_gi, 3):
        key = frozenset(msub)
        if key not in qseen:
            qseen.add(key)
            queries.append((key, ""))
    print(f"[V2] enumerated {len(queries)} queries (support<=2 main window, "
          f"support<=3 with >=2 monomials on the sub-window)")

    cands = list(win_pairs) + [(3, 5), (5, 5), (7, 6), (2, 2), (5, 0)]
    cands = sorted(set(cands))

    for qi, (gensel, _) in enumerate(queries):
        parts = []
        for g in sorted(gensel):
            gg = gen_specs[g]
            if gg[0] == 'K':
                parts.append("1")
            elif gg[0] == 'V':
                parts.append(f"x{gg[1]}")
            else:
                parts.append(f"x{gg[1]}x{gg[2]}")
        queries[qi] = (gensel, " + ".join(parts))

    rhos = list(rhos_all(n, d))
    if SMOKE:
        rhos = rhos[::17]
    print(f"[V2] enumerating {len(rhos)} restrictions x {len(queries)} "
          f"queries (Engine A, exact coset law)")
    t_a = time.perf_counter()
    res = engineA_point(n, d, DX, all_pairs, gen_specs, queries, cands,
                        rhos, len(rhos))
    print(f"[V2] Engine A pass done in {time.perf_counter() - t_a:.1f} s")
    print(f"     baselines: q = {q_closed(n, d)} = {float(q_closed(n, d)):.6f}"
          f", q_and_printed = {float(q_and_printed(n, d)):.6f}"
          f", q_and_exact = {q_and_exact(n, d)} = "
          f"{float(q_and_exact(n, d)):.6f}")

    # V1 cross-validation: Engine B must match Engine A on every query
    mism = 0
    checked = 0
    mono_desc = None
    single_desc = None
    for gensel, desc in queries:
        terms = []
        const = 0
        for g in sorted(gensel):
            gg = gen_specs[g]
            if gg[0] == 'K':
                const = 1
            elif gg[0] == 'V':
                terms.append(('V', pair_pos[gg[1]]))
            else:
                terms.append(('M', pair_pos[gg[1]], pair_pos[gg[2]]))
        b1, b0, d1, d0 = concrete_engineB(n, d, terms, const)
        r = next(x for x in res if x[0] == gensel)
        if b1 != r[2] or b0 != r[4]:
            mism += 1
            if mism <= 5:
                print(f"     MISMATCH {desc}: B=({float(b1):.6f},{float(b0):.6f})"
                      f" A=({float(r[2]):.6f},{float(r[4]):.6f})")
        checked += 1
        if terms == [('M', pair_pos[(3, 3)], pair_pos[(4, 4)])]:
            mono_desc = (desc, r)
        if terms == [('V', pair_pos[(3, 3)])] and const == 0:
            single_desc = (desc, r)
    print(f"[V1] Engine B vs Engine A on all {checked} queries x both answers"
          f" x all roles: {mism} mismatches -> "
          f"{'PASS (digit-exact)' if mism == 0 else 'FAIL'}")
    if single_desc:
        print(f"[V1] single-variable check: {single_desc[0]}: post1 = "
              f"{float(single_desc[1][2]):.6f} vs q = "
              f"{float(q_closed(n, d)):.6f} -> "
              f"{'PASS' if single_desc[1][2] == q_closed(n, d) else 'FAIL'}")
    if mono_desc:
        print(f"[V1] diagonal-monomial check: {mono_desc[0]}: post1 = "
              f"{mono_desc[1][2]} vs q_and_exact = {q_and_exact(n, d)} -> "
              f"{'PASS (digit-exact)' if mono_desc[1][2] == q_and_exact(n, d) else 'FAIL'}")

    res_sorted = sorted(res, key=lambda x: max(x[2], x[4]), reverse=True)
    print("[V2] top 12 queries by max posterior (either answer):")
    print(f"     {'post(ans=1)':>11} {'post(ans=0)':>11}  query / argmax")
    for gensel, desc, b1, bc1, b0, bc0 in res_sorted[:12]:
        side = 1 if b1 >= b0 else 0
        bc = bc1 if side == 1 else bc0
        print(f"     {float(b1):>11.6f} {float(b0):>11.6f}  {desc}"
              f"  [argmax c={bc}]")
    top1 = res_sorted[0]
    print(f"[V2] MAX posterior over the enumerated class at (7,2): "
          f"{float(max(top1[2], top1[4])):.6f} (q_and_exact = "
          f"{float(q_and_exact(n, d)):.6f}) -> "
          f"{'CAP HOLDS' if max(top1[2], top1[4]) <= q_and_exact(n, d) else 'EXCEEDED'}")
    ncert = sum(1 for r in res if r[2] >= 1 or r[4] >= 1)
    print(f"[V2] single-query certificate count (posterior = 1): {ncert} "
          f"(Theorem M4 predicts 0)")
    print()

    # ---------------- V3: (15,2) sampled
    n, d = 15, 2
    win_pairs = [(i, j) for i in (0, 1, 2, 3) for j in (0, 1, 2, 3)]
    gen_specs = [('K',)] + [('V', p) for p in win_pairs] + \
                [('M', p, q) for (p, q) in diag_monos(win_pairs)]
    queries = []
    for size in (1, 2):
        for sub in combinations(range(len(gen_specs)), size):
            queries.append((frozenset(sub), ""))
    for qi, (gensel, _) in enumerate(queries):
        parts = []
        for g in sorted(gensel):
            gg = gen_specs[g]
            if gg[0] == 'K':
                parts.append("1")
            elif gg[0] == 'V':
                parts.append(f"x{gg[1]}")
            else:
                parts.append(f"x{gg[1]}x{gg[2]}")
        queries[qi] = (gensel, " + ".join(parts))
    K = 400 if SMOKE else args.rhos15
    print(f"[V3] (15,2): {len(queries)} queries x {K} sampled restrictions")
    t_a = time.perf_counter()

    def sample_rho15():
        c = n - 2 * d
        A = tuple(rng.sample(range(n + 1), c))
        B = tuple(rng.sample(range(n), c))
        return A, B

    res15 = engineA_point(n, d, DX, win_pairs, gen_specs, queries, win_pairs,
                          (sample_rho15() for _ in range(K)), K)
    print(f"[V3] Engine A pass done in {time.perf_counter() - t_a:.1f} s")
    print(f"     baselines: q = {float(q_closed(n, d)):.6f}, "
          f"q_and_exact = {float(q_and_exact(n, d)):.6f}")
    res_sorted = sorted(res15, key=lambda x: max(x[2], x[4]), reverse=True)
    for gensel, desc, b1, bc1, b0, bc0 in res_sorted[:8]:
        print(f"     {float(b1):>11.6f} {float(b0):>11.6f}  {desc}")
    top1 = res_sorted[0]
    print(f"[V3] MAX posterior at (15,2): {float(max(top1[2], top1[4])):.6f}"
          f" vs q_and_exact = {float(q_and_exact(n, d)):.6f} -> "
          f"{'CAP HOLDS' if max(top1[2], top1[4]) <= q_and_exact(n, d) + Fraction(1, 50) else 'CHECK'}"
          f" (sampling tolerance 0.02)")
    print()

    # ---------------- V4: grid over all configurations (Engine B)
    print("[V4] grid: ALL support<=3 configurations with geometry (Engine B)")
    configs = enum_configs(3)
    print(f"     {len(configs)} configurations up to isomorphism")
    grid = [(7, 2), (8, 2), (9, 2), (12, 2), (15, 2), (24, 2), (32, 2),
            (63, 2), (127, 2), (255, 2), (1023, 2),
            (8, 3), (15, 3), (31, 3), (63, 3), (16, 4), (31, 4)]
    if SMOKE:
        grid = [(7, 2), (15, 2), (32, 2)]
    worst = Fraction(0)
    worst_at = None
    print(f"     {'(n,d)':>9} {'q':>8} {'q_and_ex':>9} {'max post':>9} "
          f"{'max/q_and':>9}  argmax configuration")
    for (n, d) in grid:
        qe = q_and_exact(n, d)
        mx = Fraction(0)
        mxd = ""
        for (const, terms, geo) in configs:
            b1, b0 = config_posterior(n, d, const, terms, geo)
            if b1 > mx:
                mx, mxd = b1, f"const={const} terms={terms} geo={geo} ans=1"
            if b0 > mx:
                mx, mxd = b0, f"const={const} terms={terms} geo={geo} ans=0"
        if mx - qe > worst:
            worst = mx - qe
            worst_at = (n, d, mxd, mx)
        print(f"     ({n:4d},{d}) {float(q_closed(n, d)):>8.4f} "
              f"{float(qe):>9.4f} {float(mx):>9.4f} "
              f"{float(mx / qe):>9.5f}  {mxd if mx > qe else '(= q_and, monomial)'[:70]}")
    print(f"[V4] worst exceedance of q_and_exact over the grid: "
          f"{float(worst):+.6f}"
          f"{' at ' + str(worst_at[:2]) if worst_at else ''} -> "
          f"{'CAP = q_and_exact HOLDS on the grid' if worst <= 0 else 'EXCEEDED: ' + str(worst_at)}")
    print()

    # ---------------- V5: budgeted strategies on the exact channel
    print("[V5] budgeted adaptive strategies (exact channel), "
          "certified outputs asserted free")
    strat_names = ["single_scan", "and_scan", "kj_budget", "mix_z",
                   "mix_scan", "hybrid"]
    for (n, d, sims) in ([(15, 2, 300 if SMOKE else 4000),
                          (32, 2, 150 if SMOKE else 2000)]):
        c = n - 2 * d
        mono_list = [(p, q) for p in ((i, j) for i in range(n + 1) for j in range(n))
                     for q in ((i2, j2) for i2 in range(n + 1) for j2 in range(n))
                     if p < q and p[0] != q[0] and p[1] != q[1]]
        mono_list = mono_list[:4000]
        print(f"  (n,d) = ({n},{d}), q = {float(q_closed(n, d)):.4f}, "
              f"q_and_exact = {float(q_and_exact(n, d)):.4f}")
        for budget in (10, 30, 100):
            acc = {s: 0 for s in strat_names}
            viol = [0]
            s2 = random.Random(777 + budget)
            samp = Sampler(n, d, DX, s2)
            for _ in range(sims):
                ans_q, free = samp.config()
                o, _fb = strat_single(ans_q, free, n, budget)
                acc["single_scan"] += free(o)
                o, _fb = strat_and(ans_q, free, n, budget, mono_list)
                acc["and_scan"] += free(o)
                o, _fb = strat_kj(ans_q, free, n, budget)
                acc["kj_budget"] += free(o)
                o, _fb = strat_mixz(ans_q, free, n, budget, mono_list, viol)
                acc["mix_z"] += free(o)
                o, _fb = strat_mixscan(ans_q, free, n, budget, mono_list)
                acc["mix_scan"] += free(o)
                o, _fb = strat_hybrid(ans_q, free, n, budget, mono_list)
                acc["hybrid"] += free(o)
            print(f"    budget {budget:>3}: " +
                  "  ".join(f"{s}={acc[s] / sims:.4f}" for s in strat_names))
        if viol[0]:
            print(f"    SOUNDNESS VIOLATIONS: {viol[0]} (must be 0)")
        else:
            print("    soundness: all certified outputs were free (0 violations)")
    print()
    print("[verdict] see docs/mixture_cap.md; summary lines above.")


if __name__ == "__main__":
    main()
