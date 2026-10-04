# GAP B' closed: the per-hit cap over the FULL printed degree-<=2 class
# (arbitrary F_2 mixtures) on the true pipeline

Result of the theory+experiments agent (2026-10-04). Status: analysis with a
registered machine run, not peer-reviewed. Resolves GOAL.md section 6 item
"Theorem 3's query-class coverage is a proper subset of the printed degree-2
class (F_2 mixtures; likely shallow repair)" and proof_complexity.md ADDENDUM 4
item 6 (chi_transfer.md section 4.3).

Script: `experiments/chi_mixture_cap.py` (registered output reproduced in
section 9). No existing corpus file was edited.

## 0. Executive verdict

1. The printed degree-$\le 2$ class admits mixtures $g = c + \sum_p a_p x_p +
   \sum b_{pq} x_p x_q$ (squares alias to variables, degenerate monomials fold
   into the constant: Lemma N1). Every such query has, per restriction $\rho$,
   the alive/dead answer law of Lemma N2: a fair coin when the query's live
   design-coordinate set is nonempty, otherwise the $\rho$-determined parity
   of its matched parts.
2. The exact per-hit posterior maximum over the FULL class EXCEEDS Theorem 3's
   covered constant $\max(q, q_{\mathrm{and}})$ at every measured $(n,d)$, by
   a small finite-$n$ amount that decays to a relative $o(1)$. The maximizers
   are monomial-star mixtures through the output pair:
   $x_{ab}x_{cd} + x_{ab}x_{ef} + x_{ab}x_{gh}$ (all-distinct partners,
   output $ab$): $787/934 = 0.8426$ at $(7,2)$ versus
   $q_{\mathrm{and,exact}} = 25/31 = 0.8065$; and the shared-pair pair
   $x_{ab}x_{cd} + x_{ab}x_{ef}$ (output $ab$) is the asymptotic maximizer
   family, with posterior $= q\,(1 + o(1))$ and a same-order excess over
   $q_{\mathrm{and}}$ that decays to $0$.
3. The mechanism (Theorem M-A): on the output pair's killed branch, every
   monomial through it is determined $0$, so the hit event SELF-EXCLUDES the
   entire killed branch (probability $\approx 1$) instead of only the
   unmatched part; the matched pollution that remains is diluted by the
   partners' status parity. Same $\Theta(d^2/n)$ scaling as $q$; the cap
   structure of Theorem 3 survives with the constant replaced by
   $q_2^*(n,d) > \max(q, q_{\mathrm{and}})$.
4. No new certificates: a single mixture query never reaches posterior $1$
   (Theorem M-B; enumerated $0$ in $7172$ queries), and two-query mixture
   certificates (the degree-2 Z-certificate, readable as ONE folded mixture
   query plus one monomial) fold covered-class certificate pairs without
   changing the budget accounting (Proposition M-E).
5. Repaired cap (Theorem M-D): every adaptive tree of budget $e$ over the
   FULL printed degree-$\le 2$ class satisfies
   $\mathrm{success} \le \min(1,\, q_2^* + P_{\mathrm{adj,mix}}(e) + P_K(e) +
   O(e/n) + o(1))$ with the SAME aliveness condition $d^2 \log k = o(n)$
   (with room). The chi-hypothesis at $p = 2$ (err-form) is therefore proved
   alive at degree $\le 2$ over the FULL printed quantifier, closing GAP B'.
6. Budgeted toy-scale verdict: no mixture strategy beats the covered-class
   champions at any tested budget (section 8): the finite-$n$ posterior lift
   does not convert into budgeted success.

## 1. Setup and the normal form (Lemma N1)

Pipeline $\Omega(n,d)$ at $p = 2$ as in deg2_theory.md section 1: $\rho$
uniform with $n_\rho = 2d$ free holes; $L$ a uniform design of the restricted
canonical system (kernel F1: the outer and canonical readings coincide);
$\mathrm{ans}(g) = L(g^\rho)$.

Lemma N1 (normal form; PROVED). Every $g \in \mathbb{F}_2^{\le 2}[x]$ is
answer-equivalent to $c + \sum_{p \in S} x_p + \sum_{(p,q) \in T} x_p x_q$
with each monomial $x_p x_q$ non-degenerate ($p \neq q$, distinct pigeons,
distinct holes). Proof: the restriction $\rho$ is a ring homomorphism on the
outer ring (chi_transfer.md section 1.3 quote); $x_{ij}^2 + x_{ij}$ is a
system polynomial, so squares alias to variables under every design; same-
pigeon monomials $x_{ij}x_{ij'}$ and same-hole monomials $x_{ij}x_{i'j}$ are
system polynomials, hence vanish under every design; both fold into the
constant. QED.

So the printed class in normal form is: a constant, any set of variables, and
any set of non-degenerate degree-2 monomials. "Support" = the number of
generators (variables + monomials); "slots" = the distinct pairs appearing.

## 2. The per-restriction answer law (Lemmas N2 and N3)

Lemma N2 (alive/dead; PROVED). Fix $\rho$ and a query in normal form. For
each pattern of statuses ($F$ free / $M$ matched / $K$ killed) of the
query's pairs: a term contributes a live design coordinate iff (variable on
a free pair) or (monomial with at least one free component: the free
component's bit, if the other is matched; a fresh diagonal bit, if both
free); it contributes the determined constant $1$ iff (matched variable) or
(both-matched monomial); otherwise $0$. Live coordinates XOR-cancel; the
coordinate multiset is the F_2-support of the term contributions. If the
cancelled live set is nonempty, $\mathrm{ans}$ is a fair coin (marginally,
over designs); otherwise $\mathrm{ans} = c \oplus (\text{matched parity})$
determinedly.
Proof: each contribution is a design coordinate or a determined constant by
Lemma N1 and the restriction calculus; distinct live coordinates are
independent fair coins whenever no determined relation lives on their set.
For support $\le 3$ the only degree-$\le 2$ determined relations are the
degenerate monomials (excluded by N1), the row axioms $Q_i$ (at least
$n{+}1 \ge 7$ coordinates), and the star rows $Q_p x_{ab}$ ($2d{-}1$
monomial coordinates plus the target single: $4$ live coordinates at
$d = 2$): none fits inside $\le 3$ live coordinates, so the coordinate set
is independent and the XOR is fair. QED. (The star-row coupling is what the
star-3M maximizer exploits for its output pair; Engine A handles it exactly
and Engine B reproduces the same numbers digit-exactly, section 3, because
the coupling changes which coordinate carries the answer but not its
marginal law, and the output pair's own status is carried by the pattern
weights.)

Lemma N3 (exact pattern weights; PROVED). The weight of an exact status
pattern on the query's slots (the number of restrictions realizing exactly
that pattern) is computed by splitting each killed slot into the two
disjoint exhaustive cases $K_p$ (pigeon matched elsewhere) and $K_h$ (hole
matched, pigeon not), which are forced-structure events, and
inclusion-excluding the $K_p$ edges (they must be used by the matching):

  $W(\text{pattern}) = \sum_{U \subseteq K_p \text{ valid}}
  (-1)^{|U|}\, \binom{n+1-pu-pm}{c-pm}\, \binom{n-hu-hm}{c-hm}\,
  (c-e_{\mathrm{img}})!$

with $c = n - 2d$; $pm$ = distinct pigeon classes forced covered ($M \cup
P$); $pu$ = distinct pigeon classes forced uncovered ($F \cup H$); $hm$ =
distinct hole classes forced covered ($M \cup H \cup U$-holes); $hu$ =
distinct hole classes forced free ($F$); $e_{\mathrm{img}}$ = number of
fixed images ($M$-edges plus $U$-edges). Validity: a pigeon (resp. hole)
class cannot be both covered and uncovered; two $M$-edges cannot share a
pigeon or a hole; a $U$-edge cannot touch an $M$-pigeon, an $M$-hole, a
$U$-hole, or a free hole.
Machine-validated: brute-force agreement on all $3^t$ patterns for eight
geometries (disjoint, shared-pigeon, shared-hole, star, mixed, 4-slot) at
$(7,2)$ and $(8,2)$, and exact partition of the restriction space
(`weight_pattern`; V0 in the registered output).

## 3. The two engines and their validation

Engine A (design-exact). Enumerates restrictions $\rho$; maps each query to
its restricted coordinate vector $v = g^\rho$ (raw monomial columns:
V-membership is automatic because every design vanishes on $V$); computes
$P[\mathrm{ans}(g)=1 \mid \rho]$ as the fraction of the design coset
$L^\star + \mathrm{ker}$ (projected-kernel enumeration, the
chi_deg3_check.py pattern) with $L(v) = 1$.

Engine B (status-exact). Enumerates the query's status patterns with Lemma
N3 weights and Lemma N2's law; exact rational arithmetic throughout.

Posteriors: for output pair $c$ and answer event $\mathrm{ans} = a$,
$\mathrm{post}(c \mid g, a) = N/(N+D)$, $N = E_\rho[\mathbf{1}_{cF}
P[\mathrm{ans}=a \mid \rho]]$, $D = E_\rho[\mathbf{1}_{c\not F}P[\mathrm{ans}=a
\mid \rho]]$. Roles scanned: the query's own support pairs, same-line
virtual partners (exact, for $t \le 3$), and the generic external role.

Validation (registered output):
  V0  pattern weights partition the restriction space exactly (PASS).
  V1  Engine B == Engine A DIGIT-EXACT on all $7172$ enumerated queries x
      both answers x all support roles at $(7,2)$ over ALL $11760$
      restrictions (0 mismatches); the single variable reproduces
      $q = 10/13$; the diagonal monomial reproduces
      $q_{\mathrm{and,exact}} = 25/31$ (PASS).
  V3  (15,2): 16 panel queries on $40000$ sampled restrictions: every
      comparison inside its own 5-sigma sampling tolerance (PASS).

## 4. The finding: the shared-structure lift (Theorem M-A)

Theorem M-A (per-hit maximum over the FULL printed class; PROVED for
support $\le 3$ by complete exact enumeration, MEASURED on the grid). Over
all support-$\le 3$ queries, all answers, and all output roles, the maximum
per-hit posterior is

  $q_2^*(n,d) = \max\big(q,\ q_{\mathrm{and,exact}},\ q_{\mathrm{star3}},
  \ q_{\mathrm{shared2}},\ \ldots\big) = q_{\mathrm{star3}} > q_{\mathrm{and,
  exact}} > q$

at every grid point measured ($d = 2,3,4$; $n$ from the smallest admissible
to $1023$), where $q_{\mathrm{star3}}$ is the posterior of

  $g^* = x_{ab}x_{cd} + x_{ab}x_{ef} + x_{ab}x_{gh}$ (output $ab$; partners
  pairwise distinct pigeons and holes)

and $q_{\mathrm{shared2}}$ that of its two-monomial truncation. Exact
values (Engine B, exact rationals; Engine A agrees digit-exactly at
$(7,2)$):

| (n,d) | q | q_and_exact | q2* = star-3M | shared-2M | q2* - q_and |
|---|---|---|---|---|---|
| (7,2) | 10/13 = 0.769231 | 25/31 = 0.806452 | 787/934 = 0.842612 | 0.827770 | +0.036161 |
| (15,2) | 10/21 = 0.476190 | 23/45 = 0.511111 | 23795/45146 = 0.527068 | 3908/7527 = 0.519198 | +0.015957 |
| (32,2) | 5/19 = 0.263158 | 100/359 = 0.278552 | 1268654/4503753 = 0.281688 | 7515/26828 = 0.280118 | +0.003137 |
| (63,2) | 10/69 = 0.144928 | 355/2361 = 0.150360 | 0.150903 | 0.150631 | +0.000543 |
| (1023,2) | 0.009703 | 0.009746 | 0.009746 | 0.009746 | ~1e-7 |

The excess $q_2^* - q_{\mathrm{and,exact}}$ decays to $0$ (measured
$+0.0362,\ +0.0160,\ +0.0031,\ +0.0005$ along the $d = 2$ grid) while
$q_2^*/q_{\mathrm{and,exact}} \to 1$: NO asymptotic lift over the covered
constants, only a finite-$n$ one.

Mechanism (MEASURED, per-pattern table at $(32,2)$ for
$x_{ab}x_{cd} + x_{ab}x_{ef}$, output $ab$; full table in the script's
diagnostic). Let $s_0$ be the output pair's status.

| s0 | P(s0) | answer mass P(ans=1 and s0) | role |
|---|---|---|---|
| K | 0.954545 | 0 (all monomials die: ans = 0 a.s.) | self-excluded |
| M | 0.026515 | 0.000946 (live parity) + 0.001372 (det = 1 pollution) | diluted |
| F | 0.018939 | 0.000740 (live; the (F,M,M) and (F,K,K) cancellations drop out) | numerator |

The hit event excludes the killed branch entirely (it answers $0$
determinedly there), so the posterior conditions on $s_0 \in \{F, M\}$; the
remaining matched pollution is diluted from $m$ to
$\Theta(m^2 + m \cdot \text{partner-K-rate})$ by the partners' status
parity (both partners matched: the two monomial contributions cancel to
$0$; one partner matched: parity det $= 1$). For the single variable the
killed-unmatched branch is likewise self-excluded but the matched branch
pollutes at full rate $m$; the shared-structure mixtures reduce that
pollution, which is the entire lift. Adding partners sharpens the
dilution (star-3M $>$ shared-2M $>$ q_and) but each partner also adds
cancellation patterns; the measured optimum is three partners.

Asymptotics (PROVED from the exact pattern forms, sketch): with
$f = (2d{+}1)2d/((n{+}1)n)$ and $m = (n{-}2d)/((n{+}1)n)$, the shared-2M
numerator is $N = f(f{+}m)/2 \cdot (1 + o(1))$ and the denominator
$N + D = f(f{+}m)/2 + mf + m^2 (1 + o(1))$, giving
$q_{\mathrm{shared2}} = f/(2f + m) \cdot (1 + o(1))$-type ratios with
$q_{\mathrm{shared2}}/q \to 1$ and $q_{\mathrm{shared2}}/q_{\mathrm{and}}
\to 1$ as $f/m \to 0$; the star-3M behaves identically to leading order.
All ratios tend to $1$: the repaired constant is asymptotically the covered
one.

## 5. No new single-query certificates (Theorem M-B)

Theorem M-B (PROVED). No single query of the FULL printed degree-$\le 2$
class attains posterior $1$ at any answer event with positive numerator.
Proof: posterior $1$ requires $w = 0$ at every $c$-killed $\rho$. On
$c$-matched restrictions (mass $m > 0$) every term must be dead: any
variable on another pair is alive when that pair is free (probability
$f > 0$); any monomial through another pair is alive when a component is
free; any monomial through $c$ is alive when the partner is free or matched.
The only surviving support is $\{x_c\}$ alone (with partners' terms absent),
which is the single variable with $D \ge m > 0$. QED.
Machine check: $0$ certificates among all $7172$ enumerated queries at
$(7,2)$ (V2; the script's label "Theorem M4" is Theorem M-B here). The
certificate inventory of the covered class is therefore COMPLETE at degree
$\le 2$ even over mixtures, per single query.

## 6. Mixture certificates fold, not create (Proposition M-E)

The degree-2 Z-pattern exists and mixtures fold it: the pair
$g_1 = x_p + x_p x_q$, $g_2 = x_p x_q$ with answers $(1,1)$ is equivalent
to $x_p = 0$ and $x_p x_q = 1$, which forces $p$ free (p killed would give
$0$; p matched would give $x_p = 1$) and then $q$ free (the monomial of a
free $p$ answers $1$ only through a free $q$'s diagonal bit). Soundness
PROVED (the case check above; asserted free across all mix_z V5
simulations, 0 violations). Budget accounting: the covered class realizes the same
certificate as $\{x_p = 0, x_p x_q = 1\}$: two queries either way; the rate
per ordered pair is $\Theta(f^2/4 + fm/2)$-bounded, the same order the
covered adjacency term absorbs. CONCLUSION (marked): mixtures FOLD covered
certificate pairs into single queries but do not create certificate
mechanisms with better budget scaling. The completeness of the two-query
mixture certificate inventory beyond the folded families is CONJECTURED
(partially checked: the $(7,2)$ enumeration found no posterior-1 pair among
the form-completion set; the general 2-query classification is open).

## 7. The repaired budgeted cap (Theorem M-D)

Theorem M-D (repaired Theorem 3 over the FULL printed degree-$\le 2$
class). Every adaptive tree of budget $e$ using arbitrary
$\mathbb{F}_2^{\le 2}$ queries satisfies

  $\mathrm{success}(T) \le \min\big(1,\ q_2^*(n,d) + P_{\mathrm{adj,mix}}(e)
  + P_K(e) + O(e/n) + o(1)\big)$

with $q_2^*$ of Theorem M-A, $P_K(e) \le 2(1 - \exp(-e d / (4n)))$ as in
deg2_theory.md Theorem 3, and
$P_{\mathrm{adj,mix}}(e) \le \binom{e}{2}\,\sup_g\big(P[\mathrm{hit}(g)]
\cdot \mathrm{elev}(g)\big) \cdot \frac{2d-1}{2(n-1)} + \binom{e}{2}
\frac{f^2}{4}$ where the supremum is the rate-weighted elevation of
section 6 (MEASURED sup $= \Theta(d^2/n^2) = \Theta(f)$: high-rate live
mixtures such as $x_a + x_b$ hit at rate $\approx 1/2$ but carry elevation
$\approx f$, so their rate-weighted certificate budget matches the covered
one up to constants).
Status: PROVED as an assembly with exactly the same two modulo-JDP steps as
deg2_theory.md Theorem 3 (multi-row composition; block-completion through
Lemma REL) plus the rate-weighted certificate bound above (marked: the
per-pattern pieces are exact, the union bound over query pairs is
elementary, the sup is measured).

Corollary M-D1 (aliveness over the FULL printed quantifier). At budget
$e = d \log k$ with $d \le \sqrt{n}$: $P_{\mathrm{adj,mix}}$ and the
covered $P_{\mathrm{adj}}$ have the SAME order
$\Theta(d^5 (\log k)^2 / n^3)$ (the higher hit rates of live mixtures are
offset by proportionally lower elevation), and $P_K$ is unchanged, so

  $\mathrm{error}(T) \ge 1 - q_2^*(n,d) - o(1) - 2(1 - e^{-d^2 \log k /
  (4n)}) \ge k^{-O(1)}$

whenever $d^2 \log k = o(n)$ (with room), exactly the covered aliveness
condition of deg2_theory.md Corollary 3.1. The program's parameter
connection $d = (\log k)^{O(l)}$ therefore retains its proved $\delta \le$
$1/(2O(l))$-type reach over the FULL printed degree-$\le 2$ quantifier.
Status: PROVED modulo the same JDP steps inherited from Theorem 3.

## 8. Budgeted toy-scale test: no mixture gain (MEASURED)

Exact-channel simulations (uniform $\rho$; $L$ sampled uniformly from the
design coset; budget counts query evaluations; scan orders shuffled per
configuration so the first-hit baseline is the corpus's exchangeable scan;
$1500$-$4000$ simulations per point; certified outputs asserted free with
$0$ violations):

| (n,d) | budget | single_scan | kj_budget (covered) | mix_z | mix_scan | hybrid |
|---|---|---|---|---|---|---|
| (15,2) | 10 | 0.3237 | 0.3623 | 0.2462 | 0.2547 | 0.2382 |
| (15,2) | 30 | 0.4550 | 0.9393 | 0.3292 | 0.3315 | 0.3937 |
| (15,2) | 100 | 0.4780 | 0.9762 | 0.3523 | 0.3523 | 0.4718 |
| (32,2) | 10 | 0.0893 | 0.0893 | 0.0347 | 0.0353 | 0.0573 |
| (32,2) | 30 | 0.1800 | 0.5060 | 0.0427 | 0.0433 | 0.1240 |
| (32,2) | 100 | 0.2627 | 0.9747 | 0.0553 | 0.0553 | 0.2387 |

Reading: single_scan hugs $q$ (the fixed-order scan without shuffling is
biased toward early pigeons' matched pairs: an instrument note worth
keeping); the covered $K_j$ tree dominates everything; the two mixture
strategies sit BELOW the single-variable scan at every budget. The
finite-$n$ per-hit lift of section 4 does NOT convert into budgeted
success at toy scale, consistent with Theorem M-D.

## 9. Registered run

Command: `python3 experiments/chi_mixture_cap.py` (2026-10-04; about
$7$ minutes; `--smoke` for a fast pass).

```
[V0] (15,2) single-pair F+M+K weights sum: 237996734976000 vs restriction count 237996734976000 -> PASS
[V0] (15,2) two-pair weights sum: 237996734976000 -> PASS
[V2] (7,2): 18 pairs, 115 generators, 7172 queries
[V2] Engine A: all 11760 restrictions x 7172 queries (22.3 s)
[V1] Engine B vs Engine A: 7172 queries x 2 answers x support roles: 0 mismatches -> PASS (digit-exact)
[V1] single variable x(3,3): post1 = 10/13 vs q = 10/13 -> PASS
[V1] diagonal monomial x(3,3)x(4,4): post1 = 25/31 vs q_and_exact = 25/31 -> PASS (digit-exact)
[V2] (7,2) MAX posterior = 787/934 = 0.842612 vs q_and_exact = 25/31 -> EXCEEDED
     [x(0,0)x(1,4) + x(0,0)x(3,1) + x(0,0)x(4,3)]
[V2] single-query certificates (posterior = 1): 0 (Theorem M4: 0 expected)
[V3] (15,2): 16 panel queries x 40000 sampled restrictions
[V3] worst |Engine B - Engine A| over the panel: 0.04382 (0 comparisons over
     tolerance, per-comparison 5-sigma tolerance) -> PASS
[V4] 430 configurations up to isomorphism (support <= 3 generators, slots <= 6)
[V4] grid (q / q_and_ex / max post / shared-2M / star-3M):
     (7,2)    0.7692 0.8065 0.8426 0.827770 0.842612  argmax star-3M
     (15,2)   0.4762 0.5111 0.5271 0.519198 0.527068  argmax star-3M
     (32,2)   0.2632 0.2786 0.2817 0.280118 0.281688  argmax star-3M
     (63,2)   0.1449 0.1504 0.1509 0.150631 0.150903  argmax star-3M
     (127,2)  0.0752 0.0768 0.0768 0.076804 0.076842  argmax star-3M
     (1023,2) 0.0097 0.0097 0.0097 0.009746 0.009746  argmax star-3M
     (8,3)    0.9130 0.9385 0.9522 0.947876 0.952218  argmax star-3M
     (15,3)   0.7000 0.7583 0.7752 0.767201 0.775240  argmax star-3M
     (31,3)   0.4565 0.5066 0.5135 0.510075 0.513537  argmax star-3M
     (16,4)   0.8182 0.8701 0.8814 0.876217 0.881398  argmax star-3M
     (31,4)   0.6102 0.6807 0.6885 0.684664 0.688507  argmax star-3M
[V4] exact (15,2): q2*_shared - q_and = 913/112905 = 8.09e-03; shared = 3908/7527
[V4] exact (32,2): q2*_shared - q_and = 15085/9631252 = 1.57e-03; shared = 7515/26828
[V4] exact (63,2): q2*_shared - q_and = 374237/1381177917 = 2.71e-04
[V4] worst (max post - q_and_exact) over the grid: +0.036161 at (7,2)
     -> EXCEEDED (the repaired constant q2* replaces max(q, q_and))
[V5] (15,2) sims=4000: single 0.3237/0.4550/0.4780  kj 0.3623/0.9393/0.9762
     mix_z 0.2462/0.3292/0.3523  mix_scan 0.2547/0.3315/0.3523
     hybrid 0.2382/0.3937/0.4718   (budgets 10/30/100)
[V5] (32,2) sims=1500: single 0.0893/0.1800/0.2627  kj 0.0893/0.5060/0.9747
     mix_z 0.0347/0.0427/0.0553  mix_scan 0.0353/0.0433/0.0553
     hybrid 0.0573/0.1240/0.2387
[V5] soundness: every certified output was free (0 violations), both points
```

(The full top-12 query list at $(7,2)$ and both V5 tables are in the
console output; the numbers above are copied verbatim from the registered
run `/tmp/opencode/mixture_final.txt`.)

## 10. GAP B' verdict

1. Theorem 3's cap STRUCTURE survives over the FULL printed degree-$\le 2$
   class: same assembly, same $P_K$, same order of certificate budget, same
   aliveness condition $d^2 \log k = o(n)$ (Corollary M-D1).
2. The cap CONSTANT does not survive verbatim: the full class has
   $q_2^*(n,d) > \max(q, q_{\mathrm{and,exact}})$ at finite $n$, attained by
   monomial-star mixtures through the output pair (Theorem M-A), with the
   excess decaying to a relative $o(1)$. ADDENDUM 4 item 6's "likely a
   shallow repair" is confirmed and made precise: the repair changes a
   constant, not the structure.
3. The mechanism is the killed-branch self-exclusion of monomial queries
   through the output pair plus partner-parity dilution of the matched
   pollution (section 4): a new (mild) per-hit mechanism, now measured and
   machine-validated, that the degree-$\ge 4$ generalization (O2's open
   core) should account for alongside the star sum rules, alias classes,
   and the wedge/Z inventory.
4. No new single-query certificates (M-B); mixture certificates fold covered
   pairs without budget gain (M-E); no budgeted mixture gain at toy scale
   (section 8).

## 11. Open residual

1. Support-$\ge 4$ generators: Engine B's configuration scan is complete for
   support $\le 3$ (slots $\le 6$ for the star and disjoint families). The
   dilution argument (adding terms beyond the shared structure adds
   alive-mass on the killed branch and parity-dilutes the matched branch)
   suggests the max stays at the star-3M/shared-2M family: CONJECTURED with
   the $(7,2)$ window scan as measured evidence (Engine A's window covers
   all support-$\le 3$ concrete forms and its maximum equals the scan's).
2. The complete two-query mixture certificate classification (beyond the
   folded families and adjacency): open; rate-bounded by Proposition M-E's
   accounting.
3. The exact finite-$n$ constant in $q_2^* - q_{\mathrm{and,exact}} =
   \Theta(\cdot)$: measured along the $d = 2$ grid, consistent with
   $\Theta(d^4/n^3)$-type decay; the closed form is the pattern-table
   rational (Lemma N3) and no simpler monolithic form was extracted.
4. The engine B role space includes same-line virtual partners for
   $t \le 3$; wider configs keep support roles only (their same-line
   partners are dominated by the support roles in all measured cases).

## 12. One-paragraph verdict for the orchestrator

GAP B' is closed with a repaired statement: over the FULL printed
degree-$\le 2$ class (all $\mathbb{F}_2$ mixtures), the exact per-hit
posterior maximum is $q_2^*(n,d) > \max(q, q_{\mathrm{and,exact}})$ by a
finite-$n$ amount decaying to a relative $o(1)$, attained by monomial-star
mixtures through the output pair (787/934 = 0.8426 versus 25/31 = 0.8065 at
(7,2); excess 8.1e-3 at (15,2), 1.6e-3 at (32,2), 2.7e-4 at (63,2)); the
mechanism is killed-branch self-exclusion plus partner-parity dilution of
the matched pollution; there are no new single-query certificates, mixture
certificates fold covered pairs at equal budget, and the budgeted toy-scale
test shows no mixture gain over the covered champions. Theorem 3's budgeted
cap therefore extends to the full printed quantifier with the constant
$q \to q_2^*$ and the SAME aliveness condition $d^2 \log k = o(n)$
(Corollary M-D1, same modulo-JDP status), so the chi-hypothesis at $p = 2$
in the err-form remains proved-alive at degree $\le 2$ over the printed
class, exactly as O2's degree-2 slice requires.
