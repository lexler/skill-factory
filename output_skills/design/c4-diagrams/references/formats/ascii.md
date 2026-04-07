# ASCII C4 Diagrams

Text-based diagrams that work everywhere: inline documentation, chat, code review comments, terminals. No rendering tools needed.

These illustrate conventions. Adapt the layout to fit your specific diagram.

## Box Drawing Characters

Use Unicode box-drawing characters, not `+`, `-`, `|`:

- Corners: `┌` `┐` `└` `┘`
- Walls: `│` (vertical), `─` (horizontal)
- Arrows: `▶` `◀` `▲` `▼` for arrowheads, `│` `─` for arrow shafts

Do NOT use `+` for corners or `|` for walls.

## Element Representation

### People

```
   .--.
   |  |
   '--'
  Person
 [Role/desc]
```

### Software Systems, Containers, Components

Boxes with name, type, technology, and description:

```
┌───────────────────────────────────┐
│    Internet Banking System        │
│       [Software System]           │
│                                   │
│  Allows customers to manage       │
│  their bank accounts              │
└───────────────────────────────────┘
```

```
┌───────────────────────────────────┐
│        API Application            │
│   [Container: Spring Boot]        │
│                                   │
│  Provides banking functionality   │
│  via JSON/HTTPS API               │
└───────────────────────────────────┘
```

### External Elements

Distinguish external elements with dashed borders or explicit labels:

```
┌ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ┐
  Mainframe System
  [Ext. Software System]

  Core banking functionality
└ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ┘
```

### Databases

```
┌───────────────────────────┐
│       Database            │
│ [Container: PostgreSQL]   │
│                           │
│ Stores account data       │
└───────────────────────────┘
```

Mark with `[Container: PostgreSQL]` — the type label is enough to convey it's a database.

## Relationships

### Horizontal arrows

```
┌─────────┐  "Makes API calls to"  ┌─────────┐
│   SPA   │───────────────────────▶│   API   │
│ [React] │      JSON/HTTPS        │[Spring] │
└─────────┘                        └─────────┘
```

### Vertical arrows

```
┌─────────┐
│   SPA   │
│ [React] │
└─────────┘
     │
     │ "Makes API calls to"
     │ JSON/HTTPS
     ▼
┌─────────┐
│   API   │
│[Spring] │
└─────────┘
```

### Arrow direction

Arrow points in the direction of the dependency or data flow. Label sits alongside the shaft, not at the head.

## Boundaries

Use labeled borders to group elements:

```
┌══════════════════════════════════════════════┐
║        Internet Banking System               │
│                                              │
│   ┌────────┐    ┌────────┐    ┌────────┐    │
│   │  SPA   │───▶│  API   │───▶│   DB   │    │
│   │ React  │    │ Spring │    │ PgSQL  │    │
│   └────────┘    └────────┘    └────────┘    │
│                                              │
└══════════════════════════════════════════════┘
```

## System Context Example

```
System Context diagram for Internet Banking System

   .--.                ┌──────────────────────────────┐
   |  |                │   Internet Banking System    │
   '--'  ──"Uses"────▶ │     [Software System]        │
 Customer              │                              │
                       │ Allows customers to manage   │
                       │ their bank accounts           │
                       └──────────┬───────────┬────────┘
                                  │           │
                "Gets account     │           │  "Sends emails via"
                 data from"      │           │   SMTP
                 XML/HTTPS        │           │
                                  ▼           ▼
              ┌ ─ ─ ─ ─ ─ ─ ─ ┐  ┌ ─ ─ ─ ─ ─ ─ ─ ┐
                Mainframe          E-mail System
                [Ext. System]      [Ext. System]
              └ ─ ─ ─ ─ ─ ─ ─ ┘  └ ─ ─ ─ ─ ─ ─ ─ ┘

Legend:
  ┌───┐  Internal system
  ┌ ─ ┐  External system
  ──▶    Relationship (direction of dependency/data flow)
```

## Validation

After creating any ASCII diagram, run the alignment checker to verify all boxes have consistent line widths:

```bash
uv run ${CLAUDE_SKILL_DIR}/scripts/check_ascii_alignment.py <diagram-file>
```

The script checks that every box opened with `┌` has its right wall `│` aligned on all lines down to the closing `└`. Fix any reported misalignments before presenting the diagram.

If the diagram is inline in a markdown file with code blocks, the script handles that too.

## Layout Guidelines

- Place the primary element or initiator at the top or left
- Flow generally top-to-bottom or left-to-right
- Keep relationship labels close to the arrow they describe
- Use consistent box widths within a diagram
- Every line inside a box must have `│` at the same column as `┐` — run the validator to catch drift
- For complex diagrams, prioritize readable flow over compact layout

## Title and Legend

Always include at the top:

```
System Context diagram for Internet Banking System

Legend:
  ┌───┐  Internal system
  ┌ ─ ┐  External system
  ──▶    Relationship (direction of dependency/data flow)
```
