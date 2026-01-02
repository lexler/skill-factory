# Node.js Scrubbers

Scrubbers normalize dynamic data before comparison.

## Imports

```javascript
const { Scrubbers } = require('approvals').scrubbers;
// Or:
import { Scrubbers } from 'approvals/lib/Scrubbers/Scrubbers';
```

## Built-in Scrubbers

### guidScrubber

Replaces UUIDs with `guid_1`, `guid_2`, etc.

```javascript
const scrubber = Scrubbers.createGuidScrubber();

// Or legacy static method:
Scrubbers.guidScrubber(data);
```

**Example:**
```javascript
import { verifyAsJson } from 'approvals/lib/Providers/Jest/JestApprovals';
import { Options } from 'approvals/lib/Core/Options';
import { Scrubbers } from 'approvals/lib/Scrubbers/Scrubbers';

verifyAsJson(
  { id: '58f471f1-8b1f-413c-8971-21cb23bfc8f2', name: 'Alice' },
  new Options().withScrubber(Scrubbers.createGuidScrubber())
);
// Result: { id: "guid_1", name: "Alice" }
```

## Custom Regex Scrubber

```javascript
Scrubbers.createReqexScrubber(regex, replacement)
```

Note: Method name has typo "Reqex" (not "Regex").

### With String Replacement

```javascript
const scrubber = Scrubbers.createReqexScrubber(
  /\d{4}-\d{2}-\d{2}/gi,
  '<DATE>'
);

verify(
  'Created: 2024-01-15',
  new Options().withScrubber(scrubber)
);
// Result: Created: <DATE>
```

### With Lambda Replacement

```javascript
const scrubber = Scrubbers.createReqexScrubber(
  /user_\d+/gi,
  (index) => `<user_${index}>`
);

verify(
  'user_123 assigned to user_456',
  new Options().withScrubber(scrubber)
);
// Result: <user_0> assigned to <user_1>
```

## Combining Scrubbers

### multiScrubber

Chain multiple scrubbers:

```javascript
const scrubber = Scrubbers.multiScrubber([
  Scrubbers.createGuidScrubber(),
  Scrubbers.createReqexScrubber(/\d{4}-\d{2}-\d{2}/, '<DATE>'),
  (text) => text.replace(/password=\w+/, 'password=<HIDDEN>')
]);

verify(data, new Options().withScrubber(scrubber));
```

## Date Scrubber

```javascript
import { DateScrubber } from 'approvals/lib/Scrubbers/DateScrubber';

const scrubber = DateScrubber.getScrubberFor('2020-09-10T08:07:89Z');
```

Supported formats (pass an example to `getScrubberFor()`):

- `23:30:00` - Time only
- `2020-09-10T08:07Z` - ISO 8601 short
- `2020-09-10T08:07:89Z` - ISO 8601 with seconds
- `2020-09-10T01:23:45.678Z` - ISO 8601 with milliseconds
- `20210505T091112Z` - Compact ISO format
- `2014/05/13 16:30:59.786` - Slash-separated with milliseconds
- `Tue May 13 16:30:00` - Day Mon DD HH:MM:SS
- `Tue May 13 16:30:00 -0800 2014` - With timezone offset
- `Wed Nov 17 22:28:33 EET 2021` - With timezone name
- `Tue May 13 2014 23:30:00.789` - Day Mon DD YYYY HH:MM:SS.ms
- `13 May 2014 23:50:49,999` - DD Mon YYYY HH:MM:SS,ms
- `May 13, 2014 11:30:00 PM PST` - Mon DD, YYYY HH:MM:SS AM/PM TZ
- `Sun, 06 Nov 2022 11:23:20 GMT` - RFC 2822

## Using with verify Functions

### With Options (Jest)

```javascript
import { verify } from 'approvals/lib/Providers/Jest/JestApprovals';
import { Options } from 'approvals/lib/Core/Options';

verify(data, new Options().withScrubber(myScrubber));
```

### With verifyAndScrub (legacy)

```javascript
const approvals = require('approvals');

approvals.verifyAndScrub(
  __dirname,
  'test_name',
  data,
  myScrubber
);
```

### With verifyAsJSONAndScrub

```javascript
approvals.verifyAsJSONAndScrub(
  __dirname,
  'test_name',
  jsonData,
  myScrubber
);
```

## Custom Scrubber Function

Any function `string -> string` works:

```javascript
const myScrubber = (text) => {
  return text
    .replace(/Bearer [a-zA-Z0-9]+/, 'Bearer <TOKEN>')
    .replace(/\d{10}/, '<TIMESTAMP>');
};

verify(apiResponse, new Options().withScrubber(myScrubber));
```

## Common Patterns

### Scrub API Response

```javascript
const apiScrubber = Scrubbers.multiScrubber([
  Scrubbers.createGuidScrubber(),
  DateScrubber.getScrubberFor('2020-09-10T01:23:45.678Z'),
  Scrubbers.createReqexScrubber(/"token":\s*"[^"]+"/, '"token": "<TOKEN>"'),
]);

verifyAsJson(response, new Options().withScrubber(apiScrubber));
```

### Scrub Log Output

```javascript
const logScrubber = Scrubbers.multiScrubber([
  DateScrubber.getScrubberFor('23:30:00'),
  (text) => text.split('\n')
    .filter(line => !line.includes('DEBUG'))
    .join('\n'),
]);
```
