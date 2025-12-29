---
name: tdd
description: Follows test-driven development process when writing code. Use when implementing features with TDD, writing tests first, or when user mentions TDD or test-driven development.
---

# Test-Driven Development

When starting, announce: "TDD mode: [auto|human]"

MODE (user specifies, default: auto)
- auto: fully automated, no stops
- human: wait for confirmation at key points

STARTER_CHARACTER = 🔴 for red test, 🌱 for green, 🌀 when refactoring, always followed by a space

## Core Rules

1. Write only one test at a time - focus on the simplest, lowest-hanging fruit test
2. Predict failures - State what we expect to fail before running tests
3. Two-step red phase:
   - First: Make it fail to compile (class/method doesn't exist)
   - Second: Make it compile but fail the assertion (return wrong value)
4. Minimal code to pass - Just enough to make the test green
5. No comments in production code - Keep it clean unless specifically asked
6. Run all tests every time - Not just the one you're working on
7. Refactor at the first opportunity when the tests are green
8. Test behavior, not implementation - check responses or state, not method calls
9. Push back when something seems wrong or unclear

## Test Planning

1. Think about what the code you want to write should do
2. Plan tests as single-line `[TEST]` comments. Example:
   ```
   [TEST] Zero plus a number is equal to that number
   [TEST] Add two positive numbers
   [TEST] Add two negative numbers
   [TEST] Adds a negative and a positive number
   [TEST] Division by zero is not allowed
   ...
   ```
3. Check completeness - consider [ZOMBIES](references/zombies.md) and any other edge cases. Missing anything?
4. If MODE is human, wait for confirmation after test planning

## Implementation Phase

1. Replace the next comment with a failing test
2. Test should be in format given-when-then (do not add as comments), with empty line separating them
3. Predict what will fail
4. Run tests, see compilation error (if testing something new)
5. Add minimal code to compile
6. Predict assertion failure
7. Run tests, see assertion failure
8. Add minimal code to pass
9. Predict whether the tests will pass and why. Run tests, see green
10. Simplify. Look at the code you just added, only the change you added. Did you accidentally add too much code? Can you take something out with having the tests still passing? Make a list of simplifications.
    - If there's simplifications left, take one step to simplify.
    - Run tests, make sure everything is still green
    - Repeat until you cannot see any way to simplify any further without affecting existing functionality and other tests.
11. Refactor.
    - Think about things that can be improved about the code we are working on that is already written without affecting the functionality at all. How do we get the code more expressive? Cleaner? Simpler? Make a todo list of things to improve.
    - Say `🧹 Starting refactoring stage` and output a list of refactorings you're planning to do
    - Implement the simplest refactoring from the list.
    - Run tests. If they are passing, mark that refactoring as done and move on to the next one. Otherwise, undo the change and try again.
    - If there's still refactorings to implement, repeat. Otherwise say "🧹 Refactoring complete" and continue
12. Go to step 1 for the next [TEST] comment. Repeat until all planned tests are passing.

## Final Evaluation

1. Analyze the code written and think about the tests that we might have missed.
2. If there are any gaps in the tests, start the process for the missing tests from the beginning, starting from test comments then following the process flow until done
3. Is anything still hardcoded in the code that shouldn't be? Fix it, analyze test gaps and go back to previous stages if needed.
4. Analyze code expressiveness and quality. If there's anything you can see to improve, go to refactoring phase.
