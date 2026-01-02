# Node.js ApprovalTests

## Installation

```bash
npm install approvals
```

## Quick Start

### Jest
```javascript
import { verify, verifyAsJson } from 'approvals/lib/Providers/Jest/JestApprovals';

describe('Reports', () => {
  it('generates report', () => {
    const result = generateReport();
    verify(result);
  });
});
```

### Mocha
```javascript
require('approvals').mocha();

describe('Reports', function() {
  it('generates report', function() {
    this.verify(generateReport());
  });
});
```

**First run:** Test fails, `.received` file created. Review it, approve it (copy to `.approved`), rerun.

## Common Imports

### Jest
```javascript
import { verify, verifyAsJson, verifyAll } from 'approvals/lib/Providers/Jest/JestApprovals';
import { verifyAllCombinations2 } from 'approvals/lib/Providers/Jest/CombinationApprovals';
import { Options } from 'approvals/lib/Core/Options';
```

### Mocha/Other
```javascript
const approvals = require('approvals');
```

## Core Patterns

### verify() - Basic verification
```javascript
verify(result);
approvals.verify(__dirname, 'test_name', result);
```

### verifyAsJson() - Objects as formatted JSON
```javascript
verifyAsJson(user);
approvals.verifyAsJSON(__dirname, 'test_name', user);
```

### verifyAll() - Collections with labels
```javascript
verifyAll('Users', users, (u) => `${u.name}: ${u.email}`);
```

### Scrubbing
```javascript
approvals.verifyAndScrub(
  __dirname, 'test_name', result,
  (text) => text.replace(/\d{4}-\d{2}-\d{2}/, '<DATE>')
);
```

## Node.js-Specific Notes

**__dirname required** - Mocha/raw API needs directory path for file location.

**Jest integration** - Cleaner API without __dirname, auto-detects test name.

**TypeScript** - Full type definitions included.

## Git Setup

```gitignore
*.received.*
```

Commit all `.approved.*` files.

## Deep References

- [API Reference](references/nodejs/api.md) - All functions and Options
- [Setup & Configuration](references/nodejs/setup.md) - reporters, config options
- [Scrubbers](references/nodejs/scrubbers.md) - Handling dynamic data
- [Inline Approvals](references/nodejs/inline.md) - Store approvals in code
