# Lens: Duplication

Duplication often hides. It's not just copy-pasted code — it's multiple structures encoding the same concept, or parallel lists that could derive from one source.

## The Question

What knowledge exists in more than one place? Where would a change require updating multiple locations?

## How to Spot

- Multiple data structures encoding the same set of things
- Parallel arrays that always change together
- Similar transformations repeated across the codebase
- Constants or magic values that appear in multiple places

## The Test

Is the same knowledge written more than once? That's duplication.

## Process

Look for structures that encode the same knowledge. Could they derive from a single source of truth?

## Go Deeper

What else is duplicated? What other knowledge lives in multiple places?
