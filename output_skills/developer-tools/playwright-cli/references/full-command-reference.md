# Full command reference

SKILL.md covers the working subset. The complete, version-matched reference ships inside the CLI itself — consult it rather than this file for anything not in SKILL.md, so it never goes stale.

## The shipped reference

`playwright-cli --help` lists every command, and prints the path to the CLI's own bundled `SKILL.md` near the top (`Agent skill: …/cli-client/skill/SKILL.md`). That file documents each command group in full and links to deeper references (tracing, mocking, codegen, storage state).

```bash
playwright-cli --help                  # all commands, grouped
playwright-cli --help <command>        # detail for one command
```

## Command groups beyond the core loop

Available but out of scope for SKILL.md — read the shipped reference when a task needs them:

- Tabs — `tab-list`, `tab-new`, `tab-select`, `tab-close`
- Storage — cookies, localStorage, sessionStorage get/set/list/clear
- Network — `route` / `unroute` to mock responses, `network-state-set` for offline
- Mouse and keyboard primitives — `mousemove`, `mousewheel`, `keydown`, `keyup`
- DevTools — `tracing-start/stop`, `video-start/stop`, `run-code`, `generate-locator`, `highlight`
- Spec-driven testing and codegen — plan / generate / heal Playwright tests

## Global flags worth knowing

- `--raw` — output only the result value (pipeable; see SKILL.md)
- `--json` — wrap every reply as JSON for structured parsing
