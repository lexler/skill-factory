# Java ApprovalTests

## Installation

Look up latest version at https://mvnrepository.com/artifact/com.approvaltests/approvaltests

### Maven
```xml
<dependency>
    <groupId>com.approvaltests</groupId>
    <artifactId>approvaltests</artifactId>
    <version>VERSION</version>
    <scope>test</scope>
</dependency>
```

### Gradle
```groovy
testImplementation 'com.approvaltests:approvaltests:VERSION'
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

`@UseReporter` annotation sets reporter at class level:
```java
@UseReporter(Junit5Reporter.class)
public class MyTest { }
```

JUnit 5 recommended. Use `Junit5Reporter`.

Java 8+ required for formatter lambdas.

## Git Setup

```gitignore
*.received.*
```

Commit all `.approved.*` files.

## Quick Decision Guide

- Objects → `JsonApprovals.verifyAsJson(obj)`
- Arrays/lists (structured) → `JsonApprovals.verifyAsJson(items)`
- Arrays/lists (labeled) → `Approvals.verifyAll("Items", items, formatter)`
- Non-deterministic data → scrubbers, add before first run ([scrubbers.md](references/java/scrubbers.md))
- Multiple scenarios per test → `NamerFactory.withParameters()` ([advanced.md](references/java/advanced.md))
- Input combinations → `CombinationApprovals.verifyAllCombinations()` (or `verifyBestCoveringPairs` for huge sets) ([api.md](references/java/api.md))
- State progressions → `StoryBoard` ([api.md](references/java/api.md))
- Console output → `ConsoleOutput` ([logging.md](references/java/logging.md))
- Short inline expectations → `Options().inline(expected)` ([inline.md](references/java/inline.md))

## Reference Files

- [api.md](references/java/api.md) - verifyXml/Html, CombinationApprovals, StoryBoard, Verifiable interface, database results
- [scrubbers.md](references/java/scrubbers.md) - DateScrubber formats, GuidScrubber, RegExScrubber, combining scrubbers
- [reporters.md](references/java/reporters.md) - IDE/diff tool reporters, FirstWorkingReporter, custom reporters
- [setup.md](references/java/setup.md) - JUnit 4/5 setup, dynamic tests, Kotlin support
- [inline.md](references/java/inline.md) - Text blocks for inline approvals, InlineOptions modes
- [logging.md](references/java/logging.md) - ConsoleOutput for System.out/err verification
- [advanced.md](references/java/advanced.md) - NamerFactory, PackageSettings, OS/machine-specific tests, common mistakes
