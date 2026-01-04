---
name: bdd-with-approvals
description: Scannable BDD tests written in domain language. Use when doing BDD.
---

STARTER_CHARACTER = 🧪📋

# BDD with Approval Tests

## The Shift

Tests at implementation level are noisy and hard to validate, especially when AI writes them at super speeds and developer tries to guide it on higher level. 
BDD with approvals expresses behavior at domain level. The fixture file IS the spec. A human looks at it and immediately sees: correct or not.

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

## Implementation

**One-time per domain:**
1. Parser - extracts input from fixture format
2. Formatter - converts actual output to fixture format
3. Single test file discovers and runs all fixtures

Keep parser/formatter simple. Format should be close to natural representation.

## Format Design

**The question:** Can someone validate correctness in <5 seconds?

Design for human eyes, not machine parsing. Match the domain's natural representation—how you'd explain it on a whiteboard.

**Avoid:**
- Dense JSON (hard to scan)
- Single-line formats (no visual structure)
- Formats requiring mental parsing
- Over-engineering the parser

## Approved Logs

Turn production logs into tests by copying and fixing incorrect lines. Quick bug reproduction.

**Caveat:** Logs are for runtime observability, not test validation. Tying tests to log format creates coupling—log changes break tests. Use sparingly when logs happen to capture the behavior well.

See [references/approved-logs.md](references/approved-logs.md).
