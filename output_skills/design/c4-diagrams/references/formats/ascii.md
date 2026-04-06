# ASCII C4 Diagrams

For inline diagrams in code, commit messages, terminal output, or anywhere rich rendering isn't available.

There is no standard ASCII format for C4. These conventions produce readable diagrams in monospace text.

## Element Notation

People:
```
  O
 /|\   Customer
 / \
```

Or simplified:
```
[Customer]
```

Software systems and containers as labeled boxes:
```
┌──────────────────────┐
│   Banking System     │
│   (Software System)  │
└──────────────────────┘
```

With technology:
```
┌──────────────────────┐
│   API Application    │
│   [Spring Boot]      │
└──────────────────────┘
```

Databases as cylinders or labeled boxes:
```
┌──────────────────────┐
│   Database           │
│   [PostgreSQL]       │
│   (datastore)        │
└──────────────────────┘
```

## Relationships

Use arrows with labels:
```
──────────────>   directional
── "label" ──>    with description
<─────────────>   bidirectional
```

## System Boundary

Use a dashed or double-line box:
```
┌ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ┐
  Internet Banking System
│                                       │
  ┌──────────┐    ┌──────────────────┐
│ │ Web App  │    │ API Application  │  │
  │ [React]  │───>│ [Spring Boot]   │
│ └──────────┘    └────────┬─────────┘  │
                           │
│                          ▼            │
                  ┌──────────────────┐
│                 │ Database         │  │
                  │ [PostgreSQL]     │
│                 └──────────────────┘  │
└ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ┘
```

## Complete System Context Example

```
                    [Customer]
                        │
                        │ manages accounts
                        ▼
           ┌────────────────────────┐
           │    Internet Banking    │
           │    System              │
           └───────────┬────────────┘
              ┌────────┼────────┐
              │                 │
              ▼                 ▼
┌──────────────────┐  ┌──────────────────┐
│ Mainframe        │  │ Email System     │
│ Banking System   │  │                  │
└──────────────────┘  └──────────────────┘
```

## Complete Container Example

```
                         [Customer]
                          │     │
               visits     │     │  manages accounts
                          ▼     ▼
┌ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ┐
  Internet Banking System
│                                                   │
  ┌────────────┐   ┌───────────┐   ┌────────────┐
│ │ Web App    │──>│ SPA       │──>│ API        │  │
  │ [Spring]   │   │ [React]   │   │ [Spring]   │
│ └────────────┘   └───────────┘   └─────┬──────┘  │
                                         │
│                                        ▼         │
                                ┌──────────────┐
│                               │ Database     │   │
                                │ [PostgreSQL] │
│                               └──────────────┘   │
└ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ┘
          │                          │
          ▼                          ▼
┌──────────────────┐    ┌──────────────────┐
│ Mainframe        │    │ Email System     │
│ Banking System   │    │                  │
└──────────────────┘    └──────────────────┘
```

## Guidelines

- Use box-drawing characters (┌ ─ ┐ │ └ ┘ ├ ┤ ┬ ┴ ┼) for clean lines
- Fall back to +, -, |, and = if box-drawing characters aren't available
- Keep diagrams under ~80 columns wide when possible
- Vertical flow (top to bottom) is easiest to read in terminals
- Label relationships on or near the arrow lines
- Use brackets for technology: `[PostgreSQL]`, `[React]`
- Use parentheses for element type: `(datastore)`, `(external)`
