---
name: approval-tests
description: Writes approval tests (snapshot/golden master testing) for Python, JavaScript/TypeScript, or Java. Use when verifying complex output, characterization testing legacy code, testing combinations, or working with .approved/.received files.
---

STARTER_CHARACTER = 📸

# Approval Tests

## Philosophy

"A picture's worth 1000 assertions."

Approval tests verify complex output by comparing against a saved "golden master" file instead of writing individual assertions. You capture the output once, review it, approve it, and future runs compare against that approved snapshot.

You don't need to know the expected output upfront. Run the code, see what it produces, approve if correct. Whoever writes the code reviews the output.

**Use approval tests when:**
- Output is complex - instead of 20 assertions, one approval captures everything
- Characterizing legacy code - snapshot behavior, then refactor safely
- Combinatorial testing - test all input combinations in one approval
- Assertions would be tedious or brittle

**Use assertions when:**
- Simple values or specific edge cases
- Non-deterministic output that can't be scrubbed

## Core Workflow

```
1. Write test with verify(result)
2. Run test → FAILS (no .approved file yet)
3. Creates: TestName.approved.txt (empty) + TestName.received.txt (actual output)
4. Review .received file - is this correct?
5. YES → rename/copy .received to .approved
6. Run test again → PASSES
7. Commit .approved file to version control
```

**File naming convention:**
```
{TestClass}.{test_method}.approved.txt   ← commit this
{TestClass}.{test_method}.received.txt   ← gitignore this
```

**Critical rules:**
- `.approved` files ARE your test expectations - commit them
- `.received` files are temporary - add `*.received.*` to .gitignore
- Never edit `.approved` files by hand - always generate via test

When a test fails, a diff tool opens showing approved vs received. This is how you review changes. Reporters configure which diff tool to use.

## Core API Pattern

All languages follow the same pattern:

```
verify(result)                    # Basic string/object verification
verify_as_json(object)            # Objects as formatted JSON
verify_all(header, items)         # Collections with labels
verify_all_combinations(fn, inputs)  # All input combinations
```

Non-deterministic data (timestamps, GUIDs) must be scrubbed before verification.

## Key Techniques

- Scrubbers - replace values that change between runs (timestamps, UUIDs, random numbers, ports, paths) with stable placeholders like `[Date1]` or `guid_1`. Without scrubbing, tests pass locally but fail in CI.
- Inline approvals - expectations in source code instead of separate files. Avoids file proliferation for short output. Python uses docstrings, Java uses text blocks.
- Storyboard - capture state progressions over multiple frames. Each step appears in the diff, making it easy to see how state changes. For workflows, state machines, any object changing over time. Python/Java have classes; Node.js uses string building.
- Combinations - test all permutations of input parameters in one approval. Exhaustive coverage without writing separate tests for each case. For large sets, pairwise testing reduces millions of combinations to ~100.
- Multiple approvals per test - when one test method has multiple scenarios, each needs its own approval file. Parameter-based naming creates separate files per scenario.

See language references for implementation details.

## Language References

Detect language from project files, then read the appropriate reference for installation, quick start, core patterns, and links to deeper reference files:

- [python.md](python.md) - Python (`pyproject.toml`, `setup.py`, `requirements.txt`)
- [nodejs.md](nodejs.md) - JavaScript/TypeScript (`package.json`)
- [java.md](java.md) - Java (`pom.xml`, `build.gradle`)

## Anti-Patterns

- Don't write assertions for complex objects - use verify_as_json() instead
- Don't commit .received files - they're temporary
- Don't forget scrubbers for timestamps, GUIDs, random values
- Don't over-verify - one approval per logical behavior. Large approvals hide signal in noise; unrelated changes break tests.
- Don't hand-edit .approved files - always generate via test. Hand-edited files may not match actual code output.
- Don't use verify_all for structured data - use `verify_as_json({"items": items})`
- Don't mix approvals with assertions - the approval captures everything
- Don't call verify() multiple times without NamerFactory - each overwrites the same file

Flaky tests across environments usually means unscrubbed dynamic data (timestamps, UUIDs, ports, paths).
