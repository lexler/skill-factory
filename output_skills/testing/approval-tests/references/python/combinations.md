# Python Combination Testing

Test all combinations of input parameters with a single approval file.

## Contents

- [verify_all_combinations_with_labeled_input](#verify_all_combinations_with_labeled_input)
- [verify_all_combinations](#verify_all_combinations)
- [verify_best_covering_pairs](#verify_best_covering_pairs)
- [Handling Edge Cases](#handling-edge-cases)
- [When to Use Which](#when-to-use-which)

## verify_all_combinations_with_labeled_input

Recommended. Parameter names appear in output.

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

Output:

```
(size: small, quantity: 1, with_discount: True) => 8.50
(size: small, quantity: 1, with_discount: False) => 10.00
(size: small, quantity: 5, with_discount: True) => 42.50
...
```

## verify_all_combinations

Positional arguments. Less readable output, but works for simple cases.

```python
from approvaltests import verify_all_combinations

def test_pricing():
    verify_all_combinations(
        calculate_price,
        [
            ["small", "medium", "large"],
            [1, 5, 10],
            [True, False],
        ]
    )
```

Output:

```
[small, 1, True] => 8.50
[small, 1, False] => 10.00
...
```

## verify_best_covering_pairs

Pairwise testing - covers all two-parameter combinations with fewer test cases. Requires `allpairspy`.

```python
from approvaltests import verify_best_covering_pairs

def test_pricing():
    verify_best_covering_pairs(
        calculate_price,
        [
            ["small", "medium", "large"],
            [1, 5, 10, 20, 50],
            [True, False],
            ["standard", "express", "overnight"],
        ]
    )
```

Full combinations: 3×5×2×3 = 90 tests
Pairwise: ~15-20 tests, still covers all parameter pairs

## Handling Edge Cases

### Include None and empty values

```python
from approvaltests import verify_all_combinations_with_labeled_input

def test_user_creation():
    verify_all_combinations_with_labeled_input(
        create_user,
        name=["Alice", "", None],
        email=["a@b.com", "invalid", None],
        age=[25, 0, -1, None],
    )
```

### Handling exceptions

Exceptions appear in output as error messages:

```python
from approvaltests import verify_all_combinations_with_labeled_input

def test_division():
    verify_all_combinations_with_labeled_input(
        lambda a, b: a / b,
        a=[10, 0],
        b=[2, 0],
    )
```

Output:

```
(a: 10, b: 2) => 5.0
(a: 10, b: 0) => ZeroDivisionError: division by zero
(a: 0, b: 2) => 0.0
(a: 0, b: 0) => ZeroDivisionError: division by zero
```

### Custom formatting

```python
from approvaltests import verify_all_combinations_with_labeled_input

def format_result(result):
    if isinstance(result, float):
        return f"${result:.2f}"
    return str(result)

def test_pricing():
    verify_all_combinations_with_labeled_input(
        calculate_price,
        size=["S", "M", "L"],
        quantity=[1, 10],
        formatter=format_result,
    )
```

## When to Use Which

Use `verify_all_combinations_with_labeled_input` (recommended):
- Most cases
- When output readability matters
- When parameter names help understand the test

Use `verify_all_combinations`:
- Simple positional functions
- When you already have lists of values

Use `verify_best_covering_pairs`:
- 4+ parameters with many values each
- Full combinations would be hundreds/thousands
- Most bugs involve 2-parameter interactions
