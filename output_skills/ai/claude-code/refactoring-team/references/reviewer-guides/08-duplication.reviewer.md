# Lens: Duplication (Reviewer Guide)

## When to Apply

After patterns. Once patterns are explicit, duplicate encodings of the same concept become visible.

## What to Look For in Diffs

- Multiple lists/structures consolidated into one source of truth
- Derived values instead of parallel definitions
- Single constants replacing scattered magic values

## First Pass

Worker should spot obvious duplication — parallel lists, repeated constants, similar transformations.

## Second Pass

If worker found nothing:
- Look for data structures that define the same set of things
- Find the same knowledge written in multiple places
- Ask: what knowledge is encoded more than once?

## Trade-off Reminder

Not all duplication is bad. Sometimes explicit parallel structures are clearer than a clever derivation. Ask: does consolidating help readers, or just satisfy DRY purists?

## When Done

Move on when duplicated knowledge is consolidated where it helps clarity, and left explicit where that's clearer.
