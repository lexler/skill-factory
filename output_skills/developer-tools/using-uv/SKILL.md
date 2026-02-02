---
name: using-uv
description: Python package and project management with UV. Use when creating Python scripts, initializing projects, or managing dependencies.
---

# UV

UV is a fast Python package manager. Two modes:

## Scripts vs Projects

**Use scripts when:**
- Single .py file
- Quick utility, one-off task
- No shared dependencies across files

**Use projects when:**
- Multiple files, modules, or packages
- Team collaboration
- Need reproducible environments
- Building a library or application

## Scripts

Standalone Python files with inline dependencies (PEP 723).

```python
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = ["requests", "rich"]
# ///

import requests
from rich import print
```

Run: `uv run script.py`

See [references/scripts.md](references/scripts.md) for full guide.

## Projects

Structured Python with pyproject.toml and lockfile.

```bash
uv init myproject
cd myproject
uv add requests
uv run python main.py
```

Key files:
- `pyproject.toml` - metadata and dependencies
- `uv.lock` - exact versions for reproducibility
- `.python-version` - Python version

See [references/projects.md](references/projects.md) for full guide.

## Common Patterns

```bash
uv run pytest                     # Run in project env
uv add --dev pytest               # Dev dependency
uvx ruff check .                  # One-off tool execution
uv run --with rich script.py      # Script with ad-hoc dep
```
