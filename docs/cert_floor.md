# The certification floor for degree-1 trees: the exact optimum is
# 2^{-Theta(d^2)}, so the 2^{-Theta(d)} conjecture and Theorem T's optimality
# are both false

Original result of this session (2026-10-03): statement, proof, exact
enumeration, Bayes audit, and Monte Carlo verification. Script:
`cert_floor_check.py` (runtime 31 s, registered output reproduced at the end).
No existing corpus file was edited.

## Scope and outcome

The task as given: prove that every adaptive tree using only degree-1 queries errs
with probability at least 2^{-Theta(d)}, making Theorem T
(success 1 - 2^{-(2d+1)}) optimal within the degree-1 family.

RESULT: the conjectured floor is false, and the task has a stronger, clean
answer. The optimal error over the ENTIRE adaptive degree-1 family (no query
budget, adaptivity allowed) is exactly

  err* = (1 - 2d/n) . (2d+1) . (2d)! / 2^((2d+1) . 2d)
       = 2^(-4d^2 + 2d log2(d) - O(d))           (Stirling)
       = 2^{-Theta(d^2)},

and it is attained by a NON-ADAPTIVE tree that queries every variable once and
applies counting certificates. At (32,2): err* = 1.0e-4, against the conjectured
floor 2^{-5} = 3.1e-2 and Theorem T's error 2^{-(2d+1)} = 3.1e-2. At (64,4):
err* = 6.7e-17 against 2^{-9} = 2.0e-3. The mechanism the corpus and the task
missed: a decision tree can COUNT the 1s in a row or column of answers, and
killed rows/columns have exactly one 1 because the matching is a function.

## Setup

Pipeline of arXiv:2609.35927 at p = 2, parameters (n,d): rho uniform over
partial injections leaving exactly 2d+1 free pigeons D and 2d free holes R
among n+1 pigeons / n holes; L a uniform random degree-d design of the
restricted system; the answer to a query g is L(g^rho). Proved channel law
(corpus, task statement): for a single variable x_ij the answer is a fresh
independent fair coin if (i,j) in D x R, deterministically 1 if (i,j) is
matched, deterministically 0 if killed-unmatched. L is F_2-linear with L(1) = 1
and the free-pair design bits are independent fair coins (disjoint-support
property). The answer table M is the (n+1) x n table M(i,j) = ans(x_ij); we
call M(i,j) = 1 a "one-entry". A configuration means a pair (Z, c) =
((D,R,mu), coins) of the pipeline; M is a function of the configuration.

Fallback convention for all trees below: on an exhausted search output the
fixed pair (0,0), free with probability f = (2d+1) . 2d / ((n+1) n). Under the
canonical Z used for exact enumeration (killed pigeons i -> hole i for
i < n-2d), (0,0) is matched, so "strict" exact values carry no fallback luck.

## Lemma 1 (linearity of answers) - PROVED

For any affine-linear query g = a + sum_{p in S} x_p (a in F_2, S any set of
pairs, the degree-1 query class), ans(g) = a + XOR_{p in S} ans(x_p).

Proof. ans(g) = L(g^rho) = L(a . 1 + sum_p x_p^rho) = a . L(1) +
sum_p L(x_p^rho) = a + sum_p ans(x_p) over F_2, using linearity of L and
L(1) = 1. QED.

Corollary 2 (full-scan dominance) - PROVED. For every adaptive degree-1 tree T
there is a NON-ADAPTIVE tree T' that queries all n(n+1) single variables and
then outputs, with the same success probability as T on every configuration.

Proof. By Lemma 1 the answer to any query is an F_2 function of M. By induction
on the query index, T's t-th query and its answer are functions of M for every
t, so T's output label is a function of M. T' computes M by a fixed full scan,
then replays T's decision procedure, answering each simulated query by
Lemma 1, and outputs T's final label. QED.

Consequence: the optimal error over the whole adaptive degree-1 family equals
the Bayes error of the pair posterior given M,

  err* = E_M[ 1 - max_p P(p free | M) ],

and randomized trees do not beat the deterministic optimum (convexity).

## Lemma 3 (counting certificates) - PROVED

In every configuration, every killed pigeon's row of M contains exactly one
one-entry (at its matched hole) and every killed hole's column contains exactly
one one-entry (at its matched pigeon). Hence, soundly against every
configuration consistent with the transcript:

  (a) a row containing any number of 1s other than exactly one certifies its
      pigeon free;
  (b) a column containing any number of 1s other than exactly one certifies its
      hole free;
  (c) a one-entry in the row of a certified-free pigeon certifies its hole
      free, and a one-entry in the column of a certified-free hole certifies
      its pigeon free.

Proof. Killed pigeon i: x_{i,rho(i)} answers 1 (matched); every other pair
(i,j') is killed-unmatched and answers 0; there is no free hole in the row
because i is not in D. Symmetrically for columns. Soundness of (a): if the
pigeon were killed its row would show exactly one 1. Soundness of (c): with the
pigeon certified free, a one-entry (i,j) cannot be matched, and killed j would
make (i,j) killed-unmatched (answer 0). QED.

The corpus's trees aggregate answers by XOR (Q_i = 1 + row XOR). The
certificates above need the COUNT, which a decision tree may compute but no
single parity query can express. This is the whole gap.

## Lemma 4 (pigeonhole rescue) - PROVED

If every row of M shows exactly one 1, then some column shows at least two
1s. Proof: n+1 rows and n columns. In that event the column is certified free
by Lemma 3(b), a certified-free column contains no matched pair, so every
one-entry in it certifies its pigeon free by Lemma 3(c), and the tree outputs
a CERTIFIED free pair (error 0 on this event). QED.

## Lemma 5 (the hard class b) - PROVED

Define class b = { every column of M shows exactly one 1 and every row shows
at most one 1 }. Then:

  (i) P[class b] = (2d+1) . (2d)! / 2^((2d+1) . 2d);
  (ii) on class b the free-region coin matrix is a permutation matrix on 2d of
       the 2d+1 free pigeons plus one all-zero row, and every one-entry of M
       lies in the near-permutation formed by the killed matching and that
       partial permutation;
  (iii) the configurations consistent with class-b M are exactly the
       C(n, n-2d) choices of n-2d one-entries as the matched pairs; each hole
       is free in a fraction exactly 2d/n of them, the all-zero row's pigeon is
       free in all of them, and NO pair has posterior above 2d/n;
  (iv) the Bayes error on class b is exactly 1 - 2d/n.

Proof. (i) Killed rows and columns show exactly one 1 automatically, so the
condition lives on the (2d+1) x 2d free-region coin matrix: each of the 2d
columns has exactly one 1, and the rows sum to 2d with each row at most one 1,
forcing exactly one all-zero row and a bijection elsewhere: (2d+1) choices
times (2d)! permutation matrices. (ii) immediate. (iii) a consistent
configuration is any choice of n-2d one-entries as mu' with killed sets their
endpoints: disjoint rows and columns hold automatically (each column has one
one-entry, rows at most one), every unchosen one-entry has both endpoints
free, and the coins are forced; conversely every configuration generating this
M arises so. Each hole's column edge is chosen in C(n-1, n-2d-1) of the
C(n, n-2d) twins, so P[hole free] = 1 - C(n-1,n-2d-1)/C(n,n-2d) = 2d/n; the
all-zero row cannot be matched, so its pigeon has posterior 1; every
matched-candidate pigeon has posterior 1 - 2d/n; and hence every pair has
joint posterior at most 2d/n (pairs with the all-zero row: exactly 2d/n; all
other pairs: bounded by the hole's 2d/n). (iv) immediate. QED.

## Theorem F (exact certification floor) - PROVED

Every adaptive degree-1 tree for the Omega(n,d) pipeline at p = 2 (no query
budget) has error probability exactly

  err* = (1 - 2d/n) . (2d+1) . (2d)! / 2^((2d+1) . 2d)
       = 2^{-Theta(d^2)},

and the following NON-ADAPTIVE tree attains it: query all n(n+1) variables in
fixed order; compute row and column counts; then
  (1) if some row and some column both have count != 1, output (that row's
      pigeon, that column's hole);
  (2) else if every row has count exactly 1, output the first one-entry of the
      first column with count >= 2;
  (3) else if every column has count exactly 1 and some certified row has
      count >= 2, output that pigeon with its first 1-column;
  (4) else (class b) output (the count-0 row's pigeon, any hole).

Proof. The four cases exhaust all M. Cases 1-3 output pairs with posterior 1
by Lemma 3 and Lemma 4 (best possible). Case 4 is class b, where by Lemma 5
the posterior of every pair is at most 2d/n and the tree attains it. By
Corollary 2 no tree exceeds the Bayes value on any M. QED.

Numeric checks. Exact enumeration over all coin matrices (canonical Z) gives
strict success 0.906250 at (4,1) = 1 - 6/64 and 0.9998856 at (5,2) =
1 - 120/2^20, matching P[class b] = (2d+1)(2d)!/2^((2d+1)2d) digit for digit.
Monte Carlo at (32,2): success 1.0000 in 2000 runs (expected failures 0.2 at
err* = 1.0e-4); at (64,4): 1.0000 in 800 runs (err* = 6.7e-17).

## Bayes audit (per-class optimality, ground truth for Theorem F)

Theorem F's proof rests on two computational facts that the script checks
directly against the FULL configuration space:

  (a) EXHAUSTIVE at (4,1): all 120 x 64 = 7680 configurations enumerated and
      grouped into 6120 answer-table classes. On every class the counting
      tree's output pair achieves exactly the maximum pair posterior
      (max |tree - best| = 0), and the pooled Bayes error
      E_M[1 - max posterior] = 0.046875 equals floor_exact(4,1) exactly.
  (b) SAMPLED at (5,2): 200000 configurations, 199346 distinct classes. Seven
      multi-config classes show a nonzero tree-vs-empirical-best gap; every
      one of them is a class-b table (all columns exactly one 1, every row at
      most one 1), where Lemma 5(iii) makes all pair posteriors flat at 2d/n
      and small samples fluctuate. A gap on any other table would have
      refuted Theorem F; none occurred.

## Theorem R (rows+columns parity tree, O(n) queries) - PROVED

Adding the corpus's own Q_i row-XOR queries and their column duals
K_j = 1 + column XOR already beats Theorem T at equal O(n) query cost. Tree
rc_parity: scan all Q_i and K_j (2n+1 queries); certified sets I (rows with
answer 1: free pigeons) and J (columns with answer 1: free holes); if both
nonempty output (min I, min J); if I is empty, the global parity identity
(sum of row XORs = sum of column XORs = XOR of all free coins) forces some
column certified, scan those columns for a one-entry and output it; symmetric
if J is empty. Its error is exactly

  err_R = [ sum_{b odd} C(2d,b) 2^(2d(2d-b-1))
          + sum_{a odd} C(2d+1,a) 2^((2d-a)(2d-1)) ] / 2^((2d+1) . 2d)
        = (6d+2) 2^{-6d} (1 + o(1)),

versus Theorem T's 2^{-(2d+1)}: an exponential gap of 2^{4d}/poly(d). The
purely non-adaptive variant (output (min I, min J) only when both sets are
nonempty, fallback otherwise) has error 2^{-(2d+1)} + 2^{-2d}. Exact
enumeration: rc_parity strict success 0.9965019 at (5,2) = 1 - 3668/2^20,
matching the formula sum (F1: 1028, F2: 2640). Measured 0.9955 at (32,2),
0.9960 at (64,2), 1.0000 at (64,4). QED (case analysis as in the script).

## Correction to Theorem T's record (channel-law audit)

The corpus's Theorem T states error exactly 2^{-(2d+1)} with "phase 2 never
fails given certification". Under the corpus's own stated query
Q_i = 1 + sum_j x_ij, a free pigeon answers 1 iff its row XOR is 0 (the corpus
text itself says "Q_i^rho = 1 + XOR of the 2d free-row design bits"), so the
certified pigeon's row has EVEN parity, and the phase-2 row scan fails when
that row is all-zero, with conditional probability 2^{1-2d}. The simulation
`chi_two_phase.py` (line 50) and `chi_two_phase_retry.py` (line 41) instead
certify when the row XOR equals 1, which is not the answer law of any degree-1
query (the no-constant row sum answers 1 on every killed pigeon). Under the
literal law:

  plain two-phase error = 2^{-(2d+1)} + (1 - 2^{-(2d+1)}) . 2^{1-2d}
                        = 5 . 2^{-(2d+1)} (1 + o(1)),
  retry error           = ((1 + 2^{1-2d})/2)^{2d+1} = 2^{-(2d+1)} (1 + o(1)).

Measured (2000/1500/800 sims): literal 0.8500 at (32,2) (pred 0.8505), retry
0.9430 (pred 0.9448); the published-law tree measures 0.9695, reproducing the
corpus's 0.97. Exact enumeration at (5,2): literal strict 0.8476562 =
(31/32)(7/8), retry strict 0.9436865 = 1 - (9/16)^5, both digit-exact. So
Theorem T's claimed VALUE is recovered asymptotically by the retry variant, the
plain tree's constant is 5x larger, and the proof's "phase 2 never fails" step
is a gap under the stated channel law. Independently of this correction,
Theorem T is not optimal: Theorem R and Theorem F both dominate it.

## Effect on the corpus's recorded claims

1. two_phase_tree.md implication 1 ("the two-phase structure is plausibly
   optimal within certification-style strategies") and the task's floor
   conjecture: FALSE. The exact optimum is Theorem F.
2. proof_complexity.md Proposition D (non-adaptive cap, success <= (s+1) f +
   o(1) for arbitrary queries): FALSE as stated. rc_nonadaptive is
   non-adaptive with success 1 - 3 . 2^{-(2d+1)} at s = 2n+1 queries, e.g.
   0.9067 exact at (64,2) versus the Prop D bound 130 . f = 0.625. Prop C
   (single-variable) and Theorem B (adaptive single-variable) are untouched:
   they bind only when s = O(poly) with f(1+s/2) < 1, and the counting tree's
   s = n(n+1) makes those bounds vacuous.
3. Open Problem O1 (adaptive degree-2 detection) and the chi-hypothesis of
   Theorem 6.1: the UNBOUNDED-quantifier form at p = 2 is settled by Theorem F
   (degree 1 already reaches the Bayes optimum 2^{-Theta(d^2)}), but with the
   budget that Theorem 6.1 actually quantifies over, (d, d log k)-trees, the
   attack is inert: the expected number of answer-1s seen by e single queries
   is ~ e/n, so row/column count certificates (needing two 1s in one line)
   do not appear until e ~ n, far above d log k. Within budget Theorem B's cap
   governs and the chi-hypothesis survives. Budget remark: Theorem T's own
   witness costs ~2n queries and therefore exceeds the budget d log k
   whenever d < 2 n^{1-delta} (at k = 2^{n^delta}); the corpus's unbounded
   quantifiers and its budgeted theorem should be reconciled.
4. chi-transfer (conditional): for the counting tree, chi(P, rho) = 1 iff the
   label is not free AND 1 is not in Span(V^rho union A). Its queried forms
   span all single variables, whose linear span contains only zero-constant
   forms; so the chi-condition holds whenever no degree-<=d consequence in
   V^rho has constant term 1 (a reading of Def 4.3 to verify against the
   paper; the corpus's design existence L(1) = 1, L|V = 0 shows only
   1 not in V). Under that reading the floor theorem transfers to the
   chi-task verbatim.

## What is proved vs open

PROVED: Lemma 1, Corollary 2, Lemma 3, Lemma 4, Lemma 5, Theorem F (exact
optimal error and achiever), Theorem R (exact rc_parity error), the two-phase
correction, the channel audit. All closed forms verified digit-exactly by full
enumeration of the coin space at (4,1) (2^6 matrices) and (5,2) (2^20
matrices); per-class Bayes-optimality verified exhaustively at (4,1) (all 7680
configurations) and by sampling at (5,2); Monte Carlo at (32,2), (64,2),
(64,4).

OPEN: (a) the budgeted floor: the optimal error of e-query degree-1 trees as a
function of e; in particular whether any e = d log k tree beats Theorem B's
cap, which is what Theorem 6.1's hypothesis needs at p = 2; (b) the exact Bayes
program at degree 2: Lemma 1's reduction dies there (a monomial answer is not
an XOR of single answers), so O1's content survives at degree >= 2; (c) whether
the corpus's Definition 3.1 quantifies over budgeted trees (reading to verify
against arXiv:2609.35927); if unbounded, Omega(n,d) at p = 2 is refuted as a
pseudo-solution by Theorem F for every k with k^{-O(1)} < err*, i.e.
log k > 4d^2 - O(d log d).

## Registered run

python3 cert_floor_check.py  (seeds 271828 / 141421 / +7 / 7777; 31 s total)

[BAYES] (4,1) exhaustive: 7680 configs, 6120 M-classes
  counting tree vs Bayes on every class: max |tree - best pair| = 0 configs
  E_M[1 - max posterior] = 0.046875 vs floor_exact = 0.046875 -> MATCH
[BAYES] (5,2) sampled (200000 configs): 199346 distinct M-classes
  7 gapped class(es); all class-b: True (gaps [-1 x 7])

[MC] n=32 d=2 sims=2000
  thmT_literal        0.8500 (pred 0.8505)   bench 0.9688
  thmT_literal_retry  0.9430 (pred 0.9448)
  rc_parity           0.9955 (pred 0.9966)   beats bench YES
  rc_nonadaptive      0.8995 (pred 0.9080)
  scan_all_counting   1.0000 (floor 0.9998999) beats bench YES
  scan_all_first1     0.1410
  thmT_published      0.9695 (pred 0.9693)   [flipped law, audit only]
[MC] n=64 d=2 sims=1500
  thmT_literal 0.8380 (0.8484); retry 0.9327 (0.9440); rc_parity 0.9960
  (0.9965) YES; counting 1.0000 (floor 0.9998927) YES; published 0.9667
[MC] n=64 d=4 sims=800
  thmT_literal 0.9888 (0.9904); retry 0.9988 (0.9979); rc_parity 1.0000
  (1.0000) YES; counting 1.0000 (floor 1 - 6.7e-17) YES; published 1.0000
[EXACT] (4,1), 64 matrices, strict success:
  thmT_literal 0.437500; retry 0.578125; rc_parity 0.875000;
  rc_nonadaptive 0.625000; scan_all_counting 0.906250 (= 1 - 6/64)
[EXACT] (5,2), 2^20 matrices, strict success:
  thmT_literal 0.8476562 (= (31/32)(7/8)); retry 0.9436865 (= 1-(9/16)^5);
  rc_parity 0.9965019 (= 1 - 3668/2^20); rc_nonadaptive 0.9062500 (= 1-3/32);
  scan_all_counting 0.9998856 (= 1 - 120/2^20); all closed forms digit-exact.
