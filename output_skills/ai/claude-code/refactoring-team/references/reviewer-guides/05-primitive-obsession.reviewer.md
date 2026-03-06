# Lens: Primitive Obsession (Reviewer Guide)

## When to Apply

After abstraction consistency. Now that functions are clean, hidden concepts become visible.

## What to Look For in Diffs

- Tuples/dicts replaced with named types (NamedTuple, dataclass)
- New type definitions that name previously implicit concepts
- Code that's clearer because concepts have names

## First Pass

Worker should identify obvious primitives carrying meaning — tuples unpacked the same way repeatedly, dicts with known keys.

## Second Pass

If the worker found nothing and you still see something to improve, point to all those things that could be a concept in our codebase, and ask the worker questions about it and whether it is a hidden concept.

## Discover Through Writing

If concepts aren't obvious, have worker write to `playground/concepts.md`:
1. List data structures and how they're used
2. Write what you'd call each if explaining to someone
3. Names used that don't exist in code = hidden concepts

## When Done

Move on when primitives feel appropriate — no obvious concepts hiding as raw data.
