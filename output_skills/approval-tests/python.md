# Python ApprovalTests

## Installation

```bash
pip install approvaltests
```

## Quick Start

```python
from approvaltests import verify, verify_as_json, verify_all

def test_report():
    result = generate_report()
    verify(result)
```

**First run:** Test fails, `.received` file created. Review it, approve it (copy to `.approved`), rerun.

## Common Imports

```python
from approvaltests import (
    verify,
    verify_as_json,
    verify_all,
    verify_all_combinations,
    Options,
)
from approvaltests.scrubbers import scrub_all_dates, scrub_all_guids
```

## Core Patterns

### verify() - Basic verification
```python
verify(result)                    # String output
verify(str(complex_object))       # Object via __str__
```

### verify_as_json() - Objects as formatted JSON
```python
verify_as_json(user)              # Pretty-printed JSON
verify_as_json({"users": users})  # Works with dicts, lists
```

### verify_all() - Collections with labels
```python
verify_all("Users", users, lambda u: f"{u.name}: {u.email}")
```

### Scrubbing non-deterministic data
```python
verify(result, options=Options().with_scrubber(scrub_all_dates))
```

### Combination testing
```python
verify_all_combinations(
    process_order,
    [["S", "M", "L"], ["red", "blue"], ["standard", "express"]]
)
```

## Python-Specific Notes

**Use verify_as_json() over str()** - Python's `__str__` may not be stable or readable. JSON gives consistent, diff-friendly output.

**pytest integration** - Works out of the box. File naming uses test function name.

**unittest integration** - Also supported, uses class.method naming.

## Git Setup

```gitignore
*.received.*
```

Commit all `.approved.*` files.

## Deep References

- [API Reference](references/python/api.md) - All verify functions and Options
- [Setup & Configuration](references/python/setup.md) - pytest plugin, reporters, config files
- [Scrubbers](references/python/scrubbers.md) - Handling timestamps, GUIDs, dynamic data
- [Inline Approvals](references/python/inline.md) - Store approvals in docstrings
- [Logging Verification](references/python/logging.md) - Test log output with SimpleLogger
- [Advanced Patterns](references/python/advanced.md) - Multiple approvals, parametrized tests, configuration
