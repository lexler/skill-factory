# Python Inline Approvals

Store expected output in the test's docstring instead of separate `.approved` files.
Helps solve the problem of "there's too many approved files" when the approved output is small.

## Contents

- [Basic Usage](#basic-usage)
- [InlineOptions](#inlineoptions)
- [Parse Class](#parse-class)
- [With Combinations](#with-combinations)
- [Preserving Whitespace](#preserving-whitespace)
- [When to Use](#when-to-use)

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
- Output matches docstring: pass
- Output differs: reporter shows diff, can auto-update docstring

## InlineOptions

```python
from approvaltests import verify, Options
from approvaltests.inline.inline_options import InlineOptions

# Automatic - auto-approves without confirmation
verify(result, options=Options().inline(InlineOptions.automatic()))

# Semi-automatic - adds marker you must delete to approve
verify(result, options=Options().inline(InlineOptions.semi_automatic()))

# Shows previous alongside new
verify(result, options=Options().inline(InlineOptions.semi_automatic_with_previous_approved()))
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

Delete the marker line to approve.

## Parse Class

For input/output mapping tests:

```python
from approvaltests.inline.parse import Parse

def test_uppercase():
    """
    hello -> HELLO
    world -> WORLD
    """
    Parse.doc_string().verify_all(lambda s: s.upper())
```

With type transforms:

```python
from approvaltests.inline.parse import Parse

def test_add():
    """
    1, 2 -> 3
    5, 3 -> 8
    """
    Parse.doc_string().transform2(int, int).verify_all(lambda a, b: a + b)
```

With auto-approve:

```python
Parse.doc_string(auto_approve=True).verify_all(lambda s: s.upper())
```

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
from approvaltests import verify, Options

def test_indented():
    """
    <<approvaltests:preserve-leading-whitespace>>
        4 spaces indent
            8 spaces indent
    """
    verify(get_indented_text(), options=Options().inline())
```

## When to Use

Inline approvals work best for:
- Short output (few lines)
- Input/output mapping tests
- Tests where expectation should be visible alongside code

File approvals work best for:
- Long or complex output
- Binary data
- JSON/XML where syntax highlighting helps
