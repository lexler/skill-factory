# Nullables Skill Improvements

## Medium Priority

- [ ] **Add Contents/TOC to logic-sandwich.md** — At 110 lines, just over the 100-line threshold. A brief TOC helps Claude navigate

- [ ] **Add Contents/TOC to event-driven.md** — At 112 lines, also just over threshold

- [ ] **Strengthen description trigger phrases** — Current description is good but could add: "sociable tests", "state-based testing", "avoid mocking libraries", "test doubles without mocks". Make it even easier to trigger

## Low Priority / Consider

- [ ] **Consolidate "When to Use" guidance** — Info about when to use Nullables appears in both the "When to Use" section and scattered in other places. Consider consolidating

- [ ] **Remove Jest-specific syntax from output-tracking.md** — Line 113-114 uses `expect.any(Number)` with a note it's Jest-specific. Since rest of skill uses `assert`, could replace example with the portable destructuring pattern shown in test-patterns.md

- [ ] **Consider trimming SKILL.md examples** — The core pattern example is detailed (full Clock class). Could potentially move full implementation to a reference and keep SKILL.md at the conceptual level. This is debatable since the pattern IS the core of the skill

## Done
