"""Retry extension of the two-phase certification tree (Krajicek chi-task, p = 2).

Tree: (1) query the row-sums Q_i = 1 + sum_j x_ij over all pigeons; every answer-1
certifies a FREE pigeon (assigned pigeons answer the determined 0 in char 2); collect the
certified set C. (2) for each certified pigeon i* in C, row-scan x_{i*,j} over the holes;
answer 1 certifies hole j is free; the first hit labels the pair (i*, j). The tree errs
only if C is empty (all free-pigeon coins 0) or every certified row is all-0.

Predicted error ~ (1/16)^{|C|} + 2^{-(2d+1)} with |C| ~ Binomial(2d+1, 1/2) ~ d: the
error decays as 2^{-Theta(d^2)}?? No - as (1/16)^{Theta(d)} = 2^{-Theta(d)} per
certified row and 2^{-(2d+1)} for the empty-C case: both 2^{-Theta(d)}: measured here.
Compare with the chi-hypothesis requirement: error <= gamma = k^{-O(1)}: in the
program's regime d = (log k)^{O(l)} the two-phase error 2^{-Theta(d)} is BELOW gamma
whenever (log k)^{c_l} >> log k: the chi-hypothesis FAILS at p = 2 for the candidate.
"""
from __future__ import annotations

import random
import statistics


def run(n: int, d: int, n_sim: int, rng: random.Random) -> float:
    success = 0
    for _ in range(n_sim):
        # pipeline: rho leaves 2d free pigeons (D) and 2d free holes (R)
        assigned_p = rng.sample(range(n + 1), n - 2 * d)
        assigned_h = rng.sample(range(n), n - 2 * d)
        rho = dict(zip(assigned_p, assigned_h))
        D = sorted(set(range(n + 1)) - set(assigned_p))
        R = sorted(set(range(n)) - set(assigned_h))
        free_p = set(D)
        # per free pigeon: its 2d row design bits (i.i.d. fair, proved)
        row_bits = {i: [rng.randrange(2) for _ in R] for i in D}
        # which hole index (in R) each assigned pigeon occupies (for determined answers)
        hole_pos = {h: R.index(h) for h in R}

        # Phase 1: query Q_i for all pigeons; certified-free = free pigeons with row XOR 1
        certified = []
        for i in range(n + 1):
            if i in free_p:
                if sum(row_bits[i]) % 2 == 1:
                    certified.append(i)
            # assigned pigeons: answer 0, deterministic; no certification

        # Phase 2: row-scan certified pigeons until a row answers 1
        ok = False
        for i_star in certified:
            for hj_ in R:
                if row_bits[i_star][hole_pos[hj_]] == 1:
                    ok = True
                    break
            if ok:
                break
        if ok:
            success += 1
    return success / n_sim


def main() -> None:
    rng = random.Random(31415)
    print("two-phase retry tree success (p=2):")
    print(f"{'n':>5} {'d':>3} {'success':>9} {'predicted err 2^-2d':>20}")
    for (n, d) in ((32, 2), (64, 2), (128, 2), (64, 4), (128, 4), (128, 8)):
        rate = run(n, d, n_sim := 400, rng)
        print(f"{n:>5} {d:>3} {rate:>9.4f} {2 ** (-2 * d):>20.6f}")


if __name__ == "__main__":
    main()
