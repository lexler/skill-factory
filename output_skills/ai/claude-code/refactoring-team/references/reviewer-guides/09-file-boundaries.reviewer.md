# Lens: File Boundaries (Reviewer Guide)

## When to Apply

After patterns. Now that internal structure is clear, file-level organization becomes visible.

## What to Look For in Diffs

- Files renamed to reflect their concept
- Code moved between files to create coherent units
- New files created for distinct concepts
- "utils" files eliminated or properly named

## First Pass

Worker should find obvious issues — vague file names, clear concepts split across files.

## Second Pass

If file structure still feels off:
- Look at imports — heavy cross-importing suggests wrong boundaries
- Check if "utils" contains actual utilities or hidden concepts
- Ask if each file could be explained in one sentence

## When Done

Move on when files feel like coherent units — each represents one clear concept.
