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
from patch_eval_viewer import UPSTREAM_BLOCK, PATCHED_BLOCK, PatchTargetChanged, apply_inline_text_patch


def viewer_file(tmp_path, body):
    path = tmp_path / "generate_review.py"
    path.write_text(f"def embed_file(path):\n{body}")
    return path


def test_patches_upstream_content(tmp_path):
    path = viewer_file(tmp_path, UPSTREAM_BLOCK)
    assert apply_inline_text_patch(path) == "patched"
    content = path.read_text()
    assert PATCHED_BLOCK in content
    assert UPSTREAM_BLOCK not in content


def test_second_run_is_a_no_op(tmp_path):
    path = viewer_file(tmp_path, UPSTREAM_BLOCK)
    apply_inline_text_patch(path)
    before = path.read_text()
    assert apply_inline_text_patch(path) == "already patched"
    assert path.read_text() == before


def test_unrecognized_content_raises(tmp_path):
    path = viewer_file(tmp_path, "    else:\n        something_new_from_upstream()\n")
    with pytest.raises(PatchTargetChanged):
        apply_inline_text_patch(path)


def test_cli_patches_and_reports(tmp_path):
    path = viewer_file(tmp_path, UPSTREAM_BLOCK)
    script = Path(__file__).resolve().parent / "patch_eval_viewer.py"
    out = subprocess.run(
        [sys.executable, str(script), str(path)],
        capture_output=True,
        text=True,
    )
    assert out.returncode == 0, out.stderr
    assert "patched" in out.stdout
    assert PATCHED_BLOCK in path.read_text()


def test_cli_fails_loudly_on_changed_upstream(tmp_path):
    path = viewer_file(tmp_path, "    else:\n        something_new_from_upstream()\n")
    script = Path(__file__).resolve().parent / "patch_eval_viewer.py"
    out = subprocess.run(
        [sys.executable, str(script), str(path)],
        capture_output=True,
        text=True,
    )
    assert out.returncode != 0
    assert "upstream" in out.stderr.lower()


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-q"]))
