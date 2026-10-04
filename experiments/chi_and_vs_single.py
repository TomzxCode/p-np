"""AND-query vs single-variable labeling at p=2 (Krajicek chi-task toy experiment).

Compares two tree strategies on the Omega(32,2) pipeline at p=2 with equal budget e' = 3000
queries:
  (a) single-variable scan: query outer variables x_ij; first answer-1 pair is labeled;
  (b) AND-scan: query products x_ij * x_kl (two distinct random outer pairs); the first
      answer-1 product labels one of its two component pairs (uniform choice).
Predictions (per-pair Bayes from the exact answer-channel law):
  (a) labeled pair free with probability ~ q = (f/2)/(f/2+m) ~ 0.26 once a hit occurs;
  (b) an answer-1 certifies BOTH component pairs are not killed-unmatched, giving each
      ~0.42 freeness posterior - HIGHER than (a), at a rarer hit rate (~1.2e-3/query).
Success metric: labeled pair in D^rho x R^rho (the tree avoids error in the Thm 6.1 sense).
"""
from __future__ import annotations

import random
import statistics

from chi_p2_adaptive import build

CANON_N = 4


def main() -> None:
    kernel2, mono_index = build()
    rng = random.Random(31337)
    const_vec = 1 << mono_index[tuple()]
    n, d = 32, 2
    outer_pairs = [(i, j) for i in range(n + 1) for j in range(n)]
    n_sim = 500
    budget = 3000

    single_success = []
    and_success = []

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

        def var_ans(pair: tuple[int, int]) -> int:
            (i, j) = pair
            if i in rho:
                return 1 if rho[i] == j else 0
            if j in rho_inv:
                return 0
            return (L >> canon[(i, j)]) & 1

        # (a) single-variable scan
        lab_single = None
        for (i, j) in (rng.choices(outer_pairs, k=budget)):
            if var_ans((i, j)) == 1:
                lab_single = (i, j)
                break
        if lab_single is None:
            lab_single = rng.choice(outer_pairs)
        single_success.append(1.0 if lab_single in free_set else 0.0)

        # (b) AND scan: product queries over random distinct pair-pairs
        lab_and = None
        for _ in range(budget):
            pa, pb = rng.sample(outer_pairs, 2)
            va = var_ans(pa)
            vb = var_ans(pb)
            if va == 1 and vb == 1:
                lab_and = rng.choice([pa, pb])
                break
        if lab_and is None:
            lab_and = rng.choice(outer_pairs)
        and_success.append(1.0 if lab_and in free_set else 0.0)

    print(f"outer n={n}, d={d}, p=2, simulations={n_sim}, budget={budget} queries")
    print(f"(a) single-variable first-hit success: "
          f"{statistics.mean(single_success):.4f} (median {statistics.median(single_success):.2f})")
    print(f"(b) AND-query first-hit success:       "
          f"{statistics.mean(and_success):.4f} (median {statistics.median(and_success):.2f})")
    print("(Bayes prediction: (a) -> 0.26; (b) -> ~0.41 per hit)")


if __name__ == "__main__":
    main()
