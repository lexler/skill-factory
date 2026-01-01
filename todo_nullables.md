# Nullables Skill Development Plan

## Goal

Create a Claude Code skill for James Shore's Nullables pattern that:
- Teaches Claude how to write tests without mocks using Nullables
- Uses progressive disclosure - core concepts in SKILL.md, details in references
- Triggers when users want to test infrastructure, avoid mocks, or apply "testing without mocks"

## Key Challenge

Nullables is a **dense pattern** with many interconnected concepts. The skill must balance:
- **Comprehensive coverage** - all patterns: Nullable factories, Output Tracking, Configurable Responses, Embedded Stubs, Infrastructure Wrappers
- **Context efficiency** - Claude shouldn't load 2000 lines when the user just wants to create a simple wrapper

## Strategy: Layered Disclosure

```
SKILL.md (~200-300 lines)
├── When to use Nullables (decision framework)
├── Core pattern overview (the essentials)
├── Quick example (one complete wrapper)
└── Links to detailed references

references/
├── infrastructure-wrappers.md     (how to build wrappers)
├── output-tracking.md             (observing behavior)
├── configurable-responses.md      (parameterizing test inputs)
├── embedded-stubs.md              (stubbing third-party code)
├── test-patterns.md               (structuring tests)
└── examples/                      (real code samples)
```

## Execution Plan

### Phase 1: Foundation
- [x] Read anthropic skill docs (overview, skills, best-practices)
- [x] Read create_new_skill-process.md
- [x] Read James Shore's "Testing Without Mocks" article
- [x] Explore simple example repo
- [x] Explore complex example repo

### Phase 2: Skill Design
- [x] Define name and description (trigger words matter!)
- [x] Design SKILL.md structure
- [x] Plan reference file organization
- [x] Identify what goes in SKILL.md vs references

### Phase 3: Write SKILL.md
- [x] Write frontmatter (name, description)
- [x] Write "When to Use Nullables" section
- [x] Write core pattern explanation
- [x] Write minimal working example
- [x] Add pointers to reference files

### Phase 4: Write Reference Files
- [x] infrastructure-wrappers.md - building the foundation
- [x] output-tracking.md - observing what happens
- [x] configurable-responses.md - controlling inputs
- [x] embedded-stubs.md - faking third-party code
- [x] test-patterns.md - writing effective tests

### Phase 5: Review & Polish
- [x] Check against anthropic best-practices.md
- [x] Verify progressive disclosure works (SKILL.md stands alone for simple cases)
- [x] Ensure terminology consistency
- [x] Remove anything Claude already knows
- [x] Check references are one level deep

### Phase 6: Evaluate
- [x] Read through as if seeing it fresh
- [x] Ask: Does the description trigger correctly?
- [x] Ask: Is SKILL.md under 500 lines?
- [x] Ask: Can someone use core patterns without reading all references?
- [x] Ask: Are anti-examples included to prevent common mistakes?

## Final Evaluation Results

### Files Created
| File | Lines | Purpose |
|------|-------|---------|
| SKILL.md | 240 | Core concepts, complete example, anti-patterns |
| references/infrastructure-wrappers.md | 270 | Building complete wrappers with step-by-step |
| references/output-tracking.md | 223 | Tracking writes and side effects |
| references/configurable-responses.md | 247 | Controlling external inputs, sequences |
| references/embedded-stubs.md | 296 | Stubbing third-party code, async patterns |
| references/test-patterns.md | 306 | Structuring tests, helper functions |
| **Total** | **1,582** | |

### Quality Assessment

**Triggering**: Description includes all key terms (testing without mocks, nullables, output tracking, configurable responses, embedded stub, infrastructure wrapper)

**Progressive Disclosure**:
- SKILL.md provides complete working knowledge for simple cases (Clock, CommandLine)
- References loaded only for complex scenarios (async, sequences, event-driven)

**Anti-patterns**: Three common mistakes explicitly shown with BAD/GOOD examples

**Abstraction Level**: Emphasized throughout - parameters at caller's level, not implementation details

### What Could Be Improved in Future Iterations
1. Add TypeScript examples in a separate reference
2. Consider A-Frame architecture reference (currently omitted to reduce scope)
3. Add language-specific guidance for Python/Java

## Design Decisions

### What belongs in SKILL.md (always loaded when triggered)
- The "why" - when Nullables beats mocks
- Core pattern: create() / createNull() factory methods
- One complete, minimal example (CommandLine wrapper)
- Quick reference for Output Tracking and Configurable Responses
- Links to deep-dive references

### What belongs in references (loaded on demand)
- Full patterns with multiple examples
- Edge cases (async, event-driven, complex responses)
- A-Frame architecture details
- Language-specific considerations (TypeScript, Java)
- Test helper patterns

### Trigger words for description
- "test without mocks", "testing without mocks"
- "nullables", "nullable pattern"
- "infrastructure wrapper", "infrastructure testing"
- "avoid mocking", "no mocks"
- "output tracking", "configurable responses"
- "embedded stub"

## Anti-patterns to Address

1. **Testing implementation not behavior** - Nullables test state/output, not calls
2. **Over-stubbing** - Only stub what you need in Embedded Stubs
3. **Constructor work** - Constructors should do nothing; use connect()/start()
4. **Magic dependency injection** - Use explicit factory methods, no frameworks
5. **Testing the mock** - Tests should exercise real code paths

## Resources Used

### Primary Sources
| Resource | What I Used From It |
|----------|---------------------|
| James Shore article (testing-without-mocks) | Core concepts, terminology, all pattern definitions |
| Simple example repo | Basic Nullable implementation, CommandLine wrapper, App test structure |
| Complex example repo | HttpClient wrapper, Rot13Client (high-level Nullable), ConfigurableResponses utility, OutputListener/OutputTracker |

### Skill Creation Docs
| Resource | What I Used From It |
|----------|---------------------|
| overview.md | Progressive disclosure levels, token costs, Skill structure |
| skills.md | SKILL.md format, where skills live, troubleshooting |
| best-practices.md | Conciseness principles, degrees of freedom, naming, anti-patterns |
| create_new_skill-process.md | Step-by-step creation workflow, review checklist |

### Key Patterns Extracted

**From Simple Example:**
```javascript
// Core pattern: two factory methods
static create() { return new CommandLine(process); }
static createNull({ args = [] } = {}) { return new CommandLine(new StubbedProcess(args)); }

// Output tracking
trackOutput() { return this._listener.trackOutput(); }
```

**From Complex Example:**
```javascript
// Configurable Responses for multiple return values
static createNull(uuids = uuid.NIL) {
    return new UuidGenerator(new StubbedUuid(uuids));
}
// StubbedUuid uses ConfigurableResponses.create(uuids)

// High-level Nullable delegating to lower-level Nullable
static createNull(options = [{}]) {
    const httpResponses = options.map(response => nulledHttpResponse(response));
    const httpClient = HttpClient.createNull({ [TRANSFORM_ENDPOINT]: httpResponses });
    return new Rot13Client(httpClient);
}
```

## Success Criteria

1. Claude can implement a basic Infrastructure Wrapper with Nullable from just SKILL.md
2. Claude knows to check references for complex cases (async, events, multiple responses)
3. The skill triggers on natural requests like "help me test this HTTP client without mocks"
4. Tests written with skill guidance follow state-based (not interaction-based) approach
5. No mock library imports in resulting code
