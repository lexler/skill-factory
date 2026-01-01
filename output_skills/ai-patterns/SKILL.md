---
name: ai-patterns
description: Reference patterns for augmented coding with AI. Use when discussing AI coding patterns, anti-patterns, obstacles, context management, steering AI, or looking up Lexler's patterns collection.
---

# AI Patterns Reference

Patterns for effective AI-augmented software development by Lada Kesseler (github nickname lexler), Llewellyn Falco, and contributors.

## First Step: Always Update the Reference Repository

Pull latest patterns:
```bash
git -C /Users/ladak/workspace/knowledge/references-for-skills/ai-patterns-lexler/augmented-coding-patterns pull
```

## Patterns Location

Base path: `/Users/ladak/workspace/knowledge/references-for-skills/ai-patterns-lexler/augmented-coding-patterns/documents`

---

## Context Management

Managing AI context, knowledge, and focus.

### Obstacles

- **context-rot** - Earlier instructions lose influence as conversation grows
- **cannot-learn** - LLMs can't learn from interactions; fixed weights prevent adaptation
- **limited-context-window** - Fixed context size forces choices about what to keep loaded
- **limited-focus** - Too much context causes diluted or misdirected attention
- **excess-verbosity** - AI defaults to verbose output with low signal-to-noise ratio

### Anti-patterns

- **distracted-agent** - Using one agent for everything spreads attention; instructions inconsistently followed

### Patterns

- **context-management** - Treat context as scarce resource requiring active append/reset operations
- **knowledge-document** - Save important information as markdown files for session loading
- **ground-rules** - Essential behavioral rules auto-loaded into every session
- **extract-knowledge** - Save emerging insights and corrections from ephemeral context to files immediately during sessions
- **focused-agent** - Single narrow responsibility gives AI cognitive space to follow rules better
- **reference-docs** - On-demand knowledge loaded only when needed for current task
- **knowledge-composition** - Split knowledge into focused, composable files with single responsibilities
- **semantic-zoom** - Control abstraction levels—zoom out for overview or zoom in for details
- **noise-cancellation** - Explicitly ask AI to be succinct and strip filler from responses

---

## Reliability & Quality

Handling non-determinism, complexity, and verification.

### Obstacles

- **non-determinism** - Same input produces different outputs; results unpredictable
- **hallucinations** - AI invents non-existent APIs, methods, or syntax
- **degrades-under-complexity** - AI performance drops with complex multi-step tasks
- **selective-hearing** - AI ignores certain instructions; training data overrides explicit directives

### Anti-patterns

- **perfect-recall-fallacy** - Expecting AI to perfectly remember library details instead of letting it discover
- **unvalidated-leaps** - Building on unverified assumptions instead of validating each step
- **ai-slop** - Using AI output without human judgment, just light editing

### Patterns

- **knowledge-checkpoint** - Checkpoint planning before implementation to preserve thinking investment
- **parallel-implementations** - Run multiple implementations in parallel; pick best or combine
- **offload-deterministic** - Use code scripts for deterministic work instead of asking AI repeatedly
- **playgrounds** - Create isolated folders for AI to experiment and test assumptions safely
- **chain-of-small-steps** - Break complex goals into small, focused, verifiable steps
- **hooks** - Lifecycle event hooks intercept workflow; inject targeted corrections
- **reminders** - Repeat critical instructions as explicit steps; structural compliance
- **feedback-flip** - Have different AI focus on evaluation; flip from producing to finding problems
- **refinement-loop** - Give AI specific improvement goal and loop it; each pass removes one layer

---

## Communication

Directing AI behavior, getting honest feedback, and alignment.

### Obstacles

- **black-box-ai** - AI's reasoning is hidden; you can only see inputs and outputs
- **compliance-bias** - AI prioritizes following instructions over questioning unclear requests

### Anti-patterns

- **silent-misalignment** - AI accepts nonsensical instructions instead of asking clarifying questions
- **answer-injection** - Putting solutions in questions limits AI's breadth and better approaches
- **tell-me-a-lie** - Forcing AI to provide answers that don't exist causes fabrication

### Patterns

- **active-partner** - Grant permission for AI to push back, disagree, and flag contradictions
- **check-alignment** - Force AI to show understanding before implementing to catch misalignment early
- **context-markers** - Visual emoji signals to show what instructions AI is currently following
- **cast-wide** - Push AI to show alternatives you haven't considered; avoid first-solution bias
- **reverse-direction** - Break monologue inertia—ask AI what it thinks instead
- **polyglot-ai** - Use right modality for task—voice for convenience, images for visual problems
- **text-native** - Keep everything as text; enables direct editing, version control, instant iteration

---

## Additional Patterns

Patterns not on the main journey but useful in practice.

- **shared-canvas** - Markdown files as shared specs/docs; all humans and AI collaborate together
- **softest-prototype** - Use markdown instructions + AI agent instead of code for flexible exploration
- **take-all-paths** - Build multiple prototypes not one; test all, pick best through exploration
- **borrow-behaviors** - Give AI example and it adapts—styles, patterns, code across languages

---

## Browse All

List patterns by category:
```bash
ls /Users/ladak/workspace/knowledge/references-for-skills/ai-patterns-lexler/augmented-coding-patterns/documents/patterns/
ls /Users/ladak/workspace/knowledge/references-for-skills/ai-patterns-lexler/augmented-coding-patterns/documents/anti-patterns/
ls /Users/ladak/workspace/knowledge/references-for-skills/ai-patterns-lexler/augmented-coding-patterns/documents/obstacles/
```

## Online

View at: https://lexler.github.io/augmented-coding-patterns/
