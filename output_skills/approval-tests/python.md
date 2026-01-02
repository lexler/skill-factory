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

## Core Patterns

### verify() - Basic verification
```python
verify(result)                    # String output
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

## Key Rules

- Use verify_as_json() for objects, not str(). JSON is stable and diff-friendly
- Always scrub non-deterministic data. Timestamps, GUIDs, random IDs break tests
- One approval per behavior. Don't mix unrelated verifications

## Git Setup

```gitignore
*.received.*
```

Commit all `.approved.*` files.

## When to Read More

**Need a specific verify function?** → [API Reference](references/python/api.md)

**Testing legacy code or state machines?** → [Testing Patterns](references/python/patterns.md)

**Testing many input combinations?** → [Combination Testing](references/python/combinations.md)

**Dealing with timestamps, GUIDs, random values?** → [Scrubbers](references/python/scrubbers.md)

**Want approvals in docstrings?** → [Inline Approvals](references/python/inline.md)

**Verifying log output?** → [Logging Verification](references/python/logging.md)

**Setting up reporters or config?** → [Setup & Configuration](references/python/setup.md)
