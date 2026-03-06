# Lens: Structural Storytelling

Code structure should tell a story. A reader should understand what the code does by how it's organized, before reading the details.

## The Question

Does the structure of this code tell its story? Can someone understand the flow without jumping around?

## The Narrative Hierarchy

Code should read from high-level to low-level:
1. **Entry points** — public API, main orchestration (what this code DOES)
2. **Direct helpers** — functions that entry points call
3. **Utilities** — low-level operations, foundational functions

## How to Spot

- Entry points buried in the middle or bottom of files
- Helper functions defined before the functions that use them
- Having to scroll up and down to understand the flow
- Implementation details appearing before the big picture

## The Test

Cover the bottom half of the file. Can you understand what the code does from just the top?

## Go Deeper

What else obscures the story? What structural changes would make the narrative clearer?
