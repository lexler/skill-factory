# Skill Factory Structure

```
skill-factory/
├── CLAUDE.md                           # Agent instructions for this project
├── scripts/                            # Automation scripts
│   └── fetch_anthropic_skill_docs.py   # Fetch latest Anthropic docs
├── docs/                               # All knowledge about creating skills
│   ├── knowledge/
│   │   └── anthropic-skill-docs/       # Official Anthropic skill documentation
│   │       ├── map.md                  # Guide to this folder
│   │       ├── sources.txt             # URLs to fetch docs from
│   │       ├── overview.md             # (fetched)
│   │       ├── skills.md               # (fetched)
│   │       ├── best-practices.md       # (fetched)
│   │       └── quickstart.md           # (fetched)
│   ├── map.md                          # This file - repository structure
│   └── project.md                      # Project-specific information
└── output_skills/                      # Created skills organized by name
    ├── tdd/
    ├── nullables/
    └── refactoring/
```

## Purpose

- **docs/**: Contains all instructional material the agent uses to create skills
- **output_skills/**: Stores completed skills, each in its own folder
- **CLAUDE.md**: Provides context to the agent about this repository's purpose
