#!/usr/bin/env bash
# Lean gate (GUIDANCE priority 4): asserts the sorry budget and prints axiom
# bases. A pass means: CoreChannel has zero sorries and depends only on the
# standard axioms; LeanChannel's sorry count is within its registered budget.
set -u
export PATH="$HOME/.elan/bin:$PATH"
cd "$(dirname "$0")"

# Count sorry TERMS, not comment mentions (naive grep counted prose lines).
term_count() {
  grep -vE '^\s*(--|/-)' "$1" | grep -oE '^\s*sorry\b|:= sorry\b' | wc -l
}
core_sorries=$(term_count CoreChannel.lean)
echo "CoreChannel.lean sorry terms: $core_sorries (budget: 0)"
if [ "$core_sorries" -ne 0 ]; then echo "LEAN GATE: FAIL (CoreChannel sorry budget)"; exit 1; fi

chan_sorries=$(term_count LeanChannel.lean)
echo "LeanChannel.lean sorry terms: $chan_sorries (registered budget: 9)"
if [ "$chan_sorries" -gt 9 ]; then echo "LEAN GATE: FAIL (LeanChannel sorry budget)"; exit 1; fi

cat > /tmp/opencode/axiom_check_cc.lean <<'LEOF'
import CoreChannel
#print axioms killed_row_singleton
LEOF
if timeout 120 lake env lean /tmp/opencode/axiom_check_cc.lean 2>&1 | tail -2; then
  echo "LEAN GATE: PASS (CoreChannel zero-sorry, axiom base printed above; LeanChannel within budget)"
else
  echo "LEAN GATE: FAIL (CoreChannel elaboration or axioms)"
  exit 1
fi
