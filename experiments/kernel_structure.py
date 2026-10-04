"""Kernel-level fidelity check of the p=2 answer channel (Krajicek Omega(n,d) pipeline),
under the PRINTED OUTER reading of Definition 4.3 of arXiv:2609.35927.

Task (re-dispatch brief, 2026-10-03): at outer (n,d) in {(7,1),(15,2),(31,3)}, reconstruct
the solution space of the outer-reading design constraints, classify the degree-1 columns,
test the channel-law clauses on >=10^5 uniform design samples, and adjudicate whether the
corpus's coin-channel simulators sample a strict superset of the legal outer-reading
designs (and at what cost to the distributions the corpus's theorems use).

WHAT IS RECONSTRUCTED, AND WHY (constraint set imposed, with corpus citations)
-----------------------------------------------------------------------------
The pipeline (proof_complexity.md, quoting Def 4.3 of arXiv:2609.35927): rho is a partial
injection leaving exactly n_rho = 2d free holes (hence 2d+1 free pigeons D and 2d free
holes R); L is a degree-d design, linear, L(1)=1, "vanishing on V(n,d)^rho", of the
restricted system; the answer to a query g is omega(g) = L(g^rho). The corpus's paper
(paper/p2_results.tex, Definition def:pipeline items 2-3, the adopted OUTER reading) makes
this precise:
  - g^rho substitutes x_ij -> 1 if rho(i)=j, -> 0 if i is assigned and j != rho(i), and
    leaves x_ij alone on D x R. The printed clause does not cover (free pigeon, matched
    hole); the corpus's own channel law (killed-unmatched answers are the DETERMINED 0:
    cert_floor.md Lemma 3 proof; chi_p2_adaptive.py header; chi_two_phase.py) forces the
    zeroing completion x_ij^rho = 0 there. Any completion leaving those variables symbolic
    would make killed-unmatched answers undetermined design values, contradicting the
    corpus's law. We impose the zeroing completion.
  - V(n,d)^rho = "span of the restrictions of the outer degree-<=d consequences".
So the imposed constraint set is exactly:
  (i)  L kills every restriction (g.h)^rho, h in -PHP_n (razborov_check.py's
       system_polys), g an outer monomial, deg(g.h) <= d;
  (ii) L(e_0) = 1 for designs; kernel vectors are the homogeneous variant L(e_0) = 0.
Restricted polynomials live on the D x R monomial space (degree-<=d multiset monomials
over the (2d+1)*2d free-pair variables plus the constant), the space razborov_check.py
tabulates at N = 2d. Generator rows are built THROUGH THE OUTER ROUTE only (outer polys,
outer shifts, then restriction), never by copying the canonical list; the canonical list
(razborov_check-style at (2d,d)) is built independently and the two spans are compared.
rho is fixed to the corpus's canonical restriction (cert_floor.md "canonical Z": pigeon i
-> hole i for i < n-2d, 0-based); all rho with the same free sizes give isomorphic systems.

HEADLINE FINDINGS (all exact unless quoted as measured; reproduced by this script)
---------------------------------------------------------------------------------
F1. V(n,d)^rho = V(2d,d) EXACTLY at all three points (equal ranks, mutual containment):
    the printed outer reading and the canonical Des(2d,d) reading impose the SAME
    design space. Reason (verified term-by-term): every restricted outer generator is a
    canonical generator shift or 0 (an assigned pigeon's Q_i^rho = 0; killed Booleans,
    collisions, two-hole monomials restrict to 0), and deg(h^rho) = deg(h) whenever
    h^rho != 0, so the shift ranges coincide. The design-space debate
    (proof_complexity.md correction block, "Design-space readings") therefore dissolves
    at kernel level: no reading of "vanishing on V(n,d)^rho" can differ from canonical.
F2. Consequently each free row carries a FORCED parity: L kills Q_i^rho = 1 + sum_{j in
    R} x_ij, so the XOR of every free row's 2d design values is 1, and the row-sum answer
    is Q_i -> 0 DETERMINEDLY on every pigeon, free ones included: the parity-certificate
    basis of the two-phase tree (chi_two_phase.py: "free pigeon answers a fair row-coin")
    is refuted at kernel level. This confirms proof_complexity.md's ADDENDUM finding 3
    ("L(Q_i^rho) = 0 determinedly for ALL pigeons") as a theorem, not a measurement.
F3. Channel law, exact status: free-pair answers are marginally fair, and JOINTLY i.i.d.
    fair on any query set missing at least one cell of each free row (the completion
    structure; p2_results.tex Lemma lem:completion, Corollary cor:coin); a fully queried
    free row is locked to parity 1 (only 2^(2d-1) of the 2^(2d) patterns occur).
    Matched -> 1, killed-unmatched -> 0, L(1) = 1, F_2-linearity: hold exactly.
F4. Disjoint-support lemma: TRUE at d = 1 (the (2,1) kernel basis has pairwise disjoint
    single-variable supports); FALSE at d >= 2 for the RREF basis (a row's free-single
    vectors share the row's parity pivot column), and impossible for EVERY basis: within
    one row, 2d-1 even-weight disjointly supported vectors need total weight >= 2(2d-1)
    > 2d. The i.i.d. conclusion is rescued not by disjointness but by completion (F3).
F5. KEY QUESTION (brief item 4): the coin-channel simulators (chi_two_phase.py,
    chi_two_phase_retry.py, chi_thmT_verify.py, cert_floor_check.py, chi_o1_scaling.py,
    chi_p2_multivar.py, chi_and_vs_single.py) sample i.i.d. fair row bits and DROP
    constraints. At degree 1 they drop exactly the 2d+1 free-row parity constraints:
    their samples are a STRICT SUPERSET of legal outer-reading designs (legal fraction
    2^{-(2d+1)}, measured). Effect on the distributions the corpus's theorems use:
      - single-variable answers: UNCHANGED (total variation exactly 0) marginally and on
        row-incomplete sets; changed (TV exactly 1/2) only on fully queried free rows,
        an event of probability <= (n+1) C(e,2d) / C(n,2d) (the paper's E_full bound,
        negligible at budget). Theorem B, Props A/C/D, the Bayes posteriors, and the
        completion lemma are kernel-faithful.
      - row-sum parities: CHANGED COMPLETELY (coin: fair coin on free pigeons; designs:
        determined 0 on every pigeon; TV = 1/2). The two-phase parity certificate is a
        coin-model-only object, as p2_results.tex Proposition prop:rigidity already
        states; here it is verified from the kernel.
      - degree 2 (the AND-query line, thm:and): the simulators' product semantics
        (answer = product of factor answers) violate three design identities:
        same-hole and same-pigeon products of free pairs answer DETERMINED 0 (collision
        / two-hole monomials lie in V) while the coin channel says 1 w.p. 1/4, and the
        Q-shift sum rule XOR_j L(x_rj x_cd) = L(x_cd) holds identically while the coin
        channel satisfies it only w.p. ~1/2 (its rows' XOR is a fair bit). The square
        law L(x^2) = L(x) is the one degree-2 identity the product semantics gets right
        (ans(x)^2 = ans(x)); diagonal products answer a fresh fair bit independent of
        the two single answers (P[coord = b1*b2] = 1/2, not 1). The AND-no-lift identity
        is a coin-model statement; its pipeline transfer is NOT covered by this check.
F6. Control: the only kernel whose single-variable answers realize the coin law VERBATIM
    (i.i.d. even on full rows, Q_i fair on free pigeons) is the outer-design kernel
    {L : L kills the UNRESTRICTED outer V(n,d), L(1) = 1} with omega(g) = L(g^rho) read
    in the outer space: there the row parities are absorbed by the never-queried
    killed-pair design values. But that kernel VIOLATES the printed vanishing condition
    (Q_i^rho in V(n,d)^rho forces L(Q_i^rho) = 0; measured: only ~1/2 of sampled outer
    designs kill it). So no design space satisfying the printed definition realizes the
    coin law: the coin channel is the design space's row-incomplete single-variable
    shadow (cor:coin's E_full qualification is the exact fidelity statement).
F7. Counting certificates (cert_floor.md Theorem F): under the design law a fully
    scanned free row has an ODD count of 1s: P(count = c) = C(2d,c)/2^{2d-1} on odd c,
    so count 1 occurs with probability 2d/2^{2d-1}, TWICE the coin model's 2d/2^{2d}.
    Killed rows still show exactly one 1. The counting mechanism survives; Theorem F's
    constant is a coin-model number.

Standalone; imports razborov_check.py (the corpus's gf2 machinery) only. ASCII output.
"""
from __future__ import annotations

import math
import random
import time
from itertools import combinations_with_replacement

from razborov_check import monomials, shift, system_polys, to_vec

RNG_SEED = 20261003
N_SAMPLES = 100_000                    # uniform design samples per law (brief: >= 1e5)
N_COIN = 100_000                       # coin-channel comparison samples
POINTS = ((7, 1), (15, 2), (31, 3))    # outer (n,d); restricted systems (2d,d)
CONTROL_POINTS = ((7, 1), (15, 2))     # F6 outer-design control
CORPUS_TABLE = {(4, 2): (165, 65), (6, 3): (12110, 2079)}   # proof_complexity.md


# ---------------------------------------------------------------------------
# small GF(2) toolkit (pivot = highest set bit; razborov_check conventions)
# ---------------------------------------------------------------------------

def echelon_hom(rows: list[int]) -> dict[int, int]:
    piv: dict[int, int] = {}
    for v in rows:
        while v:
            h = v.bit_length() - 1
            if h in piv:
                v ^= piv[h]
            else:
                piv[h] = v
                break
    return piv


def echelon_rhs(rows: list[tuple[int, int]]) -> dict[int, tuple[int, int]]:
    """Echelon of (vec, rhs) rows; raises if 0=1 becomes derivable (i.e. 1 in V)."""
    ech: dict[int, tuple[int, int]] = {}
    for m, r in rows:
        while m:
            h = m.bit_length() - 1
            if h in ech:
                pm, pr = ech[h]
                m ^= pm
                r ^= pr
            else:
                ech[h] = (m, r)
                break
        if m == 0 and r == 1:
            raise RuntimeError("inconsistent design system: 1 in V (no designs exist)")
    return ech


def reduce_mod(m: int, ech: dict[int, int]) -> int:
    # pivot COLUMNS descending (not bit_length: ties among same-length columns must
    # resolve by column, else a larger pivot's row can re-set a cleared lower bit)
    for h in sorted(ech, reverse=True):
        if (m >> h) & 1:
            m ^= ech[h]
    return m


def particular(ech: dict[int, tuple[int, int]]) -> int:
    """One solution x of x.m = rhs on every echelon row (x supported on pivots)."""
    x = 0
    for c in sorted(ech):
        m, r = ech[c]
        mask = m ^ (1 << c)
        if r ^ ((x & mask).bit_count() & 1):
            x |= 1 << c
    return x


def null_basis(ech: dict[int, tuple[int, int]], ncols: int) -> dict[int, int]:
    """One kernel vector per free column: {free_col: vec} (small points only)."""
    out: dict[int, int] = {}
    for fc in range(ncols):
        if fc in ech:
            continue
        y = 1 << fc
        for c in sorted(ech):
            m, _ = ech[c]
            mask = m ^ (1 << c)
            if (y & mask).bit_count() & 1:
                y ^= 1 << c
        out[fc] = y
    return out


def rowspace_intersection(ech: dict[int, tuple[int, int]], T: list[int]) -> list[int]:
    """W = rowspace(ech) and F_2^T, as basis vectors over T-position bits.

    A combination sum c_p E_p has support inside T iff c_p = 0 at every pivot p not in T
    (leading-bit argument: the highest such pivot's bit survives) and the remaining
    T-pivot combination is zero off T. The c-vectors are therefore the kernel of the
    off-T-masked T-pivot rows, tracked through a small echelon.
    """
    tpos = {c: k for k, c in enumerate(T)}
    tmask = 0
    for c in T:
        tmask |= 1 << c
    ech2: dict[int, tuple[int, int]] = {}
    ker: list[int] = []
    for c in sorted(ech):
        if c not in tpos:
            continue
        m, _ = ech[c]
        v = m & ~tmask
        cv = 1 << tpos[c]
        inserted = False
        while v:
            h = v.bit_length() - 1
            if h in ech2:
                vm, vc = ech2[h]
                v ^= vm
                cv ^= vc
            else:
                ech2[h] = (v, cv)
                inserted = True
                break
        if not inserted:
            ker.append(cv)
    basis = []
    for cv in ker:
        w = 0
        while cv:
            lsb = cv & -cv
            k = lsb.bit_length() - 1
            cv ^= lsb
            wb = ech[T[k]][0] & tmask
            while wb:                       # T-column bits -> T-position bits
                lsb = wb & -wb
                wb ^= lsb
                w |= 1 << tpos[lsb.bit_length() - 1]
        basis.append(w)
    # the cv -> w map can collapse independent kernel combinations onto dependent
    # T-restrictions; filter to an independent basis
    return list(echelon_hom(basis).values())


def orthocomplement(basisW: list[int], tdim: int) -> list[int]:
    """Basis of {y in F_2^tdim : y.w = 0 for all w in basisW}."""
    piv: dict[int, int] = {}
    for w in basisW:
        while w:
            h = w.bit_length() - 1
            if h in piv:
                w ^= piv[h]
            else:
                piv[h] = w
                break
    out = []
    for f in range(tdim):
        if f in piv:
            continue
        y = 1 << f
        for c in sorted(piv):
            mask = piv[c] ^ (1 << c)
            if (y & mask).bit_count() & 1:
                y ^= 1 << c
        out.append(y)
    return out


def project(x: int, T: list[int]) -> int:
    y = 0
    for k, c in enumerate(T):
        if (x >> c) & 1:
            y |= 1 << k
    return y


def span_equal(a: list[int], b: list[int]) -> bool:
    ea, eb = echelon_hom(list(a)), echelon_hom(list(b))
    if len(ea) != len(eb):
        return False
    return all(reduce_mod(v, ea) == 0 for v in eb.values())


def sample_coset(basis: list[int], shift: int, rng: random.Random) -> int:
    """Uniform element of shift + span(basis)."""
    y = shift
    for v in basis:
        if rng.getrandbits(1):
            y ^= v
    return y


# ---------------------------------------------------------------------------
# statistics helpers
# ---------------------------------------------------------------------------

def chi2_z(counts: list[int], n_tot: int) -> float:
    """Standardized chi-square (stat - dof)/sqrt(2 dof); |z| <~ 4 at 99.99%."""
    k = len(counts)
    if k < 2 or n_tot == 0:
        return 0.0
    exp = n_tot / k
    stat = sum((o - exp) ** 2 for o in counts) / exp
    dof = k - 1
    return (stat - dof) / math.sqrt(2.0 * dof)


def pair_z(tab: list[list[int]]) -> float:
    """Standardized 2x2 independence chi-square."""
    rs = [tab[0][0] + tab[0][1], tab[1][0] + tab[1][1]]
    cs = [tab[0][0] + tab[1][0], tab[0][1] + tab[1][1]]
    tot = rs[0] + rs[1]
    if min(rs) == 0 or min(cs) == 0:
        return 0.0
    stat = 0.0
    for r in range(2):
        for c in range(2):
            e = rs[r] * cs[c] / tot
            stat += (tab[r][c] - e) ** 2 / e
    return (stat - 1.0) / math.sqrt(2.0)


# ---------------------------------------------------------------------------
# restriction machinery (canonical rho: pigeon i -> hole i for i < n-2d, 0-based)
# ---------------------------------------------------------------------------

class Restriction:
    def __init__(self, n: int, d: int):
        self.n = n
        self.d = d
        self.nfr = 2 * d
        self.nasg = n - 2 * d

    def ridx(self, i: int, j: int) -> int:
        """0-based outer pair (pigeon i, hole j) -> restricted VARIABLE index."""
        return (i - self.nasg) * self.nfr + (j - self.nasg)

    def cidx(self, i: int, j: int) -> int:
        """Same pair -> restricted monomial COLUMN index (constant occupies column 0)."""
        return self.ridx(i, j) + 1

    def mono(self, t: tuple[int, ...]):
        """Outer monomial (0-based var indices) -> restricted monomial tuple | 1 | 0."""
        out = []
        for a in t:
            i, j = divmod(a, self.n)
            if i < self.nasg:
                if j == i:
                    continue                # matched: folds into the constant
                return 0                    # killed-unmatched
            if j < self.nasg:
                return 0                    # free pigeon, matched hole: killed-unmatched
            out.append(self.ridx(i, j))
        return tuple(sorted(out))

    def poly(self, f: dict[tuple[int, ...], int]) -> dict[tuple[int, ...], int]:
        out: dict[tuple[int, ...], int] = {}
        for t, c in f.items():
            r = self.mono(t)
            if r != 0:
                out[r] = out.get(r, 0) ^ c
        return {t: c for t, c in out.items() if c}


def restricted_outer_rows(n: int, d: int) -> list[int]:
    """Generator rows of V(n,d)^rho, built THROUGH THE OUTER ROUTE only.

    Rows are (h^rho).(g^rho) over outer system polys h and outer monomials g with
    deg(g) <= d - deg(h). Since (h.g)^rho = h^rho.g^rho, the row depends only on
    (h^rho, g^rho), so we iterate over distinct restricted polys and distinct images.
    images(k) = {g^rho : deg(g) <= k} = every D x R monomial of degree <= k (realized
    by g = the monomial itself) plus the constant 1 (realized by any all-matched
    monomial; n - 2d >= 1 at every point); zeros contribute nothing.
    """
    R = Restriction(n, d)
    rmonos = monomials(R.nfr, d)
    rindex = {t: i for i, t in enumerate(rmonos)}
    mvars = n * (n + 1)
    images = {0: [()]}
    for s in range(1, d + 1):              # images of exact-degree-s outer monomials
        imgs = set()
        for t in combinations_with_replacement(range(mvars), s):
            r = R.mono(t)
            if r != 0:
                imgs.add(r)
        images[s] = sorted(imgs)
    for s in range(1, d + 1):              # cumulative: shifts of degree <= s
        images[s] = sorted(set(images[s]) | set(images[s - 1]))
    seen = set()
    rpolys = []
    for f in system_polys(n):              # corpus insertion order preserved
        rf = R.poly(f)
        if not rf:
            continue
        key = tuple(sorted(rf.items()))
        if key not in seen:
            seen.add(key)
            rpolys.append(rf)
    rows = []
    for rf in rpolys:
        dh = max(len(t) for t in rf)
        if dh > d:
            continue                     # poly cannot appear in degree-<=d consequences
        for g in images[d - dh]:
            rows.append(to_vec(shift(rf, g), rindex))
    return rows


def canonical_rows(nr: int, d: int) -> list[int]:
    """Generator rows of V(2d,d), built exactly like razborov_check.analyze."""
    monos = monomials(nr, d)
    mono_index = {t: i for i, t in enumerate(monos)}
    rows = []
    for f in system_polys(nr):
        df = max(len(t) for t in f)
        for mono in monos:
            if len(mono) + df <= d:
                rows.append(to_vec(shift(f, mono), mono_index))
    return rows


def outer_rows(n: int, d: int) -> list[int]:
    """Generator rows of the UNRESTRICTED outer V(n,d) (F6 control)."""
    monos = monomials(n, d)
    mono_index = {t: i for i, t in enumerate(monos)}
    rows = []
    for f in system_polys(n):
        df = max(len(t) for t in f)
        for mono in monos:
            if len(mono) + df <= d:
                rows.append(to_vec(shift(f, mono), mono_index))
    return rows


# ---------------------------------------------------------------------------
# per-point analysis under the printed outer reading
# ---------------------------------------------------------------------------

def analyze_restricted(n: int, d: int) -> dict:
    t0 = time.perf_counter()
    R = Restriction(n, d)
    nfr, nasg = R.nfr, R.nasg
    nr = nfr + 1                  # restricted rows: 2d+1 free pigeons (razborov_check
    n_singles = nr * nfr          # uses n = holes; the system has n+1 pigeons)
    rmonos = monomials(nfr, d)
    rindex = {t: i for i, t in enumerate(rmonos)}
    ncols = len(rmonos)
    free_pigeons = list(range(nasg, n + 1))
    killed_pigeons = list(range(nasg))

    print("=" * 79)
    print(f"OUTER (n={n}, d={d}) | canonical rho: 0-based pigeons {nasg}..{n} and holes "
          f"{nasg}..{n-1} free | restricted system ({nfr},{d})")
    print("=" * 79)

    # -- A. construction; outer = canonical identification -----------------------
    r_rows = restricted_outer_rows(n, d)
    c_rows = canonical_rows(nfr, d)
    ech_r, ech_c = echelon_hom(r_rows), echelon_hom(c_rows)
    rank_r, rank_c = len(ech_r), len(ech_c)
    fwd = all(reduce_mod(v, ech_r) == 0 for v in c_rows)
    rev = all(reduce_mod(v, ech_c) == 0 for v in r_rows)
    tag = ""
    if (nr, d) in CORPUS_TABLE:
        cr, _ = CORPUS_TABLE[(nr, d)]
        tag = f"  [corpus table rank V = {cr}: {'MATCH' if cr == rank_r else 'MISMATCH'}]"
    print(f"A1. V(n,d)^rho generator rows (outer route): {len(r_rows)}, rank = {rank_r}{tag}")
    print(f"A2. canonical V(2d,d) = V({nfr},{d}) generator rows: {len(c_rows)}, "
          f"rank = {rank_c}")
    ok = fwd and rev and rank_r == rank_c
    print(f"A3. V(n,d)^rho = V(2d,d): {'VERIFIED (containment both ways)' if ok else 'FAILED'}")
    assert ok

    ech_a = echelon_rhs([(g, 0) for g in r_rows] + [(1, 1)])
    rank_A = len(ech_a)
    dim_des = ncols - rank_A
    Lstar = particular(ech_a)
    assert Lstar & 1 == 1
    assert all((Lstar & g).bit_count() % 2 == 0 for g in r_rows)
    tag = ""
    if (nr, d) in CORPUS_TABLE:
        _, cd = CORPUS_TABLE[(nr, d)]
        tag = f"  [corpus table dim Des = {cd}: {'MATCH' if cd == dim_des else 'MISMATCH'}]"
    print(f"A4. design space: dim S = {ncols}, rank(A) = {rank_A}, dim Des = {dim_des} "
          f"(|Des| = 2^{dim_des}){tag}")

    # -- B. degree-1 classification and the disjoint-support lemma ----------------
    piv_single = sorted(c for c in ech_a if 1 <= c <= n_singles)
    assert len(piv_single) == nr
    row_pivot = {}
    for c in piv_single:
        rr, jr = divmod(c - 1, nfr)
        assert jr == nfr - 1, "parity pivot expected at each row's last hole"
        row_pivot[rr] = c
    free_single = [c for c in range(1, n_singles + 1) if c not in ech_a]
    print(f"B1. degree-1 columns: {n_singles} | pivot: {len(piv_single)} "
          f"(= e_0's row + one parity pivot per free row, each at its last hole) "
          f"| free: {len(free_single)} = ({nr})({nfr-1})")
    print(f"B2. each pivot single is parity-determined: L(x_rowpivot) = 1 + XOR(the other "
          f"{nfr-1} design values of its row); kernel rows have EVEN row parities")

    full_nb = null_basis(ech_a, ncols) if ncols <= 500 else None
    if full_nb is not None:
        for y in full_nb.values():
            assert all((y & g).bit_count() % 2 == 0 for g in r_rows)
        sup = {fc: [c for c in range(1, n_singles + 1) if (full_nb[fc] >> c) & 1]
               for fc in free_single}
        fcs = sorted(sup)
        nov = sum(1 for i in range(len(fcs)) for j in range(i + 1, len(fcs))
                  if set(sup[fcs[i]]) & set(sup[fcs[j]]))
        print(f"B3. RREF kernel basis, single-variable supports: each free single "
              f"carries {{itself, its row's parity pivot}}; pairwise-disjoint: "
              f"{'YES' if nov == 0 else f'NO ({nov} overlapping pairs)'}")
        if d == 1:
            print("    d=1: one free single per row -> the corpus's disjoint-support "
                  "lemma HOLDS at (2,1)")
        else:
            print(f"    d>=2: no basis at all can have disjoint single-variable supports "
                  f"({nfr-1} even-weight disjoint vectors in {nfr} coordinates need "
                  f"weight >= {2*(nfr-1)} > {nfr}); the i.i.d. law rests on completion, "
                  f"not disjointness")
    else:
        print("B3. full kernel basis skipped at this size (projected machinery below)")

    # -- coordinate sets (all COLUMN indices: variable v sits in column v+1) ------
    per_row = min(2, nfr - 1)
    win = sorted(R.cidx(i, nasg + t) for i in free_pigeons[:3] for t in range(per_row))
    win_T = [0] + win
    fr_row = sorted(R.cidx(free_pigeons[0], j) for j in range(nasg, n))
    fr_T = [0] + fr_row
    q_T = [0] + sorted(R.cidx(i, j) for i in free_pigeons for j in range(nasg, n))
    a = R.cidx(free_pigeons[0], nasg)
    b = R.cidx(free_pigeons[1], nasg)
    has_d2 = d >= 2
    if has_d2:
        c2 = R.cidx(free_pigeons[0], nasg + 1)
        d2v = R.cidx(free_pigeons[1], nasg + 1)
        e = R.cidx(free_pigeons[2], nasg)
        sh_col = rindex[tuple(sorted((a - 1, e - 1)))]      # same hole, pigeons 0,2
        sp_col = rindex[tuple(sorted((a - 1, c2 - 1)))]     # same pigeon (0)
        sq_col = rindex[(a - 1, a - 1)]
        dg_col = rindex[tuple(sorted((a - 1, d2v - 1)))]
        sum_cols = [rindex[tuple(sorted((R.ridx(free_pigeons[0], j), b - 1)))]
                    for j in range(nasg, n)]
        d2_T = sorted({0, a, b, c2, d2v, e, sh_col, sp_col, sq_col, dg_col}
                      | set(sum_cols))

    def proj_machinery(T: list[int]):
        Wb = rowspace_intersection(ech_a, T)
        pi = orthocomplement(Wb, len(T))
        assert len(Wb) + len(pi) == len(T)
        assert all(((w & y).bit_count() & 1) == 0 for w in Wb for y in pi)
        return Wb, pi, project(Lstar, T)

    Wb_win, pi_win, Ls_win = proj_machinery(win_T)
    Wb_fr, pi_fr, Ls_fr = proj_machinery(fr_T)
    Wb_q, pi_q, Ls_q = proj_machinery(q_T)
    if has_d2:
        Wb_d2, pi_d2, Ls_d2 = proj_machinery(d2_T)
        pos = {c: k for k, c in enumerate(d2_T)}
    print(f"B4. projected kernel structure (exact): window {len(win)} cells: "
          f"dim(rowspace|_T) = {len(Wb_win)}, dim(pi_T K) = {len(pi_win)}; full free "
          f"row: dim(rowspace|_T) = {len(Wb_fr)} (e_0 + its row sum), dim(pi_T K) = "
          f"{len(pi_fr)} (the parity subspace)"
          + (f"; degree-2 spot set: {len(d2_T)} coords, dim(rowspace|_T) = {len(Wb_d2)}"
             if has_d2 else "; no degree-2 columns at d = 1"))

    # -- B5. degree-2 column classification: which product answers are determined -
    if has_d2:
        def is_pivot(col: int) -> bool:
            return col in ech_a
        cls = {"same-hole": [0, 0], "same-pigeon": [0, 0],
               "diagonal": [0, 0], "square": [0, 0]}
        for i1 in range(nr):
            for i2 in range(i1 + 1, nr):
                for j in range(nfr):                      # same hole, two pigeons
                    col = rindex[(i1 * nfr + j, i2 * nfr + j)]
                    cls["same-hole"][0] += 1
                    cls["same-hole"][1] += is_pivot(col)
        for i in range(nr):
            for j1 in range(nfr):
                for j2 in range(j1 + 1, nfr):             # same pigeon, two holes
                    col = rindex[(i * nfr + j1, i * nfr + j2)]
                    cls["same-pigeon"][0] += 1
                    cls["same-pigeon"][1] += is_pivot(col)
        for i1 in range(nr):
            for i2 in range(i1 + 1, nr):
                for j1 in range(nfr):
                    for j2 in range(nfr):
                        if j1 != j2:                      # diagonal (both differ)
                            col = rindex[tuple(sorted((i1 * nfr + j1,
                                                       i2 * nfr + j2)))]
                            cls["diagonal"][0] += 1
                            cls["diagonal"][1] += is_pivot(col)
        for i in range(nr):
            for j in range(nfr):
                col = rindex[(i * nfr + j, i * nfr + j)]
                cls["square"][0] += 1
                cls["square"][1] += is_pivot(col)
        assert cls["same-hole"][1] == cls["same-hole"][0]
        assert cls["same-pigeon"][1] == cls["same-pigeon"][0]
        print(f"B5. degree-2 column classification (pivot = answer design-determined):")
        for k in ("same-hole", "same-pigeon", "square", "diagonal"):
            tot, pv = cls[k]
            print(f"      {k:<11}: {tot:3d} columns, {pv:3d} pivot "
                  f"({tot - pv:3d} free)")

    # -- C. sampling tests ---------------------------------------------------------
    rng = random.Random(RNG_SEED + 1000 * n + d)
    win_counts = [0] * (1 << len(win))
    cell_hits = {c: 0 for c in win}
    pair_tabs = {}
    fr_counts = [0] * (1 << len(fr_row))
    fr_xor1 = 0
    d2_stat = {"sh1": 0, "sp1": 0, "sqmis": 0, "sumviol": 0,
               "dg1": 0, "dgeq": 0}
    d2_joint = [0] * 8            # (dg, s_a, s_d)
    l1 = 0
    for _ in range(N_SAMPLES):
        LT = sample_coset(pi_win, Ls_win, rng)
        l1 += LT & 1
        wb = [(LT >> (1 + k)) & 1 for k in range(len(win))]
        idx = 0
        for k, v in enumerate(wb):
            idx |= v << k
            if v:
                cell_hits[win[k]] += 1
        win_counts[idx] += 1
        for i in range(len(win)):
            for j in range(i + 1, len(win)):
                tab = pair_tabs.setdefault((i, j), [[0, 0], [0, 0]])
                tab[wb[i]][wb[j]] += 1
        LF = sample_coset(pi_fr, Ls_fr, rng)
        fv = 0
        cnt = 0
        for k in range(len(fr_row)):
            v = (LF >> (1 + k)) & 1
            fv |= v << k
            cnt += v
        fr_counts[fv] += 1
        fr_xor1 += cnt & 1
        if has_d2:
            LD = sample_coset(pi_d2, Ls_d2, rng)
            s_a, s_b, s_d = ((LD >> pos[x]) & 1 for x in (a, b, d2v))
            sh = (LD >> pos[sh_col]) & 1
            sp = (LD >> pos[sp_col]) & 1
            sq = (LD >> pos[sq_col]) & 1
            sr = 0
            for cc in sum_cols:
                sr ^= (LD >> pos[cc]) & 1
            dg = (LD >> pos[dg_col]) & 1
            d2_stat["sh1"] += sh
            d2_stat["sp1"] += sp
            d2_stat["sqmis"] += sq ^ s_a
            d2_stat["sumviol"] += sr ^ s_b
            d2_stat["dg1"] += dg
            d2_stat["dgeq"] += 1 if dg == (s_a & s_d) else 0
            d2_joint[(dg << 2) | (s_a << 1) | s_d] += 1

    # full-kernel end-to-end validation at small points
    full_note = ""
    if full_nb is not None:
        rngF = random.Random(RNG_SEED + 555 * n + d)
        fcs = sorted(full_nb)
        bad = 0
        for _ in range(2000):
            L = sample_coset([full_nb[fc] for fc in fcs], Lstar, rngF)
            for rr in range(nr):
                x = 0
                for j in range(nfr):
                    x ^= (L >> (1 + rr * nfr + j)) & 1
                if x != 1:
                    bad += 1
        full_note = (f"; full-kernel 2000-sample check: row-parity violations = {bad}")
        # projected-vs-full: same span on every tested T
        tsets = [(win_T, pi_win), (fr_T, pi_fr), (q_T, pi_q)]
        if has_d2:
            tsets.append((d2_T, pi_d2))
        for T, pi in tsets:
            assert span_equal([project(full_nb[fc], T) for fc in full_nb], pi)

    # row-sum answers Q_i
    q_free_one = [0] * nr
    for _ in range(N_SAMPLES):
        LQ = sample_coset(pi_q, Ls_q, rng)
        for rr in range(nr):
            x = 0
            for k in range(nfr):
                x ^= (LQ >> (1 + rr * nfr + k)) & 1
            q_free_one[rr] += 1 ^ x        # Q_i = 1 + XOR(free-row answers)
    # killed pigeons: Q_i^rho is the zero polynomial (structural check)
    for i in killed_pigeons:
        Qi = {(): 1}
        for j in range(n):
            Qi[(i * n + j,)] = 1
        assert R.poly(Qi) == {}, "assigned pigeon's restricted row sum must vanish"

    # exact enumeration at the smallest point
    exact_note = ""
    if full_nb is not None and len(full_nb) <= 12:
        fcs = sorted(full_nb)
        good = 0
        for msk in range(1 << len(fcs)):
            L = Lstar
            for kk, fc in enumerate(fcs):
                if (msk >> kk) & 1:
                    L ^= full_nb[fc]
            okk = True
            for rr in range(nr):
                x = 0
                for j in range(nfr):
                    x ^= (L >> (1 + rr * nfr + j)) & 1
                if x != 1:
                    okk = False
                    break
            good += okk
        exact_note = (f"; exact enumeration: {good}/{1 << len(fcs)} designs have all "
                      f"free-row parities = 1")

    # -- reporting -----------------------------------------------------------------
    print(f"C1. [L(1)=1] L(e_0) = 1 in {l1}/{N_SAMPLES} samples: "
          f"{'PASS' if l1 == N_SAMPLES else 'FAIL'}{exact_note}")
    zc = {c: (cell_hits[c] / N_SAMPLES - 0.5) / math.sqrt(0.25 / N_SAMPLES)
          for c in win}
    zmax = max(abs(z) for z in zc.values())
    print(f"C2. [marginal fairness, {len(win)} free-pair window cells] max |z| = "
          f"{zmax:.2f}: {'PASS' if zmax < 4 else 'FAIL'}")
    zw = max(abs(pair_z(t)) for t in pair_tabs.values())
    print(f"C3. [pairwise independence, {len(pair_tabs)} window pairs] max |z| = "
          f"{zw:.2f}: {'PASS' if zw < 4 else 'FAIL'}")
    zj = chi2_z(win_counts, N_SAMPLES)
    print(f"C4. [joint i.i.d. on the row-incomplete {len(win)}-cell window] chi2 z = "
          f"{zj:+.2f} over {len(win_counts)} patterns: "
          f"{'PASS' if abs(zj) < 4 else 'FAIL'}")
    oddz = chi2_z([fr_counts[v] for v in range(len(fr_counts))
                   if v.bit_count() % 2 == 1], N_SAMPLES)
    print(f"C5. [FULL free row, {nfr} cells] P(row XOR = 1) = {fr_xor1}/{N_SAMPLES} = "
          f"{fr_xor1/N_SAMPLES:.4f} (coin channel predicts 0.5): "
          f"{'PASS: parity locked' if fr_xor1 == N_SAMPLES else 'FAIL'}; "
          f"patterns occurring: {sum(1 for c in fr_counts if c)} of {1 << nfr} "
          f"(= 2^{nfr-1}); uniform-on-parity-1 z = {oddz:+.2f}{full_note}")
    print(f"C6. [row-sum certificate Q_i = 1 + XOR(row answers)]")
    print(f"    free pigeons: P(Q_i = 1) = "
          f"[{', '.join(f'{q/N_SAMPLES:.4f}' for q in q_free_one)}] "
          f"(coin channel claims 1/2 each): "
          f"{'PASS -> determined 0: certificate DEAD' if sum(q_free_one) == 0 else 'FAIL'}")
    print(f"    killed pigeons: Q_i^rho = 0 identically (verified above): answer 0 "
          f"determinedly; agrees with the coin channel here")
    if has_d2:
        print(f"C7. [degree-2 laws vs the coin channel's product semantics]")
        print(f"    same-hole product of free pairs: P(=1) = "
              f"{d2_stat['sh1']}/{N_SAMPLES}  (design: 0; coin: 1/4)")
        print(f"    same-pigeon product:             P(=1) = "
              f"{d2_stat['sp1']}/{N_SAMPLES}  (design: 0; coin: 1/4)")
        print(f"    square = its single variable:    mismatches = "
              f"{d2_stat['sqmis']}/{N_SAMPLES}  (design: = L(x); coin: = L(x) as "
              f"well - product semantics square correctly: AGREE)")
        print(f"    Q-shift sum rule XOR_j L(x_0j x_b) = L(x_b): violations = "
              f"{d2_stat['sumviol']}/{N_SAMPLES}  (design: 0; coin: ~1/2)")
        print(f"    diagonal product: P(=1) = {d2_stat['dg1']/N_SAMPLES:.4f} (fresh fair "
              f"bit); P(= product of its two singles) = {d2_stat['dgeq']/N_SAMPLES:.4f} "
              f"(coin channel: exactly 1); joint (dg,s_a,s_d) z = "
              f"{chi2_z(d2_joint, N_SAMPLES):+.2f}")
    else:
        print("C7. [degree-2 laws] n/a at d = 1 (no degree-2 monomial columns)")

    # -- D. item 4: coin channel vs design space ------------------------------------
    crng = random.Random(RNG_SEED + 999 * n + d)
    legal = 0
    for _ in range(N_COIN):
        legal_row = True
        for _r in range(nr):
            if crng.getrandbits(nfr).bit_count() & 1 != 1:
                legal_row = False
        legal += legal_row
    exp_legal = N_COIN * 2.0 ** (-nr)
    zlegal = (legal - exp_legal) / math.sqrt(exp_legal * (1 - 2.0 ** (-nr)))
    print(f"D1. [strict superset] legal fraction of coin samples: {legal}/{N_COIN} = "
          f"{legal/N_COIN:.5f} vs 2^-({nr}) = {2.0**(-nr):.5f} (z = {zlegal:+.2f}): "
          f"the simulators' samples are a strict superset of legal designs")
    print(f"D2. [TV, exact] row-incomplete single-variable transcripts: TV(coin, design) "
          f"= 0 (completion structure; C4 confirms). Fully queried free row: TV = 1/2 "
          f"(parity-1 half-space vs uniform; C5). Free-pigeon row sums: TV = 1/2 "
          f"(determined 0 vs fair coin; C6).")
    print(f"D3. [E_full bound] P[some free row fully queried by e queries] <= "
          f"(n+1) C(e,2d) / C(n,2d):")
    k25 = int(round(n ** 0.25))
    for e, lab in ((2 * n + 1, "two-phase tree 2n+1"),
                   (n * (n + 1), "full scan n(n+1)"),
                   (max(2 * d, d * k25), f"budget d log2(k), k = 2^(n^0.25): e ~ {max(2*d, d*k25)}")):
        b = (n + 1) * math.comb(e, 2 * d) / math.comb(n, 2 * d)
        print(f"      e = {e:6d} ({lab}): <= {min(1.0, b):.2e}")
    print(f"    runtime {time.perf_counter()-t0:.1f}s")

    return {"n": n, "d": d, "rank": rank_r, "dim_des": dim_des,
            "legal_frac": legal / N_COIN}


# ---------------------------------------------------------------------------
# F6 control: the outer-design kernel (kills UNRESTRICTED outer V(n,d))
# ---------------------------------------------------------------------------

def analyze_outer(n: int, d: int) -> None:
    R = Restriction(n, d)
    ncols = len(monomials(n, d))
    n_singles = n * (n + 1)
    nasg = R.nasg
    free_pigeons = list(range(nasg, n + 1))
    print("-" * 79)
    print(f"F6 CONTROL at (n={n}, d={d}): outer-design kernel (L kills UNRESTRICTED "
          f"V(n,d); omega(g) = L(g^rho) read in the outer space)")
    print("-" * 79)
    rows = outer_rows(n, d)
    ech = echelon_rhs([(g, 0) for g in rows] + [(1, 1)])
    rank = len(ech)
    Lstar = particular(ech)
    T = list(range(n_singles + 1))
    Wb = rowspace_intersection(ech, T)
    pi = orthocomplement(Wb, len(T))
    LsT = project(Lstar, T)
    print(f"    dim S = {ncols}, rank = {rank}; rowspace|_singles dim = {len(Wb)} "
          f"(e_0 + the {n+1} outer row sums: {'MATCH' if len(Wb) == n + 2 else 'MISMATCH'}"
          f" with the outer degree-one span lemma); pi dim = {len(pi)}")
    rng = random.Random(RNG_SEED + 31 * n + d)
    cells = sorted(R.cidx(free_pigeons[0], j) for j in range(nasg, n))
    buckets = [0] * (1 << len(cells))
    qone = 0
    for _ in range(N_SAMPLES):
        LT = sample_coset(pi, LsT, rng)
        v = 0
        x = 0
        for k, c in enumerate(cells):
            bit = (LT >> (1 + k)) & 1
            v |= bit << k
            x ^= bit
        buckets[v] += 1
        qone += 1 ^ x
    z = chi2_z(buckets, N_SAMPLES)
    print(f"    FREE pigeon, entire row queried ({len(cells)} free cells): joint "
          f"uniformity z = {z:+.2f}: the coin law holds VERBATIM (no E_full event)")
    print(f"    P(Q_i = 1 | free) = {qone/N_SAMPLES:.4f} (coin law's 1/2; the "
          f"printed-reading kernel gives 0)")
    print(f"    printed vanishing check: L kills Q_i^rho in only {N_SAMPLES - qone}/"
          f"{N_SAMPLES} samples ~ 1/2 (the printed condition demands all, since "
          f"Q_i^rho in V(n,d)^rho): this reading EXCLUDES itself from Definition 4.3")
    i0 = 0
    Qi = {(): 1}
    for j in range(n):
        Qi[(i0 * n + j,)] = 1
    print(f"    killed pigeon: Q_i^rho = {R.poly(Qi) or '0'} -> answer 0 determinedly "
          f"(agrees with both the coin channel and the printed reading)")


# ---------------------------------------------------------------------------

def main() -> None:
    print("kernel_structure: kernel-level fidelity check of the Omega(n,d) answer")
    print("channel at p = 2 under the PRINTED OUTER reading (L vanishing on")
    print("V(n,d)^rho). Constraint set: L kills every restriction (g.h)^rho of the")
    print("outer degree-<=d consequences (razborov_check system polys + shifts;")
    print("restriction kills killed-unmatched pairs and folds matched pairs into the")
    print("constant), with L(1) = 1. See the module docstring for every citation.")
    print()
    results = {}
    for (n, d) in POINTS:
        results[(n, d)] = analyze_restricted(n, d)
        print()
    for (n, d) in CONTROL_POINTS:
        analyze_outer(n, d)
        print()

    print("=" * 79)
    print("VERDICT (brief item 4: does the coin channel DROP outer-reading constraints?)")
    print("=" * 79)
    print("1. V(n,d)^rho = V(2d,d) at all three points: the printed outer reading and")
    print("   the canonical Des(2d,d) reading are the SAME design space at kernel level.")
    print("2. YES: the coin-channel simulators drop constraints. At degree 1 they drop")
    print("   exactly the 2d+1 free-row parities (XOR of each free row's answers = 1);")
    print("   their samples are a strict superset of legal designs. Measured legal")
    print("   fraction vs 2^-(2d+1):")
    for r in results.values():
        print(f"     (n={r['n']}, d={r['d']}): {r['legal_frac']:.5f} vs "
              f"{2.0 ** (-(2 * r['d'] + 1)):.5f}")
    print("   At degree 2 the product semantics also violate the collision/two-hole")
    print("   determinations and the Q-shift sum rules (C7); the square law is the")
    print("   one degree-2 identity the product semantics gets right.")
    print("3. Effect on the distributions the corpus's theorems use:")
    print("   - single-variable answers: UNCHANGED (TV = 0) on row-incomplete sets and")
    print("     marginally fair always; changed (TV = 1/2) only on fully queried free")
    print("     rows (E_full, negligible at budget). Theorem B, Props A/C/D, the Bayes")
    print("     posteriors, and completion are kernel-faithful.")
    print("   - row-sum parities: CHANGED COMPLETELY (designs: Q_i = 0 on EVERY pigeon;")
    print("     coin: fair on free pigeons). The two-phase parity certificate is a")
    print("     coin-model-only object: confirms prop:rigidity and ADDENDUM finding 3.")
    print("   - degree-2 AND-query laws: NOT faithful (C7): the no-lift identity is a")
    print("     coin-model statement; the pipeline's AND channel differs.")
    print("4. The only kernel realizing the coin law verbatim (F6 control) violates the")
    print("   printed vanishing condition. Under Definition 4.3 as printed, the coin")
    print("   channel is NOT the design space: it is exactly the design space's")
    print("   row-incomplete single-variable answer law (cor:coin's E_full clause).")
    print("5. Disjoint-support lemma: holds at (2,1); impossible for every basis at")
    print("   d >= 2; the correct replacement is the completion structure (C4/C5).")
    print("6. Counting certificates survive the design law but with the odd-count")
    print("   distribution C(2d,c)/2^(2d-1) on odd c (Theorem F's constant is a")
    print("   coin-model number; killed rows still show exactly one 1).")


if __name__ == "__main__":
    main()
