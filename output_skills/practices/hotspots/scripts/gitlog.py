"""Parse `git log --numstat` output into commits with per-file changes."""

import re
import subprocess
from dataclasses import dataclass, field

HEADER = re.compile(r"^--(?P<hash>[0-9a-f]+)--(?P<date>\d{4}-\d{2}-\d{2})--(?P<author>.+)$")
NUMSTAT = re.compile(r"^(?P<added>\d+|-)\t(?P<deleted>\d+|-)\t(?P<path>.+)$")
BRACED_RENAME = re.compile(r"\{[^{}]* => (?P<new>[^{}]*)\}")
WHOLE_RENAME = re.compile(r"^.* => (?P<new>.+)$")

LOG_FORMAT = "--%h--%ad--%aN"


@dataclass
class FileChange:
    path: str
    added: int
    deleted: int


@dataclass
class Commit:
    hash: str
    date: str
    author: str
    changes: list = field(default_factory=list)


def normalize_rename(path):
    if "{" in path:
        collapsed = BRACED_RENAME.sub(lambda m: m.group("new"), path)
        return collapsed.replace("//", "/")
    whole = WHOLE_RENAME.match(path)
    if whole:
        return whole.group("new")
    return path


def parse_log(text):
    commits = []
    for line in text.splitlines():
        line = line.rstrip("\n")
        if not line:
            continue
        header = HEADER.match(line)
        if header:
            commits.append(Commit(header["hash"], header["date"], header["author"]))
            continue
        stat = NUMSTAT.match(line)
        if stat and commits:
            added = 0 if stat["added"] == "-" else int(stat["added"])
            deleted = 0 if stat["deleted"] == "-" else int(stat["deleted"])
            commits[-1].changes.append(FileChange(normalize_rename(stat["path"]), added, deleted))
    return commits


def read_log(repo, months, exclude_pathspecs=()):
    command = [
        "git", "-C", repo, "log", "--no-merges", "--no-renames",
        f"--since={months}.month", "--numstat", "--date=short",
        f"--pretty=format:{LOG_FORMAT}", "--", ".",
    ] + [f":(exclude){p}" for p in exclude_pathspecs]
    return subprocess.run(command, capture_output=True, text=True, check=True).stdout


def tracked_files(repo):
    output = subprocess.run(
        ["git", "-C", repo, "ls-files"], capture_output=True, text=True, check=True
    ).stdout
    return set(output.splitlines())
