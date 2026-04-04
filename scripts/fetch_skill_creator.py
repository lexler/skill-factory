#!/usr/bin/env -S uv run --script
# /// script
# dependencies = ["requests>=2.31.0"]
# requires-python = ">=3.11"
# ///

import requests
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
REPO_ROOT = SCRIPT_DIR.parent
OUTPUT_DIR = REPO_ROOT / "docs" / "knowledge" / "anthropic-skill-creator"

REPO = "anthropics/claude-plugins-official"
BASE_PATH = "plugins/skill-creator/skills/skill-creator"
API_BASE = f"https://api.github.com/repos/{REPO}/contents"
TIMEOUT = 30


def fetch_directory(api_path, local_dir):
    url = f"{API_BASE}/{api_path}"
    response = requests.get(url, timeout=TIMEOUT)
    response.raise_for_status()

    for item in response.json():
        if item["type"] == "file":
            fetch_file(item["download_url"], local_dir / item["name"])
        elif item["type"] == "dir":
            fetch_directory(item["path"], local_dir / item["name"])


def fetch_file(download_url, output_path):
    output_path.parent.mkdir(parents=True, exist_ok=True)
    print(f"  {output_path.relative_to(REPO_ROOT)}")

    response = requests.get(download_url, timeout=TIMEOUT)
    response.raise_for_status()
    output_path.write_bytes(response.content)


def fetch_skill_creator():
    print(f"Fetching skill-creator from {REPO}...")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    fetch_directory(BASE_PATH, OUTPUT_DIR)
    print("Done.")


if __name__ == "__main__":
    fetch_skill_creator()
