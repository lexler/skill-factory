# Lens: Primitive Obsession

Domain concepts often hide as primitives. A tuple isn't just a tuple — it represents something. A dict isn't just a dict — it has a name you'd use when explaining.

## The Question

What concepts in this code are hiding as raw data structures?

## How to Spot

Ask: if I had to explain this to someone, would I use a name that doesn't exist in the code?

Look for:
- Tuples unpacked the same way in multiple places
- Dicts with known keys accessed repeatedly
- Strings split/joined in consistent patterns
- Data passed between functions that "means something"

## First Pass

Look broadly. What tuples, dicts, or strings carry meaning beyond their type?

## Go Deeper

What else in this code fits this lens? What other primitives are carrying hidden meaning?
