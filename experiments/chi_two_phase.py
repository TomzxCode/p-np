"""Two-phase certification tree at p=2: does it break Omega(n,d) as a pseudo-solution?

Phase 1: query the pigeon-constraint polynomials Q_i = 1 + sum_j x_ij (degree 1).
  Assigned pigeon i: Q_i^rho = 1 + x_{i,rho(i)} = 0 (char 2) -> answer 0, DETERMINED.
  Free pigeon i:      Q_i^rho = 1 + sum_{j in R} x_ij -> fair coin (answer 1 w.p. 1/2).
  So answer 1 CERTIFIES pigeon i is free.
Phase 2: for a certified-free pigeon i*, query row variables x_{i*,j} for all holes j.
  j in R (free hole): fair coin; j in rng(rho): determined 0.
  So answer 1 CERTIFIES hole j is free -> the pair (i*, j) is in D x R: SUCCESS.

Predicted success at d = 2 (5 free pigeons, 4 free holes):
  error = P[no pigeon certifies] + P[pigeon certified but no hole-bit 1]
        ~ 2^{-(2d+1)}·(nothing) + 2^{-2d} = 1/16 ~ 0.0625, i.e., success ~ 0.94
  (up to fallback terms), versus the single-variable cap 0.26 and the chi-hypothesis
  requirement error >= k^{-O(1)} (tiny): the two-phase tree's CONSTANT error 2^{-2d}
  still satisfies error >= k^{-O(1)} for super-polynomial k, but it refutes Theorem B's
  cap extrapolation and shows the candidate Omega(n,2) fails against degree-1 adaptive
  trees UNLESS the Q_i certification is blocked (it is not: Q_i queries are degree-1,
  inside every stated tree class).
"""
from __future__ import annotations

import random
import statistics


def main() -> None:
    rng = random.Random(2718)
    n_sim = 500
    print(f"{'n':>5} {'d':>3} {'success':>9} {'pred err 2^-2d':>15}")
    for (n, d) in ((32, 2), (64, 2), (128, 2), (64, 4)):
        success = []
        for _ in range(n_sim):
            # pipeline: rho leaves 2d+1 free pigeons (D) and 2d free holes (R)
            assigned_p = rng.sample(range(n + 1), n - 2 * d)
            assigned_h = rng.sample(range(n), n - 2 * d)
            rho = dict(zip(assigned_p, assigned_h))
            rho_inv = {j: i for i, j in rho.items()}
            D = sorted(set(range(n + 1)) - set(assigned_p))
            R = sorted(set(range(n)) - set(assigned_h))
            free_p = set(D)
            # per free pigeon: its 2d row design bits (i.i.d. fair, proved)
            row_bits = {i: [rng.randrange(2) for _ in R] for i in D}

            # Phase 1: query Q_i for all pigeons until answer 1
            certified = None
            for i in range(n + 1):
                if i in free_p:
                    # free pigeon: Q_i^rho = 1 + XOR(row bits) -> answer 1 w.p. 1/2
                    if sum(row_bits[i]) % 2 == 1:
                        certified = i
                        break
                else:
                    pass  # assigned: answer 0, deterministic
            if certified is None:
                # no certification: fallback label, free w.p. base rate
                chosen = (rng.choice(range(n + 1)), rng.choice(range(n)))
                success.append(1.0 if chosen[0] in D and chosen[1] in R else 0.0)
                continue
            # Phase 2: row-scan the certified pigeon for a hole answering 1
            jstar = None
            for hj_ in R:
                if row_bits[certified][R.index(hj_)] == 1:
                    jstar = hj_
                    break
            success.append(1.0 if jstar is not None else 0.0)
        mean = statistics.mean(success)
        pred = 2 ** (-2 * d)
        print(f"{n:>5} {d:>3} {1-mean:>9.4f} {pred:>15.4f}")
        del success


if __name__ == "__main__":
    main()
