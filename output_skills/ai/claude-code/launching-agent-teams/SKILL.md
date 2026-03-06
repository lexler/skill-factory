---
name: launching-agent-teams
description: Launches agent teams with structured roles and task decomposition. Use when asked to create a team, spawn teammates, or coordinate multiple agents in parallel.
---

STARTER_CHARACTER = 🚀👥

## Setup

Update reference docs to get the latest from Anthropic:
```bash
python ${CLAUDE_SKILL_DIR}/scripts/update-docs.py
```

## Prerequisites

Agent teams are experimental. The user must have this in their settings (`~/.claude/settings.json` or `.claude/settings.json`):
```json
{
  "env": {
    "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"
  }
}
```

If the flag isn't set, tell the user and offer to add it before proceeding.

## Teams vs Subagents — Pick the Right Tool

Before launching a team, confirm it's the right approach:

**Use agent teams when:**
- Teammates need to communicate with each other
- Work benefits from debate, challenge, or cross-pollination
- Tasks span multiple independent areas (frontend/backend/tests)
- Investigation needs competing hypotheses

**Use subagents instead when:**
- Workers just report results back (no inter-agent communication)
- Tasks are focused and self-contained
- You want lower token cost
- Sequential dependency between steps

**Use git worktrees when:**
- You want manual parallel sessions without automated coordination

If the task fits subagents better, say so and offer that instead.

## Launching a Team

### 1. Clarify the Work

Before spawning anything, understand:
- What's the goal?
- What are the independent pieces?
- What would each teammate own?

### 2. Decompose Into Roles

Each teammate should own a distinct, non-overlapping area. Overlap causes file conflicts and wasted tokens.

Aim for 3-5 teammates. More than that creates coordination overhead that rarely pays off. Each teammate should have 5-6 tasks to stay productive.

Anti-patterns:
- Two teammates editing the same file
- A teammate with only one small task (just do it yourself)
- Roles so broad they inevitably overlap

### 3. Size Tasks Appropriately

- Too small: coordination overhead exceeds the benefit
- Too large: teammates work too long without check-ins
- Right size: self-contained units with a clear deliverable (a function, a test file, a review document)

### 4. Write Rich Spawn Prompts

Teammates do NOT inherit the lead's conversation history. They only get:
- CLAUDE.md and project context
- The spawn prompt you write

Include in each spawn prompt:
- Specific files/modules they own
- Relevant context they need (architecture decisions, constraints)
- What "done" looks like
- Technologies, patterns, or conventions to follow

### 5. Configure Display Mode

- `in-process` (default): all teammates in one terminal, cycle with Shift+Down
- `tmux`/`auto`: split panes, each teammate visible (requires tmux or iTerm2)

For monitoring multiple teammates, split panes are better. Suggest tmux if available.

### 6. Create the Team

Present the proposed team structure to the user for approval before spawning. The structure should cover:
- Team goal
- Number of teammates and their roles
- What each teammate owns (specific files/modules)
- Model choice (default: inherit from lead, or Sonnet for cost efficiency)
- Whether plan approval is needed (recommend for risky/destructive work)

## Team Management

- **Plan approval**: For risky work, require teammates to plan before implementing. The lead reviews and approves/rejects plans.
- **Direct messaging**: Users can message individual teammates via Shift+Down (in-process) or clicking panes (split mode).
- **Task dependencies**: Tasks can depend on other tasks. Blocked tasks auto-unblock when dependencies complete.
- **Hooks**: `TeammateIdle` (exit code 2 sends feedback, keeps teammate working) and `TaskCompleted` (exit code 2 prevents completion).

## Key Constraints

- One team per session — clean up before starting a new one
- No nested teams — teammates cannot spawn their own teams
- Lead is fixed — can't transfer leadership
- No session resumption for in-process teammates — after resume, spawn new ones
- All teammates start with the lead's permission mode
- Shutdown can be slow — teammates finish current tool call first

## Parallel Work Principles

From large-scale multi-agent projects:
- **Decompose for true parallelism**: if all agents converge on the same bug/file, parallelization fails regardless of team size
- **Design for agent orientation**: teammates entering fresh need rich context in their spawn prompts and CLAUDE.md — documentation is their primary interface
- **Lightweight coordination**: file-based task lists + git conflict resolution work better than complex orchestration
- **Acknowledge hard limits**: autonomous agents have ceilings — plan for human verification of critical outcomes

## Cleanup

Always clean up through the lead:
```
Clean up the team
```

Shut down teammates first, then clean up. If orphaned tmux sessions persist:
```bash
tmux ls
tmux kill-session -t <session-name>
```

## Reference

- [references/anthropic-agent-teams.md](references/anthropic-agent-teams.md) - Complete agent teams documentation
- [references/anthropic-sub-agents.md](references/anthropic-sub-agents.md) - Subagents documentation (for comparison and configuration)
