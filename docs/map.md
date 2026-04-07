# Skill Factory Structure

```
skill-factory/
├── CLAUDE.md                           # Agent instructions for this project
├── update-docs                         # Bash wrapper to update documentation
├── scripts/                            # Automation scripts
│   ├── sources.txt                     # URLs to fetch docs from
│   ├── fetch_anthropic_skill_docs.py   # Fetch latest Anthropic docs
│   └── fetch_skill_creator.py          # Fetch latest skill-creator from GitHub
├── docs/                               # All knowledge about creating skills
│   ├── knowledge/
│   │   ├── anthropic-skill-docs/       # Official Anthropic skill documentation
│   │   │   ├── overview.md             # What skills are, why they exist, core concepts
│   │   │   ├── skills.md               # Implementation syntax, structure, usage patterns
│   │   │   ├── best-practices.md       # Proven patterns, common pitfalls, guidelines
│   │   │   ├── sub-agents.md           # Subagent configuration (context: fork)
│   │   │   └── hooks-guide.md          # Hooks and skill integration
│   │   └── anthropic-skill-creator/     # Anthropic's skill-creator (eval infrastructure)
│   │       ├── SKILL.md                # Main skill-creator instructions
│   │       ├── agents/                 # Grader, comparator, analyzer agents
│   │       ├── scripts/                # Eval runner, benchmarks, description optimizer
│   │       ├── eval-viewer/            # HTML eval viewer and report generator
│   │       ├── references/             # JSON schemas for evals, grading, benchmarks
│   │       └── assets/                 # HTML templates for trigger eval review
│   ├── create_new_skill-process.md     # Instructions for creating skills
│   ├── create_evals-process.md        # Instructions for evaluating skills
│   ├── map.md                          # This file - repository structure
│   └── project.md                      # Project-specific information
└── output_skills/                      # Created skills organized by category
    ├── testing/
    │   ├── tdd/
    │   ├── nullables/
    │   ├── approval-tests/
    │   └── bdd-with-approvals/
    ├── design/
    │   ├── align/
    │   ├── collaborative-design/
    │   ├── event-modeling/
    │   └── hexagonal-architecture/
    ├── practices/
    │   ├── growing-outside-in-systems/
    │   ├── refactoring/
    │   └── refinement-loop/
    ├── ai/
    │   ├── ai-patterns/
    │   ├── creating-process-files/
    │   └── claude-code/                # subfolder for Claude Code-specific skills
    │       ├── creating-hooks/
    │       ├── launching-agent-teams/
    │       ├── refactoring-team/
    │       └── writing-statuslines/
    └── developer-tools/
        ├── git-worktrees/
        ├── using-uv/
        └── writing-bash-scripts/
```

Eval workspaces are created as siblings to skill directories, named `{skill-name}-workspace/` (e.g., `c4-diagrams-workspace/`). They are gitignored and not tracked.

## Purpose

- **docs/**: All instructional material and fetched dependencies for creating and evaluating skills
- **output_skills/**: Completed skills, each in a category subfolder. Symlinked to `~/.claude/skills/` via the `./skills` script
- **CLAUDE.md**: Project instructions — overrides the Anthropic skill-creator plugin
