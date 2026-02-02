---
name: event-modeling
description: Designs systems using Event Modeling — vertical slices with commands, events, read models, and specifications. Use when designing a new system, modeling domain behavior, planning vertical slices, discussing event sourcing, or analyzing an existing codebase's business processes.
---

STARTER_CHARACTER = 🗺️

## What Event Modeling Produces

A set of vertical slices that fully describe a system's behavior. Each slice is independently implementable and testable. The model uses business language throughout — no infrastructure or technical terms.

```
                    ┌─────────────────────────────────────┐
                    │          Event Model                │
                    │                                     │
                    │  ┌───────────┐  ┌───────────┐       │
                    │  │  Slice 1  │  │  Slice 2  │  ...  │
                    │  │ STATE_    │  │ STATE_    │       │
                    │  │ CHANGE    │  │ VIEW      │       │
                    │  └───────────┘  └───────────┘       │
                    │         │              ▲            │
                    │         │  (events)    │            │
                    │         └──────────────┘            │
                    └─────────────────────────────────────┘
```

## Slice Types

Three types. Every behavior in the system fits one:

STATE_CHANGE — user does something
- Screen → Command → Event
- Command produces one or more events
- May have error events for failure paths

STATE_VIEW — system shows something
- Events → Read Model → Screen
- Read model aggregates data from one or more events

AUTOMATION — system reacts to something
- Event → Processor → Command → Event
- Background process, no user interaction

See [references/slice-types.md](references/slice-types.md) for element rules, dependency patterns, and naming conventions.

## Conversational Design Process

Work with the user through these phases. Move at the user's pace — they might want to go deep on one slice before seeing the full picture.

### Phase 1: Understand the Domain
Identify aggregates (core business entities), actors, and high-level use cases. Ask about the business processes, not technical implementation.

### Phase 2: High-Level Model
Draft all slices without field details. Show the flow between them — which events feed which read models, which screens lead to which commands. This is the "map" of the system.

Format as a markdown document with one section per slice. Include slice type, aggregate, elements, and how slices connect.

### Phase 3: Slice Detail
Walk through one slice at a time. For each:
- Define fields with types and example values
- Identify business rules (not simple validations — real domain rules)
- Write specifications as Given/When/Then scenarios

### Phase 4: Executable Specifications
Turn specifications into approval fixture files using the `bdd-with-approvals` skill. That skill teaches how to:
- Design scannable fixture formats adapted to the domain
- Structure input/output for human validation
- Build parsers and formatters

Read that skill when it's time to design fixtures. The event model specs (Given events / When command / Then events) map naturally to the approved fixture pattern.

### Analyzing Existing Code
When working with an existing codebase instead of greenfield:
- Read the code to extract domain concepts
- Map existing operations to slice types (writes → STATE_CHANGE, reads → STATE_VIEW, background → AUTOMATION)
- Put code references (class names, packages) in element descriptions
- Extract specs from unit tests and comments

## Output Format

Produce markdown, not JSON. Design for human readability — someone should look at the model and understand the system.

Write model artifacts to files. Ask the user where they want them (e.g., `docs/event-model.md`). Update the files as the model evolves through conversation.

### High-Level Model

One document showing all slices and their relationships:

```markdown
# [System Name] Event Model

## Aggregates
- Owner — pet owners who use the clinic
- Pet — animals registered to owners

## Slices

### Register Owner [STATE_CHANGE]
Aggregate: Owner
Screen: Owner Registration Form
Command: Register Owner → Event: Owner Registered
Error: → Owner Registration Failed

### View Owner Profile [STATE_VIEW]
Aggregate: Owner
Events: Owner Registered, Pet Registered → Read Model: Owner Profile
Screen: Owner Profile

### Notify Vet of New Patient [AUTOMATION]
Trigger: Pet Registered → Processor: New Patient Notifier
Command: Send Notification → Event: Vet Notified
```

### Detailed Slice

Per-slice detail includes fields and specifications:

```markdown
## Register Owner [STATE_CHANGE]
Aggregate: Owner

### Command: Register Owner
  firstName: String — "George"
  lastName: String — "Franklin"
  address: String — "110 W. Liberty St."
  city: String — "Madison"
  telephone: String — "6085551023"

### Event: Owner Registered
  ownerId: UUID — <generated>
  firstName: String — "George"
  lastName: String — "Franklin"
  address: String — "110 W. Liberty St."
  city: String — "Madison"
  telephone: String — "6085551023"

### Event: Owner Registration Failed
  errors: Map — {"lastName": "required"}

### Specifications

#### Successfully register with valid data
Given: (no prior state)
When: Register Owner
  firstName: George, lastName: Franklin
  address: 110 W. Liberty St., city: Madison
  telephone: 6085551023
Then: Owner Registered
  ownerId: <generated>, firstName: George, lastName: Franklin

#### Fail when required fields missing
Given: (no prior state)
When: Register Owner
  firstName: George, city: Madison
Then: Owner Registration Failed
  errors: {address: required, telephone: required}

#### Business rules
- All fields mandatory: firstName, lastName, address, city, telephone
- Telephone must be numeric, max 10 digits
```

These are defaults. Adapt the format to the domain — what matters is that a person can scan it and quickly validate correctness.

## Anti-Patterns

- Technical language in element names ("insertOwnerRecord" → "Register Owner")
- Skipping STATE_VIEW slices — every query/display is a slice
- Circular dependencies between elements
- Specs that test simple validation ("must be a number") instead of business rules
- Jumping to fixture format before the model is understood
- Combining multiple commands in one slice — one command per STATE_CHANGE

## See Also

- For executable test specifications: invoke the `bdd-with-approvals` skill
- For approval testing mechanics: invoke the `approval-tests` skill
