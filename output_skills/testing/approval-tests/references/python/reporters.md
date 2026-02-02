# Python Reporters

Reporters handle what happens when an approval fails - showing diffs, opening diff tools, or custom actions.

## Contents

- [Using Factory](#using-factory)
- [Custom Diff Tool](#custom-diff-tool)
- [Custom Reporter Class](#custom-reporter-class)
- [Chaining Reporters](#chaining-reporters)

## Using Factory

```python
from approvaltests import verify, Options
from approvaltests.reporters import GenericDiffReporterFactory

factory = GenericDiffReporterFactory()
reporter = factory.get("BeyondCompare")
verify("Hello", options=Options().with_reporter(reporter))
```

Available reporters include: BeyondCompare, DiffMerge, KDiff3, Meld, P4Merge, TkDiff, VSCode, IntelliJ.

## Custom Diff Tool

```python
from approvaltests import verify, Options
from approvaltests.reporters import GenericDiffReporter

reporter = GenericDiffReporter.create("/path/to/diff/tool")
verify("Hello", options=Options().with_reporter(reporter))
```

## Custom Reporter Class

```python
from approvaltests import verify, Options
from approvaltests.core.reporter import Reporter

class MyReporter(Reporter):
    def report(self, received_path: str, approved_path: str) -> bool:
        print(f"Mismatch: {received_path} vs {approved_path}")
        return True

verify(result, options=Options().with_reporter(MyReporter()))
```

The `report` method receives paths to both files. Return `True` if the reporter handled the failure.

## Chaining Reporters

Use `FirstWorkingReporter` to try multiple reporters in order:

```python
from approvaltests import verify, Options
from approvaltests.reporters import FirstWorkingReporter, GenericDiffReporterFactory
from approvaltests.reporters import PythonNativeReporter

factory = GenericDiffReporterFactory()
reporter = FirstWorkingReporter(
    factory.get("VSCode"),
    factory.get("IntelliJ"),
    PythonNativeReporter(),
)
verify("Hello", options=Options().with_reporter(reporter))
```

Falls back through the list until one works.
