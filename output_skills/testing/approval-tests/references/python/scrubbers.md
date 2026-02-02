# Python Scrubbers

Scrubbers normalize non-deterministic data before comparison. Flaky tests across environments usually means unscrubbed timestamps, UUIDs, ports, or paths.

## Contents

- [Imports](#imports)
- [Built-in Scrubbers](#built-in-scrubbers)
- [DateScrubber](#datescrubber)
- [Regex Scrubber](#regex-scrubber)
- [Line Scrubber](#line-scrubber)
- [Combining Scrubbers](#combining-scrubbers)
- [Custom Scrubber Function](#custom-scrubber-function)

## Imports

```python
from approvaltests import verify, Options
from approvaltests.scrubbers import (
    scrub_all_guids,
    scrub_all_dates,
    create_regex_scrubber,
    create_line_scrubber,
    combine_scrubbers,
)
from approvaltests.scrubbers.date_scrubber import DateScrubber
```

## Built-in Scrubbers

### scrub_all_guids

Replaces UUIDs with `<guid_0>`, `<guid_1>`, etc. Same GUID gets same replacement.

```python
from approvaltests import verify, Options
from approvaltests.scrubbers import scrub_all_guids

verify(
    "ID: 2fd78d4a-ad49-447d-96a8-deda585a9aa5",
    options=Options().with_scrubber(scrub_all_guids)
)
# Output: ID: <guid_0>
```

### scrub_all_dates

Replaces `YYYY-MM-DD HH:MM:SS` format with `<date0>`, `<date1>`, etc.

```python
from approvaltests import verify, Options
from approvaltests.scrubbers import scrub_all_dates

verify(
    "Created: 2024-01-15 10:30:00",
    options=Options().with_scrubber(scrub_all_dates)
)
# Output: Created: <date0>
```

## DateScrubber

For date formats not covered by `scrub_all_dates`, use `DateScrubber.get_scrubber_for()` with an example date matching your format:

```python
from approvaltests import verify, Options
from approvaltests.scrubbers.date_scrubber import DateScrubber

scrubber = DateScrubber.get_scrubber_for("03:14:15")

verify("Started at 10:30:45", options=Options().with_scrubber(scrubber))
# Output: Started at <date0>
```

Supported formats include:
- `2020-02-02` - ISO date
- `2020-09-10T01:23:45.678Z` - ISO 8601 with milliseconds
- `Tue May 13 16:30:00 2014` - ctime format
- `May 13, 2014 11:30:00 PM PST` - US format with timezone

### Custom Date Format

```python
from approvaltests.scrubbers.date_scrubber import DateScrubber

DateScrubber.add_scrubber(
    "2025-07-20",
    r"\d{4}-\d{2}-\d{2}",
    display_message=False
)

scrubber = DateScrubber.get_scrubber_for("2025-07-20")
```

## Regex Scrubber

### Static Replacement

```python
from approvaltests import verify, Options
from approvaltests.scrubbers import create_regex_scrubber

scrubber = create_regex_scrubber(r"user_\d+", "<USER>")

verify("Created by user_12345", options=Options().with_scrubber(scrubber))
# Output: Created by <USER>
```

### Indexed Replacement

```python
from approvaltests import verify, Options
from approvaltests.scrubbers import create_regex_scrubber

scrubber = create_regex_scrubber(
    r"user_\d+",
    lambda n: f"<user_{n}>"
)

verify("user_123 assigned to user_456", options=Options().with_scrubber(scrubber))
# Output: <user_0> assigned to <user_1>
```

## Line Scrubber

Removes entire lines containing a substring:

```python
from approvaltests import verify, Options
from approvaltests.scrubbers import create_line_scrubber

scrubber = create_line_scrubber("password")

verify(
    "user: admin\npassword: secret123\nemail: a@b.com",
    options=Options().with_scrubber(scrubber)
)
# Output:
# user: admin
# email: a@b.com
```

## Combining Scrubbers

### Using combine_scrubbers()

```python
from approvaltests import verify, Options
from approvaltests.scrubbers import combine_scrubbers, scrub_all_guids, scrub_all_dates, create_regex_scrubber

scrubber = combine_scrubbers(
    scrub_all_guids,
    scrub_all_dates,
    create_regex_scrubber(r"secret_\w+", "[REDACTED]"),
)

verify(data, options=Options().with_scrubber(scrubber))
```

### Using add_scrubber() chain

```python
from approvaltests import verify, Options
from approvaltests.scrubbers import scrub_all_guids, scrub_all_dates, create_line_scrubber

options = (Options()
    .with_scrubber(scrub_all_guids)
    .add_scrubber(scrub_all_dates)
    .add_scrubber(create_line_scrubber("DEBUG")))

verify(data, options=options)
```

## Custom Scrubber Function

Any `str -> str` function works:

```python
from approvaltests import verify, Options

def redact_env(text: str) -> str:
    return text.replace("PRODUCTION", "[ENV]")

verify(data, options=Options().with_scrubber(redact_env))
```
