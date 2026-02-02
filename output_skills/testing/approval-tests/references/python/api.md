# Python ApprovalTests API

## Contents

- [Core Verify Functions](#core-verify-functions)
- [Options Class](#options-class)
- [Storyboard](#storyboard)
- [MarkdownTable](#markdowntable)
- [Command Line](#command-line)

For combination testing, see [combinations.md](combinations.md).
For scrubbers, see [scrubbers.md](scrubbers.md).
For logging verification, see [logging.md](logging.md).

## Core Verify Functions

```python
from approvaltests import (
    verify,
    verify_as_json,
    verify_all,
    verify_xml,
    verify_html,
    verify_file,
    verify_exception,
    verify_binary,
)
```

### verify()

Basic string verification.

```python
from approvaltests import verify

verify("Hello World")
```

### verify_as_json()

Object to pretty-printed JSON. Preferred for structured data.

```python
from approvaltests import verify_as_json

verify_as_json(user)
verify_as_json({"users": users, "count": len(users)})
```

### verify_all()

Collection with header label and optional formatter.

```python
from approvaltests import verify_all

verify_all("Users", users)
verify_all("Prices", items, lambda x: f"{x.name}: ${x.price}")
```

### verify_xml()

Pretty-prints XML before verification.

```python
from approvaltests import verify_xml

verify_xml(xml_string)
```

### verify_html()

Pretty-prints HTML before verification. Requires `beautifulsoup4`.

```python
from approvaltests import verify_html

verify_html(html_string)
```

### verify_file()

Verify contents of an existing file.

```python
from approvaltests import verify_file

verify_file("output/report.txt")
```

### verify_exception()

Verify exception message.

```python
from approvaltests import verify_exception

verify_exception(lambda: divide(1, 0))
```

### verify_binary()

Binary data (images, PDFs). Second argument is file extension.

```python
from approvaltests import verify_binary

verify_binary(image_bytes, ".png")
```

## Options Class

Fluent configuration. All methods return new Options instance.

```python
from approvaltests import verify, Options

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
- `for_file.with_additional_information("suffix")` - Add suffix to filename
- `inline()` - Enable inline approvals (see [inline.md](inline.md))

## Storyboard

Captures state progression over multiple frames. Use for state machines, animations, multi-step workflows.

```python
from approvaltests import verify
from approvaltests.storyboard import Storyboard

story = Storyboard()
story.add_description("Testing game state transitions")
story.add_frame(game.get_state())
game.move("north")
story.add_frame(game.get_state(), title="After moving north")
game.pick_up("sword")
story.add_frame(game.get_state(), title="After picking up sword")
verify(story)
```

Output stacks frames vertically:

```
Testing game state transitions

Initial Frame:
room: entrance
inventory: []

After moving north:
room: hallway
inventory: []

After picking up sword:
room: hallway
inventory: [sword]
```

Context manager form:

```python
from approvaltests import verify_storyboard

with verify_storyboard() as story:
    story.add_frame(state1)
    do_something()
    story.add_frame(state2)
```

## MarkdownTable

Test multiple inputs against multiple functions in a grid.

```python
from approvaltests import verify
from approvaltests.utilities.markdown_table import MarkdownTable

inputs = ["hello", "WORLD", "MiXeD"]
table = MarkdownTable.with_headers("Input", "upper()", "lower()", "len()")
table.add_rows_for_inputs(inputs, str.upper, str.lower, len)
verify(table)
```

Output:

```
| Input | upper() | lower() | len() |
| ----- | ------- | ------- | ----- |
| hello | HELLO   | hello   | 5     |
| WORLD | WORLD   | world   | 5     |
| MiXeD | MIXED   | mixed   | 5     |
```

## Command Line

Test CLI output:

```python
from approvaltests.utilities.command_line_approvals import verify_command_line

verify_command_line("python --version")
```

Test argparse help:

```python
from approvaltests import verify_argument_parser

verify_argument_parser(parser)
```
