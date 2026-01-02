# Python ApprovalTests Setup

## Contents

- [Installation](#installation)
- [pytest Integration](#pytest-integration)
- [unittest Integration](#unittest-integration)
- [Reporters](#reporters)
- [Configuration](#configuration)
- [Git Setup](#git-setup)
- [CI Troubleshooting](#ci-troubleshooting)

## Installation

```bash
pip install approvaltests
```

For pytest reporter selection:

```bash
pip install pytest-approvaltests
```

Optional dependencies:

```bash
pip install pyperclip        # ClipboardReporter
pip install beautifulsoup4   # verify_html
pip install allpairspy       # verify_best_covering_pairs
pip install testfixtures mock  # verify_logging
```

## pytest Integration

```python
from approvaltests import verify

def test_simple():
    result = "Hello ApprovalTests"
    verify(result)
```

Run with reporter:

```bash
pytest --approvaltests-use-reporter='PythonNative'
```

## unittest Integration

```python
import unittest
from approvaltests import verify

class MyTest(unittest.TestCase):
    def test_simple(self):
        verify("Hello ApprovalTests")

if __name__ == "__main__":
    unittest.main()
```

## Reporters

### Using Options

```python
from approvaltests import verify, Options
from approvaltests.reporters import PythonNativeReporter

verify("Hello", options=Options().with_reporter(PythonNativeReporter()))
```

### Using Factory

```python
from approvaltests import verify, Options
from approvaltests.reporters import GenericDiffReporterFactory

factory = GenericDiffReporterFactory()
reporter = factory.get("BeyondCompare")
verify("Hello", options=Options().with_reporter(reporter))
```

### Custom Diff Tool

```python
from approvaltests import verify, Options
from approvaltests.reporters import GenericDiffReporter

reporter = GenericDiffReporter.create("/path/to/diff/tool")
verify("Hello", options=Options().with_reporter(reporter))
```

### Custom Reporter Class

```python
from approvaltests import verify, Options
from approvaltests.core.reporter import Reporter

class MyReporter(Reporter):
    def report(self, received_path: str, approved_path: str) -> bool:
        print(f"Mismatch: {received_path} vs {approved_path}")
        return True

verify(result, options=Options().with_reporter(MyReporter()))
```

### Default Reporter

Set globally:

```python
from approvaltests import set_default_reporter
from approvaltests.reporters import PythonNativeReporter

set_default_reporter(PythonNativeReporter())
```

Or via pytest fixture in `conftest.py`:

```python
import pytest
from approvaltests import set_default_reporter
from approvaltests.reporters import PythonNativeReporter

@pytest.fixture(scope="session", autouse=True)
def configure_approvaltests():
    set_default_reporter(PythonNativeReporter())
```

## Configuration

### Approval File Subdirectory

Place `approvaltests_config.json` in test directory:

```json
{
  "subdirectory": "approved_files"
}
```

All `.approved` and `.received` files go to `tests/approved_files/`.

### Custom File Extensions

```python
from approvaltests import verify, Options

verify(html_content, options=Options().for_file.with_extension(".html"))
verify(xml_content, options=Options().for_file.with_extension(".xml"))
```

## Git Setup

Add to `.gitignore`:

```
*.received.*
```

Commit all `.approved.*` files.

For consistent line endings across platforms, add to `.gitattributes`:

```
*.approved.* text eol=lf
```

## CI Troubleshooting

### Test passes locally, fails in CI

Common causes:

**Line endings** - Windows vs Unix

Solution: Add `.gitattributes` rule above

**Timezones** - Date output differs by environment

Solution: Use scrubbers for timestamps (see [scrubbers.md](scrubbers.md))

**Locale/encoding** - Character encoding differs

Solution: Set `PYTHONIOENCODING=utf-8` in CI

**Missing scrubber** - Environment-specific data not scrubbed

Common culprits: file paths, hostnames, process IDs, timestamps

### PyCharm strips trailing whitespace

PyCharm auto-removes trailing whitespace on save, causing approval files to mismatch.

Fix: File → Settings → Editor → General → On Save → uncheck "Remove trailing spaces"

### Comparing files manually

```bash
git diff --no-index test.approved.txt test.received.txt
```
