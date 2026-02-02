# Python ApprovalTests

## Installation

```bash
pip install approvaltests
```

## Quick Start

```python
from approvaltests import verify

def test_report():
    result = generate_report()
    verify(result)
```

First run fails and creates two files:
- `test_file.test_report.received.txt` - actual output
- `test_file.test_report.approved.txt` - empty (the expectation)

Review `.received`, if correct, copy to `.approved`. Rerun → passes.

## Recommended Imports

```python
from approvaltests import verify, verify_as_json, verify_all, Options
from approvaltests.scrubbers import scrub_all_guids, scrub_all_dates, create_regex_scrubber
```

## Core Patterns

### verify_as_json() - Objects (preferred for structured data)

```python
from approvaltests import verify_as_json

def test_user():
    user = get_user(123)
    verify_as_json(user)
```

Produces readable, diff-friendly JSON. Use this for any object, dict, or list.

### verify_all() - Collections with labels

```python
from approvaltests import verify_all

def test_users():
    users = get_all_users()
    verify_all("Users", users, lambda u: f"{u.name}: {u.email}")
```

### Scrubbing timestamps, GUIDs, random values

```python
from approvaltests import verify, Options
from approvaltests.scrubbers import scrub_all_dates, scrub_all_guids

def test_api_response():
    response = call_api()
    options = Options().with_scrubber(scrub_all_dates).add_scrubber(scrub_all_guids)
    verify(response, options=options)
```

Always add scrubbers BEFORE the first test run, not after CI fails.

### Combination testing

```python
from approvaltests import verify_all_combinations_with_labeled_input

def test_pricing():
    verify_all_combinations_with_labeled_input(
        calculate_price,
        size=["S", "M", "L"],
        color=["red", "blue"],
        express=[True, False],
    )
```

Tests all 12 combinations in one approval file.

### Multiple scenarios per test

`NamerFactory.with_parameters()` creates separate approval files per scenario. See [patterns.md](references/python/patterns.md).

## Git Setup

```gitignore
*.received.*
```

Commit all `.approved.*` files.

## Reference Files

- [api.md](references/python/api.md) - verify_xml/html/binary, Storyboard, MarkdownTable, Options methods
- [scrubbers.md](references/python/scrubbers.md) - Custom date formats, regex patterns, combining scrubbers, line removal
- [combinations.md](references/python/combinations.md) - Input combinations, pairwise testing, exception handling
- [patterns.md](references/python/patterns.md) - Characterization tests, multiple approvals per test, common mistakes
- [inline.md](references/python/inline.md) - Expectations in docstrings instead of .approved files
- [logging.md](references/python/logging.md) - Log output verification, SimpleLogger method tracing
- [reporters.md](references/python/reporters.md) - Custom diff tools, reporter chains
- [setup.md](references/python/setup.md) - CI troubleshooting, pytest config, approval file locations
