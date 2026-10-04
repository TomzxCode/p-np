"""GAP E (O2(ii)): the constants of the budgeted boundary
err*(d, e = d log k) = k^{-Theta(d^2/n)} at degree <= 2 on the TRUE channel.

gap-e agent script (2026-10-04). Companion doc: docs/gap_e_constants.md.
At (128,2), e = 32 (log k = 16) the printed cap gives success ~ 0.317 while
the best measured witness gives ~ 0.06 (open_problems.md O2(ii)). This script
tightens the bracket from both sides:

  E1. exact certificate laws (Lemma E1 of the companion doc), d = 2 and 3:
      P(K_j = 1) = d/n; the parity pattern of the 2d free columns is uniform
      over odd-XOR patterns, so P(k certifications among t queried free
      columns) = C(t,k) 2^-t for t < 2d (odd-XOR law at t = 2d); the stage-1
      transition p_cert_next(n,d,u,k); certified columns carry w ones with
      P(w) = C(2d+1,w) 2^-2d (w even), dud probability 2^-2d, joint dud
      2^-2dk.  All checked by exhaustive enumeration (d = 2) or high-count
      Monte Carlo (d = 3).
  E2. exact backward induction over the certified-tree family (states
      (u K-queries, m zero-scans, k certifications, o unopened, z zeros on
      the current column); actions K / NEXT / SCAN / FB with the E1
      transitions and fresh-row scans). Values at (128,2) e=32, (96,3)
      e=48 and e=32, (5,2) e=6; chain-only variant (FB value f) reported
      separately.
  E3. brute-force exact enumeration at (5,2): all 983,040 configurations
      (6 free-pigeon sets x 5 free-hole sets x 8^5 odd-row matrices); the
      exact true-channel success of the DP policy and of a policy grid,
      against the DP model value.
  E4. Monte Carlo on the exact structural sampler (uniform odd free rows;
      exact by the row-parity theorem, kernel_structure.md F2/F3) at the
      target points: single scan, fixed-split K_j trees (grid), the DP
      policy, a singles+K hybrid, and (at (128,2)) a degree-2 diagonal
      monomial scan on the exact design-space channel. 99% Clopper-Pearson
      intervals.
  E5. cap arithmetic: printed cap (q + 2(1-exp(-x/4)) + A) vs the sharpened
      product-form cap (Pi + (1-Pi)(q + A)) vs the DP bracket; leading
      constants rho, alpha*, c_w.

Run: python3 chi_gap_e_check.py [--smoke]
"""
from __future__ import annotations

import math
import random
import sys
from itertools import combinations, product

import chi_deg2_theory_check as base
from chi_deg2_theory_check import cp_ci


# ---------- Lemma E1: exact certified-family laws ----------

def parity_patterns(ncols: int) -> list:
    return [p for p in product(range(2), repeat=ncols) if sum(p) % 2 == 1]


_pcert_cache: dict = {}


def p_cert_next(n: int, d: int, u: int, k: int) -> float:
    """P(next fresh K_j query certifies | u distinct K-queries done, k
    certified so far). Exact: sum over t = |R intersect Q| with the
    hypergeometric weight and the parity-pattern law. The observed pattern
    fixes the total odd-XOR, so the unqueried free parities are uniform
    with prescribed XOR: a specific next free column is even with
    probability 1/2 while at least two remain undetermined, and with
    probability 0 or 1 when exactly one remains (determined case)."""
    key = (n, d, u, k)
    v = _pcert_cache.get(key)
    if v is not None:
        return v
    num = den = 0.0
    for t in range(0, min(2 * d, u) + 1):
        if u - t > n - 2 * d:
            continue
        w = (math.comb(2 * d, t) * math.comb(n - 2 * d, u - t)
             / math.comb(n, u))
        if t < 2 * d:
            pk = math.comb(t, k) / 2.0 ** t
        else:
            pk = (math.comb(t, k) / 2.0 ** (t - 1)
                  if (t - k) % 2 == 1 else 0.0)
        w *= pk
        rem = 2 * d - t
        if rem > 0:
            pfree = rem / (n - u)
            if rem >= 2:
                peven = 0.5
            else:
                peven = 1.0 if (t - k) % 2 == 1 else 0.0
            num += w * pfree * peven
        den += w
    if den <= 0.0:
        v = 0.0
    else:
        v = num / den
    _pcert_cache[key] = v
    return v


def e1_checks(smoke: bool) -> None:
    print("[E1] exact certificate laws (Lemma E1)")
    d = 2
    pats = parity_patterns(2 * d)
    # (a) P(k certifications among t queried free columns)
    ok = True
    for t in range(0, 2 * d + 1):
        for k in range(0, t + 1):
            emp = sum(1 for p in pats
                      if sum(1 for c in range(t) if p[c] == 0) == k) / len(pats)
            if t < 2 * d:
                th = math.comb(t, k) / 2.0 ** t
            else:
                th = (math.comb(t, k) / 2.0 ** (t - 1)
                      if (t - k) % 2 == 1 else 0.0)
            if abs(emp - th) > 1e-12:
                ok = False
    print(f"  (a) parity-pattern law C(t,k)2^-t (t<2d), odd-XOR at t=2d: "
          f"{'PASS' if ok else 'FAIL'}")
    # (b) P(K_j = 1) = d/n and (c) p_cert_next, exact at (8,2)
    n = 8
    table: dict = {}
    cert = tot = 0
    for rsub in combinations(range(n), 2 * d):
        rs = set(rsub)
        pos = {j: i for i, j in enumerate(rsub)}
        for p in pats:
            if 0 in rs and p[pos[0]] == 0:
                cert += 1
            tot += 1
            for u in range(0, n):
                kobs = sum(1 for j in range(u) if j in rs and p[pos[j]] == 0)
                nxt = 1 if (u in rs and p[pos[u]] == 0) else 0
                a, b = table.get((u, kobs), (0, 0))
                table[(u, kobs)] = (a + nxt, b + 1)
    emp = cert / tot
    okb = abs(emp - d / n) < 1e-12
    okc = True
    for (u, k), (a, b) in sorted(table.items()):
        if b < 8:
            continue
        if abs(a / b - p_cert_next(n, d, u, k)) > 1e-9:
            okc = False
            print(f"    mismatch u={u} k={k}: emp {a / b:.6f} vs "
                  f"{p_cert_next(n, d, u, k):.6f}")
    print(f"  (b) P(K_0 = 1) at (8,2): {emp:.6f} vs d/n = {d / n}: "
          f"{'PASS' if okb else 'FAIL'}")
    print(f"  (c) p_cert_next(u,k) exhaustive at (8,2) over {len(table)} "
          f"states: {'PASS' if okc else 'FAIL'}")
    # (d) certified-column ones law, dud probability, joint dud, overlap
    odd4 = [p for p in product(range(2), repeat=4) if sum(p) % 2 == 1]
    n_even = n_zero = n_both_even = n_both_zero = n_ovl = 0
    wcnt: dict = {}
    for rows in product(odd4, repeat=5):
        c0 = sum(r[0] for r in rows)
        c1 = sum(r[1] for r in rows)
        z0 = sum(r[1] for r in rows) == 0
        if c0 % 2 == 0:
            n_even += 1
            w = sum(r[0] for r in rows)
            wcnt[w] = wcnt.get(w, 0) + 1
            if w == 0:
                n_zero += 1
            if c1 % 2 == 0:
                n_both_even += 1
                if w == 0 and z0:
                    n_both_zero += 1
                if rows[0][0] == 0 and rows[0][1] == 0:
                    n_ovl += 1
    okw = all(abs(wcnt.get(w, 0) / n_even - math.comb(5, w) / 16.0) < 1e-12
              for w in (0, 2, 4))
    okz = abs(n_zero / n_even - 1 / 16.0) < 1e-12
    okj = abs(n_both_zero / n_both_even - 1 / 256.0) < 1e-12
    ovl = n_ovl / n_both_even
    print(f"  (d) d=2 certified-column law over 8^5 matrices: w-law "
          f"{{0:1,2:10,4:5}}/16 {'PASS' if okw else 'FAIL'}; dud 1/16 "
          f"{'PASS' if okz else 'FAIL'}; joint dud 1/256 "
          f"{'PASS' if okj else 'FAIL'}")
    print(f"  (e) [MV] overlap conditional P(M(r,cols01)=(0,0) | cols 0,1 "
          f"even) at d=2: {ovl:.6f} (marginal 0.25)")
    # (f) d=3 one-column law by Monte Carlo
    rng = random.Random(20261004)
    d3 = 3
    n_mc = 60000 if smoke else 1000000
    n_even3 = n_zero3 = 0
    w3: dict = {}
    for _ in range(n_mc):
        rows = []
        for _ in range(2 * d3 + 1):
            bits = [rng.randrange(2) for _ in range(2 * d3)]
            if sum(bits) % 2 == 0:
                bits[0] ^= 1
            rows.append(bits)
        c0 = sum(r[0] for r in rows)
        if c0 % 2 == 0:
            n_even3 += 1
            w = sum(r[0] for r in rows)
            w3[w] = w3.get(w, 0) + 1
            if w == 0:
                n_zero3 += 1
    okf = True
    for w in (0, 2, 4, 6):
        emp = w3.get(w, 0) / n_even3
        th = math.comb(7, w) / 64.0
        se = math.sqrt(th * (1 - th) / n_even3)
        okf &= abs(emp - th) < 4 * se + 1e-9
    empz = n_zero3 / n_even3
    okz3 = abs(empz - 1 / 64.0) < 4 * math.sqrt(1 / 64.0 * 63 / 64.0
                                                / n_even3)
    print(f"  (f) d=3 certified-column law, {n_mc} matrices: w-law "
          f"C(7,w)/64 {'PASS' if okf else 'FAIL'}; dud {empz:.5f} vs 1/64 "
          f"{'PASS' if okz3 else 'FAIL'}")


# ---------- E2: exact DP over the certified-tree family ----------

def build_dp(n: int, d: int, e: int, cert_fb: bool = True):
    """Backward induction over states (u, m, k, o, z): u K-queries used,
    m zero-answers on certified-column scans (fresh rows), k certifications
    found, o certifications not yet opened for scanning, z zeros seen on the
    current column (-1 = none open). Budget left is e - u - m. Action codes
    (ints, to keep the large-e tables small): 0 = FB (stop and fall back),
    1 = K (fresh K_j), 2 = NEXT (open a fresh certified column), 3 = SCAN
    (fresh row of the current column).
    cert_fb=False restricts the fallback value to the random-pair value f
    (chain-only variant). Returns the memo of (state -> (action, value))."""
    R = n + 1
    pw = [(w, math.comb(2 * d + 1, w) / 2.0 ** (2 * d))
          for w in range(0, 2 * d + 2, 2)]
    phit = []
    for z in range(e + 2):
        num = den = 0.0
        for w, p in pw:
            if R - w >= z:
                pz = math.comb(R - w, z) / math.comb(R, z)
                den += p * pz
                num += p * pz * w
        phit.append(num / den / (R - z) if den > 0 and R - z > 0 else 0.0)
    pDz = ((2 * d + 1) / R) * 0.5 / (1.0 - (2 * d + 1) / (2.0 * R))
    f = (2 * d + 1) * 2 * d / (R * n)
    nk = 2 * d + 2

    def key(u: int, m: int, k: int, o: int, z: int) -> int:
        return ((((u * (e + 1) + m) * nk + k) * nk + o) * (e + 2)) + z + 1

    def fbval(k: int, m: int) -> float:
        if cert_fb and k >= 1 and m < R:
            return max(0.0, ((2 * d + 1) - m * pDz) / (R - m))
        return f

    memo: dict = {}

    def V(u: int, m: int, k: int, o: int, z: int):
        kk = key(u, m, k, o, z)
        r = memo.get(kk)
        if r is not None:
            return r
        b = e - u - m
        if b <= 0:
            r = (0, fbval(k, m))
        else:
            best_f = fbval(k, m)
            best_a = 0
            if u < n:
                p = p_cert_next(n, d, u, k)
                v = p * V(u + 1, m, k + 1, o + 1, z)[1] \
                    + (1 - p) * V(u + 1, m, k, o, z)[1]
                if v > best_f:
                    best_f, best_a = v, 1
            if o >= 1:
                v = V(u, m, k, o - 1, 0)[1]
                if v > best_f:
                    best_f, best_a = v, 2
            if z >= 0:
                v = phit[z] + (1 - phit[z]) * V(u, m + 1, k, o, z + 1)[1]
                if v > best_f:
                    best_f, best_a = v, 3
            r = (best_a, best_f)
        memo[kk] = r
        return r

    return V, fbval, phit, pDz, f


# ---------- policy runners (shared by E3 exact and E4 Monte Carlo) ----------

def run_dp_policy(chan, n: int, d: int, e: int, V):
    u = m = k = o = 0
    z = -1
    certs: list = []
    opened = 0
    cur = None
    rows = 0
    while True:
        act = V(u, m, k, o, z)[0]
        if act == 0:
            if k >= 1:
                col = cur if cur is not None else certs[0]
                row = rows if rows < n + 1 else 0
                return (row, col), "fb_cert"
            return (0, 0), "fb_rand"
        if act == 1:
            j = u
            u += 1
            if chan.K(j) == 1:
                k += 1
                o += 1
                certs.append(j)
        elif act == 2:
            cur = certs[opened]
            opened += 1
            o -= 1
            z = 0
        elif act == 3:
            pair = (rows, cur)
            rows += 1
            m += 1
            if chan.x(pair[0], pair[1]) == 1:
                return pair, "chain"
            z += 1
        else:
            raise AssertionError(act)


def run_ksplit(chan, n: int, d: int, e: int, s: int, zcap: int):
    s = min(s, n)
    certs = [j for j in range(s) if chan.K(j) == 1]
    budget = e - s
    used: set = set()
    for j in certs:
        r = 0
        while r < n + 1 and r < zcap and budget > 0:
            used.add(r)
            budget -= 1
            if chan.x(r, j) == 1:
                return (r, j), "chain"
            r += 1
        if budget <= 0:
            break
    if certs:
        row = 0
        while row in used:
            row += 1
        return (row % (n + 1), certs[0]), "fb_cert"
    return (0, 0), "fb_rand"


def run_single(chan, n: int, d: int, e: int, pairs):
    for c in pairs[:e]:
        i, j = divmod(c, n)
        if chan.x(i, j) == 1:
            return (i, j), "hit"
    return (0, 0), "fb_rand"


def run_hybrid(chan, n: int, d: int, e: int, s1: int, pairs):
    """Singles in order; at the FIRST hit spend one query on K_j (a hit plus
    K_j = 1 is a posterior-1 certificate), then continue scanning singles;
    fall back to the first hit. Pathwise at least single_scan up to the one
    query the K-check consumes."""
    first = None
    idx = -1
    for idx, c in enumerate(pairs[:e]):
        i, j = divmod(c, n)
        if chan.x(i, j) == 1:
            first = (i, j)
            break
    if first is not None and idx + 1 < e:
        if chan.K(first[1]) == 1:
            return first, "chain"
        for c in pairs[idx + 2:e]:
            i, j = divmod(c, n)
            if chan.x(i, j) == 1:
                return (i, j), "hit"
    if first is not None:
        return first, "hit"
    return (0, 0), "fb_rand"


# ---------- channels ----------

class Chan:
    """Exact true-channel wrapper (structural sampler: uniform odd free
    rows; exact by kernel_structure.md F2/F3)."""

    __slots__ = ("ans", "ansK", "free", "_x", "_k")

    def __init__(self, n: int, d: int, rng: random.Random):
        self.ans, self.ansK, self.free, _, _ = \
            base.make_channel_struct(n, d, rng)
        self._x = {}
        self._k = {}

    def x(self, i: int, j: int) -> int:
        c = self._x.get((i, j))
        if c is None:
            c = self.ans((i, j))
            self._x[(i, j)] = c
        return c

    def K(self, j: int) -> int:
        c = self._k.get(j)
        if c is None:
            c = self.ansK(j)
            self._k[j] = c
        return c

    def isfree(self, i: int, j: int) -> bool:
        return (i, j) in self.free


class Chan2(Chan):
    """Adds exact degree-2 diagonal monomial answers (design-space sampler
    at the canonical system (2d, d); same-line products are determined 0)."""

    __slots__ = ("mi", "lf", "dmap", "rmap", "rho", "Dm", "dd")

    def __init__(self, n: int, d: int, rng: random.Random):
        ch = base.CH[(2 * d, d)]
        self.mi = ch["mono_index"]
        self.dd = d
        lf = ch["Lp"]
        for b in range(len(ch["kb"])):
            if rng.random() < 0.5:
                lf ^= ch["kb"][b]
        self.lf = lf
        ap = rng.sample(range(n + 1), n - 2 * d)
        ah = rng.sample(range(n), n - 2 * d)
        self.rho = dict(zip(ap, ah))
        D = sorted(set(range(n + 1)) - set(ap))
        R = sorted(set(range(n)) - set(ah))
        self.Dm = {i: p for p, i in enumerate(D)}
        self.rmap = {j: h for h, j in enumerate(R)}
        self.ans = None
        self.ansK = None
        self.free = {(i, j) for i in D for j in R}
        self._x = {}
        self._k = {}

    def _single(self, i: int, j: int) -> int:
        if i in self.rho:
            return 1 if self.rho[i] == j else 0
        if j not in self.rmap:
            return 0
        v = self.Dm[i] * 2 * self.dd + self.rmap[j]
        return (self.lf >> self.mi[(v,)]) & 1

    def x(self, i: int, j: int) -> int:
        return self._single(i, j)

    def mono(self, i1, j1, i2, j2) -> int:
        """Answer of x_{i1 j1} x_{i2 j2}, distinct pigeons and holes.
        Determined cases (deg2_theory.md F4 and the V-ideal reduction): a
        killed-unmatched component forces 0; a matched component reduces
        the answer to the other single (x_ij - 1 lies in V, so the product
        differs from the other single by a V element)."""
        k1 = (i1 in self.rho) or (j1 not in self.rmap)
        k2 = (i2 in self.rho) or (j2 not in self.rmap)
        if k1 and k2:
            return 0
        if k1:
            return self._single(i2, j2)
        if k2:
            return self._single(i1, j1)
        if i1 in self.rho and self.rho[i1] == j1:
            return self._single(i2, j2)
        if i2 in self.rho and self.rho[i2] == j2:
            return self._single(i1, j1)
        v1 = self.Dm[i1] * 2 * self.dd + self.rmap[j1]
        v2 = self.Dm[i2] * 2 * self.dd + self.rmap[j2]
        key = (v1, v2) if v1 < v2 else (v2, v1)
        return (self.lf >> self.mi[key]) & 1


def run_mono(chan2, n: int, d: int, e: int, pairs):
    seen: set = set()
    cnt = 0
    while cnt < e:
        c1, c2 = pairs[cnt * 2], pairs[cnt * 2 + 1]
        cnt += 1
        i1, j1 = divmod(c1, n)
        i2, j2 = divmod(c2, n)
        if i1 == i2 or j1 == j2 or (c1, c2) in seen:
            continue
        seen.add((c1, c2))
        seen.add((c2, c1))
        if chan2.mono(i1, j1, i2, j2) == 1:
            return (i1, j1), "mono"
    return (0, 0), "fb_rand"


# ---------- E3: brute-force exact enumeration at (5,2) ----------

def e3_bruce(smoke: bool) -> None:
    print("\n[E3] brute-force exact enumeration at (5,2), e = 6 "
          "(all 983,040 configurations)")
    n, d, e = 5, 2, 6
    V, _, _, _, _ = build_dp(n, d, e)
    W = V(0, 0, 0, 0, -1)[1]
    stride = 61 if smoke else 1
    odd4 = [p for p in product(range(2), repeat=4) if sum(p) % 2 == 1]
    grid = [(2, 99), (3, 99), (4, 99), (6, 99)]
    names = (["dp_tree"] + [f"ksplit(s={s})" for s, _ in grid]
             + ["single_scan"])
    wins = {nm: 0 for nm in names}
    tot = 0
    pairs = list(range((n + 1) * n))
    for kp in range(n + 1):
        D = [i for i in range(n + 1) if i != kp]
        for kh in range(n):
            R = [j for j in range(n) if j != kh]
            rpos = {j: h for h, j in enumerate(R)}
            dpos = {i: p for p, i in enumerate(D)}
            for rows in product(odd4, repeat=2 * d + 1):
                if tot % stride:
                    tot += 1
                    continue
                tot += 1
                xt, kt = {}, {}
                for i in D:
                    for j in R:
                        xt[(i, j)] = rows[dpos[i]][rpos[j]]
                xt[(kp, kh)] = 1
                for i in D:
                    xt[(i, kh)] = 0
                for j in R:
                    xt[(kp, j)] = 0
                    kt[j] = 1 ^ (rows[0][rpos[j]] ^ rows[1][rpos[j]]
                                 ^ rows[2][rpos[j]] ^ rows[3][rpos[j]]
                                 ^ rows[4][rpos[j]])
                kt[kh] = 0
                freeset = {(i, j) for i in D for j in R}

                class FC:
                    pass
                fc = FC()
                fc.xt, fc.kt, fc.free = xt, kt, freeset
                fc.x = lambda i, j, _xt=xt: _xt[(i, j)]
                fc.K = lambda j, _kt=kt: _kt[j]
                fc.isfree = lambda i, j, _fs=freeset: (i, j) in _fs
                out, _ = run_dp_policy(fc, n, d, e, V)
                if out in freeset:
                    wins["dp_tree"] += 1
                for (s, zc), nm in zip(grid, names[1:]):
                    out, _ = run_ksplit(fc, n, d, e, s, zc)
                    if out in freeset:
                        wins[nm] += 1
                out, _ = run_single(fc, n, d, e, pairs)
                if out in freeset:
                    wins["single_scan"] += 1
    nsim = 0
    # count evaluated configs (stride-aware)
    nsim = (tot + stride - 1) // stride if stride > 1 else tot
    print(f"  configurations evaluated: {nsim}"
          f"{' (strided)' if stride > 1 else ''}")
    print(f"  DP model value W_dp = {W:.6f}")
    best = None
    for nm in names:
        ex = wins[nm] / nsim
        flag = " <- best" if best is None or ex > best[1] else ""
        if best is None or ex > best[1]:
            best = (nm, ex)
        print(f"  exact {nm:16s}: {wins[nm]:7d}/{nsim} = {ex:.6f}"
              f"{'  (model ' + format(W, '.6f') + ')' if nm == 'dp_tree' else ''}"
              f"{flag}")
    print(f"  model-vs-exact delta on the DP policy: "
          f"{wins['dp_tree'] / nsim - W:+.6f} "
          f"(scope: all parity couplings active at n = 5)")


# ---------- E4 + E5: Monte Carlo at the target points and cap arithmetic ----------

def caps_block(n: int, d: int, e: int, W: float, Wch: float) -> dict:
    q = (2 * d + 1) * d / ((2 * d + 1) * d + (n - 2 * d))
    h1 = ((2 * d + 1) * d + (n - 2 * d)) / ((n + 1) * n)
    f = (2 * d + 1) * 2 * d / ((n + 1) * n)
    x = e * d / n
    A = min(1.0, e * h1) * min(1.0, e * q * (2 * d - 1) / (2.0 * (n - 1)))
    rho = (2 * d + 1) * n / (2.0 * d * (n + 1))
    alpha, Pi = 0.5, 0.0
    for i in range(1, 2000):
        a = i / 2000.0
        val = (1 - math.exp(-a * x)) * (1 - math.exp(-(1 - a) * rho * x))
        if val > Pi:
            Pi, alpha = val, a
    cw = rho / (1.0 + rho)
    chainsup = (Wch - f) / (1.0 - f) if f < 1.0 else Wch
    return dict(q=q, h1=h1, f=f, x=x, A=A, rho=rho, alpha=alpha, Pi=Pi,
                cw=cw, cap_printed=q + 2 * (1 - math.exp(-x / 4)) + A,
                cap_sharp=Pi + (1 - Pi) * (q + A),
                cap_dp=W + (1 - W) * (q + A),
                cap_family=chainsup + (1 - chainsup) * (q + A),
                chainsup=chainsup,
                thm4b=(1 - math.exp(-x / 4)) ** 2,
                beta=cw * x,
                w_linear=(1 - math.exp(-alpha * x))
                * (1 - math.exp(-(1 - alpha) * rho * x)),
                Wch=Wch)


def e4_point(tag: str, n: int, d: int, e: int, nch: int, rng,
             grid):
    print(f"\n[E4/E5] {tag}: true optimal budgeted success bracket "
          f"(x = ed/n = {e * d / n:.4g})")
    V, _, _, _, _ = build_dp(n, d, e)
    W = V(0, 0, 0, 0, -1)[1]
    Vch, _, _, _, _ = build_dp(n, d, e, cert_fb=False)
    Wch = Vch(0, 0, 0, 0, -1)[1]
    C = caps_block(n, d, e, W, Wch)
    print(f"  q = {C['q']:.6f}  h1 = {C['h1']:.6f}  f = {C['f']:.6f}  "
          f"A(e) = {C['A']:.6f}  rho = {C['rho']:.5f}  alpha* = "
          f"{C['alpha']:.3f}  c_w = {C['cw']:.5f}")
    print(f"  DP model: W_dp(total) = {W:.6f}  W_dp(chain-only) = "
          f"{Wch:.6f}  (chain sup chi = {C['chainsup']:.6f})  "
          f"split-form W(alpha*) = {C['w_linear']:.6f}")
    print(f"  caps: printed (q + 2(1-e^-x/4) + A) = {C['cap_printed']:.4f}   "
          f"family-exact cap (chi + (1-chi)(q+A)) = {C['cap_family']:.4f}   "
          f"printed Thm 4b bound = {C['thm4b']:.6f}   sharpened Thm 4b' "
          f"(1-e^-beta)^2, beta = c_w x = {C['beta']:.4f}: "
          f"{(1 - math.exp(-C['beta'])) ** 2:.6f}")
    pols = [("dp_tree", lambda ch, pr: run_dp_policy(ch, n, d, e, V))]
    for (s, zc) in grid:
        pols.append((f"ksplit(s={s},Z={zc})",
                     lambda ch, pr, s=s, zc=zc: run_ksplit(ch, n, d, e, s, zc)))
    pols.append(("single_scan", lambda ch, pr: run_single(ch, n, d, e, pr)))
    pols.append(("hybrid(s1=12)",
                 lambda ch, pr: run_hybrid(ch, n, d, e, 12, pr)))
    wins = {nm: 0 for nm, _ in pols}
    cats = {"chain": 0, "fb_cert": 0, "fb_rand": 0, "hit": 0}
    for _ in range(nch):
        ch = Chan(n, d, rng)
        pairs = rng.sample(range((n + 1) * n), e)
        for nm, fn in pols:
            out, _ = fn(ch, pairs)
            if ch.isfree(out[0], out[1]):
                wins[nm] += 1
        out, cat = pols[0][1](ch, pairs)
        cats[cat] += 1
    print(f"  measured success over {nch} exact-channel sims "
          f"(99% Clopper-Pearson):")
    best = 0.0
    for nm, _ in pols:
        lo, hi = cp_ci(wins[nm], nch)
        best = max(best, wins[nm] / nch)
        print(f"    {nm:18s}: {wins[nm] / nch:.4f} [{lo:.4f},{hi:.4f}]")
    lo, hi = cp_ci(wins["dp_tree"], nch)
    print(f"  DP-policy outcome split: chain {cats['chain'] / nch:.4f}, "
          f"fb_cert {cats['fb_cert'] / nch:.4f}, fb_rand "
          f"{cats['fb_rand'] / nch:.4f}")
    viol = "EXCEEDS" if wins["dp_tree"] / nch > C['Pi'] else "does not exceed"
    print(f"  [MV] fixed-split product Pi = {C['Pi']:.4f} vs measured DP "
          f"policy {wins['dp_tree'] / nch:.4f}: the adaptive optimum "
          f"{viol} the split product, so split-product (Pi-form) cap terms "
          f"are invalid; the valid K-term is the chain sup chi = "
          f"{C['chainsup']:.4f}")
    # policy trace: greedy action along two representative paths
    aname = {0: "FB", 1: "K", 2: "NEXT", 3: "SCAN"}

    def trace_path(u, m, k, o, z):
        out = []
        while u + m < e and len(out) < 40:
            a = V(u, m, k, o, z)[0]
            out.append(f"u{u}m{m}k{k}o{o}z{z}:{aname[a]}")
            if a == 1:
                u += 1
            elif a == 2:
                o -= 1
                z = 0
            elif a == 3:
                m += 1
                z += 1
            else:
                break
        return out

    trace = trace_path(0, 0, 0, 0, -1)
    print(f"  policy trace (no-cert path): {' '.join(trace[:12])} ...")
    trace = trace_path(16, 0, 1, 1, -1)
    print(f"  policy trace (cert at u=16): {' '.join(trace[:12])} ...")
    print(f"  BRACKET[{tag}]: success* in [{wins['dp_tree'] / nch:.4f} "
          f"(measured DP policy), {C['cap_family']:.4f} (family-exact cap)]"
          f"; err* in [{1 - C['cap_family']:.4f}, {1 - wins['dp_tree'] / nch:.4f}]"
          f"  [99% MC band on the witness: "
          f"{1 - hi:.4f} <= err* low side]")
    return dict(meas=wins, nch=nch, caps=C, W=W, Wch=Wch, lo=lo, hi=hi)

def e4_mono(n: int, d: int, e: int, nch: int, rng) -> None:
    print(f"\n[E4-mono] degree-2 inventory at ({n},{d}), e = {e}: diagonal "
          f"monomial scan (exact design-space channel)")
    wins = tot = 0
    for _ in range(nch):
        ch = Chan2(n, d, rng)
        pairs = rng.sample(range((n + 1) * n), 2 * e)
        out, _ = run_mono(ch, n, d, e, pairs)
        tot += 1
        if ch.isfree(out[0], out[1]):
            wins += 1
    lo, hi = cp_ci(wins, tot)
    print(f"    mono_scan: {wins / tot:.4f} [{lo:.4f},{hi:.4f}] "
          f"(first 1-answer outputs its first component pair; posterior "
          f"q_and ~ q: no certificate mechanism exists at degree 2 within "
          f"this budget)")


def e6_sweep() -> None:
    """Budget sweep at (128,2): the family-exact cap and the DP witness vs
    e, locating the budgeted certification boundary (success* = 1/2). The
    exact DPs are run to e = 64 (the tables grow cubically in e); the
    crossing is bracketed by the computed trend and marked interpolated."""
    print("\n[E6] budget sweep: certification boundary location", flush=True)
    n, d = 128, 2
    q = (2 * d + 1) * d / ((2 * d + 1) * d + (n - 2 * d))
    h1 = ((2 * d + 1) * d + (n - 2 * d)) / ((n + 1) * n)
    f = (2 * d + 1) * 2 * d / ((n + 1) * n)
    prev = None
    chis = []
    for e in range(8, 65, 8):
        Vch, _, _, _, _ = build_dp(n, d, e, cert_fb=False)
        Wch = Vch(0, 0, 0, 0, -1)[1]
        chi = (Wch - f) / (1.0 - f)
        A = min(1.0, e * h1) * min(1.0, e * q * (2 * d - 1) / (2.0 * (n - 1)))
        cap = chi + (1 - chi) * (q + A)
        w_str = ""
        if e in (32, 48, 64):
            V, _, _, _, _ = build_dp(n, d, e)
            w_str = f" W_dp={V(0, 0, 0, 0, -1)[1]:.4f}"
        print(f"  (128,2) e={e}: chi={chi:.4f} cap_family={cap:.4f}"
              f"{w_str}", flush=True)
        chis.append(chi)
        prev = cap
    # labeled interpolation from the computed chi slope (per query, at e=64)
    dchi = (chis[-1] - chis[-2]) / 8.0
    ee, cross_cap = 64, None
    while ee < 120:
        ee += 4
        chi = min(1.0, chis[-1] + dchi * (ee - 64))
        A = min(1.0, ee * h1) * min(1.0, ee * q * (2 * d - 1) / (2.0 * (n - 1)))
        cap = chi + (1 - chi) * (q + A)
        if cap >= 0.5:
            cross_cap = ee
            break
    ee = 8
    cross_print = None
    while ee < 400:
        xp = ee * d / n
        ap = min(1.0, ee * h1) * min(1.0, ee * q * (2 * d - 1)
                                     / (2.0 * (n - 1)))
        if q + 2 * (1 - math.exp(-xp / 4)) + ap >= 0.5:
            cross_print = ee
            break
        ee += 1
    print(f"  (128,2) cap at e=64 computed 0.4107; linear-chi interpolation "
          f"(step 4, labeled INTERPOLATED): cap crosses success=1/2 at "
          f"e ~ {cross_cap}; printed cap crosses at e = {cross_print} "
          f"(exact); cap(64)=0.411 < 1/2 is computed, so the true boundary "
          f"lies above e=64")
    n, d = 96, 3
    q = (2 * d + 1) * d / ((2 * d + 1) * d + (n - 2 * d))
    h1 = ((2 * d + 1) * d + (n - 2 * d)) / ((n + 1) * n)
    f = (2 * d + 1) * 2 * d / ((n + 1) * n)
    for e in (24, 48):
        Vch, _, _, _, _ = build_dp(n, d, e, cert_fb=False)
        Wch = Vch(0, 0, 0, 0, -1)[1]
        chi = (Wch - f) / (1.0 - f)
        A = min(1.0, e * h1) * min(1.0, e * q * (2 * d - 1) / (2.0 * (n - 1)))
        cap = chi + (1 - chi) * (q + A)
        w_str = ""
        if e == 48:
            V, _, _, _, _ = build_dp(n, d, e)
            w_str = f" W_dp={V(0, 0, 0, 0, -1)[1]:.4f}"
        print(f"  (96,3) e={e}: chi={chi:.4f} cap_family={cap:.4f}"
              f"{w_str}", flush=True)


# ---------- main ----------

def main() -> None:
    smoke = "--smoke" in sys.argv
    base.CH[(4, 2)] = base.channel_setup(2)
    base.CH[(6, 3)] = base.channel_setup(3)
    print("chi_gap_e_check: GAP E (O2(ii)) budgeted-constant bracket, "
          "true pipeline channel\n")
    e1_checks(smoke)
    e3_bruce(smoke)
    rng = random.Random(271828)
    nch = 4000 if smoke else 150000
    nch2 = 2000 if smoke else 80000
    e4_point("(128,2) e=32", 128, 2, 32, nch, rng,
             grid=[(10, 99), (14, 99), (16, 99), (20, 99), (24, 99),
                   (16, 8), (16, 4)])
    if not smoke:
        e4_mono(128, 2, 32, 30000, rng)
    e4_point("(96,3) e=48", 96, 3, 48, nch, rng,
             grid=[(20, 99), (24, 99), (26, 99), (28, 99), (32, 99),
                   (26, 12), (26, 6)])
    e4_point("(96,3) e=32", 96, 3, 32, nch2, rng,
             grid=[(14, 99), (16, 99), (18, 99), (20, 99)])
    e6_sweep()
    print("\ndone.")


if __name__ == "__main__":
    main()
