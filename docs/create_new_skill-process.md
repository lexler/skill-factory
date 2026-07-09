# Create New Skill

STARTER_CHARACTER = 📚

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

Then read `docs/knowledge/writing-great-skills/SKILL.md` and its `GLOSSARY.md` — the authoring theory this process builds on: invocation choice, information hierarchy, leading words, failure modes. Vendored from [mattpocock/skills](https://github.com/mattpocock/skills) by Matt Pocock (MIT).

### 3. Clarify the Goal
Ask the user:
- What specific task should Claude be able to do?
- Think about what Claude does NOT already know that this skill needs to provide. Show it as a suggestion to the user.
- Are there examples that should be included as reference material? You can search online or ask for the user input.

### 4. Choose Invocation, Propose Name and Description

**Invocation first.** Decide who fires the skill:
- Model-invoked (default): the agent triggers it from the description, and other skills can reach it. The description sits in context every turn — it must earn that load.
- User-invoked (`disable-model-invocation: true`): only the user, typing its name, fires it. Zero context load; the description becomes a human-facing one-liner and the trigger guidance below doesn't apply.

Pick model-invocation only when the agent or another skill must reach the skill on its own.

Based on what the user described, SUGGEST:
- A skill name (the essence of what it does, extremely succinct, lowercase with hyphens)
- A description for discovery (see guidance below)

**Writing the description:**
The description is the primary trigger mechanism — Claude Code uses it to decide when to activate a skill from potentially 100+ installed skills. It must be lean and precise.

Distill the essential purpose. Don't echo the user's phrasing — capture the *gist* of what the skill is and when it should fire. Lead with what the skill does (third person), then include trigger context.

Evaluate the description through each lens:
- Gist: Does it capture what the skill IS, or is it echoing what the user said?
- Leading word: The skill's anchor concept opens the description and does the invocation work.
- One trigger per branch: Synonyms that rename the same use case are duplication — keep only genuinely distinct branches.
- Name + description as a pair: Read them together. Does the description add signal beyond the name, or just restate it?
- False positives: Could common words cause this to activate on unrelated tasks?
- False negatives: Would someone who needs this skill use words not in the description?
- Overfocus: Does mentioning a specific example make the skill seem narrower than it is?
- Human scan: If a user sees this in a list of 50 skills, can they instantly tell what it does?
- Every word earns its place: Read each word — if you remove it, does the description get worse? If not, remove it.

Each iteration of the description goes to its own file: `playground/{skill-name}-description-{N}.md`. Write your first draft, then apply all lenses — read back from the file before each pass. If any lens leads to a change, write the new version to the next `{N}` and run all lenses again. Each iteration gets its own file so the trail stays intact. Stop when you see nothing further to improve.

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
- End each step on a completion criterion the agent can check — exhaustive where it matters ("every modified model accounted for", not "produce a change list"). A vague criterion invites premature completion.
- Collapse restatements into a leading word — one pretrained concept the agent thinks with (a *tight* loop, the test goes *red*). Reuse it in the description so invocation and execution share the anchor.
- Prompt the positive: state the target behaviour directly. Keep a prohibition only as a hard guardrail you can't phrase positively, and pair it with what to do instead.
- Use principles + anti-examples, not good examples to copy (avoids collapsing solution space)
- Write declarative instructions in plain prose; lists over markdown tables (tables require rendering to read easily)

### 8. Add Supporting Files (if multi-file)

**References:** Detailed docs, loaded only when needed. The branch test decides what moves out: inline what every run needs; push behind a context pointer what only some branches reach. The pointer's wording, not its target, decides whether the agent follows it — say what the file holds and when to read it.

**Examples in references:** When including examples, add framing:
> "These illustrate the principle. Consider what fits your context."

**Scripts:** For operations that need deterministic reliability.

**One level deep means link chains, not folders.** SKILL.md should link directly to content files - avoid SKILL.md → index.md → actual-content.md chains. Organizing references into subfolders (`references/architecture/`, `references/building/`) is fine as long as SKILL.md links directly to each file.

### 9. Review Against Best Practices
First run the mechanical frontmatter check — it catches invalid YAML, disallowed keys, name/description limits, and angle brackets in the description:
```bash
uv run --with pyyaml docs/knowledge/anthropic-skill-creator/scripts/quick_validate.py output_skills/{category}/{skill-name}
```

Then re-read `docs/knowledge/anthropic-skill-docs/best-practices.md` and `skills.md` (troubleshooting section). Compare to what you created:
- Does the description include clear trigger words?
- Run the no-op test sentence by sentence: does this sentence change behaviour versus what Claude does by default? Delete failing sentences whole — rewriting them just shrinks the no-op.
- Single source of truth: each meaning lives in one place, so changing a behaviour is a one-place edit.
- Are references one level deep?
- Any anti-patterns present?

Suggest improvements before proceeding.

### 10. Evaluate (optional)
Ask the user if they'd like to create evals for this skill. Explain that evals are realistic test prompts paired with assertions about expected output — they measure whether the skill actually improves Claude's behavior compared to baseline, track quality across iterations, and catch regressions. If yes, follow `docs/create_evals-process.md`.

### 11. Install Skill (optional)
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

### 12. Test
- Restart Claude Code to load the skill
- Ask Claude to do a task that should trigger the skill
- Verify: Does it trigger? Does Claude follow instructions correctly?
- Try edge cases

### 13. Iterate
Diagnose observed problems against the failure modes (full definitions in `docs/knowledge/writing-great-skills/SKILL.md`):
- Doesn't trigger → sharpen the description: leading word up front, one trigger per branch
- Rushes or skips steps → premature completion: sharpen the completion criterion first; split the sequence only if the criterion is irreducibly fuzzy and the rush persists
- Same meaning in several places → duplication: collapse to a single source of truth, or into a leading word
- Lines that no longer bear on what the skill does → sediment: prune
- Every line live, skill still too long → sprawl: disclose reference behind pointers, split by branch
- Lines Claude obeys by default → no-ops: delete
- Steering by prohibition → negation: restate as the target behaviour

## Output
Save completed skill to `output_skills/[category]/[skill-name]/SKILL.md`.

Look at existing category folders in `output_skills/` and pick the best fit. Confirm with the user before saving. If none fit well, propose a new category — suggest your best pick, list alternatives you considered with brief reasons for rejecting them, then let the user decide.
