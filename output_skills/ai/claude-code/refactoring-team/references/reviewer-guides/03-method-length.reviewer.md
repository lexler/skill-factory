# Lens: Method Length (Reviewer Guide)

## When to Apply

After naming is clear. Easier to see function boundaries when names communicate well.

## What to Look For in Diffs

- Function extractions with clear names
- Early returns reducing nesting
- Long functions split into focused pieces

## First Pass

Worker should find obvious long functions and extract where clear.

## Second Pass

If functions are still long:
- Point to functions with multiple "paragraphs" of logic
- Look for entry points doing I/O + processing + output (should be separate)
- Check for deep nesting that early returns could flatten

## When Done

Move on when functions feel focused — each does one nameable thing.
