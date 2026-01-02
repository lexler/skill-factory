# Python Testing Patterns

## Contents

- [Quick Decision Guide](#quick-decision-guide)
- [Characterization Tests](#characterization-tests)
- [Multiple Approvals Per Test](#multiple-approvals-per-test)
- [Common Mistakes](#common-mistakes)

## Quick Decision Guide

- Objects → `verify_as_json(obj)`, not `verify(str(obj))`
- Lists (structured) → `verify_as_json({"items": items})`
- Lists (labeled) → `verify_all("Items", items, formatter)`
- Non-deterministic data → scrubbers, add before first run ([scrubbers.md](scrubbers.md))
- Multiple scenarios per test → `NamerFactory.with_parameters()`, not multiple `verify()` calls
- Input combinations → [combinations.md](combinations.md)
- State progression → Storyboard ([api.md](api.md))
- Log output → [logging.md](logging.md)

## Characterization Tests

Capture existing behavior before refactoring:

```python
from approvaltests import verify

def test_legacy_billing():
    result = legacy_billing_system.calculate(test_order)
    verify(result)
```

Run once to capture current behavior as baseline. The approval file becomes your safety net during refactoring.

## Multiple Approvals Per Test

By default, one `verify()` per test. For multiple approvals, use `NamerFactory.with_parameters()`.

### Parametrized Tests (pytest)

```python
import pytest
from approvaltests import verify
from approvaltests.namer import NamerFactory

@pytest.mark.parametrize("year", [1992, 1993, 1900, 2000])
def test_leap_year(year):
    result = is_leap_year(year)
    verify(f"{year}: {result}", options=NamerFactory.with_parameters(year))
```

Creates: `test_leap_year.1992.approved.txt`, `test_leap_year.1993.approved.txt`, etc.

### Multiple Verifies in One Test

```python
from approvaltests import verify, settings
from approvaltests.namer import NamerFactory

def test_multiple():
    settings().allow_multiple_verify_calls_for_this_method()

    verify(result1, options=NamerFactory.with_parameters("scenario1"))
    verify(result2, options=NamerFactory.with_parameters("scenario2"))
```

### Run All, Report All Failures

```python
from approvaltests import verify
from approvaltests.asserts import gather_all_exceptions_and_throw
from approvaltests.namer import NamerFactory

def test_all_scenarios():
    scenarios = ["a", "b", "c", "d"]
    gather_all_exceptions_and_throw(
        scenarios,
        lambda s: verify(process(s), options=NamerFactory.with_parameters(s))
    )
```

### Adding Suffix to Filename

```python
from approvaltests import verify, Options

verify(result, options=Options().for_file.with_additional_information("scenario1"))
```

Creates: `TestClass.test_method.scenario1.approved.txt`

## Common Mistakes

### Mixing approvals with assertions

The approval captures everything. If you're adding assertions alongside `verify()`, you're probably testing two things.

```python
# Not this
def test_user():
    user = create_user()
    assert user.id > 0
    verify_as_json(user)

# This - the approval captures everything including id
def test_user():
    verify_as_json(create_user())
```

### Over-approving

Approving an entire database record when you only care about one field. Large approvals hide real changes in noise.

```python
# Not this - approves 50 fields when you care about 3
verify_as_json(full_user_record)

# This - approve only what matters
verify_as_json({
    "name": user.name,
    "email": user.email,
    "status": user.status,
})
```

### Under-scrubbing

Tests pass locally, fail in CI.

If it varies by environment, scrub it:
- Timestamps
- UUIDs/GUIDs
- File paths
- Hostnames
- Process IDs

### Hand-editing .approved files

Breaks the contract. The approved file should only be created by running the test and approving the received output.

If the output is wrong, fix the code and regenerate.

### Multiple verify() without NamerFactory

Each `verify()` overwrites the same file. Only the last one is tested.

```python
# Broken - only tests result2
def test_both():
    verify(result1)
    verify(result2)

# Fixed - separate files
def test_both():
    settings().allow_multiple_verify_calls_for_this_method()
    verify(result1, options=NamerFactory.with_parameters("first"))
    verify(result2, options=NamerFactory.with_parameters("second"))
```
