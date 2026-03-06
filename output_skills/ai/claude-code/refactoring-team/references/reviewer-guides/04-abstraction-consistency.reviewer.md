# Lens: Abstraction Consistency (Reviewer Guide)

## When to Apply

After method length. Functions are now smaller, easier to see level mixing.

## What to Look For in Diffs

- Inline code extracted to match surrounding abstraction level
- Entry points becoming pure orchestration
- Low-level details pushed into helper functions

## First Pass

Worker should find obvious mixing — inline code surrounded by function calls.

## Second Pass

If levels still feel mixed:
- Look at entry points: are they pure orchestration or do they do detailed work?
- Check if arg parsing, path manipulation, or I/O details live at the right level
- Find functions where one line feels "different" from the rest

## When Done

Move on when functions feel uniform — each line belongs at the same level.
