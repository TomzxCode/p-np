"""Where does DPLL actually struggle? Locate genuinely hard CNF families and measure growth.

Phase A: random 3-XOR systems. For each (n, density), measure the unsatisfiability rate and
the size of the inconsistent row-subset found by GF(2) elimination (an upper bound on the
minimal unsat core). A core over c variables bounds any DPLL refutation by roughly 2^c nodes,
so small cores mean the family is easy for search regardless of resolution theory.

Phase B: DPLL node growth on (i) the best XOR regime found by phase A, and (ii) the pigeonhole
principle PHP_{h+1}^h, which has a provably exponential resolution lower bound (Haken 1985).
"""
from __future__ import annotations

import random
import statistics
import time

from sat_scaling import (
    NodeBudgetExceeded,
    NodeCounter,
    dpll,
    tseitin_xor_gate,
)


def build_xor(n: int, m: int, seed: int):
    """Planted random 3-XOR system, m equations, last parity flipped.

    Returns (rows, clauses): rows are (varmask, parity); clauses is the Tseitin CNF.
    """
    rng = random.Random(seed)
    planted = [rng.random() < 0.5 for _ in range(n + 1)]
    rows: list[tuple[int, int]] = []
    clauses: list[list[int]] = []
    aux = n + 1
    for i in range(m):
        vs = rng.sample(range(1, n + 1), 3)
        parity = planted[vs[0]] ^ planted[vs[1]] ^ planted[vs[2]]
        if i == m - 1:
            parity ^= 1
        mask = (1 << vs[0]) | (1 << vs[1]) | (1 << vs[2])
        rows.append((mask, parity))
        d, r = aux, aux + 1
        aux += 2
        clauses.extend(tseitin_xor_gate(vs[0], vs[1], d))
        clauses.extend(tseitin_xor_gate(d, vs[2], r))
        clauses.append([r] if parity else [-r])
    return rows, clauses


def eliminate(rows: list[tuple[int, int]]) -> tuple[int, int | None]:
    """GF(2) elimination. Returns (rank, comb): comb is a bitmask over row indices whose rows
    sum to 0 with parity 1 (an inconsistent subsystem) if the system is unsatisfiable."""
    pivots: dict[int, tuple[int, int, int]] = {}
    for i, (mask, par) in enumerate(rows):
        msk, p, comb = mask, par, 1 << i
        while msk:
            h = msk.bit_length() - 1
            if h in pivots:
                pm, pp, pc = pivots[h]
                msk ^= pm
                p ^= pp
                comb ^= pc
            else:
                pivots[h] = (msk, p, comb)
                break
        else:
            if p:
                return len(pivots), comb
    return len(pivots), None


def phase_a() -> float:
    print("phase A: XOR unsat rate and core-size upper bound (single elimination dependency)")
    print(f"{'n':>4} {'alpha':>6} {'unsat':>6} {'med core':>9} {'max core':>9}")
    best_alpha = 2.8
    best_score = -1.0
    for n in (20, 40, 80):
        for alpha10 in (12, 16, 20, 24, 28, 32):
            alpha = alpha10 / 10.0
            m = int(round(alpha * n))
            unsat = 0
            cores: list[int] = []
            for s in range(5):
                rows, _ = build_xor(n, m, 7000 * n + 101 * alpha10 + s)
                _, comb = eliminate(rows)
                if comb is not None:
                    unsat += 1
                    cores.append(bin(comb).count("1"))
            med = statistics.median(cores) if cores else 0.0
            mx = max(cores) if cores else 0
            print(f"{n:>4} {alpha:>6.1f} {unsat:>3}/5 {med:>9.0f} {mx:>9}")
            # prefer regimes that are always unsat with large cores
            score = unsat * 1000 + med + mx / 10.0
            if n == 40 and score > best_score:
                best_score = score
                best_alpha = alpha
    print(f"selected alpha for phase B: {best_alpha}")
    return best_alpha


def xor_unsat_instance(n: int, alpha: float, k: int) -> list[list[int]] | None:
    """Return the Tseitin CNF of a truly unsatisfiable XOR system, or None after 8 tries."""
    m = int(round(alpha * n))
    for s in range(8):
        rows, clauses = build_xor(n, m, 90000 * n + 131 * int(alpha * 10) + k * 7 + s)
        _, comb = eliminate(rows)
        if comb is not None:
            return clauses
    return None


def php_formula(h: int) -> list[list[int]]:
    """Pigeonhole principle PHP_{h+1}^h: variables p(i, j) = pigeon i sits in hole j."""
    var: dict[tuple[int, int], int] = {}

    def v(i: int, j: int) -> int:
        return var.setdefault((i, j), len(var) + 1)

    clauses: list[list[int]] = []
    for i in range(h + 1):
        clauses.append([v(i, j) for j in range(1, h + 1)])
    for i1 in range(h + 1):
        for i2 in range(i1 + 1, h + 1):
            for j in range(1, h + 1):
                clauses.append([-v(i1, j), -v(i2, j)])
    return clauses


def run_family(label: str, make_formula, sizes: list[int], instances: int, cap: int) -> None:
    print(f"\n=== {label} ===")
    print(f"{'size':>5} {'med nodes':>10} {'max':>8} {'capped':>8}")
    for s in sizes:
        nodes: list[int] = []
        capped = 0
        for k in range(instances):
            formula = make_formula(s, k)
            if formula is None:
                continue
            counter = NodeCounter(cap)
            try:
                dpll(formula, counter)
            except NodeBudgetExceeded:
                capped += 1
            nodes.append(counter.value)
        med = statistics.median(nodes) if nodes else 0.0
        mx = max(nodes) if nodes else 0
        print(f"{s:>5} {med:>10.0f} {mx:>8} {capped:>4}/{instances}")


if __name__ == "__main__":
    alpha_star = phase_a()
    run_family(
        f"phase B1: XOR at alpha={alpha_star} (truly unsat instances only)",
        lambda n, k: xor_unsat_instance(n, alpha_star, k),
        sizes=[16, 24, 32],
        instances=3,
        cap=15000,
    )
    run_family(
        "phase B2: pigeonhole PHP_(h+1)^h (resolution-exponential by Haken)",
        lambda h, k: php_formula(h),
        sizes=[6, 8, 10, 12],
        instances=3,
        cap=15000,
    )
