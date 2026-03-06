# Lens: Formatting (Reviewer Guide)

## When to Apply

First lens in Phase 2. Clears surface noise so deeper issues become visible.

## What to Look For in Diffs

- Deletions of dead code, unused imports
- Formatting consistency improvements
- Removal of redundant wrappers

## First Pass

Worker should find the obvious: unused imports, commented code, clear formatting issues.

## Second Pass

If code still has noise, look for:
- Redundant exception handling
- Code that exists but is never called
- Inconsistencies worker missed

## When Done

Move on when the surface is clean — no obvious noise remains.
