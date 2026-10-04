"""Empirical clue: how does a naive DPLL solver scale on different instance families?

Experiment 1: random 3-SAT at clause-to-variable ratio 4.26 (near the satisfiability
threshold ~4.267). Experiment 2: Tseitin-encoded random 3-variable XOR systems over GF(2),
planted-satisfiable and expanding w.h.p. (known to require exponential-size resolution
refutations on expander graphs, hence exponential DPLL search).

Flat medians on random 3-SAT with growing node counts on structured XOR instances expose
the average-case-easy / worst-case-hard split that sits at the heart of P vs NP.
"""
from __future__ import annotations

import random
import statistics
import time

RATIO = 4.26
SIZES = [14, 16, 18, 20, 22, 24, 26]
INSTANCES_PER_N = 15
NODE_CAP = 100_000


class NodeBudgetExceeded(Exception):
    """Raised when a single instance exceeds the solver's node budget."""


class NodeCounter:
    def __init__(self, cap: int) -> None:
        self.value = 0
        self.cap = cap

    def tick(self) -> None:
        self.value += 1
        if self.value > self.cap:
            raise NodeBudgetExceeded


def random_formula(n: int, m: int, seed: int) -> list[list[int]]:
    """Uniform random 3-CNF: m clauses, each 3 distinct variables, random polarities."""
    rng = random.Random(seed)
    clauses: list[list[int]] = []
    for _ in range(m):
        vs = rng.sample(range(1, n + 1), 3)
        clauses.append([v if rng.random() < 0.5 else -v for v in vs])
    return clauses


def simplify(clauses: list[list[int]], lit: int) -> list[list[int]] | None:
    """Assign lit=True; return reduced clause list, or None on conflict."""
    out: list[list[int]] = []
    for c in clauses:
        if lit in c:
            continue
        if -lit in c:
            rest = [x for x in c if x != -lit]
            if not rest:
                return None
            out.append(rest)
        else:
            out.append(c)
    return out


def choose_literal(clauses: list[list[int]]) -> int:
    counts: dict[int, int] = {}
    for c in clauses:
        for lit in c:
            counts[lit] = counts.get(lit, 0) + 1
    return max(counts, key=counts.get)  # type: ignore[arg-type]


def dpll(clauses: list[list[int]], counter: NodeCounter) -> bool:
    counter.tick()
    while True:
        unit = next((c[0] for c in clauses if len(c) == 1), None)
        if unit is None:
            break
        clauses = simplify(clauses, unit)
        if clauses is None:
            return False
    lits = {lit for c in clauses for lit in c}
    for lit in [x for x in lits if -x not in lits]:
        clauses = simplify(clauses, lit)
        assert clauses is not None
    if not clauses:
        return True
    lit = choose_literal(clauses)
    for branch in (lit, -lit):
        reduced = simplify(clauses, branch)
        if reduced is None:
            continue
        if dpll(reduced, counter):
            return True
    return False


def tseitin_xor_gate(x: int, y: int, z: int) -> list[list[int]]:
    """Clauses enforcing z = x XOR y."""
    return [
        [x, y, -z],
        [x, -y, z],
        [-x, y, z],
        [-x, -y, -z],
    ]


def random_xor_formula(n: int, seed: int, unsat: bool = True) -> list[list[int]]:
    """Random 3-XOR system on n variables, Tseitin-encoded as CNF.

    Plants a random assignment and picks n+1 random triples: n equations constrain each
    triple's parity to the planted value; the last equation's parity is flipped, making the
    system unsatisfiable w.h.p. over an expanding core. Expanding XOR systems are the
    canonical hard case for resolution and hence for DPLL search (Ben-Sasson-Wigderson).
    """
    rng = random.Random(seed)
    planted = [rng.random() < 0.5 for _ in range(n + 1)]
    clauses: list[list[int]] = []
    next_aux = n + 1
    for i in range(n + 1):
        vs = rng.sample(range(1, n + 1), 3)
        parity = planted[vs[0]] ^ planted[vs[1]] ^ planted[vs[2]]
        if i == n and unsat:
            parity ^= 1
        d = next_aux
        r = next_aux + 1
        next_aux += 2
        clauses.extend(tseitin_xor_gate(vs[0], vs[1], d))
        clauses.extend(tseitin_xor_gate(d, vs[2], r))
        clauses.append([r] if parity else [-r])
    return clauses


def run_experiment(label: str, generator, sizes: list[int] = SIZES,
                   instances: int = INSTANCES_PER_N, cap: int = NODE_CAP) -> None:
    global NODE_CAP
    NODE_CAP = cap
    print(f"\n=== {label} ===")
    print(f"{'n':>4} {'med nodes':>10} {'mean':>10} {'max':>10} {'capped':>8}")
    medians: list[float] = []
    maxima: list[float] = []
    for n in sizes:
        nodes: list[float] = []
        capped = 0
        for k in range(instances):
            formula = generator(n, 1000 * n + k)
            counter = NodeCounter(NODE_CAP)
            try:
                dpll(formula, counter)
            except NodeBudgetExceeded:
                capped += 1
            nodes.append(float(counter.value))
        med_nodes = statistics.median(nodes)
        medians.append(med_nodes)
        maxima.append(max(nodes))
        print(
            f"{n:>4} {med_nodes:>10.0f} {statistics.mean(nodes):>10.0f} "
            f"{max(nodes):>10.0f} {capped:>4}/{instances}"
        )
    print("growth factor per +2 variables:")
    for series_label, series in (("median", medians), ("max", maxima)):
        factors = [series[i] / series[i - 1] for i in range(1, len(sizes)) if series[i - 1] > 0]
        geo = statistics.geometric_mean(factors) if factors else float("nan")
        print(f"  {series_label:>6}: geometric-mean x{geo:.2f} per +2 variables")


if __name__ == "__main__":
    run_experiment(
        f"experiment 1: random 3-SAT, ratio {RATIO}",
        lambda n, seed: random_formula(n, int(round(RATIO * n)), seed),
    )
    run_experiment(
        "experiment 2: Tseitin 3-XOR (planted, over-determined, UNSAT), larger n",
        random_xor_formula,
        sizes=[30, 40, 50],
        instances=5,
        cap=20_000,
    )
