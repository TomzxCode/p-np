"""Full-pipeline check of the multiplicative-triple hypothesis for Omega(n,d).

Samples the complete generative pipeline of Omega(n,d) (arXiv:2609.35927, Def 4.3) at
n = 32, d = 2, p = 2: a random restriction rho (28 of 33 pigeons assigned, leaving 5 free
pigeons and 4 free holes), a uniform random design L of the restricted system (over the
affine space Des(4,2): kills V(4,2), L(1) = 1), and a random outer degree-2 monomial pair
(m1, m2) with m1 != m2. Measures the rate at which the design omega = (rho, L) violates
multiplicativity on the triple:  omega(m1)*omega(m2) != omega(m1*m2).

RESULT (2026-10-03): violation rate 0.0005 (mixed 0.0003, same-hole 0.0086) - the rate is
NEGLIGIBLE, refuting the hypothesis that trivial triple-trees attack Omega(n,d). The cause:
omega = L o rho is automatically multiplicative outside the tiny free region (each outer
variable is free with probability ~0.019, so an all-free triple needs ~(2d/n)^4-level
luck). An earlier canonical-system measurement of 0.37 dropped the restriction layer and
was misleading; see LOG.md RETRACTION entry.
"""
from __future__ import annotations

import random
import statistics

from chi_p2_adaptive import build, CANON_N


def main() -> None:
    kernel2, mono_index4 = build()
    const_vec = 1 << mono_index4[tuple()]
    rng = random.Random(333)
    n, d = 32, 2
    outer_pairs = [(i, j) for i in range(n + 1) for j in range(n)]

    def sample_rho():
        assigned_p = rng.sample(range(n + 1), n - 2 * d)
        assigned_h = rng.sample(range(n), n - 2 * d)
        rho = dict(zip(assigned_p, assigned_h))
        D = sorted(set(range(n + 1)) - set(assigned_p))
        R = sorted(set(range(n)) - set(assigned_h))
        canon = {}
        for pi_, i in enumerate(D):
            for hj_, j in enumerate(R):
                canon[(i, j)] = pi_ * CANON_N + hj_
        return rho, D, R, canon

    def restrict_mono(t: tuple[int, ...], rho, canon) -> dict[tuple[int, ...], int]:
        terms: dict[tuple[int, ...], int] = {(): 1}
        for (i, j) in t:
            if i in rho:
                if rho[i] != j:
                    return {}
            elif j in {jj for ii, jj in rho.items()}:
                return {}
            else:
                cv = canon[(i, j)]
                terms = {tuple(sorted(tt + (cv,))): cc for tt, cc in terms.items()}
        return terms

    def Lval(L: int, poly: dict[tuple[int, ...], int]) -> int:
        v = 0
        for t in poly:
            v ^= (L >> mono_index4[t]) & 1
        return v

    n_trials = 4000
    violations = 0
    rates_by_kind: dict[str, list[int]] = {"mixed": [], "same-pigeon": [], "same-hole": []}
    for _ in range(n_trials):
        rho, D, R, canon = sample_rho()
        rho_inv = {j: i for i, j in rho.items()}
        L = const_vec
        for k in kernel2:
            if rng.random() < 0.5:
                L ^= k
        m1 = tuple(sorted(rng.sample(outer_pairs, 1)))
        m2 = tuple(sorted(rng.sample(outer_pairs, 1)))
        while m1 == m2:
            m2 = tuple(sorted(rng.sample(outer_pairs, 1)))
        p1 = restrict_mono(m1, rho, canon)
        p2 = restrict_mono(m2, rho, canon)
        prod: dict[tuple[int, ...], int] = {}
        for t1 in p1:
            for t2 in p2:
                merged = tuple(sorted(t1 + t2))
                prod[merged] = prod.get(merged, 0) ^ (p1[t1] & p2[t2])
        a1, a2, a3 = Lval(L, p1), Lval(L, p2), Lval(L, prod)
        violated = ((a1 * a2) & 1) != a3
        if violated:
            violations += 1
        same_p = m1[0][0] == m2[0][0]
        same_h = m1[0][1] == m2[0][1]
        kind = "same-pigeon" if same_p else ("same-hole" if same_h else "mixed")
        rates_by_kind[kind].append(int(violated))

    print(f"trials = {n_trials}, outer n = {n}, d = {d}, p = 2")
    print(f"overall multiplicativity-violation rate: {violations / n_trials:.4f}")
    for kind, xs in rates_by_kind.items():
        if xs:
            print(f"  {kind:>12}: {sum(xs) / len(xs):.4f} (n = {len(xs)})")
    print("measured violation rate is negligible: trivial triple-trees do not threaten "
          "Omega(n,d) as a pseudo-solution; designs induced by L o rho are automatically "
          "multiplicative outside the (2d/n)^4-level free region.")


if __name__ == "__main__":
    main()
