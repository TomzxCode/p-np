import Lake
open Lake DSL

package «lean_channel» where
  leanOptions := #[⟨`autoImplicit, false⟩]

require mathlib from "mathlib4"

@[default_target]
lean_lib «LeanChannel»
