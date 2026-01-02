# ApprovalTests Python Skill Improvements

## Structure Issues

- [x] **Consolidate duplicated patterns** - Created `references/python/patterns.md` and `references/python/combinations.md`. Trimmed `advanced.md` to just configuration. Updated `python.md` links.

- [ ] **Remove Java/Node.js cross-references from Python flow** - The `links.md` file has all three languages. When focused on Python, Claude doesn't need to see Java/Node.js source locations. Consider splitting into language-specific link files or embedding links directly in language files.

## Content Gaps

- [ ] **Document MarkdownTable utility** - Useful for testing multiple inputs against multiple functions. Pattern: `MarkdownTable.with_headers("Input", "Fn1", "Fn2").add_rows_for_inputs(inputs, fn1, fn2)`. Not mentioned anywhere.

- [ ] **Expand Storyboard documentation** - Current api.md mentions it briefly but misses:
  - `add_description()` method for labeling sections
  - Framing as "comic book panels stacked vertically for diff tools"
  - When to use (state machines, workflows, animations)

- [ ] **Add custom reporter creation pattern** - References mention reporters but not how to create custom ones. Pattern: extend `Reporter`, implement `report(self, received_path, approved_path) -> bool`, return bool for chain-of-responsibility fallback.

- [ ] **Document CLI usage** - `python -m approvaltests -t TEST_ID -r "received output"` for cross-stack integration. Not mentioned.

- [ ] **Add PyCharm whitespace gotcha** - Known issue: PyCharm strips trailing whitespace from approval files. Fix: File → Settings → Editor → General → On Save → uncheck "Remove trailing spaces". This trips up many users.

- [ ] **Document minimal installation option** - `pip install approvaltests-minimal` exists for projects that don't need extras. Current docs only show `pip install approvaltests`.

- [ ] **Clarify allpairspy dependency** - `verify_best_covering_pairs()` requires `allpairspy` package but this isn't mentioned where the function is documented.

## Description/Triggering

- [ ] **Enrich trigger phrases in description** - Current description is good but could add:
  - "golden master testing"
  - "snapshot testing" (common term from JS ecosystem)
  - "characterization testing"
  - "working with .approved/.received files" (already there, good)

  Users coming from Jest/Vitest may say "snapshot" not "approval".

## Conciseness

- [ ] **Trim obvious explanations** - `scrubbers.md` explains what GUIDs and dates are. Claude knows this. Keep just the pattern: `scrub_all_guids` replaces with `<guid_0>`, `<guid_1>`, etc.

- [ ] **Reduce redundancy in api.md** - Function signatures are shown with both signature and example that does the same thing. Consider keeping just one or making examples show non-obvious usage.

- [ ] **Trim installation section** - `pip install approvaltests` doesn't need explanation. Move to one-liner at top of python.md.

## Missing Anti-patterns

- [ ] **Add: Don't use verify_all when verify_as_json works** - Seen pattern where people use `verify_all("items", items)` when `verify_as_json({"items": items})` is cleaner and shows structure.

- [ ] **Add: Don't create approval files manually** - People sometimes create `.approved.txt` by hand instead of running test → reviewing .received → approving. This leads to format drift.

- [ ] **Add: Don't mix approval and assertion styles** - Seen tests that do `verify(result)` then also `assert result.count == 5`. The approval should capture everything.

## Enhancement Ideas

- [ ] **Add "Common Scrubber Recipes" section** - Practical combinations people actually need:
  - API responses (timestamps + IDs + tokens)
  - Log files (timestamps + log levels to filter)
  - Database dumps (IDs + created_at + updated_at)

- [ ] **Emphasize labeled combinations** - `verify_all_combinations_with_labeled_input()` produces much clearer output than `verify_all_combinations()`. Current docs show both equally; should recommend labeled version first.

- [ ] **Add troubleshooting: "Test passes locally, fails in CI"** - Usually means:
  - Different line endings (Windows vs Unix)
  - Timezone differences in date output
  - Missing scrubber for environment-specific data

  Common pain point worth documenting.

- [ ] **Add: How to diff .approved files in git** - `git diff --no-index file.approved.txt file.received.txt` or setting up git attributes for better diffing.

## Low Priority

- [ ] **Consider splitting api.md** - Currently has imports, core functions, combinations, Options, Storyboard, command line testing, logging verification. Could split into focused files if it grows further.

- [ ] **Add visual example of approval workflow** - ASCII diagram showing: test runs → .received created → user reviews → approves → .approved exists → future runs compare. Some users find visual helpful.
