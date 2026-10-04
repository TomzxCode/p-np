"""Exact measurement of the AND-query freeness posterior at p = 2.

Question: for product queries x_ab * x_cd on the Omega(32,2) pipeline, what is
  P(ans = 1)   and   P[pa free | ans = 1] ?
This settles (with data, not analysis) whether AND-queries carry a stronger freeness
posterior than single-variable queries (single-var: P(ans=1) ~ 0.036, posterior ~ 0.26).

Method: exact channel simulation (proved law: free pair -> i.i.d. fair design bit;
killed-unmatched -> 0; killed-matched -> 1). For each sample (rho, L): many random
distinct pair-pairs (pa, pb); record (ans = 1, pa's freeness). Estimates with 95% CIs.
"""
from __future__ import annotations

import math
import random
import statistics

from chi_p2_adaptive import build

CANON_N = 4


def main() -> None:
    kernel2, mono_index = build()
    rng = random.Random(9182)
    const_vec = 1 << mono_index[tuple()]
    n, d = 32, 2
    outer_pairs = [(i, j) for i in range(n + 1) for j in range(n)]
    n_sim = 400
    n_qp = 200  # product queries per sample

    ans1 = 0
    ans1_free = 0
    ans1_bothfree = 0
    total = 0
    pa_free_given_ans1 = []

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
        free_set = {(i, j) for i in D for j in R}

        # design value of a queried outer variable, fixed for this (rho, L) sample:
        # free -> the variable's own design bit (fair, proved); killed-unmatched -> 0;
        # killed-matched -> 1.
        def val(pair: tuple[int, int]) -> int:
            (i, j) = pair
            if i in rho:
                return 1 if rho[i] == j else 0
            if j in rho_inv:
                return 0
            cv = canon[(i, j)]
            return (L >> cv) & 1

        for _ in range(n_qp):
            pa, pb = rng.sample(outer_pairs, 2)
            a1 = (val(pa) == 1) and (val(pb) == 1)
            total += 1
            if a1:
                ans1 += 1
                pa_free = pa in free_set
                ans1_free += pa_free
                if pb in free_set:
                    ans1_bothfree += 1

    print(f"outer n={n}, d={d}, p=2; samples={n_sim}, product-queries={n_qp}/sample, "
          f"total={total}")
    r1 = ans1 / total
    ci = 1.96 * math.sqrt(max(r1 * (1 - r1), 1e-12) / total)
    print(f"P(ans=1)            = {r1:.5f} +/- {ci:.5f}")
    if ans1:
        rf = ans1_free / ans1
        cif = 1.96 * math.sqrt(rf * (1 - rf) / ans1)
        print(f"P[pa free | ans=1]  = {rf:.4f} +/- {cif:.4f}")
        rb = ans1_bothfree / ans1
        cib = 1.96 * math.sqrt(rb * (1 - rb) / ans1)
        print(f"P[both free | ans=1] = {rb:.4f} +/- {cib:.4f}")
    print("single-variable reference: P(ans=1) ~ 0.036, posterior ~ 0.26")
    print("base rate P(free pair) ~ 0.019")


if __name__ == "__main__":
    main()
