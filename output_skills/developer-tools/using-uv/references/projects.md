# UV Projects

Structured Python development with pyproject.toml, lockfiles, and virtual environments.

## Contents
- Project structure
- Initialization
- Dependency management
- Running commands
- Development dependencies
- Syncing and locking
- Building and publishing
- Workspaces
- Configuration

## Project Structure

```
myproject/
├── pyproject.toml      # Project metadata and dependencies
├── uv.lock             # Exact versions (cross-platform)
├── .python-version     # Python version for the project
├── .venv/              # Virtual environment
├── src/
│   └── myproject/
│       └── __init__.py
└── tests/
```

## Initialization

```bash
uv init myproject                     # New project
uv init                               # Current directory
uv init --lib myproject               # Library (src layout)
uv init --app myproject               # Application
```

## Dependency Management

```bash
uv add requests                       # Add dependency
uv add 'requests>=2.28,<3'            # With version constraint
uv add requests rich httpx            # Multiple at once
uv remove requests                    # Remove dependency
uv add -r requirements.txt            # From requirements file
```

Git/URL sources:
```bash
uv add git+https://github.com/user/repo
uv add git+https://github.com/user/repo@v1.0.0
```

## Running Commands

```bash
uv run python main.py                 # Run Python
uv run pytest                         # Run pytest
uv run uvicorn main:app --reload      # Run any command
```

`uv run` automatically:
1. Verifies lockfile matches pyproject.toml
2. Syncs environment with lockfile
3. Executes command

## Development Dependencies

```bash
uv add --dev pytest pytest-cov        # Dev dependencies
uv add --dev ruff mypy                # Linting/typing
```

In pyproject.toml:
```toml
[dependency-groups]
dev = ["pytest", "ruff", "mypy"]
```

Sync with/without dev:
```bash
uv sync                               # Includes dev by default
uv sync --no-dev                      # Production only
```

## Syncing and Locking

```bash
uv sync                               # Install from lockfile
uv lock                               # Update lockfile
uv lock --upgrade                     # Upgrade all packages
uv lock --upgrade-package requests    # Upgrade specific package
```

## One-off Tool Execution

```bash
uvx ruff check .                      # Run tool without installing
uvx black .                           # Format code
uvx mypy src/                         # Type check
```

`uvx` runs tools in isolated environments.

## Building and Publishing

```bash
uv build                              # Create dist/
uv publish                            # Publish to PyPI
```

Creates:
- `dist/myproject-0.1.0.tar.gz` (source)
- `dist/myproject-0.1.0-py3-none-any.whl` (wheel)

## Workspaces

Monorepo with multiple packages sharing a lockfile:

```
monorepo/
├── pyproject.toml          # Workspace root
├── uv.lock                 # Shared lockfile
├── packages/
│   ├── core/
│   │   └── pyproject.toml
│   └── api/
│       └── pyproject.toml
```

Root pyproject.toml:
```toml
[tool.uv.workspace]
members = ["packages/*"]
```

Reference workspace members:
```toml
[project]
dependencies = ["core"]

[tool.uv.sources]
core = { workspace = true }
```

## Configuration

pyproject.toml `[tool.uv]` section:

```toml
[tool.uv]
package = true                        # Force packaging

[tool.uv.sources]
mylib = { path = "../mylib" }         # Local path
private = { git = "https://..." }     # Git source
```

Platform constraints:
```toml
[tool.uv]
environments = [
    "sys_platform == 'darwin'",
    "sys_platform == 'linux'",
]
```

## Python Version Management

```bash
uv python install 3.12                # Install Python
uv python list                        # Show available
uv python pin 3.12                    # Set for project
```

In pyproject.toml:
```toml
[project]
requires-python = ">=3.11"
```
