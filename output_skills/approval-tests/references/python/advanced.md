# Python Advanced Patterns

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

Creates separate files: `test_leap_year.1992.approved.txt`, `test_leap_year.1993.approved.txt`, etc.

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

Don't stop on first failure - run all verifies, report all failures:

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

## Configuration

### approvaltests_config.json

Place in test directory to configure subdirectory for approval files:

```json
{
  "subdirectory": "approved_files"
}
```

All `.approved` and `.received` files go to `tests/approved_files/` instead of alongside tests.

### Default Reporter

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

## Additional Info in Filename

```python
verify(result, options=Options().for_file.with_additional_information("scenario1"))
```

Creates: `TestClass.test_method.scenario1.approved.txt`
