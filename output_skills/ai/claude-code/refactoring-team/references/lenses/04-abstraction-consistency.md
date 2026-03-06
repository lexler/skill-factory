# Lens: Abstraction Consistency

Each function should operate at one level of abstraction. Don't mix orchestration with implementation details.

## The Question

Are functions mixing high-level flow with low-level details?

## How to Spot

Look at a function's body:
- Are all the lines at the same "level"?
- Is there inline code surrounded by function calls?
- Does the function orchestrate (call other functions) AND do detailed work?

Example of inconsistency: a function that calls `validate()`, `process()`, then has 10 lines of inline file path manipulation, then calls `save()`.

## Process

Read each function. Does it feel like everything belongs together at the same level? Or are some lines "zoomed in" compared to others?

## Go Deeper

What other functions mix levels? Where else is orchestration mixed with implementation?
