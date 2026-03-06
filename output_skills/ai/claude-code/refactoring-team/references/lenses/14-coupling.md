# Lens: Coupling & Dependencies

Code that knows too much about too many things. A change in one place ripples unpredictably through many others.

## The Question

What does each unit depend on, and is that dependency necessary?

## How to Spot

- Reaching through objects: `a.getB().getC().doThing()` — this unit knows its collaborators' internals
- One change, many files: a single conceptual change forces edits scattered across the codebase
- One file, many reasons to change: a module that changes whenever *anything* changes
- Pass-through: parameters or data flowing through a function untouched, coupling it to both caller and callee

## Process

Trace the ripple in both directions:
- Outward: if I changed this unit, what else would break?
- Inward: what forces *this* unit to change? How many unrelated reasons does it have to change?

If the ripple crosses many boundaries in either direction, the coupling is too tight.

## Trade-off

Some coupling is necessary — zero coupling means the code does nothing. The question is whether each dependency is *essential* (this unit genuinely needs it) or *accidental* (an artifact of how the code was written).

## Go Deeper

What coupling is still invisible? Where do framework details leak into domain logic? Where do modules depend on each other in circles?
