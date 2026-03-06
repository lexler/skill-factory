# Lens: Patterns

Code often implements patterns without naming them. Making patterns explicit helps readers understand the structure.

## The Question

What patterns exist in this code that aren't explicitly named or visible in the structure?

## How to Spot

- Repeated structures that follow a template
- Code that "feels like" a known pattern (parser, state machine, strategy, builder)
- Implicit rules or grammar that could be made explicit
- Duplication that hints at an underlying pattern

## Trade-off

Not every pattern needs to be named. Sometimes explicit is better than DRY. Ask: does naming this pattern make the code clearer, or just more abstract?

## Process

Step back and look at the shape of the code. What patterns emerge? What would you call the overall approach?

## Go Deeper

What other patterns exist? What structure is implicit that could be explicit?
