# Python Testing Patterns

## Characterization Tests

Capture existing behavior before refactoring:

```python
def test_legacy_billing():
    result = legacy_billing_system.calculate(test_order)
    verify(result)  # Captures current behavior as baseline
```

Run once to capture, then refactor with safety net.

## JSON Verification

For complex objects, verify as formatted JSON:

```python
verify_as_json(user)
```

Benefits:
- Readable structure
- Diff-friendly format
- Catches added/removed fields

## Collection Verification

Verify lists with labels:

```python
verify_all("Users", users, lambda u: f"{u.name}: {u.email}")
```

Output:
```
Users
[0] = Alice: alice@example.com
[1] = Bob: bob@example.com
```

## Scrubbing Non-Deterministic Data

Handle dynamic values that change between runs:

```python
verify(result, options=Options()
    .with_scrubber(scrub_all_dates)
    .add_scrubber(scrub_all_guids))
```

Common scrub targets:
- Timestamps
- UUIDs/GUIDs
- Random IDs
- Process IDs
- Absolute file paths

See [scrubbers.md](scrubbers.md) for full API.

## Storyboard Pattern

Verify sequences of states (state machines, multi-step workflows, animations):

```python
from approvaltests.storyboard import Storyboard

story = Storyboard()
story.add_description("Initial setup")
story.add_frame(initial_state)
story.add_frame(after_action, title="After click")
story.add_frame(final_state, title="Final")
verify(story)
```

Or with context manager:

```python
from approvaltests import verify_storyboard

with verify_storyboard() as story:
    story.add_frame(state1)
    story.add_frame(state2)
```

Output stacks frames vertically for easy diffing.

## Exception Verification

Verify error messages:

```python
verify_exception(lambda: divide(1, 0))
```

## File Verification

Verify file contents:

```python
verify_file("output/report.txt")
```

## XML/HTML Pretty-Print

Auto-formats for readable diffs:

```python
verify_xml(xml_string)
verify_html(html_string)  # requires beautifulsoup4
```

## Inline Approvals

Store expected output in test docstring:

```python
def test_greeting():
    """
    Hello World!
    """
    verify(get_greeting(), options=Options().inline())
```

See [inline.md](inline.md) for advanced inline patterns.

## Multiple Approvals Per Test

By default, one `verify()` call per test. For multiple approvals, use `NamerFactory.with_parameters()`.

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

### Non-Blocking Multiple Verifies

Run all verifies, report all failures at once:

```python
from approvaltests import verify
from approvaltests.asserts import gather_all_exceptions_and_throw
from approvaltests.namer import NamerFactory

def test_all_scenarios():
    scenarios = ["a", "b", "c", "d"]
    gather_all_exceptions_and_throw(
        scenarios,
        lambda s: verify(
            process(s),
            options=NamerFactory.with_parameters(s)
        )
    )
```

## Custom Naming

Add scenario info to filename:

```python
verify(result, options=Options().for_file.with_additional_information("scenario1"))
```

Creates: `TestClass.test_method.scenario1.approved.txt`

## Verifying Logs and Results

When you need both log output and return value:

**Option 1: Log the result too** (single approval file)
```python
with verify_logging():
    result = process_data()
    logging.info(f"result = {result}")
```

**Option 2: Separate files**
```python
from approvaltests.namer import NamerFactory

with verify_logging(options=NamerFactory.with_parameters("logs")):
    result = process_data()
verify(result)  # Separate approval file
```

See [logging.md](logging.md) for more logging patterns.

## Tips

1. **One approval per behavior** - Don't verify unrelated things together
2. **Use scrubbers early** - Avoid flaky tests from day one
3. **Review diffs carefully** - They show exactly what changed
