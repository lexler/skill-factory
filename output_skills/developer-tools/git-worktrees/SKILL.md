---
name: git-worktrees
description: Creates git worktrees for parallel development. Use when creating a git worktree, setting up multiple working directories, or working on features in parallel.
---

# Git Worktrees

## Directory Convention

Worktrees live in a sibling directory named `<project>_worktrees`:

```
parent/
├── myproject/              # main repo
└── myproject_worktrees/    # worktrees directory
    ├── feature_1/
    └── feature_2/
```

## Branch Naming

Use `<feature>_<N>` pattern when creating multiple worktrees:
- `auth-refactor_1`, `auth-refactor_2`
- `api-migration_1`, `api-migration_2`

## Workflow

1. Get project name from current directory
2. Create worktrees directory if needed: `../<project>_worktrees/`
3. Create worktree with new branch: `git worktree add <path> -b <branch>`

## Creating Multiple Worktrees

When asked for N worktrees for a feature:

```bash
PROJECT=$(basename "$PWD")
WORKTREES_DIR="../${PROJECT}_worktrees"
mkdir -p "$WORKTREES_DIR"

for i in $(seq 1 N); do
    git worktree add "${WORKTREES_DIR}/<feature>_${i}" -b "<feature>_${i}"
done
```

## Cleanup

Remove worktree and branch:
```bash
git worktree remove <path>
git branch -d <branch>
```

List all worktrees: `git worktree list`
