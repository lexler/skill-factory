# Python Logging Verification

Verify log output and trace method execution.

## Contents

- [SimpleLogger](#simplelogger)
- [verify_logging](#verify_logging)
- [Combining Logs with Results](#combining-logs-with-results)

## SimpleLogger

### verify_simple_logger()

Capture and verify everything logged in a context:

```python
from approvaltests.utilities.simple_logger import SimpleLogger, verify_simple_logger

def test_logging():
    with verify_simple_logger():
        SimpleLogger.variable("count", 42)
        SimpleLogger.variable("name", "Alice", show_types=True)
```

Output:

```
variable: count = 42
variable: name = Alice <str>
```

### Method Tracing with use_markers()

Log method entry/exit with parameters:

```python
from approvaltests.utilities.simple_logger import SimpleLogger, verify_simple_logger

def process(x, y):
    with SimpleLogger.use_markers(f"x = {x}, y = {y}"):
        pass

def test_process():
    with verify_simple_logger():
        process(1, 2)
```

Output:

```
-> in: process(x = 1, y = 2) in test_file
<- out: process()
```

For values that change during execution, use a lambda:

```python
from approvaltests.utilities.simple_logger import SimpleLogger, verify_simple_logger

def countdown(n):
    with SimpleLogger.use_markers(lambda: f"n = {n}"):
        while n > 0:
            n -= 1

def test_countdown():
    with verify_simple_logger():
        countdown(10)
```

Output:

```
-> in: countdown(n = 10) in test_file
<- out: countdown(n = 0)
```

### log_to_string()

Capture logs to a string for manual verification:

```python
from approvaltests import verify
from approvaltests.utilities.simple_logger import SimpleLogger

def test_with_string():
    output = SimpleLogger.log_to_string()
    SimpleLogger.variable("x", 123)
    verify(output)
```

## verify_logging

Verify standard Python logging output. Requires `testfixtures` and `mock`.

```python
import logging
from approvaltests.utilities.logging import verify_logging

def test_logs():
    with verify_logging():
        logging.info("Starting process")
        logging.warning("Watch out")
```

## Combining Logs with Results

Three approaches when you need both log output and return value:

### Approach 1: Log the result too

Single approval file with both logs and result.

```python
import logging
from approvaltests.utilities.logging import verify_logging

def test_with_logs():
    with verify_logging():
        result = load_data()
        logging.info(f"result = {result}")
```

### Approach 2: Separate approval files

```python
from approvaltests import verify
from approvaltests.utilities.logging import verify_logging
from approvaltests.namer import NamerFactory

def test_separate():
    with verify_logging(options=NamerFactory.with_parameters("logging")):
        result = load_data()
    verify(result)
```

Creates two files: `test_separate.logging.approved.txt` and `test_separate.approved.txt`

### Approach 3: Separate tests

Cleanest separation, but runs code twice.

```python
from approvaltests import verify
from approvaltests.utilities.logging import verify_logging

def test_logs_only():
    with verify_logging():
        load_data()

def test_result_only():
    verify(load_data())
```
