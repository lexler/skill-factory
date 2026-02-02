# Slice Types Reference

## Element Types

Command — an action that changes state. Named as action verbs: "Register Owner", "Schedule Visit", "Cancel Booking"

Event — a fact about what happened. Named in past tense: "Owner Registered", "Visit Scheduled", "Booking Cancelled"

Read Model — a data view for presentation. Named as descriptive nouns: "Owner Profile", "Visit History", "Cart Items"

Screen — a UI representation. Named as UI-focused nouns: "Registration Form", "Owner Profile Page", "Search Results"

Processor — a background automation. Named as process descriptions: "Payment Processor", "Notification Sender"

## STATE_CHANGE

User does something that changes system state.

Required elements: 1 Command + 1 or more Events
Optional elements: 1 Screen (when preceded by a STATE_VIEW slice)

```
Screen ──→ Command ──→ Event
                  └──→ Error Event (failure path)
```

Dependencies:
- Screen OUTBOUND → Command INBOUND
- Command OUTBOUND → Event INBOUND

Specifications pattern:
- GIVEN: prior events (or "no prior state")
- WHEN: the command with field values
- THEN: resulting event(s) with field values

Each command produces exactly one type of success event. It may also produce error events for failure paths. Model error paths as separate events (e.g., "Owner Registration Failed") — they represent distinct outcomes.

## STATE_VIEW

System presents data to a user.

Required elements: 1 Read Model
Optional elements: 1 Screen (when preceded by a STATE_CHANGE slice)

```
Event(s) ──→ Read Model ──→ Screen
```

Dependencies:
- Event OUTBOUND → Read Model INBOUND (one or more events feed the read model)
- Read Model OUTBOUND → Screen INBOUND

Specifications pattern:
- GIVEN: events that produce the data
- THEN: read model contents

A read model can aggregate data from multiple events across different aggregates. This is where cross-aggregate views live (e.g., "Owner Profile" shows Owner + Pet + Visit data).

## AUTOMATION

System reacts to an event without user interaction.

Required elements: 1 Processor + 1 Command + 1 or more Events

```
Event ──→ Processor ──→ Command ──→ Event
```

Dependencies:
- Event triggers the Processor
- Processor OUTBOUND → Command INBOUND
- Command OUTBOUND → Event INBOUND

Specifications pattern:
- GIVEN: triggering event
- WHEN: processor runs
- THEN: command executed, resulting event(s)

Automations never connect directly to other events without going through a processor. They represent background processes: notifications, scheduled jobs, integrations.

## Dependency Rules

- All dependencies reference existing elements within the model
- No circular dependencies
- Every element has at least one dependency (input or output)
- Events flow forward — they feed read models and trigger automations
- Commands are the only way to produce new events

## Field Definitions

Each field has:
- name — camelCase, business-focused
- type — String, Boolean, Int, Long, Double, Decimal, Date, DateTime, UUID, Custom
- example — a concrete example value
- optional — whether the field can be absent (default: required)
- cardinality — Single or List

List fields contain multiple items of the same structure. Use subfields to describe the shape of list items.

## Naming Conventions

Use business terminology throughout. The model should read like a business process description, not a technical specification.

- "Register Owner" not "createOwnerRecord"
- "Owner Registered" not "ownerCreatedEvent"
- "Owner Profile" not "ownerDetailsDTO"
- "Visit History" not "visitListView"
