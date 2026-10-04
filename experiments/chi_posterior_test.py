"""Threshold test for the p=2 answer-1 posterior (fast exact version).

Proven shortcut: in the augmented design space (L kills V(2d,2), L(1)=1), the kernel basis
vectors each have disjoint single-variable free-column support, so for uniform random L the
values L(x_ij) on free pairs are i.i.d. fair bits over GF(2). Hence the Omega(n,d) answer
channel at p=2 is exactly:
  - (i,j) free:            fair independent coin;
  - (i,j) killed-matched:  answer 1 (determined);
  - (i,j) killed-unmatched: answer 0 (determined).
This makes the depth-1 adaptive strategy's success exactly simulable in O(1) per query.

Prediction: success of the first-answer-1 strategy ~ q = (P(free)/2) / (P(free)/2 + P(matched))
with P(free) ~ ((2d+1)/(n+1)) * (2d/n), P(matched) ~ (1/n)*(1 - 2d/n) — crossing 1/2 at
d ~ sqrt(n/2), i.e., q -> 1 in the regime d >> sqrt(n), where Theorem 6.1's chi-hypothesis
is threatened (trees would avoid error with probability -> 1 - k^{-O(1)}).
"""
from __future__ import annotations

import random
import statistics


def main() -> None:
    rng = random.Random(4242)
    n = 128
    s = 40
    n_sim = 500

    print(f"outer n={n}, candidate budget s={s}, simulations={n_sim}")
    print(f"{'d':>4} {'2d^2/(2d^2+n)':>14} {'success':>9} {'base P(free)':>13}")
    for d in (2, 4, 8, 11, 16, 24, 32):
        outer_pairs = [(i, j) for i in range(n + 1) for j in range(n)]
        success = []
        for _ in range(n_sim):
            assigned_p = rng.sample(range(n + 1), n - 2 * d)
            assigned_h = rng.sample(range(n), n - 2 * d)
            rho = dict(zip(assigned_p, assigned_h))
            rho_inv = {j: i for i, j in rho.items()}
            D = set(range(n + 1)) - set(assigned_p)
            R = set(range(n)) - set(assigned_h)
            free_set = {(i, j) for i in D for j in R}
            order = outer_pairs[:]
            rng.shuffle(order)
            chosen = None
            for (i, j) in order[:s]:
                if i in rho:
                    ans = 1 if rho[i] == j else 0
                elif j in rho_inv:
                    ans = 0
                else:
                    ans = rng.randrange(2)  # free: exact fair coin (proven above)
                if ans == 1:
                    chosen = (i, j)
                    break
            if chosen is None:
                chosen = order[s] if s < len(order) else order[-1]
            success.append(1.0 if chosen in free_set else 0.0)
        p_free = ((2 * d + 1) / (n + 1)) * (2 * d / n)
        p_match = ((n - 2 * d) / (n + 1)) * (1 / n)
        q_pred = (p_free / 2) / (p_free / 2 + p_match) if (p_free / 2 + p_match) else float("nan")
        mean = statistics.mean(success)
        print(f"{d:>4} {q_pred:>14.3f} {mean:>9.4f} {p_free:>13.4f}")


if __name__ == "__main__":
    main()
