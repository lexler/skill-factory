---
name: align
description: Presents a proposed approach in progressive confirmable chunks with recommended decisions and alternatives. Use when aligning on a design, plan, or technical approach before implementation.
argument-hint: [file|folder]
---

STARTER_CHARACTER = 🎯

## Goal

Synchronize the mental model between you and the user before implementation begins. Discrepancies found during implementation are expensive — find them now while changes are free. Your job is to make your thinking visible so the user can spot where your understanding diverges from theirs.

## Core Principle

Propose, don't ask. Think first, then present your thinking for confirmation. The user's job is to spot divergence and course-correct, not to generate the approach.

## Flow — Zoom In

Each level deepens understanding. Confirm before going deeper.

```
Goal → Big Picture → Straightforward Details → Non-obvious Decisions (one by one)
```

### 1. Goal

State what you understand the goal to be and why it matters. A sentence or two. This catches the deepest misalignment — if you're solving the wrong problem, nothing else matters.

Confirm with AskUserQuestion before going deeper.

### 2. Big Picture

Present the overall shape of the approach: how do the pieces relate, what's the high-level flow. ASCII diagram. A few sentences, not a page.

Confirm with AskUserQuestion before going deeper.

### 3. Straightforward Details

Decisions where there's really only one reasonable approach. No ⭐/❌ needed since there are no real alternatives. The user confirms or flags exceptions.

Group items by topic. Anchor each group with an ASCII diagram — not just for file structures, but for any group: roles and their responsibilities, control flow, communication between components. The diagram is what makes a group scannable. Present one group at a time, confirm, move to the next group.

Each item: one line stating the decision. Save the "why" — it's obvious.

### 4. Non-obvious Decisions

Decisions with real tradeoffs, multiple valid approaches, or where your recommendation might surprise the user.

First, present a brief index of what's coming — just the problem titles, no recommendations. This lets the user see the scope.

Then walk through each one (or small related groups) with:
- The problem: what is being decided, why it matters
- ⭐ Recommended approach with rationale
- ❌ Alternatives considered with why they were rejected
- ASCII diagram if the item involves structure or flow

Confirm each with AskUserQuestion before moving to the next.

When the user rejects a recommendation, check whether downstream items are affected. If so, flag which ones need revisiting.

## After Corrections

When the user corrects something, re-present the full updated version (diagram, section, whatever was corrected) before asking to proceed. Don't just show the delta. The user needs to see the corrected whole — it often triggers additional corrections they wouldn't have noticed otherwise.

## Anti-patterns

- Jumping to detail-level decisions before establishing the big picture
- Flat-listing many decisions without grouping by topic (user loses context)
- Presenting the full detailed analysis for every item (save depth for non-obvious items only)
- Asking open-ended questions instead of proposing (the user invoked this to see YOUR thinking)
- Presenting a group of decisions without a visual anchor (diagram makes it scannable)
- Offering redundant AskUserQuestion options that split the same intent
- Continuing with pre-planned items after a redirect without reconsidering downstream impact
