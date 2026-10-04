#!/usr/bin/env python3
"""chi_mixture3.py

MIXTURE-3 (all_degrees.md section 5.2 item 2): O2's literal quantifier allows
arbitrary degree-<=d polynomials as queries.  The mixture class is covered
only at d = 2 (mixture_cap.md, Theorems M-A/M-B/M-D).  This script measures
the exact per-hit labeling posterior over the FULL printed degree-<=3 class
(F_2 mixtures of a constant, singles, degree-2 diagonals, and degree-3
matching triples) on the true Omega(n,d) pipeline at p = 2, at d >= 3 where
degree-3 monomial columns exist, and tests whether the covered constant
q3* = max(q, q_and_exact, post3) (deg3_theory.md Theorem P3) survives.

Degree-3 queries need d >= 3 (ans(g) = L(g^rho) is defined for deg g <= d),
so the slice points are (7,3)/(8,3)/(15,3) and the regime-style points
(31,3)/(63,3); the d = 4 rows probe the d-dependence.

Channel: the TRUE pipeline (uniform designs of the restricted canonical
system V(2d,d); kernel_structure.md F1).  Two engines, as in
chi_mixture_cap.py:

  Engine A (design-exact): restricted coordinate "vector" v = g^rho kept as
      a small set of raw monomial columns (each restricted term contributes
      at most one column: a single column, a diagonal column, a triple
      column, the constant column 0, or nothing); V-membership is automatic
      because every design vanishes on V.  P[ans=1|rho] = exact fraction of
      the design coset Lstar + kernel with L(v) = 1 (projected-kernel
      enumeration, the chi_deg3_check.py pattern).
  Engine B (status-exact): per status pattern (F/M/K per slot) the answer
      is a fair coin iff the XOR-cancelled live coordinate set is nonempty,
      else the determined constant; exact pattern weights by Lemma N3
      (chi_mixture_cap.py weight_pattern, degree-agnostic).  Exact for
      support <= 3 because at d >= 3 the smallest determined relation on
      all-distinct free coordinates is a degree-3 star (2d-2 >= 4 fresh
      triple columns); rows need 2d >= 6 and degree-2 stars 2d-1 >= 5.

Normal form (Lemma N1 extended to degree 3): squares alias to variables,
x^2 y aliases to x y (or 0 on a line), collision-containing monomials are
determined 0, so every printed query reduces to c + singles + diagonals +
matching triples.

Checks (registered run):
  V0  pattern weights partition the restriction space at (7,3); Engine B
      pure single / diagonal / triple reproduce q, q_and_exact, post3
      digit-exactly at several points (Theorem P3 cross-check).
  V1  (7,3): Engine B == Engine A digit-exact on all enumerated concrete
      queries x both answers x support roles over ALL 56 restrictions.
  V2  (7,3) posterior max over the abstract class scan (through-output
      star hypergraphs with <= 4 partners exhaustively over geometries,
      all-distinct 5/6-partner stars, general and sampled configurations);
      single-query certificate count (Theorem M3-B analogue: 0 expected).
  V3  (15,3): panel of queries on sampled restrictions vs Engine B
      (per-comparison 5-sigma tolerance).
  V4  grid: winners + baselines on a (n,d) grid vs
      q3_cov = max(q, q_and_exact, post3); exact fractions and ratios.
  V5  budgeted adaptive strategies at (7,3) and (15,3) on the exact
      channel; certified outputs asserted free (soundness).
  V6  mechanism tables: per-output-status decomposition of the winner
      (killed-branch self-exclusion check) at (15,3).

Run: python3 experiments/chi_mixture3.py [--smoke]
"""
from __future__ import annotations

import argparse
import math
import os
import random
import sys
import time
from collections import Counter
from fractions import Fraction
from itertools import combinations, permutations, product

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from kernel_structure import canonical_rows, echelon_rhs, particular
from razborov_check import monomials
import chi_mixture_cap as capm
from chi_mixture_cap import (DesignExact, _partitions, _rank_geo, count_rhos,
                             p_ext_free, posts_from_table, q_and_exact,
                             q_closed, rho_data, rhos_all, weight_pattern)

T0 = time.perf_counter()


def elapsed() -> float:
    return time.perf_counter() - T0


# ------------------------------------------------------- Engine B (degree 3)

def law_of_terms3(terms, assign, const):
    """Live coordinate set (XOR-cancelled) and determined constant.

    terms: ('V', s) / ('M', a, b) / ('T', a, b, c) over slot indices.
    assign: 'F'/'M'/'K' per slot.  Live keys: (s,) single column,
    (a, b) diagonal column, (a, b, c) triple column.  Returns
    (live_nonempty, det): the per-pattern answer law is a fair coin in the
    first case and the determined constant det otherwise (Lemma N2 read at
    degree 3; exact on <= 3 live coordinates because no determined
    relation of degree <= 3 lives on <= 3 all-distinct free coordinates).
    """
    live = {}
    det = const
    for t in terms:
        if t[0] == 'V':
            s = assign[t[1]]
            if s == 'F':
                key = (t[1],)
                live[key] = live.get(key, 0) ^ 1
            elif s == 'M':
                det ^= 1
        elif t[0] == 'M':
            _, a, b = t
            sa, sb = assign[a], assign[b]
            if sa == 'K' or sb == 'K':
                continue
            if sa == 'F' and sb == 'F':
                key = (a, b) if a < b else (b, a)
            elif sa == 'M' and sb == 'M':
                det ^= 1
                continue
            else:
                key = (a,) if sa == 'F' else (b,)
            live[key] = live.get(key, 0) ^ 1
        else:
            _, a, b, c = t
            sa, sb, sc = assign[a], assign[b], assign[c]
            if sa == 'K' or sb == 'K' or sc == 'K':
                continue
            fr = tuple(sorted(s for s, sv in ((a, sa), (b, sb), (c, sc))
                              if sv == 'F'))
            if not fr:
                det ^= 1
            else:
                live[fr] = live.get(fr, 0) ^ 1
    return any(live.values()), det


def status_table3(geo, terms, const):
    """Per-config rows: (assign, w2, frees); w2 in {0,1,2} = 2*P[ans=1|pat]."""
    t = len(geo)
    rows = []
    for assign in product('FMK', repeat=t):
        live, det = law_of_terms3(terms, assign, const)
        w2 = 1 if live else (0 if det == 0 else 2)
        frees = frozenset(k for k in range(t) if assign[k] == 'F')
        rows.append((assign, w2, frees))
    return rows


_TABLE_CACHE: dict = {}


def table3(geo, terms, const):
    return status_table3(geo, terms, const)


def virtual_post3(n, d, terms, const, geo, vgeo):
    """Exact (post1, post0) for the LAST slot of vgeo (a virtual same-line
    partner carrying no terms), given the support terms."""
    t = len(geo)
    S = [0, 0]
    Nv = [0, 0]
    for assign in product('FMK', repeat=t + 1):
        W = weight_pattern(n, d, vgeo, assign)
        if W == 0:
            continue
        live, det = law_of_terms3(terms, assign[:t], const)
        w2 = 1 if live else (0 if det == 0 else 2)
        for a, w2a in ((0, 2 - w2), (1, w2)):
            S[a] += W * w2a
            if assign[t] == 'F':
                Nv[a] += W * w2a
    return (Fraction(Nv[1], S[1]) if S[1] else Fraction(0),
            Fraction(Nv[0], S[0]) if S[0] else Fraction(0))


def posts_with_virtuals3(n, d, const, terms, geo):
    """Support-pair roles + generic external role + same-line virtual
    partner roles (virtuals only for t <= 3, as in chi_mixture_cap.py)."""
    t = len(geo)
    base = posts_from_table(n, d, geo, table3(geo, terms, const))
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
        p1, p0 = virtual_post3(n, d, terms, const, geo,
                               geo + ((c, fresh_h),))
        out[('vp', c, 1)], out[('vp', c, 0)] = p1, p0
    for h in sorted({g[1] for g in geo}):
        p1, p0 = virtual_post3(n, d, terms, const, geo,
                               geo + ((fresh_p, h),))
        out[('vh', h, 1)], out[('vh', h, 0)] = p1, p0
    return out


def concrete_engineB3(n, d, pair_terms, const):
    """Exact per-role posteriors for one concrete query (Engine B).

    pair_terms: list of ('V', p) / ('M', p, q) / ('T', p, q, r) with
    concrete outer pairs p = (i, j).  Returns (slots, posts).
    """
    slots = sorted({p for t in pair_terms for p in t[1:]})
    idx = {p: k for k, p in enumerate(slots)}
    terms = tuple((t[0],) + tuple(idx[s] for s in t[1:]) for t in pair_terms)
    geo = tuple((p[0], p[1]) for p in slots)
    raw = posts_from_table(n, d, geo, table3(geo, terms, const))
    posts = {}
    for a in (0, 1):
        for k, p in enumerate(slots):
            posts[(a, p)] = raw[('pair', k, a)]
        posts[(a, 'ext')] = raw[('ext', a)]
    return slots, posts


# --------------------------------------------------------- closed forms

def post3_exact(n, d):
    """deg3_theory.md Theorem P3: exact per-hit posterior of one
    all-distinct degree-3 monomial (matching triple)."""
    c = n - 2 * d

    def cnt(a, b, f):
        if b < 0 or a < 0 or f < 0:
            return 0
        return math.comb(a, b) * math.factorial(f)

    A0 = (cnt(n - 2, c - 3, c - 3) * math.comb(n - 3, c - 3)
          if c >= 3 else 0)
    u = (math.comb(n - 2, c - 1) * math.comb(n - 3, c - 1)
         * math.factorial(c - 1)) if c >= 1 else 0
    v = (math.comb(n - 2, c - 2) * math.comb(n - 3, c - 2)
         * math.factorial(c - 2)) if c >= 2 else 0
    w = math.comb(n - 2, c) * math.comb(n - 3, c) * math.factorial(c)
    return Fraction(2 * u + v + w, 2 * A0 + 3 * u + 3 * v + w)


def q3_cov(n, d):
    """The covered degree-<=3 constant: max(q, q_and_exact, post3)."""
    return max(q_closed(n, d), q_and_exact(n, d), post3_exact(n, d))


# --------------------------------------------------- abstract configurations

TERM_OCC = {'V': 1, 'M': 2, 'T': 3}


def _edges(terms):
    pairs = [t[1:] for t in terms if t[0] == 'M']
    triples = [t[1:] for t in terms if t[0] == 'T']
    return pairs, triples


def _valid_partial(pairs, triples, pig, hol, upto):
    for pr in pairs:
        if max(pr) <= upto and (pig[pr[0]] == pig[pr[1]]
                                or hol[pr[0]] == hol[pr[1]]):
            return False
    for tr in triples:
        if max(tr) <= upto and (len({pig[x] for x in tr}) < 3
                                or len({hol[x] for x in tr}) < 3):
            return False
    return True


def enum_geoms(terms, k, mode, rng, n_sample):
    """Geometries ((pigclass, holclass) per slot; slot 0 fixed to (0,0)).

    mode 'full': canonical exhaustive enumeration (k <= 4).
    mode 'distinct': the all-distinct star (each partner its own pigeon and
    hole class) - the d = 2 winner's geometry.
    mode 'sample': random valid geometries (falsification probe).
    """
    pairs, triples = _edges(terms)
    out = []
    seen = set()
    if k == 0:
        return [((0, 0),)]
    if mode == 'distinct':
        pig = [0] * (k + 1)
        hol = [0] * (k + 1)
        used = {(0, 0)}
        for s in range(1, k + 1):
            if (s, s) in used:
                return []
            pig[s], hol[s] = s, s
            used.add((s, s))
        if _valid_partial(pairs, triples, pig, hol, k):
            return [tuple((pig[s], hol[s]) for s in range(k + 1))]
        return []
    if mode == 'full':
        pig = [0] * (k + 1)
        hol = [0] * (k + 1)
        used = {(0, 0)}

        def rec(i):
            if i > k:
                key = _rank_geo(list(zip(pig, hol)))
                if key not in seen:
                    seen.add(key)
                    out.append(tuple((pig[s], hol[s])
                                     for s in range(k + 1)))
                return
            mp = max(pig[:i])
            mh = max(hol[:i])
            for pc in range(mp + 2):
                for hc in range(mh + 2):
                    if (pc, hc) in used:
                        continue
                    pig[i], hol[i] = pc, hc
                    used.add((pc, hc))
                    if _valid_partial(pairs, triples, pig, hol, i):
                        rec(i + 1)
                    used.discard((pc, hc))
        rec(1)
        return out

    tries = 0
    while len(out) < n_sample and tries < n_sample * 60:
        tries += 1
        p2, h2 = [0] * (k + 1), [0] * (k + 1)
        u2 = {(0, 0)}
        ok = True
        for s in range(1, k + 1):
            for _ in range(40):
                pc = rng.randrange(0, k + 2)
                hc = rng.randrange(0, k + 2)
                if (pc, hc) not in u2:
                    break
            else:
                ok = False
                break
            p2[s], h2[s] = pc, hc
            u2.add((pc, hc))
        if not ok or not _valid_partial(pairs, triples, p2, h2, k):
            continue
        key = _rank_geo(list(zip(p2, h2)))
        if key not in seen:
            seen.add(key)
            out.append(tuple((p2[s], h2[s]) for s in range(k + 1)))
    return out


def _hypergraphs_from_types(types, anchor):
    """All slot-identification patterns for a multiset of term types.

    anchor=True: every term contains the output slot 0 (star families; a
    V-term is the output variable x_ab itself).
    Returns list of (name, terms, k) with terms over slots 0..k.
    """
    if anchor:
        occs = [(ti, pi) for ti, ty in enumerate(types)
                for pi in range(TERM_OCC[ty] - 1)]
    else:
        occs = [(ti, pi) for ti, ty in enumerate(types)
                for pi in range(TERM_OCC[ty])]
    out = []
    seen = set()
    for part in _partitions(occs):
        blk_of = {}
        for bi, block in enumerate(part):
            for o in block:
                blk_of[o] = bi
        ok = True
        for ti, ty in enumerate(types):
            na = TERM_OCC[ty] - (1 if anchor else 0)
            if na == 0:
                continue
            bs = [blk_of[(ti, pi)] for pi in range(na)]
            if len(set(bs)) != len(bs):
                ok = False
                break
        if not ok:
            continue
        if anchor:
            m_blocks = [blk_of[(ti, 0)] for ti, ty in enumerate(types)
                        if ty == 'M']
            if len(set(m_blocks)) != len(m_blocks):
                continue
            tbs = [[blk_of[(ti, 0)], blk_of[(ti, 1)]]
                   for ti, ty in enumerate(types) if ty == 'T']
            if any(set(tbs[i]) == set(tbs[j])
                   for i in range(len(tbs))
                   for j in range(i + 1, len(tbs))):
                continue
        flat = {o: i for i, o in enumerate(occs)}
        order = sorted(range(len(part)),
                       key=lambda bi: min(flat[o] for o in part[bi]))
        rank = {bi: i + (1 if anchor else 0) for i, bi in enumerate(order)}
        terms = []
        for ti, ty in enumerate(types):
            if anchor:
                # every term contains the output slot 0; the remaining
                # slots are the term's partner occurrences (an unordered
                # set: same slot set = same monomial)
                terms.append((ty, 0)
                             + tuple(sorted(rank[blk_of[(ti, pi)]]
                                            for pi in range(TERM_OCC[ty]
                                                            - 1))))
            elif ty == 'V':
                terms.append(('V', rank[blk_of[(ti, 0)]]))
            else:
                terms.append((ty,)
                             + tuple(sorted(rank[blk_of[(ti, pi)]]
                                            for pi in range(TERM_OCC[ty]))))
        key = tuple(terms)
        if key in seen:
            continue
        seen.add(key)
        out.append(("".join(types)
                    + ("-star" if anchor else "-gen")
                    + str(len(part)), tuple(terms), len(part)))
    return out


TYPE_SETS = [['V'], ['M'], ['T'],
             ['M', 'M'], ['M', 'T'], ['T', 'T'], ['V', 'M'], ['V', 'T'],
             ['M', 'M', 'M'], ['M', 'M', 'T'], ['M', 'T', 'T'],
             ['T', 'T', 'T'], ['V', 'M', 'M'], ['V', 'M', 'T'],
             ['V', 'T', 'T']]


def build_configs(rng, k_full=4, samp5=60, samp6=20, gen3_samples=400):
    """All abstract degree-<=3 mixture configurations for the scan.

    Complete: through-output star hypergraphs (every term through the
    output slot) with <= 4 partner slots, exhaustively over geometries;
    plus the all-distinct geometry for every 5- and 6-partner star.
    Sampled: shared-class geometries at 5/6 partners, general (not
    through-output) 2-term hypergraphs exhaustively at <= 4 slots, and
    sampled general 3-term hypergraphs at <= 6 slots.
    Returns list of (name, terms, geo).
    """
    out = []
    seen = set()

    def add(name, terms, geo):
        key = tuple(sorted((t[0],) + tuple(geo[s] for s in t[1:])
                           for t in terms))
        if key in seen:
            return False
        seen.add(key)
        out.append((name, terms, geo))
        return True

    nstar = 0
    for types in TYPE_SETS:
        for (name, terms, k) in _hypergraphs_from_types(types, anchor=True):
            if k <= k_full:
                geoms = enum_geoms(terms, k, 'full', rng, 0)
            else:
                geoms = enum_geoms(terms, k, 'distinct', rng, 0)
                ns = samp5 if k == 5 else samp6
                geoms += enum_geoms(terms, k, 'sample', rng, ns)
            for g in geoms:
                if add(name, terms, g):
                    nstar += 1
    ngen2 = 0
    for types in [['V', 'V'], ['V', 'M'], ['V', 'T'], ['M', 'M'],
                  ['M', 'T'], ['T', 'T']]:
        for (name, terms, k) in _hypergraphs_from_types(types, anchor=False):
            if k <= k_full:
                geoms = enum_geoms(terms, k, 'full', rng, 0)
            else:
                geoms = enum_geoms(terms, k, 'distinct', rng, 0)
                geoms += enum_geoms(terms, k, 'sample', rng, 20)
            for g in geoms:
                if add(name, terms, g):
                    ngen2 += 1
    ngen3 = 0
    tries = 0
    while ngen3 < gen3_samples and tries < gen3_samples * 300:
        tries += 1
        types = [rng.choice(['V', 'M', 'T']) for _ in range(3)]
        occs = [(ti, pi) for ti, ty in enumerate(types)
                for pi in range(TERM_OCC[ty])]
        part = {}
        nxt = 0
        for o in occs:
            if rng.random() < 0.5 and nxt:
                part[o] = rng.randrange(nxt)
            else:
                part[o] = nxt
                nxt += 1
        if nxt > 6:
            continue
        ok = True
        for ti, ty in enumerate(types):
            bs = [part[(ti, pi)] for pi in range(TERM_OCC[ty])]
            if len(set(bs)) != len(bs):
                ok = False
                break
        if not ok:
            continue
        order = sorted(set(part.values()))
        rank = {b: i for i, b in enumerate(order)}
        terms = []
        for ti, ty in enumerate(types):
            if ty == 'V':
                terms.append(('V', rank[part[(ti, 0)]]))
            else:
                terms.append((ty,)
                             + tuple(rank[part[(ti, pi)]]
                                     for pi in range(TERM_OCC[ty])))
        geoms = enum_geoms(terms, nxt, 'full' if nxt <= k_full else 'sample',
                           rng, 12)
        for g in geoms:
            if add("".join(types) + "-gen3s", tuple(terms), g):
                ngen3 += 1
                break
    print(f"[cfg] star configs {nstar}, general-2 {ngen2}, "
          f"general-3 sampled {ngen3}, total {len(out)} "
          f"({elapsed():.1f} s)")
    return out


# ------------------------------------------------- Engine A (design-exact)

def build_designs(d):
    DX = DesignExact(d)
    DX.colT = {t: i for i, t in enumerate(DX.monos) if len(t) == 3}
    return DX


def gen_desc(g):
    if g[0] == 'V':
        return f"x{g[1]}"
    if g[0] == 'M':
        return f"x{g[1]}x{g[2]}"
    return f"x{g[1]}x{g[2]}x{g[3]}"


def restricted_col(g, st, cvar, DX, n):
    """Restricted column set of one generator under rho (frozenset)."""
    if g[0] == 'V':
        i, j = g[1]
        s = st[i * n + j]
        if s == 1:
            return frozenset((0,))
        if s == 0:
            return frozenset((cvar[i * n + j],))
        return frozenset()
    if g[0] == 'M':
        i, j = g[1]
        i2, j2 = g[2]
        s1, s2 = st[i * n + j], st[i2 * n + j2]
        if s1 == 2 or s2 == 2:
            return frozenset()
        if s1 == 1 and s2 == 1:
            return frozenset((0,))
        if s1 == 1:
            return frozenset((cvar[i2 * n + j2],))
        if s2 == 1:
            return frozenset((cvar[i * n + j],))
        u, v = sorted((cvar[i * n + j] - 1, cvar[i2 * n + j2] - 1))
        return frozenset((DX.colD[(u, v)],))
    i, j = g[1]
    i2, j2 = g[2]
    i3, j3 = g[3]
    ss = (st[i * n + j], st[i2 * n + j2], st[i3 * n + j3])
    if 2 in ss:
        return frozenset()
    fr = [(a, b) for (a, b), s in (((i, j), ss[0]), ((i2, j2), ss[1]),
                                   ((i3, j3), ss[2])) if s == 0]
    if not fr:
        return frozenset((0,))
    if len(fr) == 1:
        return frozenset((cvar[fr[0][0] * n + fr[0][1]],))
    if len(fr) == 2:
        u, v = sorted((cvar[fr[0][0] * n + fr[0][1]] - 1,
                       cvar[fr[1][0] * n + fr[1][1]] - 1))
        return frozenset((DX.colD[(u, v)],))
    u, v, w = sorted(cvar[a * n + b] - 1 for (a, b) in fr)
    return frozenset((DX.colT[(u, v, w)],))


def query_pairs(gen_specs, gensel):
    s = set()
    for g in gensel:
        s.update(gen_specs[g][1:])
    return sorted(s)


def engineA_point3(n, d, DX, gen_specs, queries, pairs, rho_source):
    """Engine A pass: exact posterior per role for each query.

    queries: list of (frozenset-of-gen-indices, desc).  Rho-major pass:
    per restriction only the needed generators are restricted; query
    vectors are small column sets kept as sorted tuples (each restricted
    term contributes at most one column).  P[ans=1|rho] is computed from
    the projected kernel on the support (dimension <= 3), scaled to the
    common denominator 8.  Returns {gensel: (desc, posts, den1, den0)}.
    """
    ncand = len(pairs)
    pos = {p: k for k, p in enumerate(pairs)}
    qsel = []
    qdesc = {}
    for gensel, desc in queries:
        gs = sorted(gensel)
        qdesc[frozenset(gs)] = desc
        own = [pos[p] for p in query_pairs(gen_specs, gs)]
        ft = 0
        for k in own:
            ft |= 1 << k
        qsel.append((gs, tuple(own), ft))
    used_g = set()
    for gs, _, _ in qsel:
        used_g.update(gs)
    tallies = [Counter() for _ in qsel]
    cntF = [0] * ncand
    nrho = 0
    wset = {}

    def w_of(ts):
        ent = wset.get(ts)
        if ent is None:
            T = tuple(ts)
            LsT = 0
            for k, c in enumerate(T):
                if (DX.Lstar >> c) & 1:
                    LsT |= 1 << k
            pi = DX._pk(T)
            dim = len(pi)
            cnt = 0
            for msk in range(1 << dim):
                y = LsT
                for b in range(dim):
                    if (msk >> b) & 1:
                        y ^= pi[b]
                if y.bit_count() & 1:
                    cnt += 1
            ent = (cnt, 1 << dim)
            wset[ts] = ent
        return ent

    for A, B in rho_source:
        st, cvar = rho_data(n, d, A, B)
        cm = 0
        for k, (i, j) in enumerate(pairs):
            if st[i * n + j] == 0:
                cm |= 1 << k
                cntF[k] += 1
        cols = {gi: restricted_col(gen_specs[gi], st, cvar, DX, n)
                for gi in used_g}
        for qi, (gs, own, ft) in enumerate(qsel):
            v: set = set()
            for gi in gs:
                v ^= cols[gi]
            tallies[qi][(tuple(sorted(v)), cm & ft)] += 1
        nrho += 1
    out = {}
    for qi, (gs, own, ft) in enumerate(qsel):
        gensel = frozenset(gs)
        desc = qdesc[gensel]
        S1 = 0
        N1 = [0] * ncand
        for (ts, om), cnt in tallies[qi].items():
            wn, wd = w_of(ts)
            wi = wn * (8 // wd)
            S1 += cnt * wi
            m = om
            k = 0
            while m:
                if m & 1:
                    N1[k] += cnt * wi
                m >>= 1
                k += 1
        posts = {}
        for k in own:
            p1 = Fraction(N1[k], S1) if S1 else Fraction(0)
            den0 = nrho * 8 - S1
            p0 = Fraction(cntF[k] * 8 - N1[k], den0) if den0 else Fraction(0)
            posts[pairs[k]] = {1: p1, 0: p0}
        out[gensel] = (desc, posts, Fraction(S1, 8), nrho - Fraction(S1, 8))
    return out


# ------------------------------------------------------------ channel sim

class Sampler3:
    """Exact-channel configuration sampler at (n, d), d >= 3."""

    def __init__(self, n, d, DX, rng):
        self.n, self.d, self.DX, self.rng = n, d, DX, rng
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

        def ans_triple(p, q, r):
            sv = [pairinfo(p), pairinfo(q), pairinfo(r)]
            if 2 in sv:
                return 0
            fr = [x for x, s in ((p, sv[0]), (q, sv[1]), (r, sv[2]))
                  if s == 0]
            if not fr:
                return 1
            if len(fr) == 1:
                return ans_var(fr[0])
            if len(fr) == 2:
                a, b = sorted((col(fr[0]) - 1, col(fr[1]) - 1))
                return (L >> self.DX.colD[(a, b)]) & 1
            a, b, cc = sorted(col(x) - 1 for x in fr)
            return (L >> self.DX.colT[(a, b, cc)]) & 1

        def ans_q(g):
            if g[0] == 'V':
                return ans_var(g[1])
            if g[0] == 'M':
                return ans_mono(g[1], g[2])
            if g[0] == 'T':
                return ans_triple(g[1], g[2], g[3])
            return 1

        def free(p):
            return pairinfo(p) == 0

        def ans_K(j):
            v = 1
            for i in range(n + 1):
                v ^= ans_var((i, j))
            return v

        return ans_q, free, ans_K


# -------------------------------------------------------------- strategies

def strat_single(ans_q, free, n, budget, order):
    used = 0
    for p in order:
        if used >= budget:
            return (0, 0)
        used += 1
        if ans_q(('V', p)) == 1:
            return p
    return (0, 0)


def strat_kj(ans_q, free, n, budget):
    """Covered champion, corpus form: parity per column via n+1 singles."""
    used = 0
    cert = []
    for j in range(n):
        if used + n + 1 > budget:
            break
        used += n + 1
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


def strat_kj_direct(ans_q, free, ans_K, n, budget, order_j):
    """Covered champion, linear form queried as ONE query per column."""
    used = 0
    cert = []
    for j in order_j:
        if used >= budget:
            break
        used += 1
        if ans_K(j) == 1:
            cert.append(j)
    for j in cert:
        for i in range(n + 1):
            if used >= budget:
                return (0, 0)
            used += 1
            if ans_q(('V', (i, j))) == 1:
                return (i, j)
    return (0, 0)


def strat_triplescan(ans_q, free, n, budget, tri_list):
    used = 0
    for t in tri_list:
        if used >= budget:
            return (0, 0)
        used += 1
        if ans_q(('T',) + t) == 1:
            return t[0]
    return (0, 0)


def strat_mix3(ans_q, free, n, budget, out_list, partners_of, fam):
    """Star-mixture scan: for each candidate output pair, one mixture
    query (the XOR of its term answers)."""
    used = 0
    for ab in out_list:
        if used >= budget:
            return (0, 0)
        used += 1
        v = 0
        for t in fam(ab, partners_of(ab)):
            v ^= ans_q(t)
        if v == 1:
            return ab
    return (0, 0)


def strat_mixz3(ans_q, free, n, budget, tri_list, viol):
    """Degree-3 mixture-folded Z certificate: x_p + T, then T."""
    used = 0
    for t in tri_list:
        if used >= budget:
            break
        used += 1
        if (ans_q(('V', t[0])) ^ ans_q(('T',) + t)) == 1:
            if used >= budget:
                break
            used += 1
            if ans_q(('T',) + t) == 1:
                if not free(t[0]):
                    viol[0] += 1
                return t[0]
    return (0, 0)


def strat_wedge3(ans_q, free, n, budget, wedge_list, viol):
    """Covered deg-3 inventory (Lemma S3 strongest form): two monomials
    carrying the same pigeon in DISTINCT hole cells, nothing else shared;
    both answering 1 certify that pigeon free; then scan its row."""
    used = 0
    for (t1, t2, p) in wedge_list:
        if used + 2 > budget:
            break
        used += 2
        if ans_q(('T',) + t1) == 1 and ans_q(('T',) + t2) == 1:
            for j in range(n):
                if used >= budget:
                    return (0, 0)
                used += 1
                if ans_q(('V', (p, j))) == 1:
                    if not free((p, j)):
                        viol[0] += 1
                    return (p, j)
    return (0, 0)


def strat_hybrid3(ans_q, free, n, budget, order, tri_list):
    used = 0
    ti = 0
    for p in order:
        if used >= budget:
            return (0, 0)
        used += 1
        if ans_q(('V', p)) == 1:
            return p
        if used >= budget:
            return (0, 0)
        if ti < len(tri_list):
            t = tri_list[ti]
            ti += 1
            used += 1
            if ans_q(('T',) + t) == 1:
                return t[0]
    return (0, 0)


# --------------------------------------------------------------------- main

def match_triples(pairs):
    """All matching triples (distinct pigeons, distinct holes) in a window."""
    out = []
    for a, b, c in combinations(range(len(pairs)), 3):
        pa, pb, pc = pairs[a], pairs[b], pairs[c]
        if (len({pa[0], pb[0], pc[0]}) == 3
                and len({pa[1], pb[1], pc[1]}) == 3):
            out.append((pa, pb, pc))
    return out


def diag_monos(pairs):
    out = []
    for a in range(len(pairs)):
        for b in range(a + 1, len(pairs)):
            (i1, j1), (i2, j2) = pairs[a], pairs[b]
            if i1 != i2 and j1 != j2:
                out.append((pairs[a], pairs[b]))
    return out


def instantiate(terms, geo):
    """Concrete pairs for an abstract config (class index = outer index)."""
    out = []
    for t in terms:
        out.append((t[0],) + tuple((geo[s][0], geo[s][1]) for s in t[1:]))
    return tuple(out)


def scan_point(n, d, cfgs, keep=None):
    """Max posterior over configs (all roles incl. ext and virtuals),
    with certificate count and a ranked top list."""
    best = Fraction(0)
    arg = None
    ncert = 0
    ranked = []
    for (name, terms, geo) in cfgs:
        posts = posts_with_virtuals3(n, d, 0, terms, geo)
        loc = max(posts.values())
        if loc >= 1:
            ncert += 1
        ranked.append((loc, name, terms, geo))
        if loc > best:
            best = loc
            am = max(posts, key=lambda k: posts[k])
            arg = (name, am, terms, geo)
    ranked.sort(reverse=True, key=lambda x: x[0])
    capm._WP_CACHE.clear()
    return best, arg, ranked[:keep] if keep else ranked, ncert


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--rhos15", type=int, default=20000)
    ap.add_argument("--samp5", type=int, default=60)
    ap.add_argument("--samp6", type=int, default=20)
    ap.add_argument("--gen3", type=int, default=400)
    args = ap.parse_args()
    SMOKE = args.smoke
    if SMOKE:
        args.samp5, args.samp6, args.gen3 = 8, 4, 60
        args.rhos15 = 4000
    rng = random.Random(20261004)

    print("chi_mixture3: MIXTURE-3 - the per-hit posterior cap over the")
    print("FULL printed degree-<=3 class (F_2 mixtures) on the true")
    print("Omega(n,d) pipeline at p=2, d>=3. Engine A = exact")
    print("projected-coset answer law; Engine B = proved alive/dead")
    print("status calculus with exact inclusion-exclusion pattern")
    print("weights; they must agree digit-exactly.")
    print()

    # ================= V0: machinery + closed-form baselines ============
    DX3 = build_designs(3)
    print(f"[setup] restricted system (6,3): {DX3.ncols} columns, "
          f"kernel dim {len(DX3.kb)} (dim Des = 2079 expected), "
          f"Lstar(1) = {DX3.Lstar & 1} (must be 1)")
    assert DX3.ncols == 14190 and len(DX3.kb) == 2079
    assert DX3.Lstar & 1 == 1

    tot = count_rhos(7, 3)
    geo3 = ((0, 0), (1, 1), (2, 1))
    s = sum(weight_pattern(7, 3, geo3, a) for a in product('FMK', repeat=3))
    print(f"[V0] (7,3) 3-slot shared-pigeon weights sum: {s} vs "
          f"restriction count {tot} -> {'PASS' if s == tot else 'FAIL'}")
    assert s == tot

    single = (('V', 0), ((0, 0),))
    diag = (('M', 0, 1), ((0, 0), (1, 1)))
    tri = (('T', 0, 1, 2), ((0, 0), (1, 1), (2, 2)))
    ok_all = True
    for (n, d) in [(7, 3), (8, 3), (15, 3), (31, 3), (15, 4)]:
        p_s = posts_with_virtuals3(n, d, 0, (single[0],), single[1])
        p_d = posts_with_virtuals3(n, d, 0, (diag[0],), diag[1])
        p_t = posts_with_virtuals3(n, d, 0, (tri[0],), tri[1])
        ok = (p_s[('pair', 0, 1)] == q_closed(n, d)
              and p_d[('pair', 0, 1)] == q_and_exact(n, d)
              and p_t[('pair', 0, 1)] == post3_exact(n, d))
        ok_all &= ok
        print(f"[V0] ({n},{d}) pure single/diag/triple = "
              f"{float(p_s[('pair', 0, 1)]):.6f} / "
              f"{float(p_d[('pair', 0, 1)]):.6f} / "
              f"{float(p_t[('pair', 0, 1)]):.6f} vs q / q_and_ex / post3 = "
              f"{float(q_closed(n, d)):.6f} / {float(q_and_exact(n, d)):.6f}"
              f" / {float(post3_exact(n, d)):.6f} -> "
              f"{'PASS (digit-exact)' if ok else 'FAIL'}")
    assert ok_all
    print()

    # ================= build the configuration space ====================
    configs = build_configs(rng, samp5=args.samp5, samp6=args.samp6,
                            gen3_samples=args.gen3)

    # ================= V2: full scan at (7,3) ===========================
    n, d = 7, 3
    print(f"[V2] full abstract scan at (7,3) over {len(configs)} configs")
    best7, arg7, top7, ncert = scan_point(n, d, configs, keep=40)
    qc = q3_cov(n, d)
    print(f"[V2] (7,3) MAX posterior = {best7} = {float(best7):.6f} vs "
          f"q3_cov = max(q, q_and_ex, post3) = {qc} = {float(qc):.6f} -> "
          f"{'EXCEEDED' if best7 > qc else 'COVERED CAP HOLDS'}")
    print(f"[V2] argmax: {arg7[0]} role {arg7[1][:2]} "
          f"terms {arg7[2]} geo {arg7[3]}")
    print("[V2] top 12:")
    for loc, name, terms, geo in top7[:12]:
        print(f"     {float(loc):.6f}  {name}  {terms} {geo}")
    print(f"[V2] single-query certificates (posterior = 1) among all "
          f"{len(configs)} configs: {ncert} (Theorem M3-B analogue: "
          f"0 expected)")
    print()

    # ================= V1: Engine A cross-validation at (7,3) ===========
    n, d = 7, 3
    allp = [(i, j) for i in range(n + 1) for j in range(n)]
    gen_specs = [('V', p) for p in allp] \
        + [('M', p, q) for (p, q) in diag_monos(allp)] \
        + [('T',) + t for t in match_triples(allp)]
    gpos = {g: k for k, g in enumerate(gen_specs)}
    queries = []
    qseen = set()

    def addq(terms):
        try:
            gensel = frozenset(gpos[t] for t in terms)
        except KeyError:
            return
        if gensel not in qseen:
            qseen.add(gensel)
            queries.append((gensel, ""))

    core = [(i, j) for i in (0, 1, 2, 3) for j in (0, 1, 2, 3, 4)]
    core_set = set(core)
    core_gi = [k for k, g in enumerate(gen_specs)
               if all(p in core_set for p in g[1:])]
    for g in core_gi:
        addq((gen_specs[g],))
    pairs2 = list(combinations(core_gi, 2))
    for sub in rng.sample(pairs2, min(2600, len(pairs2))):
        addq(tuple(gen_specs[g] for g in sub))
    star3 = set()
    for ab in core:
        pool = [('V', ab)]
        pool += [('M', ab, q) for q in core
                 if q != ab and q[0] != ab[0] and q[1] != ab[1]]
        pool += [('T', ab, q, r) for q in core for r in core
                 if q != ab and r != ab and q != r
                 and q[0] != ab[0] and q[1] != ab[1]
                 and r[0] != ab[0] and r[1] != ab[1]
                 and q[0] != r[0] and q[1] != r[1]][:12]
        for sub in combinations(pool, 3):
            if len({p for t in sub for p in t[1:]}) <= 5:
                star3.add(tuple(sorted(sub)))
    star3 = sorted(star3)
    for sub in rng.sample(star3, min(300 if SMOKE else 2000, len(star3))):
        addq(sub)
    for loc, name, terms, geo in top7:
        addq(instantiate(terms, geo))
    allg = list(range(len(gen_specs)))
    for _ in range(0 if SMOKE else 1500):
        ts = [gen_specs[g] for g in rng.sample(allg, rng.choice([2, 3]))]
        ps = [p for t in ts for p in t[1:]]
        if len({(p[0], p[1]) for p in ps}) != len(ps):
            continue
        ok = True
        for t in ts:
            if t[0] == 'M' and (t[1][0] == t[2][0] or t[1][1] == t[2][1]):
                ok = False
            if t[0] == 'T' and (len({x[0] for x in t[1:]}) < 3
                                or len({x[1] for x in t[1:]}) < 3):
                ok = False
        if ok:
            addq(tuple(ts))
    queries = [(k, " + ".join(gen_desc(gen_specs[g]) for g in sorted(k)))
               for k, _ in queries]
    rhos = list(rhos_all(n, d))
    print(f"[V1] (7,3): {len(allp)} pairs, {len(gen_specs)} generators, "
          f"{len(queries)} queries x all {len(rhos)} restrictions")
    t0 = time.perf_counter()
    res = engineA_point3(n, d, DX3, gen_specs, queries, allp, rhos)
    print(f"[V1] Engine A pass done in {time.perf_counter() - t0:.1f} s")
    mism = 0
    for gensel, (desc, apost, _d1, _d0) in res.items():
        terms = tuple(gen_specs[g] for g in sorted(gensel))
        slots, bposts = concrete_engineB3(n, d, terms, 0)
        for p in slots:
            for a in (0, 1):
                if bposts[(a, p)] != apost[p][a]:
                    mism += 1
                    if mism <= 5:
                        print(f"     MISMATCH {desc} ans={a} c={p}: "
                              f"B={float(bposts[(a, p)]):.7f} "
                              f"A={float(apost[p][a]):.7f}")
    print(f"[V1] Engine B vs Engine A: {len(queries)} queries x 2 answers "
          f"x support roles: {mism} mismatches -> "
          f"{'PASS (digit-exact)' if mism == 0 else 'FAIL'}")
    print()

    # ================= V3: (15,3) sampled panel =========================
    n, d = 15, 3
    panel_pairs = [(i, j) for i in range(4) for j in range(5)]
    gen_specs = [('V', p) for p in panel_pairs] \
        + [('M', p, q) for (p, q) in diag_monos(panel_pairs)] \
        + [('T',) + t for t in match_triples(panel_pairs)]
    gpos = {g: k for k, g in enumerate(gen_specs)}
    m00, m11 = (0, 0), (1, 1)
    panel_terms = [
        [('V', m00)],
        [('M', m00, (2, 2))],
        [('T', m00, (2, 2), (3, 3))],
        [('M', m00, (2, 2)), ('M', m00, (2, 3))],
        [('M', m00, (2, 2)), ('M', m00, (2, 3)), ('M', m00, (3, 2))],
        [('T', m00, (2, 2), (3, 3)), ('T', m00, (2, 3), (3, 2))],
        [('T', m00, (2, 2), (3, 3)), ('M', m00, (2, 3))],
        [('T', m00, (2, 2), (3, 3)), ('M', m00, (2, 3)),
         ('M', m00, (3, 2))],
        [('T', m00, (2, 2), (3, 3)), ('T', m00, (2, 3), (3, 2)),
         ('T', m00, (2, 4), (3, 1))],
        [('M', m00, (2, 2)), ('M', (0, 1), (1, 3))],
        [('T', m00, (2, 2), (3, 3)), ('V', m11)],
        [('M', m00, (2, 2)), ('M', m11, (3, 3))],
    ]
    queries = []
    for terms in panel_terms:
        gensel = frozenset(gpos[t] for t in terms)
        desc = " + ".join(gen_desc(gen_specs[g]) for g in sorted(gensel))
        queries.append((gensel, desc))
    K = args.rhos15

    def sample_rho():
        c = n - 2 * d
        return (tuple(rng.sample(range(n + 1), c)),
                tuple(rng.sample(range(n), c)))

    print(f"[V3] (15,3): {len(queries)} panel queries x {K} sampled "
          f"restrictions (exact per-rho law)")
    t0 = time.perf_counter()
    res15 = engineA_point3(n, d, DX3, gen_specs, queries, panel_pairs,
                           (sample_rho() for _ in range(K)))
    print(f"[V3] Engine A pass done in {time.perf_counter() - t0:.1f} s")
    worst = 0.0
    bad = 0
    worst_d = ""
    for gensel, (desc, apost, den1, den0) in res15.items():
        terms = [gen_specs[g] for g in sorted(gensel)]
        slots, bposts = concrete_engineB3(n, d, terms, 0)
        for p in slots:
            for a in (0, 1):
                diff = abs(float(bposts[(a, p)]) - float(apost[p][a]))
                den = den1 if a == 1 else den0
                tol = 5 * 0.5 / math.sqrt(max(float(den), 1.0)) + 0.002
                if diff > tol:
                    bad += 1
                    if bad <= 5:
                        print(f"     V3 EXCEEDS {desc} ans={a} c={p}: "
                              f"B={float(bposts[(a, p)]):.4f} "
                              f"A={float(apost[p][a]):.4f} tol={tol:.4f}")
                if diff > worst:
                    worst = diff
                    worst_d = f"{desc} ans={a} c={p} (tol {tol:.4f})"
    print(f"[V3] worst |Engine B - Engine A| over the panel: {worst:.5f} "
          f"({bad} comparisons over tolerance, per-comparison 5-sigma "
          f"tolerance) -> {'PASS' if bad == 0 else 'FAIL'}  [{worst_d}]")
    print()

    # ================= V4: grid =========================================
    print("[V4] second full scan at (15,3)")
    best15, arg15, top15, _ = scan_point(15, 3, configs, keep=40)
    print(f"[V4] (15,3) MAX posterior = {float(best15):.6f} vs q3_cov = "
          f"{float(q3_cov(15, 3)):.6f} -> "
          f"{'EXCEEDED' if best15 > q3_cov(15, 3) else 'COVERED'}; "
          f"argmax {arg15[0]}")
    print()
    print("[V4] grid: winners + baselines vs q3_cov = "
          "max(q, q_and_exact, post3)")
    grid_cfgs = []
    seen_key = set()
    for loc, name, terms, geo in top7 + top15:
        if (terms, geo) not in seen_key:
            seen_key.add((terms, geo))
            grid_cfgs.append((name, terms, geo))
    baselines = [
        ("single", (single[0],), single[1]),
        ("diag", (diag[0],), diag[1]),
        ("triple", (tri[0],), tri[1]),
        ("shared-2M", (('M', 0, 1), ('M', 0, 2)),
         ((0, 0), (1, 1), (2, 2))),
        ("star-3M", (('M', 0, 1), ('M', 0, 2), ('M', 0, 3)),
         ((0, 0), (1, 1), (2, 2), (3, 3))),
        ("star-3T-disjoint", (('T', 0, 1, 2), ('T', 0, 3, 4),
                              ('T', 0, 5, 6)),
         ((0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6))),
    ]
    for (name, terms, geo) in baselines:
        if (terms, geo) not in seen_key:
            seen_key.add((terms, geo))
            grid_cfgs.insert(0, (name, terms, geo))
    grid = ([(7, 3), (8, 3), (9, 3), (15, 3), (31, 3), (63, 3), (127, 3),
             (255, 3), (1023, 3), (15, 4), (31, 4), (63, 4)]
            if not SMOKE else [(7, 3), (15, 3), (31, 3)])
    print(f"     {len(grid_cfgs)} configs on the grid; {len(grid)} points")
    print(f"     {'(n,d)':>9} {'q':>7} {'q_and_ex':>8} {'post3':>7} "
          f"{'q3_cov':>7} {'max mix':>8} {'excess':>10} {'max/post3':>9}"
          f"  argmax")
    worst_exc = Fraction(0)
    worst_at = None
    for (n, d) in grid:
        qc = q3_cov(n, d)
        best = Fraction(0)
        argd = ""
        for (name, terms, geo) in grid_cfgs:
            posts = posts_with_virtuals3(n, d, 0, terms, geo)
            loc = max(posts.values())
            if loc > best:
                best = loc
                am = max(posts, key=lambda k: posts[k])
                argd = f"{name} role {am[0]}"
        exc = best - qc
        if exc > worst_exc:
            worst_exc, worst_at = exc, (n, d, argd)
        p3 = post3_exact(n, d)
        capm._WP_CACHE.clear()
        print(f"     ({n:4d},{d}) {float(q_closed(n, d)):>7.4f} "
              f"{float(q_and_exact(n, d)):>8.4f} {float(p3):>7.4f} "
              f"{float(qc):>7.4f} {float(best):>8.4f} "
              f"{float(exc):>+10.6f} {float(best / p3):>9.6f}  {argd}")
    print(f"[V4] worst excess over the grid: {float(worst_exc):+.6f}"
          + (f" at {worst_at[0], worst_at[1]}: {worst_at[2]}" if worst_at
             else "")
          + " -> " + ("covered constant holds" if worst_exc <= 0
                      else "EXCEEDED (repaired constant q3*_mix needed)"))
    for (n, d) in [(15, 3), (31, 3)]:
        qc = q3_cov(n, d)
        best = Fraction(0)
        barg = None
        for (name, terms, geo) in grid_cfgs:
            posts = posts_with_virtuals3(n, d, 0, terms, geo)
            loc = max(posts.values())
            if loc > best:
                best = loc
                barg = name
        print(f"[V4] exact ({n},3): max - q3_cov = {best - qc} = "
              f"{float(best - qc):.3e}; max = {best} = {float(best):.6f} "
              f"[{barg}]; q3_cov = {qc} = {float(qc):.6f}")
    print()

    # ================= V6: mechanism tables at (15,3) ===================
    print("[V6] mechanism: per-output-status decomposition at (15,3)")
    n, d = 15, 3
    totW = count_rhos(n, d)
    mech_cfgs = [(name, terms, geo)
                 for loc, name, terms, geo in top15[:3]]
    mech_cfgs += [(b[0], b[1], b[2]) for b in baselines[3:]]
    mech_cfgs.append(("triple", (tri[0],), tri[1]))
    for (name, terms, geo) in mech_cfgs:
        table = table3(geo, terms, 0)
        agg = {sv: [0, 0] for sv in 'FMK'}
        for (assign, w2, frees) in table:
            W = weight_pattern(n, d, geo, assign)
            if not W:
                continue
            agg[assign[0]][0] += W
            agg[assign[0]][1] += W * w2
        lines = []
        for sv in 'FMK':
            w0, w1 = agg[sv]
            lines.append(f"{sv}: P={float(Fraction(w0, totW)):.6f} "
                         f"P(ans=1&s0)={float(Fraction(w1, 2 * totW)):.6f}")
        okK = agg['K'][1] == 0
        print(f"[V6] {name}: " + " | ".join(lines)
              + f"  killed-branch ans-1 mass = {agg['K'][1]} "
              f"({'SELF-EXCLUDED' if okK else 'NOT excluded'})")
    print()

    # ================= V5: budgeted strategies ==========================
    print("[V5] budgeted adaptive strategies (exact channel); certified")
    print("     outputs asserted free; budget counts query evaluations")

    def fam_mmm(ab, ps):
        return [('M', ab, ps[i]) for i in range(3)]

    def fam_ttt(ab, ps):
        return [('T', ab, ps[0], ps[1]), ('T', ab, ps[2], ps[3]),
                ('T', ab, ps[4], ps[5])]

    for (n, d, sims) in ([(7, 3, 150 if SMOKE else 4000),
                          (15, 3, 100 if SMOKE else 1500)]):
        allp = [(i, j) for i in range(n + 1) for j in range(n)]
        tri_all = match_triples(allp)
        rng_t = random.Random(4242 + n)
        rng_t.shuffle(tri_all)
        tri_all = tri_all[:6000]
        # Lemma S3 wedge attempts: two triples carrying the same pigeon in
        # DISTINCT hole cells, all other cells disjoint (pigeons and holes)
        wedge_list = []
        for p in range(n + 1):
            others_p = [i for i in range(n + 1) if i != p]
            for j1 in range(n):
                for j2 in range(n):
                    if j1 >= j2:
                        continue
                    holes_left = [h for h in range(n) if h not in (j1, j2)]
                    if len(others_p) < 4 or len(holes_left) < 4:
                        continue
                    for t in range(6):
                        ps = rng_t.sample(others_p, 4)
                        hs = rng_t.sample(holes_left, 4)
                        t1 = ((p, j1), (ps[0], hs[0]), (ps[1], hs[1]))
                        t2 = ((p, j2), (ps[2], hs[2]), (ps[3], hs[3]))
                        wedge_list.append((t1, t2, p))
        rng_t.shuffle(wedge_list)
        names = ["single_scan", "kj_budget", "kj_direct", "triple_scan",
                 "mix3_mmm", "mix3_ttt", "mixz3", "wedge3", "hybrid3"]
        print(f"  (n,d) = ({n},{d}): q = {float(q_closed(n, d)):.4f}, "
              f"q_and_exact = {float(q_and_exact(n, d)):.4f}, "
              f"post3 = {float(post3_exact(n, d)):.4f}, sims = {sims}")
        for budget in (10, 30, 100):
            acc = {s: 0 for s in names}
            viol = [0]
            s2 = random.Random(777 + budget + n)
            s3 = random.Random(555 + budget)
            samp = Sampler3(n, d, DX3, s2)
            for _ in range(sims):
                ans_q, free, ans_K = samp.config()
                order = allp[:]
                s3.shuffle(order)
                tris = tri_all[:]
                s3.shuffle(tris)
                oj = list(range(n))
                s3.shuffle(oj)

                def partners_of(ab):
                    (a, b) = ab
                    pi = [i for i in range(n + 1) if i != a][:6]
                    hi = [j for j in range(n) if j != b][:6]
                    return [(pi[t], hi[t]) for t in range(6)]

                acc["single_scan"] += free(strat_single(ans_q, free, n,
                                                        budget, order))
                acc["kj_budget"] += free(strat_kj(ans_q, free, n, budget))
                acc["kj_direct"] += free(strat_kj_direct(ans_q, free,
                                                         ans_K, n, budget,
                                                         oj))
                acc["triple_scan"] += free(strat_triplescan(ans_q, free, n,
                                                            budget, tris))
                acc["mix3_mmm"] += free(strat_mix3(ans_q, free, n, budget,
                                                   order, partners_of,
                                                   fam_mmm))
                acc["mix3_ttt"] += free(strat_mix3(ans_q, free, n, budget,
                                                   order, partners_of,
                                                   fam_ttt))
                acc["mixz3"] += free(strat_mixz3(ans_q, free, n, budget,
                                                 tris, viol))
                acc["wedge3"] += free(strat_wedge3(ans_q, free, n, budget,
                                                   wedge_list, viol))
                acc["hybrid3"] += free(strat_hybrid3(ans_q, free, n, budget,
                                                     order, tris))
            print("    budget %3d: " % budget
                  + "  ".join(f"{s}={acc[s] / sims:.4f}" for s in names))
        if viol[0]:
            print(f"    SOUNDNESS VIOLATIONS (certified output not free): "
                  f"{viol[0]}")
        else:
            print("    soundness: every certified output was free "
                  "(0 violations)")
    print()
    print("[verdict] summary lines above; full reading in docs/mixture3.md")


if __name__ == "__main__":
    main()
