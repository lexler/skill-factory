---
name: approval-tests
description: Writes approval tests (snapshot/golden master testing) for Python, JavaScript/TypeScript, or Java. Use when verifying complex output, characterization testing legacy code, testing combinations, or working with .approved/.received files.
---

# Approval Tests

## Philosophy

"A picture's worth 1000 assertions."

Approval tests verify complex output by comparing against a saved "golden master" file instead of writing individual assertions. You capture the output once, review it, approve it, and future runs compare against that approved snapshot.

**Use approval tests when:**
- Output is complex (JSON, XML, formatted text, multiple fields)
- Characterizing legacy code behavior before refactoring
- Testing combinations of inputs
- Assertions would be tedious or brittle

**Use assertions when:**
- Testing simple values
- Testing specific edge cases
- Output is non-deterministic and can't be scrubbed

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

## When Approval Tests Shine

**Complex objects** - Instead of asserting 20 fields individually, verify the whole object as JSON. One approval captures everything.

**Characterization tests** - Capture legacy behavior before refactoring. Run `verify(result)` to snapshot current behavior, then refactor with a safety net.

**Combinatorial testing** - Test all combinations of inputs with a single approval file. `verify_all_combinations()` generates every permutation.

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

**Don't write assertions for complex objects** - Use verify_as_json() instead of multiple assertions.

**Don't commit .received files** - They're temporary test artifacts.

**Don't forget scrubbers** - Timestamps, GUIDs, random values will cause random failures. Scrub them.

**Don't over-verify** - One approval per logical behavior, not one per line of output.

**Don't hand-edit .approved files** - Always generate through running tests.
