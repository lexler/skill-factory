# Driving a logged-in browser

To act inside a session that's already authenticated (an SSO'd internal app, a site behind a login you don't want to automate), attach to a running Chrome over the DevTools protocol instead of launching a fresh one.

## Attach to a running Chrome

Start Chrome with remote debugging exposed, then attach:

```bash
playwright-cli attach --cdp=http://localhost:9222
```

The CLI also accepts a channel name when the browser isn't already listening:

```bash
playwright-cli attach --cdp=chrome
playwright-cli attach --cdp=msedge
```

Once attached, every command drives that real browser and its existing cookies and tabs. `detach` releases it and leaves the browser running; `close` would terminate it.

## Persisting auth without attaching

When you control the launch, a persistent profile carries cookies between runs:

```bash
playwright-cli open --persistent
playwright-cli open --profile=/path/to/profile   # explicit directory
```

Or capture and replay storage state (cookies + localStorage):

```bash
playwright-cli state-save auth.json   # after logging in once
playwright-cli state-load auth.json   # in a later run
```

## Notes

- `attach` repoints the session slot to the attached browser. If a `default` session was already in use, attaching reuses that slot — name the session (`-s=work`) to keep them separate.
- The underlying Chrome keeps running after `detach`; re-attach with the same `--cdp` endpoint to resume.
