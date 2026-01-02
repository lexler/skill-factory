# Approval Testing Patterns

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

## Storyboard Pattern

Verify sequences of states:

```python
story = Storyboard()
story.add_frame(initial_state)
story.add_frame(after_action, title="After click")
story.add_frame(final_state, title="Final")
verify(story)
```

Good for:
- State machine transitions
- Multi-step workflows
- Animation frames

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
verify_html(html_string)
```

## Inline Approvals

Store expected output in test code (Python, Java):

```python
def test_greeting():
    """
    Hello World!
    """
    verify(get_greeting(), options=Options().inline())
```

## Naming Conventions

Default: `{TestClass}.{test_method}.approved.txt`

Custom naming for scenarios:

```python
verify(result, options=Options()
    .for_file.with_additional_information("scenario1"))
```

## Multiple Approvals Per Test

When you need separate approval files for different scenarios in one test:

```python
from approvaltests.namer import NamerFactory

def test_user_states():
    verify(user_before, options=NamerFactory.with_parameters("before"))
    verify(user_after, options=NamerFactory.with_parameters("after"))
```

Creates: `test_user_states.before.approved.txt` and `test_user_states.after.approved.txt`

For non-blocking verification (run all, report all failures):

```python
from approvaltests.asserts import gather_all_exceptions_and_throw

gather_all_exceptions_and_throw(
    scenarios,
    lambda s: verify(process(s), options=NamerFactory.with_parameters(s))
)
```

See Python details: [advanced.md](../python/advanced.md)

## Verifying Logs and Results

When you need both log output and return value verified:

**Option 1: Log the result too** (single approval file)
```python
with verify_logging():
    result = process_data()
    logging.info(f"result = {result}")
```

**Option 2: Separate files**
```python
with verify_logging(options=NamerFactory.with_parameters("logs")):
    result = process_data()
verify(result)  # Separate approval file
```

See Python details: [logging.md](../python/logging.md)

## Tips

1. **One approval per behavior** - Don't verify unrelated things together
2. **Commit .approved files** - They're your test expectations
3. **Never commit .received files** - Add `*.received.*` to .gitignore
4. **Use scrubbers early** - Avoid flaky tests from day one
5. **Review diffs carefully** - They show exactly what changed
