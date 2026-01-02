# Java Scrubbers

Scrubbers normalize dynamic data before comparison.

## Imports

```java
import org.approvaltests.scrubbers.*;
import org.approvaltests.core.Options;
```

## Built-in Scrubbers

### GuidScrubber

Replaces UUIDs with `guid_1`, `guid_2`, etc.

```java
String[] guids = {
    "2fd78d4a-ad49-447d-96a8-deda585a9aa5",
    "2fd78d4a-1111-1111-1111-deda585a9aa5"
};
Approvals.verifyAll("guids", guids, new Options(Scrubbers::scrubGuid));
```

Output:
```
guids[0] = guid_1
guids[1] = guid_2
```

### DateScrubber

Auto-detects date format from example:

```java
Scrubber scrubber = DateScrubber.getScrubberFor("00:00:00");
Approvals.verify("created at 03:14:15", new Options().withScrubber(scrubber));
```

Output: `created at [Date1]`

#### Supported Date Formats

Pass an example date to `getScrubberFor()`:

- `23:30:00` - Time only
- `2024-12-17` - ISO date
- `2020-09-10T08:07Z` - ISO 8601 short
- `2020-09-10T08:07:89Z` - ISO 8601 with seconds
- `2020-09-10T01:23:45.678Z` - ISO 8601 with milliseconds
- `2024-12-18T14:04:46.746130Z` - ISO 8601 with nanoseconds
- `20210505T091112Z` - Compact ISO format
- `2014/05/13 16:30:59.786` - Slash-separated with ms
- `2025-05-15 16:57:04.599` - Datetime with space
- `Tue May 13 16:30:00` - Day Mon DD HH:MM:SS
- `Wed Nov 17 22:28:33 EET 2021` - With timezone name
- `Tue May 13 16:30:00 -0800 2014` - With timezone offset
- `13 May 2014 23:50:49,999` - DD Mon YYYY HH:MM:SS,ms
- `May 13, 2014 11:30:00 PM PST` - Mon DD, YYYY HH:MM:SS AM/PM TZ
- `13/05/2014 23:50:49` - DD/MM/YYYY with separators (., -, /)
- `Wed, 21 Oct 2015 07:28:00 GMT` - RFC 2822

#### Custom Date Format

```java
DateScrubber.addScrubber("2023-Dec-25", "\\d{4}-[A-Za-z]{3}-\\d{2}");
Scrubber scrubber = DateScrubber.getScrubberFor("2023-Dec-25");
```

#### With SimpleDateFormat

```java
SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd");
DateScrubber scrubber = DateScrubber.forSimpleDateFormat(sdf);
```

## RegExScrubber

### Static Replacement

```java
Scrubber scrubber = new RegExScrubber("\\d+", "[number]");
Approvals.verify("Count: 42", new Options(scrubber));
// Output: Count: [number]
```

### Dynamic Replacement

```java
Scrubber scrubber = new RegExScrubber("user_\\d+", n -> "user_" + n);
Approvals.verify("user_123 and user_456", new Options(scrubber));
// Output: user_1 and user_2
```

## Combining Scrubbers

### Scrubbers.scrubAll()

```java
Scrubber portScrubber = new RegExScrubber(":\\d+/", ":[port]/");
Scrubber dateScrubber = DateScrubber.getScrubberFor("20210505T091112Z");
Scrubber signatureScrubber = new RegExScrubber("Signature=.+", "Signature=[sig]");

Scrubber combined = Scrubbers.scrubAll(portScrubber, dateScrubber, signatureScrubber);

Approvals.verify(
    "http://127.0.0.1:55079/foo?Date=20210505T091112Z&Signature=4a7dd6f",
    new Options(combined)
);
```

Output: `http://127.0.0.1:[port]/foo?Date=[Date1]&Signature=[sig]`

### MultiScrubber Class

```java
Scrubber combined = new MultiScrubber(
    Arrays.asList(scrubber1, scrubber2, scrubber3)
);
```

## Using with Options

### Constructor

```java
Approvals.verify(data, new Options(Scrubbers::scrubGuid));
```

### withScrubber Method

```java
Options options = new Options()
    .withScrubber(DateScrubber.getScrubberFor("2024-01-15"));
Approvals.verify(data, options);
```

## Custom Scrubber

Implement the `Scrubber` interface:

```java
Scrubber myScrubber = input -> input
    .replaceAll("Bearer [a-zA-Z0-9]+", "Bearer [TOKEN]")
    .replaceAll("\\d{10}", "[TIMESTAMP]");

Approvals.verify(apiResponse, new Options(myScrubber));
```

## Common Patterns

### Scrub API Response

```java
Scrubber apiScrubber = Scrubbers.scrubAll(
    new GuidScrubber(),
    DateScrubber.getScrubberFor("2024-01-15T10:30:00Z"),
    new RegExScrubber("\"id\":\\s*\\d+", "\"id\": [ID]")
);

JsonApprovals.verifyAsJson(response, new Options(apiScrubber));
```

### Scrub Timestamps

```java
Scrubber scrubber = Scrubbers.scrubAll(
    DateScrubber.getScrubberForTimestamp(),
    DateScrubber.getScrubberForSqlDate()
);
```

## Built-in Utility Scrubbers

- `Scrubbers.scrubGuid(input)` - Scrub UUIDs
- `DateScrubber.getScrubberForTimestamp()` - Java Timestamp
- `DateScrubber.getScrubberForSqlDate()` - SQL Date
- `DateScrubber.getScrubberForDate()` - Java Date
