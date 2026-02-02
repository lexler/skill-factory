#!/usr/bin/env -S uv run --script
# /// script
# dependencies = ["requests>=2.31.0"]
# requires-python = ">=3.11"
# ///

from pathlib import Path
import requests

SCRIPT_DIR = Path(__file__).parent
SKILL_ROOT = SCRIPT_DIR.parent
REFERENCES_DIR = SKILL_ROOT / "references"

SOURCES = [
    ("https://code.claude.com/docs/en/slash-commands.md", "anthropic-slash-commands.md"),
]

def fetch_docs():
    REFERENCES_DIR.mkdir(parents=True, exist_ok=True)

    for url, filename in SOURCES:
        output_path = REFERENCES_DIR / filename

        print(f"Fetching {filename}...")
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()

            output_path.write_text(response.text, encoding="utf-8")
            print(f"  Saved to {output_path}")
        except requests.RequestException as e:
            print(f"  Failed: {e}")

if __name__ == "__main__":
    fetch_docs()
