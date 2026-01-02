# Python ApprovalTests API

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
    verify_all_combinations,
    verify_all_combinations_with_labeled_input,
    verify_best_covering_pairs,
    Options,
)
```

## Core Functions

### verify()
```python
def verify(
    data: Any,
    *,
    options: Optional[Options] = None,
) -> None
```
Basic verification. Converts data to string and compares to approved file.

```python
verify("Hello World")
verify(str(my_object))
verify(formatted_output, options=Options().with_scrubber(scrub_dates))
```

### verify_as_json()
```python
def verify_as_json(
    object_to_verify: Any,
    *,
    deserialize_json_fields: bool = False,
    options: Optional[Options] = None,
) -> None
```
Serialize object to pretty-printed JSON.

```python
verify_as_json(user)
verify_as_json({"users": users, "count": len(users)})
```

### verify_all()
```python
def verify_all(
    header: str,
    alist: Iterable[Any],
    formatter: Optional[Callable] = None,
    *,
    options: Optional[Options] = None,
) -> None
```
Verify a collection with a header label.

```python
verify_all("Users", users)
verify_all("Prices", items, lambda x: f"{x.name}: ${x.price}")
```

### verify_xml()
```python
def verify_xml(
    xml_string: str,
    *,
    options: Optional[Options] = None,
) -> None
```
Pretty-print and verify XML.

### verify_html()
```python
def verify_html(
    html_string: str,
    *,
    options: Optional[Options] = None,
) -> None
```
Pretty-print and verify HTML. Requires `beautifulsoup4`.

### verify_file()
```python
def verify_file(
    file_name: str,
    *,
    options: Optional[Options] = None,
) -> None
```
Verify contents of an existing file.

### verify_exception()
```python
def verify_exception(
    code_that_throws_exception: Callable,
    *,
    options: Optional[Options] = None,
) -> None
```
Verify exception message.

```python
verify_exception(lambda: divide(1, 0))
```

### verify_binary()
```python
def verify_binary(
    data: Union[bytes, bytearray, memoryview],
    file_extension_with_dot: str,
    *,
    options: Optional[Options] = None,
) -> None
```
Verify binary data (images, PDFs, etc).

```python
verify_binary(image_bytes, ".png")
```

## Combination Testing

### verify_all_combinations()
```python
def verify_all_combinations(
    function_under_test: Callable,
    input_arguments: Sequence[Sequence[Any]],
    *,
    options: Optional[Options] = None,
) -> None
```
Test all combinations of inputs.

```python
verify_all_combinations(
    calculate_price,
    [
        ["small", "medium", "large"],  # sizes
        [1, 5, 10],                     # quantities
    ]
)
# Tests: calculate_price("small", 1), calculate_price("small", 5), ...
```

### verify_all_combinations_with_labeled_input()
```python
def verify_all_combinations_with_labeled_input(
    function_under_test: Callable,
    *,
    options: Optional[Options] = None,
    **kwargs: Any,
) -> None
```
Combinations with named parameters (clearer output).

```python
verify_all_combinations_with_labeled_input(
    calculate_price,
    size=["small", "medium", "large"],
    quantity=[1, 5, 10],
)
```

### verify_best_covering_pairs()
Same signature as `verify_all_combinations()` but uses pairwise testing for fewer combinations.

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

Capture object state progression over time. Output stacks frames vertically like comic book panels—easy to diff.

Use for: state machines, multi-step workflows, animations, before/after comparisons.

```python
from approvaltests.storyboard import Storyboard

story = Storyboard()
story.add_description("Testing user registration flow")
story.add_frame(initial_state)
story.add_frame(after_action, title="After click")
story.add_frame(final_state, title="Final")
verify(story)
```

Methods:
- `add_frame(obj, title=None)` - Capture a state snapshot
- `add_description(text)` - Add context/labels between frames

Or with context manager:

```python
from approvaltests import verify_storyboard

with verify_storyboard() as story:
    story.add_frame(state1)
    story.add_frame(state2)
```

## MarkdownTable

Test multiple inputs against multiple functions in one approval:

```python
from approvaltests.utilities.markdown_table import MarkdownTable

inputs = ["hello world", "foo_bar", "CamelCase"]
table = MarkdownTable.with_headers("Input", "Upper", "Lower", "Title")
table.add_rows_for_inputs(inputs, str.upper, str.lower, str.title)
verify(table)
```

Output:
```
| Input       | Upper       | Lower       | Title       |
| ----------- | ----------- | ----------- | ----------- |
| hello world | HELLO WORLD | hello world | Hello World |
| foo_bar     | FOO_BAR     | foo_bar     | Foo_Bar     |
| CamelCase   | CAMELCASE   | camelcase   | Camelcase   |
```

## Command Line Testing

```python
from approvaltests.utilities.command_line_approvals import verify_command_line

verify_command_line("python --version")
verify_command_line("echo hello", input_string="test input")
```

## Logging Verification

```python
from approvaltests.utilities.logging import verify_logging

with verify_logging():
    logging.info("Something happened")
    logging.warning("Watch out")
```
