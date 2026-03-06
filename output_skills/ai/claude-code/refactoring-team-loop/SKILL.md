---
name: refactoring-team-loop
description: Iterative code refactoring through progressive lenses via a worker-reviewer agent team, with a quality-check loop for a second pass.
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

## Launch Round 1

Generate a short random ID: `head -c 3 /dev/urandom | xxd -p | head -c 3`

Use it to name the teammates:
- Worker: `worker-ID` (e.g. `worker-a3f`)
- Reviewer: `reviewer-ID` (e.g. `reviewer-a3f`)

Read the spawn prompts:
- Worker: [references/worker-prompt.md](references/worker-prompt.md)
- Reviewer: [references/reviewer-prompt.md](references/reviewer-prompt.md)

Before spawning, replace these placeholders in both prompts:
- `TARGET_PATH` -> actual target path
- `TEST_COMMAND` -> actual test command
- `LENSES_DIR` -> `${CLAUDE_SKILL_DIR}/references/lenses`
- `GUIDES_DIR` -> `${CLAUDE_SKILL_DIR}/references/reviewer-guides`
- `WORKER_NAME` -> the worker's name (e.g. `worker-a3f`)
- `REVIEWER_NAME` -> the reviewer's name (e.g. `reviewer-a3f`)

Spawn both teammates.

Tell the user:
- Shift+Down cycles between teammates
- For split panes: set `teammateMode: "tmux"` in settings

## Wait for Round 1 Completion

When both teammates go idle, check that `REFACTORING-LOG.md` exists. This signals the round is complete.

## Quality Check

Spawn a quality checker to assess the result:

1. Generate a new ID: `head -c 3 /dev/urandom | xxd -p | head -c 3`
2. Name it `checker-ID` (e.g. `checker-c9d`)
3. Read [references/quality-checker-prompt.md](references/quality-checker-prompt.md)
4. Replace placeholders:
   - `TARGET_PATH` -> actual target path
   - `LENSES_DIR` -> `${CLAUDE_SKILL_DIR}/references/lenses`
   - `CHECKER_NAME` -> the checker's name
5. Spawn the quality checker

When the checker goes idle, read `.refactoring-remaining-issues.md`.

## Loop Decision

If the "Worth Fixing" section in `.refactoring-remaining-issues.md` has meaningful issues, launch Round 2. If empty or trivial, refactoring is complete — tell the user and run `speak "Refactoring complete"`.

## Launch Round 2

1. Generate new IDs for worker and reviewer
2. Read the spawn prompts again (worker-prompt.md and reviewer-prompt.md)
3. Replace all placeholders as in Round 1
4. Read `.refactoring-remaining-issues.md` and prepend its "Worth Fixing" items to the worker prompt under a `## Priority Issues` header — these are what the worker should focus on first
5. Spawn both teammates
6. When both go idle and a new `REFACTORING-LOG.md` is written, refactoring is complete

Run `speak "Refactoring complete"` and tell the user.

Cap at 2 total rounds. Do not loop further.
