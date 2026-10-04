/-!
# CoreChannel.lean — core-Lean-only formalization of the two most valuable
surviving channel results

No mathlib, no batteries: only Lean 4 core (Init).  Everything is plain
`Bool`/`Nat`/`List`; pigeon and hole indices are `Nat`s with explicit bounds
(`WellFormed` plays the role that `mu : Fin (n+1) → Option (Fin n)` plays in
the mathlib file `LeanChannel.lean`).

Formalized here (survivors of the 2026-10-03 correction of the corpus; see
FEASIBILITY.md):

(a) The channel-law answer function on the pair-status model
    (`pairStatus`, `answer`: matched pairs answer `true`, killed pairs answer
    `false`, open pairs get whatever the channel returned), together with the
    counting lemma (Lemma 3 of cert_floor.md, row half):
    every killed pigeon's answer row contains exactly one `true`.
(b) Soundness of the counting certificate: a pigeon whose row's `true`-count
    differs from `1` is free.

Both theorems are fully proved; the file compiles with the bare Lean 4 core
in seconds:

    lean CoreChannel.lean
-/

namespace CoreChannel

/-! ## The pair-status model -/

/-- Status of a `(pigeon, hole)` pair:

* `matched`: the pair is realized by the partial injection;
* `killed`:  the pigeon holds a *different* hole, so this pair is ruled out;
* `open_`:   the pigeon holds no hole at all, so the pair is undecided and the
  channel answers it by its coin (the answer is not determined). -/
inductive PairStatus where
  | matched | killed | open_

/-- A configuration: `mu i = some j` means pigeon `i` was assigned hole `j`,
`mu i = none` means pigeon `i` is free.  (The `Option` already encodes "each
pigeon holds at most one hole"; the injection's other half is not needed for
the two results below.) -/
def Mu := Nat → Option Nat

/-- A configuration is well formed for a table with `m` columns (holes
`0, …, m-1`) when every assigned hole is one of the columns. -/
def WellFormed (mu : Mu) (m : Nat) : Prop := ∀ i j, mu i = some j → j < m

/-- The pair status induced by a configuration. -/
def pairStatus (mu : Mu) (i j : Nat) : PairStatus :=
  match mu i with
  | none => PairStatus.open_
  | some j' => if j = j' then PairStatus.matched else PairStatus.killed

/-- The channel-law answer function on the pair-status model: a matched pair
answers `1` (`true`), a killed pair answers `0` (`false`); an open pair's
answer is whatever the channel returned, carried by `g : Nat → Nat → Bool`.
Only the determined entries are used below; the coin entries are opaque. -/
def answer (mu : Mu) (g : Nat → Nat → Bool) (i j : Nat) : Bool :=
  match pairStatus mu i j with
  | PairStatus.matched => true
  | PairStatus.killed => false
  | PairStatus.open_ => g i j

/-- A pigeon's answer row: its answer for every column `j < m`. -/
def row (mu : Mu) (g : Nat → Nat → Bool) (m i : Nat) : List Bool :=
  (List.range m).map (answer mu g i)

/-- A pigeon is killed when it holds some hole. -/
def Killed (mu : Mu) (i : Nat) : Prop := ∃ j, mu i = some j

/-- A pigeon is free when it holds no hole. -/
def Free (mu : Mu) (i : Nat) : Prop := mu i = none

/-! ## The channel law, deterministic half -/

/-- Channel law, matched case: a realized pair answers `1`. -/
theorem answer_matched (mu : Mu) (g : Nat → Nat → Bool) (i j : Nat)
    (h : pairStatus mu i j = PairStatus.matched) : answer mu g i j = true := by
  simp [answer, h]

/-- Channel law, killed case: a ruled-out pair answers `0`. -/
theorem answer_killed (mu : Mu) (g : Nat → Nat → Bool) (i j : Nat)
    (h : pairStatus mu i j = PairStatus.killed) : answer mu g i j = false := by
  simp [answer, h]

/-- For a killed pigeon (holding hole `j₀`) every entry of its row is
determined: `1` at column `j₀`, `0` everywhere else — the coin never enters a
killed pigeon's row. -/
theorem answer_of_killed (mu : Mu) (g : Nat → Nat → Bool) (i j j₀ : Nat)
    (hmu : mu i = some j₀) : answer mu g i j = decide (j = j₀) := by
  unfold answer pairStatus
  rw [hmu]
  by_cases h : j = j₀ <;> simp [h]

/-! ## Counting infrastructure (self-contained, no mathlib) -/

/-- Number of occurrences of `j` in a `Nat` list. -/
def countOcc (j : Nat) : List Nat → Nat
  | [] => 0
  | x :: l => (if x = j then 1 else 0) + countOcc j l

/-- Number of `true` entries of a `Bool` list. -/
def countTrue : List Bool → Nat
  | [] => 0
  | b :: l => (if b then 1 else 0) + countTrue l

theorem countOcc_append (j : Nat) :
    ∀ l₁ l₂ : List Nat, countOcc j (l₁ ++ l₂) = countOcc j l₁ + countOcc j l₂ := by
  intro l₁
  induction l₁ with
  | nil => intro l₂; simp [countOcc]
  | cons x l ih =>
    intro l₂
    by_cases h : x = j <;> simp [h, countOcc, ih] <;> omega

theorem countOcc_range_ge (j m : Nat) (h : m ≤ j) :
    countOcc j (List.range m) = 0 := by
  induction m with
  | zero => rfl
  | succ m ih =>
    rw [List.range_succ, countOcc_append, ih (by omega)]
    have hne : m ≠ j := by omega
    simp [countOcc, hne]

/-- A number `j` occurs in `List.range m` exactly when `j < m`, and then
exactly once. -/
theorem countOcc_range_of_lt (j m : Nat) (hj : j < m) :
    countOcc j (List.range m) = 1 := by
  induction m generalizing j with
  | zero => exact absurd hj (Nat.not_lt_zero j)
  | succ m ih =>
    rw [List.range_succ, countOcc_append]
    by_cases h1 : j < m
    · have h2 : m ≠ j := by omega
      rw [ih j h1]
      simp [countOcc, h2]
    · have hjeq : j = m := by omega
      subst hjeq
      rw [countOcc_range_ge j j (Nat.le_refl j)]
      simp [countOcc]

/-- Counting `true`s over a row of column indicators `fun j => j = j₀` is the
same as counting occurrences of `j₀`. -/
theorem countTrue_map_indicator (j₀ : Nat) :
    ∀ l : List Nat,
        countTrue (l.map (fun j => decide (j = j₀))) = countOcc j₀ l := by
  intro l
  induction l with
  | nil => rfl
  | cons x l ih =>
    by_cases h : x = j₀ <;> simp [h, countTrue, countOcc, ih] <;> omega

/-! ## (a) The counting lemma -/

/-- **Counting lemma** (Lemma 3 of cert_floor.md, row half): the answer row of
a killed pigeon contains exactly one `1`.  The coin values of free pairs are
irrelevant: a killed pigeon has none. -/
theorem killed_row_singleton (mu : Mu) (g : Nat → Nat → Bool) (m i j₀ : Nat)
    (hmu : mu i = some j₀) (hj : j₀ < m) :
    countTrue (row mu g m i) = 1 := by
  have hrow : row mu g m i
      = (List.range m).map (fun j => decide (j = j₀)) := by
    simp only [row]
    apply List.map_congr_left
    intro j _
    exact answer_of_killed mu g i j j₀ hmu
  rw [hrow, countTrue_map_indicator]
  exact countOcc_range_of_lt j₀ m hj

/-- Same, phrased with the `Killed` predicate and under the table's
well-formedness hypothesis. -/
theorem killed_row_singleton' (mu : Mu) (g : Nat → Nat → Bool) (m i : Nat)
    (hwf : WellFormed mu m) (hk : Killed mu i) :
    countTrue (row mu g m i) = 1 := by
  obtain ⟨j₀, hj₀⟩ := hk
  exact killed_row_singleton mu g m i j₀ hj₀ (hwf i j₀ hj₀)

/-! ## (b) Soundness of the counting certificate -/

/-- **Soundness of the counting certificate** (certificate (a) of
cert_floor.md): if a pigeon's row does not have `1`-count exactly `1`, then
the pigeon is free.  (Contrapositive: killed rows always count exactly one
`1`, by `killed_row_singleton`; so observing any other count certifies
freeness.)  This direction uses well-formedness: the pigeon's hole must be a
column of the table. -/
theorem cert_row_free (mu : Mu) (g : Nat → Nat → Bool) (m i : Nat)
    (hwf : WellFormed mu m) (h : countTrue (row mu g m i) ≠ 1) :
    Free mu i := by
  cases hmi : mu i with
  | none => exact hmi
  | some j₀ =>
    exfalso
    exact h (killed_row_singleton mu g m i j₀ hmi (hwf i j₀ hmi))

end CoreChannel
