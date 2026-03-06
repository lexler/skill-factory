# Lens: Structural Storytelling (Reviewer Guide)

## When to Apply

After file boundaries. Now that files are coherent, internal narrative structure becomes the focus.

## What to Look For in Diffs

- Functions reordered to tell a story (entry points first)
- Public API moved to top of files
- Related functions grouped together
- Code that reads top-to-bottom without jumping

## First Pass

Worker should find obvious ordering issues — entry points not at top, related functions scattered.

## Second Pass

If structure still doesn't tell a story:
- Apply the "cover test": hide bottom half, can you understand from top?
- Look for the narrative: what's the "chapter order" that makes sense?
- Check if helper functions come after the functions that call them

## When Done

Move on when files read like a story — high-level first, details after, a natural flow from top to bottom.
