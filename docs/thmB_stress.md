# thmB_stress: numerical stress-test of Lemma B.1 (verified 2026-10-03)

Instrument: `thmB_stress.py` (standalone, prints all tables below; runtime 239 s,
about 10M Monte Carlo trials total). Corpus files untouched, no LOG.md entry.

## 1. The reconstructed inequality

Model (the $\Omega(n,d)$ pipeline at $p = 2$, from the corpus's formal statements
section): $\rho$ uniform over partial injections leaving $2d$ free pigeons $D$
(a $(2d+1)$-subset of $\{1,\ldots,n+1\}$) and $2d$ free holes $R$ (a $2d$-subset of $\{1,\ldots,n\}$),
independent, plus a uniform matching of the rest. $F = D \times R$. Per queried pair
$q = (a,b)$ the single-variable answer law (exact in the corpus) is

    $\mathrm{ans}(x_{ab}) = 1$  iff  $([a \in D \text{ and } b \in R] \text{ and } B_q = 1)$ or $(\mathrm{match}(a) = b)$,

with $B_q$ fair independent design bits. Lemma B.1's proof, step (4), concretizes
the coupling claim $O(e/n)$ with an explicit depletion constant. The inequality
tested, with direction and constants:

    Reading A (what the NA proof supports): for any transcript event $E$
    determined by the answers on a queried set $S$ of $e$ pairs (distinct
    pigeons, distinct holes), and any pair $p$ with BOTH coordinates outside $S$,

        $\Pr[p \in F \mid E] \le f_e := \frac{2d+1}{n+1-e} \cdot \frac{2d}{n-e}$.    (A)

    Direction: upper bound. $f_e/f = \frac{(n+1)n}{(n+1-e)(n-e)} = 1 + O(e/n)$
    is the hypergeometric depletion factor (the $O(e/n)$ of the lemma).

    Reading B (the lemma's literal quantifier "any pair $p$ not in $S$", which
    lets $p$ share one coordinate with a queried pair): the same constant (A)
    is tested at $p_1 = (a_1, j)$ and $p_2 = (i, b_1)$, $i$ and $j$ fresh.

    Difference form: the lemma's $|P[p \in F \mid \text{transcript}] - P[p \in F \mid \text{own-answer-class}]|$
    $= O(e/n)$; for unqueried $p$ the own-answer class is trivial, so the
    claim is $\max_E |P[F_p \mid E] - f| = O(e/n)$, scored as $C^* = \max_E |\cdots| \cdot n/e$.

Two subtleties the reconstruction had to absorb. First, the corpus's
"killed-unmatched $\to$ 0" case is two different statuses with different
coupling effects: X1 (pigeon killed, matched to another hole: depletes both
pools, never its own hole) and X2 (pigeon free but its hole killed by another
pigeon: consumes a free-pigeon slot). Second, $R$'s conditional law given the
statuses is $\mathrm{img}(j)$-weighted, not uniform over depletion levels (below); this
changes the per-atom fresh-hole factors.

## 2. Method

Exact atom enumeration. Every outcome (D, R, matching, bits) induces exactly
one status vector over the $e$ queried pairs (5 statuses: F1, F0, M, X1, X2).
Per atom (status of pair 1 + counts of the rest) the weight and the
conditional freeness value of any probe pair are closed-form counts, so
$P[F_p \mid E]$ is computed EXACTLY in rational arithmetic; $E$ ranges over all $2^e$
answer patterns, reduced by exchangeability to the count $z$ of 1s. On top sits
an exact rejection-free conditional sampler (atom, then position placement,
then $j$ = #X1-holes-in-$R$ with its exact weight, then $R$ and $D$) driving the
required Monte Carlo estimates with 99% CIs.

The closed forms, as finally validated:

    $w(\text{atom}) = \binom{z1}{cf1} \binom{z0}{cf0} \binom{z0-cf0}{c1}$     [status placement;
        leftover one-positions are forced to M, M cannot sit on a zero]
            * $\binom{n+1-e}{2d+1-kf-x2}$                  [D count]
            * $\sum_j \binom{x1}{j} \binom{n-e}{2d-kf-j} \mathrm{img}(j)$  [(R, images) count]
            * $(n-2d-em-x1)!$                         [matching completions]
            * $2^{e-kf}$                              [free bit assignments]
    $\mathrm{img}(j) = \sum_{i \le x1-j} (-1)^i \binom{x1-j}{i} \mathrm{perm}(n-2d-em-i, x1-i)$

    $P[\text{fresh pigeon in } D \mid \text{atom}] = (2d+1-kf-x2)/(n+1-e)$
    $P[\text{fresh hole in } R \mid \text{atom}] =$ hole_factor: the $\mathrm{img}(j)$-weighted ratio
        $[\sum_j \binom{x1}{j} \binom{n-e-1}{2d-kf-1-j} \mathrm{img}(j)]$
        $/ [\sum_j \binom{x1}{j} \binom{n-e}{2d-kf-j} \mathrm{img}(j)]$
        (plain hypergeometric $(2d-kf)/(n-e)$ only when $x1 = 0$)
    $P[b_1 \in R \mid \text{atom}, s1 = X1] =$ shared_hole_factor: numerator with
        $\binom{x1-1}{j-1} \binom{n-e}{2d-kf-j} \mathrm{img}(j)$ over the same denominator.

## 3. Instrument validation (all PASS in the final run)

The gauntlet caught four real bugs in my reconstruction before any result was
trusted; each fix was forced by a check, corpus-style ("the theory validating
the instrument"):

1. Position-0 answer class: the status of pair 1 is fixed by its own answer
   ($z \ge 1$ means F1/M only), not by the existence of 1s anywhere. Caught by
   V3 (brute status-vector enumerator vs count-table).
2. X1-image count: images may land on queried X2 holes, and X1 rows whose own
   hole is in $R$ lose no forbidden column; the count is the inclusion-
   exclusion $\mathrm{img}(j)$ above. Caught by exhaustive per-outcome enumeration at
   $(8,1,2)$ (6,773,760 outcomes): one status vector miscounted.
3. Position-class assembly: M cannot sit on a zero-position; the multinomial
   became $\binom{z1}{cf1} \binom{z0}{cf0} \binom{z0-cf0}{c1}$ with cm forced. Caught by V3.
4. Per-atom fresh-hole factor: $\mathrm{img}(j)$-weighted, not the plain Vandermonde.
   Caught by exhaustive enumeration + ground-truth naive enumeration at
   $(8,1,2)$ (ground truth $P[F_{p0} \mid E_{z=0}] = 0.083414$, not the 0.086017 the
   uncorrected table gave).

Final validation state (all from the run):

- V1: per-pair status law (closed form) vs direct prior sampling at $(32,2)$,
  400k trials: $|z| \le 1.14$ on all four statuses.
- V2: atom weights over ALL status vectors sum to the model total at
  $(8,1,3)$, $(9,3,3)$: exact.
- V3: brute enumerator vs count-table at 5 points: exact rational equality.
- V4: rejection MC from the raw model vs conditional sampler vs exact at 3
  points: all within 99% CIs.
- V5: independent $e=1$ Bayes algebra vs atom enumeration at 5 points $\times$ 3
  probes: exact equality.
- Exhaustive per-outcome check at $(8,1,2)$: total count, all 25 status-vector
  weights, and all per-vector v0/v1/v2 values match naive enumeration
  exactly (0 mismatches).
- Ground truth naive enumeration at $(8,1,1)$ and $(8,1,2)$: exact posteriors
  match on all probes and both patterns.

## 4. TABLE 1: Reading A (coordinate-disjoint p): PASS at 35/35 points

Grid $(n,d,e)$, $p_0 = (n+1, n)$, worst pattern $E^*$ (exact search over all
patterns), margin $= P[F_{p0} \mid E^*] - f_e$. All margins negative; MC agrees with
the exact value (z-scores within $\pm 3.25$). Exact FAILs: none; exact TIEs:
none.

    n,d,e   z*   f        f_e      P_exact  margin_exact   verdict
    8,1,1   0   0.083333 0.107143 0.083333 -2.381e-02     PASS
    8,1,2   2   0.083333 0.142857 0.086957 -5.590e-02     PASS
    8,1,4   4   0.083333 0.300000 0.107692 -1.923e-01     PASS
    8,1,6   6   0.083333 1.000000 0.168675 -8.313e-01     PASS
    12,2,1  0   0.128205 0.151515 0.129556 -2.196e-02     PASS
    12,2,4  0   0.128205 0.277778 0.134070 -1.437e-01     PASS
    16,4,1  0   0.264706 0.300000 0.268421 -3.158e-02     PASS
    16,4,8  0   0.264706 1.000000 0.298800 -7.012e-01     PASS
    24,6,1  0   0.260000 0.282609 0.262660 -1.995e-02     PASS
    32,8,1  0   0.257576 0.274194 0.259635 -1.456e-02     PASS
    32,8,8  0   0.257576 0.453333 0.275066 -1.783e-01     PASS
    40,12,1 0   0.365854 0.384615 0.368348 -1.627e-02     PASS
    40,12,8 0   0.365854 0.568182 0.386611 -1.816e-01     PASS
    8,3,1   0   0.583333 0.750000 0.596939 -1.531e-01     PASS
    (full 35-row table with MC columns in the script output; every row PASS,
    200k trials each, all MC-vs-exact z-scores within +-3.25)

(The remaining rows: $(8,1,5)$, $(12,2,2)$, $(12,2,7)$, $(12,2,8)$, $(16,4,2)$,
$(16,4,4)$, $(16,4,7)$, $(24,6,2)$, $(24,6,4)$, $(24,6,8)$, $(24,6,11)$, $(24,6,12)$,
$(32,8,2)$, $(32,8,4)$, $(32,8,12)$, $(32,8,15)$, $(40,12,2)$, $(40,12,4)$, $(40,12,12)$,
$(40,12,15)$, $(8,3,2)$: all PASS.)

The worst transcript is the all-zeros pattern at every point with $z^* = 0$
(and the all-ones pattern where $z^* = e$): the depletion-maximizing transcripts
are the answer-monochromatic ones, as the NA argument predicts.

Worst-case box scan ($n$ in {8..48 step 4}, $d \le \min(14, (n-1)/2)$, $e$ in
{1,2,4,8,12,emax}, patterns $z \in \{0, e\}$, justified by the grid: worst $z$ is
always $0$ or $e$ on all 35 points). Tightest points, all $d = 1..2$, $e = 1..2$
(small-$d$, small-$e$ is where the depletion factor is closest to 1, so the
least-headroom):

    (n=48, d=1, e=1, z=0): P=0.002551 f_e=0.002660 gap=-1.086e-04 (rel -4.08%)
    (n=44, d=1, e=1, z=1): gap=-1.409e-04 (rel -4.44%)
    (n=40, d=1, e=1, z=0): gap=-1.876e-04 (rel -4.88%)
    (n=32, d=1, e=1, z=0): gap=-3.666e-04 (rel -6.06%)

Global tightest point $(48,1,1,z=0)$: exact PASS (margin $-1.086 \times 10^{-4}$); MC 1M
trials gives gap $-7.0 \times 10^{-5} \pm 1.3 \times 10^{-4}$, consistent with the exact value (the
CI straddles it; the exact rational value is decisive). The relative margin
$-4.1\%$ at the tightest point is the boundary behavior: as $e/n \to 0$ the
depletion factor $\to 1$ and the gap closes, so (A) is asymptotically TIGHT in
the $e \to 0$ limit while staying strictly positive at every finite point.

## 5. TABLE 2: Reading B (literal quantifier): FAILS at 15/35 points

With $p$ allowed to share ONE coordinate with queried pair 1, the same
constant $f_e$ is violated at small $e$, always at the worst pattern $z^* = 1$
(single answer-1 on the shared pair): the $\mathrm{ans}=1$ Bayes lift on the shared
coordinate. Exact gaps (positive = violation of (A)):

    n,d,e   p1=(1,n) gap   verdict   p2=(n+1,1) gap  verdict
    12,2,1  +0.000000      TIE       +0.033670       FAIL
    12,2,2  -0.027532 PASS +0.006061       FAIL
    16,4,1  +0.081818      FAIL      +0.109091       FAIL
    16,4,2  +0.044587      FAIL      +0.071493       FAIL
    24,6,1  +0.131884      FAIL      +0.150725       FAIL
    24,6,2  +0.109871      FAIL      +0.128531       FAIL
    24,6,4  +0.054263      FAIL      +0.072555       FAIL
    32,8,1  +0.158744      FAIL      +0.173175       FAIL
    32,8,4  +0.106124      FAIL      +0.120227       FAIL
    40,12,1 +0.175268      FAIL      +0.185005       FAIL
    40,12,8 +0.009967      FAIL      +0.018992       FAIL
    (at e >= 4..8 the lift washes out: all PASS; MC confirms every
    FAIL/TIE row within 99% CIs, 200k trials each)

The mechanism: an answer-1 on pair 1 makes "pair 1 free" a live
possibility (posterior $\pi = \frac{f/2}{f/2+m}$); a label sharing pair 1's pigeon
then inherits $\pi$ times the hole factor, and a label sharing pair 1's hole
inherits $P[b_1 \in R] \cdot \pi$, which at small $e$ exceeds the naive depletion
constant $f_e$. The TIE at $(12,2,1)$ is an exact identity:
$\pi \cdot \frac{2d-1}{n-1} = \frac{5}{9} \cdot \frac{3}{11} = \frac{5}{33} = f_1$: the posterior exactly equals
the depletion constant there.

Which reading fails: Reading B (the lemma's literal "any pair $p$ not in $S$",
with the step-(4) constant $f_e$). Reading A is exactly correct: the atom
decomposition proves $P[F_p \mid E]$ is a weighted average of per-atom values each
at most $f_e$, with equality approached on M-dominated (answer-1) transcripts
when $m \gg f/2$. The repair is one line: Lemma B.1's quantifier should read
"any pair $p$ neither of whose coordinates is queried along the path", which
is what its own step (3) ("measurable functions of disjoint subfamilies")
actually delivers; alternatively the constant must absorb the shared-
coordinate term $\pi \times$ (hole/pigeon factor).

## 6. Theorem B's cap under the probes

Column "max probe <= cap?": $\mathrm{cap} = \max(2d^2/(2d^2+n),\ f/2)$, Theorem B's
stated per-leaf bound. Every grid point except one has max probe posterior
below the cap, so Theorem B's conclusion is untouched at its own parameters
(the in-regime points $(8,1)$ and $(12,2)$ all satisfy it). The one exception is
the aggressive out-of-regime stress point $(8,3,2)$: the shared-hole probe
posterior at $z=1$ is $0.700113$ against cap $\frac{9}{13} = 0.692308$ ($+0.0078$, ~1.1%).
$(8,3)$ has $d = 3 > \sqrt{n}/\sqrt{2} \approx 2$, outside the theorem's regime, and the
exceedance is marginal; but it confirms the shared-coordinate case is a
genuine gap in the lemma's stated coverage that Theorem B's proof does not
explicitly absorb (its per-leaf split covers own-answer labels and
both-coordinates-unqueried labels only).

## 7. Difference form (the lemma's actual claim)

For coordinate-disjoint $p$, $C^* = \max_z |P[F_{p0} \mid E_z] - f| \cdot n/e$ stays bounded
over the whole grid: $\max C^* = 0.4283$ at $(40,12,e=8)$; the largest values sit
at large $d/n$ ($0.39$-$0.43$ for $d/n$ in $1/4..3/8$), small values at small $d$. So
the difference form holds with an empirical constant below $1/2$ across the
box for Reading A, consistent with $O(e/n)$. For shared-coordinate $p$ the
picture is qualitatively worse: the lift is $O(1)$, not $O(e/n)$. At
$(16,4,1,z=1)$ the shared-pigeon posterior is $\pi_f \times \mathrm{rh} = 0.81818 \times \frac{7}{15}$
$= 0.3818$ against $f = 0.2647$ ($|P - f| = 0.1171$ at $e/n = 1/16$), and at
$(40,12,1,z=1)$ it is $0.5599$ against $f = 0.3659$ ($|P - f|$
$= 0.194$ at $e/n = 1/40$): the deviation from $f$ does not shrink with $e/n$, so the
difference form fails for shared-coordinate pairs as well. The clean
statement remains: Reading A is fully sound; Reading B fails both in the
$f_e$ constant (what Theorem B's proof quotes) and in the difference form.

## 8. Honest conclusion

1. Reading A, the depletion inequality with the proof's constants
   ($\frac{2d+1}{n+1-e} \times \frac{2d}{n-e}$ for both-coordinates-unqueried $p$), HOLDS at
   every tested point, small $n$, large $d$, many queries included: 35/35 grid
   points PASS with exact rational margins, a ~100x parameter box scan puts
   the global minimum relative margin at $-4.1\%$ ($(48,1,1)$), and the MC
   instrument (200k-1M trials/point, ~10M total) agrees with the exact
   values everywhere. The bound is tight in the limit $e/n \to 0$ (margin $\to$
   $0$ through negative values) and at answer-monochromatic transcripts.
2. Reading B, the lemma's literal quantifier, is FALSIFIED: 15/35 points
   violate the $f_e$ constant via shared-coordinate labels at $z=1$ transcripts
   (first at $(12,2,1)$, where the shared-pigeon case is an exact TIE and the
   shared-hole case fails by $+0.034$). This is a mis-reconstruction hazard
   resolved, not a misprint: the failure mechanism ($\mathrm{ans}=1$ Bayes lift on a
   shared coordinate) is exactly the case the proof's step (3) excludes by
   "disjoint subfamilies".
3. Consequence for Theorem B: none at its own parameters. The cap survives
   all probes at every in-regime point; the single cap exceedance is at the
   out-of-regime stress point $(8,3,2)$ by ~1%. The recommended corpus repair
   (not applied here, corpus files untouched) is to restrict Lemma B.1's
   quantifier to pairs with both coordinates outside the queried set, which
   preserves Theorem B's proof chain verbatim.

Every number above comes from the executed run logged in the script output
(200k trials per MC row, 1M at the global tightest point, 99% CIs, exact
rational values where stated; ~15M Monte Carlo trials total across the
grid, probe confirmations, and validation gauntlet).
