# Lens: Final Review (Reviewer Guide)

## When to Apply

After all other lenses. This is the wrap-up — assess the code holistically and decide what deserves a second pass.

## Phase 1: Assess

Read through the refactored code end to end. Earlier lenses changed the code — those changes may have created new opportunities that were invisible on the first pass.

Ask for each lens area:
- Did the responsibility and coupling changes reveal new cohesion issues?
- Did extracting functions create new naming or abstraction-level problems?
- Did consolidating logic surface new duplication or wrong abstractions?
- Are there conditionals that became visible only after other cleanup?

## Phase 2: Design Lens Re-runs

Pick the lenses that would benefit most from a re-run. Prioritize by impact — which re-run would produce the most meaningful improvement?

Message **WORKER_NAME** with the plan: which lenses to re-apply and in what order. For each lens, tell the worker to read the lens file again and apply it with fresh eyes — not as a touch-up, but as if seeing the code for the first time. Walk them through one lens at a time, reviewing diffs after each.

## Phase 3: Method-Length Re-examination

After the design re-runs, re-apply 03-method-length thoroughly. This is not a cleanup pass — it is the most important re-application because every design lens changes what's extractable:

- New names and types now exist that didn't before — phases inside long functions may now have obvious names
- Responsibilities have shifted — functions that were "fine" early on may now clearly do too much
- The worker's first-pass assumptions are stale — challenge them

Push the worker to look at every function again, not just the ones that changed. Functions that got a pass early ("it's just orchestration," "it's main") deserve the hardest second look. If a function still has blank-line paragraphs, phases, or repeated structure, it is still too long — the design lenses should have provided the vocabulary to name those pieces.

Then re-apply 02-naming and 01-formatting as a final surface cleanup.

## Wrap-up

Write REFACTORING-LOG.md:
- What was refactored (summary of the journey — key transformations, patterns applied, before/after highlights)
- Current problems (issues that cannot be fixed by restructuring alone — things needing behavior changes)
- Future improvements (recommendations for the human — what should the code do differently?)

Then run: `speak "Refactoring complete"`
