"""Scaling-law test: p=2 adaptive success vs n at fixed d and fixed query budget.

Prediction from the rare-event analysis (chi_p2_multivar.py context): at fixed d = 2 and a
fixed candidate budget s, the depth-1 adaptive strategy's success (leaf label is free)
scales as ~Theta(1/n^2): the answer-1 hit probability is ~s/n (dominated by the rare
killed-matched event) and the hit posterior is ~20/n (free density over matched density),
with the fallback label free with probability ~20/n^2.

Measuring at n = 32, 64, 128 with s = 25, d = 2, p = 2, designs sampled exactly.
"""
from __future__ import annotations

import random
import statistics

from chi_p2_adaptive import build, CANON_N


def main() -> None:
    kernel2, mono_index = build()
    rng = random.Random(777)
    d = 2
    s = 25  # fixed candidate budget
    n_sim = 400

    print(f"fixed d={d}, budget s={s}, simulations={n_sim}")
    print(f"{'n':>5} {'success':>9} {'pred ~C/n^2':>12}")
    results = []
    for n in (32, 64, 128):
        outer_pairs = [(i, j) for i in range(n + 1) for j in range(n)]
        success = []
        for _ in range(n_sim):
            L = 1 << mono_index[tuple()]  # L(constant) = 1
            for k in kernel2:
                if rng.random() < 0.5:
                    L ^= k
            assigned_p = rng.sample(range(n + 1), n - 2 * d)
            assigned_h = rng.sample(range(n), n - 2 * d)
            rho = dict(zip(assigned_p, assigned_h))
            D = sorted(set(range(n + 1)) - set(assigned_p))
            R = sorted(set(range(n)) - set(assigned_h))
            free_set = {(i, j) for i in D for j in R}
            order = outer_pairs[:]
            rng.shuffle(order)
            chosen = None
            for (i, j) in order[:s]:
                if i in rho:
                    ans = 1 if rho[i] == j else 0
                elif j in {jj for ii, jj in rho.items()}:
                    ans = 0
                else:
                    cv = D.index(i) * CANON_N + R.index(j)
                    ans = (L >> cv) & 1
                if ans == 1:
                    chosen = (i, j)
                    break
            if chosen is None:
                chosen = order[s] if s < len(order) else order[-1]
            success.append(1.0 if chosen in free_set else 0.0)
        mean = statistics.mean(success)
        results.append((n, mean))
        print(f"{n:>5} {mean:>9.4f} {results[0][1] * (results[0][0] / n) ** 2:>12.4f}"
              if n != 32 else
              f"{n:>5} {mean:>9.4f} {'(reference)':>12}")
    # scaling exponent fit: log success ~ -a log n
    import math
    if len(results) >= 2 and all(m > 0 for (_, m) in results):
        (n0, m0), (n1, m1) = results[0], results[-1]
        expo = math.log(m0 / m1) / math.log(n1 / n0)
        print(f"empirical scaling: success ~ n^{-expo:.2f} "
              f"(n^{'-2'} predicted by the matched-rarity cap)")


if __name__ == "__main__":
    main()
