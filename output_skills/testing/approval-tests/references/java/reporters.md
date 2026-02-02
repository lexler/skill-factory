# Java Reporters

Reporters handle what happens when an approval fails - showing diffs, opening diff tools, or custom actions.

## Contents

- [Using Reporters](#using-reporters)
- [Available Reporters](#available-reporters)
- [FirstWorkingReporter](#firstworkingreporter)
- [Custom Reporter](#custom-reporter)
- [PackageSettings](#packagesettings)

## Using Reporters

### Via Annotation (class-level)

```java
import org.approvaltests.reporters.UseReporter;
import org.approvaltests.reporters.intellij.IntelliJReporter;

@UseReporter(IntelliJReporter.class)
public class MyTest {
    @Test
    void testSomething() {
        Approvals.verify(result);
    }
}
```

### Via Options (per-test)

```java
Approvals.verify(result, new Options().withReporter(new Junit5Reporter()));
```

## Available Reporters

### IDE Reporters

```java
@UseReporter(IntelliJReporter.class)
@UseReporter(EclipseReporter.class)
@UseReporter(VsCodeReporter.class)
```

### Diff Tool Reporters

```java
@UseReporter(BeyondCompare4Reporter.class)     // Windows/Mac
@UseReporter(KaleidoscopeDiffReporter.class)   // Mac
@UseReporter(MeldMergeReporter.class)          // Linux
@UseReporter(TortoiseDiffReporter.class)       // Windows
@UseReporter(P4MergeReporter.class)            // Cross-platform
@UseReporter(KDiff3Reporter.class)             // Cross-platform
```

### JUnit Reporters

```java
@UseReporter(Junit4Reporter.class)
@UseReporter(Junit5Reporter.class)
```

### CI/Utility Reporters

```java
@UseReporter(QuietReporter.class)        // Silent fail, no diff output
@UseReporter(ClipboardReporter.class)    // Copies approve command to clipboard
@UseReporter(AutoApproveReporter.class)  // Auto-approves (use with caution)
@UseReporter(DiffReporter.class)         // System default diff tool
```

## FirstWorkingReporter

Try reporters in order until one works:

```java
import org.approvaltests.reporters.FirstWorkingReporter;

@UseReporter(FirstWorkingReporter.class)
public class MyTest {
    // Tries reporters in order: IntelliJ → VS Code → Beyond Compare → Clipboard
}
```

Custom chain via Options:

```java
Reporter chain = new FirstWorkingReporter(
    new IntelliJReporter(),
    new VsCodeReporter(),
    new ClipboardReporter()
);
Approvals.verify(result, new Options().withReporter(chain));
```

## Custom Reporter

Implement the `Reporter` interface:

```java
import org.approvaltests.core.ApprovalFailureReporter;

public class MyReporter implements ApprovalFailureReporter {
    @Override
    public boolean report(String received, String approved) {
        System.out.println("Mismatch:");
        System.out.println("  Received: " + received);
        System.out.println("  Approved: " + approved);
        return true;  // true = reporter handled it
    }
}

// Usage
@UseReporter(MyReporter.class)
public class MyTest { }
```

## PackageSettings

Set default reporter for all tests in a package:

```java
package org.myapp.tests;

import org.approvaltests.reporters.UseReporter;
import org.approvaltests.reporters.intellij.IntelliJReporter;

@UseReporter(IntelliJReporter.class)
public class PackageSettings {
    // Applies to all tests in this package and subpackages
}
```

For package-wide configuration details, see [advanced.md](advanced.md).
