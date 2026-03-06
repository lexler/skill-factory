# Lens: Naming (Reviewer Guide)

## When to Apply

After formatting is clean. Names are easier to evaluate without surface noise.

## What to Look For in Diffs

- Renames that clarify intent
- Vague names replaced with specific ones
- Verb changes (get → parse, handle → validate)

## First Pass

Worker should find obvious naming issues — generic names, unclear abbreviations.

## Second Pass

If names still feel off:
- Question verb choices: does "get" really retrieve, or does it transform?
- Look for implementation language hiding in names
- Check if names match what the code actually does

## When Done

Move on when names communicate clearly — someone new could understand without reading implementations.
