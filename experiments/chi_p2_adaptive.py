"""p=2 adaptive-lift experiment for the Krajicek chi-task (arXiv:2609.35927, Thm 6.1).

Question: at p = 2, do adaptive trees beat fixed-label trees on Omega(n,d) instances?
Setting: outer system -PHP_n, n = 32, d = 2; restrictions rho leave 5 free pigeons and
4 free holes (n_rho = 2d = 4); designs L uniform over the affine space Des(4,2)
(kills V(4,2), L(1) = 1; dimension 65). A depth-1 adaptive tree queries candidate outer
variables x_ij in some order; at p = 2 every answer is a bit:
  - (i,j) free:                        answer = L(x_ij), fair coin over random L;
  - (i,j) killed, matched (rho(i)=j):  answer = 1, determined;
  - (i,j) killed, unmatched:           answer = 0, determined.
So P(answer = 1) = P(free)/2 + P(killed-matched), giving posterior
P(free | answer = 1) = (P(free)/2) / P(answer = 1) ~ 0.26 at these parameters, versus the
fixed-label baseline P(free) ~ 0.019. The experiment measures both by exact GF(2) sampling
of uniform designs over the augmented constraint system.
"""
from __future__ import annotations

import random
import statistics

from razborov_check import gf2_rank, monomials, shift, system_polys, to_vec

CANON_N = 4  # restricted system: 5 pigeons, 4 holes


def build() -> tuple[list[int], dict[tuple[int, ...], int]]:
    """Kernel basis of {L : L kills V(4,2), L(constant) = 0}; designs are e_0 + kernel.

    The augmented constraint row e_0 forces L(constant) = 1; every kernel vector then has
    constant-coordinate 0, so e_0 + a random subset is a uniform design.
    """
    monos = monomials(CANON_N, 2)
    mono_index = {t: i for i, t in enumerate(monos)}
    n_monos = len(monos)
    polys = system_polys(CANON_N)
    gens = []
    for f in polys:
        df = max(len(t) for t in f)
        for mono in monos:
            if len(mono) + df <= 2:
                gens.append(to_vec(shift(f, mono), mono_index))
    rows = gens + [1]  # e_0: force L(constant) = 1
    _, pivots = gf2_rank(rows)
    pivot_cols = sorted(p.bit_length() - 1 for p in pivots)
    col_row = dict(zip(pivot_cols, pivots))
    kernel2: list[int] = []
    for fc in range(n_monos):
        if fc in col_row:
            continue
        y = 1 << fc
        for c in pivot_cols:  # ascending: rows have support only at columns <= their pivot
            p = col_row[c]
            mask = p & ~(1 << c)
            if bin(y & mask).count("1") & 1:
                y |= 1 << c
        kernel2.append(y)
    return kernel2, mono_index


def main() -> None:
    kernel2, mono_index = build()
    rng = random.Random(20261)
    const_vec = 1 << mono_index[tuple()]
    n, d = 32, 2
    outer_pairs = [(i, j) for i in range(n + 1) for j in range(n)]
    n_sim = 300

    def sample_design() -> int:
        L = const_vec
        for k in kernel2:
            if rng.random() < 0.5:
                L ^= k
        return L

    def sample_rho() -> tuple[dict[int, int], list[int], list[int]]:
        assigned_p = rng.sample(range(n + 1), n - 2 * d)
        assigned_h = rng.sample(range(n), n - 2 * d)
        rho = dict(zip(assigned_p, assigned_h))
        D = sorted(set(range(n + 1)) - set(assigned_p))
        R = sorted(set(range(n)) - set(assigned_h))
        return rho, D, R

    fixed_success = []
    adapt_success = []
    for _ in range(n_sim):
        L = sample_design()
        rho, D, R = sample_rho()
        rho_inv = {j: i for i, j in rho.items()}
        free_set = {(i, j) for i in D for j in R}
        lab = rng.choice(outer_pairs)
        fixed_success.append(1.0 if lab in free_set else 0.0)
        order = outer_pairs[:]
        rng.shuffle(order)
        chosen = None
        for (i, j) in order:
            if i in rho:
                ans = 1 if rho[i] == j else 0
            elif j in rho_inv:
                ans = 0
            else:
                cv = D.index(i) * CANON_N + R.index(j)
                ans = (L >> cv) & 1
            if ans == 1:
                chosen = (i, j)
                break
        if chosen is None:
            chosen = order[-1]
        adapt_success.append(1.0 if chosen in free_set else 0.0)

    p_free = ((2 * d + 1) / (n + 1)) * (2 * d / n)
    p_match = ((n - 2 * d) / (n + 1)) * (1 / n)
    p_ans1 = p_free / 2 + p_match
    posterior = (p_free / 2) / p_ans1
    print(f"outer n={n}, d={d}, p=2, simulations={n_sim}, design dim = {len(kernel2)}")
    print(f"analytic: P(free)={p_free:.4f}  P(ans=1)={p_ans1:.4f}  "
          f"posterior P(free|ans=1)={posterior:.4f}")
    print(f"fixed-label success:  mean {statistics.mean(fixed_success):.4f}")
    print(f"adaptive success:     mean {statistics.mean(adapt_success):.4f} "
          f"(median {statistics.median(adapt_success):.2f})")
    print(f"analytic adaptive prediction ~ posterior * P(hit in 33 queries) = "
          f"{posterior * (1 - (1 - p_ans1) ** 33):.4f}")


if __name__ == "__main__":
    main()
