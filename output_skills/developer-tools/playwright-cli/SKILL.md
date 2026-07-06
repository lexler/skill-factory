---
name: playwright-cli
description: "Drive a browser from the terminal with playwright-cli: snapshot the page, then act on elements by ref. Use when automating browser interactions, filling web forms, testing UIs, or driving logged-in web apps from the command line."
---

STARTER_CHARACTER = 🎭

# playwright-cli

Driving a browser from the shell. Each command prints the executed Playwright code, the page state, and a fresh snapshot.

## The loop

Snapshot to see the page, act on an element by its ref, snapshot again.

```bash
playwright-cli snapshot          # accessibility tree with [ref=e8] handles
playwright-cli click e8          # act on a ref
playwright-cli snapshot          # confirm the result
```

Refs are not stable. Any DOM change renumbers them — re-snapshot before acting on a page that just changed. Acting on a stale ref hits the wrong element or none.

For a large page, snapshot a region instead of the whole tree: `snapshot e34` or `snapshot --depth=4`.

## Targeting elements

A target is one of three things — a ref, a CSS selector, or a Playwright locator:

```bash
playwright-cli click e8
playwright-cli click ".todo-list .toggle"
playwright-cli click "getByRole('button', { name: 'Submit' })"
playwright-cli click "getByText('buy milk')"
```

A bare descriptive phrase is not a target. `click "the submit button"` is parsed as a CSS selector and fails with "does not match any elements". Prefer refs; reach for `getByRole`/`getByText` when a ref won't survive a re-render.

## Key commands

```bash
playwright-cli goto https://example.com
playwright-cli fill e5 "user@example.com" --submit   # clear, type, then Enter — one step
playwright-cli type "free text into the focused element"
playwright-cli press Enter                            # also: Tab, Escape, ArrowDown
playwright-cli select e9 "option-value"
playwright-cli check e12        # uncheck / hover / dblclick likewise
playwright-cli screenshot       # saves to .playwright-cli/
```

`fill` works on React/controlled inputs where raw DOM events don't. After filling, the field must blur before dependent values (totals, validation) update — `--submit` or a following `press Tab` does that.

## Inspecting and verifying

```bash
playwright-cli eval "el => el.getAttribute('data-testid')" e5   # attributes the snapshot hides
playwright-cli console                                          # page console messages
playwright-cli requests                                         # network log, then `request <n>`
```

`--raw` strips the wrapper so output pipes, and proves what an action changed:

```bash
playwright-cli --raw snapshot > before.yml
playwright-cli click e8
playwright-cli --raw snapshot > after.yml
diff before.yml after.yml
```

## Sessions

`open` launches a fresh browser; `--persistent` keeps cookies across runs. To drive an already-running, logged-in browser instead, attach over CDP. See [references/attaching-to-chrome.md](references/attaching-to-chrome.md).

Name parallel browsers with `-s=<name>` (omit it for the implicit `default` session). `playwright-cli list`, `close`, `close-all`.

## Full command set

The above is the working subset. The CLI ships its own exhaustive reference — tabs, storage, mocking, tracing, video, codegen. See [references/full-command-reference.md](references/full-command-reference.md).
