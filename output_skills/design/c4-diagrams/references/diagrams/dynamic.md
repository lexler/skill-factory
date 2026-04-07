# Dynamic Diagram

Shows how elements interact at runtime to fulfill a specific use case, user story, or feature. Complements the static structure diagrams by revealing behavior.

## Scope

A specific feature, use case, or user story — not the whole system.

## Elements

Flexible — you can show software systems, containers, or components interacting, depending on the level of detail needed. Pick the level that matches the story you're telling.

## Audience

Technical and non-technical people, depending on the level of abstraction chosen.

## How It Works

Based on UML communication diagrams. Elements are arranged freely (not in sequence diagram columns) with numbered interactions showing the order of operations.

Two presentation styles:
- **Collaboration style** — elements arranged spatially with numbered arrows between them
- **Sequence style** — elements in columns with numbered messages flowing between them

Both convey the same information. Collaboration style works better in ASCII and for non-linear flows. Sequence style works better for strictly sequential interactions.

## What to Include

- Only the elements involved in this specific use case
- Numbered interactions in execution order
- Description of what happens at each step
- The initiating actor/event

## What NOT to Include

- Elements not involved in this flow
- Every possible error path (focus on the primary flow, note exceptions separately)
- Implementation details below the chosen abstraction level

## When to Create

Use sparingly. Create Dynamic diagrams for:
- Complex interactions that aren't obvious from static structure
- Recurring patterns worth documenting
- Flows that cross multiple containers or systems
- Onboarding material for non-obvious behavior

Don't create one for every endpoint or feature — only when the dynamic view adds understanding that the static diagrams don't convey.
