# Create New Skill

STARTER_CHARACTER = 📚🧩

## Description

Create a Claude Code skill.

Skills are a context management mechanism. They package knowledge Claude needs for specific tasks while keeping context lean through progressive disclosure:
- **Startup**: Only name + description loaded (~100 tokens per skill)
- **When triggered**: Full SKILL.md instructions loaded
- **As needed**: References loaded only when the task requires them

This fights limited focus (LLMs can't attend to everything) and context rot (earlier instructions slip as conversations grow).

Skills are NOT slash commands - those are user-invoked prompts.

## Steps

### 1. Update Documentation
Run the update script to fetch the latest Anthropic skill docs:
```bash
./update-docs
```

### 2. Learn Skill Patterns
Read the official documentation in `docs/knowledge/anthropic-skill-docs/`:
- `overview.md` - Core concepts and architecture
- `skills.md` - Implementation patterns
- `best-practices.md` - Guidelines and pitfalls

### 3. Clarify the Goal
Ask the user:
- What specific task should Claude be able to do?
- Think about what does Claude NOT already know that this skill needs to provide. Show it as a suggestion to the user.
- Are there examples that should be included as reference material? You can search online or ask for the user input.

### 4. Propose Name and Description
Based on what the user described, SUGGEST:
- A skill name (the essence of what it does, extremely succinct, lowercase with hyphens)
- A description (what it does + trigger words users would say)

Present both for user approval before proceeding.

### 5. Research (if needed)
If the domain is unfamiliar:
- Gather domain knowledge first
- Identify patterns, terminology, and common workflows

### 6. Design Structure

**Skill anatomy:**
```
skill-name/
├── SKILL.md (required)
├── scripts/      - Executable code for deterministic operations
├── references/   - Detailed docs, examples, loaded as needed
└── assets/       - Templates, images used in output
```

Decide scope:
- **Single file**: Simple guidance, under 500 lines
- **Multi-file**: Complex domain with reference materials or scripts

**Do NOT include:** README.md, CHANGELOG.md, INSTALLATION_GUIDE.md, or other auxiliary documentation.

### 7. Write SKILL.md

**Frontmatter:**
```yaml
---
name: skill-name
description: [What it does]. Use when [trigger phrases user would say].
---
```
- Name: The essence of what the skill does. Lowercase, hyphens. Avoid verbose names.
- Description: Third person, specific, includes trigger words. This is the primary triggering mechanism.

**Body:**
- Start with `STARTER_CHARACTER = [emoji]` — This signals when the skill is active. Pick an emoji that represents the skill's purpose as much as possible.
- Concise instructions. Assume Claude is smart, but help guide and focus it by providing good order and progressive disclosure.
- Use principles + anti-examples, not good examples to copy (avoids collapsing solution space)
- Avoid markdown tables - use lists or prose instead (tables require rendering to read easily)
- Don't do question-based formatting ("Need X? Do Y")
- Try to avoid leading language ("When you want to...", "If you need...")
- Don't add hand-holding phrasing in attempt to provide hand-holding guidance. 

### 8. Add Supporting Files (if multi-file)

**References:** Detailed docs, loaded only when needed. Keep SKILL.md lean.

**Examples in references:** When including examples, add framing:
> "These illustrate the principle. Consider what fits your context."

**Scripts:** For operations that need deterministic reliability.

**One level deep means link chains, not folders.** SKILL.md should link directly to content files - avoid SKILL.md → index.md → actual-content.md chains. Organizing references into subfolders (`references/architecture/`, `references/building/`) is fine as long as SKILL.md links directly to each file.

### 9. Review Against Best Practices
Re-read `docs/knowledge/anthropic-skill-docs/best-practices.md` and `skills.md` (troubleshooting section). Compare to what you created:
- Does the description include clear trigger words?
- Is the body concise? Remove anything Claude already knows.
- Are references one level deep?
- Any anti-patterns present?

Suggest improvements before proceeding.

### 10. Install Skill
Ask user: **Global skill or project skill?**

**Global (symlink, personal, all projects):**
```bash
./skills install [skill-name]
```

**Project (copy, shared via git):**
```bash
./skills local install [skill-name]
```

Check status with `./skills status` or `./skills local status`.

Tell user to restart Claude Code to load the skill.

### 11. Test
- Restart Claude Code to load the skill
- Ask Claude to do a task that should trigger the skill
- Verify: Does it trigger? Does Claude follow instructions correctly?
- Try edge cases

### 12. Iterate
- Skill doesn't trigger → improve description with better trigger words
- Claude misses steps → make instructions more prominent
- Too verbose → remove what Claude already knows
Note any other issues and think broader. Read the skill documentation again, then read the skill definition, suggest improvements based on the issues seen. 

## Output
Save completed skill to: `output_skills/[skill-name]/SKILL.md`
