#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# ///
"""Create the next iteration-N directory under an eval workspace.

Always creates a fresh directory; never writes where outputs or feedback
already live. This keeps each round's outputs (and the feedback.json pinned
to them) welded to the version they describe, instead of bleeding stale
feedback onto regenerated outputs.
"""

import re
import sys
from pathlib import Path

ITERATION_PATTERN = re.compile(r"^iteration-(\d+)$")


def highest_iteration(base: Path) -> int:
    """Highest N among existing iteration-N dirs, or 0 if none."""
    if not base.is_dir():
        return 0
    numbers = [
        int(m.group(1))
        for child in base.iterdir()
        if child.is_dir() and (m := ITERATION_PATTERN.match(child.name))
    ]
    return max(numbers, default=0)


def next_iteration_dir(base: Path) -> Path:
    """Create and return base/iteration-(highest+1). Never touches existing dirs."""
    base = Path(base)
    target = base / f"iteration-{highest_iteration(base) + 1}"
    target.mkdir(parents=True, exist_ok=False)
    return target


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: next_iteration.py <workspace-base-dir>", file=sys.stderr)
        return 2
    print(next_iteration_dir(Path(argv[1])))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
