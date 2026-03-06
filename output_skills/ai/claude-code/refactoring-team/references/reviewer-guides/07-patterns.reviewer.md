# Lens: Patterns (Reviewer Guide)

## When to Apply

After domain alignment. Now that the domain is clear, structural patterns become visible.

## What to Look For in Diffs

- Patterns named explicitly in code structure
- Duplication consolidated (but only if it helps clarity)
- Implicit rules made explicit

## First Pass

Worker should identify obvious patterns — repeated structures, implicit templates.

## Second Pass

If patterns are still hidden:
- Look for the "shape" of the code — what does it remind you of?
- Find duplication across functions — is there an underlying pattern?
- Check if grammar or rules could be made visible in names

## Trade-off Check

Before consolidating duplication, ask: is this clearer or just more DRY? Sometimes explicit duplication is better than forced abstraction.

## When Done

Move on when the code's patterns are visible in its structure — readers can see the "shape" of the solution.
