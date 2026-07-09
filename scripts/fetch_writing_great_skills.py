#!/usr/bin/env -S uv run --script
# /// script
# dependencies = ["requests>=2.31.0"]
# requires-python = ">=3.11"
# ///

import requests
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
REPO_ROOT = SCRIPT_DIR.parent
OUTPUT_DIR = REPO_ROOT / "docs" / "knowledge" / "writing-great-skills"

REPO = "mattpocock/skills"
SKILL_PATH = "skills/productivity/writing-great-skills"
API_BASE = f"https://api.github.com/repos/{REPO}/contents"
TIMEOUT = 30

ATTRIBUTION = f"""# Attribution

The files in this folder are vendored verbatim from
https://github.com/{REPO} ({SKILL_PATH}/),
written by Matt Pocock and licensed under MIT (see LICENSE).

Do not edit them here — run `./update-docs` to refresh from upstream.
"""


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


def fetch_license():
    url = f"{API_BASE}/LICENSE"
    response = requests.get(url, timeout=TIMEOUT)
    response.raise_for_status()
    fetch_file(response.json()["download_url"], OUTPUT_DIR / "LICENSE")


def fetch_writing_great_skills():
    print(f"Fetching writing-great-skills from {REPO}...")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    fetch_directory(SKILL_PATH, OUTPUT_DIR)
    fetch_license()
    (OUTPUT_DIR / "ATTRIBUTION.md").write_text(ATTRIBUTION)
    print(f"  {OUTPUT_DIR.relative_to(REPO_ROOT) / 'ATTRIBUTION.md'}")
    print("Done.")


if __name__ == "__main__":
    fetch_writing_great_skills()
