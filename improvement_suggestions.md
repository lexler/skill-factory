# Nullables Skill Improvement Suggestions

Analysis based on:
- Skill creation best practices from `docs/knowledge/anthropic-skill-docs/`
- James Shore's original article and example repositories
- The existing `nullable_todo.md` suggestions

---

## The Core Insight Appears Too Late

**Problem:** The most powerful framing from Shore - "production code with an off switch" - appears in line 10, buried after the header. This is THE insight that makes Nullables click.

But even Shore's framing is missing the WHY: external communication is slow, flaky, and unreliable. We want tests that run in milliseconds and never fail because a server is down. Fast tests = fast feedback loops = better code.

**Suggested opening:**
```
Nullables are production code with an "off switch" for external communication.
External I/O is slow and flaky - we want tests that run instantly and never
fail due to network issues. Fast tests mean fast feedback loops.
```

**Suggestion:** Lead with the insight AND the motivation, not the when-to-use rules.

- [ ] Move "production code with an off switch" to be the first sentence after the header
- [ ] Consider opening with: "Nullables are production code with an 'off switch' for infrastructure. No mock libraries. Real code paths in tests."

---

## A-Frame Architecture is Detailed but Premature

**Current:** 40+ lines on A-Frame architecture before the core pattern.

**Problem:** Someone wanting to write their first Nullable doesn't need the full architectural context. A-Frame is important but is "pull knowledge" (read when needed) not "push knowledge" (must know first).

Best practices say: *"SKILL.md serves as an overview that points Claude to detailed materials as needed."*

**Options:**
- [ ] Option A: Keep brief A-Frame summary in SKILL.md (2-3 lines), move detailed explanation to `references/architecture/a-frame.md`
- [ ] Option B: Move A-Frame section AFTER the core pattern and examples, making it "additional context" rather than prerequisite

---

## Core Pattern Section is Strong but Could Be Leaner

The "Two Factory Methods" section is the heart of the skill. It's good but the Clock example could be tighter.

- [ ] Consider trimming the StubbedDate class from the example (it's an implementation detail that distracts from the pattern)
- [ ] Add a one-liner after the example emphasizing: "That's it. Real dependency in `create()`, stubbed dependency in `createNull()`"

---

## CommandLine Example is Verbose for SKILL.md

**Current:** ~40 lines for a complete CommandLine wrapper.

**Problem:** Full implementations belong in references. SKILL.md should show the essence.

Best practices: *"Keep SKILL.md body under 500 lines for optimal performance."* (Current is ~274, so not critical, but trimming helps focus.)

- [ ] Trim to show just the skeleton pattern (create/createNull/constructor)
- [ ] Move complete CommandLine to `references/building/infrastructure-wrappers.md` (already has FileSystem example)
- [ ] Or: Add framing like "// Full example - the pattern is lines 6-14"

---

## OutputListener Appears Without Introduction

**Line 96:** `import { OutputListener } from "./output_listener.js";`

**Problem:** The reader encounters OutputListener in the example before understanding what it is. The explanation comes later in "Three Supporting Patterns."

- [ ] Add a brief inline comment: `// OutputListener is a reusable helper - see output-tracking.md`
- [ ] Or: Reorder so "Output Tracking" brief intro appears before the CommandLine example

---

## Missing "Quick Start" For Immediate Action

**Problem:** No step-by-step for someone wanting to try right now.

Best practices: *"Include both what the Skill does and when to use it"* - but also HOW to start.

- [ ] Add a 5-step Quick Start after the intro:
  ```
  ## Quick Start
  1. Identify your infrastructure (HTTP, DB, files, clock)
  2. Create a wrapper class with `create()` and `createNull()` factories
  3. Inject the wrapper via constructor
  4. In tests, use `createNull()` with configured responses
  5. Call `trackOutput()` to verify what was written
  ```

---

## Reference Navigation Lacks Reading Order

**Current:** The "Reference Files" section at the end lists files with descriptions but doesn't guide which to read first.

**Suggestion:**
- [ ] Add reading order guidance: "Start with `infrastructure-wrappers.md` to build your first Nullable"
- [ ] Or: Group as "Start Here" vs "Deep Dives"

---

## Missing Key Terminology from Shore's Pattern Language

Shore's article defines specific terms that the skill sometimes uses different names for:

| Shore's Term | Current Skill | Status |
|--------------|--------------|--------|
| Narrow Tests | (implied) | Missing explicit mention |
| State-Based Tests | Mentioned in anti-patterns | Could be more prominent |
| Overlapping Sociable Tests | test-patterns.md | Consider adding to SKILL.md |
| Signature Shielding | test-patterns.md | Good, keep there |
| Zero-Impact Instantiation | "Constructor does work" anti-pattern | Same concept, different name |
| Parameterless Instantiation | infrastructure-wrappers.md | Good |
| Narrow Integration Tests | test-patterns.md | Good |
| Behavior Simulation | event-driven.md as `simulateX()` | Good |

- [ ] Consider adding a terminology box linking to Shore's pattern language
- [ ] Or: Add brief definitions for "narrow tests" and "state-based tests" since these are foundational

---

## The Tradeoff Discussion is Missing

**Problem:** Shore explicitly discusses a key tradeoff: *"do you want that in your production code?"* - referring to embedded stubs and factory methods.

This is honest guidance that helps users make informed decisions.

- [ ] Add a brief "Tradeoffs" section:
  ```
  ## Tradeoffs

  Nullables put test-supporting code in production. The factory methods and embedded stubs ship with your app. This is intentional: they enable features like dry-run mode and cache warming. If your team forbids test code in production, Nullables aren't a fit.
  ```

---

## Anti-Patterns Section Could Be Tighter

**Current anti-patterns:**
1. Using mock libraries
2. Writing broad integration tests
3. Testing interactions instead of outcomes
4. Constructor does work
5. Parameters at wrong abstraction level

**Issues:**
- "Constructor does work" is a general anti-pattern, not Nullables-specific
- Could distinguish "general design anti-patterns" from "Nullables-specific anti-patterns"

- [ ] Consider splitting: "These make Nullables impossible" vs "These undermine Nullables' benefits"
- [ ] Or: Trim to focus on the Nullables-specific ones (mock libraries, interactions, abstraction level)

---

## Examples Follow "Good Example" Pattern - Consider Anti-Examples

Best practices: *"Use principles + anti-examples, not good examples to copy (avoids collapsing solution space)"*

**Current:** The skill uses good examples heavily.

**Observation:** The anti-patterns section already does this well. But the main examples could benefit from brief "don't do this" contrasts inline.

- [ ] The existing BAD/GOOD patterns in anti-patterns are good
- [ ] Consider adding brief anti-examples to the Core Pattern section showing what NOT to do in `createNull()`

---

## Language Focus is JavaScript - Consider Noting Applicability

**Current:** All examples are JavaScript.

**Problem:** Users in Python, TypeScript, Java may wonder if the pattern applies.

**Note:** The embedded-stubs.md already has a Java example (Thin Wrapper Pattern).

- [ ] Add a brief note: "Examples use JavaScript. The pattern applies to any language - see embedded-stubs.md for Java example"
- [ ] Or: Add Python example in a reference file

---

## The nullable_todo.md File Has Overlapping Suggestions

The existing `nullable_todo.md` file has good suggestions that overlap with this analysis. Consider merging.

Key overlapping points:
- Description needs better trigger words (both agree)
- SKILL.md structure/ordering (both agree)
- A-Frame may be too detailed (both agree)
- CommandLine example is long (both agree)
- OutputListener needs introduction (both agree)
- Missing Quick Start (both agree)
- Reference navigation (both agree)

- [ ] Merge this file with nullable_todo.md, keeping one authoritative list
- [ ] Or: Delete nullable_todo.md after implementing suggestions

---

## Consider Adding a "Philosophy" Section

**Problem:** The skill teaches mechanics but the philosophy (sociable tests, state-based over interaction-based, overlapping coverage) could be more explicit.

Shore's core argument: traditional mock-based tests *"lock in implementation details"* - Nullables test *"what was produced, not what methods were called"*.

- [ ] Add a brief philosophy statement:
  ```
  ## Philosophy

  Mocks verify method calls. Nullables verify outcomes. When you refactor internals, mock-based tests break. Nullables tests keep passing because they check what your code produces, not how it produces it.
  ```

---

## Structural Recommendation: Proposed Reordering

Based on analysis, here's a suggested SKILL.md flow:

```
1. Core Insight (2 lines) - "production code with an off switch"
2. Quick Start (5 steps)
3. Core Pattern: Two Factory Methods (trimmed example)
4. Testing with Nullables (brief example)
5. When to Use / When NOT to Use
6. Three Supporting Patterns (Output Tracking, Configurable Responses, Embedded Stubs - brief with links)
7. A-Frame Architecture (condensed, or link to reference)
8. Anti-Patterns (focused on Nullables-specific)
9. Reference Navigation (with reading order)
```

- [ ] Discuss reordering with Archie before implementing

---

## Summary: Priority Order

**Critical (affects triggering):**
- [ ] Improve description with trigger words

**High (affects usability):**
- [ ] Add Quick Start section
- [ ] Lead with core insight ("production code with off switch")
- [ ] Trim or relocate A-Frame section
- [ ] Add OutputListener introduction before it's used

**Medium (polish):**
- [ ] Add reference reading order guidance
- [ ] Add tradeoffs discussion
- [ ] Consider adding philosophy section
- [ ] Trim CommandLine example
- [ ] Merge with nullable_todo.md

**Low (nice to have):**
- [ ] Note cross-language applicability
- [ ] Add Shore's terminology where different
- [ ] Tighten anti-patterns section
