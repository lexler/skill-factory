---
name: creating-hooks
description: Creates Claude Code hooks.
---

STARTER_CHARACTER = 🪝

## Setup

First, update the reference docs to get the latest from Anthropic:
```bash
python ~/.claude/skills/creating-hooks/scripts/update-docs.py
```

## What Hooks Are

Shell commands that execute at lifecycle points in Claude Code. Unlike prompts, hooks are deterministic—they always run when triggered.

## Configuration

Hooks live in settings files:
- `~/.claude/settings.json` - User settings (all projects)
- `.claude/settings.json` - Project settings (shared via git)
- `.claude/settings.local.json` - Local project settings (not committed)

```json
{
  "hooks": {
    "EventName": [
      {
        "matcher": "ToolPattern",
        "hooks": [
          {
            "type": "command",
            "command": "your-command-here"
          }
        ]
      }
    ]
  }
}
```

**Matcher**: Pattern to match tool names (case-sensitive)
- Exact match: `Write`
- Regex: `Edit|Write`
- All tools: `*` or omit

**Environment variables**:
- `$CLAUDE_PROJECT_DIR` - Absolute path to project root
- `$CLAUDE_ENV_FILE` - File path for persisting env vars (SessionStart only)

## Hook Events

**Tool events** (matcher applies):
- `PreToolUse` - Before tool executes
- `PostToolUse` - After tool completes
- `PermissionRequest` - Permission dialog shown

**Session events**:
- `SessionStart` - Session begins/resumes (matcher: startup/resume/clear/compact)
- `SessionEnd` - Session ends
- `PreCompact` - Before compaction (matcher: manual/auto)

**Other events**:
- `UserPromptSubmit` - User submits prompt
- `Stop` - Agent finishes
- `SubagentStop` - Subagent finishes
- `Notification` - Alerts sent (matcher: notification type)

## Exit Codes

- **0**: Success. stdout shown in verbose mode. For `UserPromptSubmit`/`SessionStart`, stdout added to context.
- **2**: Block. stderr fed to Claude as error message. Blocks the action.
- **Other**: Non-blocking error. stderr shown to user.

## JSON Output

For advanced control, return JSON to stdout with exit code 0:

```json
{
  "continue": false,
  "stopReason": "Message shown when stopping"
}
```

### PreToolUse Control

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "allow",
    "permissionDecisionReason": "Auto-approved",
    "updatedInput": { "field": "modified value" }
  }
}
```

Decisions: `"allow"` (bypass permission), `"deny"` (block), `"ask"` (prompt user)

### PostToolUse Feedback

```json
{
  "decision": "block",
  "reason": "Explanation fed to Claude"
}
```

### Stop/SubagentStop Control

```json
{
  "decision": "block",
  "reason": "Must fix X before stopping"
}
```

## Hook Input

Hooks receive JSON via stdin:

```json
{
  "session_id": "abc123",
  "transcript_path": "/path/to/transcript.jsonl",
  "cwd": "/current/dir",
  "permission_mode": "default",
  "hook_event_name": "PreToolUse",
  "tool_name": "Write",
  "tool_input": { "file_path": "/path", "content": "..." }
}
```

## Common Patterns

**Auto-format after edit**:
```json
{
  "hooks": {
    "PostToolUse": [{
      "matcher": "Edit|Write",
      "hooks": [{
        "type": "command",
        "command": "jq -r '.tool_input.file_path' | xargs -I{} sh -c 'echo {} | grep -q \"\\.ts$\" && npx prettier --write {}'"
      }]
    }]
  }
}
```

**Block dangerous commands**:
```json
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "Bash",
      "hooks": [{
        "type": "command",
        "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/validate-bash.py"
      }]
    }]
  }
}
```

**Inject context on prompt**:
```json
{
  "hooks": {
    "UserPromptSubmit": [{
      "hooks": [{
        "type": "command",
        "command": "echo '[REMINDER: Follow TDD]'"
      }]
    }]
  }
}
```

**Desktop notification**:
```json
{
  "hooks": {
    "Notification": [{
      "hooks": [{
        "type": "command",
        "command": "osascript -e 'display notification \"Claude needs input\" with title \"Claude Code\"'"
      }]
    }]
  }
}
```

## Hook Scripts

For complex logic, use external scripts. UV single-file format works well:

```python
#!/usr/bin/env -S uv run --script
# /// script
# dependencies = []
# requires-python = ">=3.11"
# ///

import json
import sys

data = json.load(sys.stdin)
tool_input = data.get("tool_input", {})

# Validation logic here

if should_block:
    print("Error message", file=sys.stderr)
    sys.exit(2)

sys.exit(0)
```

## Anti-Patterns

- Using exit code 2 without stderr message (Claude gets no feedback)
- Forgetting to handle JSON parsing errors in scripts
- Blocking without explaining why (Claude will retry the same thing)
- Long-running hooks without timeout (default is 60s)
- Modifying files in PreToolUse (use PostToolUse for modifications)

## Reference

- [references/anthropic-hooks.md](references/anthropic-hooks.md) - Complete reference (input schemas, prompt hooks, MCP tools)
- [references/anthropic-hooks-guide.md](references/anthropic-hooks-guide.md) - Quickstart and examples
