# Java ApprovalTests Setup

## Maven

```xml
<dependency>
    <groupId>com.approvaltests</groupId>
    <artifactId>approvaltests</artifactId>
    <version>24.3.0</version>
    <scope>test</scope>
</dependency>
```

## Gradle

```groovy
testImplementation 'com.approvaltests:approvaltests:24.3.0'
```

## JUnit 5 Setup

```java
import org.approvaltests.Approvals;
import org.approvaltests.core.Options;
import org.approvaltests.reporters.UseReporter;
import org.approvaltests.reporters.intellij.IntelliJReporter;
import org.junit.jupiter.api.Test;

class MyTest {
    @Test
    void testOutput() {
        String result = generateOutput();
        Approvals.verify(result);
    }
}
```

### With Reporter Annotation

```java
@UseReporter(IntelliJReporter.class)
class MyTest {
    @Test
    void testOutput() {
        Approvals.verify(result);
    }
}
```

## JUnit 4 Setup

```java
import org.approvaltests.Approvals;
import org.junit.Test;

public class MyTest {
    @Test
    public void testOutput() {
        String result = generateOutput();
        Approvals.verify(result);
    }
}
```

## Dynamic Tests (JUnit 5)

```java
import org.approvaltests.integrations.junit5.JupiterApprovals;
import org.junit.jupiter.api.DynamicTest;
import org.junit.jupiter.api.TestFactory;
import java.util.stream.Stream;

class DynamicTestExample {
    @TestFactory
    Stream<DynamicTest> dynamicTests() {
        return Stream.of("hello", "world")
            .map(input -> JupiterApprovals.dynamicTest(
                "test_" + input,
                options -> Approvals.verify(process(input), options)
            ));
    }
}
```

## Git Configuration

Add to `.gitignore`:
```
*.received.*
```

Add to `.gitattributes`:
```
*.approved.* binary
```

The `binary` attribute prevents line ending changes.

## Reporter Selection

### IDE Reporters

```java
// IntelliJ
@UseReporter(IntelliJReporter.class)

// Eclipse
@UseReporter(EclipseReporter.class)

// VS Code
@UseReporter(VsCodeReporter.class)
```

### Diff Tool Reporters

```java
@UseReporter(BeyondCompare4Reporter.class)  // Windows/Mac
@UseReporter(KaleidoscopeDiffReporter.class) // Mac
@UseReporter(MeldMergeReporter.class)        // Linux
```

### CI Reporters

```java
@UseReporter(QuietReporter.class)     // Just fails, no output
@UseReporter(ClipboardReporter.class) // Copies approve command
```

## Options Configuration

```java
@Test
void testWithOptions() {
    Options options = new Options()
        .withReporter(new Junit5Reporter())
        .forFile().withExtension(".json");

    Approvals.verify(result, options);
}
```

## File Naming

Default: `ClassName.methodName.approved.txt`

Custom naming:

```java
Options options = new Options()
    .forFile()
    .withBaseName("custom_name")
    .withAdditionalInformation("scenario1");
// Creates: custom_name.scenario1.approved.txt
```

## Kotlin Support

```kotlin
import org.approvaltests.Approvals
import org.approvaltests.core.Options
import org.junit.jupiter.api.Test

class MyTest {
    @Test
    fun `test output`() {
        val result = generateOutput()
        Approvals.verify(result)
    }
}
```
