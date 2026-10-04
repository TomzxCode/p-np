"""GF(2) verification and dimension tables for the Razborov/Krajicek PHP consequence spaces.

V(n,d) = span{ g*f : f in -PHP_n, deg(g*f) <= d } inside F_2^{<=d}[x_ij], where -PHP_n is the
polynomial system: hole-collisions x_{i1 j} x_{i2 j}, two-holes-per-pigeon x_{i j1} x_{i j2},
pigeon-placed Q_i = 1 + sum_j x_ij (char 2), and Boolean x_ij^2 + x_ij.

Verified here for small (n, d) with 2 <= d <= n/2 (Razborov's Theorem 4.1 regime):
  (1) 1 is NOT in V(n,d)                        -> designs exist (Corollary 4.2),
  (2) closure: g in V(n,d), deg(g*h) <= d  =>   g*h in V(n,d),
and reported: dim S(n,d), rank V(n,d), and the affine design-space dimension
  dim Des(n,d) = dim S(n,d) - dim V(n,d) - 1.
Relevance: Krajicek's pseudo-solution program (arXiv:2609.35927) builds Omega(n,d) from
restrictions rho leaving exactly n_rho = 2d free holes and designs L in Des(n_rho, d); the
tables give |Des(2d, d)| = 2^{dim Des(2d, d)} directly.
"""
from __future__ import annotations

import random
from itertools import combinations, combinations_with_replacement


def system_polys(n: int) -> list[dict[tuple[int, ...], int]]:
    """The -PHP_n polynomials as {monomial-tuple: coeff} dicts over GF(2).

    Variables are indexed 0..n(n+1)-1, variable (i, j) with i in [n+1] (pigeons),
    j in [n] (holes), index = (i-1)*n + (j-1). Monomials are sorted tuples of
    variable indices (repetition allowed). Coefficients are 0/1 (char 2).
    """
    m = n * (n + 1)

    def v(i: int, j: int) -> int:
        return (i - 1) * n + (j - 1)

    polys: list[dict[tuple[int, ...], int]] = []
    # hole collisions: x_{i1 j} * x_{i2 j}, i1 < i2
    for j in range(1, n + 1):
        for i1 in range(1, n + 2):
            for i2 in range(i1 + 1, n + 2):
                a, b = sorted((v(i1, j), v(i2, j)))
                polys.append({(a, b): 1})
    # two holes per pigeon: x_{i j1} * x_{i j2}, j1 < j2
    for i in range(1, n + 2):
        for j1 in range(1, n + 1):
            for j2 in range(j1 + 1, n + 1):
                a, b = sorted((v(i, j1), v(i, j2)))
                polys.append({(a, b): 1})
    # every pigeon placed: Q_i = 1 + sum_j x_ij  (char 2: minus = plus)
    for i in range(1, n + 2):
        poly: dict[tuple[int, ...], int] = {(): 1}
        for j in range(1, n + 1):
            poly[(v(i, j),)] = 1
        polys.append(poly)
    # Boolean: x_ij^2 + x_ij
    for i in range(1, n + 2):
        for j in range(1, n + 1):
            a = v(i, j)
            polys.append({(a, a): 1, (a,): 1})
    return polys


def monomials(n: int, d: int) -> list[tuple[int, ...]]:
    m = n * (n + 1)
    monos = [tuple()]
    for k in range(1, d + 1):
        monos.extend(combinations_with_replacement(range(m), k))
    return monos


def shift(poly: dict[tuple[int, ...], int], mono: tuple[int, ...]) -> dict[tuple[int, ...], int]:
    """Multiply poly by the monomial `mono` (merge sorted tuples with repetition)."""
    out: dict[tuple[int, ...], int] = {}

    def merge(a: tuple[int, ...], b: tuple[int, ...]) -> tuple[int, ...]:
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

    for t in poly:
        nt = merge(t, mono)
        out[nt] = out.get(nt, 0) ^ poly[t]
    return out


def to_vec(poly: dict[tuple[int, ...], int], mono_index: dict[tuple[int, ...], int]) -> int:
    vec = 0
    for t in poly:
        vec ^= 1 << mono_index[t]
    return vec


def gf2_rank(vectors: list[int]) -> tuple[int, list[int]]:
    """Return (rank, pivot-reduced basis)."""
    pivots: dict[int, int] = {}
    rank = 0
    for v in vectors:
        while v:
            h = v.bit_length() - 1
            if h in pivots:
                v ^= pivots[h]
            else:
                pivots[h] = v
                rank += 1
                break
        # v == 0 -> dependent, continue
    return rank, list(pivots.values())


def in_span(vec: int, pivots: list[int]) -> bool:
    """Membership by reduction in DECREASING leading-bit order (single pass suffices:
    XOR-ing pivot with leading bit h clears bit h and only touches strictly lower bits)."""
    for p in sorted(pivots, key=lambda x: x.bit_length(), reverse=True):
        h = p.bit_length() - 1
        if (vec >> h) & 1:
            vec ^= p
    return vec == 0


def analyze(n: int, d: int, closure_trials: int = 10, seed: int = 0) -> None:
    rng = random.Random(seed * 1000 + 17 * n + d)
    polys = system_polys(n)
    monos = monomials(n, d)
    mono_index = {t: i for i, t in enumerate(monos)}
    N = len(monos)

    deg = {t: len(t) for t in monos}
    # V(n,d) generators: monomial shifts of system polynomials
    gens: list[int] = []
    gens_low: list[int] = []  # generators of degree <= d-1 (for closure sampling)
    for f in polys:
        df = max(len(t) for t in f)
        for mono in monos:
            if len(mono) + df <= d:
                g = shift(f, mono)
                vec = to_vec(g, mono_index)
                gens.append(vec)
                if len(mono) + df <= d - 1:
                    gens_low.append(vec)

    rank_v, basis_v = gf2_rank(gens)
    one_vec = 1 << mono_index[()]
    one_outside = not in_span(one_vec, basis_v)

    # closure spot-check: random g in span(gens_low), h = single variable
    closure_ok = True
    if gens_low and d >= 2:
        var_monos = [t for t in monos if len(t) == 1]
        for _ in range(closure_trials):
            g = 0
            for _ in range(8):
                g ^= rng.choice(gens_low)
            h = rng.choice(var_monos)
            # multiply vector g by monomial h
            prod = 0
            t_bits = [i for i in range(N) if (g >> i) & 1]
            ok = True
            for i in t_bits:
                t = monos[i]
                nt = tuple(sorted(t + h))
                if len(nt) > d:
                    ok = False
                    break
                prod ^= 1 << mono_index[nt]
            if not ok:
                continue
            if not in_span(prod, basis_v):
                closure_ok = False
                break

    dim_s = N
    dim_des = dim_s - rank_v - (1 if one_outside else 0)
    print(
        f"n={n} d={d} | dim S={dim_s} | rank V={rank_v} | dim Des={dim_des} "
        f"| |Des|=2^{dim_des} | 1 not in V: {one_outside} | closure: {closure_ok}"
    )


if __name__ == "__main__":
    import time

    print("GF(2) dimension tables and Razborov Theorem 4.1 checks for -PHP_n")
    cases = [(n, 2) for n in (4, 5, 6, 7, 8)] + [(6, 3)]
    for n, d in cases:
        assert 2 <= d <= n / 2, f"Razborov regime requires d <= n/2: n={n}, d={d}"
        start = time.perf_counter()
        analyze(n, d)
        print(f"    ({time.perf_counter() - start:.1f}s)")
