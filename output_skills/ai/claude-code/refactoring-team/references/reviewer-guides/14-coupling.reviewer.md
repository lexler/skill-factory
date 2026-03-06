# Lens: Coupling & Dependencies (Reviewer Guide)

## When to Apply

After semantic clarity. Now that the code reads well, look at the invisible wires between units — what depends on what, and why.

## What to Look For in Diffs

- Dependencies removed or narrowed (imports reduced, parameters simplified)
- Domain logic separated from framework/library details
- Chains of object access shortened — units no longer reaching through collaborators
- Unnecessary intermediaries inlined or given real responsibility

## First Pass

Worker should find the obvious: chains of object access, scattered changes from a single concept, framework details mixed into domain logic.

## Second Pass

If coupling still feels heavy:
- Do the ripple trace yourself: pick a unit and ask "if I changed this, what else breaks?" If the answer is "many things," there's coupling the worker missed
- Look for modules that depend on each other in circles
- Look for data or parameters passed through untouched — invisible wires the worker may not have noticed

## When Done

Move on when dependencies feel intentional — each unit depends on what it genuinely needs and nothing more.
