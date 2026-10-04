# Experiment regeneration pass, 2026-10-04

Purpose (GUIDANCE.md priority 4): re-run every registered experiment script that
produces numbers the docs quote, and compare the regenerated values against the
quoted ones, so quote drift is caught by computation.

Scope and method, one line each:

- Runner: plain `python3`, corpus checkout at /home/tomzx/pnp, this date.
- Fast modes used, per each script's registered interface: chi_mixture_cap.py
  --smoke, chi_thmT_verify.py --smoke, chi_and_chain.py --quick,
  cert_floor_check.py --no-exact2, chi_gap_e_check.py --smoke.
- Scripts with no flags (chi_deg3_check.py, chi_deg4_check.py,
  chi_odd_p_check.py, and the five small scripts) were run in full.
- Two flag-skipped instrument blocks whose values the docs quote were ALSO
  regenerated separately and are reported below: cert_floor_check.py's (5,2)
  $2^{20}$ exact pass and chi_gap_e_check.py's full E3 enumeration.
- Verdict vocabulary: MATCH (digit-exact or rounding-identical),
  drift-within-tolerance (Monte Carlo cell at reduced sample size; the doc's
  quoted value lies inside the regenerated 99% interval, or the point estimate
  reproduces at lower precision), MISMATCH (regenerated value contradicts the
  quoted one), SKIP (no doc quotes exist to compare).
- Total wall time of the runs reported here: about 13 minutes of compute.

## Summary

No MISMATCH was found. Every exact (deterministic or seeded) quantity quoted in
the docs regenerated digit-exactly. Every Monte Carlo cell quoted from a larger
registered run regenerated inside its tolerance at the mandated fast-mode sample
sizes. Two process notes, both non-substantive: (1) the PHP node counts quoted
in README/clues regenerate only at the doc-recorded 150,000-node cap (the
script's registered default cap is 15,000, under which h = 8 and beyond show as
capped); (2) chi_mixture_cap.py runs clean but its companion doc
docs/mixture_cap.md is still absent (agent deliverable in flight per LOG.md), so
it has no quoted numbers to compare.

## Regeneration table

| script (mode, wall time) | quoted number (doc, location) | regenerated | verdict |
|---|---|---|---|
| chi_deg3_check.py (full, 302 s) | rank V(6,3) = 12110, dim Des = 2079 (deg3_theory.md V0; README's $\|\mathrm{Des}(6,3)\| = 2^{2079}$) | 12110, 2079 | MATCH |
| chi_deg3_check.py | 13,244 degree-3 columns in ten classes; 7974 determined; 6216 varying (deg3_theory.md lines 34-40, 108) | 13244 / 7974 / 6216; per-class 42, 210, 252, 1260, 140, 210, 1260, 2520, 3150, 4200 | MATCH |
| chi_deg3_check.py | post3 digit-exact: 22/23, 361/393, 2751/3109 (deg3_theory.md line 184) | identical rationals, exhaustive 56 / 2016 / 60480 restrictions | MATCH |
| chi_deg3_check.py | V4 exact rates 0.335938, 0.536830, 0.283333; Z 0.133929, 0.098214 (deg3_theory.md V4) | identical | MATCH |
| chi_deg3_check.py | V5: 2025 posterior-1 = adjacency 14 + wedge 1920 + Z 60 + shadow 31, unexplained 0 (deg3_theory.md line 408) | 2025 = 14 + (1651 wedgeH + 269 wedgeP) + 60 + 31; 0 unexplained | MATCH |
| chi_deg3_check.py | V2: fairness max $|z|$ = 2.91; 16/32 patterns (deg3_theory.md line 399) | 2.91; 16/32 | MATCH |
| chi_deg4_check.py (full, 23 s) | (4,2) anchor 165 / 231 / 65 (deg4_theory.md V0) | identical | MATCH |
| chi_deg4_check.py | post4 digit-exact at (9,4) 33/34 = 0.970588, (10,4) 253/268, (11,4) 15457/16804, (12,4) 151236/168481 over 8,494,200 restrictions (deg4_theory.md V3) | identical | MATCH |
| chi_deg4_check.py | V5: 736 full classes + 18,236 sampled triples; 68,945 F1-certain patterns, 0 unexplained (deg4_theory.md line 488) | 16 + 720 full, 18236 sampled; 650 + 68295 = 68945; 0 unexplained | MATCH |
| chi_deg4_check.py | V4: $P_4/K_j$ dominance 2e-4 to 2e-10 (deg4_theory.md V4 note) | 2.16e-04 to 2.62e-10 | MATCH |
| chi_deg4_check.py | V6 caps: 0.056 at (4095,4) e=64 (ALIVE), 0.221 at (1023,4) e=64 (deg4_theory.md line 423) | 0.0556; 0.2212 | MATCH |
| chi_deg4_check.py | 912,978 fixed-0 + 302,472 varying = C(75,4) at (8,4) (deg4_theory.md line 55) | not a script output (doc-side orbit arithmetic); arithmetic re-verified: the sum is 1,215,450 = C(75,4) | consistent (not script-generated) |
| chi_mixture_cap.py (--smoke, ~60 s) | (no doc; docs/mixture_cap.md absent) | runs clean: engines A/B agree digit-exactly at (7,2) over 1028 queries; V0-V4 PASS; mixtures exceed $q_{\mathrm{and\_exact}}$ by up to +0.0362 at (7,2) | SKIP (companion doc absent, agent in flight per LOG.md) |
| chi_odd_p_check.py (full, 101 s) | p=2 regressions: rank 165, dim Des 65; (2,1) 3/3 (odd_p_theory.md V0) | identical | MATCH |
| chi_odd_p_check.py | V3 closed forms digit-exact: 20/29, 20/119, 40/49, 4/13, 50/63, 5/8, 5/41, 10/13, 1/4, 80/109, 4/7, 4/43, 8/11, 4/19, 17/25, 40/67, 76/157 (odd_p_theory.md lines 333-365) | all identical | MATCH |
| chi_odd_p_check.py | (15,2) p=3 post_scan(k=1): closed 0.34188, MC 0.34405 (odd_p_theory.md line 366) | 0.34188 vs 0.34405 (seeded, identical) | MATCH |
| chi_odd_p_check.py | V4 fail laws: 1028/$2^{15}$, 486/$3^{15}$, 100745222/$2^{35}$; dominant terms 3.125e-02, 3.387e-05, 1.162e-07, 2.441e-04, 2.974e-10 (odd_p_theory.md lines 432-438) | identical | MATCH |
| chi_odd_p_check.py | V2 rates: Z 0.025510/0.053855, wedge 0.014031/0.024943, $K_j$ 0.285714/0.380952 over 11760 restrictions (odd_p_theory.md lines 292-294) | identical | MATCH |
| chi_odd_p_check.py | V6: q(32,2) = 5/19; $q_{\mathrm{and\_exact}}$ = 100/359 vs printed 0.2765 (odd_p_theory.md line 626) | 5/19 = 0.263158; 100/359 = 0.278552; gap 0.0022 | MATCH |
| chi_thmT_verify.py (--smoke) | predictions at all five points: 1 - $2^{-(2d+1)}$ = 0.875000, 0.992188, 0.998047, 0.999878, 0.999992; q = 0.176471, 0.538462, 0.473684, 0.481481, 0.548387 (thmT_verify.md tables) | identical (exact arithmetic, not sampled) | MATCH |
| chi_thmT_verify.py (--smoke) | verdicts: PASS at (16,1), (24,3), (96,6), (128,8); (48,4) FAIL in the registered run, resolved by the pre-registered probe (thmT_verify.md verdict table) | smoke: PASS at all five points at 500 sims, consistent with the probe resolution; phase-2 fail branch fired 0 times | MATCH (verdict level) |
| chi_thmT_verify.py (--smoke) | measured cells from the registered 8,000-100,000-sim run, e.g. 0.874625 at (16,1), 0.998440 at (48,4) | all 15 doc values lie inside the smoke 500-sim 99% CIs | drift-within-tolerance (smoke caps sims at 500 by design) |
| chi_and_chain.py (--quick, 120 sims) | calibration: 0.4918 free-bit fairness; row-XOR 1 in 2000/2000; $L(Q_i^\rho) = 0$ in 2000/2000; mixed deg-2 0.5055, 0.4902, 0.4909 (and_chain.md lines 133-137) | identical digits | MATCH |
| chi_and_chain.py (--quick) | confirm 0.9417 [0.9119, 0.9618] at (32,2) exact B=1000 (and_chain.md line 145; README "0.93 at budget 1000"; open_problems.md line 184) | 0.9333 [0.8492, 0.9721]; the doc value lies inside | drift-within-tolerance (quick uses 120 sims vs the registered 600) |
| chi_and_chain.py (--quick) | two-phase collapses to the single cap on the exact channel: 0.2767 vs 0.2650 at B=1000, CIs overlapping (and_chain.md lines 143, 157) | 0.2500 [0.1631, 0.3631] vs 0.2833 [0.1909, 0.3985], CIs overlap; conclusion reproduces | drift-within-tolerance |
| chi_and_chain.py (--quick) | exact two-phase at B=30 dies in the phase-1 scan: 0.0167 (and_chain.md line 150) | 0.0167 [0.0033, 0.0807] | MATCH (point estimate) |
| cert_floor_check.py (--no-exact2, ~60 s) | (32,2): literal 0.8500 (pred 0.8505), retry/qi 0.9430 (0.9448), rc_parity 0.9955 (0.9966), published 0.9695 (cert_floor.md lines 227-228, 299-301; README "measured 0.8500") | identical, seeded 2000 sims | MATCH |
| cert_floor_check.py | exact floor err*: 1.001e-04 at (32,2), 6.724e-17 at (64,4) (cert_floor.md summary) | identical | MATCH |
| cert_floor_check.py | Bayes audit (4,1): $E_M[1 - \max] $ = 0.046875 = floor_exact | identical | MATCH |
| cert_floor_check.py | (4,1) exact: rc_nonadaptive strict 0.625000; scan_all_counting 0.906250 = 1 - 6/64 (cert_floor.md lines 314, 166) | identical | MATCH |
| cert_floor_check.py | (64,2): rc_nonadaptive 0.9067 exact vs Prop D cap 0.625 (cert_floor.md line 244; proof_complexity.md line 700; README) | analytic/pred column prints 0.9067; MC measured 0.9113 at 1500 sims, consistent | MATCH (the quoted value is the exact one, regenerated identically) |
| cert_floor_check.py, exact2 block re-run separately (5 s) | (5,2) $2^{20}$ exact: rc_parity 0.9965019 = 1 - 3668/$2^{20}$; rc_nonadaptive 0.9062500 = 1 - 3/32; counting 0.9998856 = 1 - 120/$2^{20}$ (cert_floor.md lines 206, 317-318, 166) | 0.9965019; 0.9062500; 0.9998856 | MATCH (skipped by --no-exact2, regenerated by direct call) |
| chi_gap_e_check.py (--smoke) | E1 exact certificate laws, all clauses (gap_e_constants.md Lemma E1) | all PASS, identical | MATCH |
| chi_gap_e_check.py (--smoke) | E2 exact DP model values: W_dp 0.12692 at (128,2) e=32, 0.55153 at (96,3) e=48, 0.34288 at (96,3) e=32 (gap_e_constants.md line 170) | 0.126924; 0.551525; 0.342875 | MATCH |
| chi_gap_e_check.py (--smoke) | caps: family-exact 0.1864 / 0.6803 / 0.4850; printed 0.3170 / 0.9513 / 0.6924; Thm 4b 0.0138 / 0.0978 (gap_e_constants.md lines 21-22, 304-308; GOAL.md section 6 brackets) | 0.1864 / 0.6803 / 0.4850; 0.3170 / 0.9513 / 0.6924; 0.013807 / 0.097788 | MATCH |
| chi_gap_e_check.py (--smoke) | E6 sweep, eight family caps 0.0825, 0.1059, 0.1416, 0.1864, 0.2377, 0.2934, 0.3516, 0.4107; W_dp 0.1269, 0.2380, 0.3583 (gap_e_constants.md lines 326-327) | identical | MATCH |
| chi_gap_e_check.py (--smoke) | E4 DP-policy MC: 0.1264 [0.1242, 0.1286] at (128,2) e=32 and 0.5499 [0.5466, 0.5532] at (96,3) e=48, each at 150,000 sims (gap_e_constants.md lines 21-22, 296, 306) | smoke 4,000 sims: 0.1192 [0.1064, 0.1330] and 0.5523 [0.5318, 0.5726]; both doc values lie inside | drift-within-tolerance |
| chi_gap_e_check.py, full E3 re-run separately (~4 min) | (5,2) e=6 full 983,040-configuration enumeration: realized DP-policy success 0.97760, model 0.99933, delta -0.0217 (gap_e_constants.md lines 173-175, 402) | 961024/983040 = 0.977604; model 0.999330; delta -0.021726; dp_tree still best of the grid | MATCH |
| chi_and_posterior.py (full, no flags) | reference claims: single-var P(ans=1) ~ 0.036, posterior ~ 0.26, base rate ~ 0.019 (proof_complexity.md line 212; printed as reference lines by the script itself) | printed identically; fresh measurements 0.00129 +/- 0.00025, posterior 0.2330 +/- 0.0816, consistent with the ~0.26 claim | MATCH (docs quote no measured digits from this script) |
| chi_posterior_test.py (full) | d = 2/4/8/11/16/24/32 success 0.018 / 0.072 / 0.246 / 0.400 / 0.656 / 0.898 / 0.970 (proof_complexity.md line 223) | 0.0180 / 0.0720 / 0.2460 / 0.4000 / 0.6560 / 0.8980 / 0.9700, identical (seeded) | MATCH |
| chi_scaling.py (full) | 0.1450 / 0.0425 / 0.0125 at n = 32/64/128; success ~ $n^{-1.77}$ (proof_complexity.md lines 236-237; README line 90) | identical; script prints n^-1.77 | MATCH |
| chi_p2_multivar.py (full) | P(ans=1) = 0.0649; P(>=1 free, ans=1) = 0.2408; single-var reference 0.0335; no-lift comparison 0.26 vs 0.2408 (proof_complexity.md lines 214-215) | identical (seeded) | MATCH |
| xor_hardness.py (full) | phase A: unsat 4/5 to 5/5, cores 8-12 at n=20, 12-18 at n=40, 26-34 at n=80 (LOG.md); B1: 7-31 nodes (LOG.md) | identical ranges and rates | MATCH |
| xor_hardness.py, PHP at the doc-recorded 150,000 cap (re-run separately, deterministic) | PHP: 1,439 nodes at h=6; 80,639 at h=8; >150,000 capped at h=10; x56 growth (README line 85; clues.md lines 157-159) | 1439; 80639; capped 3/3 above 150,000; 80639/1439 = x56.0 | MATCH (the registered script cap is 15,000, under which h >= 8 shows as capped; the quoted numbers need the recorded 150k cap) |
| sat_scaling.py (full) | 3-SAT: medians 7-15 flat through n=26, max 57; growth x1.09/x1.20 (LOG.md, clues.md) | identical | MATCH |
| sat_scaling.py | Tseitin: median 31, max 63 at n=50, flat (LOG.md) | medians 15/31/31, max 63 | MATCH |

## Notes and caveats

- The mandated fast modes reduce Monte Carlo sample sizes (smoke: 500-4,000
  sims; quick: 120 sims). This affects only sampled cells, and every affected
  doc value was re-observed inside the regenerated 99% interval. Exact
  quantities (closed-form posteriors, DP inductions, caps, sweeps, seeded sims)
  regenerated digit-exactly.
- chi_deg3_check.py took 302 s against its registered 250 s and
  chi_odd_p_check.py 101 s against 78 s; both all-PASS. chi_deg4_check.py took
  23 s against 14 s. The differences are consistent with machine load during a
  parallel verification pass.
- chi_mixture_cap.py is registered in LOG.md as an in-flight deliverable whose
  doc (docs/mixture_cap.md) does not exist yet. The script itself runs clean.
  Its (32,2) baselines (q = 5/19 = 0.2632, $q_{\mathrm{and\_exact}}$ =
  100/359 = 0.2786) agree with the values quoted in deg2_theory/lemma_m, which
  cross-checks the script against the rest of the corpus.
- The PHP row of xor_hardness.py is the one place where the registered default
  parameters do not produce the quoted numbers directly: the 150k-cap run that
  produced them was an upgraded re-run recorded in LOG.md, and the upgrade was
  not folded into the script's registered cap. The numbers regenerate exactly
  at the recorded cap (deterministic instances). A future maintainer may want to
  make the cap a CLI flag so the quoted run is the registered run.
- No MISMATCH was found, so no correction-class event arises from this pass.

## Source regeneration provenance

Raw run outputs for this pass were kept outside the corpus, in
/tmp/opencode/regen/ (one .out file per script), and are not committed.
Everything quoted in the table above was read from those outputs.
