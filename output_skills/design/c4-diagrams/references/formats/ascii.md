# ASCII C4 Diagrams

For inline diagrams in code, commit messages, terminal output, or anywhere rich rendering isn't available.

There is no standard ASCII format for C4. These conventions prioritize readability over decoration.

## Core Principle

ASCII diagrams are structured text with visual hints, not pixel art. Keep them simple. Boxes hold the name and technology — nothing else.

## Elements

Boxes with corners. Name on the first line, technology in brackets on the second:

```
┌──────────────────┐
│ API Application  │
│ [Spring Boot]    │
└──────────────────┘
```

People as simple labels in parentheses:

```
(Customer)
```

Do not draw multi-line ASCII person figures. Do not put descriptions inside boxes — the diagram is not the place for prose.

## Relationships

Horizontal arrows: `───▶` and `◀───`
Vertical arrows: `│` with `▼` or `▲` at the end

Labels on a separate line next to the arrow:

```
(Customer)
    │
    │  manages accounts
    ▼
┌──────────────────┐
│ Banking System   │
└──────────────────┘
```

## System Boundaries

A boundary box wrapping its containers. Every line within the box must be the same character width — verify this after drawing.

```
┌────────────────────────────────────────────┐
│ Internet Banking System                    │
│                                            │
│  ┌──────────┐   ┌────────┐   ┌──────────┐  │
│  │ Web App  │──▶│ SPA    │──▶│ API      │  │
│  │ [Spring] │   │ [React]│   │ [Spring] │  │
│  └──────────┘   └────────┘   └────┬─────┘  │
│                                   │        │
│                                   ▼        │
│                            ┌──────────┐    │
│                            │ Database │    │
│                            │[Postgres]│    │
│                            └──────────┘    │
└────────────────────────────────────────────┘
```

## Complete System Context Example

```
                  (Customer)
                      │
               manages accounts
                      │
                      ▼
             ┌────────────────┐
             │ Internet       │
             │ Banking System │
             └───────┬────────┘
                     │
            ┌────────┴────────┐
            │                 │
            ▼                 ▼
   ┌─────────────────┐  ┌───────────────┐
   │ Mainframe       │  │ Email System  │
   │ Banking System  │  │               │
   └─────────────────┘  └───────────────┘
```

## Complete Container Example

```
                       (Customer)
                        │     │
             visits     │     │  manages accounts
                        ▼     ▼
┌─────────────────────────────────────────────────────┐
│ Internet Banking System                             │
│                                                     │
│  ┌──────────┐    ┌─────────┐    ┌────────────────┐  │
│  │ Web App  │───▶│ SPA     │───▶│ API            │  │
│  │ [Spring] │    │ [React] │    │ [Spring Boot]  │  │
│  └──────────┘    └─────────┘    └───────┬────────┘  │
│                                         │           │
│                                         ▼           │
│                                  ┌────────────┐     │
│                                  │ Database   │     │
│                                  │ [Postgres] │     │
│                                  └────────────┘     │
└─────────────────────────────────────────────────────┘
                  │                    │
                  ▼                    ▼
        ┌─────────────────┐   ┌───────────────┐
        │ Mainframe       │   │ Email System  │
        │ Banking System  │   │               │
        └─────────────────┘   └───────────────┘
```

## Guidelines

- Use Unicode box-drawing characters: `┌`, `┐`, `└`, `┘` for corners, `─` for horizontal, `│` for vertical. Do not mix styles (no `+---+`, no `=====`).
- Use Unicode arrow characters: `▶` `◀` `▲` `▼` for arrowheads. Horizontal arrows: `───▶`. Vertical arrows: `│` with `▼` or `▲` at the end.
- After drawing a diagram, pipe it through `uv run ${CLAUDE_SKILL_DIR}/scripts/check_ascii_alignment.py` to verify all boxes are aligned. Fix any issues before presenting the diagram.
- Verify that vertical arrow lines (`│` and `▼`) align with the box edge they connect to. A `▼` arrow entering a box should land on a column inside the box's top edge, not off to the side.
- Put relationship labels on a separate line next to the arrow, not inline
- Use brackets for technology: `[Postgres]`, `[React]`
- Use parentheses for people: `(Customer)`, `(Admin)`
- Choose the layout direction (vertical or horizontal) that best fits the relationships being shown
- When a diagram gets too complex, simplify — drop less important relationships or split into multiple diagrams
- Do not include legends. The conventions are simple enough to be self-evident.
