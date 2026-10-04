"""Adversarial search for high-chi trees (Krajicek arXiv:2609.35927, Theorem 6.1).

At d = 2 fixed and growing n, condition 1 of chi (leaf label not free under rho) stops
binding: Pr[free] = ((2d+1)/(n+1)) * (2d/n) -> 0, so the conjecture's near-1 chi-probability
reading lives in the regime d/n -> 0, and the real battleground is condition 2 (path
liveness). This script hill-climbs over depth-2 decision-list trees (queries q1, q2: random
degree-2 monomials over outer variables; fixed leaf label) for several n, evaluating chi on
a fixed rho pool, with restarts, and reports the best chi found against the condition-1 cap.
"""
from __future__ import annotations

import random
import statistics

from razborov_check import gf2_rank, monomials, shift, system_polys, to_vec

CANON_N = 4  # restricted system for d = 2: 5 pigeons, 4 holes


def build_canonical() -> list[int]:
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
    return sorted(basis, key=lambda x: x.bit_length(), reverse=True), mono_index


def reduce_against(vec: int, pivots_desc: list[int]) -> int:
    for p in pivots_desc:
        h = p.bit_length() - 1
        if (vec >> h) & 1:
            vec ^= p
    return vec


def span_contains(vec: int, basis_desc: list[int], extra: list[int]) -> bool:
    piv = list(basis_desc)
    for e in sorted(extra, key=lambda x: x.bit_length(), reverse=True):
        r = reduce_against(e, piv)
        if r:
            placed = False
            for idx, p in enumerate(piv):
                if r.bit_length() > p.bit_length():
                    piv.insert(idx, r)
                    placed = True
                    break
            if not placed:
                piv.append(r)
    return reduce_against(vec, piv) == 0


def main() -> None:
    d = 2
    rng = random.Random(4711)
    basis_desc, mono_index4 = build_canonical()
    const_vec = 1 << mono_index4[tuple()]

    for n in (8, 16, 32):
        outer_pairs = [(i, j) for i in range(n + 1) for j in range(n)]
        # fixed rho pool for fair comparisons within this n
        pool = []
        for _ in range(150):
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
            pool.append((rho, rho_inv, D, R, canon))

        def restrict(t: tuple[int, ...], entry) -> dict[tuple[int, ...], int]:
            rho, rho_inv, D, R, canon = entry
            terms: dict[tuple[int, ...], int] = {(): 1}
            for (i, j) in t:
                if i in rho:
                    if rho[i] != j:
                        return {}
                elif j in rho_inv:
                    return {}
                else:
                    cv = canon[(i, j)]
                    terms = {tuple(sorted(tt + (cv,))): cc for tt, cc in terms.items()}
            return terms

        def to_v(poly: dict[tuple[int, ...], int]) -> int:
            vec = 0
            for t in poly:
                vec ^= 1 << mono_index4[t]
            return vec

        def chi_prob(tree: tuple[tuple[int, ...], tuple[int, ...], tuple[int, ...]]) -> float:
            q1, q2, lab = tree
            hits = 0
            for (rho, rho_inv, D, R, canon) in pool:
                free_pairs = {(i, j) for i in D for j in R}
                if lab in free_pairs:
                    continue  # cond1 fails for every path -> chi = 0 on this rho
                extras = []
                alive = True
                for (g, a) in ((q1, 0), (q2, 0)):
                    # the tree queries with both branches; a live path needs the
                    # constraint g^rho + a consistent; we take the (0,0) label path
                    # per Lemma 5.2's uniform-path convention on this label assignment
                    gr = to_v(restrict(g, (rho, rho_inv, D, R, canon)))
                    extras.append(gr)  # answers a=0 -> constraint g^rho + 0
                if not alive:
                    continue
                one_vec = 1 << mono_index4[tuple()]
                # chi = 1 iff cond1 and 1 NOT in span(V + constraints)
                if not span_contains(one_vec, basis_desc, extras):
                    hits += 1
            return hits / len(pool)

        # condition-1 cap for the best fixed label: 1 - Pr[free] (max over labels,
        # estimated empirically)
        caps = []
        for lab in rng.sample(outer_pairs, 40):
            cap = sum(1 for (rho, rho_inv, D, R, _) in pool
                      if lab not in {(i, j) for i in D for j in R}) / len(pool)
            caps.append(cap)
        cond1_cap = max(caps)

        best_chi = 0.0
        best_tree = None
        for restart in range(4):
            cur = (tuple(sorted(rng.sample(outer_pairs, 2))),
                   tuple(sorted(rng.sample(outer_pairs, 2))),
                   rng.choice(outer_pairs))
            cur_chi = chi_prob(cur)
            for _ in range(50):
                cand = list(cur)
                which = rng.randrange(3)
                if which < 2:
                    cand[which] = tuple(sorted(rng.sample(outer_pairs, 2)))
                else:
                    cand[2] = rng.choice(outer_pairs)
                cand_chi = chi_prob(tuple(cand))
                if cand_chi > cur_chi:
                    cur, cur_chi = tuple(cand), cand_chi
            if cur_chi > best_chi:
                best_chi, best_tree = cur_chi, cur

        print(f"n={n}: best chi over search = {best_chi:.4f} "
              f"(cond1 cap ~ {cond1_cap:.4f}); best tree label pair = {best_tree[2]}")


if __name__ == "__main__":
    main()
