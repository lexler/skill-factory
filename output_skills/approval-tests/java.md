# Java ApprovalTests

## Installation

### Maven
```xml
<dependency>
    <groupId>com.approvaltests</groupId>
    <artifactId>approvaltests</artifactId>
    <version>24.9.0</version>
    <scope>test</scope>
</dependency>
```

### Gradle
```groovy
testImplementation 'com.approvaltests:approvaltests:24.9.0'
```

## Quick Start

```java
import org.approvaltests.Approvals;
import org.junit.jupiter.api.Test;

class ReportTest {
    @Test
    void generatesReport() {
        String result = generateReport();
        Approvals.verify(result);
    }
}
```

**First run:** Test fails, `.received` file created. Review it, approve it (copy to `.approved`), rerun.

## Common Imports

```java
import org.approvaltests.Approvals;
import org.approvaltests.JsonApprovals;
import org.approvaltests.combinations.CombinationApprovals;
import org.approvaltests.core.Options;
import org.approvaltests.scrubbers.DateScrubber;
```

## Core Patterns

### Approvals.verify() - Basic verification
```java
Approvals.verify(result);
Approvals.verify(object.toString());
```

### JsonApprovals.verifyAsJson() - Objects as formatted JSON
```java
JsonApprovals.verifyAsJson(user);
```

### Approvals.verifyAll() - Collections with labels
```java
Approvals.verifyAll("Users", users, u -> u.getName() + ": " + u.getEmail());
```

### Scrubbing
```java
Options options = new Options()
    .withScrubber(DateScrubber.getScrubberFor("00:00:00"));
Approvals.verify(result, options);
```

### Combinations
```java
CombinationApprovals.verifyAllCombinations(
    (size, color) -> createProduct(size, color),
    new String[]{"S", "M", "L"},
    new String[]{"red", "blue"}
);
```

## Java-Specific Notes

**@UseReporter annotation** - Set reporter at class level:
```java
@UseReporter(Junit5Reporter.class)
public class MyTest { }
```

**JUnit 5** - Recommended. Use `Junit5Reporter`.

**Lambda functions** - Java 8+ required for formatter lambdas.

## Git Setup

```gitignore
*.received.*
```

Commit all `.approved.*` files.

## Reference Files

- [api.md](references/java/api.md) - verifyXml/Html, CombinationApprovals, Verifiable interface, database results
- [scrubbers.md](references/java/scrubbers.md) - DateScrubber formats, GuidScrubber, RegExScrubber, combining scrubbers
- [setup.md](references/java/setup.md) - JUnit 4/5 setup, reporter selection, dynamic tests, Kotlin support
- [inline.md](references/java/inline.md) - Text blocks for inline approvals, InlineOptions modes
- [logging.md](references/java/logging.md) - ConsoleOutput for System.out/err verification
- [advanced.md](references/java/advanced.md) - NamerFactory, PackageSettings, OS/machine-specific tests
