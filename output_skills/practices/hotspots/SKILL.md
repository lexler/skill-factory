---
name: hotspots
description: Find where a codebase actually costs time by mining its git history (Tornhill hotspot analysis). Produces ranked refactoring targets with evidence, change-coupling seams, and a do-not-refactor list; re-run after refactoring to verify it paid off.
disable-model-invocation: true
---

STARTER_CHARACTER = 🔥

Hotspot analysis ranks files by change frequency × complexity. Code that is both complicated and changed often is where refactoring pays; complicated but stable code is not — "if it never changes, it's not costing us money." The scripts compute every number deterministically; your job is scoping, validation, and interpretation. A hotspot is a pointer to where to look, never a diagnosis.

If the user wants to check whether a past refactoring paid off and `hotspots/data/mine.json` exists in the repo, jump to VERIFY. Otherwise run the steps in order.

## 1. SCOPE

Decide and record:
- Window: default 12 months; use "since last major release" if the user names one. Under ~6 months of history, warn that rankings are unreliable.
- Target: repo root, or the subtree the user cares about in a monorepo.
- Extra excludes: skim the tree for generated/vendored content the defaults miss (see default list in `scripts/mine.py`). Keep test files in — a test file as top hotspot is a real and common finding.
- History quality: if most commits are PR squashes, note that coupling signal is weakened.

Done when window, target, and extra excludes are chosen and any history caveats are noted for the report header.

## 2. MINE

```bash
uv run ${CLAUDE_SKILL_DIR}/scripts/mine.py <repo> --months <N> [--exclude PATTERN]... --out hotspots/data/mine.json
uv run ${CLAUDE_SKILL_DIR}/scripts/coupling.py <repo> --months <N> [--exclude PATTERN]... --out hotspots/data/coupling.json
```

Pass the same `--months` and `--exclude` flags to both. If `summary.warnings` reports too few commits or nothing ranked, widen the window or lower `--min-revs` and re-run.

Done when both JSON files exist and `files_ranked` > 0.

## 3. VALIDATE

Take the top ~10 files by score from `mine.json`. Read each one and give a verdict — confirmed hotspot, or discarded with the false-positive class it belongs to (catalog in [references/interpretation.md](references/interpretation.md)). When discards free up slots, pull in the next candidates so ~10 get verdicts.

Done when every candidate has a verdict and one-line reason.

## 4. DEEPEN

For each confirmed hotspot:
- X-ray: find the hot functions inside the file. Read it, then check which regions keep changing: `git log --since=<window> -p -- <file>` (or `git log -L :<function>:<file>` for a suspect function).
- Seams: pull the file's partners from `coupling.json`. A test↔code pair is normal; coupling across module boundaries is an architecture finding worth naming.

Done when every confirmed hotspot has internal target functions and its coupling partners (or "none above thresholds").

## 5. REPORT

Write `hotspots/report.md`:
- Header: repo, window, excludes, params, history caveats.
- Refactoring targets, ranked: per file — the numbers (commits, churn, authors, LOC, indentation), the evidence in one or two sentences, hot functions, coupling seams.
- Do-not-refactor: `stable_complex` entries plus stable-complex quadrant files — complex but quiet; touching them is risk without payoff.
- Discarded candidates with reasons.
- Method footnote: score = change-frequency percentile × size percentile; thresholds used; pointer to `hotspots/data/` as the verify baseline.

Keep the two JSONs — they are the baseline VERIFY compares against. Done when the report answers "what to refactor first, why, and what to leave alone" without opening the JSONs. Offer the top target to the refactoring workflow the user normally uses.

## VERIFY (after a refactoring)

1. Read `params` from `hotspots/data/mine.json` and re-run both scripts with the same flags to fresh files (e.g. `hotspots/data/mine-after.json`).
2. For each refactored file, compare raw complexity against the baseline: LOC, indent_total, indent_mean, indent_sd. Falling numbers mean the refactoring paid off structurally; scores and ranks are percentile-relative, so never compare those across runs. A split file counts as improved when the successor files are each simpler than the original.
3. Append a dated "Verification" section to `hotspots/report.md` with a per-file verdict — improved / unchanged / worse — and the numbers behind it, then replace the baseline JSONs with the fresh ones.

Done when every refactored file has a verdict backed by before/after numbers.

## Reference

[references/interpretation.md](references/interpretation.md) — read during VALIDATE and when writing the report: quadrant meanings, the false-positive catalog, metric caveats, and threshold tuning.
