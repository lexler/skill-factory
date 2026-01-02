# Python Combination Testing

Test all combinations of input parameters with a single approval file.

## Contents

- [Why Use Combinations?](#why-use-combinations)
- [verify_all_combinations()](#verify_all_combinations)
- [verify_all_combinations_with_labeled_input()](#verify_all_combinations_with_labeled_input)
- [verify_best_covering_pairs()](#verify_best_covering_pairs)
- [When to Use](#when-to-use)
- [Tips](#tips)

## Why Use Combinations?

Instead of writing N×M tests for N×M input combinations:

```python
def test_small_red(): assert process("small", "red") == ...
def test_small_blue(): assert process("small", "blue") == ...
def test_medium_red(): assert process("medium", "red") == ...
# ... tedious and error-prone
```

Write one test that captures all combinations:

```python
verify_all_combinations(
    process,
    sizes=["small", "medium", "large"],
    colors=["red", "blue", "green"]
)
```

Output:
```
(size: small, color: red) => small-red-product
(size: small, color: blue) => small-blue-product
...
```

## verify_all_combinations()

```python
from approvaltests import verify_all_combinations

def test_pricing():
    verify_all_combinations(
        calculate_price,
        [
            ["small", "medium", "large"],  # sizes
            [1, 5, 10],                     # quantities
            [True, False],                  # with_discount
        ]
    )
```

## verify_all_combinations_with_labeled_input()

Clearer output with parameter names (recommended):

```python
from approvaltests import verify_all_combinations_with_labeled_input

def test_pricing():
    verify_all_combinations_with_labeled_input(
        calculate_price,
        size=["small", "medium", "large"],
        quantity=[1, 5, 10],
        with_discount=[True, False],
    )
```

## verify_best_covering_pairs()

Pairwise testing - fewer combinations while covering all pairs. Requires `allpairspy` package.

```python
from approvaltests import verify_best_covering_pairs

def test_pricing():
    verify_best_covering_pairs(
        calculate_price,
        [sizes, quantities, discounts, shipping_options]
    )
# Tests ~20 combinations instead of hundreds
```

## When to Use

All Combinations:
- Total combinations are manageable (<100)
- All combinations are valid
- You want exhaustive coverage

Pairwise (Best Covering Pairs):
- Many parameters with many values
- Most bugs involve 2-parameter interactions
- Full combinations would be thousands

## Tips

- Prefer labeled input. `verify_all_combinations_with_labeled_input()` produces clearer output
- Start small. Begin with 2-3 values per parameter
- Add edge cases. Include None, empty strings, boundary values
- Use meaningful values, not just "a", "b", "c"
- Review the output. Combinations reveal unexpected behaviors
