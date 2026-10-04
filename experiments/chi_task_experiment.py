"""Toy-scale empirical estimate of the Krajicek chi-quantity (arXiv:2609.35927, Thm 6.1).

Setting: outer system -PHP_n with n = 8 (9 pigeons, 8 holes), degree d = 2, over GF(2).
Restrictions rho leave exactly n_rho = 2d = 4 free holes (and 5 free pigeons), matching the
Omega(n,d) construction (Def 4.3 of arXiv:2609.35927). Designs L are drawn conceptually from
Des(4,2) (dimension 65, verified in razborov_check.py); the tree's answers along a path are
the path's edge labels, so Theorem 6.1's quantity Prob_{rho,P}[chi(P,rho)=1] is computable
without sampling L at all:

chi(P, rho) = 1  iff  lab(P) not in D^rho x R^rho  AND  1 not in Span(V(4,2) + {g^rho + a}
over the path's queries g with answers a).

We sample random depth-2 decision-list trees (one random degree-2 monomial query per level,
fixed random leaf label) and report the distribution of per-tree chi-probabilities, plus the
marginals of the two conditions. Toy scale only: the conjecture concerns optimal trees at
d = n^{delta'}; this calibrates the quantity, it does not test the asymptotic claim.
"""
from __future__ import annotations

import random
import statistics

from razborov_check import gf2_rank, monomials, shift, system_polys, to_vec

CANON_N = 4  # restricted system: 5 pigeons, 4 holes


def build_canonical() -> tuple[list[int], dict[tuple[int, ...], int], list[tuple[int, ...]]]:
    monos = monomials(CANON_N, 2)
    mono_index = {t: i for i, t in enumerate(monos)}
    polys = system_polys(CANON_N)
    gens = []
    for f in polys:
        df = max(len(t) for t in f)
        for mono in monos:
            if len(mono) + df <= 2:
                gens.append(to_vec(shift(f, mono), mono_index))
    _, basis = gf2_rank(gens)
    basis_sorted = sorted(basis, key=lambda x: x.bit_length(), reverse=True)
    return basis_sorted, mono_index, monos


def reduce_against(vec: int, pivots_desc: list[int]) -> int:
    for p in pivots_desc:
        h = p.bit_length() - 1
        if (vec >> h) & 1:
            vec ^= p
    return vec


def span_contains(vec: int, basis_desc: list[int], extra: list[int]) -> bool:
    """Is vec in span(basis + extras)?  extras may contain at most 2 vectors."""
    piv = list(basis_desc)
    for e in sorted(extra, key=lambda x: x.bit_length(), reverse=True):
        r = reduce_against(e, piv)
        if r:
            # insert r keeping decreasing order
            for idx, p in enumerate(piv):
                if r.bit_length() > p.bit_length():
                    piv.insert(idx, r)
                    break
            else:
                piv.append(r)
    return reduce_against(vec, piv) == 0


def main() -> None:
    n, d = 8, 2
    rng = random.Random(2026)
    basis_desc, mono_index4, monos4 = build_canonical()
    const_vec = 1 << mono_index4[tuple()]
    outer_pairs = [(i, j) for i in range(n + 1) for j in range(n)]

    n_trees, n_rho = 60, 100
    tree_probs: list[float] = []
    cond1_all: list[float] = []
    cond2_all: list[float] = []

    for _ in range(n_trees):
        q1 = tuple(sorted(rng.sample(outer_pairs, 2)))
        q2 = tuple(sorted(rng.sample(outer_pairs, 2)))
        lab = rng.choice(outer_pairs)
        path_chi = [0] * 4
        path_c1 = [0] * 4
        path_c2 = [0] * 4
        for _ in range(n_rho):
            assigned_p = rng.sample(range(n + 1), n - 2 * d)
            assigned_h = rng.sample(range(n), n - 2 * d)
            rho = dict(zip(assigned_p, assigned_h))
            rho_inv = {j: i for i, j in rho.items()}
            D = sorted(set(range(n + 1)) - set(assigned_p))
            R = sorted(set(range(n)) - set(assigned_h))
            D_set, R_set = set(D), set(R)

            def canon(i: int, j: int) -> int:
                return (D.index(i)) * CANON_N + (R.index(j))

            def restrict(t: tuple[int, ...]) -> dict[tuple[int, ...], int]:
                terms: dict[tuple[int, ...], int] = {(): 1}
                for (i, j) in t:
                    if i in rho:
                        if rho[i] != j:
                            return {}
                    elif j in rho_inv:
                        return {}
                    else:
                        cv = canon(i, j)
                        terms = {tuple(sorted(tt + (cv,))): cc for tt, cc in terms.items()}
                return terms

            for pi_, (a1, a2) in enumerate([(0, 0), (0, 1), (1, 0), (1, 1)]):
                cond1 = lab not in {(i, j) for i in D for j in R}
                path_c1[pi_] += cond1
                g1r = to_vec(restrict(q1), mono_index4)
                g2r = to_vec(restrict(q2), mono_index4)
                c1v = g1r ^ (const_vec if a1 else 0)
                c2v = g2r ^ (const_vec if a2 else 0)
                one_in = span_contains(const_vec, basis_desc, [c1v, c2v])
                path_c2[pi_] += one_in
                if cond1 and not one_in:
                    path_chi[pi_] += 1
        for pi_ in range(4):
            cond1_all.append(path_c1[pi_] / n_rho)
            cond2_all.append(path_c2[pi_] / n_rho)
            tree_probs.append(path_chi[pi_] / n_rho)

    def stats(xs: list[float]) -> tuple[float, float, float]:
        return min(xs), statistics.median(xs), max(xs)

    print(f"trees={n_trees}, rho-samples={n_rho}; n={n}, d={d}, p=2; "
          f"tree family: depth-2 decision lists, degree-2 monomial queries")
    mn, md, mx = stats(tree_probs)
    print(f"chi probability per tree:  min {mn:.4f}  median {md:.4f}  max {mx:.4f}")
    mn, md, mx = stats(cond1_all)
    print(f"cond 1 (lab not free):     min {mn:.4f}  median {md:.4f}  max {mx:.4f}")
    mn, md, mx = stats(cond2_all)
    print(f"cond 2 (1 in span):        min {mn:.4f}  median {md:.4f}  max {mx:.4f}")
    print(f"paths with cond1: {sum(1 for x in cond1_all if x > 0.5)} of {len(cond1_all)}")


if __name__ == "__main__":
    main()
