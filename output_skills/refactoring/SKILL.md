---
name: refactoring
description: Refactoring process. Always follow when refactoring, simplifying and improving code. Always follow when user or document mentions refactoring.
---

# Refactoring Production Code

STARTER_CHARACTER = 🟣

When starting, announce: "🟣Using REFACTORING skill".

Ask one question at a time and wait for a response.
Search for ./test.sh script in the root and run it for all tests on every refactoring. If it's not present, create it and ensure it runs all tests. 
Never change test code in this process. Work autonomously as much as possible.

## Process

Confirm the relevant test file and its location before starting.

For each refactor:
1. Ensure all tests pass
2. Choose and perform the simplest possible refactoring (one at a time)
3. Ensure all tests pass after the change
4. Commit each successful refactor with the message format: "- r <refactoring>" (quotes must include the - r).
5. Provide a status update after each refactor

If a refactor fails three times or no further refactoring is found, pause and check with the user.

## Code Style

Prefer self-explanatory, readable code over comments.

- Use functional helper methods for clarity
- Remove comments and dead code
- Extract paragraphs into methods
- Use better variable names
- Remove unused imports
- Remove unhelpful local variables

## Language-Specific

For Java: See [references/java.md](references/java.md)
