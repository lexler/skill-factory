# System Context Diagram

Source: https://c4model.com/diagrams/system-context

## Scope
A single software system.

## Audience
Everyone — technical and non-technical. This is the diagram you show stakeholders, new team members, and anyone asking "what does this thing do?"

## Elements

**Primary:** The software system in scope — drawn as a box in the center.

**Supporting:** People and external software systems that directly interact with the system in scope. Nothing else.

## What to Include
- Every person/role that uses or is affected by the system
- Every external system that the system sends data to or receives data from
- Relationship labels describing what happens ("sends email notifications", "authenticates via"), not implementation ("HTTP POST", "gRPC")

## What to Exclude
- Anything inside the system — no containers, no components, no code
- Technology choices — this level is technology-agnostic
- Protocols and data formats
- Systems that don't directly interact with the system in scope (indirect dependencies belong in a System Landscape diagram)

## Relationship Labels
Use business language. Describe what the user does or what flows between systems.

Good: "manages appointments", "sends order confirmations to"
Bad: "uses", "calls API", "HTTP/JSON"

## Common Mistakes
- Drawing the system too small or off-center — it's the star of this diagram
- Showing internal structure (databases, APIs) — save that for Container level
- Including indirect dependencies — only show direct interactions
- Using technical jargon in labels when the audience is non-technical
