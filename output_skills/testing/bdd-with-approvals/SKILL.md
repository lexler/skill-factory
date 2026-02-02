---
name: bdd-with-approvals
description: Scannable BDD tests written in domain language. Use when doing BDD.
---

# BDD with Approval Tests

## The Problem

Specifications live in documents. They drift from reality because nothing enforces them.

Tests verify implementation. Written after code, they document what IS, not what SHOULD BE. They're noisy. You can't glance at them and quickly validate correctness.

You need an artifact that:
- Captures expected behavior before code exists
- Stays in sync because it's executable
- A human can validate at a glance

## Executable Specifications

The fixture file IS that artifact. Write it BEFORE implementation.

Think through scenarios by creating approval files. Describe expected behavior in domain language. Implementation is driven by making these specs pass. Specs stay executable, never go stale.

A human looks at the fixture and immediately sees: correct or not. No translation between "spec" and "test". They're the same artifact.

For the approval testing technique itself (verify, scrubbers, combinations), see `/approval-tests`. For nulled infrastructure in system tests, see `/nullables`.

## Approved Fixtures

Test files combining input and expected output in a format designed for human validation.

```
## Input
(context, parameters, initial state)

## Output
(expected results, side effects, final state)
```

Test runner reads fixtures, executes code, compares output. Adding test cases = adding files, not code.

**Design the format for YOUR domain:**
- Grid/spatial problems → ASCII art
- Transformations → before/after
- Workflows → step sequences with results
- API interactions → request/response pairs

See [references/approved-fixtures.md](references/approved-fixtures.md) for examples.

## Format Design

**The question:** Can someone validate correctness in <5 seconds?

Design for human eyes, not machine parsing. Match the domain's natural representation. How you'd explain it on a whiteboard.

**What makes formats scannable:**
- Columnar layouts with visual alignment
- Consistent structure across all cases
- Whitespace that groups related elements

**Avoid:**
- Dense JSON (hard to scan)
- Single-line formats (no visual structure)
- Formats requiring mental parsing

## Implementation

**One-time per domain:**
1. Parser - extracts input from fixture format
2. Formatter (printer) - converts actual output to fixture format
3. Single test file discovers and runs all fixtures

Keep parser/formatter simple. Format should be close to natural representation.

## Approved Logs

Turn production logs into tests by copying and fixing incorrect lines. Quick bug reproduction.

**Caveat:** Logs are for runtime observability, not test validation. Tying tests to log format creates coupling. Log changes break tests. Use sparingly when logs happen to capture the behavior well.

See [references/approved-logs.md](references/approved-logs.md).
