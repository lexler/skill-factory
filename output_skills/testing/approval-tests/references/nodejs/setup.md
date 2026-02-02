# Node.js Approvals Setup

## Installation

```bash
npm install approvals
```

## Mocha Setup

```javascript
// In your test file or setup file
require('approvals').mocha();

// Or with custom base directory:
require('approvals').mocha('/path/to/approvals');
```

### Mocha Test Example

```javascript
require('approvals').mocha();

describe('My Feature', function() {
  it('generates correct output', function() {
    const result = generateOutput();
    this.verify(result);
  });

  it('returns correct JSON', function() {
    const data = fetchData();
    this.verifyAsJSON(data);
  });
});
```

## Jest Setup

### Import Methods Directly

```javascript
import { verify, verifyAsJson, verifyAll } from 'approvals/lib/Providers/Jest/JestApprovals';
import { Options } from 'approvals/lib/Core/Options';

describe('My Feature', () => {
  it('generates correct output', () => {
    verify(generateOutput());
  });

  it('returns correct JSON', () => {
    verifyAsJson(fetchData());
  });
});
```

## Direct API Usage

Without test framework integration:

```javascript
const approvals = require('approvals');

// Verify a string
approvals.verify(__dirname, 'test_name', 'expected output');

// Verify JSON
approvals.verifyAsJSON(__dirname, 'test_name', { key: 'value' });
```

## Configuration

### Global Configuration

```javascript
const approvals = require('approvals');

approvals.configure({
  reporters: ['vscode', 'p4merge'],
  normalizeLineEndingsTo: '\n',
  appendEOL: true,
});
```

### Home Directory Config

Create `~/.approvalsConfig` (YAML or JSON):

```yaml
reporters:
  - vscode
  - p4merge
normalizeLineEndingsTo: "\n"
appendEOL: true
```

### Per-Test Override

```javascript
approvals.verify(__dirname, 'test', data, {
  reporters: ['gitdiff'],
  normalizeLineEndingsTo: false
});
```

## Git Configuration

Add to `.gitignore`:
```
*.received.*
```

Add to `.gitattributes`:
```
*.approved.* eol=lf
```

## TypeScript Setup

```typescript
import approvals from 'approvals';
import { verify, verifyAsJson } from 'approvals/lib/Providers/Jest/JestApprovals';
import { Options } from 'approvals/lib/Core/Options';

// Use directly
verify('Hello World');
verifyAsJson({ key: 'value' });
```

## CI Configuration

For CI environments without diff tools:

```javascript
approvals.configure({
  reporters: ['copycommand'],  // Just outputs copy command
  // or
  reporters: ['donothing'],    // Silent, just fails
});
```

## Reporters

```javascript
approvals.configure({
  reporters: ['vscode', 'p4merge', 'gitdiff']
});
```

For available reporters, MultiReporter, and custom reporters, see [reporters.md](reporters.md).
