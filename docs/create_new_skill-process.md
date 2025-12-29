# Create New Skill

STARTER_CHARACTER = 🎯

## Description

Create a Claude Code skill that works effectively. Skills teach Claude domain-specific expertise that triggers automatically when relevant.

## Steps

### 1. Clarify the Goal
- What specific task should Claude be able to do?
- When should this skill trigger? (What would a user say?)
- What does Claude NOT already know that this skill needs to provide?

### 2. Research (if needed)
- If the domain is unfamiliar, gather knowledge first
- Identify patterns, terminology, and common workflows
- Find examples of good/bad approaches

### 3. Design Structure
Decide scope:
- **Single file**: Simple guidance, under 500 lines
- **Multi-file**: Complex domain with reference materials, scripts, or conditional workflows

### 4. Write SKILL.md
```yaml
---
name: doing-the-thing
description: [What it does]. Use when [trigger phrases user would say].
---
```
- Name: lowercase, hyphens, gerund form preferred (e.g., `processing-pdfs`)
- Description: Third person, specific, includes trigger words
- Body: Concise instructions. Assume Claude is smart.

### 5. Add Supporting Files (if multi-file)
- Reference docs for detailed information
- Utility scripts for deterministic operations
- Keep references one level deep from SKILL.md

### 6. Test
- Ask Claude to do a task that should trigger the skill
- Verify: Does it trigger? Does Claude follow instructions correctly?
- Try edge cases

### 7. Iterate
- If skill doesn't trigger → improve description with better trigger words
- If Claude misses steps → make instructions more prominent
- If too verbose → remove what Claude already knows

## Output
Save completed skill to: `output_skills/[skill-name]/SKILL.md`

## Reference
Read `docs/knowledge/anthropic-skill-docs/` for official patterns and best practices.
