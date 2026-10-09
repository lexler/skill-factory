---
name: deep-research
description: "ChatGPT Deep Research: whether a question earns a run, writing its prompt, running it, and filing the cited report in the research archive. Use when deep research is asked for, when saving a ChatGPT Deep Research chat, or when a question needs a broad, sourced survey of current work."
---

STARTER_CHARACTER = 🔭

# ChatGPT Deep Research

Archie's ChatGPT Pro subscription runs Deep Research: 5 to 30 minutes of browsing that ends in a long report with numbered sources. The deep-research tool in `~/ws/sprouts/chatgpt-deep-research` starts a run in its own signed-in Chrome, waits for it, and files the report in Archie's research archive. Runs come from a monthly quota of about 250.

## Whether a question earns a run

A run earns its place when the answer is a survey: the current state of a field, options compared across many sources, what other fields already know about Archie's problem.

Reach for something else when:
- one fact or a few pages answer it: WebSearch and WebFetch;
- the answer lives in code, a repo or Archie's notes: read them, since ChatGPT sees only the prompt;
- the question needs client material, names or secrets to make sense: the prompt goes to OpenAI, so ask Archie first;
- you want to see whether the tool works: runs are never spent on trials; the tool's own tests cover that.

Done when you can say in one sentence what the report will help Archie decide or understand.

## Writing the prompt

The prompt is an open question: short, problem first, in Archie's voice, free of answer injection, ending with "What am I not thinking about?" Read `~/ws/sprouts/chatgpt-deep-research/docs/prompt-guide.md` before writing one; it holds the rules and a before-and-after example. Where you lack a fact about Archie's situation, such as why he needs this now, ask him.

Write the prompt to a file outside the repo, such as your scratchpad. Show it to Archie, or to the session that asked for the research, and run only on their go.

Done when Archie or the asking session has said go on this exact text.

## Running it

One run at a time: check that none is going (`pgrep -fl 'chatgpt-deep-research/src/cli.ts'` prints nothing), then start it in the background, since it waits up to 90 minutes:

```sh
node ~/ws/sprouts/chatgpt-deep-research/src/cli.ts run <prompt-file> --slug <slug> --summary "<one sentence>"
```

It prints the chat URL first, a progress line every minute, and `Saved <report-file>` at the end.

- `--slug`: a few lowercase words naming the topic, joined by dashes. The file becomes `<date>-<slug>.md`.
- `--summary`: one sentence for the index, saying what the report covers and what it is for. Without it the index gets ChatGPT's plan title, which reads poorly.

The other two commands take a chat URL:
- `save <chat-url> --slug <slug> --summary "…"` files a finished Deep Research chat, such as one Archie started by hand, or a run that outlasted the 90 minutes. First search the archive for the chat URL (`grep -l '<chat-url>' ~/second-brain/research/*.md`): a chat found there is already filed. When you don't know the topic yet, leave out `--slug` and `--summary`; the slug then comes from ChatGPT's plan title, and you write the summary after reading the report. Saving again with the same slug replaces the report and its index line.
- `status <chat-url>` prints `completed`, or `researching (<status>)`.

The tool handles Chrome and ChatGPT itself. When it says the sign-in is gone, pass its instructions to Archie; signing in is his step. When it says the research ended with a status like `failed` or `stopped`, report that with the chat URL rather than starting another run.

## Filing the report

The tool writes `~/second-brain/research/<date>-<slug>.md`, with the prompt, chat URL and times in front matter and the numbered sources at the end, and adds one line to `~/second-brain/research/index.md`: `- [Title](file) - summary`.

After `Saved`:
- Read the index line. Fix the summary in `index.md` by hand if it doesn't tell Archie at a glance what the report is.
- Read the report and give the asker its answer at a glance, with the report path.
- When the research serves a project, link the report from that project's docs.

Done when the report is in the archive, its index line reads as one clear sentence, and the asker has the answer and the path.
