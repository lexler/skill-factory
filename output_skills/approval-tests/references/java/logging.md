# Java Console Output Verification

Capture and verify console output and error streams.

## ConsoleOutput

### Basic Usage

```java
import org.approvaltests.utils.ConsoleOutput;
import org.junit.jupiter.api.Test;

@Test
void testConsoleOutput() {
    try (ConsoleOutput console = new ConsoleOutput()) {
        System.out.println("Hello, World!");
        System.out.println("Processing complete");
        console.verifyOutput();
    }
}
```

ConsoleOutput captures everything written to `System.out` and `System.err` within the try-with-resources block.

### Verify Standard Output

```java
@Test
void testStdOut() {
    try (ConsoleOutput console = new ConsoleOutput()) {
        runProcessThatPrints();
        console.verifyOutput();
    }
}
```

### Verify Error Output

```java
@Test
void testStdErr() {
    try (ConsoleOutput console = new ConsoleOutput()) {
        runProcessThatLogsErrors();
        console.verifyError();
    }
}
```

### Verify Both Streams

```java
@Test
void testBothStreams() {
    try (ConsoleOutput console = new ConsoleOutput()) {
        System.out.println("Standard output");
        System.err.println("Error output");
        console.verifyAll();
    }
}
```

Output format:
```
Output:
Standard output

Error:
Error output
```

## With Options

### Scrubbing Console Output

```java
@Test
void testWithScrubbing() {
    try (ConsoleOutput console = new ConsoleOutput()) {
        System.out.println("Process started at 10:30:00");
        System.out.println("Completed successfully");

        Options options = new Options()
            .withScrubber(DateScrubber.getScrubberFor("00:00:00"));
        console.verifyOutput(options);
    }
}
```

### Inline Approvals

```java
@Test
void testInlineConsole() {
    var expected = """
        Hello, World!
        Processing complete
        """;
    try (ConsoleOutput console = new ConsoleOutput()) {
        System.out.println("Hello, World!");
        System.out.println("Processing complete");
        console.verifyOutput(new Options().inline(expected));
    }
}
```

## Getting Raw Output

For custom processing before verification:

```java
@Test
void testRawAccess() {
    try (ConsoleOutput console = new ConsoleOutput()) {
        runProcess();

        String output = console.getOutput();
        String errors = console.getError();

        // Custom processing
        String filtered = filterNoise(output);
        Approvals.verify(filtered);
    }
}
```

## Common Patterns

### Testing CLI Output

```java
@Test
void testCliApplication() {
    try (ConsoleOutput console = new ConsoleOutput()) {
        MyCliApp.main(new String[]{"--help"});
        console.verifyOutput();
    }
}
```

### Testing Logging Libraries

When your code uses `System.out` or `System.err` directly:

```java
@Test
void testLegacyLogging() {
    try (ConsoleOutput console = new ConsoleOutput()) {
        LegacyService service = new LegacyService();
        service.processWithLogging(data);
        console.verifyAll();
    }
}
```

### Combining with Return Value

```java
@Test
void testOutputAndResult() {
    String result;
    try (ConsoleOutput console = new ConsoleOutput()) {
        result = process();
        console.verifyOutput(new Options()
            .forFile()
            .withAdditionalInformation("console"));
    }
    Approvals.verify(result);
}
```

Creates two files: `test.console.approved.txt` and `test.approved.txt`
