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
- Think about what Claude does NOT already know that this skill needs to provide. Show it as a suggestion to the user.
- Are there examples that should be included as reference material? You can search online or ask for the user input.

### 4. Propose Name and Description
Based on what the user described, SUGGEST:
- A skill name (the essence of what it does, extremely succinct, lowercase with hyphens)
- A description for discovery (see guidance below)

**Writing the description:**
The description is the primary trigger mechanism — Claude Code uses it to decide when to activate a skill from potentially 100+ installed skills. It must be lean and precise.

Distill the essential purpose. Don't echo the user's phrasing — capture the *gist* of what the skill is and when it should fire. Lead with what the skill does (third person), then include trigger context.

Evaluate the description through each lens:
- Gist: Does it capture what the skill IS, or is it echoing what the user said?
- Name + description as a pair: Read them together. Does the description add signal beyond the name, or just restate it?
- False positives: Could common words cause this to activate on unrelated tasks?
- False negatives: Would someone who needs this skill use words not in the description?
- Overfocus: Does mentioning a specific example make the skill seem narrower than it is?
- Human scan: If a user sees this in a list of 50 skills, can they instantly tell what it does?
- Every word earns its place: Read each word — if you remove it, does the description get worse? If not, remove it.

Write the description to `playground/{skill-name}-description-0.md`. Then apply all lenses — read back from the file before each pass. If any lens leads to a change, write the new version to `playground/{skill-name}-description-{N+1}.md` and run all lenses again. Stop when you see nothing further to improve.

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
description: [What it does]. Use when [trigger context]. (drop the second part if it's redundant with the first)
---
```
- Name: The essence of what the skill does. Lowercase, hyphens. Avoid verbose names.
- Description: Lean and precise. Third person. Lead with what the skill does, follow with trigger context. This is the primary triggering mechanism — revisit step 4 guidance if needed.

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
Save completed skill to `output_skills/[category]/[skill-name]/SKILL.md`.

Look at existing category folders in `output_skills/` and pick the best fit. Confirm with the user before saving. If none fit well, propose a new category — suggest your best pick, list alternatives you considered with brief reasons for rejecting them, then let the user decide.
