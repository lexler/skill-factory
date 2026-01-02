# Python Inline Approvals

Inline approvals store the expected output directly in the test's docstring instead of separate `.approved` files.

## Basic Usage

```python
from approvaltests import verify, Options

def test_fizz_buzz():
    """
    1
    2
    Fizz
    4
    Buzz
    """
    verify(fizz_buzz(5), options=Options().inline())
```

The docstring IS the approved output. When the test runs:
- If output matches docstring → pass
- If output differs → reporter shows diff, can auto-update docstring

## InlineOptions

Control inline approval behavior:

```python
from approvaltests import verify, Options
from approvaltests.inline.inline_options import InlineOptions

# Automatic mode - auto-approves without confirmation
options = Options().inline(InlineOptions.automatic())

# Semi-automatic - requires manual deletion of marker to approve
options = Options().inline(InlineOptions.semi_automatic())

# Shows previous approved alongside current result
options = Options().inline(InlineOptions.semi_automatic_with_previous_approved())
```

### Semi-Automatic Marker

When using `semi_automatic()`, the docstring gets a marker:
```python
def test_example():
    """
    new result here
    ***** DELETE ME TO APPROVE *****
    """
```

Delete the marker line to approve the new result.

## Parse Class

For input → output style tests:

```python
from approvaltests.inline.parse import Parse

def test_uppercase():
    """
    hello -> HELLO
    world -> WORLD
    """
    Parse.doc_string().verify_all(lambda s: s.upper())

def test_add():
    """
    1, 2 -> 3
    5, 3 -> 8
    """
    Parse.doc_string().transform2(int, int).verify_all(lambda a, b: a + b)
```

For auto-approve: `Parse.doc_string(auto_approve=True)`

## With Combinations

```python
from approvaltests import verify_all_combinations_with_labeled_input, Options

def test_combinations():
    """
    (arg1: 1, arg2: 2) => 3
    (arg1: 1, arg2: 4) => 5
    (arg1: 3, arg2: 2) => 5
    (arg1: 3, arg2: 4) => 7
    """
    verify_all_combinations_with_labeled_input(
        lambda a, b: a + b,
        arg1=(1, 3),
        arg2=(2, 4),
        options=Options().inline(),
    )
```

## Preserving Whitespace

Use marker for leading whitespace:

```python
def test_indented():
    """
    <<approvaltests:preserve-leading-whitespace>>
        4 spaces indent
            8 spaces indent
    """
    verify(get_indented_text(), options=Options().inline())
```

## When to Use

Inline approvals:
- Short output (few lines)
- Input→output mapping tests
- Tests and expectations co-located

File approvals:
- Long or complex output
- Binary data
- JSON/XML benefiting from syntax highlighting
