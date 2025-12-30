---
name: refactoring
description: Refactoring process. Invoke immediately when user or document mentions refactoring, or proactively when code gets too complex or messy.
---

# Refactoring Production Code

STARTER_CHARACTER = 🟣

When starting, announce: "🟣Using REFACTORING skill".

Work autonomously as much as possible. Start with the simplest thing or file and proceed to the more complex ones.
Search for ./test.sh script in the root and run it for all tests on every refactoring. 
If it's not present, create it and ensure it runs all tests. 
Never change test code in this process. 

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

## Final Evaluation
- Say "🔍Evaluating refactoring"
- Carefully look at existing code
- Think about problem space:
  - What is the purpose of the code? Express it as both fully and succinctly as possible, say 'CODE PURPOSE: [CODE_PURPOSE]', replace CODE_PURPOSE with your summary.
  - Does the actual code express that purpose in a way that is clear to see and understand for the reader?
  - Look for opportunities to use domain language over implementation details in both explanations and names. Express what things ARE and why they exist, instead of how they're implemented.
  - Think about applying this on different layers of abstraction: the whole file, methods, or parts of methods
  - Look for methods where levels of abstraction are mixed: too much detail vs more abstract blocks that express the meaning. Can you see an opportunity to raise the level of abstraction in the more detailed sections?
  - Think about the list of refactorings that you could implement to make the code better from that perspective
  - If you identified improvements, follow the same refactoring process to implement them, be sure to commit and run tests as before, performing simplest refactoring first.

## Language-Specific

For Java: See [references/java.md](references/java.md)
