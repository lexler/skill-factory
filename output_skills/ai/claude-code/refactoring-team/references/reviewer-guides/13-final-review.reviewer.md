# Lens: Final Review (Reviewer Guide)

## When to Apply

After all other lenses. This is the wrap-up — push refactoring to its limit.

## What Worker Should Do

Implement remaining refactorings, not just list them. Worker should also note issues beyond refactoring's reach.

## Your Job: The Loop

Review worker's changes. Ask: "Are there more refactorings?"

- **Yes** → Send worker back: "I see more refactoring opportunities: [specific example]. Go again."
- **No** → Refactoring is exhausted. Write the summary.

Keep looping until worker truly can't find more. Don't let them stop early.

## When Refactoring Is Exhausted

Write REFACTORING-LOG.md:

- What was refactored (summary of the journey — key transformations, patterns applied, before/after highlights)
- Current problems (issues that can't be fixed by restructuring alone — things needing behavior changes)
- Future improvements (recommendations for the human — what should the code do differently?)

## When Done

When no refactorings remain and you've written the log, run `speak "Refactoring complete"`.
