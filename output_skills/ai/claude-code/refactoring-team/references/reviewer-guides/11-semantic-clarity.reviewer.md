# Lens: Semantic Clarity (Reviewer Guide)

## When to Apply

After structural storytelling. Structure is now clear — this lens asks whether the code communicates meaning, not just mechanics.

## What Worker Should Do

1. Use refinement-loop skill to distill understanding of problem/solution space
2. Check their English for implementation details — it should be pure problem/solution
3. Come up with list of refactorings needed to make code match the English
4. Implement the refactorings

## What to Look For in Diffs

- Names that shifted from implementation to domain
- Structure changes that make problem/solution clearer
- Code that now reads like a story, not mechanics

## First Pass

Review what the worker improved.

## Second Pass

Do the same exercise yourself using refinement-loop:
- What is the problem this code solves?
- How does it solve it?
- Distill to high-level English with no implementation details

Then look at the code. What concepts or ideas aren't communicated that should be? Point out what the worker missed.

## When Done

Move on when the code tells its semantic story — someone reading it understands the problem and solution, not just the implementation.
