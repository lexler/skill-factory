# Java ApprovalTests API

## Contents

- [Imports](#imports)
- [Core Methods](#core-methods)
- [JsonApprovals](#jsonapprovals)
- [CombinationApprovals](#combinationapprovals)
- [Options Class](#options-class)
- [Reporters](#reporters)
- [Verifiable Interface](#verifiable-interface)
- [File Operations](#file-operations)
- [Database Results](#database-results)

For scrubbers, see [scrubbers.md](scrubbers.md).
For multiple approvals per test, see [advanced.md](advanced.md).
For console output verification, see [logging.md](logging.md).

## Imports

```java
import org.approvaltests.Approvals;
import org.approvaltests.core.Options;
import org.approvaltests.JsonApprovals;
import org.approvaltests.combinations.CombinationApprovals;
```

## Core Methods

### Approvals.verify()

```java
Approvals.verify(String response)
Approvals.verify(String response, Options options)
Approvals.verify(Object object)
Approvals.verify(Object object, Options options)
```

```java
Approvals.verify("Hello World");
Approvals.verify(myObject.toString());
```

### Approvals.verifyAll()

```java
Approvals.verifyAll(String label, T[] array)
Approvals.verifyAll(T[] values, Function1<T, String> formatter)
Approvals.verifyAll(String header, T[] values, Function1<T, String> formatter)
```

```java
String[] names = {"Alice", "Bob", "Charlie"};
Approvals.verifyAll("names", names);

Approvals.verifyAll("users", users, u -> u.getName() + ": " + u.getEmail());
```

### XML/HTML Verification

```java
Approvals.verifyXml(String xml)
Approvals.verifyXml(String xml, Options options)
Approvals.verifyHtml(String html)
Approvals.verifyHtml(String html, Options options)
```

### Exception Verification

```java
Approvals.verifyException(() -> {
    throw new RuntimeException("Expected error");
});
```

## JsonApprovals

```java
JsonApprovals.verifyJson(String json)
JsonApprovals.verifyAsJson(Object object)
JsonApprovals.verifyAsJson(Object object, Options options)
```

```java
User user = new User("Alice", 30);
JsonApprovals.verifyAsJson(user);
```

## CombinationApprovals

Test all combinations of inputs:

```java
CombinationApprovals.verifyAllCombinations(
    (size, color) -> createProduct(size, color),
    new String[]{"S", "M", "L"},
    new String[]{"red", "blue"}
);
```

Pairwise testing (fewer combinations):

```java
CombinationApprovals.verifyBestCoveringPairs(
    (a, b, c) -> process(a, b, c),
    params1, params2, params3
);
```

Skip invalid combinations:

```java
CombinationApprovals.verifyAllCombinations(
    (a, b) -> {
        if (invalidCombo(a, b)) throw new SkipCombination();
        return process(a, b);
    },
    params1, params2
);
```

## Options Class

```java
Options options = new Options()
    .withReporter(new Junit5Reporter())
    .withScrubber(DateScrubber.getScrubberFor("00:00:00"))
    .forFile().withExtension(".json");

Approvals.verify(result, options);
```

### Methods

- `withReporter(reporter)` - Set failure reporter
- `withScrubber(scrubber)` - Set scrubber function
- `inline(expected)` - Use inline approvals
- `forFile().withExtension(".ext")` - Set file extension
- `forFile().withBaseName(name)` - Custom base filename
- `forFile().withAdditionalInformation(info)` - Add info to filename

## Reporters

See [reporters.md](reporters.md) for full reporter reference.

Common reporters: `Junit5Reporter`, `IntelliJReporter`, `QuietReporter`, `ClipboardReporter`

```java
// Via annotation
@UseReporter(Junit5Reporter.class)
public class MyTest { }

// Via Options
Approvals.verify(result, new Options().withReporter(new Junit5Reporter()));
```

## Verifiable Interface

For custom objects:

```java
public class MyClass implements Verifiable {
    @Override
    public VerifyParameters getVerifyParameters(Options options) {
        return new VerifyParameters(
            options.createWriter(this.toString()),
            options.forFile().getNamer(),
            options.getReporter()
        );
    }
}

// Then just:
Approvals.verify(myObject);
```

## File Operations

```java
Approvals.verifyEachFileInDirectory(new File("output/"));
Approvals.verifyEachFileInDirectory(directory, file -> file.getName().endsWith(".json"));
```

## Database Results

```java
ResultSet rs = statement.executeQuery("SELECT * FROM users");
Approvals.verify(rs);
```
