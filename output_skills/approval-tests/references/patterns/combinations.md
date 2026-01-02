# Combination Testing

Test all combinations of input parameters with a single approval file.

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
(size: small, color: green) => small-green-product
(size: medium, color: red) => medium-red-product
...
```

## Python

### verify_all_combinations()

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

### verify_all_combinations_with_labeled_input()

Clearer output with parameter names:

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

### verify_best_covering_pairs()

Pairwise testing - fewer combinations while covering all pairs:

```python
from approvaltests import verify_best_covering_pairs

def test_pricing():
    verify_best_covering_pairs(
        calculate_price,
        [sizes, quantities, discounts, shipping_options]
    )
# Tests ~20 combinations instead of hundreds
```

## JavaScript

### Jest

```javascript
import { verifyAllCombinations2 } from 'approvals/lib/Providers/Jest/CombinationApprovals';

it('tests all combinations', () => {
  verifyAllCombinations2(
    (size, color) => createProduct(size, color),
    ['small', 'medium', 'large'],
    ['red', 'blue']
  );
});
```

Methods for 1-9 parameters:
- `verifyAllCombinations1(func, params1)`
- `verifyAllCombinations2(func, params1, params2)`
- ...up to `verifyAllCombinations9`

## Java

```java
import org.approvaltests.combinations.CombinationApprovals;

@Test
void testAllCombinations() {
    CombinationApprovals.verifyAllCombinations(
        (size, color) -> createProduct(size, color),
        new String[]{"small", "medium", "large"},
        new String[]{"red", "blue"}
    );
}
```

### Pairwise Testing

```java
CombinationApprovals.verifyBestCoveringPairs(
    (a, b, c) -> process(a, b, c),
    params1, params2, params3
);
```

### Skip Invalid Combinations

```java
CombinationApprovals.verifyAllCombinations(
    (size, shipping) -> {
        if (size.equals("large") && shipping.equals("express")) {
            throw new SkipCombination();  // Invalid combo
        }
        return process(size, shipping);
    },
    sizes, shippingOptions
);
```

## When to Use

**All Combinations** - When:
- Total combinations are manageable (<100)
- All combinations are valid
- You want exhaustive coverage

**Pairwise (Best Covering Pairs)** - When:
- Many parameters with many values
- Most bugs involve 2-parameter interactions
- Full combinations would be thousands

## Tips

1. **Start small** - Begin with 2-3 values per parameter
2. **Add edge cases** - Include nulls, empty strings, boundary values
3. **Use meaningful values** - Not just "a", "b", "c"
4. **Review the output** - Combinations reveal unexpected behaviors
