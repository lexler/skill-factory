# Lens: Method Length

Long functions do too much. Each function should do one thing that can be named.

## The Question

What functions are trying to do multiple things? What sequences could be extracted and named?

## How to Spot

- Functions with multiple "phases" or "steps"
- Long sequences of operations that form a logical unit
- Deep nesting (often signals multiple concerns)
- Code blocks that could stand alone with a clear name

## Early Returns

Deep nesting often signals too much in one function. Early returns can:
- Handle edge cases first, reducing indentation
- Make the happy path obvious
- Eliminate else branches entirely

## Process

Look at each function. Could you split it? What would you name the pieces?

## Go Deeper

What other long functions exist? What sequences are hiding that deserve a name?
