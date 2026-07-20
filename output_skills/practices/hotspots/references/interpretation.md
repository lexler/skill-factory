# Interpreting Hotspot Results

## Contents
- Quadrants
- False-positive catalog
- Metric caveats
- Threshold tuning

## Quadrants

Files are split on median change frequency and median LOC among ranked files:

- hotspot — high frequency, high complexity. The refactoring targets; effort here pays.
- stable-complex — complex but quiet. Do NOT refactor as a priority: no change means no interest paid on the debt. Candidates for the do-not-refactor list.
- active-simple — changed often but small. Usually healthy; worth a glance only if the same tiny file changes with every feature (possible shotgun-surgery symptom, check its coupling).
- quiet — low on both. Ignore.

The `stable_complex` array in mine.json lists large files that fell below the min-revs floor entirely (including zero commits) — the ranking never sees them, but they belong on the do-not-refactor list.

## False-positive catalog

A high score earns a file a *reading*, not a verdict. Discard candidates that match these classes, and name the class in the report:

- Config / registry / aggregator files — routing tables, DI containers, changelogs, translation files, barrel/index files, docs indexes. They change with everything while carrying no design debt. High coupling plus low indentation depth is the tell.
- Generated or auto-fetched content — build output, vendored copies, files a script rewrites wholesale. Churn is mechanical. Add an exclude and re-run MINE rather than discarding by hand each time.
- Brand-new feature code — a file under active initial development is hot because it is being built, not because it resists change. Check its first commit date; under ~3 months old, note it as "watch, don't refactor yet."
- Mass reformatting — a prettier/gofmt sweep inflates churn and coupling in one commit. The changeset-size cap absorbs most of this; if one slipped through, the tell is a single commit contributing most of the churn.
- Bot commits — dependabot/renovate authorship dominating a file's history means the frequency is not human effort.

Not false positives:
- Test files. A test file as top hotspot means expensive-to-maintain tests — a genuine refactoring target.
- Files you feel are "fine." The numbers say developers keep returning; read closely before overruling them.

## Metric caveats

- LOC as complexity biases toward big files; it is a proxy, chosen because more elaborate metrics correlate strongly with it anyway.
- Indentation stats (4 spaces or 1 tab = one logical level) are meaningful as trends and within-file comparisons, never as absolute cross-language numbers. Rising indentation with flat LOC means the file is getting denser — a warning sign.
- Coupling can only see commit granularity. Squash-merge-heavy repos blur it; say so in the report and lean on file-level evidence instead.
- Renamed files restart their history (mining runs `--no-renames` and keeps only currently-tracked paths). A recently renamed hotspot may look cooler than it is.
- Frequency counts changes, not reasons. Distinguishing debt-churn from feature-churn requires reading commit messages during VALIDATE.

## Threshold tuning

Defaults live in the scripts (`--help` shows them); tune when results look wrong:

- Top ranks dominated by config/generated files → tighten excludes, not thresholds.
- Nothing ranked → widen `--months` or lower `--min-revs` (small or young repos).
- Coupling shows nothing, yet you expect pairs (tests, clones) → lower `--min-coupling` toward 20 or `--min-shared` toward 3.
- Coupling drowning in pairs → raise `--min-coupling` toward 50; degrees ≥ 50% are worth investigating, ≥ 90% signals a clone or lockstep dependency.
