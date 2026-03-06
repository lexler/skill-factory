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

## Phase 2: Plan

Pick the lenses that would benefit most from a re-run. Prioritize by impact — which re-run would produce the most meaningful improvement?

Always end the plan with the surface lenses (01-formatting, 02-naming, 03-method-length) — structural refactoring creates new surface mess that needs a final cleanup pass.

Message **WORKER_NAME** with the plan: which lenses to re-apply and in what order. For each lens, tell the worker to read the lens file again and apply it fresh.

## Phase 3: Execute

Walk the worker through the re-run plan one lens at a time, reviewing diffs after each. When the re-run plan is exhausted and no further improvements are visible, move to wrap-up.

## Wrap-up

Write REFACTORING-LOG.md:
- What was refactored (summary of the journey — key transformations, patterns applied, before/after highlights)
- Current problems (issues that cannot be fixed by restructuring alone — things needing behavior changes)
- Future improvements (recommendations for the human — what should the code do differently?)

Then run: `speak "Round complete"`

After writing the log, go idle. The manager will decide whether to run a quality check and potentially launch another round.
