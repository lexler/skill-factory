# Java Advanced Patterns

## Contents

- [Multiple Approvals Per Test](#multiple-approvals-per-test)
- [Configuration](#configuration)
- [Custom File Extensions](#custom-file-extensions)
- [Additional Info in Filename](#additional-info-in-filename)
- [Machine-Specific Tests](#machine-specific-tests)
- [Common Mistakes](#common-mistakes)

For inline approvals, see [inline.md](inline.md).
For console output capture, see [logging.md](logging.md).

## Multiple Approvals Per Test

By default, one `Approvals.verify()` call per test. For multiple approvals, use `NamerFactory`.

### Parametrized Tests (JUnit 5)

```java
import org.approvaltests.Approvals;
import org.approvaltests.namer.NamerFactory;
import org.approvaltests.namer.NamedEnvironment;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvSource;

class LeapYearTest {
    @ParameterizedTest
    @CsvSource({"Oskar,4", "Birgit,1"})
    void testWithParameters(String name, int age) {
        try (NamedEnvironment en = NamerFactory.withParameters(name, age)) {
            String output = name + ":" + age;
            Approvals.verify(output);
        }
    }
}
```

Creates separate files: `testWithParameters.Oskar.4.approved.txt`, `testWithParameters.Birgit.1.approved.txt`

### Multiple Verifies in One Test

#### Using NamerFactory.useMultipleFiles()

```java
import org.approvaltests.Approvals;
import org.approvaltests.namer.NamerFactory;
import org.approvaltests.namer.MultipleFilesLabeller;

@Test
void testMultipleFiles() {
    try (MultipleFilesLabeller labeller = NamerFactory.useMultipleFiles()) {
        Approvals.verify("one");
        labeller.next();
        Approvals.verify("two");
    }
}
```

Creates: `testMultipleFiles.1.approved.txt`, `testMultipleFiles.2.approved.txt`

#### Using Options-Based Approach

```java
import org.approvaltests.Approvals;
import org.approvaltests.namer.FileCounter;

@Test
void testMultipleFilesViaOptions() {
    FileCounter labeller = Approvals.NAMES.useMultipleFiles();
    Approvals.verify("one", labeller.next());
    Approvals.verify("two", labeller.next());
}
```

## Configuration

### PackageSettings

Create a `PackageSettings.java` class in your test package to configure defaults:

```java
package org.myapp.tests;

import org.approvaltests.reporters.UseReporter;
import org.approvaltests.reporters.intellij.IntelliJReporter;

@UseReporter(IntelliJReporter.class)
public class PackageSettings {
    // Reporter applies to all tests in this package and subpackages
}
```

### Approval Subdirectory

Store approval files in a subdirectory instead of alongside tests:

```java
package org.myapp.tests;

public class PackageSettings {
    public static String UseApprovalSubdirectory = "approvals";
}
```

Creates files in `tests/approvals/` instead of `tests/`.

### Base Directory

Specify a different base directory for approval files:

```java
public class PackageSettings {
    public static String ApprovalBaseDirectory = "../resources/approvals";
}
```

## Custom File Extensions

```java
Options options = new Options()
    .forFile()
    .withExtension(".html");
Approvals.verify(htmlContent, options);
```

```java
Options options = new Options()
    .forFile()
    .withExtension(".json");
JsonApprovals.verifyAsJson(data, options);
```

## Additional Info in Filename

```java
Options options = new Options()
    .forFile()
    .withAdditionalInformation("scenario1");
Approvals.verify(result, options);
```

Creates: `TestClass.testMethod.scenario1.approved.txt`

## Machine-Specific Tests

For tests that produce different output on different machines:

```java
import org.approvaltests.namer.NamerFactory;

@Test
void testMachineSpecific() {
    try (var env = NamerFactory.asMachineNameSpecificTest()) {
        Approvals.verify(getSystemInfo());
    }
}
```

Creates: `testMachineSpecific.MACHINENAME.approved.txt`

### OS-Specific Tests

```java
@Test
void testOsSpecific() {
    try (var env = NamerFactory.asOsSpecificTest()) {
        Approvals.verify(getPathSeparator());
    }
}
```

Creates: `testOsSpecific.Mac.approved.txt` or `testOsSpecific.Windows.approved.txt`

## Common Mistakes

### Multiple verify() calls without NamerFactory

Each `Approvals.verify()` overwrites the same file. Only the last one is tested.

```java
// Broken - only tests result2
@Test
void testBoth() {
    Approvals.verify(result1);
    Approvals.verify(result2);
}

// Fixed - separate files
@Test
void testBoth() {
    try (MultipleFilesLabeller labeller = NamerFactory.useMultipleFiles()) {
        Approvals.verify(result1);
        labeller.next();
        Approvals.verify(result2);
    }
}
```

### Hand-editing .approved files

Breaks the contract. The approved file should only be created by running the test and approving the received output.

If the output is wrong, fix the code and regenerate.

### Over-approving

Approving an entire entity when you only care about a few fields. Large approvals hide real changes in noise.

```java
// Not this - approves 50 fields when you care about 3
JsonApprovals.verifyAsJson(fullUserRecord);

// This - approve only what matters
JsonApprovals.verifyAsJson(Map.of(
    "name", user.getName(),
    "email", user.getEmail(),
    "status", user.getStatus()
));
```

### Under-scrubbing

Tests pass locally, fail in CI.

If it varies by environment, scrub it: timestamps, UUIDs, file paths, hostnames, process IDs.

### Mixing approvals with assertions

The approval captures everything. If you're adding assertions alongside `verify()`, you're probably testing two things.

```java
// Not this
@Test
void testUser() {
    User user = createUser();
    assertThat(user.getId()).isGreaterThan(0);
    JsonApprovals.verifyAsJson(user);
}

// This - the approval captures everything including id
@Test
void testUser() {
    JsonApprovals.verifyAsJson(createUser());
}
```
