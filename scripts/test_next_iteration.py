#!/usr/bin/env -S uv run --script
# /// script
# dependencies = ["pytest>=8"]
# requires-python = ">=3.11"
# ///

import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from next_iteration import next_iteration_dir


def test_empty_base_creates_iteration_1(tmp_path):
    result = next_iteration_dir(tmp_path)
    assert result == tmp_path / "iteration-1"
    assert result.is_dir()


def test_increments_past_highest(tmp_path):
    (tmp_path / "iteration-1").mkdir()
    (tmp_path / "iteration-2").mkdir()
    assert next_iteration_dir(tmp_path) == tmp_path / "iteration-3"


def test_ignores_non_iteration_dirs(tmp_path):
    (tmp_path / "current-evals").mkdir()
    (tmp_path / "meditate").mkdir()
    assert next_iteration_dir(tmp_path) == tmp_path / "iteration-1"


def test_uses_max_not_count_on_gaps(tmp_path):
    (tmp_path / "iteration-1").mkdir()
    (tmp_path / "iteration-3").mkdir()
    assert next_iteration_dir(tmp_path) == tmp_path / "iteration-4"


def test_never_overwrites_existing(tmp_path):
    first = next_iteration_dir(tmp_path)
    (first / "marker.txt").write_text("keep me")
    second = next_iteration_dir(tmp_path)
    assert second != first
    assert (first / "marker.txt").read_text() == "keep me"


def test_creates_base_if_missing(tmp_path):
    base = tmp_path / "does-not-exist-yet"
    result = next_iteration_dir(base)
    assert result == base / "iteration-1"
    assert result.is_dir()


def test_cli_prints_created_path(tmp_path):
    script = Path(__file__).resolve().parent / "next_iteration.py"
    out = subprocess.run(
        [sys.executable, str(script), str(tmp_path)],
        capture_output=True,
        text=True,
    )
    assert out.returncode == 0, out.stderr
    assert out.stdout.strip() == str(tmp_path / "iteration-1")
    assert (tmp_path / "iteration-1").is_dir()


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-q"]))
