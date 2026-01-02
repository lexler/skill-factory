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

const scrubber = DateScrubber.getScrubberFor('2024-01-15 10:30:00');
```

Supported formats:
- `2024-01-15` (ISO date)
- `2024-01-15 10:30:00` (datetime)
- `2020-09-10T08:07:89Z` (ISO 8601)
- `Tue May 13 16:30:00 2014`
- Many more locale formats

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
  DateScrubber.getScrubberFor('2024-01-15T10:30:00Z'),
  Scrubbers.createReqexScrubber(/"token":\s*"[^"]+"/, '"token": "<TOKEN>"'),
]);

verifyAsJson(response, new Options().withScrubber(apiScrubber));
```

### Scrub Log Output

```javascript
const logScrubber = Scrubbers.multiScrubber([
  DateScrubber.getScrubberFor('2024-01-15 10:30:00'),
  (text) => text.split('\n')
    .filter(line => !line.includes('DEBUG'))
    .join('\n'),
]);
```
