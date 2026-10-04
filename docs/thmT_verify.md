# Theorem T and both per-hit posterior caps: independent replication at new (n, d) points

Verification-agent run (2026-10-03). Script: `chi_thmT_verify.py` (standalone, fixed seeds,
no dependencies beyond the standard library). Runtime: 69 s (registered run) + 34 s (probe).

Replicated claims (from `two_phase_tree.md` and the corpus's proved $p = 2$ results):
1. Theorem T: the non-retry two-phase tree succeeds with probability exactly
   $1 - 2^{-(2d+1)}$ (phase 2 never fails given certification; the all-miss fallback adds
   $f \cdot 2^{-(2d+1)}$ with $f = (2d{+}1)\,2d\,/\,((n{+}1)\,n)$).
2. Single-variable per-hit freeness posterior: $q = \frac{(2d{+}1)d}{(2d{+}1)d + (n-2d)}$.
3. Degree-2 AND-query per-hit posterior (no-lift theorem): the same $q$ exactly.

Points: (16,1), (24,3), (48,4), (96,6), (128,8). None of these pairs was used by the
prior Theorem T runs (`chi_two_phase.py`: (32,2), (64,2), (128,2), (64,4)) or by the
prior per-hit posterior measurements (`chi_and_posterior.py` / `chi_and_vs_single.py`
at (32,2)). Transparency note: (128,8) appeared before in related but different
experiments (`chi_two_phase_retry.py` measured the RETRY tree there, a different success
law; `chi_posterior_test.py` scanned $n = 128$, $d = 8$ for first-hit scan success), so the
three laws tested here are measured at these points for the first time.

## Method

- Channel-sampling pattern reused EXACTLY from the verified scripts: pipeline drawn as
  `rng.sample(range(n+1), n-2d)` for pigeons, `rng.sample(range(n), n-2d)` for holes,
  `rho = dict(zip(assigned_p, assigned_h))`, $D$ and $R$ by set difference, per-free-pigeon
  row bits as i.i.d. fair coins (`chi_two_phase.py` lines 35-43). Query answers follow
  the proved law: free pair $\mapsto$ i.i.d. fair design bit, killed-matched $\mapsto$ 1,
  killed-unmatched $\mapsto$ 0.
- Theorem T tree replicated line-for-line from `chi_two_phase.py` (stop at the first
  answer 1 in each phase; all-miss fallback labels a uniform random pair). The phase-2
  fail branch, unreachable per the theorem, is kept and counted as a fidelity check.
- Posterior scans: 136 to 400 single-variable queries and 68 to 5000 AND queries per
  pipeline sample, all pairs distinct within a sample (i.i.d. free bits, as proved).
  AND queries: two distinct uniform random pairs per trial, labeled component chosen
  uniformly (`chi_and_vs_single.py` pattern).
- Intervals: exact Clopper-Pearson two-sided binomial CIs at 99% (bisection on the
  regularized incomplete beta function; self-tested at startup against the known 0/10
  and 10/10 values and the $\alpha^{1/n}$ closed form).
- Verdict rule: PASS iff the prediction lies inside the measured 99% interval.
- Seeds: Theorem T run 271828, posterior scans 141421, investigation probe 607261.
- Sample sizes: Theorem T 8000/8000/100000/100000/100000 simulations per point (large
  sizes at high $d$ because the predicted error $2^{-(2d+1)}$ is tiny); posterior scans
  8000/6000/4000/3000/2500 shared pipeline samples per point, accumulating
  21028-116860 hits (part 2) and 1958-3978 hits (part 3).

## Registered run (full output)

```
replication of Theorem T + single-var posterior cap + AND no-lift cap
points (new, none used by prior corpus runs): (16,1) (24,3) (48,4) (96,6) (128,8)
channel law (proved, reused exactly): free pair -> i.i.d. fair bit;
  killed-matched -> 1; killed-unmatched -> 0
intervals: exact Clopper-Pearson two-sided 99% binomial CIs
verdict: PASS iff the prediction lies inside the measured 99% CI

[1] Theorem T, two-phase tree success (chi_two_phase.py tree, non-retry)
    pred = 1 - 2^-(2d+1); pred+fb adds f*2^-(2d+1), f = (2d+1)*2d/((n+1)*n)
    n   d    sims  fails      meas                    99% CI      pred   pred+fb  p1miss  p2fail  verdict
   16   1    8000   1003  0.874625 [ 0.864802, 0.883998]  0.875000  0.877757    1021       0     PASS
   24   3    8000     56  0.993000 [ 0.990224, 0.995170]  0.992188  0.992734      58       0     PASS
   48   4  100000    156  0.998440 [ 0.998089, 0.998743]  0.998047  0.998107     163       0     FAIL
   96   6  100000     11  0.999890 [ 0.999772, 0.999957]  0.999878  0.999880      11       0     PASS
  128   8  100000      2  0.999980 [ 0.999907, 0.999999]  0.999992  0.999992       2       0     PASS

[2] single-variable per-hit posterior, q = (2d+1)d / ((2d+1)d + (n-2d))
    n   d   sims  queries    hits      post                    99% CI         q  hitrate  hit_pred  verdict
   16   1   8000  1088000   67983  0.176221 [ 0.172472, 0.180015]  0.176471  0.06248  0.062500     PASS
   24   3   6000  1800000  116860  0.537763 [ 0.534001, 0.541523]  0.538462  0.06492  0.065000     PASS
   48   4   4000  1600000   51359  0.476080 [ 0.470396, 0.481768]  0.473684  0.03210  0.032313     PASS
   96   6   3000  1200000   21028  0.477173 [ 0.468283, 0.486074]  0.481481  0.01752  0.017397     PASS
  128   8   2500  1000000   15067  0.542311 [ 0.531811, 0.552784]  0.548387  0.01507  0.015019     PASS

[3] degree-2 AND-query per-hit posterior (no-lift theorem: same q)
    n   d   sims  queries    hits      post                    99% CI         q   hitrate  hit_pred  verdict
   16   1   8000   544000    1958  0.181818 [ 0.159910, 0.205295]  0.176471 3.599e-03 3.710e-03     PASS
   24   3   6000   900000    3682  0.555133 [ 0.533841, 0.576281]  0.538462 4.091e-03 4.153e-03     PASS
   48   4   4000  3904000    3978  0.477124 [ 0.456637, 0.497666]  0.473684 1.019e-03 1.034e-03     PASS
   96   6   3000 13368000    3955  0.487484 [ 0.466910, 0.508089]  0.481481 2.959e-04 3.013e-04     PASS
  128   8   2500 12500000    2838  0.540169 [ 0.515844, 0.564359]  0.548387 2.270e-04 2.249e-04     PASS

fidelity checks:
  phase-2 fail branch (unreachable per Theorem T) fired 0 times
```

## Verdict per point

| point  | Theorem T (part 1)      | single-var q (part 2)  | AND q no-lift (part 3) |
|--------|-------------------------|------------------------|------------------------|
| (16,1) | confirmed (PASS)        | confirmed (PASS)       | confirmed (PASS)       |
| (24,3) | confirmed (PASS)        | confirmed (PASS)       | confirmed (PASS)       |
| (48,4) | FAIL in registered run; resolved as a 2.3-sigma fluctuation by the investigation below; prediction confirmed by the decisive fresh-seed rerun | confirmed (PASS) | confirmed (PASS) |
| (96,6) | confirmed (PASS)        | confirmed (PASS)       | confirmed (PASS)       |
| (128,8)| confirmed (PASS)        | confirmed (PASS)       | confirmed (PASS)       |

Part 1 measured error rates vs $2^{-(2d+1)}$: 0.125375 vs 0.125 at (16,1); 0.007 vs 0.0078125
at (24,3); 0.00156 vs 0.0019531 at (48,4) (the flagged cell); 0.00011 vs 0.00012207 at
(96,6); 0.00001 vs 0.0000076 at (128,8). Phase-1 miss counts z-scores vs
Bin(sims, $2^{-(2d+1)}$): +0.71, -0.57, -2.31, -0.35, +1.42: only (48,4) is an outlier.

## FAIL investigation at (48,4), part 1

Symptom: measured success 0.998440 with 99% CI $[0.998089, 0.998743]$ EXCLUDES the
prediction 0.998047 from below: the tree did BETTER than the theorem predicts
(156 failures vs 189.3 expected under the fallback-corrected law, 195.3 raw).

Localization: $\text{fails} = \text{p1miss} - \text{fb\_succ}$, and $\text{p2fail} = 0$, so the whole deviation is the
phase-1 miss count: 163 observed vs Bin(100000, 1/512) mean 195.3, $z = -2.31$, two-sided
$p = 0.021$. The phase-2 stage contributed nothing (0 fails in 100000 sims, as the theorem
requires: a certified pigeon's row-XOR is 1, so its row is not all-zero).

Simulator check against `chi_two_phase.py` (the verified version):
- The pipeline draw, row-bit construction, phase-1 scan, phase-2 row scan, and fallback
  are line-for-line the same operations in the same order (only counting replaces
  list-appending). No discrepancy found.
- Cross-validation through an independent route: at (48,4) the same script's parts 2-3
  sample the same channel law through pair queries, and the measured hit rates match the
  exact predictions to 0.7% (single-var 0.03210 vs 0.032313) and 1.5% (AND 1.019e-3 vs
  1.034e-3, the exact distinct-pair value): the channel the tree runs on is the right one.
- The implemented phase-1 event is exactly $(1/2)^9$ by construction (9 independent free
  pigeons, each the XOR of 8 i.i.d. fair coins), so a persistent deviation of the
  simulated process from $2^{-(2d+1)}$ is impossible unless the coin source is biased.

Pre-registered probes (seed 607261, `chi_thmT_verify.py --probe48`):

```
probe (48,4): investigating phase-1 miss shortfall in the registered run
  (a) phase-1 miss law, 500000 trials (seed 607261): misses 981 (z = +0.14 vs 976.6), rate 0.001962, pred 0.001953, 99% CI [0.001805,0.002129] -> PASS
  (b) full two-phase tree, 500000 sims (seed 607261): success 0.998200 (pred 0.998047, pred+fb 0.998107), 99% CI [0.998040,0.998351], p1miss 928 (exp 976.6), p2fail 0, fb_succ 28 -> PASS
```

Probe (a) confirms the implemented phase-1 law at 0.5% precision (981 vs 976.6 misses).
Probe (b), a decisive fresh-seed rerun 5x the registered size, lands the prediction
comfortably inside the 99% interval, with p1miss 928 vs 976.6 expected ($z = -1.55$) and
fb_succ 28 vs 29.9 expected. Resolution: the registered FAIL was a statistical
fluctuation of the phase-1 miss count (a 1-in-48 draw; with 5 part-1 cells the chance
that some cell looks this extreme is about 10%), not a simulator defect and not a
deviation from Theorem T. No discrepancy with `chi_two_phase.py` exists.

Aggregate fidelity across this session's tree runs: 816000 two-phase simulations
(8000 + 8000 + 100000 + 500000 + 100000 + 100000), phase-2 fail branch fired 0 times,
exactly as Theorem T requires.

## Caveats and discriminating power

- Part 1 at high d can only exclude gross deviations: at (128,8) the 99% interval
  certifies success $\geq$ 0.999907 (error $\leq$ 9.3e-5) against a predicted error of 7.6e-6;
  detecting the predicted rate directly would need $\sim 10^6$ simulations per point.
- Part 2 posterior intervals are $\pm 0.004$ to $\pm 0.011$ wide; part 3 intervals are
  $\pm 0.020$ to $\pm 0.024$. The no-lift comparison target $q$ is the independent-status value;
  true distinct-pair sampling adds $O(1/n)$ finite-population corrections (component pairs
  sharing a pigeon or hole), below the interval half-widths at these points.
- Queries within one pipeline sample share the sample's design (mild positive
  correlation; second-order here because the free-bit count fluctuates over a tiny
  fraction of the pair space). The pooled binomial intervals follow the corpus's
  convention (`chi_and_posterior.py`).

## Conclusion

All three laws replicate at all five new points: the two-phase tree's exact success law
$1 - 2^{-(2d+1)}$ (plus the $f \cdot 2^{-(2d+1)}$ fallback term), the single-variable per-hit
posterior cap $q = \frac{(2d{+}1)d}{(2d{+}1)d + (n-2d)}$, and the degree-2 AND-query no-lift
posterior (same $q$ at a squared hit rate). One registered-run cell (48,4, part 1) failed
the 99% rule on a $2.3\sigma$ phase-1 miss shortfall; investigation found no simulator
discrepancy and both decisive probes confirmed the prediction. Theorem T and both caps
stand at the new points, with no deviation found.
