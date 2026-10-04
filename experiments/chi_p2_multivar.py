"""p=2 multi-variable query lift test (Krajicek chi-task, arXiv:2609.35927).

At p = 2 over the Omega(n,d) pipeline (outer n = 32, d = 2, restrictions leaving 5 free
pigeons / 4 free holes, uniform designs L of the restricted (4,2) system), the answer to a
query g is a single bit. For SINGLE-variable queries x_ij the answer is informative:
  free -> fair coin; killed-unmatched -> 0; killed-matched -> 1,
giving P(ans=1) ~ 0.036 and posterior P(free | ans=1) ~ 0.26 (measured last turn: 0.24).

For MULTI-variable queries the determined parts are XORs of random match-indicators, so
P(ans = 1) should be ~1/2 REGARDLESS of freeness: no lift. This is the no-lift prediction
underlying the p=2 statistical core of the pseudo-solution program: if no shallow tree at
p=2 beats the single-query 0.26-style cap, then every tree errs with probability >= 1-O(d^3
log k / n^2) >> k^{-O(1)}, and Krajicek's Theorem 6.1 yields the AC0[2]-Frege lower-bound
program's target. Measured here for degree-2 two-variable queries:
  P(ans=1), and P(at least one queried variable free | ans=1).
"""
from __future__ import annotations

import random
import statistics

from chi_p2_adaptive import build

CANON_N = 4


def main() -> None:
    kernel2, mono_index = build()
    const_vec = 1 << mono_index[tuple()]
    rng = random.Random(555)
    n, d = 32, 2
    outer_vars = [(i, j) for i in range(n + 1) for j in range(n)]
    n_sim = 400
    n_queries = 60  # random 2-variable queries per (rho, L) sample

    ans1_with_free = 0  # ans=1 AND at least one queried var free
    ans1_total = 0
    free_total = 0      # queries with >=1 free var (marginal)
    total = 0
    single_ans1 = 0
    single_total = 0

    for _ in range(n_sim):
        L = const_vec
        for k in kernel2:
            if rng.random() < 0.5:
                L ^= k
        assigned_p = rng.sample(range(n + 1), n - 2 * d)
        assigned_h = rng.sample(range(n), n - 2 * d)
        rho = dict(zip(assigned_p, assigned_h))
        rho_inv = {j: i for i, j in rho.items()}
        D = sorted(set(range(n + 1)) - set(assigned_p))
        R = sorted(set(range(n)) - set(assigned_h))
        canon = {}
        for pi_, i in enumerate(D):
            for hj_, j in enumerate(R):
                canon[(i, j)] = pi_ * CANON_N + hj_

        def answer_bit(t: tuple[int, ...]) -> int:
            """Answer to the degree-2 monomial query t = (var1, var2), rho-restricted."""
            vals = []
            for (i, j) in t:
                if i in rho:
                    vals.append(1 if rho[i] == j else 0)
                elif j in rho_inv:
                    vals.append(0)
                else:
                    vals.append(None)  # free: design value
            if any(v is None for v in vals):
                # free coordinates present: XOR of independent fair design bits
                return rng.randrange(2)
            return vals[0] ^ vals[1]

        for _ in range(n_queries):
            v1, v2 = rng.sample(outer_vars, 2)
            free_any = (v1 in {(i, j) for i in D for j in R}) or \
                       (v2 in {(i, j) for i in D for j in R})

            def ans_bit(t: tuple[int, int]) -> int:
                (i, j) = t
                if i in rho:
                    return 1 if rho[i] == j else 0
                if j in rho_inv:
                    return 0
                cv = canon[(i, j)]
                return (L >> cv) & 1

            a = ans_bit(v1) ^ ans_bit(v2)
            total += 1
            free_total += free_any
            if a == 1:
                ans1_total += 1
                free_total = free_total
                if free_any:
                    ans1_with_free += 1
            # single-variable reference: first variable
            sa = ans_bit(v1)
            single_total += 1
            single_ans1 += sa

    print(f"outer n={n}, d={d}, p=2; samples={n_sim}, queries/sample={n_queries}")
    print(f"P(ans=1) for 2-variable XOR queries:      {ans1_total / total:.4f}  (no-lift prediction ~0.5)")
    print(f"P(>=1 queried var free):                  {free_total / total:.4f}")
    print(f"P(>=1 queried var free | ans=1):          "
          f"{ans1_with_free / max(ans1_total, 1):.4f}  (no-lift prediction ~ {free_total / total:.4f})")
    print(f"single-variable reference P(ans=1):       {single_ans1 / single_total:.4f} "
          f"(lift present: 0.036 expected)")
    print(f"posterior comparison: single-var ~0.26 lift vs multi-var "
          f"{ans1_with_free / max(ans1_total, 1):.4f} (no lift)")


if __name__ == "__main__":
    main()
