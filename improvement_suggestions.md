# Nullables Skill Improvement Suggestions


## Missing Patterns from James Shore

- [x] **Add "Fake It Once You Make It" pattern** - Added as 4th supporting pattern + detailed in infrastructure-wrappers.md

- [x] **Add "Grow Evolutionary Seeds" guidance** - Added in Getting Started section

- [x] **Add "Paranoic Telemetry" principle** - Added in Testing Philosophy section

- [x] **Emphasize "Narrow Integration Tests" more** - Expanded in Testing Techniques with explanation of why they matter

- [x] **Add "Collaborator-Based Isolation"** - Added to Testing Philosophy section

---

## Structure & Length

- [x] **Move A-Frame architecture to references** - Condensed in SKILL.md, detailed version in `references/architecture/a-frame.md`

- [ ] **Simplify the CommandLine example** - Current example is ~40 lines. The core pattern (two factory methods) could be shown in ~15 lines. Move full example to references.

- [x] **Add a Quick Start section** - Added "Getting Started" section with greenfield and existing codebase guidance

- [x] **Explain OutputListener before using it** - Improved inline comment to clarify purpose

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

- [x] **Add "Signs You're Over-Engineering" section** - Added after Anti-Patterns

- [x] ~~**Add quick reference/cheat sheet**~~ - Deleted; redundant with SKILL.md

- [x] **Add "Nullable vs Mock" comparison table** - Added side-by-side code example in intro

---

## Anti-Patterns

- [x] **Expand "Constructor connects to infrastructure"** - Added Zero-Impact Instantiation term and link

- [x] **Add "Stub lives in test file" anti-pattern** - Added to Anti-Patterns section

- [x] **Add "Mocking your own code" anti-pattern** - Added to Anti-Patterns section

---

## Conciseness Review

- [ ] **Remove explanations Claude already knows**:
  - "Nullables are production code. They can power real features like dry-run mode..." - This insight is novel, keep.
  - "External I/O is slow and flaky..." - Claude knows this. Could trim.
  - Full factory method pattern explanation - Claude knows factory patterns. Focus on what's specific: `createNull()` takes caller-level abstractions.

- [x] **Check for repeated concepts** - A-Frame consolidated (condensed in SKILL.md, details in reference)

---

## Test Patterns Reference

- [x] **Add "Signature Shielding" to SKILL.md** - Added in Testing Techniques section

- [x] **Add Behavior Simulation summary** - Added in Testing Techniques section

---

## Existing Suggestions (from nullable_todo.md)

The following were already identified and should still be addressed:

- [x] Reorder for progressive understanding - Testing patterns merged into Testing with Nullables, Getting Started section added
- [ ] Review each section: Does this explain something Claude wouldn't already know? (from nullable_todo.md)
- [ ] Trim explanations of general concepts (from nullable_todo.md)
