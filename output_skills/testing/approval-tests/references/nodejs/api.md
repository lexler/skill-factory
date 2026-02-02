# Node.js Approvals API

## Imports

```javascript
const approvals = require('approvals');

// Or for Jest:
import { verify, verifyAsJson, verifyAll } from 'approvals/lib/Providers/Jest/JestApprovals';
import { Options } from 'approvals/lib/Core/Options';
```

## Core Functions

### verify()
```javascript
approvals.verify(dirName, testName, data, optionsOverride?)
```
- **dirName**: Directory for approval files (use `__dirname`)
- **testName**: Test identifier (becomes filename)
- **data**: String or Buffer to verify
- **optionsOverride**: Optional config overrides

```javascript
approvals.verify(__dirname, 'test_output', 'Hello World');
```

### verifyAsJSON()
```javascript
approvals.verifyAsJSON(dirName, testName, data, optionsOverride?)
```
Auto-stringifies objects to JSON.

```javascript
approvals.verifyAsJSON(__dirname, 'test_user', { name: 'Alice', age: 30 });
```

### verifyAndScrub()
```javascript
approvals.verifyAndScrub(dirName, testName, data, scrubber, optionsOverride?)
```
Apply scrubber before verification.

```javascript
approvals.verifyAndScrub(
  __dirname,
  'test_output',
  data,
  (text) => text.replace(/\d{4}-\d{2}-\d{2}/, '<DATE>')
);
```

### verifyAsJSONAndScrub()
```javascript
approvals.verifyAsJSONAndScrub(dirName, testName, data, scrubber, optionsOverride?)
```
Combines JSON stringify with scrubbing.

### verifyWithControl()
```javascript
approvals.verifyWithControl(namer, writer, reporterFactory?, optionsOverride?)
```
Full control over namer, writer, reporter.

## Mocha Integration

```javascript
require('approvals').mocha();

describe('Tests', function() {
  it('should verify', function() {
    this.verify('Hello World');
    this.verifyAsJSON({ key: 'value' });
  });
});
```

## Jest Integration

```javascript
import { verify, verifyAsJson, verifyAll } from 'approvals/lib/Providers/Jest/JestApprovals';

describe('Tests', () => {
  it('should verify', () => {
    verify('Hello World');
    verifyAsJson({ key: 'value' });
  });
});
```

### verifyAll()
```javascript
verifyAll(header, list, formatter?, options?)
```

```javascript
verifyAll('Users', users, (u) => `${u.name}: ${u.email}`);
```

## Options Class

```javascript
import { Options } from 'approvals/lib/Core/Options';

const options = new Options()
  .withScrubber(myScrubber)
  .withReporter(myReporter)
  .forFile().withFileExtension('.json');

verify(data, options);
```

### Methods

- `withScrubber(fn)` - Set scrubber function
- `withReporter(reporter)` - Set reporter
- `withNamer(namer)` - Custom naming
- `forFile().withFileExtension('.ext')` - Set file extension
- `withConfig(modifier)` - Modify config

## Configuration

### Global Configure
```javascript
approvals.configure({
  reporters: ['p4merge', 'vscode'],
  normalizeLineEndingsTo: '\n',
  appendEOL: true,
  maxLaunches: 5,
});
```

### Config Options

- `reporters` (string[]) - Diff tools to try (default: see below)
- `normalizeLineEndingsTo` (boolean|string) - '\n' or '\r\n' (default: false)
- `appendEOL` (boolean) - Add EOL at end (default: true)
- `stripBOM` (boolean) - Remove BOM (default: false)
- `forceApproveAll` (boolean) - Auto-approve all (default: false)
- `maxLaunches` (number) - Max reporter launches (default: 10)

For reporters (diff tools, MultiReporter, custom reporters), see [reporters.md](reporters.md).

## Combination Testing (Jest)

```javascript
import { verifyAllCombinations2 } from 'approvals/lib/Providers/Jest/CombinationApprovals';

it('tests combinations', () => {
  verifyAllCombinations2(
    (a, b) => `${a} + ${b} = ${a + b}`,
    [1, 2, 3],    // First param options
    [10, 20]      // Second param options
  );
});
```

## Namer and Writer

### Namer Interface
```javascript
{
  getApprovedFile(ext) { return '/path/test.approved.txt'; },
  getReceivedFile(ext) { return '/path/test.received.txt'; }
}
```

### Writer Interface
```javascript
{
  getFileExtension() { return '.txt'; },
  write(filePath) { /* write data to filePath */ }
}
```
