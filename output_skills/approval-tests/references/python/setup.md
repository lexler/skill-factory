# Python ApprovalTests Setup

## Installation

```bash
pip install approvaltests
```

For minimal installation (no extras):
```bash
pip install approvaltests-minimal
```

## pytest Integration

Install the pytest plugin for reporter selection:
```bash
pip install pytest-approvaltests
```

Run tests with a reporter:
```bash
pytest --approvaltests-use-reporter='PythonNative'
```

### Example Test

```python
from approvaltests import verify

def test_simple():
    result = "Hello ApprovalTests"
    verify(result)
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

## Dependencies

**Required:**
```
pytest>=4.0.0
empty-files>=0.0.3
typing_extensions>=3.6.2
```

**Optional (for specific features):**
```
pyperclip>=1.5.29     # ClipboardReporter
beautifulsoup4>=4.4.0 # verify_html
allpairspy>=2.1.0     # verify_best_covering_pairs
testfixtures>=7.1.0   # verify_logging
mock>=5.1.0           # verify_logging
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
reporter = factory.get("BeyondCompare")  # or any configured reporter
verify("Hello", options=Options().with_reporter(reporter))
```

### Custom Diff Tool

```python
from approvaltests.reporters import GenericDiffReporter

reporter = GenericDiffReporter.create("/path/to/diff/tool")
verify("Hello", options=Options().with_reporter(reporter))
```

### Custom Reporter Class

Extend `Reporter` for full control:

```python
from approvaltests.core.reporter import Reporter

class MyReporter(Reporter):
    def report(self, received_path: str, approved_path: str) -> bool:
        # Compare files, show diff, or take custom action
        # Return True if handled, False to try next reporter
        print(f"Mismatch: {received_path} vs {approved_path}")
        return True
```

Use it:
```python
verify(result, options=Options().with_reporter(MyReporter()))
```

### Custom reporters.json

Create a JSON file:
```json
[
    ["BeyondCompare4", "/path/to/BCompare"],
    ["VSCode", "/path/to/code", "--diff"]
]
```

Load it:
```python
factory = GenericDiffReporterFactory()
factory.load('/path/to/myreporters.json')
reporter = factory.get_first_working()
```

## Git Configuration

Add to `.gitignore`:
```
*.received.*
```

Commit `.approved.*` files to version control.

## Python Versions

Supports: 3.8, 3.9, 3.10, 3.11, 3.12, 3.13, 3.14

## Gotchas

### PyCharm Strips Trailing Whitespace

PyCharm auto-removes trailing whitespace on save, causing approval files to mismatch.

Fix: File → Settings → Editor → General → On Save → uncheck "Remove trailing spaces"

### Test Passes Locally, Fails in CI

Common causes:
- **Line endings** - Windows vs Unix. Add `.gitattributes`: `*.approved.* text eol=lf`
- **Timezones** - Date output differs. Use scrubbers for timestamps.
- **Locale/encoding** - Set `PYTHONIOENCODING=utf-8` in CI
- **Missing scrubber** - Environment-specific data (paths, hostnames) not scrubbed
