# Create Evals for a Skill

STARTER_CHARACTER = 🧪

## Description

Evaluate a Claude Code skill's quality by running it against test prompts and measuring results. Uses Anthropic's skill-creator infrastructure from `docs/knowledge/anthropic-skill-creator/`.

This process covers two types of evaluation:
- Quality evals: Does Claude follow the skill's instructions and produce good output?
- Trigger evals: Does the skill activate when it should and stay quiet when it shouldn't?

## Prerequisites

Run `./update-docs` to fetch the latest skill-creator infrastructure. The eval scripts, grader agents, and HTML viewer all live in `docs/knowledge/anthropic-skill-creator/`.

## Steps

### 1. Write Test Prompts

Write realistic test prompts — the kind of thing a real user would actually say when they need this skill. Not abstract descriptions, but concrete requests with context, file names, specifics.

Bad: `"Process this data"`
Good: `"I have a CSV in ~/reports/q4-sales.csv with columns for region, revenue, and headcount. Can you add a profit-margin percentage column?"`

**Coverage check before finalizing prompts:** read the skill's description and SKILL.md. Identify the dimensions along which the skill varies — output formats, input types, modes, distinct workflows, branches in the process. Every dimension needs at least one prompt for each meaningful value. Prompts that all exercise the same path leave most of the skill untested.

Save to `evals/evals.json` inside the skill directory:

```json
{
  "skill_name": "skill-name-here",
  "evals": [
    {
      "id": 1,
      "prompt": "The realistic user prompt",
      "expected_output": "Plain description of what success looks like",
      "files": []
    }
  ]
}
```

If the skill needs input files for testing, place them in `evals/files/` and reference them in the `files` array.

Schema reference: `docs/knowledge/anthropic-skill-creator/references/schemas.md`

### 2. Draft Assertions

For each test prompt, write assertions — verifiable statements about what the output should contain or how Claude should behave. Add them to the `expectations` array in `evals/evals.json`.

Assertions are written before any runs happen, deliberately (Anthropic's flow drafts them while runs are in progress). Assertions written after seeing outputs drift toward describing what was produced instead of what success requires.

Think about assertions in these categories:

- Correctness: Does the output contain the right information? ("The summary includes all three key findings from the source document")
- Completeness: Is anything missing? ("Every section from the template appears in the output")
- Format: Does the output match the expected shape? ("The output is a valid JSON file with a 'results' array")
- Behavior: Did Claude follow the skill's workflow? ("The skill's validation script was executed before producing final output")

Write assertions that are hard to satisfy without actually doing the work correctly. An assertion like "output file exists" is too weak — a wrong file still passes. Better: "output file contains column headers matching the input schema."

**Prefer mechanical validators over LLM judgment.** If the skill produces output in a format with an existing parser, linter, or compiler, write an assertion that runs that tool and checks the exit code. A mechanical "the parser accepts this" check is far stronger than a graded "this looks valid" — the LLM grader can be charitable, but a parser cannot. Look for validators that exist for the output format the skill produces, and call them in assertions when available.

When a probe *executes* the output (sandbox run), make it exercise at least one documented non-happy path, not just the demo scenario. A happy-path-only probe certifies broken outputs: a git helper that worked only when run from `main` scored perfect because the probe never ran it from another branch.

The grader agent will also critique weak assertions and suggest improvements, so the first draft doesn't need to be perfect.

### 3. Run Quality Evals

AI is non-deterministic — a single run can be an outlier. Multiple runs let you compare distributions, not data points. Use AskUserQuestion to ask the user how many runs per configuration, with these options:
- Quick (1 run each, 2 agents per prompt) — fast, lowest token cost, good for early iterations
- Standard (3 runs each, 6 agents per prompt) — reliable signal, moderate token cost
- Thorough (5 runs each, 10 agents per prompt) — high confidence, highest token cost
- Custom — user picks the number

Spawn all runs in parallel, but expect a concurrency ceiling: spawning ~18 agents at once has hit fork/pane limits. Spawn in batches of about 9, retry the failures, and for follow-up work (grading) reuse finished idle agents via messages instead of spawning fresh ones.

Each eval has two configurations: **with_skill** (the skill is loaded) and **without_skill** (no skill, just plain Claude on the same prompt). Each configuration runs N times (per the user's run-count choice).

**First, mint the iteration directory — never reuse one.** Don't hand-pick `iteration-1` or write into a directory that already holds outputs. The viewer pins each `feedback.json` review to a run by id and directory, so re-running into an existing directory silently re-attaches stale feedback to regenerated outputs. Always create a fresh one:

```bash
ITER=$(scripts/next_iteration.py output_skills/{category}/{skill-name}-workspace)
# prints e.g. output_skills/testing/tdd-workspace/iteration-3
```

`next_iteration.py` scans for existing `iteration-N` and creates the next number, never overwriting. Use the printed path — written `$ITER` below — everywhere these steps reference an iteration directory. Old iterations stay intact, so their feedback stays welded to the outputs it described.

**Eval directory names**: Name each eval directory `eval-{ID}-{slug}` where the slug says what it tests (e.g., `eval-1-stack-kata`, `eval-3-legacy-refactor`) — written `eval-{ID}-{slug}` below. Bare `eval-1` tells a reviewer nothing when scanning the workspace. The ID stays first so tooling that parses it from the name keeps working.

**With-skill runs**: Tell the agent to read the skill first, then execute the task. Include:
- The skill path
- The task prompt
- The output directory: `$ITER/eval-{ID}-{slug}/with_skill/run-{N}/outputs/`
- Which outputs to save — name the deliverable the user cares about (e.g., "the final .dsl file", "the generated test suite"), so the agent saves the right thing instead of guessing
- A request to save a transcript (every step, test, prediction, refactoring) to `transcript.md` in the run directory — the grader needs this
- A request to save `metrics.json` (tool-call counts per tool, total steps, files created, errors encountered — schema in `docs/knowledge/anthropic-skill-creator/references/schemas.md`) and `user_notes.md` (anything the agent was uncertain about, worked around, or thinks needs human review) into the outputs directory. The grader reads both; without them, the benchmark's execution metrics stay empty.

**Baseline runs**: Same task prompt but explicitly tell the agent NOT to read any skill files. Save to `$ITER/eval-{ID}-{slug}/without_skill/run-{N}/outputs/`. Request the same transcript, `metrics.json`, and `user_notes.md`.

**Baseline for an existing skill**: When the evals target changes to a skill that already worked (iteration on an installed skill), the question is "did my change help", not "is a skill useful". Snapshot the pre-change version (`cp -r <skill-path> <workspace>/skill-snapshot/`) before editing, and run the baseline agents against the snapshot instead of skill-less. Save those runs to `old_skill/` in place of `without_skill/`. Caveat: `aggregate_benchmark.py` discovers configs alphabetically and computes delta as first-minus-second, so with `old_skill`/`with_skill` the delta is old-minus-new — read the sign accordingly (or swap the summary when reporting).

Running both shows whether the skill actually adds value vs the baseline. Multiple runs show whether that value is consistent or just lucky.

Before spawning runs, write an `eval_metadata.json` for each eval. The viewer reads this to display the prompt — without it, the viewer shows "(No prompt found)" and results are hard to review.

The schema:
```json
{
  "eval_id": 1,
  "eval_name": "descriptive-name",
  "prompt": "The exact task prompt given to the agent",
  "assertions": ["assertion 1", "assertion 2"]
}
```

Write the file once at the eval level, then create symlinks from each config directory so the viewer's parent-lookup finds it for both `with_skill/run-N/` and `without_skill/run-N/` runs:

```bash
echo '{ ... }' > $ITER/eval-{ID}-{slug}/eval_metadata.json
mkdir -p $ITER/eval-{ID}-{slug}/with_skill
mkdir -p $ITER/eval-{ID}-{slug}/without_skill
ln -sf ../eval_metadata.json $ITER/eval-{ID}-{slug}/with_skill/eval_metadata.json
ln -sf ../eval_metadata.json $ITER/eval-{ID}-{slug}/without_skill/eval_metadata.json
```

(With an `old_skill` baseline, symlink into `old_skill/` instead of `without_skill/`.)

When each subagent completes, capture timing data from the task notification and save to `timing.json` in the run directory. This data is only available at notification time. Include all three fields — `aggregate_benchmark.py` reads `total_duration_seconds`, so omitting it produces a benchmark with zero times:

```json
{"total_tokens": 84852, "duration_ms": 23332, "total_duration_seconds": 23.3}
```

Named teammate agents signal completion with idle notifications that carry NO token or duration data — only Task-tool notifications have it. When it's unavailable: approximate duration from file mtimes, set `total_tokens` to 0, and record the approximation in a `note` field. Beware the aggregator's fallback — with tokens at 0 it substitutes `output_chars` as "tokens", so state in the benchmark metadata that the tokens column is output size, not token usage.

After all runs complete, check `git status` for stray files outside the workspace — executors occasionally leak test debris (e.g. a stderr redirect) into the repo root despite sandbox instructions.

### 4. Grade

Grading happens in two passes per run. The two-pass structure separates "find problems" from "judge assertions" so the grader can't quietly downgrade defects when scoring.

**Pass 1 — Defect finding.** Before grading any assertions, spawn a defect-finding agent for each run. Its sole job is to find every problem in the output: syntax errors, wrong values, missing elements, non-standard usage, inconsistencies, anything that looks off. The agent has no incentive to be charitable — it's not judging anything, just cataloguing. Save the result to `defects.md` in the run directory. The prompt should be something like:

> Read the output files at <path> and the transcript at <transcript-path>. Find every defect, error, inconsistency, or non-standard usage. Be paranoid — list anything that looks wrong or suspicious, even minor. Group findings by severity (clear errors vs questionable choices). Do not judge whether the output is "good enough" — just enumerate problems.

**Pass 2 — Assertion grading.** For each run, use the grader agent protocol from `docs/knowledge/anthropic-skill-creator/agents/grader.md`, but pass the `defects.md` from Pass 1 as additional input. Tell the grader: for each assertion, check whether any defect from `defects.md` contradicts it; if yes, the assertion fails. Save results to `grading.json`. The `expectations` entries must use exactly the fields `text`, `passed`, `evidence` — the viewer and aggregator depend on these names and silently show empty results on variants like `name`/`met`/`details`.

This makes charity expensive: the grader would have to ignore evidence already on the table. Pass 1 surfaces problems without judgment; Pass 2 cannot avoid them.

For assertions that can be checked programmatically (file exists, contains expected string, valid JSON), write and run a script instead of having the grader eyeball it. Mechanical checks bypass both passes.

### 5. Aggregate and Analyze

Once every run has a `grading.json`, build the benchmark — never hand-write `benchmark.json` (the viewer depends on exact field names, and hand-built files drift):

```bash
cd docs/knowledge/anthropic-skill-creator
python -m scripts.aggregate_benchmark <absolute-path-to-$ITER> --skill-name {name}
```

This writes `$ITER/benchmark.json` and `benchmark.md` with pass rate, time, and tokens per configuration (mean ± stddev) plus the delta.

Then spawn an analyst agent — the "Analyzing Benchmark Results" section of `docs/knowledge/anthropic-skill-creator/agents/analyzer.md`. It reads `benchmark.json` and surfaces what the aggregates hide: assertions that pass in both configurations (non-discriminating — they measure nothing), assertions that always fail (broken or beyond capability), high-variance evals (flaky), and time/token cost versus pass-rate gain. Write its observations into the benchmark's `notes` array so they show up in the viewer's Benchmark tab.

The analyst pass is where weak evals get caught. A skill that costs +180s and +24k tokens for +1% pass rate looks fine in raw outputs — only the notes make that visible.

### 6. Launch the viewer

This step is not optional — the user needs to see the results before any conclusions are drawn.

Launch the viewer using `nohup` and the Bash tool's `run_in_background: true` parameter so it survives the shell exiting:

```bash
nohup python docs/knowledge/anthropic-skill-creator/eval-viewer/generate_review.py \
  $ITER \
  --skill-name "{name}" \
  --benchmark $ITER/benchmark.json \
  > /tmp/viewer-{skill-name}.log 2>&1
```

This opens a browser at localhost with two tabs:
- Outputs: browse each test case with its prompt, see the output, leave feedback
- Benchmark: quantitative comparison between with-skill and baseline

Tell the user the viewer is open and wait for them to review and come back.

**Do not relaunch the viewer on the same port** — `generate_review.py` kills any existing process on the requested port at startup, so a second launch terminates the first. If the user asks to "reopen" the viewer, check if it's still running first (`curl -s http://localhost:3117 > /dev/null && echo running`); if it is, just remind them of the URL.

When the eval loop is finished (user satisfied, no more iterations), kill the viewer so the server doesn't linger: `lsof -ti :3117 | xargs kill`.

For iteration 2+, pass `--previous-workspace` pointing at the previous iteration dir (the `iteration-(N-1)` sibling of `$ITER`) — this is the intended way to carry the prior round's outputs and feedback forward as context.

### 7. Improve and Re-run

Read `feedback.json` from the viewer. Empty feedback means the output was fine. Focus on test cases where the user had complaints.

When improving the skill based on feedback:
- Generalize from the examples — the skill will be used on many prompts, not just these
- Read the transcripts, not just outputs — if Claude wasted time on unproductive steps, trim the instructions causing it
- Explain *why* behind instructions rather than rigid MUSTs

Mint a fresh iteration directory for the re-run — `ITER=$(scripts/next_iteration.py output_skills/{category}/{skill-name}-workspace)` — never reuse or overwrite the previous one (its outputs and feedback must stay intact). Re-run all test cases into the new `$ITER`, including baselines, re-aggregate and analyze (step 5), and relaunch the viewer (step 6) with `--previous-workspace` pointing at the prior iteration.

Loop until the user is satisfied or feedback is all empty.

**Blind A/B comparison (optional)**: If you've iterated a few times and it's unclear whether the latest version is actually better, offer a blind comparison. This gives two outputs to an independent judge without revealing which version produced them. The judge scores on a rubric (correctness, completeness, organization, usability) and picks a winner. Then an analyzer explains *why* the winner won and suggests targeted improvements.

This is worth the extra time when improvement is ambiguous. Skip it when regular evals already show clear direction.

Protocol: `docs/knowledge/anthropic-skill-creator/agents/comparator.md` and `docs/knowledge/anthropic-skill-creator/agents/analyzer.md`.

### 8. Optimize Description (optional)

After the skill's quality is solid, offer to optimize the description for better triggering accuracy. The description is what Claude uses to decide whether to activate the skill.

**Generate trigger eval queries**: Create 20 queries — a mix of should-trigger (8-10) and should-not-trigger (8-10).

Should-trigger queries: different phrasings of the same intent, casual and formal, some where the user doesn't name the skill but clearly needs it.

Should-not-trigger queries: near-misses that share keywords but need something different. These are the valuable ones. `"Write a fibonacci function"` as a negative test for a PDF skill is too easy. Better: a query that touches on a related domain but actually needs a different tool.

All queries should be realistic — include file paths, personal context, abbreviations, typos, mixed case. Not abstract one-liners.

Save the eval set to the workspace as a JSON array — this exact shape is what `run_loop` reads:

```json
[
  {"query": "the user prompt", "should_trigger": true},
  {"query": "another prompt", "should_trigger": false}
]
```

**Review with user**: Present the queries through Anthropic's review page rather than dumping them in chat — bad eval queries lead to bad descriptions, and the page makes editing painless:

1. Read the template at `docs/knowledge/anthropic-skill-creator/assets/eval_review.html`
2. Replace `__EVAL_DATA_PLACEHOLDER__` with the JSON array (unquoted — it's a JS assignment), `__SKILL_NAME_PLACEHOLDER__` and `__SKILL_DESCRIPTION_PLACEHOLDER__` with the skill's name and current description
3. Write to `playground/eval_review_{skill-name}.html` and `open` it
4. The user edits queries, toggles should-trigger, adds/removes, then clicks "Export Eval Set" — the file lands in `~/Downloads/eval_set.json` (grab the most recent if there are duplicates like `eval_set (1).json`)

**Run optimization**: The optimization loop splits queries 60% train / 40% held-out test, evaluates the current description (3 runs per query), proposes improvements using extended thinking, and iterates up to 5 times:

```bash
python -m scripts.run_loop \
  --eval-set {path-to-trigger-eval.json} \
  --skill-path {path-to-skill} \
  --model {model-id} \
  --max-iterations 5 \
  --verbose
```
(Run from the `docs/knowledge/anthropic-skill-creator/` directory.)

For `--model`, use the model ID powering the current session (it's in your system prompt) — the triggering test should match what the user actually experiences. The loop takes many minutes: run it in the background and tail its output periodically to report which iteration it's on and the scores.

Best description is selected by test score (not train score) to avoid overfitting.

**Apply**: Update the skill's SKILL.md frontmatter with the best description. Show the user before/after with scores.

## Output

Eval files are saved inside the skill directory:
```
skill-name/
  SKILL.md
  evals/
    evals.json
    files/        (input files for testing, if needed)
  ...
```

Workspace directories are created as siblings to the skill directory, named `{skill-name}-workspace/` (e.g., `output_skills/testing/tdd-workspace/`). They are gitignored (`*-workspace/`) and not picked up by the skills install script (no SKILL.md inside).
