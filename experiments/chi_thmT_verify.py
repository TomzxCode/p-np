"""Independent replication of Theorem T and both per-hit posterior caps at p = 2.

Verification-agent script (2026-10-03): replication at NEW (n, d) points not used by
any prior corpus run: (16,1), (24,3), (48,4), (96,6), (128,8). The exact p = 2 answer
channel law (proved in the corpus: disjoint-support property of the design kernel) is
sampled exactly as in chi_two_phase.py / chi_and_posterior.py / chi_posterior_test.py:
  free pair -> i.i.d. fair design bit; killed-matched -> 1; killed-unmatched -> 0.

Experiments per point:
1. Theorem T (two_phase_tree.md), the non-retry two-phase tree of chi_two_phase.py:
   success = 1 - 2^-(2d+1) exactly (phase 2 never fails given certification); the
   all-miss fallback adds f * 2^-(2d+1) with f = (2d+1)*2d / ((n+1)*n).
2. Single-variable per-hit freeness posterior: q = (2d+1)d / ((2d+1)d + (n-2d))
   (= (f1/2)/(f1/2 + m) with f1 = P(random outer pair free), m = P(killed-matched)).
3. Degree-2 AND-query per-hit posterior (no-lift theorem): the same q exactly:
   (f1^2/4 + f1*m/2) / (f1/2 + m)^2 = (f1/2)/(f1/2 + m) = q.

Intervals: exact Clopper-Pearson two-sided binomial CIs at the 99% level (bisection
on the regularized incomplete beta function; self-tested at startup). Verdict rule:
PASS iff the prediction lies inside the measured 99% interval.

Run: python3 chi_thmT_verify.py [--smoke|--probe48]
  --smoke: tiny sims, correctness check only
  --probe48: FAIL-investigation probes for the (48,4) part-1 cell
"""
from __future__ import annotations

import math
import random
import sys

POINTS = ((16, 1), (24, 3), (48, 4), (96, 6), (128, 8))
ALPHA = 0.01  # two-sided 99% confidence

# Theorem-T runs are cheap at high d (no n^2 pair scans), so they get more
# simulations where the predicted error 2^-(2d+1) is tiny; all >= 2000.
SIMS_T = {(16, 1): 8000, (24, 3): 8000, (48, 4): 100000, (96, 6): 100000, (128, 8): 100000}
# Posterior scans share pipeline samples; sized to accumulate >= ~2000 hits each.
SIMS_P = {(16, 1): 8000, (24, 3): 6000, (48, 4): 4000, (96, 6): 3000, (128, 8): 2500}

SEED_T = 271828
SEED_P = 141421


# ---------- exact binomial confidence intervals (Clopper-Pearson) ----------

def _betacf(a: float, b: float, x: float) -> float:
    """Continued fraction for the regularized incomplete beta (modified Lentz)."""
    maxit, eps, fpmin = 300, 3e-14, 1e-300
    qab, qap, qam = a + b, a + 1.0, a - 1.0
    c = 1.0
    d = 1.0 - qab * x / qap
    if abs(d) < fpmin:
        d = fpmin
    d = 1.0 / d
    h = d
    for m in range(1, maxit + 1):
        m2 = 2 * m
        aa = m * (b - m) * x / ((qam + m2) * (a + m2))
        d = 1.0 + aa * d
        if abs(d) < fpmin:
            d = fpmin
        c = 1.0 + aa / c
        if abs(c) < fpmin:
            c = fpmin
        d = 1.0 / d
        h *= d * c
        aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2))
        d = 1.0 + aa * d
        if abs(d) < fpmin:
            d = fpmin
        c = 1.0 + aa / c
        if abs(c) < fpmin:
            c = fpmin
        d = 1.0 / d
        delta = d * c
        h *= delta
        if abs(delta - 1.0) < eps:
            break
    return h


def _betainc(a: float, b: float, x: float) -> float:
    """Regularized incomplete beta I_x(a, b)."""
    if x <= 0.0:
        return 0.0
    if x >= 1.0:
        return 1.0
    ln_bt = (math.lgamma(a + b) - math.lgamma(a) - math.lgamma(b)
             + a * math.log(x) + b * math.log1p(-x))
    bt = math.exp(ln_bt)
    if x < (a + 1.0) / (a + b + 2.0):
        return bt * _betacf(a, b, x) / a
    return 1.0 - bt * _betacf(b, a, 1.0 - x) / b


def binom_cdf(k: int, n: int, p: float) -> float:
    """P[X <= k] for X ~ Binomial(n, p), exact: I_{1-p}(n-k, k+1)."""
    if k < 0:
        return 0.0
    if k >= n:
        return 1.0
    return _betainc(n - k, k + 1, 1.0 - p)


def cp_ci(k: int, n: int, alpha: float = ALPHA) -> tuple[float, float]:
    """Clopper-Pearson two-sided [lo, hi] for a binomial proportion, coverage 1-alpha."""
    if k <= 0:
        lo = 0.0
    else:
        glo, ghi = 0.0, 1.0
        for _ in range(80):
            mid = 0.5 * (glo + ghi)
            # P[X >= k | mid] = 1 - CDF(k-1, mid) = alpha/2; the tail mass is
            # increasing in p, so excess mass means the root lies below mid
            if 1.0 - binom_cdf(k - 1, n, mid) > alpha / 2:
                ghi = mid
            else:
                glo = mid
        lo = 0.5 * (glo + ghi)
    if k >= n:
        hi = 1.0
    else:
        glo, ghi = 0.0, 1.0
        for _ in range(80):
            mid = 0.5 * (glo + ghi)
            if binom_cdf(k, n, mid) > alpha / 2:
                glo = mid
            else:
                ghi = mid
        hi = 0.5 * (glo + ghi)
    return lo, hi


def self_test() -> None:
    """Check the CI machinery against known exact values before trusting it."""
    lo, hi = cp_ci(0, 10, 0.05)
    assert lo == 0.0 and abs(hi - 0.30850) < 5e-4, (lo, hi)
    lo, hi = cp_ci(10, 10, 0.05)
    assert hi == 1.0 and abs(lo - 0.69150) < 5e-4, (lo, hi)
    lo, hi = cp_ci(97, 100, 0.05)
    assert lo < 0.97 < hi, (lo, hi)
    lo, hi = cp_ci(100000, 100000, ALPHA)
    assert hi == 1.0 and abs(lo - math.exp(math.log(ALPHA / 2) / 100000)) < 1e-6, (lo, hi)
    lo, hi = cp_ci(0, 100000, ALPHA)
    assert lo == 0.0 and abs(hi - (1.0 - math.exp(math.log(ALPHA / 2) / 100000))) < 1e-6


# ---------- exact predictions ----------

def q_exact(n: int, d: int) -> float:
    """Single-variable (= AND, no-lift) per-hit freeness posterior."""
    return (2 * d + 1) * d / ((2 * d + 1) * d + (n - 2 * d))


def p1_exact(n: int, d: int) -> float:
    """Exact single-variable hit rate P(ans = 1)."""
    return ((2 * d + 1) * d + (n - 2 * d)) / ((n + 1) * n)


def p_and_exact(n: int, d: int) -> float:
    """Exact AND hit rate for two DISTINCT uniform pairs (hypergeometric-exact).

    Given a pipeline, the answer-1 set has size B + m with B ~ Bin(F, 1/2),
    F = (2d+1)*2d free pairs, m = n-2d matched pairs. One trial draws two distinct
    uniform pairs, so P(ans=1) = E[|S|(|S|-1)] / (M(M-1)), M = (n+1)*n, and
    E[|S|(|S|-1)] = F/4 + mu^2 - mu with mu = F/2 + m (= M * p1_exact).
    """
    nn = (n + 1) * n
    big_f = (2 * d + 1) * (2 * d)
    mu = (2 * d + 1) * d + (n - 2 * d)
    return (big_f / 4 + mu * mu - mu) / (nn * (nn - 1))


# ---------- experiment 1: Theorem T (non-retry two-phase tree) ----------

def run_theorem_t(n: int, d: int, n_sim: int, rng: random.Random) -> tuple[int, ...]:
    succ = miss1 = fail2 = fb = fb_succ = 0
    for _ in range(n_sim):
        # pipeline: rho leaves 2d+1 free pigeons (D) and 2d free holes (R)
        # (exact sampling pattern of chi_two_phase.py)
        assigned_p = rng.sample(range(n + 1), n - 2 * d)
        assigned_h = rng.sample(range(n), n - 2 * d)
        rho = dict(zip(assigned_p, assigned_h))
        D = sorted(set(range(n + 1)) - set(assigned_p))
        R = sorted(set(range(n)) - set(assigned_h))
        free_p = set(D)
        # per free pigeon: its 2d row design bits (i.i.d. fair, proved)
        row_bits = {i: [rng.randrange(2) for _ in R] for i in D}
        # phase 1: query Q_i = 1 + sum_j x_ij; first free pigeon answering 1 certifies
        certified = None
        for i in range(n + 1):
            if i in free_p and sum(row_bits[i]) % 2 == 1:
                certified = i
                break
        if certified is None:
            # all-miss fallback: label a uniform random pair (chi_two_phase.py)
            miss1 += 1
            fb += 1
            chosen = (rng.choice(range(n + 1)), rng.choice(range(n)))
            if chosen[0] in D and chosen[1] in R:
                fb_succ += 1
                succ += 1
            continue
        # phase 2: row-scan the certified pigeon; killed holes answer 0, free fair
        jstar = None
        row = row_bits[certified]
        for pos in range(len(R)):
            if row[pos] == 1:
                jstar = R[pos]
                break
        if jstar is None:
            fail2 += 1  # unreachable per Theorem T; tracked as a fidelity check
        else:
            succ += 1
    return succ, miss1, fail2, fb, fb_succ


# ---------- experiments 2 + 3: posterior scans on shared pipeline samples ----------

def run_posteriors(n: int, d: int, n_sim: int, rng: random.Random) -> tuple[int, ...]:
    nn = (n + 1) * n
    t2 = min(400, nn // 2)              # single-variable queries per sample
    t3 = min(5000, (nn - t2) // 2)      # AND queries per sample (2 distinct pairs each)
    h2 = k2 = 0  # single-variable: hits (ans=1), free hits
    h3 = k3 = 0  # AND: hits (ans=1), free labels
    for _ in range(n_sim):
        assigned_p = rng.sample(range(n + 1), n - 2 * d)
        assigned_h = rng.sample(range(n), n - 2 * d)
        rho = dict(zip(assigned_p, assigned_h))
        D = set(range(n + 1)) - set(assigned_p)
        R = set(range(n)) - set(assigned_h)
        idxs = rng.sample(range(nn), t2 + 2 * t3)  # all distinct within the sample
        # (a) single-variable queries (chi_posterior_test.py channel, distinct pairs)
        for idx in idxs[:t2]:
            i, j = divmod(idx, n)
            if i in D:
                if j in R and rng.randrange(2):  # free pair: fair design bit
                    h2 += 1
                    k2 += 1
            elif rho[i] == j:  # killed-matched: determined 1, never free
                h2 += 1
        # (b) degree-2 AND queries on consecutive distinct pairs
        #     (chi_and_vs_single.py pattern; uniform label among the two components)
        for t in range(t2, t2 + 2 * t3, 2):
            i, j = divmod(idxs[t], n)
            if i in D:
                if not (j in R and rng.randrange(2)):
                    continue  # component a answers 0
            elif rho[i] != j:
                continue  # component a killed-unmatched
            i2, j2 = divmod(idxs[t + 1], n)
            if i2 in D:
                if not (j2 in R and rng.randrange(2)):
                    continue  # component b answers 0
            elif rho[i2] != j2:
                continue
            h3 += 1  # ans = 1: both components answered 1
            if rng.randrange(2):  # uniform label choice between pa, pb
                i, j = i2, j2
            if i in D and j in R:
                k3 += 1
    return t2, t3, h2, k2, h3, k3


# ---------- FAIL investigation probe for the (48,4) part-1 cell ----------

def probe_48() -> None:
    """Investigation of the (48,4) FAIL in the registered run (seed 271828).

    Registered-run symptom: measured success ABOVE prediction (fewer phase-1
    misses than 2^-(2d+1) predicts: 163 observed vs 195.3 expected in 100000
    simulations, z = -2.31). Two pre-registered probes:
    (a) direct phase-1 miss probe: the implemented phase-1 event is exactly
        (1/2)^(2d+1) by construction (2d+1 independent free pigeons, each an XOR
        of 2d i.i.d. fair coins), so a huge-N probe must hit Bin(N, 1/512);
    (b) decisive fresh-seed rerun of the full two-phase tree, N = 500000.
    """
    n, d = 48, 4
    rows, cols = 2 * d + 1, 2 * d
    pred_miss = 2.0 ** (-(2 * d + 1))
    print(f"probe (48,{d}): investigating phase-1 miss shortfall in the registered run")
    # (a) phase-1 law only
    n_trials = 500000
    rng = random.Random(607261)
    misses = 0
    for _ in range(n_trials):
        miss = True
        for _ in range(rows):
            if sum(rng.randrange(2) for _ in range(cols)) % 2 == 1:
                miss = False
                break
        if miss:
            misses += 1
    lo, hi = cp_ci(misses, n_trials)
    exp_miss = n_trials * pred_miss
    z = (misses - exp_miss) / math.sqrt(n_trials * pred_miss * (1 - pred_miss))
    verdict = "PASS" if lo <= pred_miss <= hi else "FAIL"
    print(f"  (a) phase-1 miss law, {n_trials} trials (seed 607261): "
          f"misses {misses} (z = {z:+.2f} vs {exp_miss:.1f}), "
          f"rate {misses / n_trials:.6f}, pred {pred_miss:.6f}, "
          f"99% CI [{lo:.6f},{hi:.6f}] -> {verdict}")
    # (b) full tree, fresh seed, decisive size
    n_sim = 500000
    rng2 = random.Random(607261)
    succ, miss1, fail2, fb, fb_succ = run_theorem_t(n, d, n_sim, rng2)
    lo2, hi2 = cp_ci(succ, n_sim)
    pred = 1.0 - pred_miss
    f_fb = rows * cols / ((n + 1) * n)
    pred_fb = pred + f_fb * pred_miss
    verdict2 = "PASS" if lo2 <= pred <= hi2 else "FAIL"
    print(f"  (b) full two-phase tree, {n_sim} sims (seed 607261): "
          f"success {succ / n_sim:.6f} (pred {pred:.6f}, pred+fb {pred_fb:.6f}), "
          f"99% CI [{lo2:.6f},{hi2:.6f}], p1miss {miss1} (exp {n_sim * pred_miss:.1f}), "
          f"p2fail {fail2}, fb_succ {fb_succ} -> {verdict2}")


# ---------- driver ----------

def main() -> None:
    smoke = "--smoke" in sys.argv
    if "--probe48" in sys.argv:
        probe_48()
        return
    sims_t = {p: (min(500, v) if smoke else v) for p, v in SIMS_T.items()}
    sims_p = {p: (min(500, v) if smoke else v) for p, v in SIMS_P.items()}
    self_test()
    print("replication of Theorem T + single-var posterior cap + AND no-lift cap")
    print("points (new, none used by prior corpus runs):", 
          " ".join(f"({n},{d})" for n, d in POINTS))
    print("channel law (proved, reused exactly): free pair -> i.i.d. fair bit;")
    print("  killed-matched -> 1; killed-unmatched -> 0")
    print("intervals: exact Clopper-Pearson two-sided 99% binomial CIs")
    print("verdict: PASS iff the prediction lies inside the measured 99% CI")
    print()

    # ---- part 1: Theorem T ----
    print("[1] Theorem T, two-phase tree success (chi_two_phase.py tree, non-retry)")
    print("    pred = 1 - 2^-(2d+1); pred+fb adds f*2^-(2d+1), f = (2d+1)*2d/((n+1)*n)")
    print(f"{'n':>5} {'d':>3} {'sims':>7} {'fails':>6} {'meas':>9} "
          f"{'99% CI':>25} {'pred':>9} {'pred+fb':>9} {'p1miss':>7} {'p2fail':>7} {'verdict':>8}")
    rng_t = random.Random(SEED_T)
    tot_p2fail = 0
    t1_rows = []
    for (n, d) in POINTS:
        n_sim = sims_t[(n, d)]
        succ, miss1, fail2, fb, fb_succ = run_theorem_t(n, d, n_sim, rng_t)
        tot_p2fail += fail2
        lo, hi = cp_ci(succ, n_sim)
        pred = 1.0 - 2.0 ** (-(2 * d + 1))
        f_fb = (2 * d + 1) * (2 * d) / ((n + 1) * n)
        pred_fb = pred + f_fb * (2.0 ** (-(2 * d + 1)))
        verdict = "PASS" if lo <= pred <= hi else "FAIL"
        row = (n, d, n_sim, n_sim - succ, succ / n_sim, lo, hi, pred, pred_fb,
               miss1, fail2, verdict)
        t1_rows.append(row)
        print(f"{n:>5} {d:>3} {n_sim:>7} {n_sim - succ:>6} {succ / n_sim:>9.6f} "
              f"[{lo:>9.6f},{hi:>9.6f}] {pred:>9.6f} {pred_fb:>9.6f} "
              f"{miss1:>7} {fail2:>7} {verdict:>8}")
    print()

    # ---- parts 2 + 3: posterior scans ----
    print("[2] single-variable per-hit posterior, q = (2d+1)d / ((2d+1)d + (n-2d))")
    print(f"{'n':>5} {'d':>3} {'sims':>6} {'queries':>8} {'hits':>7} {'post':>9} "
          f"{'99% CI':>25} {'q':>9} {'hitrate':>8} {'hit_pred':>9} {'verdict':>8}")
    rng_p = random.Random(SEED_P)
    t3_data = []
    for (n, d) in POINTS:
        n_sim = sims_p[(n, d)]
        t2, t3, h2, k2, h3, k3 = run_posteriors(n, d, n_sim, rng_p)
        q = q_exact(n, d)
        lo2, hi2 = cp_ci(k2, h2)
        post2 = k2 / h2 if h2 else float("nan")
        v2 = "PASS" if lo2 <= q <= hi2 else "FAIL"
        print(f"{n:>5} {d:>3} {n_sim:>6} {n_sim * t2:>8} {h2:>7} {post2:>9.6f} "
              f"[{lo2:>9.6f},{hi2:>9.6f}] {q:>9.6f} {h2 / (n_sim * t2):>8.5f} "
              f"{p1_exact(n, d):>9.6f} {v2:>8}")
        t3_data.append((n, d, n_sim, t3, h3, k3, q))
    print()
    print("[3] degree-2 AND-query per-hit posterior (no-lift theorem: same q)")
    print(f"{'n':>5} {'d':>3} {'sims':>6} {'queries':>8} {'hits':>7} {'post':>9} "
          f"{'99% CI':>25} {'q':>9} {'hitrate':>9} {'hit_pred':>9} {'verdict':>8}")
    for (n, d, n_sim, t3, h3, k3, q) in t3_data:
        lo3, hi3 = cp_ci(k3, h3)
        post3 = k3 / h3 if h3 else float("nan")
        v3 = "PASS" if lo3 <= q <= hi3 else "FAIL"
        print(f"{n:>5} {d:>3} {n_sim:>6} {n_sim * t3:>8} {h3:>7} {post3:>9.6f} "
              f"[{lo3:>9.6f},{hi3:>9.6f}] {q:>9.6f} {h3 / (n_sim * t3):>9.3e} "
              f"{p_and_exact(n, d):>9.3e} {v3:>8}")
    print()

    print("fidelity checks:")
    print(f"  phase-2 fail branch (unreachable per Theorem T) fired {tot_p2fail} times")
    print("  hitrate columns: measured vs exact prediction (part 3 exact values are")
    print("  for distinct-pair sampling; the independent-status approx is (f1/2+m)^2)")
    print("  part 2 and part 3 share pipeline samples; query sets are disjoint")


if __name__ == "__main__":
    main()
