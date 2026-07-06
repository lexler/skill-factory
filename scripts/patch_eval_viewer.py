#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# ///
"""Re-apply our local fix to Anthropic's eval viewer after ./update-docs.

Upstream renders only known text extensions inline; extensionless outputs
(bash scripts like `cleanup-logs`) become download-only blobs, which makes
code review in the viewer impossible. This patch teaches embed_file to
render any UTF-8-decodable unknown file as inline text.

Runs as part of ./update-docs so the fix survives every doc refresh.
Fails loudly if upstream's embed_file changed shape — then the patch (or
the fix itself, if upstream fixed it) needs a human look.
"""

import sys
from pathlib import Path

VIEWER_PATH = (
    Path(__file__).resolve().parent.parent
    / "docs/knowledge/anthropic-skill-creator/eval-viewer/generate_review.py"
)

UPSTREAM_BLOCK = '''    else:
        # Binary / unknown — base64 download link
        try:
            raw = path.read_bytes()
            b64 = base64.b64encode(raw).decode("ascii")
        except OSError:
            return {"name": path.name, "type": "error", "content": "(Error reading file)"}
        return {
            "name": path.name,
            "type": "binary",
            "mime": mime,
            "data_uri": f"data:{mime};base64,{b64}",
        }
'''

PATCHED_BLOCK = '''    else:
        try:
            raw = path.read_bytes()
        except OSError:
            return {"name": path.name, "type": "error", "content": "(Error reading file)"}
        # Extensionless scripts and other unknown files that decode as text
        # render inline instead of hiding behind a download link
        try:
            content = raw.decode("utf-8")
            if "\\x00" not in content:
                return {"name": path.name, "type": "text", "content": content}
        except UnicodeDecodeError:
            pass
        # Binary — base64 download link
        b64 = base64.b64encode(raw).decode("ascii")
        return {
            "name": path.name,
            "type": "binary",
            "mime": mime,
            "data_uri": f"data:{mime};base64,{b64}",
        }
'''


class PatchTargetChanged(Exception):
    """Upstream's embed_file no longer matches what this patch expects."""


def apply_inline_text_patch(viewer_path: Path) -> str:
    content = viewer_path.read_text()
    if PATCHED_BLOCK in content:
        return "already patched"
    if UPSTREAM_BLOCK not in content:
        raise PatchTargetChanged(
            f"{viewer_path} has neither the upstream nor the patched embed_file block. "
            "Upstream changed — review whether the inline-text fix is still needed "
            "and update patch_eval_viewer.py."
        )
    viewer_path.write_text(content.replace(UPSTREAM_BLOCK, PATCHED_BLOCK))
    return "patched"


def main(argv: list[str]) -> int:
    viewer_path = Path(argv[1]) if len(argv) > 1 else VIEWER_PATH
    try:
        result = apply_inline_text_patch(viewer_path)
    except PatchTargetChanged as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1
    print(f"eval viewer inline-text fix: {result}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
