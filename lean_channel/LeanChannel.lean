/-
LeanChannel.lean

Lean 4 (mathlib) formalization of what SURVIVES the 2026-10-03 major correction of the
P-vs-NP research corpus (two_phase_tree.md, proof_complexity.md, cert_floor.md):

  * the pair-status model (Free / Matched / Killed; 2d+1 free pigeons, 2d free holes),
  * the counting certificates (Lemma 3 of cert_floor.md): killed rows/columns of the
    answer table contain exactly one 1, and the sound certificates (a),(b),(c),
  * the pigeonhole rescue (Lemma 4 of cert_floor.md),
  * the F_2 linearity lemma (Lemma 1 of cert_floor.md): any degree-1 answer is an F_2
    function of the variable-answer table M, given an F_2-linear answer functional L
    with L(1) = 1,
  * the deterministic halves of the single-variable channel law
    (matched -> 1, killed-unmatched -> 0),
  * full-scan dominance (Corollary 2 of cert_floor.md): an explicitly constructed
    non-adaptive tree (one singleton query per pair, i.e. n(n+1) queries) whose output
    equals the adaptive tree's output for every answer table,
  * the F_2 linear-algebra fragment: the pivot/free-coordinate decomposition of an
    F_2-subspace of (Fin N -> F2) (the structural content of RREF existence) and the
    kernel-basis disjoint-support property on free coordinates,
  * the channel law's probabilistic half (free -> fair coin, independence), stated as
    PMF identities.

NOT formalized (retracted by the correction, on purpose): Theorem T of
two_phase_tree.md (the exact law 1 - 2^{-(2d+1)} was a simulator artifact) and its
optimality claim; Proposition D of proof_complexity.md (false as stated).

The exact floor Theorem F of cert_floor.md (err* = (1-2d/n)(2d+1)(2d)!/2^((2d+1)*2d))
is STATED below as a target theorem, marked `sorry` where the proof is not given.
-/

import Mathlib

open Finset Fintype

/-! ## 1. The pair-status model and the counting certificates -/

section PairModel

variable {n : ℕ}

abbrev Pigeon (n : ℕ) := Fin (n + 1)
abbrev Hole (n : ℕ) := Fin n
abbrev Pair (n : ℕ) := Pigeon n × Hole n

/-- The pigeons assigned a hole by the partial injection.  These are the killed
pigeons; the free pigeons are the complement (`2d+1` of them, see `freePigeons_card`). -/
def domMu {n : ℕ} (mu : Pigeon n → Option (Hole n)) : Finset (Pigeon n) :=
  univ.filter fun i => (mu i).isSome

/-- The holes taken by the partial injection; the free holes are the complement
(`2d` of them, see `freeHoles_card`). -/
def rngMu {n : ℕ} (mu : Pigeon n → Option (Hole n)) : Finset (Hole n) :=
  univ.filter fun j => ∃ i, mu i = some j

theorem mem_domMu {n : ℕ} {mu : Pigeon n → Option (Hole n)} {i : Pigeon n} :
    i ∈ domMu mu ↔ (mu i).isSome := by simp [domMu]

theorem mem_rngMu {n : ℕ} {mu : Pigeon n → Option (Hole n)} {j : Hole n} :
    j ∈ rngMu mu ↔ ∃ i, mu i = some j := by simp [rngMu]

theorem domMu_isSome {n : ℕ} {mu : Pigeon n → Option (Hole n)} {i : Pigeon n}
    (h : i ∈ domMu mu) : ∃ j, mu i = some j := by
  rw [mem_domMu, Option.isSome_iff_exists] at h
  exact h

/-- Status of a pair `(i, j)`:
  * `matched`: pigeon `i` is assigned to hole `j` (determined answer 1);
  * `free`:    both endpoints free (answer = fresh design bit);
  * `killed`:  not matched, and at least one endpoint is killed (determined answer 0). -/
inductive Status : Type where
  | free
  | matched
  | killed

def pstatus {n : ℕ} (mu : Pigeon n → Option (Hole n)) (p : Pair n) : Status :=
  if mu p.1 = some p.2 then Status.matched
  else if p.1 ∉ domMu mu ∧ p.2 ∉ rngMu mu then Status.free
  else Status.killed

theorem pstatus_matched {n : ℕ} {mu : Pigeon n → Option (Hole n)} {p : Pair n} :
    pstatus mu p = Status.matched ↔ mu p.1 = some p.2 := by
  by_cases h1 : mu p.1 = some p.2
  · simp [pstatus, h1]
  · by_cases h2 : p.1 ∉ domMu mu ∧ p.2 ∉ rngMu mu
    · simp [pstatus, h1, h2]
    · simp [pstatus, h1, h2]

theorem pstatus_free {n : ℕ} {mu : Pigeon n → Option (Hole n)} {p : Pair n} :
    pstatus mu p = Status.free ↔
      (mu p.1 ≠ some p.2 ∧ p.1 ∉ domMu mu ∧ p.2 ∉ rngMu mu) := by
  by_cases h1 : mu p.1 = some p.2
  · simp [pstatus, h1]
  · by_cases h2 : p.1 ∉ domMu mu ∧ p.2 ∉ rngMu mu
    · simp [pstatus, h1, h2]
    · simp [pstatus, h1, h2]

theorem pstatus_killed {n : ℕ} {mu : Pigeon n → Option (Hole n)} {p : Pair n} :
    pstatus mu p = Status.killed ↔
      (mu p.1 ≠ some p.2 ∧ (p.1 ∈ domMu mu ∨ p.2 ∈ rngMu mu)) := by
  by_cases h1 : mu p.1 = some p.2
  · simp [pstatus, h1]
  · by_cases h2 : p.1 ∉ domMu mu ∧ p.2 ∉ rngMu mu
    · simp [pstatus, h1, h2]
    · simp only [pstatus, if_neg h1, if_neg h2, true_iff]
      have hd : p.1 ∈ domMu mu ∨ p.2 ∈ rngMu mu := by
        by_contra hc
        push_neg at hc
        exact h2 ⟨hc.1, hc.2⟩
      exact ⟨h1, hd⟩

/-- The single-variable answer table, packaging the two DETERMINED values of the
channel law (this is what survives the correction and what the counting certificates
need).  The values on free pairs are the design bits; they are treated probabilistically
in Section 6 and are irrelevant for the counting lemmas. -/
structure AnswerTable {n : ℕ} (mu : Pigeon n → Option (Hole n)) where
  /-- the answer to the single-variable query `x_ij` -/
  val : Pair n → ZMod 2
  /-- channel law, determined value 1: killed-matched pairs answer 1 -/
  matched_one : ∀ p, mu p.1 = some p.2 → val p = 1
  /-- channel law, determined value 0: killed pigeon, pair not matched -/
  killedP_zero : ∀ p, p.1 ∈ domMu mu → mu p.1 ≠ some p.2 → val p = 0
  /-- channel law, determined value 0: free pigeon, killed hole -/
  killedH_zero : ∀ p, p.1 ∉ domMu mu → p.2 ∈ rngMu mu → val p = 0

/-- Row of the answer table at pigeon `i`: the holes whose entry is 1. -/
def rowM {n : ℕ} {mu : Pigeon n → Option (Hole n)} (T : AnswerTable mu) (i : Pigeon n) :
    Finset (Hole n) :=
  univ.filter fun j => T.val (i, j) = 1

/-- Column of the answer table at hole `j`: the pigeons whose entry is 1. -/
def colM {n : ℕ} {mu : Pigeon n → Option (Hole n)} (T : AnswerTable mu) (j : Hole n) :
    Finset (Pigeon n) :=
  univ.filter fun i => T.val (i, j) = 1

/-- **Lemma 3 of cert_floor.md, row half.**  In every configuration, a killed pigeon's
row contains exactly one one-entry, at its matched hole. -/
theorem killed_row_singleton {n : ℕ} {mu : Pigeon n → Option (Hole n)}
    (T : AnswerTable mu) {i : Pigeon n} {j0 : Hole n} (h : mu i = some j0) :
    rowM T i = {j0} := by
  ext j
  simp only [rowM, mem_filter, mem_univ, true_and, mem_singleton]
  constructor
  · intro hj
    by_contra hne
    have hdom : i ∈ domMu mu := by rw [mem_domMu]; rw [h]; simp
    have hne' : mu i ≠ some j := fun hc => hne (by rw [hc] at h; exact Option.some.inj h)
    rw [T.killedP_zero (i, j) hdom hne'] at hj
    exact absurd hj (by simp)
  · intro hj
    subst hj
    exact T.matched_one (i, j) h

/-- **Lemma 3 of cert_floor.md, column half.**  In every configuration, a killed hole's
column contains exactly one one-entry, at its matched pigeon. -/
theorem killed_col_singleton {n : ℕ} {mu : Pigeon n → Option (Hole n)}
    (T : AnswerTable mu) (hmu : ∀ i j a, mu i = some a → mu j = some a → i = j)
    {i0 : Pigeon n} {j : Hole n} (h : mu i0 = some j) :
    colM T j = {i0} := by
  ext i
  simp only [colM, mem_filter, mem_univ, true_and, mem_singleton]
  constructor
  · intro hi
    by_contra hne
    by_cases hmi : mu i = some j
    · exact hne (hmu i i0 j hmi h)
    · have h0 : T.val (i, j) = 0 := by
        by_cases hdom : i ∈ domMu mu
        · exact T.killedP_zero (i, j) hdom hmi
        · exact T.killedH_zero (i, j) hdom (by rw [mem_rngMu]; exact ⟨i0, h⟩)
      rw [h0] at hi
      exact absurd hi (by simp)
  · intro hi
    exact T.matched_one (i, j) (by rw [hi]; exact h)

/-- **Certificate (a) of Lemma 3.**  A row whose 1-entry set is not a singleton
certifies its pigeon free.  Sound against every configuration. -/
theorem cert_row_free {n : ℕ} {mu : Pigeon n → Option (Hole n)} (T : AnswerTable mu)
    {i : Pigeon n} (h : ∀ j : Hole n, rowM T i ≠ {j}) : i ∉ domMu mu := by
  intro hdom
  obtain ⟨j0, hj0⟩ := domMu_isSome hdom
  exact h j0 (killed_row_singleton T hj0)

/-- **Certificate (b) of Lemma 3.**  A column whose 1-entry set is not a singleton
certifies its hole free. -/
theorem cert_col_free {n : ℕ} {mu : Pigeon n → Option (Hole n)} (T : AnswerTable mu)
    (hmu : ∀ i j a, mu i = some a → mu j = some a → i = j) {j : Hole n}
    (h : ∀ i : Pigeon n, colM T j ≠ {i}) :
    j ∉ rngMu mu := by
  intro hrng
  obtain ⟨i0, hi0⟩ := mem_rngMu.mp hrng
  exact h i0 (killed_col_singleton T hmu hi0)

/-- **Certificate (c) of Lemma 3, row form.**  A one-entry in the row of a free pigeon
certifies its hole free. -/
theorem cert_c_row {n : ℕ} {mu : Pigeon n → Option (Hole n)} (T : AnswerTable mu)
    {i : Pigeon n} {j : Hole n} (h1 : i ∉ domMu mu) (h2 : T.val (i, j) = 1) :
    j ∉ rngMu mu := by
  intro hrng
  rw [T.killedH_zero (i, j) h1 hrng] at h2
  exact absurd h2 (by simp)

/-- **Certificate (c) of Lemma 3, column form.**  A one-entry in the column of a free
hole certifies its pigeon free. -/
theorem cert_c_col {n : ℕ} {mu : Pigeon n → Option (Hole n)} (T : AnswerTable mu)
    {i : Pigeon n} {j : Hole n} (h1 : j ∉ rngMu mu) (h2 : T.val (i, j) = 1) :
    i ∉ domMu mu := by
  intro hdom
  rcases domMu_isSome hdom with ⟨j', hj'⟩
  by_cases heq : j' = j
  · subst heq
    exact h1 (mem_rngMu.mpr ⟨i, hj'⟩)
  · have hne : mu i ≠ some j := by
      intro hc
      rw [hc] at hj'
      exact heq (Option.some.inj hj').symm
    rw [T.killedP_zero (i, j) hdom hne] at h2
    exact absurd h2 (by simp)

/-- **Lemma 4 of cert_floor.md (pigeonhole rescue).**  If every row of the answer
table shows exactly one 1, then some column shows at least two 1s; that column is then
certified free by (b), and every one-entry in it certifies its pigeon free by (c). -/
theorem pigeonhole_rescue {n : ℕ} {mu : Pigeon n → Option (Hole n)} (T : AnswerTable mu)
    (h : ∀ i : Pigeon n, ∃ j0 : Hole n, rowM T i = {j0}) :
    ∃ j : Hole n, 2 ≤ (colM T j).card := by
  by_contra hcon
  push_neg at hcon
  choose g hg using h
  have hv : ∀ i : Pigeon n, T.val (i, g i) = 1 := by
    intro i
    have hm : g i ∈ rowM T i := by rw [hg i]; simp
    simp only [rowM, mem_filter, mem_univ, true_and] at hm
    exact hm
  have hinj : Function.Injective g := by
    intro i1 i2 heq
    by_contra hne
    have hc : ({i1, i2} : Finset (Pigeon n)) ⊆ colM T (g i1) := by
      intro x hx
      simp only [mem_insert, mem_singleton] at hx
      rcases hx with hx | hx
      · rw [hx]
        simp only [colM, mem_filter, mem_univ, true_and]
        exact hv i1
      · rw [hx, heq]
        simp only [colM, mem_filter, mem_univ, true_and]
        exact hv i2
    have h2 : 2 ≤ (colM T (g i1)).card := by
      have hcc := card_le_card hc
      rw [card_insert_of_notMem (by simpa using hne), card_singleton] at hcc
      exact hcc
    have hlt := hcon (g i1)
    omega
  have hle := Fintype.card_le_of_injective g hinj
  simp only [Fintype.card_fin] at hle
  omega

end PairModel

/-! ## 2. The shape: 2d+1 free pigeons, 2d free holes -/

section Shape

/-- A configuration's restriction: a partial injection leaving exactly `n - 2d`
pigeons assigned, i.e. `2d+1` free pigeons and `2d` free holes. -/
structure Rho (n d : ℕ) where
  mu : Pigeon n → Option (Hole n)
  inj : ∀ i j a, mu i = some a → mu j = some a → i = j
  shape : (domMu mu).card = n - 2 * d

theorem card_rngMu_eq {n : ℕ} {mu : Pigeon n → Option (Hole n)}
    (hmu : ∀ i j a, mu i = some a → mu j = some a → i = j) :
    (domMu mu).card = (rngMu mu).card := by
  refine Finset.card_bij
    (fun i (_ : i ∈ domMu mu) => (mu i).get (mem_domMu.mp ‹i ∈ domMu mu›)) ?_ ?_ ?_
  · intro i hi
    exact mem_rngMu.mpr ⟨i, (Option.some_get (mem_domMu.mp hi)).symm⟩
  · intro i1 hi1 i2 hi2 hget
    have hs1 := mem_domMu.mp hi1
    have hs2 := mem_domMu.mp hi2
    have e1 : some ((mu i1).get hs1) = mu i1 := Option.some_get hs1
    have e2 : some ((mu i2).get hs2) = mu i2 := Option.some_get hs2
    exact hmu i1 i2 _ e1.symm (e2.symm.trans (congrArg some hget).symm)
  · intro j hj
    obtain ⟨p, hp⟩ := mem_rngMu.mp hj
    refine ⟨p, (mem_domMu (mu := mu)).mpr (by rw [hp]; exact Option.isSome_some), ?_⟩
    have hs : (mu p).isSome = true := by rw [hp]; exact Option.isSome_some
    have hchain : some ((mu p).get hs) = some j := by
      rw [Option.some_get hs]
      exact hp
    exact Option.some.inj hchain

/-- The number of free pigeons is exactly `2d+1`. -/
theorem freePigeons_card {n d : ℕ} (r : Rho n d) (hd : 2 * d ≤ n) :
    (univ \ domMu r.mu).card = 2 * d + 1 := by
  rw [Finset.card_sdiff, Finset.inter_univ, Finset.card_univ, Fintype.card_fin, r.shape]
  omega

/-- The number of free holes is exactly `2d`. -/
theorem freeHoles_card {n d : ℕ} (r : Rho n d) (hd : 2 * d ≤ n) :
    (univ \ rngMu r.mu).card = 2 * d := by
  rw [Finset.card_sdiff, Finset.inter_univ, Finset.card_univ, Fintype.card_fin, ← card_rngMu_eq r.inj, r.shape]
  omega

end Shape

/-! ## 3. The F_2 linearity lemma (Lemma 1 of cert_floor.md) -/

section Linearity

variable {n : ℕ}
variable {mu : Pigeon n → Option (Hole n)}

/-- An affine-linear (degree-1) query: `const + Σ_{p ∈ support} x_p`. -/
structure Form (n : ℕ) where
  const : ZMod 2
  support : Finset (Pair n)

/-- The restricted variable `x_p^rho`: a matched pair is set to the constant 1 (so a
linear `L` with `L(1) = 1` answers 1 on it), every other pair remains a variable. -/
def subst (p : Pair n) : Pair n → ZMod 2 :=
  if mu p.1 = some p.2 then 1 else Pi.single p 1

/-- The design: an F_2-linear answer functional with `L(1) = 1` vanishing on the
determined killed-unmatched coordinates.  These are exactly the proved properties of
the uniform random degree-d design that the channel law needs; the disjoint-support
structure of the underlying kernel is the pivot/free decomposition of Section 5. -/
structure Design (mu : Pigeon n → Option (Hole n)) where
  L : (Pair n → ZMod 2) →+ ZMod 2
  one_val : L 1 = 1
  killedH : ∀ p, p.1 ∉ domMu mu → p.2 ∈ rngMu mu → L (Pi.single p 1) = 0
  killedP : ∀ p, p.1 ∈ domMu mu → mu p.1 ≠ some p.2 → L (Pi.single p 1) = 0

/-- The restriction `f^rho` of a query. -/
def subForm (f : Form n) : Pair n → ZMod 2 :=
  (fun _ => f.const) + ∑ p ∈ f.support, subst (mu := mu) p

/-- The answer to the query: `L(f^rho)`. -/
def ansL (D : Design mu) (f : Form n) : ZMod 2 := D.L (subForm (mu := mu) f)

/-- The variable-answer table `M`: the answers to the single-variable queries. -/
def MofL (D : Design mu) (p : Pair n) : ZMod 2 := D.L (subst (mu := mu) p)

private theorem zmod2_cases (c : ZMod 2) : c = 0 ∨ c = 1 := by
  have h : c.val < 2 := ZMod.val_lt c
  match h2 : c.val, h with
  | 0, _ => left; exact (ZMod.val_eq_zero c).mp h2
  | 1, _ => right; rw [← ZMod.natCast_zmod_val c, h2, Nat.cast_one]
  | _ + 2, _ => omega

private theorem L_smul (D : Design mu) (c : ZMod 2) (v : Pair n → ZMod 2) :
    D.L (c • v) = c * D.L v := by
  rcases zmod2_cases c with rfl | rfl
  · simp
  · simp

private theorem L_const (D : Design mu) (c : ZMod 2) :
    D.L (fun _ : Pair n => c) = c := by
  have h : (fun _ : Pair n => c) = c • (1 : Pair n → ZMod 2) := by
    funext q; simp
  rw [h, L_smul, D.one_val, mul_one]

/-- **Lemma 1 of cert_floor.md (linearity of answers).**  The answer to any degree-1
query is the F_2 sum of its constant and the entries of the variable-answer table M
over the query's support. -/
theorem lemma1 (D : Design mu) (f : Form n) :
    ansL D f = f.const + ∑ p ∈ f.support, MofL D p := by
  simp only [ansL, subForm, MofL, map_add, map_sum, L_const]

/-- Channel law, determined value 1: killed-matched. -/
theorem MofL_matched (D : Design mu) {p : Pair n} (h : mu p.1 = some p.2) :
    MofL D p = 1 := by
  simp [MofL, subst, h, D.one_val]

/-- Channel law, determined value 0: killed pigeon, not matched. -/
theorem MofL_killedP (D : Design mu) {p : Pair n} (h1 : p.1 ∈ domMu mu)
    (h2 : mu p.1 ≠ some p.2) : MofL D p = 0 := by
  simp [MofL, subst, h2, D.killedP p h1 h2]

/-- Channel law, determined value 0: free pigeon, killed hole. -/
theorem MofL_killedH (D : Design mu) {p : Pair n} (h1 : p.1 ∉ domMu mu)
    (h2 : p.2 ∈ rngMu mu) : MofL D p = 0 := by
  have hne : mu p.1 ≠ some p.2 := by
    intro hc
    exact h1 (by rw [mem_domMu, hc]; simp)
  simp [MofL, subst, hne, D.killedH p h1 h2]

/-- Channel law, free half: the answer is the design bit `L(δ_p)` at the free
coordinate (uniform i.i.d. under the uniform design; see Section 6). -/
theorem MofL_free (D : Design mu) {p : Pair n} (h1 : p.1 ∉ domMu mu)
    (h2 : p.2 ∉ rngMu mu) : MofL D p = D.L (Pi.single p 1) := by
  have hne : mu p.1 ≠ some p.2 := by
    intro hc
    exact h1 (by rw [mem_domMu, hc]; simp)
  simp [MofL, subst, hne]

/-- The L-model produces a legitimate `AnswerTable`: the counting certificates of
Section 1 apply to it. -/
def answerTableOfL (D : Design mu) : AnswerTable mu where
  val := MofL D
  matched_one := fun p h => MofL_matched D h
  killedP_zero := fun p h1 h2 => MofL_killedP D h1 h2
  killedH_zero := fun p h1 h2 => MofL_killedH D h1 h2

end Linearity

/-! ## 4. Decision trees and full-scan dominance (Corollary 2 of cert_floor.md) -/

section Trees

variable {n : ℕ}

abbrev Query (n : ℕ) := Form n

/-- The answer to query `q` computed from a table `M` (Lemma 1). -/
def evalQ {n : ℕ} (q : Query n) (M : Pair n → ZMod 2) : ZMod 2 :=
  q.const + ∑ p ∈ q.support, M p

inductive DTree (n : ℕ) : Type where
  | leaf : Pair n → DTree n
  | node : Query n → DTree n → DTree n → DTree n

/-- Run a tree against an answer oracle for degree-1 queries. -/
def DTree.run {n : ℕ} : DTree n → (Query n → ZMod 2) → Pair n
  | .leaf ℓ, _ => ℓ
  | .node q f tr, answer =>
      if answer q = 1 then DTree.run tr answer else DTree.run f answer

/-- The queries made along the path followed by answer oracle `A`. -/
def DTree.pathQueries {n : ℕ} : DTree n → (Query n → ZMod 2) → List (Query n)
  | .leaf _, _ => []
  | .node q f tr, answer =>
      q :: (if answer q = 1 then DTree.pathQueries tr answer
        else DTree.pathQueries f answer)

/-- Non-adaptive: the query sequence is independent of the answers (as long as the
answers come from a table, which they do for every configuration by Lemma 1). -/
def DTree.Nonadaptive {n : ℕ} (t : DTree n) : Prop :=
  ∃ qs : List (Query n), ∀ M : Pair n → ZMod 2,
    t.pathQueries (fun q => evalQ q M) = qs

variable (mu : Pigeon n → Option (Hole n))

def ansQuery (D : Design mu) (q : Query n) : ZMod 2 := ansL D q

def runCfg (D : Design mu) (t : DTree n) : Pair n := t.run (ansQuery mu D)

theorem ansQuery_eq (D : Design mu) (q : Query n) :
    ansQuery mu D q = evalQ q (MofL D) := lemma1 D q

theorem runCfg_leaf (D : Design mu) (ℓ : Pair n) : runCfg mu D (DTree.leaf ℓ) = ℓ := rfl

theorem runCfg_node (D : Design mu) (q : Query n) (f tr : DTree n) :
    runCfg mu D (DTree.node q f tr) =
      if ansQuery mu D q = 1 then runCfg mu D tr else runCfg mu D f := by
  show DTree.run (DTree.node q f tr) (ansQuery mu D) = _
  rw [DTree.run]
  rfl

/-- A tree run against the channel is a tree run against the table M (Lemma 1). -/
theorem runCfg_eq (D : Design mu) (t : DTree n) :
    runCfg mu D t = t.run (fun q => evalQ q (MofL D)) := by
  induction t with
  | leaf ℓ => exact runCfg_leaf mu D ℓ
  | node q f tr ihf ihtr =>
    rw [runCfg_node, ihf, ihtr, DTree.run, ansQuery_eq mu D q]

def varQuery (n : ℕ) (p : Pair n) : Query n := ⟨0, {p}⟩

theorem evalQ_varQuery (M : Pair n → ZMod 2) (p : Pair n) :
    evalQ (varQuery n p) M = M p := by simp [evalQ, varQuery]

/-- One singleton query pins its variable's value in the running table. -/
def update1 (M : Pair n → ZMod 2) (p : Pair n) (b : ZMod 2) : Pair n → ZMod 2 :=
  fun p' => if p' = p then b else M p'

/-- The full-scan simulator: query every variable once, threading the table the
answers determine, then output `F` of the completed table.  (Noncomputable only
because `Finset.toList` is.) -/
noncomputable def scanAux (F : (Pair n → ZMod 2) → Pair n) :
    List (Pair n) → (Pair n → ZMod 2) → DTree n
  | [], M => .leaf (F M)
  | p :: ps, M =>
      .node (varQuery n p) (scanAux F ps (update1 M p 0))
        (scanAux F ps (update1 M p 1))

/-- **Corollary 2 of cert_floor.md, tree form.**  For every adaptive degree-1 tree `t`,
`scanSim t` is a NON-ADAPTIVE tree (one singleton query per pair, hence `n(n+1)`
queries) whose output equals `t`'s output for every answer table M, hence on every
configuration. -/
noncomputable def scanSim {n : ℕ} (t : DTree n) : DTree n :=
  scanAux (fun M => t.run (fun q => evalQ q M)) (univ : Finset (Pair n)).toList (fun _ => 0)

theorem scan_aux_run (F : (Pair n → ZMod 2) → Pair n) :
    ∀ (ps : List (Pair n)) (M : Pair n → ZMod 2) (A : Query n → ZMod 2),
      (∀ p' : Pair n, A (varQuery n p') = M p') →
      (scanAux F ps M).run A = F M := by
  intro ps
  induction ps with
  | nil => intro M A _; rfl
  | cons p ps ih =>
    intro M A hA
    have hp : A (varQuery n p) = M p := hA p
    by_cases hb : M p = 1
    · have h1 : M p = 1 := hb
      have hcond : A (varQuery n p) = 1 := by rw [hp, h1]
      have hupd : update1 M p 1 = M := by
        funext q
        by_cases hq : q = p
        · subst hq; simp [update1, hp, h1]
        · simp [update1, hq]
      simp only [scanAux, DTree.run, if_pos hcond, hupd, ih M A hA]
    · have h0 : M p = 0 := by
        rcases zmod2_cases (M p) with h | h
        · exact h
        · exact absurd h hb
      have hcond : ¬(A (varQuery n p) = 1) := by rw [hp]; exact hb
      have hupd : update1 M p 0 = M := by
        funext q
        by_cases hq : q = p
        · subst hq; simp [update1, hp, h0]
        · simp [update1, hq]
      simp only [scanAux, DTree.run, if_neg hcond, hupd, ih M A hA]

theorem scan_aux_run_gen (F : (Pair n → ZMod 2) → Pair n) :
    ∀ (ps : List (Pair n)) (M₀ M : Pair n → ZMod 2) (A : Query n → ZMod 2),
      (∀ p' : Pair n, A (varQuery n p') = M p') →
      (scanAux F ps M₀).run A = F (fun q => if q ∈ ps then M q else M₀ q) := by
  intro ps
  induction ps with
  | nil => intro M₀ M A _; rfl
  | cons p ps ih =>
    intro M₀ M A hA
    by_cases hcond : A (varQuery n p) = 1
    · have hMp : M p = 1 := by rw [← hA p, hcond]
      show DTree.run _ A = _
      simp only [scanAux, DTree.run, if_pos hcond]
      rw [ih (update1 M₀ p 1) M A hA]
      congr 1
      funext q
      by_cases hq : q ∈ ps
      · have h1 : q ∈ p :: ps := by simp [hq]
        simp [update1, hq, h1]
      · by_cases hqp : q = p
        · subst hqp
          have h2 : M q = 1 := hMp
          simp [update1, hq, h2]
        · have h3 : q ∉ p :: ps := by simp [hq, hqp]
          simp [update1, hq, hqp, h3]
    · have hMp : M p = 0 := by
        have h1 : ¬ (M p = 1) := fun hc => hcond (by rw [hA p]; exact hc)
        rcases zmod2_cases (M p) with h | h
        · exact h
        · exact absurd h h1
      show DTree.run _ A = _
      simp only [scanAux, DTree.run, if_neg hcond]
      rw [ih (update1 M₀ p 0) M A hA]
      congr 1
      funext q
      by_cases hq : q ∈ ps
      · have h1 : q ∈ p :: ps := by simp [hq]
        simp [update1, hq, h1]
      · by_cases hqp : q = p
        · subst hqp
          have h2 : M q = 0 := hMp
          simp [update1, hq, h2]
        · have h3 : q ∉ p :: ps := by simp [hq, hqp]
          simp [update1, hq, hqp, h3]

theorem scanSim_correct {n : ℕ} (t : DTree n) (M : Pair n → ZMod 2) :
    (scanSim t).run (fun q => evalQ q M) = t.run (fun q => evalQ q M) := by
  unfold scanSim
  have h := scan_aux_run_gen (fun M' => t.run (fun q => evalQ q M'))
      (univ : Finset (Pair n)).toList (fun _ => 0) M (fun q => evalQ q M)
      (fun p' => evalQ_varQuery M p')
  refine h.trans ?_
  congr 1
  funext q
  simp [evalQ]

theorem scan_aux_path (F : (Pair n → ZMod 2) → Pair n) :
    ∀ (ps : List (Pair n)) (M : Pair n → ZMod 2) (A : Query n → ZMod 2),
      (scanAux F ps M).pathQueries A = ps.map (varQuery n) := by
  intro ps
  induction ps with
  | nil => intro M A; rfl
  | cons p ps ih =>
    intro M A
    show DTree.pathQueries _ A = _
    simp only [scanAux, DTree.pathQueries]
    by_cases hcond : A (varQuery n p) = 1
    · rw [if_pos hcond, ih (update1 M p 1) A]; rfl
    · rw [if_neg hcond, ih (update1 M p 0) A]; rfl

theorem scanSim_nonadaptive {n : ℕ} (t : DTree n) :
    DTree.Nonadaptive (scanSim t) := by
  refine ⟨(univ : Finset (Pair n)).toList.map (varQuery n), fun M => ?_⟩
  unfold scanSim
  exact scan_aux_path _ _ _ (fun q => evalQ q M)

/-- The full scan queries every pair exactly once: `n(n+1)` queries. -/
theorem scanSim_queries {n : ℕ} (t : DTree n) :
    ((univ : Finset (Pair n)).toList.map (varQuery n)).length = (n + 1) * n := by
  simp [Fintype.card_prod, Fintype.card_fin]

/-- **Corollary 2 of cert_floor.md.** -/
theorem corollary_two {n : ℕ} (t : DTree n) :
    ∃ t' : DTree n, DTree.Nonadaptive t' ∧
      ∀ M : Pair n → ZMod 2, t'.run (fun q => evalQ q M) = t.run (fun q => evalQ q M) :=
  ⟨scanSim t, scanSim_nonadaptive t, fun M => scanSim_correct t M⟩

end Trees

/-! ## 5. The F_2 linear-algebra fragment: pivot/free decomposition and disjoint support -/

section LinearAlgebra

/-- **Pivot/free-coordinate decomposition (the structural content of RREF existence).**
Every subspace `K ≤ (Fin N → F2)` admits a set `F` of free coordinates such that the
restriction map is a bijection from `K` onto all assignments on `F`: every `w` is
realized by exactly one member of `K`.  Mathlib has no literal RREF at this time; this
theorem states the pivot/free decomposition that an RREF computation would provide.
(Existence proof not given in this pass; marked `sorry`.) -/
theorem exists_free_coords {N : ℕ} (K : Submodule (ZMod 2) (Fin N → ZMod 2)) :
    ∃ F : Finset (Fin N), ∀ w : {a : Fin N // a ∈ F} → ZMod 2,
      ∃! v ∈ K, ∀ a (ha : a ∈ F), v a = w ⟨a, ha⟩ := by
  sorry

/-- **Kernel-basis disjoint support on free coordinates.**  Given the free-coordinate
set `F` of the decomposition, for each `a ∈ F` there is a kernel vector whose support
inside `F` is exactly `{a}`.  This is the disjoint-support property of the design
kernel basis that the corpus's channel-law proof invokes.  (Proved: it needs only the
decomposition, not linearity.) -/
theorem kernel_basis_disjoint {N : ℕ} (K : Submodule (ZMod 2) (Fin N → ZMod 2))
    (F : Finset (Fin N))
    (hF : ∀ w : {a : Fin N // a ∈ F} → ZMod 2, ∃! v ∈ K, ∀ a (ha : a ∈ F), v a = w ⟨a, ha⟩)
    (a : Fin N) (ha : a ∈ F) :
    ∃ k ∈ K, k a = 1 ∧ ∀ b ∈ F, k b ≠ 0 → b = a := by
  obtain ⟨k, hk, -⟩ := hF (fun b : {a : Fin N // a ∈ F} => if b.1 = a then 1 else 0)
  obtain ⟨hkK, hkprop⟩ := hk
  refine ⟨k, hkK, ?_, ?_⟩
  · have hprop := hkprop a ha
    simpa using hprop
  · intro b hb hkb
    have hprop := hkprop b hb
    by_cases hba : b = a
    · exact hba
    · rw [if_neg hba] at hprop
      rw [hprop] at hkb
      exact absurd hkb (by simp)

end LinearAlgebra

/-! ## 6. The channel law's probabilistic half (fair coins on the free region) -/

section Coins

variable {n : ℕ}
variable (mu : Pigeon n → Option (Hole n))

/-- Free pairs: both endpoints free. -/
abbrev FreePairType : Type := {p : Pair n // p.1 ∉ domMu mu ∧ p.2 ∉ rngMu mu}

instance : Fintype (FreePairType mu) := inferInstance

/-- The answer table as a function of the free design bits: determined 1/0 off the
free region, the design bit on it. -/
def coinTable (k : FreePairType mu → Bool) (p : Pair n) : Bool :=
  if h : p.1 ∉ domMu mu ∧ p.2 ∉ rngMu mu then k ⟨p, h⟩
  else if mu p.1 = some p.2 then true else false

/-- The answer table with design bits uniform i.i.d.: the proved channel law's
probabilistic content, in the form the corpus's simulators implement. -/
noncomputable def coinPMF : PMF (Pair n → Bool) :=
  (PMF.uniformOfFintype (FreePairType mu → Bool)).map fun k p => coinTable mu k p

noncomputable def ansPMF (p : Pair n) : PMF Bool := (coinPMF mu).map fun t => t p

/-- Channel law for a single variable: matched -> determined 1. -/
theorem ansPMF_matched (p : Pair n) (h : mu p.1 = some p.2) :
    ansPMF mu p = pure true := sorry

/-- Channel law for a single variable: killed pigeon, not matched -> determined 0. -/
theorem ansPMF_killedP (p : Pair n) (h1 : p.1 ∈ domMu mu) (h2 : mu p.1 ≠ some p.2) :
    ansPMF mu p = pure false := sorry

/-- Channel law for a single variable: free pigeon, killed hole -> determined 0. -/
theorem ansPMF_killedH (p : Pair n) (h1 : p.1 ∉ domMu mu) (h2 : p.2 ∈ rngMu mu) :
    ansPMF mu p = pure false := sorry

/-- **Channel law, single variable, free -> fresh fair coin.** -/
theorem ansPMF_free (p : Pair n) (h1 : p.1 ∉ domMu mu) (h2 : p.2 ∉ rngMu mu) :
    ansPMF mu p = PMF.uniformOfFintype Bool := sorry

/-- **Channel law, independence (disjoint support at the probabilistic level).**
Distinct free pairs answer with independent coins. -/
theorem ansPMF_indep (p q : Pair n) (h1 : p.1 ∉ domMu mu) (h2 : p.2 ∉ rngMu mu)
    (h3 : q.1 ∉ domMu mu) (h4 : q.2 ∉ rngMu mu) (hpq : p ≠ q) :
    (coinPMF mu).map (fun t => (t p, t q)) = PMF.uniformOfFintype (Bool × Bool) := sorry

end Coins

/-! ## 7. The optimality chain: full-scan dominance and the exact floor (Theorem F) -/

section Floor

open scoped Classical ENNReal

variable {n d : ℕ}

instance : Finite (Rho n d) := by
  refine Finite.of_injective (fun r : Rho n d => r.mu) ?_
  intro a b h
  cases a with
  | mk mu₁ _ _ =>
  cases b with
  | mk mu₂ _ _ =>
  simp only at h
  subst h
  simp

noncomputable instance : Fintype (Rho n d) := Fintype.ofFinite _

/-- The configuration space: a shape-`(n,d)` partial injection together with i.i.d.
uniform design bits on its free pairs. -/
abbrev Config (n d : ℕ) : Type :=
  Σ _r : Rho n d, {p : Pair n // p.1 ∉ domMu _r.mu ∧ p.2 ∉ rngMu _r.mu} → Bool

noncomputable instance : Fintype (Config n d) := inferInstance

/-- The configuration PMF: `rho` uniform over the shape-`(n,d)` restrictions, design
bits uniform i.i.d.  (Defined for configurations in a nonempty `Rho n d`; for
`2 * d ≤ n` the space is nonempty.) -/
noncomputable def configPMF (n d : ℕ) [Nonempty (Rho n d)] : PMF (Config n d) :=
  (PMF.uniformOfFintype (Rho n d)).bind fun r =>
    (PMF.uniformOfFintype ({p : Pair n // p.1 ∉ domMu r.mu ∧ p.2 ∉ rngMu r.mu} → Bool)).map
      (fun k => Sigma.mk r k)

/-- The probability weight of a configuration. -/
noncomputable def weight (n d : ℕ) [Nonempty (Rho n d)] (c : Config n d) : ℝ :=
  ((configPMF n d) c : ℝ≥0∞).toReal

/-- The answer table of a configuration (via the channel model of Sections 1/3). -/
def tableOf (n d : ℕ) (c : Config n d) : Pair n → ZMod 2 :=
  fun p => if coinTable c.1.mu c.2 p then 1 else 0

def isFree (n d : ℕ) (c : Config n d) (p : Pair n) : Prop :=
  p.1 ∉ domMu c.1.mu ∧ p.2 ∉ rngMu c.1.mu

/-- The error of a degree-1 tree under the configuration ensemble: the probability
that its output label is not a free pair. -/
noncomputable def errOf (n d : ℕ) [Nonempty (Rho n d)] (t : DTree n) : ℝ :=
  ∑ c ∈ (univ : Finset (Config n d)),
    weight n d c * (if isFree n d c (t.run (fun q => evalQ q (tableOf n d c))) then 0 else 1)

/-- Full-scan dominance at the level of errors (from `corollary_two`). -/
theorem errOf_eq_of_run_eq (n d : ℕ) [Nonempty (Rho n d)] (t t' : DTree n)
    (h : ∀ M : Pair n → ZMod 2, t'.run (fun q => evalQ q M) = t.run (fun q => evalQ q M)) :
    errOf n d t' = errOf n d t := by
  unfold errOf
  exact Finset.sum_congr rfl fun c _ => by rw [h (tableOf n d c)]

/-- **Corollary 2 at the level of errors.** -/
theorem corollary_two_errOf (n d : ℕ) [Nonempty (Rho n d)] (t : DTree n) :
    ∃ t' : DTree n, DTree.Nonadaptive t' ∧ errOf n d t' = errOf n d t := by
  refine ⟨scanSim t, scanSim_nonadaptive t, errOf_eq_of_run_eq n d t (scanSim t) ?_⟩
  intro M
  exact scanSim_correct t M

noncomputable def probTable (n d : ℕ) [Nonempty (Rho n d)] (m : Pair n → ZMod 2) : ℝ :=
  ∑ c ∈ (univ : Finset (Config n d)).filter (fun c => tableOf n d c = m), weight n d c

noncomputable def posterior (n d : ℕ) [Nonempty (Rho n d)] (p : Pair n) (m : Pair n → ZMod 2) : ℝ :=
  if probTable n d m = 0 then 0 else
    (∑ c ∈ (univ : Finset (Config n d)).filter
        (fun c => tableOf n d c = m ∧ isFree n d c p), weight n d c) / probTable n d m

noncomputable def maxPosterior (n d : ℕ) (hn : 0 < n) [Nonempty (Rho n d)]
    (m : Pair n → ZMod 2) : ℝ :=
  ((univ : Finset (Pair n)).image fun p => posterior n d p m) |>.max'
    (by
      haveI : Nonempty (Pair n) := ⟨(0, ⟨0, hn⟩)⟩
      exact Finset.image_nonempty.mpr Finset.univ_nonempty)

/-- The Bayes error of the pair posterior given the full answer table:
`E_M[1 - max_p P(p free | M)]`. -/
noncomputable def bayesErr (n d : ℕ) (hn : 0 < n) [Nonempty (Rho n d)] : ℝ :=
  ∑ m ∈ (univ : Finset (Pair n → ZMod 2)),
    probTable n d m * (1 - maxPosterior n d hn m)

/-- **Theorem F of cert_floor.md.**  The exact optimal error over the whole adaptive
degree-1 family: `err* = (1 - 2d/n) · (2d+1) · (2d)! / 2^((2d+1)·2d) = 2^{-Theta(d^2)}`,
attained by the non-adaptive full-scan counting tree, with the hard class the
near-permutation class b of Lemma 5.  (Statement recorded as the target theorem; the
proof - Lemma 5's counting and the Bayes audit - is not formalized in this pass.) -/
noncomputable def errStar (n d : ℕ) : ℝ :=
  (1 - (2 * d : ℝ) / n) *
    ((2 * d + 1) * Nat.factorial (2 * d)) / (2 : ℝ) ^ ((2 * d + 1) * 2 * d)

theorem theorem_F (n d : ℕ) [Nonempty (Rho n d)] (hd : 2 * d ≤ n) (hn : 0 < n) :
    bayesErr n d hn = errStar n d := sorry

/-- Half of Theorem F: every adaptive degree-1 tree errs at least `errStar`. -/
theorem floor_lower_bound (n d : ℕ) [Nonempty (Rho n d)] (hd : 2 * d ≤ n) (hn : 0 < n)
    (t : DTree n) :
    errStar n d ≤ errOf n d t := sorry

/-- Other half: some non-adaptive tree (the full-scan counting tree) attains `errStar`
exactly.  The tree's construction and exact analysis are in cert_floor_check.py;
formalizing them is future work. -/
theorem counting_tree_attains (n d : ℕ) [Nonempty (Rho n d)] (hd : 2 * d ≤ n) (hn : 0 < n) :
    ∃ t : DTree n, DTree.Nonadaptive t ∧ errOf n d t = errStar n d := sorry

end Floor
