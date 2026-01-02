# Nullables Skill Improvement Suggestions


## Missing Patterns from James Shore

- [ ] **Add "Fake It Once You Make It" pattern** - High-level code delegates to Nullable dependencies rather than implementing its own stubs. This is the composition pattern that makes the whole system work. Currently missing entirely.

- [ ] **Add "Grow Evolutionary Seeds" guidance** - Start with hardcoded implementations, incrementally replace with infrastructure wrappers. Important for greenfield projects. Currently missing.

- [ ] **Add "Paranoic Telemetry" principle** - Assume everything fails; test error handling, timeouts, and failure paths extensively. The skill mentions error testing but doesn't emphasize this mindset.

- [ ] **Emphasize "Narrow Integration Tests" more** - Currently mentioned briefly in test-patterns.md. These are critical for verifying real paths work. Consider promoting to SKILL.md or making more prominent.

- [ ] **Add "Collaborator-Based Isolation"** - Use dependencies' own tracking methods in assertions rather than hardcoding expectations. Subtle but powerful pattern.

---

## Structure & Length

- [ ] **Move A-Frame architecture to references** - The A-Frame section is ~40 lines. Someone writing their first Nullable doesn't need this upfront. Keep brief intro ("Logic and Infrastructure are peers, coordinated by Application"), link to `references/architecture/a-frame.md`.

- [ ] **Simplify the CommandLine example** - Current example is ~40 lines. The core pattern (two factory methods) could be shown in ~15 lines. Move full example to references.

- [ ] **Add a Quick Start section** - 5 steps for someone wanting to try immediately:
  1. Identify your infrastructure dependency
  2. Create wrapper with `create()` and `createNull()`
  3. Inject via constructor
  4. Use `createNull()` in tests with configured responses
  5. Track outputs to verify behavior

- [ ] **Explain OutputListener before using it** - Line 96 imports it without explanation. Add inline note or show minimal inline version.

---

## Reference Navigation

- [ ] **Add reading order suggestion** - "Start with infrastructure-wrappers.md if building your first Nullable, then output-tracking.md"

- [ ] **Group references by purpose**:
  - "Building Your First Nullable": infrastructure-wrappers.md, output-tracking.md
  - "Advanced Patterns": configurable-responses.md, embedded-stubs.md
  - "Architecture": a-frame.md, logic-sandwich.md, event-driven.md
  - "Migration": migration.md

---

## Language Coverage

- [ ] **Add Python examples** - All examples are JavaScript. Python is a common testing context. Show at least one pattern in Python (Clock or HttpClient).

- [ ] **Add TypeScript annotations** - If keeping JS, at least mention TypeScript patterns or note "works identically in TypeScript".

---

## Missing Content

- [ ] **Add "Signs You're Over-Engineering" section** - When Nullables are overkill:
  - Wrapping already-testable code (pure functions, immutable data)
  - Simple enough to use real thing (in-memory SQLite, temp files)
  - Stub becoming as complex as the real thing

- [ ] **Add quick reference/cheat sheet** - Pattern names, when to use, 1-line examples. Could be `references/cheat-sheet.md`.

- [ ] **Add "Nullable vs Mock" comparison table** - Side-by-side showing same test written both ways.

---

## Anti-Patterns

- [ ] **Expand "Constructor connects to infrastructure"** - Add the Zero-Impact Instantiation term and link to James Shore's principle. This is a foundational concept.

- [ ] **Add "Stub lives in test file" anti-pattern** - Stubs should be embedded in production code, not scattered in test files.

- [ ] **Add "Mocking your own code" anti-pattern** - Only wrap third-party/infrastructure code. Your own classes should just be Nullable directly or have their dependencies nulled.

---

## Conciseness Review

- [ ] **Remove explanations Claude already knows**:
  - "Nullables are production code. They can power real features like dry-run mode..." - This insight is novel, keep.
  - "External I/O is slow and flaky..." - Claude knows this. Could trim.
  - Full factory method pattern explanation - Claude knows factory patterns. Focus on what's specific: `createNull()` takes caller-level abstractions.

- [ ] **Check for repeated concepts** - A-Frame architecture explained in SKILL.md and references. Consolidate.

---

## Test Patterns Reference

- [ ] **Add "Signature Shielding" to SKILL.md** - This pattern is in test-patterns.md but is valuable enough to mention in main skill (helper functions encapsulate test setup).

- [ ] **Add Behavior Simulation summary** - Event-driven.md has good content but SKILL.md barely mentions it. Add brief pointer.

---

## Existing Suggestions (from nullable_todo.md)

The following were already identified and should still be addressed:

- [ ] Reorder for progressive understanding (from nullable_todo.md)
- [ ] Review each section: Does this explain something Claude wouldn't already know? (from nullable_todo.md)
- [ ] Trim explanations of general concepts (from nullable_todo.md)
