# Important Notes for This Repo

## No Markdown Tables in Skill Files

Don't use markdown tables in SKILL.md or reference files. Use lists or prose instead.

**Why:** Tables require rendering to read easily. When working in bash/terminal, raw markdown tables are hard to scan. Lists and prose are readable without a separate tool.

## approval-tests: 2-Level Reference Depth is Intentional

The approval-tests skill has this structure:
```
SKILL.md → python.md → references/python/*.md
           nodejs.md → references/nodejs/*.md
           java.md   → references/java/*.md
```

This is 2 levels deep from SKILL.md, not 1. This is **intentional, not a bug**.

**Why:** The three languages have very different implementations. The middle layer (python.md, nodejs.md, java.md) acts as a language router, keeping SKILL.md clean of language-specific details. Without this, SKILL.md would be polluted with implementation differences that only matter to users of specific languages.
