# Skill Factory

Creates Claude Code skills with built-in best practices from Anthropic's official documentation.

## Why Skills?

Claude can't hold everything in mind at once. Squirrel!

Skills solve the problem of distracted agent by releasing information gradually:
1. **Startup**: Only name + description loaded (~100 tokens per skill)
2. **When triggered**: Full instructions loaded
3. **As needed**: References loaded only when the task requires them

This keeps context lean while making rich knowledge available on demand.

**Skills vs slash commands**: 
- Skills are model-invoked (Claude applies them when relevant based on the frontmatter and then relevant links in SKILL.md). 
- Slash commands are user-invoked (`/command`).

## Quick Start

1. Open this folder in Claude Code
2. Ask it to create a new skill
3. Answer a few questions — point to references or ask Claude to search online
4. Find your skill in `output_skills/[skill-name]/`

## Using Your Skill

This repo includes a `./skills` helper script for global installation.

**Global** (all projects) — use the script to symlink to `~/.claude/skills/`:

```bash
./skills toggle    # interactive picker
./skills status    # check what's installed
```

Edits to `output_skills/` apply immediately since it's a symlink.

**Local** (single project) — copy the skill folder to your project's `.claude/skills/` or create a symlink in your project yourself.

## STARTER_CHARACTER

Each skill defines a `STARTER_CHARACTER = [emoji]` at the top. This is a visual indicator that Claude has loaded the skill and is following its instructions. For example, the nullables skill uses ⭕️ and TDD uses 🔴/🌱/🌀.

To activate this, add the following to your global `~/.claude/CLAUDE.md`:

```
Always start replies with STARTER_CHARACTER + space (default: 🍀). Stack emojis when requested, don't replace.
```

Pick any default emoji you like — it confirms Claude is reading your ground rules. When a skill activates, its emoji stacks on top: `🍀 ⭕️` means both your global rules and the nullables skill are active.

Without this line in your global CLAUDE.md, the `STARTER_CHARACTER` lines in skills might have unpredictable behavior.

## Updating Best Practices

```bash
./update-docs
```

Pulls latest skill patterns from Anthropic.

## Structure

```
docs/           — Skill creation knowledge and patterns
output_skills/  — Generated skills (your output)
```
