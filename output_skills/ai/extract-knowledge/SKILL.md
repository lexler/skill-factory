---
name: extract-knowledge
description: "Extracts what the session learned into prose that stands alone, or reviews existing text through the same distortion lenses."
disable-model-invocation: true
argument-hint: [topic | file | pasted text]
---

STARTER_CHARACTER = 📝

# Extract Knowledge

Turn what a session knows into prose that stands alone. The reader is a stranger: they were not in the session and they see only the text. Each lens below defends the stranger against one distortion.

## Seats

Decide which seat you are in — it changes what you can verify.

- Author seat: you did the work, so the knowledge is in your context. You can verify faithfulness directly, but you are half-blind to standalone failures because you cannot un-know the session. Compensate deliberately: reread the draft as the stranger, asking of every referent "do I know this if I only have the text?"
- Reviewer seat: the argument points at text someone else wrote. You are the stranger, so standalone and prose failures are visible to you directly. For faithfulness, check claims against the source session or transcript if one is reachable; mark the claims you cannot verify instead of guessing.

## Steps

1. Read the argument. A topic means extract that topic. No argument means extract everything important. Existing text or a file path means take the reviewer seat and go straight to the lens gate.

2. Draft the extraction. Capture what the session learned: decisions with their why, corrections and preferences the user stated, insights discovered, dead ends that cost time, and questions still open. Done when every insight in scope is either in the draft or consciously judged not worth the reader's time.

3. Run the lens gate below and keep a visible verdict list: a bulleted list, one lens per line — its name, then "clean" or the defect found and fixed. A verdict names a defect caught in the draft; a lens that shaped the draft from the start still reports "clean". A lens without a verdict line was skipped, not passed. Done when the verdict list covers every lens in all three groups.

4. Output the text in chat, or return it if another agent invoked you. Persistence belongs to the caller: hand over prose, and let the caller decide if and where it becomes a file. The extracted text is the only artifact — the verdict list and any questions to the user are chat output, and stay out of the text however it is saved or passed on.

## Lens gate

Look through one lens at a time.

### Standalone — the stranger was not there

- Fourth-wall break — the text addresses the asker or narrates the process ("as requested", "I've now added"). → Rewrite from the reader's point of view, or delete the sentence.
- Context leakage — a session-private referent appears as if the reader knows it: a scratch folder, an experiment label, "the audit". → Name it in terms the reader has, or drop the referent.
- Change-relative framing — the text describes the delta ("now uses X", "the new approach") instead of the resulting state, so it is stale on arrival. → Write the timeless state.
- Orphaned claim — a fact was lifted without the context that made it true: a dangling "it", an unstated precondition, a rule that only held in one setup. → Restore the condition or cut the claim.
- Salience mismatch — content is ranked by how much session attention it got, not by what the reader needs; trivia sits level with the one thing that matters. → Reorder by reader importance and cut what does not serve the reader.

### Faithfulness — the record must match what happened

- Fabrication — a claim that never happened in the session; where the source was silent, priors filled the gap. → Trace every claim to the session; delete what you cannot trace.
- Commitment upgrade — "we discussed X" became "we decided X"; a maybe became an action item. → Restore the real speech act.
- Confidence inflation — hedges, scope limits, and caveats were stripped, so one instance reads as a general rule. → Put the hedge and the scope back.
- Success theater — failures, dead ends, objections, and open risks vanished; "done" claims exceed what was verified. → Record what failed and what is still open.
- Detail corruption — a true claim carries a wrong actor, number, date, or sequence. → Check each specific against the source.
- False causality — independent facts joined by an invented "because"; real causal structure flattened into a story. → Link only what was actually linked.
- Sycophantic record — the text captures what the user asserted, not what was established; the framing beat the evidence. → Record the conclusion the evidence supports.

### Prose — plain writing

- Padding — the text can be compressed without losing information; detail exceeds the reader's curiosity. → Compress until every word earns its weight.
- Diff narration — the text restates what its subject already shows: a commit narrating the diff, a comment narrating the code. → Keep only what the subject cannot say itself, usually the why.
- Significance inflation — small things wear grandiose framing: "comprehensive", "robust", "production-ready". → State plainly what it is.
- Slop style — slogan fragments ("No X, no Y."), snappy triads, "It's not X, it's Y", walls of bullets, bold everywhere. → Write simple English sentences.
- Tooling residue — prompt text, raw diffs, or harness machinery leaked verbatim into the text. → Delete it.
