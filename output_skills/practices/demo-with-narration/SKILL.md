---
name: demo-with-narration
description: "Demos working software: first proves every claimed behavior by exercising the real artifact, then replays the proof as a slow, voice-narrated walkthrough. Use when the user asks for a demo or to be shown that something works."
---

# Demo With Narration

STARTER_CHARACTER = 🎬

A demo is a proof performed twice: once fast and private to convince yourself, once slow and narrated to convince the person watching.

## Stage 1: Self-demo

Exercise the real artifact the way its consumer will — the built binary, the running app. A green test suite is the starting point, not the proof.

- Check every behavior you intend to claim: the happy path, each refusal path with its exact stderr reason and exit code, every way the session can end.
- Probe at least one path beyond the obvious ones (quit from the menu, not just close the window) — the extra path is where green-suite bugs hide.
- A detached GUI launch loses its exit status: wrap the launch in a subshell that writes `$?` to a file, read the file after the window closes.
- Confirm a window really rendered with a screenshot; drive close and quit through accessibility clicks.

Done when every behavior you will claim in the walkthrough has been observed working, and any bug found is fixed and re-proven.

## Stage 2: Narrated walkthrough

Replay the proof slowly. The person asked to follow along, so pace for their eyes and ears.

- Announce each step by voice (`speak`) before acting: what is about to happen, what to watch for. Pause a beat so the voice finishes before the action starts.
- One step per command, numbered. Each step proves exactly one claim.
- When something appears on screen, say how long it will stay and leave it there — ten seconds for a window is enough to actually look at it.
- After each step, one or two sentences of text recapping what was just proven.
- Order the steps as an argument: the input artifact first, then the refusal paths with their exit codes, then the happy path, then every way the session can end.
- Include at least one step that can only pass if the whole pipeline works — a validation error from the deepest layer surfacing at the outermost one — rather than only surface behaviors.

Done when every step was announced before it ran, each claim from the self-demo appeared in exactly one step, and a final recap lists every step.

## Desktop-automation safety

A System Events keystroke lands on the frontmost application, whatever process the tell block names.

- Click the specific button or menu item through accessibility instead of synthesizing keystrokes.
- When a keystroke is unavoidable: bring the target frontmost, read back which app is actually frontmost, and type only if it matches the target.
- After any slip, list the open windows and confirm nothing else was harmed before continuing.
