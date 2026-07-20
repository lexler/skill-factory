#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""Mine git history into ranked hotspots: change frequency x complexity per file.

Usage: uv run mine.py [repo] [--months N] [--min-revs N] [--exclude PATTERN]...
Writes a JSON report to stdout (or --out FILE).
"""

import argparse
import json
import statistics
import sys
from dataclasses import dataclass, field
from fnmatch import fnmatch
from pathlib import Path, PurePosixPath

from gitlog import parse_log, read_log, tracked_files

DEFAULT_EXCLUDES = [
    "node_modules/**", "vendor/**", "third_party/**", "dist/**", "build/**",
    "target/**", "out/**", ".idea/**", "__snapshots__/**",
    "*.min.js", "*.min.css", "*.map", "*.svg", "*.lock",
    "package-lock.json", "yarn.lock", "pnpm-lock.yaml", "Gemfile.lock",
    "composer.lock", "go.sum", "*.pb.go", "*_pb2.py", "*.generated.*",
]

MAX_FILE_BYTES = 2_000_000
SPACES_PER_INDENT = 4
SHORT_HISTORY_COMMITS = 100


@dataclass
class FileStats:
    commits: int = 0
    added: int = 0
    deleted: int = 0
    authors: set = field(default_factory=set)
    last_change: str = ""


@dataclass
class Complexity:
    loc: int
    indent_total: int
    indent_mean: float
    indent_sd: float
    indent_max: int


def matches_any(path, patterns):
    name = PurePosixPath(path).name
    for pattern in patterns:
        if fnmatch(path, pattern):
            return True
        if "/" not in pattern and fnmatch(name, pattern):
            return True
    return False


def aggregate_changes(commits, tracked):
    stats = {}
    for commit in commits:
        for change in commit.changes:
            if change.path not in tracked:
                continue
            entry = stats.setdefault(change.path, FileStats())
            entry.commits += 1
            entry.added += change.added
            entry.deleted += change.deleted
            entry.authors.add(commit.author)
            entry.last_change = max(entry.last_change, commit.date)
    return stats


def logical_indent(line):
    indent = 0
    for char in line:
        if char == "\t":
            indent += SPACES_PER_INDENT
        elif char == " ":
            indent += 1
        else:
            break
    return indent // SPACES_PER_INDENT


def measure_complexity(source):
    lines = [line for line in source.splitlines() if line.strip()]
    if not lines:
        return Complexity(0, 0, 0.0, 0.0, 0)
    indents = [logical_indent(line) for line in lines]
    return Complexity(
        loc=len(lines),
        indent_total=sum(indents),
        indent_mean=round(statistics.mean(indents), 2),
        indent_sd=round(statistics.pstdev(indents), 2),
        indent_max=max(indents),
    )


def read_complexity(repo, paths):
    complexity = {}
    for path in paths:
        file = Path(repo) / path
        try:
            if file.stat().st_size > MAX_FILE_BYTES:
                continue
            data = file.read_bytes()
        except OSError:
            continue
        if b"\0" in data[:8000]:
            continue
        complexity[path] = measure_complexity(data.decode("utf-8", errors="replace"))
    return complexity


def percentile_ranks(values):
    ordered = sorted(values.values())
    n = len(ordered)
    ranks = {}
    for key, value in values.items():
        less = sum(1 for v in ordered if v < value)
        equal = sum(1 for v in ordered if v == value)
        ranks[key] = (less + 0.5 * equal) / n
    return ranks


def score_files(frequency, loc, min_revs):
    candidates = [
        path for path, revs in frequency.items() if revs >= min_revs and path in loc
    ]
    if not candidates:
        return []
    frequency_pct = percentile_ranks({p: frequency[p] for p in candidates})
    size_pct = percentile_ranks({p: loc[p] for p in candidates})
    median_frequency = statistics.median(frequency[p] for p in candidates)
    median_loc = statistics.median(loc[p] for p in candidates)

    def quadrant(path):
        active = frequency[path] >= median_frequency
        complex_ = loc[path] >= median_loc
        if active and complex_:
            return "hotspot"
        if complex_:
            return "stable-complex"
        if active:
            return "active-simple"
        return "quiet"

    rows = [
        {
            "path": path,
            "frequency_pct": round(frequency_pct[path], 3),
            "size_pct": round(size_pct[path], 3),
            "score": round(frequency_pct[path] * size_pct[path], 3),
            "quadrant": quadrant(path),
        }
        for path in candidates
    ]
    rows.sort(key=lambda r: (-r["score"], r["path"]))
    for position, row in enumerate(rows, start=1):
        row["rank"] = position
    return rows


def stable_complex_files(frequency, loc, min_revs, top):
    quiet = [path for path in loc if frequency.get(path, 0) < min_revs]
    quiet.sort(key=lambda p: -loc[p])
    return [
        {"path": path, "loc": loc[path], "commits": frequency.get(path, 0)}
        for path in quiet[:top]
    ]


def build_report(repo, commits, tracked, excludes, min_revs, months, top_stable):
    kept = {path for path in tracked if not matches_any(path, excludes)}
    stats = aggregate_changes(commits, kept)
    complexity = read_complexity(repo, kept)
    frequency = {path: entry.commits for path, entry in stats.items()}
    loc = {path: c.loc for path, c in complexity.items()}

    rows = score_files(frequency, loc, min_revs)
    for row in rows:
        entry, measured = stats[row["path"]], complexity[row["path"]]
        row.update(
            commits=entry.commits, added=entry.added, deleted=entry.deleted,
            authors=len(entry.authors), last_change=entry.last_change,
            loc=measured.loc, indent_total=measured.indent_total,
            indent_mean=measured.indent_mean, indent_sd=measured.indent_sd,
            indent_max=measured.indent_max,
        )

    warnings = []
    if len(commits) < SHORT_HISTORY_COMMITS:
        warnings.append(
            f"Only {len(commits)} commits in window: rankings are unreliable; widen --months."
        )
    if not rows:
        warnings.append("No files passed the min-revs floor; nothing to rank.")

    return {
        "repo": str(Path(repo).resolve()),
        "window_months": months,
        "params": {"min_revs": min_revs, "excludes": excludes},
        "summary": {
            "commits_analyzed": len(commits),
            "files_changed": len(stats),
            "files_ranked": len(rows),
            "warnings": warnings,
        },
        "files": rows,
        "stable_complex": stable_complex_files(frequency, loc, min_revs, top_stable),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("repo", nargs="?", default=".")
    parser.add_argument("--months", type=int, default=12)
    parser.add_argument("--min-revs", type=int, default=5)
    parser.add_argument("--exclude", action="append", default=[])
    parser.add_argument("--no-default-excludes", action="store_true")
    parser.add_argument("--top-stable", type=int, default=20)
    parser.add_argument("--out")
    args = parser.parse_args()

    excludes = args.exclude if args.no_default_excludes else DEFAULT_EXCLUDES + args.exclude
    commits = parse_log(read_log(args.repo, args.months))
    tracked = tracked_files(args.repo)
    report = build_report(
        args.repo, commits, tracked, excludes, args.min_revs, args.months, args.top_stable
    )
    write_report(report, args.out)


def write_report(report, out):
    output = json.dumps(report, indent=2)
    if out:
        Path(out).parent.mkdir(parents=True, exist_ok=True)
        Path(out).write_text(output + "\n")
    else:
        sys.stdout.write(output + "\n")


if __name__ == "__main__":
    main()
