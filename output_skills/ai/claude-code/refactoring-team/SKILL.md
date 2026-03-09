---
name: refactoring-team
description: Iterative code refactoring through progressive lenses via a worker-reviewer agent team.
disable-model-invocation: true
argument-hint: "[target-path]"
hooks:
  TeammateIdle:
    - hooks:
        - type: command
          command: "${CLAUDE_SKILL_DIR}/references/guard-idle-worker.sh"
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

Generate a short random ID: `head -c 3 /dev/urandom | xxd -p | head -c 3`

Use it to name the teammates:
- Worker: `worker-ID` (e.g. `worker-a3f`)
- Reviewer: `reviewer-ID` (e.g. `reviewer-a3f`)

Read the spawn prompts:
- Worker: [references/worker-prompt.md](references/worker-prompt.md)
- Reviewer: [references/reviewer-prompt.md](references/reviewer-prompt.md)

Before spawning, replace these placeholders in both prompts:
- `TARGET_PATH` → actual target path
- `TEST_COMMAND` → actual test command
- `LENSES_DIR` → `${CLAUDE_SKILL_DIR}/references/lenses`
- `GUIDES_DIR` → `${CLAUDE_SKILL_DIR}/references/reviewer-guides`
- `WORKER_NAME` → the worker's name (e.g. `worker-a3f`)
- `REVIEWER_NAME` → the reviewer's name (e.g. `reviewer-a3f`)

## After Launch

Tell the user:
- Shift+Down cycles between worker and reviewer
- For split panes: set `teammateMode: "tmux"` in settings

## Monitor Progress

When a worker goes idle, read `.refactoring-state` to check the lens number. If it skipped a value, message the reviewer to go back and complete the skipped lens first.
