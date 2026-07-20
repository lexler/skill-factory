#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""Find change coupling: files that keep changing in the same commits.

Usage: uv run coupling.py [repo] [--months N] [--min-revs N] [--min-shared N]
                          [--min-coupling PCT] [--max-changeset-size N]
Writes a JSON report to stdout (or --out FILE).
"""

import argparse
from collections import Counter
from itertools import combinations
from pathlib import Path

from gitlog import parse_log, read_log, tracked_files
from mine import DEFAULT_EXCLUDES, matches_any, write_report


def changesets(commits, tracked, max_size):
    sets = []
    for commit in commits:
        paths = {change.path for change in commit.changes if change.path in tracked}
        if paths and len(paths) <= max_size:
            sets.append(paths)
    return sets


def coupled_pairs(sets, min_revs, min_shared, min_coupling):
    revisions = Counter()
    shared = Counter()
    for paths in sets:
        revisions.update(paths)
        shared.update(frozenset(pair) for pair in combinations(sorted(paths), 2))

    pairs = []
    for pair, count in shared.items():
        a, b = sorted(pair)
        if revisions[a] < min_revs or revisions[b] < min_revs or count < min_shared:
            continue
        degree = round(100 * count / ((revisions[a] + revisions[b]) / 2))
        if degree < min_coupling:
            continue
        pairs.append(
            {"a": a, "b": b, "shared": count, "degree": degree,
             "revs_a": revisions[a], "revs_b": revisions[b]}
        )
    pairs.sort(key=lambda p: (-p["degree"], -p["shared"], p["a"]))
    return pairs


def sum_of_coupling(sets):
    soc = Counter()
    for paths in sets:
        for path in paths:
            soc[path] += len(paths) - 1
    ranked = [{"path": path, "soc": count} for path, count in soc.items() if count > 0]
    ranked.sort(key=lambda r: (-r["soc"], r["path"]))
    return ranked


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("repo", nargs="?", default=".")
    parser.add_argument("--months", type=int, default=12)
    parser.add_argument("--min-revs", type=int, default=5)
    parser.add_argument("--min-shared", type=int, default=5)
    parser.add_argument("--min-coupling", type=int, default=30)
    parser.add_argument("--max-changeset-size", type=int, default=30)
    parser.add_argument("--exclude", action="append", default=[])
    parser.add_argument("--no-default-excludes", action="store_true")
    parser.add_argument("--out")
    args = parser.parse_args()

    excludes = args.exclude if args.no_default_excludes else DEFAULT_EXCLUDES + args.exclude
    commits = parse_log(read_log(args.repo, args.months))
    kept = {p for p in tracked_files(args.repo) if not matches_any(p, excludes)}
    sets = changesets(commits, kept, args.max_changeset_size)

    report = {
        "repo": str(Path(args.repo).resolve()),
        "window_months": args.months,
        "params": {
            "min_revs": args.min_revs, "min_shared": args.min_shared,
            "min_coupling": args.min_coupling,
            "max_changeset_size": args.max_changeset_size, "excludes": excludes,
        },
        "summary": {"changesets_analyzed": len(sets)},
        "pairs": coupled_pairs(sets, args.min_revs, args.min_shared, args.min_coupling),
        "sum_of_coupling": sum_of_coupling(sets)[:50],
    }
    write_report(report, args.out)


if __name__ == "__main__":
    main()
