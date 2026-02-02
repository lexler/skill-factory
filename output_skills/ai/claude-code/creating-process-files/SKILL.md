---
name: creating-process-files
description: Creates process files - text as code instructions for reliable AI workflows. Use when creating new process files.
---

# Creating Process Files

STARTER_CHARACTER = ⚙️

## Description

This skill helps make new process files or fine tune existing ones.
A process file describes a structured sequence of steps for AI to follow to create a predictable output.
Process files are content neutral to the project.

## Steps

This process has these distinct phases:

1. **Interview Phase** - Ask for the pieces of the process file that we are going to build
2. **Draft Phase** - Create the initial version of the process file
3. **Clarification Phase** - Ask any clarifying questions about the process file
4. **Simplification Phase** - Remove unnecessary content

## Pieces

- [FILE_NAME]
- [HEADER]
- [STARTER_CHARACTER]
- Steps
  - Title
  - Details
  - Sub-steps (optional)
- [DESCRIPTION]

## Interview Protocol

Ask one question at a time.
If you are giving options, give a list to choose from.

## Phases

### Phase 1: Interview

1. Read the provided file, and ask for the [FILE_NAME] if not provided.
2. Ask for the [HEADER] for the file.
3. Ask for a small [DESCRIPTION] of what this process is going to achieve.
4. Ask for the [STARTER_CHARACTER] emoji. A STARTER_CHARACTER is a marker (usually an emoji) that appears at the beginning of each response to indicate that the context window is intact and rules are being followed. Suggest 5-8 appropriate emoji based on the process topic.
5. We need a list of steps. Ask for each step in the process, one at a time. If anything is unclear about a step, ask clarifying questions.
6. Identify any missing steps that would achieve the stated description of the process.

### Phase 2: Draft

Create the initial version of the process file, or revise it if it already exists.
Ask to review it.

### Phase 3: Clarification

Read the draft created in phase 2.
Check for inconsistencies, contradictions, or missing information.
If any are found, ask clarifying questions one at a time.

### Phase 4: Simplification

Review the process file created in phase 2 and simplify. Be as concise as possible.

## Examples

For an example of a process file, examine this file itself.
