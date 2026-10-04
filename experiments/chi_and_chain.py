"""Adaptive AND-chaining vs the per-query posterior cap at p = 2 (Open Problem O1 probe).

Question. At the Omega(n,d) pipeline (p = 2), single-variable queries and degree-2 AND
(conjunction) queries have the same per-hit labeling posterior q = (f/2)/(f/2+m)
(no lift, proved for the single pass). Can ADAPTIVE CHAINING of many AND-queries
(conditioning later queries on earlier answers) beat the per-query posterior cap and
approach the two-phase certification tree's success 1 - 2^{-(2d+1)}?

Strategies compared at equal query budgets:
  (a) single     : single-variable scan; first answer-1 pair is labeled (baseline);
  (b) two-phase  : Q_i row-sum certification (1 query per pigeon) + row scan; on failure
                   the remaining budget runs a single scan (strongest fair version);
  (c) and-scan   : AND-pair scan (2 fresh variable reads per test; first both-1 hit
                   labels one component uniformly) - the budget-honest version of
                   chi_and_vs_single.py's (b);
  (d) and-pool   : AND-pair reads over the whole budget; every answer-1 pair enters a
                   pool; one pool member is picked uniformly at the end;
  (e) confirm    : hit-confirm-certify chain: single scan; on a hit at (i,j) spend up to
                   k=6 reads on fresh row/column neighbors; any neighbor answering 1
                   CERTIFIES the hit pair free (status combinatorics: a matched (i,j)
                   forces its whole row and column to answer 0), so the neighbor is
                   output as a certain-free pair; otherwise resume scanning; at budget
                   end the least-confirmed hit is output;
  (f) weighted   : adjacency-prioritized scan (posterior-weighted sampling): after a
                   hit, its unread row/column neighbors enter a hot list that future
                   reads draw from with prob 0.7; all 1s pool; uniform pool output;
  (g) and-split  : hierarchical AND-tree: AND-pair test; on a hit, probe up to 3
                   neighbors of each component (group, AND-refine, split); certify on a
                   neighbor-1, else resume; end: uniform over all 1s seen;
  (h) mono2      : TRUE degree-2 monomial queries (exact pipeline only): one query per
                   mixed (distinct pigeon and hole) pair-pair, answer L((x_ab x_cd)^rho);
                   first answer-1 labels one component uniformly.

Query accounting: every polynomial queried costs 1 (Q_i costs 1; a degree-2 monomial
costs 1; an AND-conjunction of two variables costs the 2 variable reads it needs).

Two answer channels:
  iid   : the corpus-standard channel (chi_o1_scaling.py, chi_two_phase.py): free pair
          -> memoized fair bit per pair; killed-matched -> 1; killed-unmatched -> 0.
          This is the stipulated channel of the task and the only feasible one at
          (64,4) (the exact design space at canon (8,4) has ~1.3M monomials).
  exact : the true Omega(32,2) GF(2) pipeline: designs sampled uniformly from
          Des(4,2) = {L : L kills every V(4,2) generator, L(1) = 1} via a particular
          solution + null space (assertion-verified against all generator rows).
          Known facts (measured, see calibrate_exact output): designs kill Q_i, so
          L(Q_i^rho) = 0 DETERMINED on free pigeons (the two-phase phase-1 signal does
          not exist on the true pipeline); same-row / same-hole degree-2 coordinates are
          determined 0; mixed degree-2 coordinates are fair and INDEPENDENT of the two
          component degree-1 bits (P[coord = b1*b2] ~ 1/2, not 1).

Measured per cell: success probability (output pair is free) with Wilson 99% CI,
P[>=1 answer-1], hit rate per query, labeling posterior among hit-derived outputs,
certified-output rate, and the posterior among certified outputs (asserted == 1:
a cert output is provably free under the status combinatorics).

Why chaining CAN in principle beat the plain AND no-lift (structural note): the proved
no-lift labels ONE OF THE AND'S OWN TWO COMPONENTS, and for independent random pairs the
matched-matched case (both components matched, answer determined 1) carries ~54% of the
answer-1 mass at (32,2) while contributing zero freeness. For ADJACENT pairs (sharing a
row or column) matched-matched is IMPOSSIBLE: if (i,j) is matched then every neighbor
answers 0 determinedly, so (hit at p AND 1 at a neighbor of p) certifies BOTH pairs free.
The confirm / and-split strategies test exactly this adjacency-conditioned event; the
open question is whether the scan can find such events often enough within budget.
"""
from __future__ import annotations

import argparse
import math
import random
import statistics

from razborov_check import monomials, system_polys, shift, to_vec

CANON_N = 4  # restricted system at d=2: 5 pigeons, 4 holes
DEG = 2
BUDGETS = (30, 100, 300, 1000)
K_CONFIRM = 6
K_SPLIT = 3
P_HOT = 0.7


# ---------------------------------------------------------------------------
# exact GF(2) design space at canon (4,2)
# ---------------------------------------------------------------------------

def build_true_designs():
    """Uniform sampler pieces for Des(4,2): particular L + null basis, verified."""
    monos = monomials(CANON_N, DEG)
    mono_index = {t: i for i, t in enumerate(monos)}
    nm = len(monos)
    gens = []
    for f in system_polys(CANON_N):
        df = max(len(t) for t in f)
        for mono in monos:
            if len(mono) + df <= DEG:
                gens.append(to_vec(shift(f, mono), mono_index))
    rows = [(g, 0) for g in gens] + [(1 << mono_index[tuple()], 1)]
    ech: dict[int, tuple[int, int]] = {}
    for m, r in rows:
        while m:
            h = m.bit_length() - 1
            if h in ech:
                pm, pr = ech[h]
                m ^= pm
                r ^= pr
            else:
                ech[h] = (m, r)
                break
        if m == 0 and r == 1:
            raise RuntimeError("inconsistent design system: 1 in V(4,2)")
    pivot_cols = sorted(ech)
    Lp = 0
    for c in pivot_cols:
        row, rhs = ech[c]
        mask = row ^ (1 << c)
        if rhs ^ (bin(Lp & mask).count("1") & 1):
            Lp |= 1 << c
    null_basis = []
    for fc in range(nm):
        if fc in ech:
            continue
        y = 1 << fc
        for c in pivot_cols:
            row, _ = ech[c]
            mask = row ^ (1 << c)
            if bin(y & mask).count("1") & 1:
                y ^= 1 << c
        null_basis.append(y)
    # verification: Lp kills every generator, Lp(1)=1; null vectors kill generators
    assert (Lp >> mono_index[tuple()]) & 1 == 1
    for g in gens:
        assert bin(Lp & g).count("1") % 2 == 0
    for y in null_basis:
        assert (y >> mono_index[tuple()]) & 1 == 0
        for g in gens:
            assert bin(y & g).count("1") % 2 == 0
    assert len(null_basis) == 65  # dim Des(4,2), matches razborov_check's table
    return Lp, null_basis, mono_index


_DESIGNS_CACHE = None


def get_designs():
    global _DESIGNS_CACHE
    if _DESIGNS_CACHE is None:
        _DESIGNS_CACHE = build_true_designs()
    return _DESIGNS_CACHE


# ---------------------------------------------------------------------------
# instances
# ---------------------------------------------------------------------------

class Instance:
    """Answer channel: free -> memoized fair bit, matched -> 1, killed-unmatched -> 0.

    Query accounting: var() and qrow() and (exact) mono2() each cost 1 query. A Q_i
    query does NOT reveal individual x_ij values (no used-marking of row entries); a
    degree-2 monomial query does not reveal its components.
    """

    def __init__(self, n: int, d: int, rng: random.Random):
        self.n = n
        self.d = d
        assigned_p = rng.sample(range(n + 1), n - 2 * d)
        assigned_h = rng.sample(range(n), n - 2 * d)
        self.rho = dict(zip(assigned_p, assigned_h))
        self.rho_inv = {j: i for i, j in self.rho.items()}
        self.D = set(range(n + 1)) - set(assigned_p)
        self.R = set(range(n)) - set(assigned_h)
        self.free_set = {(i, j) for i in self.D for j in self.R}
        self.pairs = [(i, j) for i in range(n + 1) for j in range(n)]
        self._order = self.pairs[:]
        rng.shuffle(self._order)
        self._ptr = 0
        self._used: set[tuple[int, int]] = set()
        self._bits: dict[tuple[int, int], int] = {}

    def is_free(self, pair) -> bool:
        return pair in self.free_set

    def is_used(self, pair) -> bool:
        return pair in self._used

    def fresh(self):
        while self._ptr < len(self._order):
            p = self._order[self._ptr]
            self._ptr += 1
            if p not in self._used:
                return p
        return None

    def _bit(self, pair: tuple[int, int]) -> int:
        if pair in self._bits:
            return self._bits[pair]
        (i, j) = pair
        if i in self.rho:
            a = 1 if self.rho[i] == j else 0
        elif j in self.rho_inv:
            a = 0
        else:
            a = self._free_bit(pair)
        self._bits[pair] = a
        return a

    def var(self, pair: tuple[int, int]) -> int:
        self._used.add(pair)
        return self._bit(pair)

    def qrow(self, i: int) -> int:
        """One degree-1 query: answer to Q_i = 1 + sum_j x_ij (char 2)."""
        if i in self.rho:
            return 0
        x = 0
        for j in range(self.n):
            x ^= self._bit((i, j))
        return (1 + x) & 1

    def xorrow(self, i: int) -> int:
        """One degree-1 query: answer to sum_j x_ij (row sum WITHOUT the constant).

        On an assigned pigeon this is the determined 1 (the matched entry); on a free
        pigeon it is the row XOR of the free-pair bits. This is the polynomial that
        chi_two_phase.py's certification (`sum(row_bits) % 2 == 1`) actually queries.
        """
        if i in self.rho:
            return 1
        x = 0
        for j in range(self.n):
            x ^= self._bit((i, j))
        return x

    def neighbors(self, pair):
        (i, j) = pair
        return [(i, j2) for j2 in range(self.n) if j2 != j] + \
               [(i2, j) for i2 in range(self.n + 1) if i2 != i]

    def unused_neighbors(self, pair):
        return [p for p in self.neighbors(pair) if p not in self._used]

    def random_pair(self, rng):
        return rng.choice(self.pairs)

    def _free_bit(self, pair) -> int:  # overridden
        raise NotImplementedError


class IIDInstance(Instance):
    def __init__(self, n, d, rng):
        super().__init__(n, d, rng)
        self._rng = rng

    def _free_bit(self, pair) -> int:
        return self._rng.randrange(2)


class ExactInstance(Instance):
    """True Omega(32,2): uniform design over Des(4,2); degree-2 coordinates available."""

    def __init__(self, n, d, rng):
        super().__init__(n, d, rng)
        assert (n, d) == (32, 2)
        Lp, null_basis, mono_index = get_designs()
        L = Lp
        for k in null_basis:
            if rng.random() < 0.5:
                L ^= k
        self.L = L
        self.mono_index = mono_index
        # canon variable index of each free outer pair; degree-1 monomial (v,) sits at
        # monomial position 1 + v (constant monomial first)
        self.varidx: dict[tuple[int, int], int] = {}
        for pi_, i in enumerate(sorted(self.D)):
            for hj_, j in enumerate(sorted(self.R)):
                self.varidx[(i, j)] = pi_ * CANON_N + hj_
        self._mono2_cache: dict[tuple[int, int], int] = {}

    def _free_bit(self, pair) -> int:
        return (self.L >> self.mono_index[(self.varidx[pair],)]) & 1

    def _status(self, pair: tuple[int, int]) -> int:
        (i, j) = pair
        if i in self.rho:
            return 1 if self.rho[i] == j else 2  # 1 = matched, 2 = killed-unmatched
        if j in self.rho_inv:
            return 2
        return 0  # free

    def mono2(self, pa, pb) -> int:
        """One degree-2 query: answer to (x_pa * x_cd)^rho = x_pa^rho * x_cd^rho."""
        s1 = self._status(pa)
        s2 = self._status(pb)
        if s1 == 2 or s2 == 2:
            return 0  # a killed-unmatched factor restricts to 0
        if s1 == 1 and s2 == 1:
            return 1  # both matched: restricted product is the constant 1
        if s1 == 1:
            return self._bit(pb)  # restriction collapses to the degree-1 variable
        if s2 == 1:
            return self._bit(pa)
        v1 = self.varidx[pa]
        v2 = self.varidx[pb]
        key = (min(v1, v2), max(v1, v2))
        if key not in self._mono2_cache:
            self._mono2_cache[key] = (self.L >> self.mono_index[key]) & 1
        return self._mono2_cache[key]  # both free: mixed degree-2 design coordinate


# ---------------------------------------------------------------------------
# strategies: return (out_pair, src, queries, hits, certs); src in {cert,hit,fallback}
# ---------------------------------------------------------------------------

def strat_single(inst, rng, B):
    q = hits = 0
    while q < B:
        p = inst.fresh()
        if p is None:
            break
        a = inst.var(p)
        q += 1
        hits += a
        if a:
            return p, "hit", q, hits, 0
    return inst.random_pair(rng), "fallback", q, hits, 0


def strat_two_phase(inst, rng, B, xor_variant=False):
    q = hits = certs = 0
    pigeons = list(range(inst.n + 1))
    rng.shuffle(pigeons)
    star = None
    for i in pigeons:
        if q >= B:
            break
        a = inst.xorrow(i) if xor_variant else inst.qrow(i)
        q += 1
        hits += a
        if a:
            star = i
            break
    if star is not None:
        holes = list(range(inst.n))
        rng.shuffle(holes)
        for j in holes:
            if q >= B:
                break
            a = inst.var((star, j))
            q += 1
            hits += a
            if a:
                return (star, j), "cert", q, hits, 1
    while q < B:  # single-scan continuation on remaining budget
        p = inst.fresh()
        if p is None:
            break
        a = inst.var(p)
        q += 1
        hits += a
        if a:
            return p, "hit", q, hits, certs
    return inst.random_pair(rng), "fallback", q, hits, certs


def strat_and_scan(inst, rng, B):
    q = hits = 0
    while q + 2 <= B:
        pa = inst.fresh()
        pb = inst.fresh()
        if pa is None or pb is None:
            break
        va = inst.var(pa)
        vb = inst.var(pb)
        q += 2
        hits += va + vb
        if va and vb:
            return rng.choice([pa, pb]), "hit", q, hits, 0
    return inst.random_pair(rng), "fallback", q, hits, 0


def strat_and_pool(inst, rng, B):
    q = hits = 0
    pool = []
    while q + 2 <= B:
        pa = inst.fresh()
        pb = inst.fresh()
        if pa is None or pb is None:
            break
        va = inst.var(pa)
        vb = inst.var(pb)
        q += 2
        hits += va + vb
        if va:
            pool.append(pa)
        if vb:
            pool.append(pb)
    if pool:
        return rng.choice(pool), "hit", q, hits, 0
    return inst.random_pair(rng), "fallback", q, hits, 0


def strat_confirm(inst, rng, B, k=K_CONFIRM):
    q = hits = certs = 0
    uncertified = []
    while q < B:
        p = inst.fresh()
        if p is None:
            break
        a = inst.var(p)
        q += 1
        hits += a
        if a:
            fired = None
            nconf = 0
            cands = inst.unused_neighbors(p)
            rng.shuffle(cands)
            for nb in cands[:k]:
                if q >= B:
                    break
                aa = inst.var(nb)
                q += 1
                hits += aa
                if aa:
                    fired = nb
                    break
                nconf += 1
            if fired is not None:
                return fired, "cert", q, hits, 1
            uncertified.append((p, nconf))
    if uncertified:
        best = min(range(len(uncertified)), key=lambda t: (uncertified[t][1], -t))
        return uncertified[best][0], "hit", q, hits, certs
    return inst.random_pair(rng), "fallback", q, hits, certs


def strat_weighted(inst, rng, B, p_hot=P_HOT):
    q = hits = 0
    pool = []
    hot = []

    def draw():
        while hot:
            idx = rng.randrange(len(hot))
            p = hot[idx]
            hot[idx] = hot[-1]
            hot.pop()
            if not inst.is_used(p):
                return p
        return inst.fresh()

    while q < B:
        if hot and rng.random() < p_hot:
            p = draw()
        else:
            p = inst.fresh()
            if p is None:
                p = draw()
        if p is None:
            break
        a = inst.var(p)
        q += 1
        hits += a
        if a:
            pool.append(p)
            hot.extend(inst.unused_neighbors(p))
    if pool:
        return rng.choice(pool), "hit", q, hits, 0
    return inst.random_pair(rng), "fallback", q, hits, 0


def strat_and_split(inst, rng, B, k=K_SPLIT):
    q = hits = certs = 0
    pool = []
    while q + 2 <= B:
        pa = inst.fresh()
        pb = inst.fresh()
        if pa is None or pb is None:
            break
        va = inst.var(pa)
        vb = inst.var(pb)
        q += 2
        hits += va + vb
        if va:
            pool.append(pa)
        if vb:
            pool.append(pb)
        if va and vb:
            fired = None
            for x in rng.sample([pa, pb], 2):
                cands = inst.unused_neighbors(x)
                rng.shuffle(cands)
                for nb in cands[:k]:
                    if q >= B:
                        break
                    aa = inst.var(nb)
                    q += 1
                    hits += aa
                    if aa:
                        fired = nb
                        break
                if fired is not None:
                    return fired, "cert", q, hits, 1
    if pool:
        return rng.choice(pool), "hit", q, hits, certs
    return inst.random_pair(rng), "fallback", q, hits, certs


def strat_mono2(inst, rng, B):
    """True degree-2 monomial scan (exact pipeline only): 1 query per pair-pair."""
    q = hits = 0
    seen = set()
    while q < B:
        pa = inst.random_pair(rng)
        pb = inst.random_pair(rng)
        if pa == pb:
            continue
        key = (min(pa, pb), max(pa, pb))
        if key in seen:
            continue
        seen.add(key)
        a2 = inst.mono2(pa, pb)
        q += 1
        hits += a2
        if a2:
            return rng.choice([pa, pb]), "hit", q, hits, 0
    return inst.random_pair(rng), "fallback", q, hits, 0


STRATEGIES = {
    "single": strat_single,
    "two-phase": strat_two_phase,
    "and-scan": strat_and_scan,
    "and-pool": strat_and_pool,
    "confirm": strat_confirm,
    "weighted": strat_weighted,
    "and-split": strat_and_split,
    "mono2": strat_mono2,
}


# ---------------------------------------------------------------------------
# stats and reporting
# ---------------------------------------------------------------------------

def wilson(p: float, n: int, z: float = 2.5758293035489004):
    if n == 0:
        return (0.0, 1.0)
    den = 1 + z * z / n
    ctr = (p + z * z / (2 * n)) / den
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return (max(0.0, ctr - half), min(1.0, ctr + half))


def run_cell(n, d, chan, B, name, n_sim, rng):
    succ = []
    n_hit_sims = n_hitsrc = hit_free = n_post = post_free = n_cert = cert_free = 0
    tot_q = tot_hits = 0
    for _ in range(n_sim):
        if chan == "exact":
            inst = ExactInstance(n, d, rng)
        else:
            inst = IIDInstance(n, d, rng)
        out, src, q, hits, certs = STRATEGIES[name](inst, rng, B)
        s = 1.0 if inst.is_free(out) else 0.0
        if src == "cert":
            # simulator self-check: a certified output is provably free (matched pairs
            # force all neighbors to 0, so hit+neighbor-1 excludes matched and killed)
            assert s == 1.0, f"{name}: cert output not free - channel/strategy bug"
        succ.append(s)
        n_hit_sims += 1 if hits > 0 else 0
        if src == "hit":
            n_hitsrc += 1
            hit_free += s
        if src != "fallback":
            n_post += 1
            post_free += s
        if src == "cert":
            n_cert += 1
            cert_free += s
        tot_q += q
        tot_hits += hits
    m = statistics.mean(succ)
    lo, hi = wilson(m, n_sim)
    ph = hit_free / max(1, n_hitsrc)
    ph_lo, ph_hi = wilson(ph, n_hitsrc)
    return {
        "success": m, "lo": lo, "hi": hi,
        "p_hit": n_hit_sims / n_sim,
        "hit_rate": tot_hits / max(1, tot_q),
        "post": post_free / max(1, n_post),
        "n_hitsrc": n_hitsrc, "post_hit": ph, "post_hit_lo": ph_lo, "post_hit_hi": ph_hi,
        "cert_rate": n_cert / n_sim,
        "post_cert": cert_free / max(1, n_cert),
    }


def theory(n, d):
    f = (2 * d + 1) * 2 * d / ((n + 1) * n)
    m = (n - 2 * d) / ((n + 1) * n)
    q = (f / 2) / (f / 2 + m)
    return f, m, q


# ---------------------------------------------------------------------------
# calibration probes on the exact pipeline
# ---------------------------------------------------------------------------

def calibrate_exact(n_cal=400, seed=5150):
    rng = random.Random(seed)
    Lp, null_basis, mono_index = get_designs()
    d1 = [0, 0]
    row_xor = [0, 0]
    qval = [0, 0]
    sr = [0, 0]
    sh = [0, 0]
    mixed = [0, 0]
    prod_match = 0
    ff_11 = [0, 0]
    canon_pairs = [(p, h) for p in range(CANON_N + 1) for h in range(CANON_N)]
    for _ in range(n_cal):
        L = Lp
        for k in null_basis:
            if rng.random() < 0.5:
                L ^= k
        for p in range(CANON_N + 1):
            x = 0
            for h in range(CANON_N):
                x ^= (L >> mono_index[(p * CANON_N + h,)]) & 1
                d1[(L >> mono_index[(p * CANON_N + h,)]) & 1] += 1
            row_xor[x] += 1
            qval[1 ^ x] += 1
        for p in range(CANON_N + 1):
            for h1 in range(CANON_N):
                for h2 in range(h1 + 1, CANON_N):
                    t = tuple(sorted((p * CANON_N + h1, p * CANON_N + h2)))
                    sr[(L >> mono_index[t]) & 1] += 1
        for h in range(CANON_N):
            for p1 in range(CANON_N + 1):
                for p2 in range(p1 + 1, CANON_N + 1):
                    t = tuple(sorted((p1 * CANON_N + h, p2 * CANON_N + h)))
                    sh[(L >> mono_index[t]) & 1] += 1
        for _ in range(30):
            (pa, pb) = rng.sample(canon_pairs, 2)
            if pa[0] == pb[0] or pa[1] == pb[1]:
                continue
            va = (L >> mono_index[(pa[0] * CANON_N + pa[1],)]) & 1
            vb = (L >> mono_index[(pb[0] * CANON_N + pb[1],)]) & 1
            t = tuple(sorted((pa[0] * CANON_N + pa[1], pb[0] * CANON_N + pb[1])))
            c = (L >> mono_index[t]) & 1
            mixed[c] += 1
            prod_match += int(c == (va & vb))
            if va == 1 and vb == 1:
                ff_11[c] += 1
    print("channel calibration, exact Omega(32,2) pipeline (uniform designs over"
          f" Des(4,2), {n_cal} samples):")
    print(f"  free degree-1 canon coords: P[=1] = {d1[1] / max(1, d1[0] + d1[1]):.4f}"
          f" (n={d1[0] + d1[1]}; the stipulated channel assumes 0.5)")
    print(f"  row XOR of free-row degree-1 bits: 0 -> {row_xor[0]}, 1 -> {row_xor[1]}"
          "   (design kills Q_i, so XOR = 1 forced)")
    print(f"  L(Q_i^rho) for a free pigeon (two-phase phase-1 answer):"
          f" 0 -> {qval[0]}, 1 -> {qval[1]}   (determined)")
    print(f"  same-row degree-2 coords:  0 -> {sr[0]}, 1 -> {sr[1]}   (determined)")
    print(f"  same-hole degree-2 coords: 0 -> {sh[0]}, 1 -> {sh[1]}   (determined)")
    print(f"  mixed degree-2 coords: P[=1] = {mixed[1] / max(1, mixed[0] + mixed[1]):.4f},"
          f" P[coord = b1*b2] = {prod_match / max(1, mixed[0] + mixed[1]):.4f}")
    n11 = ff_11[0] + ff_11[1]
    print(f"  P[coord=1 | both component bits = 1] = {ff_11[1] / max(1, n11):.4f}"
          f" (n={n11}; conjunction semantics would force this to be 1.0)")


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------

def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--sims", type=int, default=600)
    ap.add_argument("--seed", type=int, default=20261003)
    ap.add_argument("--quick", action="store_true")
    args = ap.parse_args()
    n_sim = 120 if args.quick else args.sims
    budgets = (30, 1000) if args.quick else BUDGETS
    names = [s for s in STRATEGIES if s != "mono2"]

    calibrate_exact()

    for (n, d) in ((32, 2), (64, 4)):
        f, m, q = theory(n, d)
        print()
        print(f"== (n={n}, d={d}): f = {f:.5f}, m = {m:.5f}, per-hit posterior cap"
              f" q = {q:.4f}, two-phase iid-model error 2^-(2d+1) ="
              f" {2.0 ** -(2 * d + 1):.5f}")
        for chan in ("iid", "exact"):
            if chan == "exact" and (n, d) != (32, 2):
                continue
            print(f"  channel: {chan}"
                  + ("  (true Omega pipeline)" if chan == "exact"
                     else "  (corpus-standard memoized-bit channel)"))
            for B in budgets:
                print(f"  budget B = {B}")
                print(f"    {'strategy':<10} {'success':>7} {'99% CI':>18} {'P(hit)':>7}"
                      f" {'hits/q':>8} {'post|hit':>8} {'[ci]':>13} {'cert%':>6}"
                      f" {'post|cert':>9}")
                for name in names + (["mono2"] if chan == "exact" else []):
                    rng = random.Random(f"{args.seed}|{n}|{d}|{chan}|{B}|{name}")
                    r = run_cell(n, d, chan, B, name, n_sim, rng)
                    print(f"    {name:<10} {r['success']:>7.4f}   [{r['lo']:.4f},"
                          f"{r['hi']:.4f}] {r['p_hit']:>7.4f} {r['hit_rate']:>8.5f}"
                          f" {r['post_hit']:>8.4f} [{r['post_hit_lo']:.4f},"
                          f"{r['post_hit_hi']:.4f}] {100 * r['cert_rate']:>6.2f}"
                          f" {r['post_cert']:>9.4f}")


if __name__ == "__main__":
    main()
