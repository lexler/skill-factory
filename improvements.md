# Nullables Skill Improvements

## SKILL.md Conciseness (Context Management)

- [ ] **Shorten the "When to Use" section** — The "Do NOT use when" items are obvious (pure logic doesn't need Nullables). Could be one line.

## Missing Concepts from James Shore

- [x] **Emphasize "production code, not test code"** — The key insight that Nullables are shippable production artifacts (useful for dry-run mode, cache warming) is mentioned once but deserves more prominence. This is the philosophical core.

- [x] **Expand Paranoic Telemetry** — Currently just a bullet point. Add brief explanation: "Assume everything fails. Test error paths, timeouts, and network failures as thoroughly as happy paths."

- [x] **Clarify Collaborator-Based Isolation** — The phrase appears in test-patterns.md but SKILL.md only hints at it. Add explicit guidance: "Use dependencies' own tracking methods in assertions rather than hardcoding expected values."

- [ ] **Promote Narrow Integration Tests** — These are mentioned but buried. They're essential: sociable tests verify logic, but you need a few tests hitting real infrastructure to verify wrappers actually work.

## Progressive Disclosure

- [ ] **Move ConfigurableResponses helper to reference** — The full implementation (lines in configurable-responses.md) is good, but SKILL.md shows too much of it inline. Link instead.

- [ ] **Extract the complete CommandLine example** — The 40-line example (lines 116-158) could be shortened to just show the pattern, with "See [building/infrastructure-wrappers.md] for complete example."

- [ ] **Link to links.md from SKILL.md** — The links.md file exists but isn't referenced. Add a "Further Reading" section pointing to it.

## Structure Improvements

- [ ] **Separate "thinking" from "building"** — The skill mixes philosophy with implementation. Consider reorganizing into:
  1. Core Concepts (what, why) — keep in SKILL.md
  2. Building Patterns (how) — extract more to references

- [ ] **Make A-Frame more prominent** — It's the architectural foundation but appears after examples. Move up or make clearer that this is the prerequisite pattern.

- [ ] **Add a "Quick Start" workflow** — After reading, Claude should know the exact steps. Something like:
  1. Identify infrastructure code
  2. Create wrapper with create()/createNull()
  3. Add embedded stub
  4. Add output tracking
  5. Write tests using createNull()

## Anti-Patterns Section

- [ ] **Add "Stub Drift" anti-pattern** — Embedded stubs can diverge from real infrastructure behavior. Solution: Narrow Integration Tests.

- [ ] **Add "God Class" warning for Traffic Cop** — Event-driven architectures can become monolithic. Split into modules when handlers grow.

- [ ] **Add "Overbuild" warning** — Don't build generic stub features that aren't test-driven through your code's public interface.

## Reference Files

- [ ] **Add table of contents to longer reference files** — embedded-stubs.md is 317 lines, infrastructure-wrappers.md is 402 lines. Adding TOCs at top helps Claude navigate if it does partial reads.

- [ ] **Consolidate architecture references** — a-frame.md (78 lines), logic-sandwich.md (110 lines), and event-driven.md (112 lines) could potentially be merged into one file since they're conceptually connected.

## Examples

- [ ] **Show failure case in main example** — Current CommandLine example only shows success. Add one test showing error configuration.

- [ ] **Add Python example** — All examples are JavaScript. The pattern is language-agnostic; showing a second language would reinforce this.

## Terminology

- [ ] **Decide on "Nullable" vs "Nullable Infrastructure"** — Be consistent. Shore uses both but the skill should pick one.

- [x] **Clarify "sociable" vs "solitary" upfront** — These terms appear without definition. Brief explanation would help.

## Output Tracking Reference

- [ ] **Simplify OutputListener in SKILL.md** — The inline OutputListener code (lines 117-145 in command_line example) is implementation detail. The concept is what matters; the implementation belongs in the reference.

## Test Patterns Reference

- [ ] **Add "expect.any()" portability warning more prominently** — The note about Jest-specific matchers is buried at the end. Move to where timestamp examples appear.

## Migration Reference

- [ ] **Add concrete "Find mocks" commands for more frameworks** — Currently only shows generic grep. Add specific patterns for Jest, Sinon, etc.
