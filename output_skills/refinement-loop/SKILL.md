---
name: refinement-loop
description: Generic iterative refinement process. Use when distilling ideas to their essence, simplifying explanations, refactoring code, or any task needing progressive improvement through multiple passes.
---

# Refinement Loop

STARTER_CHARACTER = 🔄

Iterative refinement through file artifacts. Each pass removes one layer of noise, revealing the next.

## Setup

Ensure `playground/` exists and is in `.gitignore`. All iteration files go there.

## Process

### 1. Clarify Goal (if the user hasn't defined it for you already earlier in the conversation)

Ask the user:
- What are you refining and what is the goal of refinement?
- Derive a short tag that we'll use as filename for iterating: `{goal}-{subject}` (e.g., `gist-nullables`, `simplify-api`, `distill-auth-docs`)

### 2. Capture Starting Point

Write original to: `playground/{goal}-{subject}-0.md`

### 3. Iterate

Loop:

1. **Read back** the current file (forces fresh perspective)
2. **Reflect critically**: What's missing? What's weak? What could be clearer?
3. **If improvements found**: Write improved version to `playground/{goal}-{subject}-{N+1}.md`, then loop again

#### Before Stopping - Exhaustive Check

When you think you're done, you're probably not. Run through this:

1. **List everything** that could still be improved - even small things (formatting, word choice, structure, clarity)
2. **Consider what we haven't considered** - what angles did we miss? What would someone else notice?
3. **Try improving in a new direction** - not just polishing what's there, but questioning assumptions
4. **Read as if seeing it for the first time** - does it immediately make sense? Is anything unclear?

Only stop when you've gone through this checklist extensively multiple times and genuinely found nothing. There is no "good enough" - someone will use this later and shouldn't waste time on mediocre results.

### 4. Present Final

Show the user the final version with a brief summary of the refinement journey and number of iterations you used.
If deeper issues or questions surfaced, present them to the user as well.

## Principles

- **Read back forces fresh eyes**: Reading from file breaks the "I just wrote this" blindness
- **No "good enough"**: Every detail matters. Formatting, word choice, structure - all of it
- **Consider the unconsidered**: What angles haven't we explored? What would someone else see? Is there something that the user haven't even considered, too? (you can surface it as questions at the end)
- **Files forces iterative improvement**: Writing to files prevents "pretend" iteration in conversation. Real iteration gets to much better results.
- **Earn the stop**: Run the exhaustive check. If you find nothing, you've earned stopping.
