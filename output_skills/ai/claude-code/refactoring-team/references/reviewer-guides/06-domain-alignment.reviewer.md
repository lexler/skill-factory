# Lens: Domain Alignment (Reviewer Guide)

## When to Apply

After primitive obsession. Now that concepts are named, check if they're the RIGHT names — domain names, not implementation names.

## What to Look For in Diffs

- Implementation names replaced with domain names
- New domain concepts introduced
- Code that reads more like the problem description

## First Pass

Worker should find obvious implementation language hiding domain concepts.

## Second Pass

If code still feels technical:
- Compare how you'd EXPLAIN the code vs how it READS
- Look for names that describe implementation instead of domain
- Find places where "what we're doing" is clear but "what it means" is obscured

## When Done

Move on when the code reads like a description of the problem domain — someone familiar with the domain (not the code) could follow it.
