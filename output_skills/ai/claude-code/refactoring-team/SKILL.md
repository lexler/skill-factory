---
name: refactoring-team
description: Iterative code refactoring through progressive lenses via a worker-reviewer agent team.
disable-model-invocation: true
argument-hint: "[target-path]"
---

STARTER_CHARACTER = 💎

## Prerequisites

Agent teams must be enabled in settings:
```json
{
  "env": {
    "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"
  }
}
```
If not set, offer to add it before proceeding.

## Setup

If $ARGUMENTS provided, use as target path. Otherwise ask for:
- Target path (files or folder to refactor)
- Test command to verify changes

Verify the target path exists and tests pass before proceeding.

## Launch the Team

Create an agent team with two teammates: **worker** and **reviewer**.

Read the spawn prompts:
- Worker: [references/worker-prompt.md](references/worker-prompt.md)
- Reviewer: [references/reviewer-prompt.md](references/reviewer-prompt.md)

Before spawning, replace these placeholders in both prompts:
- `TARGET_PATH` → actual target path
- `TEST_COMMAND` → actual test command
- `LENSES_DIR` → `${CLAUDE_SKILL_DIR}/references/lenses`
- `GUIDES_DIR` → `${CLAUDE_SKILL_DIR}/references/reviewer-guides`

## After Launch

Tell the user:
- Shift+Down cycles between worker and reviewer
- For split panes: set `teammateMode: "tmux"` in settings
