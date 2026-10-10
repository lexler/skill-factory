---
name: align
description: Aligns on a design or plan before implementation by proposing it in confirmable chunks, with recommended decisions and alternatives.
---

STARTER_CHARACTER = 🎯

## Goal

Align your mental model with the user's before implementation begins. Divergence found during implementation is expensive, so surface it now while changes are free.

Think first, then propose the approach. It's easier to complain than to explain: a user looking at a concrete, scannable proposal spots what's wrong early and corrects you before you build the wrong thing.

## Language

Write the shortest message that is clear on the first read, using plain English words and complete sentences.

## Flow: zoom in

Start from high level and go lower. Zoom in one level at a time:

```
Goal → Big Picture → Straightforward Details → Non-obvious Decisions (one by one)
```

### 1. Goal

State what you understand the goal to be and why it matters. Keep it to a sentence or two. This catches the deepest misalignment, because if you're solving the wrong problem, nothing else matters.

Confirm with the user that the goal is right before moving on.

### 2. Big picture

Present the overall shape of the approach: how do the pieces relate, what's the high-level flow. Use an ASCII diagram and a few sentences.

Confirm with the user before going deeper.

### 3. Straightforward details

Decisions where there's only one reasonable approach.

Group decisions where there's commonality that helps understand. 
Organize the group around meaningful differences. 

Include specific details when they change what the user is agreeing to, otherwise stay on higher level.

Use short prose or bullets for simple choices. Use an ASCII diagram
when seeing a relationship, structure, or flow makes the choice clearer.

Describe the resulting behavior with complete statements.

### 4. Non-obvious decisions

Decisions with real tradeoffs, multiple valid approaches, or where your recommendation might surprise the user.

First, present a brief index of what's coming, staying on high level: the problem titles only, without recommendations. This lets the user see the scope.

Then walk through each one (or small related groups) with:
- The problem: what is being decided, why it matters
- ⭐ Recommended approach with rationale
- ❌ Alternatives considered with why they were rejected
- ASCII diagram if the item involves structure or flow

Confirm each with a question before moving to the next.

## When the user corrects you

Re-present the full updated version of whatever was corrected (goal, diagram, group, decision) before asking to proceed. Seeing the whole again often surfaces corrections the user would miss in a delta.

After any correction or rejected recommendation, check which downstream items it affects. Flag them and rethink them before going on.
