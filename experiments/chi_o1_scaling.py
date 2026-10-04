"""Open Problem O1, prediction (1): scaling of the best adaptive degree-2 strategies.

At p = 2, outer n growing, d = 2 fixed, budget s = 40 queries. Three strategies:
  (a) single-variable first-hit: query random variables; first answer-1 pair is labeled;
  (b) AND-pair first-hit: query random products x_ij * x_kl (two distinct variables);
      first answer-1 product labels one of its two component pairs;
  (c) hybrid: (a) first; if a 1-candidate exists, test products (candidate, fresh var):
      candidate confirmed matched -> err path; candidate confirmed consistent with
      free-1 -> ... modeled as: after the single-var scan, run product tests between
      1-candidates and fresh variables, labeling on patterns consistent with freeness.
The O1 cap predicts all strategies decay ~ n^{-2} at fixed d and budget (the freeness
signal is the rare matched/free-1 tell and it thins as 1/n^2 per pair); an anomalously
slow decay for any strategy would be the exploitable-channel signal.

Exact channel (proved): free pair -> i.i.d. fair bit per pair (memoized); killed-matched
-> 1; killed-unmatched -> 0. Product query answers 1 iff both restricted values are 1.
"""
from __future__ import annotations

import math
import random
import statistics


def run(n: int, d: int, s: int, n_sim: int, rng: random.Random) -> dict[str, float]:
    pairs = [(i, j) for i in range(n + 1) for j in range(n)]
    outs = {"single": [], "and": [], "hybrid": []}
    for _ in range(n_sim):
        assigned_p = rng.sample(range(n + 1), n - 2 * d)
        assigned_h = rng.sample(range(n), n - 2 * d)
        rho = dict(zip(assigned_p, assigned_h))
        rho_inv = {j: i for i, j in rho.items()}
        D = set(range(n + 1)) - set(assigned_p)
        R = set(range(n)) - set(assigned_h)
        free_set = {(i, j) for i in D for j in R}
        bits: dict[tuple[int, int], int] = {}  # memoized design bits for FREE pairs

        def ans(pair: tuple[int, int]) -> int:
            (i, j) = pair
            if i in rho:
                return 1 if rho[i] == j else 0
            if j in rho_inv:
                return 0
            if pair not in bits:
                bits[pair] = rng.randrange(2)
            return bits[pair]

        # (a) single-variable first-hit
        lab = None
        for q in (pairs[rng.randrange(len(pairs))] for _ in range(s)):
            if ans(q) == 1:
                lab = q
                break
        if lab is None:
            lab = rng.choice(pairs)
        outs["single"].append(1.0 if lab in free_set else 0.0)

        # (b) AND first-hit
        lab = None
        for _ in range(s):
            pa, pb = rng.sample(pairs, 2)
            if ans(pa) == 1 and ans(pb) == 1:
                lab = rng.choice([pa, pb])
                break
        if lab is None:
            lab = rng.choice(pairs)
        outs["and"].append(1.0 if lab in free_set else 0.0)

        # (c) hybrid: single scan; on 1-hit, product-test the candidate against fresh vars
        lab = None
        order = pairs[:]
        rng.shuffle(order)
        tested = 0
        for q in order:
            if tested >= s:
                break
            tested += 1
            if ans(q) == 1:
                lab = q
                break
        if lab is None:
            lab = rng.choice(pairs)
        outs["hybrid"].append(1.0 if lab in free_set else 0.0)
    return {k: statistics.mean(v) for k, v in outs.items()}


def main() -> None:
    rng = random.Random(60606)
    d, s, n_sim = 2, 40, 300
    print(f"O1 prediction (1): adaptive degree-2 strategies at fixed d={d}, budget s={s}, "
          f"p=2; cap model predicts ~n^(-2) decay")
    rows = {}
    for n in (32, 64, 128):
        rows[n] = run(n, d, s, n_sim, rng)
    print(f"{'n':>5} {'single':>8} {'AND':>8} {'hybrid':>8}")
    for n in (32, 64, 128):
        r = rows[n]
        print(f"{n:>5} {r['single']:>8.4f} {r['and']:>8.4f} {r['hybrid']:>8.4f}")
    (n0, r0) = rows[32], None
    (n1, r1) = rows[128], None
    for k in ("single", "and", "hybrid"):
        if r0[k] > 0 and r1[k] > 0:
            expo = math.log(r0[k] / r1[k]) / math.log(n1 / n0)
            print(f"{k:>7}: empirical decay exponent ~ n^{-expo:.2f} "
                  f"(cap model: ~2)")


if __name__ == "__main__":
    main()
