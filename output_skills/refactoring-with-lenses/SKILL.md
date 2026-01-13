---
name: refactoring-with-lenses
description: Use when the user says 'do chupacabra refactoring'
---

# Refactoring with Lenses

STARTER_CHARACTER = 🔍

Refactor code through specific perspectives. Each lens reveals different improvements that general refactoring misses.

## Rules

- Ask one question at a time, wait for response
- Confirm file names and locations before starting
- Never change test code except renames following production changes
- All iteration files go in `playground/` (ensure it exists and is in `.gitignore`)

## Setup

1. Confirm target files/folder
2. Confirm test command works (all tests pass)
3. Create `refactoring.md` from [template.md](template.md)

## Per-Lens Process

For each unchecked lens in `refactoring.md`:

### 1. Read Lens

Read the linked lens file to understand the perspective.

### 2. Find Issues

Invoke `/refinement-loop`:
- Goal: find all issues visible through this lens
- Tag: `issues-{lens}` (e.g., `issues-naming`)
- Files: `playground/issues-{lens}-0.md` → `-1.md` → `-2.md`...
- Iterate until nothing new visible through this lens

### 3. Refactor

For each issue found:
1. Ensure tests pass
2. Make one refactoring
3. Ensure tests pass
4. Commit: `- r <refactoring>`

### 4. Feedback-Flip

Shift focus from implementing to evaluating.

Invoke `/refinement-loop` again:
- Goal: what did I miss in this lens?
- Tag: `missed-{lens}`
- Files: `playground/missed-{lens}-0.md` → `-1.md`...
- What could be better? What haven't I considered?

### 5. Refactor Missed Issues

Same process: test → change → test → commit

### 6. Update State

In `refactoring.md`:
- Mark lens complete
- Brief note of what changed (or "nothing found")
- Move to next lens
