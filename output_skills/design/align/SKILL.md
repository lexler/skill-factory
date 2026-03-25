---
name: align
description: Presents a proposed approach in progressive confirmable chunks with recommended decisions and alternatives. Use when aligning on a design, plan, or technical approach before implementation.
argument-hint: [file|folder]
---

STARTER_CHARACTER = 🎯

## Goal

Synchronize the mental model between you and the user before implementation begins. Discrepancies found during implementation are expensive — find them now while changes are free. Your job is to make your thinking visible so the user can spot where your understanding diverges from theirs.

## Core Principle

Propose, don't ask. Think first, then present your full thinking upfront. The user's job is to spot divergence and course-correct, not to generate the approach.

## Flow

```
Read input → Think fully → Present overview → User flags items → Drill into flagged
```

- Read the input context
- Think through the full approach internally
- Present a concise overview of the entire proposed approach with your default recommendation for each item
- Ask the user which items they want to discuss — everything else is accepted as-is
- Drill into only the flagged items

## The Overview

The overview is the core of this skill. It's a scannable summary of every decision and step, each with your default recommendation. The user should be able to read it in under a minute and say "looks good" or "let's talk about 2 and 5."

Each item in the overview:
- Briefly states the problem or decision (what is being decided and why it matters)
- ⭐ Your default recommendation with brief rationale
- One line, maybe two — not a full analysis

Include an ASCII diagram of the overall structure or flow when it helps comprehension.

After presenting the overview, ask the user which items (if any) they want to discuss. Use AskUserQuestion.

## Drilling In

For each flagged item, expand with:
- ⭐ Recommended approach with fuller rationale
- ❌ Alternatives considered with why they were rejected
- ASCII diagram if the item involves structure or flow

Confirm the item with AskUserQuestion before moving to the next flagged item.

When the user rejects a recommendation, check whether downstream items in the overview are affected. If so, flag which ones need revisiting.

## Anti-patterns

- Jumping to recommendations without stating the problem (user needs to understand WHAT before HOW)
- Forcing the user through N confirmation rounds when most items are fine (overview-then-flag avoids this)
- Presenting the full detailed analysis for every item upfront (save depth for flagged items only)
- Asking open-ended questions instead of proposing (the user invoked this to see YOUR thinking)
- Skipping ASCII diagrams for structural or flow topics
- Continuing with pre-planned details after a redirect without reconsidering downstream impact
