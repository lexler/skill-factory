# Skill Factory Structure

```
skill-factory/
├── CLAUDE.md                           # Agent instructions for this project
├── docs/                               # All knowledge about creating skills
│   ├── knowledge/
│   │   └── anthropic-skill-docs/       # Official Anthropic skill documentation
│   │       ├── README.md               # Guide to the documentation
│   │       ├── sources.txt             # URLs to fetch docs from
│   │       ├── update_docs.py          # Script to fetch latest docs
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
