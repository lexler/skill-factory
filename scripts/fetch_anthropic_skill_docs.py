#!/usr/bin/env -S uv run --script
# /// script
# dependencies = ["requests>=2.31.0"]
# requires-python = ">=3.11"
# ///

import requests
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
DOCS_DIR = REPO_ROOT / "docs" / "knowledge" / "anthropic-skill-docs"
SOURCES_FILE = DOCS_DIR / "sources.txt"
OUTPUT_DIR = DOCS_DIR

def fetch_docs():
    if not SOURCES_FILE.exists():
        print(f"Error: {SOURCES_FILE} not found")
        return

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    with open(SOURCES_FILE) as f:
        urls = [line.strip() for line in f if line.strip()]

    for url in urls:
        filename = url.split("/")[-1]
        output_path = OUTPUT_DIR / filename

        print(f"Fetching {filename}...")
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()

            output_path.write_text(response.text, encoding="utf-8")
            print(f"  ✓ Saved to {output_path}")
        except requests.RequestException as e:
            print(f"  ✗ Failed: {e}")

if __name__ == "__main__":
    fetch_docs()
