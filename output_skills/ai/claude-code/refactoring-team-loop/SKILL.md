---
name: refactoring-team-loop
description: Two-pass code refactoring through progressive lenses via a worker-reviewer agent team. Fresh context on the second pass catches what the first missed.
disable-model-invocation: true
argument-hint: "[target-path]"
hooks:
  TeammateIdle:
    - hooks:
        - type: command
          command: "${CLAUDE_SKILL_DIR}/../refactoring-team/references/guard-idle-worker.sh"
---

STARTER_CHARACTER = 💎

This skill wraps `refactoring-team` with a two-pass loop. All lenses, prompts, and reviewer guides live in the `refactoring-team` skill — this skill only adds the second-pass orchestration.

REFACTORING_TEAM_DIR = `${CLAUDE_SKILL_DIR}/../refactoring-team`

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

## Spawning a Round

Each round follows the same steps:

Generate a short random ID: `head -c 3 /dev/urandom | xxd -p | head -c 3`

Use it to name the teammates:
- Worker: `worker-ID` (e.g. `worker-a3f`)
- Reviewer: `reviewer-ID` (e.g. `reviewer-a3f`)

Read the spawn prompts from refactoring-team:
- Worker: `REFACTORING_TEAM_DIR/references/worker-prompt.md`
- Reviewer: `REFACTORING_TEAM_DIR/references/reviewer-prompt.md`

Before spawning, replace these placeholders in both prompts:
- `TARGET_PATH` -> actual target path
- `TEST_COMMAND` -> actual test command
- `LENSES_DIR` -> `REFACTORING_TEAM_DIR/references/lenses`
- `GUIDES_DIR` -> `REFACTORING_TEAM_DIR/references/reviewer-guides`
- `WORKER_NAME` -> the worker's name (e.g. `worker-a3f`)
- `REVIEWER_NAME` -> the reviewer's name (e.g. `reviewer-a3f`)

Append this to the reviewer prompt before spawning:

> **Loop override**: At wrap-up, say "Round complete" (not "Refactoring complete"). After writing REFACTORING-LOG.md, go idle. The manager will decide whether another round is needed.

Spawn both teammates.

## Round 1

Spawn a round. Tell the user:
- Shift+Down cycles between teammates
- For split panes: set `teammateMode: "tmux"` in settings

When both teammates go idle, check that `REFACTORING-LOG.md` exists. This signals the round is complete.

## Round 2

Kill the Round 1 teammates. Spawn a fresh round with new IDs.

When both teammates go idle and a new `REFACTORING-LOG.md` is written, refactoring is complete.

Run `speak "Refactoring complete"` and tell the user.
