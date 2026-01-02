# Java ApprovalTests Setup

## Contents

- [Maven](#maven)
- [Gradle](#gradle)
- [JUnit 5 Setup](#junit-5-setup)
- [JUnit 4 Setup](#junit-4-setup)
- [Dynamic Tests (JUnit 5)](#dynamic-tests-junit-5)
- [Git Configuration](#git-configuration)
- [Reporter Selection](#reporter-selection)
- [Options Configuration](#options-configuration)
- [File Naming](#file-naming)
- [Kotlin Support](#kotlin-support)

For full reporter list, see [reporters.md](reporters.md). For Options methods, see [api.md](api.md).

## Maven

```xml
<dependency>
    <groupId>com.approvaltests</groupId>
    <artifactId>approvaltests</artifactId>
    <version>VERSION</version>
    <scope>test</scope>
</dependency>
```

Look up latest version at https://mvnrepository.com/artifact/com.approvaltests/approvaltests

## Gradle

```groovy
testImplementation 'com.approvaltests:approvaltests:VERSION'
```

## JUnit 5 Setup

```java
import org.approvaltests.Approvals;
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

See [reporters.md](reporters.md) for full reporter reference including custom reporters and chaining.

Quick examples:

```java
// IDE
@UseReporter(IntelliJReporter.class)
@UseReporter(VsCodeReporter.class)

// CI
@UseReporter(QuietReporter.class)
@UseReporter(ClipboardReporter.class)
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
