# Owner instruction log (verbatim, dated)

Moved out of GOAL.md on 2026-10-04 (owner directive: "Move the instruction log
from the GOAL.md file out of it"). GOAL.md keeps the compiled, normative
instructions; this file keeps the verbatim history. New entries are appended
here whenever the owner issues a standing instruction.

- 2026-10-03: "Prove or disprove P != NP." (objective, repeated as the standing
  continuation directive each cycle).
- 2026-10-03: "Reset the continuation budget and set an infinite one. Then
  continue working on the problem. Use as many agents as possible to work on
  parts of the problem in parallel."
- 2026-10-03: "Stop thinking and distribute the work among subagents."
- 2026-10-03: "You should be running more parallel agents."
- 2026-10-04: "Generate a diagram of the theorems/proofs you've identified and
  what they build on and where there are currently gaps."
- 2026-10-04: "Those should be in mermaid blocks."
- 2026-10-04: "Create a file tracking all relevant bibliography."
- 2026-10-04: "Take all the instructions I gave and turn them into a GOAL.md
  file." (created GOAL.md)
- 2026-10-04: "You can use the $math$ syntax in markdown files to use latex
  expressions." (adopted: LaTeX math in presentation documents; ASCII stays in
  Mermaid labels and LOG entries)
- 2026-10-04: "Add instructions to commit and push whenever relevant." (adopted:
  GOAL.md section 4 - verify then commit with a descriptive message and push
  after every consolidated turn; append-only history; toolchain artifacts
  gitignored)
- 2026-10-04: "Move elan out of tmp if you need it." (adopted: elan moved to its
  default home /home/tomzx/.elan; PATH line in ~/.bashrc; do not reinstall into
  /tmp)
- 2026-10-04: "Have we already pulled all the lean libraries we might need?"
  (status question; answered by audit - everything needed is pulled and working)
- 2026-10-04: "Reorganize the directory in a sane directory structure instead of
  being almost entirely flat." (adopted: docs/, docs/monitors/, experiments/,
  paper/, lean_channel/; verify_corpus.py updated for the tree)
- 2026-10-04: "Dispatch 1 agent per file." (adopted: the LaTeX conversion runs
  one agent per file, each with a verify-first commit-and-push)
- 2026-10-04: "Move the instruction log from the GOAL.md file out of it."
  (created this file)
