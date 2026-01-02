# Python Configuration

## approvaltests_config.json

Place in test directory to configure subdirectory for approval files:

```json
{
  "subdirectory": "approved_files"
}
```

All `.approved` and `.received` files go to `tests/approved_files/` instead of alongside tests.

## Default Reporter

Set globally via `__init__.py`:

```python
# tests/__init__.py
from approvaltests import set_default_reporter
from approvaltests.reporters import PythonNativeReporter

def configure_approvaltests():
    set_default_reporter(PythonNativeReporter())

configure_approvaltests()
```

Or via pytest fixture in `conftest.py`:

```python
# conftest.py
import pytest
from tests.approvals_config import configure_approvaltests

@pytest.fixture(scope="session", autouse=True)
def set_default_reporter_for_all_tests():
    configure_approvaltests()
```

## Custom File Extensions

```python
verify(html_content, options=Options().for_file.with_extension(".html"))
verify(xml_content, options=Options().for_file.with_extension(".xml"))
```
