# Work log: deep-research-skill

Brief: `~/star-stone/briefs/deep-research-skill.md`. Coordinator: star-stone-26-10-07.

## State

- Skill written at `output_skills/ai/deep-research/SKILL.md`, installed globally (`./skills install deep-research`), validator and `scripts/` tests pass.
- Built from the tool's README, AGENTS.md, worklog, routes research and the two archived reports, then revised against the tool's docs pass (bc032fd).

## Decisions

- Name stays `deep-research`, as briefed. The plugin skill `anthropic-skills:deep-research` overlaps, but in trigger tests ours fired on both deep-research requests.
- Category `ai`: the skill drives an AI service, like its neighbours there.
- Call the tool as `node ~/ws/sprouts/chatgpt-deep-research/src/cli.ts`. Node 24 is the global default and no project pins an older one, so no version guard.
- Index order (Star-stone, 21:10): keep the CLI's append order. "First in the file" in the brief meant a plain scannable list.
- A run needs a go (Star-stone, 21:10): the agent shows the prompt to Archie or the asking session and runs only on a go.
- Prompt craft lives in the tool's `docs/prompt-guide.md`; the skill keeps a one-sentence anchor (*open question*, no *answer injection*) and points there, so the guide stays the single source of truth as the tool session learns from real runs.
- One-run-at-a-time check: `pgrep -fl 'chatgpt-deep-research/src/cli.ts'`. Checked it finds a running process and doesn't match itself.

## Trigger tests (`claude -p` in the scratchpad)

- "Do a deep research on blameless postmortems for agent failures" → skill fired, open-question prompt drafted, waited for go.
- "Look into how others split roadmaps vs backlogs with agents" → skill fired, same shape.
- "Latest stable Node.js?" → no skill.
- Incident: the first save test ran with only Bash disabled. The test session ran `save` through Monitor on the real ontology chat, made a duplicate `2026-10-08-untitled-pending.md`, then removed it and restored the index. Archive checked afterwards: two original files, index text unchanged. No research run, no quota used. Later tests ran in plan mode with every write and shell tool disabled.
- After pointing at the prompt guide, the postmortem request gave a three-sentence prompt and asked Archie why he needs it instead of inventing a reason (earlier drafts ran to several paragraphs and guessed the reason).
- From the save test: `save` now says to search the archive for the chat URL first, and to leave out `--slug`/`--summary` when the topic is unknown.

## Open

- No real `run` has gone through the skill yet. chatgpt-deep-research does the first full run with Archie and will report anything that changes the skill.
