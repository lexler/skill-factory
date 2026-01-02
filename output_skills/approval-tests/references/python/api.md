# Python ApprovalTests API

## Contents

- [Imports](#imports)
- [Core Functions](#core-functions)
- [Combination Testing](#combination-testing)
- [Options Class](#options-class)
- [Storyboard](#storyboard)
- [MarkdownTable](#markdowntable)
- [Command Line Testing](#command-line-testing)
- [Logging Verification](#logging-verification)

## Imports

```python
from approvaltests import (
    verify,
    verify_all,
    verify_as_json,
    verify_xml,
    verify_html,
    verify_file,
    verify_exception,
    verify_binary,
    verify_argument_parser,
    verify_all_combinations,
    verify_all_combinations_with_labeled_input,
    verify_best_covering_pairs,
    Options,
)
```

## Core Functions

### verify()
Basic string verification.
```python
verify("Hello World")
verify(formatted_output, options=Options().with_scrubber(scrub_dates))
```

### verify_as_json()
Object to pretty-printed JSON. Preferred for objects.
```python
verify_as_json(user)
verify_as_json({"users": users, "count": len(users)})
```

### verify_all()
Collection with header label.
```python
verify_all("Users", users)
verify_all("Prices", items, lambda x: f"{x.name}: ${x.price}")
```

### verify_xml() / verify_html()
Pretty-print and verify. HTML requires `beautifulsoup4`.
```python
verify_xml(xml_string)
verify_html(html_string)
```

### verify_file()
Verify contents of existing file.
```python
verify_file("output/report.txt")
```

### verify_exception()
Verify exception message.
```python
verify_exception(lambda: divide(1, 0))
```

### verify_binary()
Binary data (images, PDFs).
```python
verify_binary(image_bytes, ".png")
```

### verify_argument_parser()
Verify argparse help output.
```python
from approvaltests import verify_argument_parser
verify_argument_parser(parser)
```

## Combination Testing

See [combinations.md](combinations.md) for full patterns.

- `verify_all_combinations(fn, [[vals1], [vals2]])` - Test all input combinations
- `verify_all_combinations_with_labeled_input(fn, param1=[...], param2=[...])` - Clearer output (recommended)
- `verify_best_covering_pairs(fn, [[...], [...]])` - Pairwise testing, requires `allpairspy`

## Options Class

Fluent configuration builder. All methods return new Options instance.

```python
options = (Options()
    .with_reporter(reporter)
    .with_scrubber(my_scrubber)
    .for_file.with_extension(".json"))

verify(data, options=options)
```

### Methods

- `with_reporter(reporter)` - Set failure reporter
- `with_scrubber(fn)` - Set scrubber function
- `add_scrubber(fn)` - Chain additional scrubber
- `with_namer(namer)` - Custom file naming
- `with_comparator(cmp)` - Custom comparison logic
- `for_file.with_extension(".ext")` - Set file extension
- `inline(inline_options)` - Enable inline approvals

## Storyboard

State progression over time. Use for state machines, multi-step workflows.

```python
from approvaltests.storyboard import Storyboard

story = Storyboard()
story.add_frame(initial_state)
story.add_frame(after_action, title="After click")
verify(story)
```

Or: `with verify_storyboard() as story: story.add_frame(state)`

## MarkdownTable

Multiple inputs against multiple functions:

```python
from approvaltests.utilities.markdown_table import MarkdownTable

inputs = ["hello", "world"]
table = MarkdownTable.with_headers("Input", "Upper", "Lower")
table.add_rows_for_inputs(inputs, str.upper, str.lower)
verify(table)
```

## Command Line Testing

```python
from approvaltests.utilities.command_line_approvals import verify_command_line
verify_command_line("python --version")
```

## Logging Verification

```python
from approvaltests.utilities.logging import verify_logging

with verify_logging():
    logging.info("Something happened")
```
