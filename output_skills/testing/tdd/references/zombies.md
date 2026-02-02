# ZOMBIES - Test Case Discovery Heuristic

## Structure

**ZOM axis** (simple → complex):
- **Z** - Zero: initial state after creation (empty, not full, default values)
- **O** - One: first item, first transition
- **M** - Many: multiple items, more complex scenarios

**BIE considerations** (apply at each ZOM level):
- **B** - Boundary: transitions between states, both directions (empty↔not-empty, not-full↔full)
- **I** - Interface: let tests reveal what methods, parameters, and return types are needed
- **E** - Exceptions: error conditions, and verify the object still works after errors

**S** - Simple scenarios, simple solutions (applies throughout)

## Key principles

**Test transitions, not just states.** Verify moving from empty to not-empty, and back again.

**Procrastinate deliberately.** Defer implementation until tests demand it. Hard-coded return values are fine - tests will catch if you forget to generalize.

**Interface emerges from tests.** Don't design the API upfront. Write tests, and the needed methods reveal themselves.

**Exceptions come last.** Get happy paths working first, then test error conditions. Verify that failed operations don't corrupt the object.

## Example: Circular buffer (FIFO)

```
[TEST] New buffer is empty                               <- Z
[TEST] New buffer is not full                            <- Z
[TEST] Put one item, buffer is not empty                 <- O
[TEST] Put then get returns the item                     <- O + I
[TEST] Put then get, buffer is empty again               <- O + B (transition back)
[TEST] Put three items, get returns them in order        <- M
[TEST] Fill to capacity, buffer is full                  <- M + B
[TEST] Wrap around: fill, empty, refill works            <- M + B
[TEST] Put to full buffer fails                          <- E
[TEST] Get from empty buffer fails                       <- E
[TEST] After failed put, buffer still works              <- E (integrity check)
```

---
Source: [TDD Guided by ZOMBIES](https://blog.wingman-sw.com/tdd-guided-by-zombies) by James Grenning
