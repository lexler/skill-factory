# Skill Factory Structure

```
skill-factory/
├── CLAUDE.md                           # Agent instructions for this project
├── update-docs                         # Bash wrapper to update documentation
├── scripts/                            # Automation scripts
│   ├── sources.txt                     # URLs to fetch docs from
│   └── fetch_anthropic_skill_docs.py   # Fetch latest Anthropic docs
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
│   ├── map.md                          # This file - repository structure
│   └── project.md                      # Project-specific information
└── output_skills/                      # Created skills organized by category
    ├── testing/                        # tdd, nullables, approval-tests, bdd-with-approvals
    ├── design/                         # hexagonal-architecture, event-modeling, collaborative-design
    ├── practices/                      # refactoring, refinement-loop
    ├── ai/                             # ai-patterns, creating-process-files
    │   └── claude-code/                # creating-hooks
    └── developer-tools/                # writing-bash-scripts, using-uv, git-worktrees
```

## Purpose

- **docs/**: Contains all instructional material the agent uses to create skills
- **output_skills/**: Stores completed skills, each in a category subfolder
- **CLAUDE.md**: Provides context to the agent about this repository's purpose
