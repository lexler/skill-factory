---
name: collaborative-design
description: Designs software features collaboratively through visual scenarios and iterative refinement. Use when designing features, tools, UIs, workflows, or any system before implementation.
---

STARTER_CHARACTER = 🎨

## Purpose

Stay in design mode. Resist jumping to implementation. Explore the problem space through concrete scenarios and visual examples before committing to solutions.

## Core Principle: Show, Don't Tell

Instead of describing what happens, show it:

```
Input:                              Expected:
  Fix bug                             Fix bug

  Co-authored-by: Claude...           Co-authored-by: Alice...
  Co-authored-by: Alice...
```

This applies everywhere - scenarios, test cases, UI states. Visual beats prose.

## Process

```
Problem → Research → Timeline → Scenarios → Decisions → Validation
    ↑__________________________________________________|
              (iterate freely)
```

### 1. Clarify the Problem
- What are we building? Why?
- What does success look like?
- What constraints exist?

### 2. Research (if needed)
- Analyze existing patterns (logs, code, APIs)
- Check real-world examples
- Validate assumptions about formats, timing, etc.

### 3. Think in Timeline
Once the problem is understood, walk through what happens in order:
- What happens first?
- Then what?
- What triggers the next step?

This uncovers unknowns. Each step becomes a scenario to explore.

### 4. Show Scenarios Visually
For each scenario, show the before/after or input/output:

**State changes:**
```
Before:                    After:
  [x] claude                 [x] claude
  [ ] alice                  [x] alice    ← added
```

**UI flows:**
```
> add github: isid█
  ┌─────────────────────┐
  │   isid              │
  │ → isidore           │  ← user selects
  └─────────────────────┘
         ↓
  [x] Llewellyn Falco <...>  ← added to list
```

**Data transformations:**
```
Input:                       Output:
  msg + Claude co-author       msg only
```

Use domain language, stay high-level.

### 5. Surface Options, Then Decide
Present 2-4 options with tradeoffs. Don't decide alone:
- "Option A does X, Option B does Y. Which direction?"
- Wait for input before proceeding

### 6. Validate Before Building
- POC for risky assumptions (API timing, format parsing)
- Visual test cases (input → expected output)
- Document findings

### 7. Document Decisions
Track what was decided and why. Update docs as design evolves.

## Anti-patterns

- Jumping to code before exploring the design space
- Describing scenarios in prose instead of showing them
- Showing one solution instead of options
- Asking multiple questions at once (show the whole list, then ask each one at a time)
- Making assumptions without checking (real data, real APIs)
- Skipping visuals for "obvious" cases
- Deciding without discussing tradeoffs

## When to Exit Design Mode

- Problem is understood
- Key scenarios walked through (shown visually)
- Major decisions made and documented
- Test cases exist as visual examples
- Risky assumptions validated

Then: implementation.
