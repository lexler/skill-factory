---
name: approval-tests
description: Writes approval tests (snapshot/golden master testing) for Python, JavaScript/TypeScript, or Java. Use when verifying complex output, characterization testing legacy code, testing combinations, or working with .approved/.received files.
---

STARTER_CHARACTER = 📸

# Approval Tests

## Philosophy

"A picture's worth 1000 assertions."

Approval tests verify complex output by comparing against a saved "golden master" file instead of writing individual assertions. You capture the output once, review it, approve it, and future runs compare against that approved snapshot.

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

## Core API Pattern

All languages follow the same pattern:

```
verify(result)                    # Basic string/object verification
verify_as_json(object)            # Objects as formatted JSON
verify_all(header, items)         # Collections with labels
verify_all_combinations(fn, inputs)  # All input combinations
```

Non-deterministic data (timestamps, GUIDs) must be scrubbed before verification.

## Language References

Detect language from project files, then read the appropriate reference:

**Python** (`pyproject.toml`, `setup.py`, `requirements.txt`)
→ [python.md](python.md)

**JavaScript/TypeScript** (`package.json`)
→ [nodejs.md](nodejs.md)

**Java** (`pom.xml`, `build.gradle`)
→ [java.md](java.md)

## Cross-Language Patterns

- [Combination Testing](references/patterns/combinations.md)
- [Testing Patterns](references/patterns/testing-patterns.md)

## Anti-Patterns

- Don't write assertions for complex objects - use verify_as_json() instead
- Don't commit .received files - they're temporary
- Don't forget scrubbers for timestamps, GUIDs, random values
- Don't over-verify - one approval per logical behavior
- Don't hand-edit .approved files - always generate via test
- Don't use verify_all for structured data - use `verify_as_json({"items": items})`
- Don't mix approvals with assertions - the approval captures everything
