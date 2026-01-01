# Nullables Skill Improvements

## Description Needs Better Trigger Words

Current: "Writes tests without mocks using James Shore's Nullables pattern. Use when writing tests and designing code for testability."

Missing keywords users would naturally say: "infrastructure", "HTTP client", "database", "file system", "clock", "dependency injection", "test doubles", "sociable tests", "flaky tests", "slow tests"

- [ ] Rewrite description to include specific trigger scenarios:
  - Testing code that calls HTTP APIs
  - Testing code that touches databases/files
  - Replacing mocks with something simpler
  - Making tests faster and less flaky

## SKILL.md Could Guide the Reader Better

Current order jumps around: When to Use → A-Frame → Core Pattern → Complete Example → Testing → Supporting Patterns → Anti-Patterns → References

A learner needs a clearer path:

- [ ] Consider reordering for progressive understanding:
  1. One-sentence essence (what problem this solves)
  2. Core Pattern (the "two factory methods" - this is the heart)
  3. Minimal working example (shorter than current CommandLine)
  4. When to use / When not to use
  5. A-Frame architecture (the "how to structure your code" context)
  6. Three supporting patterns (brief, with links)
  7. Anti-patterns (keep - these are valuable)
  8. References navigation

## A-Frame Section May Be Too Detailed for SKILL.md

The A-Frame architecture explanation is valuable but quite long (~40 lines with diagram). Someone just wanting to write their first Nullable may not need the full architecture upfront.

Options:
- [ ] Keep brief A-Frame intro in SKILL.md, move detailed explanation to `references/a-frame-architecture.md`
- [ ] Or: Keep as-is if you believe architecture understanding is prerequisite (discuss with Archie)

## Complete CommandLine Example is Long

The full CommandLine wrapper example is ~40 lines of code. The principle could be shown more concisely.

- [ ] Consider trimming to show just the essence (the two factory methods pattern)
- [ ] Move full implementation to a reference file if readers want complete picture
- [ ] Or: Add comment "// Full example - skim for the pattern, don't memorize"

## OutputListener Appears Without Explanation

Line 96 imports `OutputListener` but it's not explained until references. Reader might be confused.

- [ ] Add brief inline note: "OutputListener is a reusable helper - see output-tracking.md for the implementation"
- [ ] Or: Show a minimal inline version in the example

## Missing "Quick Start" Entry Point

No step-by-step for someone wanting to try immediately.

- [ ] Add a 5-step Quick Start section:
  1. Identify your infrastructure (HTTP, DB, etc.)
  2. Create a wrapper class with `create()` and `createNull()`
  3. Inject the dependency via constructor
  4. In tests, use `createNull()` with configured responses
  5. Track outputs to verify behavior

## Reference Navigation Could Be Clearer

The "Reference Files" section at the end lists files with descriptions but doesn't guide which to read first.

- [ ] Add reading order suggestion: "Start with infrastructure-wrappers.md if building your first Nullable"
- [ ] Or: Group references as "Read First" vs "When You Need It"

## Consider What's Truly Novel

Best practices: "Only add context Claude doesn't already have."

Claude already knows:
- What dependency injection is
- What test doubles are
- How to write factory methods

The skill should focus on what's **specific to Nullables**:
- The "embedded stub" insight (stubs in production code)
- Output tracking vs mock verification
- Parameters at caller's abstraction level
- Sociable vs solitary testing philosophy

- [ ] Review each section: Does this explain something Claude wouldn't already know?
- [ ] Trim explanations of general concepts (DI, factory pattern basics)
