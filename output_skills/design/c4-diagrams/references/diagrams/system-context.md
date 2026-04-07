# System Context Diagram

The starting point for any architecture conversation. Shows the big picture: one software system, who uses it, and what it depends on.

## Scope

A single software system.

## Elements

- **Primary**: The software system in scope (center of the diagram)
- **Supporting**: People who use it, external software systems it interacts with

Nothing inside the system boundary is shown — no containers, no components. This is the most zoomed-out view of a single system.

## Audience

Everyone — technical and non-technical. This is the diagram you show stakeholders, product managers, new team members. It answers: "What is this thing, who uses it, and what does it talk to?"

## What to Include

- The software system as a single box
- All user types/roles that interact with it (don't collapse distinct roles into one generic "User" if they have different interactions)
- All external systems this system depends on or is depended upon by
- Relationship labels describing what flows between elements ("Sends email via", "Fetches customer data from")

## What NOT to Include

- Internal structure (containers, components, code)
- Infrastructure details
- Implementation technology of the system itself (save that for Container level)

## Common Mistakes

- Showing too many external systems — include only direct dependencies, not transitive ones
- Using a single "User" when there are meaningfully different roles (admin vs customer vs support agent)
- Forgetting to show systems that depend ON yours, not just systems yours depends on
- Labeling relationships as just "Uses" instead of describing the actual interaction
