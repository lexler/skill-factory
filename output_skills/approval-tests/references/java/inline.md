# Java Inline Approvals

Inline approvals store expected output directly in test code using Java text blocks (`"""`).

## Basic Usage

```java
import org.approvaltests.Approvals;
import org.approvaltests.core.Options;

@Test
void testGreeting() {
    var expected = """
        Hello World!
        Welcome to inline approvals!
        """;
    Approvals.verify(getGreeting(), new Options().inline(expected));
}
```

When the test fails, the framework automatically updates `expected` with the actual output.

## InlineOptions Modes

### Automatic Mode

Auto-approves and updates source code immediately:

```java
var expected = "";
Approvals.verify(actual, new Options().inline(expected, InlineOptions.automatic()));
```

### Semi-Automatic Mode

Adds a marker that must be manually deleted to approve:

```java
var expected = """
    actual output here
    ***** DELETE ME TO APPROVE *****
    """;
Approvals.verify(actual, new Options().inline(expected, InlineOptions.semiAutomatic()));
```

Delete the `***** DELETE ME TO APPROVE *****` line to approve.

### Semi-Automatic with Previous

Shows previous approved value for comparison:

```java
var expected = """
    new output
    vvvvv PREVIOUS RESULT vvvvv
    old output
    """;
Approvals.verify(actual, new Options().inline(expected,
    InlineOptions.semiAutomaticWithPreviousApproved()));
```

## With Code Display

Show source code context in diff:

```java
Approvals.verify(actual, new Options().inline(expected, InlineOptions.showCode(true)));
```

## Kotlin Support

Uses Kotlin string templates with `trimIndent()`:

```kotlin
@Test
fun `test greeting`() {
    val expected = """
        Hello World!
        Welcome to inline approvals!
        """.trimIndent()
    Approvals.verify(getGreeting(), Options().inline(expected))
}
```

## How It Works

1. Test fails → `InlineJavaReporter` activates
2. Reporter finds test method via stack trace
3. Parses source file and locates the `expected` variable
4. Replaces the text block content with actual output
5. Rewrites source file

## When to Use Inline vs File Approvals

**Use inline when:**
- Output is short (few lines)
- You want test and expectation in one place
- Quick iteration during TDD

**Use file approvals when:**
- Output is long or complex
- Multiple tests share similar output patterns
- Binary content (images, PDFs)
- JSON/XML that benefits from syntax highlighting
