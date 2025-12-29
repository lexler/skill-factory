# ZOMBIES - Test Case Discovery Heuristic

Use this checklist when planning tests to ensure completeness.

**Z** - Zero: What happens with zero, empty, null, none?
**O** - One: What happens with exactly one item?
**M** - Many: What happens with multiple items? (Also: More complex scenarios)
**B** - Boundary: Edge cases, limits, off-by-one errors
**I** - Interface: Does the API make sense? Are inputs/outputs clear?
**E** - Exceptions: Error conditions, invalid inputs, exceptional paths
**S** - Simple: Start with the simplest scenario first

## Example: Testing a shopping cart

```
[TEST] Empty cart has zero total                         <- Z
[TEST] Cart with one item shows that item's price        <- O
[TEST] Cart with multiple items sums their prices        <- M
[TEST] Cart handles maximum item quantity                <- B
[TEST] Adding item returns updated cart                  <- I
[TEST] Adding negative quantity throws error             <- E
[TEST] Cart exists when created                          <- S (start here)
```

Order tests by simplicity, not by ZOMBIES order.
