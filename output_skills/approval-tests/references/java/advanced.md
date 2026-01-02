# Java Advanced Patterns

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
