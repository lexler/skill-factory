# Approval Tests Skill - Planning Document

## Resources & References Used

### Approval Tests Domain

| Resource | Location | Purpose |
|----------|----------|---------|
| Main site | https://approvaltests.com | Core concepts, philosophy |
| Python implementation | `/Users/ladak/workspace/knowledge/references-for-skills/approvals/ApprovalTests.Python` | Python API, patterns, examples |
| Node.js implementation | `/Users/ladak/workspace/knowledge/references-for-skills/approvals/Approvals.NodeJS` | JS/TS API, patterns, examples |
| Java implementation | `/Users/ladak/workspace/knowledge/references-for-skills/approvals/ApprovalTests.Java` | Java API, patterns, examples |

### Skill Building Documentation

| Resource | Location | Purpose |
|----------|----------|---------|
| Overview | `docs/knowledge/anthropic-skill-docs/overview.md` | What skills are, progressive disclosure, architecture |
| Skills guide | `docs/knowledge/anthropic-skill-docs/skills.md` | Implementation patterns, SKILL.md structure, troubleshooting |
| Best practices | `docs/knowledge/anthropic-skill-docs/best-practices.md` | Authoring guidelines, anti-patterns, checklist |
| Create skill process | `docs/create_new_skill-process.md` | Step-by-step skill creation workflow |

### AI Patterns (Skill Design Guidance)

| Pattern | Type | Location | How It Informed Design |
|---------|------|----------|------------------------|
| limited-focus | Obstacle | `obstacles/limited-focus.md` | Keep SKILL.md lean, don't overload context |
| distracted-agent | Anti-pattern | `anti-patterns/distracted-agent.md` | Single responsibility, focused skill |
| focused-agent | Pattern | `patterns/focused-agent.md` | Narrow scope = better rule following |
| reference-docs | Pattern | `patterns/reference-docs.md` | On-demand loading for language-specific details |
| ground-rules | Pattern | `patterns/ground-rules.md` | Core concepts always loaded (SKILL.md body) |

Base path for AI patterns: `/Users/ladak/workspace/knowledge/references-for-skills/ai-patterns-lexler/augmented-coding-patterns/documents`

---

## Domain Understanding

### What are Approval Tests?

Snapshot-based testing where you verify complex output against a "golden master" file instead of writing assertions.

```
Traditional:  assertEquals("expected", result)
Approval:     verify(result)  →  compares to .approved.txt file
```

### Core Workflow
1. Test runs → creates `.received.txt` with actual output
2. Compare to `.approved.txt` (golden master)
3. Match → pass, delete received
4. Mismatch → fail, open diff tool, developer reviews

### Key Components (consistent across languages)

| Component | Purpose |
|-----------|---------|
| **Writer** | Serializes output to received file |
| **Namer** | Generates file paths (ClassName.methodName.approved.txt) |
| **Reporter** | Handles mismatches (opens diff tool) |
| **Scrubber** | Normalizes non-deterministic content (dates, GUIDs) |
| **Comparator** | Compares received vs approved |

### Language Implementations

| Language | Package | Main Entry |
|----------|---------|------------|
| Python | `approvaltests` | `verify()`, `verify_all()`, `verify_as_json()` |
| JS/TS | `approvals` | `approvals.verify()`, `approvals.verifyAsJSON()` |
| Java | `com.approvaltests` | `Approvals.verify()`, `Approvals.verifyAll()` |

---

## Design Decisions Needed

### 1. Scope: Single skill or per-language?

**Option A: Single skill with language references**
```
approval-tests/
├── SKILL.md (core concepts, workflow, when to use)
└── references/
    ├── python.md
    ├── nodejs.md
    └── java.md
```
Pros: Unified concepts, Claude picks language from project context
Cons: More to navigate

**Option B: Separate skills per language**
```
approval-tests-python/
approval-tests-nodejs/
approval-tests-java/
```
Pros: Focused, smaller context per trigger
Cons: Repetition, harder to maintain

### 2. Primary Use Cases

What should Claude excel at with this skill?
- Writing new approval tests from scratch
- Converting assertion-based tests to approval tests
- Understanding and maintaining existing approval tests
- Setting up approval tests in a new project
- Debugging approval test failures
- Using advanced patterns (combinations, scrubbers)

### 3. Skill Trigger Description

Draft: "Write and maintain approval tests (snapshot testing). Use when verifying complex output, converting assertion tests to approvals, or working with .approved/.received files."

---

## Progressive Disclosure Strategy

Based on the AI patterns (limited focus, focused agent, reference docs):

### Level 1: SKILL.md Body (~300 lines max)
**Always loaded when triggered**
- Core philosophy: "A picture's worth 1000 assertions"
- Basic workflow: verify → approve → commit
- File structure: .approved.txt vs .received.txt
- When to use approval tests vs assertions
- Language detection heuristic (Python/JS/Java)
- Pointers to references

### Level 2: Language References (loaded on demand)
- API specifics for each language
- Setup/installation
- Framework integration (pytest, mocha, JUnit)
- Language-specific idioms

### Level 3: Advanced Patterns (loaded on demand)
- Combination testing
- Scrubbers for non-deterministic data
- Custom reporters
- Inline approvals

---

## Decisions Made

1. **Single skill** with language-specific references
2. **Priority use cases:**
   - Writing new approval tests
   - Advanced patterns (combinations, scrubbers)
   - Inline approvals (different per language)
3. **Key pain point:** Claude hallucinates usages → need accurate API from reference repos
4. **Setup:** Separate setup references per language

---

## Files To Create

### Core
- [x] `SKILL.md` - Core concepts, workflow, philosophy (~300 lines)

### Python References
- [x] `references/python/api.md` - verify, verify_all, verify_as_json, etc.
- [x] `references/python/setup.md` - pip install, pytest integration
- [x] `references/python/inline.md` - Python inline approvals
- [x] `references/python/scrubbers.md` - Python scrubber patterns

### Node.js References
- [x] `references/nodejs/api.md` - approvals.verify, verifyAsJSON, etc.
- [x] `references/nodejs/setup.md` - npm install, mocha/jest integration
- [x] `references/nodejs/inline.md` - Node inline approvals (not supported, alternatives)
- [x] `references/nodejs/scrubbers.md` - Node scrubber patterns

### Java References
- [x] `references/java/api.md` - Approvals.verify, verifyAll, etc.
- [x] `references/java/setup.md` - Maven/Gradle deps, JUnit integration
- [x] `references/java/inline.md` - Java inline approvals
- [x] `references/java/scrubbers.md` - Java scrubber patterns

### Shared Patterns
- [x] `references/patterns/combinations.md` - Testing all input combinations
- [x] `references/patterns/testing-patterns.md` - Summary of testing patterns

---

## SKILL.md Content Plan

### Frontmatter
```yaml
---
name: approval-tests
description: Write approval tests (snapshot testing) for Python, JavaScript/TypeScript, or Java. Use when verifying complex output, testing with golden masters, or working with .approved/.received files.
---
```

### Body Sections (~300 lines target)

- [ ] **Philosophy** (~20 lines) - "A picture's worth 1000 assertions", when to use, mental model
- [ ] **Core Workflow** (~40 lines) - verify → compare → approve, file naming, .approved vs .received
- [ ] **Quick Start** (~30 lines) - Minimal example per language, how to approve first result
- [ ] **When Approval Tests Shine** (~20 lines) - Complex objects, characterization tests, combos
- [ ] **Common Patterns** (~40 lines) - verify(), verifyAll(), verifyAsJson(), scrubbing
- [ ] **Language Detection** (~20 lines) - Look at project files, pointer to reference
- [ ] **Reference Links** (~20 lines) - Links to all reference files
- [ ] **Anti-Patterns** (~30 lines) - What not to do

---

## Implementation Phases

- [x] **Phase 1: Core SKILL.md** - Write main skill file with philosophy, workflow, patterns
- [x] **Phase 2: Language API References** - Extract accurate APIs from reference repos
  - Source: `/Users/ladak/workspace/knowledge/references-for-skills/approvals/`
- [x] **Phase 3: Setup References** - Installation and framework integration per language
- [x] **Phase 4: Advanced Pattern References** - Inline approvals, scrubbers, combinations
- [ ] **Phase 5: Review & Iterate** - Check against best-practices.md, test in real usage

---

## Anti-Patterns to Address

Things Claude might do wrong without guidance:
1. Writing assertions instead of using verify()
2. Forgetting to commit .approved files
3. Committing .received files
4. Not using scrubbers for timestamps/GUIDs
5. Over-complicating simple verifications
6. Not understanding the approve workflow (rename received → approved)
7. **Hallucinating API methods** - must use accurate examples from reference repos
