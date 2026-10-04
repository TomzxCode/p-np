# Guidance on the P vs NP corpus

Written 2026-10-04 after a full review of the repository (layout, README, GOAL,
instruction log, bibliography, verifier, Lean sources, paper, open-problems
catalog, and the key theory notes). External references were checked against
the sources.

## What this actually is

This is not a P vs NP investigation. It is a detailed study of one recent
reduction (Krajicek, arXiv:2609.35927, Sep 2026) toward AC^0[p]-Frege lower
bounds for the pigeonhole principle, restricted to the p=2 case, plus a
forensics pass over unrelated claimed resolutions. That is a legitimate and even
interesting thing to do, but the headline oversells it.

The external spine holds up. arXiv:2609.35927 (Krajicek, Def 3.1, Def 4.3,
Lemma 4.4, Theorem 6.1 all exist and are quoted accurately), arXiv:2510.08814
(Goertzel), arXiv:2512.11820 (Edwards, 208 pp), and arXiv:2609.23015 (Braun)
are all present and match. The reading of Definition 3.1 and 4.3 is faithful to
the paper. That accuracy is the strongest part of the work and is worth keeping.

## What is genuinely good

- The primary-source discipline is better than most human efforts. Quotes are
  anchored, the Krajicek definitions are reproduced correctly, and the pointer
  to the open crux (the all-degrees budgeted error floor, O2) is the right one.
  Krajicek's hypothesis really does require a floor over all (d,e)-trees
  (Definition 3.1 condition 3), so the reformulation is not a misreading.
- The failure-mode taxonomy (F1 to F7) and the claim forensics are reusable.
- The self-correction ledger is unusually candid, and the
  "PROVED / MEASURED / CONJECTURED" labels are the right idea.

## The problems, most important first

1. The verdict is not a result. "P != NP, about 93% confidence" is a restated
   prior, not something this work produced. Refuting two crank preprints and
   listing known barriers does not move the probability of a Millennium
   Problem. Presenting a made-up percentage as a session output invites the
   owner to believe progress was made. Delete it or relabel it plainly as
   "subjective prior, not derived from this work".

2. The verifier does not verify. `verify_corpus.py` checks that required
   substrings appear in required files, that scripts compile, and that LOG
   headings are monotone. It tests documentation consistency, not mathematics.
   Describing a PASS as "the corpus is clean" and "351 checks all PASS"
   (README line 97) overstates it badly. It is also circular: the checker
   requires README to contain "0.97 at (32,2)" and the detail document to
   contain the same string, which proves they agree, not that 0.97 is correct.
   Rename it to something like corpus_lint.py and stop citing its PASS as
   validation.

3. Over-claiming presented as established fact. The bibliography (line 15)
   states "printed Theorem 6.1(3) is false as printed". In the source, (3) is a
   hypothesis assumed about a chosen tree T', not a claim the paper makes, so
   it cannot be false as printed. The corpus's own chi_transfer.md marks the
   universal quantifier as INFERENCE. Turning that inference into a flat
   accusation against a correct paper is precisely failure mode F1/F3. Any
   statement that a published result is wrong must be downgraded to "I could not
   make the printed hypothesis do the work; here is where I think the gap is".

4. Simulation artifacts dressed as exact laws. The "exact law" of the
   two-phase tree turned out to be a simulator bug, and the ledger records
   around eleven correction-class events, several flipping a PROVED result. The
   discipline improved, but the pattern is clear: small simulations of a
   self-defined channel generate artifacts faster than they generate insight.
   Freeze the channel semantics in a written spec before coding, and never let
   a measured constant carry a PROVED label.

5. Significance overreach and goal drift. Degree <= 2 and <= 3 caps in a p=2 toy
   are narrow. The reduction needs all degrees and all p, and even a full proof
   of O2 would only deliver a conditional lower bound. Writing about "the
   program's p=2 core" and near-miss AC^0[2]-Frege bounds implies the crux is
   close when it is not. GOAL.md tries to hold a Millennium Problem and a
   bounded session at the same time, which produces motion without convergence.

6. The work is being measured by activity, not output. A 1,700-line LOG, 30
   documents, and 22 scripts back a handful of toy lemmas. Documents layer
   corrections and supersessions instead of converging on one current
   statement. The corpus is also at risk of its own failure taxonomy: F1
   (redefining the target), F3 (transferring a toy result to the program), and
   F6 (Lean proving a convenience model, not the pipeline).

7. Hygiene drift. README says 351 checks, GOAL says about 398, the actual run
   reports 405. README says 9 Lean sorries, the file has about 10. LOG.md has
   uncommitted edits, and the LOG claims six dispatched deliverables
   (deg4_theory, mixture_cap, odd_p_theory, lemma_m, jdp_demod, gap_e_constants)
   that do not exist in docs/. This is exactly the drift the corpus's own rules
   warn against.

8. The Lean claims are softer than they read. CoreChannel.lean "zero sorry"
   proves facts about a model defined for convenience (a killed row has exactly
   one true), which is true by construction and says nothing about Krajicek's
   pipeline. LeanChannel.lean leaves the interesting parts as sorry.
   "Machine-checked" is true but not decisive for the program.

## What to do next, in priority order

1. Reframe the top of README and GOAL. State plainly: the problem is open, no
   progress toward a resolution was made, and this is a study of Krajicek's
   reduction and its open crux O2. Drop the confidence number.

2. Pick one purpose and commit to it: a learning log, a survey, or a small
   contribution. If a contribution, the only candidate is a careful note on the
   p=2 restriction of Krajicek's reduction, and it needs an expert to confirm
   the reading before anything else.

3. Highest-value single action: turn note_to_author.md from a refutation into a
   reading-check question to Krajicek or a proof-complexity person ("is my
   reading of Def 3.1/4.3 correct, and is the p=2 toy the right place to
   look?"). The owner reserves sending; recommend doing it as a question, not a
   claim.

4. Make the gate mean something: run `lake build` with an asserted sorry and
   axiom budget, run the experiments and regenerate every number the docs
   quote, and pin the cited sources by content hash so citations cannot drift.

5. Enforce PROVED vs MEASURED vs INFERRED mechanically, and forbid PROVED
   unless there is a written, line-by-line proof or a machine-checked statement
   of the same proposition.

6. Consolidate and freeze: one current theorem map, superseded framings
   archived, and the daily monitoring of crank claims reduced to a one-line
   appendix (it is low-value and it inflates the sense of having worked on the
   problem).

7. Land or remove the six missing deliverables, fix the stale counts, and
   commit LOG.md.

## Bottom line

The intern built a careful, well-sourced study around a genuine open problem
and correctly found the true crux. That is worth something. The failure is
framing and discipline: treating a survey plus toy lemmas as a verdict on
P vs NP, treating a documentation linter as verification, and repeatedly
promoting measurements to proofs. Fix the framing, right-size the tooling, and
get one expert to validate the one reading that matters. Then either pursue the
p=2 note seriously with proper proof obligations, or stop and present this as
the survey it is.
