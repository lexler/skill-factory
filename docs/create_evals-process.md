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

Think about assertions in these categories:

- Correctness: Does the output contain the right information? ("The summary includes all three key findings from the source document")
- Completeness: Is anything missing? ("Every section from the template appears in the output")
- Format: Does the output match the expected shape? ("The output is a valid JSON file with a 'results' array")
- Behavior: Did Claude follow the skill's workflow? ("The skill's validation script was executed before producing final output")

Write assertions that are hard to satisfy without actually doing the work correctly. An assertion like "output file exists" is too weak — a wrong file still passes. Better: "output file contains column headers matching the input schema."

**Prefer mechanical validators over LLM judgment.** If the skill produces output in a format with an existing parser, linter, or compiler, write an assertion that runs that tool and checks the exit code. A mechanical "the parser accepts this" check is far stronger than a graded "this looks valid" — the LLM grader can be charitable, but a parser cannot. Look for validators that exist for the output format the skill produces, and call them in assertions when available.

The grader agent will also critique weak assertions and suggest improvements, so the first draft doesn't need to be perfect.

### 3. Run Quality Evals

AI is non-deterministic — a single run can be an outlier. Multiple runs let you compare distributions, not data points. Use AskUserQuestion to ask the user how many runs per configuration, with these options:
- Quick (1 run each, 2 agents per prompt) — fast, lowest token cost, good for early iterations
- Standard (3 runs each, 6 agents per prompt) — reliable signal, moderate token cost
- Thorough (5 runs each, 10 agents per prompt) — high confidence, highest token cost
- Custom — user picks the number

Spawn all runs in parallel.

Each eval has two configurations: **with_skill** (the skill is loaded) and **without_skill** (no skill, just plain Claude on the same prompt). Each configuration runs N times (per the user's run-count choice).

**With-skill runs**: Tell the agent to read the skill first, then execute the task. Include:
- The skill path
- The task prompt
- The output directory: `{skill-name}-workspace/iteration-1/eval-{ID}/with_skill/run-{N}/outputs/`
- A request to save a transcript (every step, test, prediction, refactoring) to `transcript.md` in the run directory — the grader needs this

**Baseline runs**: Same task prompt but explicitly tell the agent NOT to read any skill files. Save to `{skill-name}-workspace/iteration-1/eval-{ID}/without_skill/run-{N}/outputs/`. Also request a transcript.

Running both shows whether the skill actually adds value vs what Claude can do on its own. Multiple runs show whether that value is consistent or just lucky.

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
echo '{ ... }' > {skill-name}-workspace/iteration-1/eval-{ID}/eval_metadata.json
mkdir -p {skill-name}-workspace/iteration-1/eval-{ID}/with_skill
mkdir -p {skill-name}-workspace/iteration-1/eval-{ID}/without_skill
ln -sf ../eval_metadata.json {skill-name}-workspace/iteration-1/eval-{ID}/with_skill/eval_metadata.json
ln -sf ../eval_metadata.json {skill-name}-workspace/iteration-1/eval-{ID}/without_skill/eval_metadata.json
```

When each subagent completes, capture timing data from the task notification (`total_tokens`, `duration_ms`) and save to `timing.json` in the run directory. This data is only available at notification time.

### 4. Grade

Grading happens in two passes per run. The two-pass structure separates "find problems" from "judge assertions" so the grader can't quietly downgrade defects when scoring.

**Pass 1 — Defect finding.** Before grading any assertions, spawn a defect-finding agent for each run. Its sole job is to find every problem in the output: syntax errors, wrong values, missing elements, non-standard usage, inconsistencies, anything that looks off. The agent has no incentive to be charitable — it's not judging anything, just cataloguing. Save the result to `defects.md` in the run directory. The prompt should be something like:

> Read the output files at <path> and the transcript at <transcript-path>. Find every defect, error, inconsistency, or non-standard usage. Be paranoid — list anything that looks wrong or suspicious, even minor. Group findings by severity (clear errors vs questionable choices). Do not judge whether the output is "good enough" — just enumerate problems.

**Pass 2 — Assertion grading.** For each run, use the grader agent protocol from `docs/knowledge/anthropic-skill-creator/agents/grader.md`, but pass the `defects.md` from Pass 1 as additional input. Tell the grader: for each assertion, check whether any defect from `defects.md` contradicts it; if yes, the assertion fails. Save results to `grading.json`.

This makes charity expensive: the grader would have to ignore evidence already on the table. Pass 1 surfaces problems without judgment; Pass 2 cannot avoid them.

For assertions that can be checked programmatically (file exists, contains expected string, valid JSON), write and run a script instead of having the grader eyeball it. Mechanical checks bypass both passes.

### 5. Launch the viewer

This step is not optional — the user needs to see the results before any conclusions are drawn.

Launch the viewer using `nohup` and the Bash tool's `run_in_background: true` parameter so it survives the shell exiting:

```bash
nohup python docs/knowledge/anthropic-skill-creator/eval-viewer/generate_review.py \
  {skill-name}-workspace/iteration-1 \
  --skill-name "{name}" \
  --benchmark {skill-name}-workspace/iteration-1/benchmark.json \
  > /tmp/viewer-{skill-name}.log 2>&1
```

This opens a browser at localhost with two tabs:
- Outputs: browse each test case with its prompt, see the output, leave feedback
- Benchmark: quantitative comparison between with-skill and baseline

Tell the user the viewer is open and wait for them to review and come back.

**Do not relaunch the viewer on the same port** — `generate_review.py` kills any existing process on the requested port at startup, so a second launch terminates the first. If the user asks to "reopen" the viewer, check if it's still running first (`curl -s http://localhost:3117 > /dev/null && echo running`); if it is, just remind them of the URL.

For iteration 2+, pass `--previous-workspace` pointing at the previous iteration.

### 6. Improve and Re-run

Read `feedback.json` from the viewer. Empty feedback means the output was fine. Focus on test cases where the user had complaints.

When improving the skill based on feedback:
- Generalize from the examples — the skill will be used on many prompts, not just these
- Read the transcripts, not just outputs — if Claude wasted time on unproductive steps, trim the instructions causing it
- Explain *why* behind instructions rather than rigid MUSTs

Re-run all test cases into `iteration-2/`, including baselines. Relaunch the viewer (step 5).

Loop until the user is satisfied or feedback is all empty.

**Blind A/B comparison (optional)**: If you've iterated a few times and it's unclear whether the latest version is actually better, offer a blind comparison. This gives two outputs to an independent judge without revealing which version produced them. The judge scores on a rubric (correctness, completeness, organization, usability) and picks a winner. Then an analyzer explains *why* the winner won and suggests targeted improvements.

This is worth the extra time when improvement is ambiguous. Skip it when regular evals already show clear direction.

Protocol: `docs/knowledge/anthropic-skill-creator/agents/comparator.md` and `docs/knowledge/anthropic-skill-creator/agents/analyzer.md`.

### 7. Optimize Description (optional)

After the skill's quality is solid, offer to optimize the description for better triggering accuracy. The description is what Claude uses to decide whether to activate the skill.

**Generate trigger eval queries**: Create 20 queries — a mix of should-trigger (8-10) and should-not-trigger (8-10).

Should-trigger queries: different phrasings of the same intent, casual and formal, some where the user doesn't name the skill but clearly needs it.

Should-not-trigger queries: near-misses that share keywords but need something different. These are the valuable ones. `"Write a fibonacci function"` as a negative test for a PDF skill is too easy. Better: a query that touches on a related domain but actually needs a different tool.

All queries should be realistic — include file paths, personal context, abbreviations, typos, mixed case. Not abstract one-liners.

**Review with user**: Present the queries for review. The user can edit, add, remove, toggle should/shouldn't trigger.

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
