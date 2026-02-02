---
name: creating-slash-commands
description: Creates Claude Code slash commands (custom prompts invoked with /). Use when creating custom commands, slash commands, command templates, or reusable prompts.
---

STARTER_CHARACTER = 📋

## Setup

First, update the reference docs to get the latest from Anthropic:
```bash
python ~/.claude/skills/creating-slash-commands/scripts/update-docs.py
```

## What Slash Commands Are

Single markdown files containing prompts that users invoke explicitly with `/command-name`. The filename (without `.md`) becomes the command name.

**Slash commands vs skills**: Commands are explicit user invocations for simple, single-file prompts. Skills are auto-discovered by Claude for complex multi-file capabilities. If unsure, default to slash command - simpler is better.

## File Locations

- **Project commands**: `.claude/commands/` - shared via git, show "(project)" in help
- **Personal commands**: `~/.claude/commands/` - cross-project, show "(user)" in help

Project commands override personal commands with the same name.

## Namespacing

Subdirectories create namespaced descriptions without changing the command name:
- `.claude/commands/frontend/test.md` creates `/test` showing "(project:frontend)"
- `.claude/commands/backend/test.md` creates `/test` showing "(project:backend)"

## Command Structure

```markdown
---
description: Brief description shown in /help
argument-hint: [required-arg] [optional-arg]
allowed-tools: Bash(git:*), Read
model: claude-opus-4-5-20251101
---

Your prompt instructions here.
Use $ARGUMENTS for all args, or $1, $2 for positional.
```

### Frontmatter Fields

- `description` - shown in `/help`, enables SlashCommand tool invocation
- `argument-hint` - shows expected parameters in autocomplete
- `allowed-tools` - tools permitted (required if using '!' bash execution)
- `model` - force specific model
- `disable-model-invocation` - prevent Claude from auto-invoking this command

## Dynamic Features

### Arguments

`$ARGUMENTS` captures everything after the command name:
```
/fix-issue 123 high-priority
# $ARGUMENTS = "123 high-priority"
```

Positional parameters for structured input:
```
/review-pr 456 high alice
# $1 = "456", $2 = "high", $3 = "alice"
```

### Bash Execution

Prefix with '!' to execute bash and inject output into context:
```markdown
---
allowed-tools: Bash(git:*)
---

Git version: !`git --version`
```

The `allowed-tools` frontmatter is required when using bash execution.

### File References

Use `@` to include file contents:
```markdown
Review @src/main.js against @docs/style-guide.md
```

## Anti-Patterns

- Creating a slash command when a skill is needed (multi-file workflows, scripts, validation steps)
- Missing `description` field (breaks SlashCommand tool and /help display)
- Using '!' bash without `allowed-tools` in frontmatter
- Overly complex multi-step logic (use a skill instead)
- Generic names without namespace context (use subdirectories)

## Common Patterns

**Git workflow commands**: Use bash execution to gather context (status, diff, log), then instruct Claude what to do with it

**Code quality commands**: Reference relevant files with `@`, specify what to check

**Model override**: Add `model: claude-opus-4-5-20251101` to force a specific model

**Shell aliases for speed**: `alias clint="claude -p '/lint'"` skips interactive mode

## Reference

For complete documentation including built-in commands, MCP integration, and plugin commands, see [references/anthropic-slash-commands.md](references/anthropic-slash-commands.md).
