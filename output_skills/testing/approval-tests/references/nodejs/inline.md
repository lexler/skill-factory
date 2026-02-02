# Node.js Inline Approvals

Inline approvals (storing expected output in docstrings/comments) are **not currently supported** in Approvals.NodeJS.

## Alternative: Standard File-Based Approvals

Use standard file-based approvals instead:

```javascript
import { verify } from 'approvals/lib/Providers/Jest/JestApprovals';

it('generates output', () => {
  verify('expected output');
  // Creates: test_name.approved.txt
});
```

## If You Need Inline-Style Tests

Consider these alternatives:

### 1. Simple Assertions for Short Output

```javascript
it('returns greeting', () => {
  expect(greet('Alice')).toBe('Hello, Alice!');
});
```

### 2. Snapshot Testing (Jest Built-in)

```javascript
it('returns greeting', () => {
  expect(greet('Alice')).toMatchInlineSnapshot(`"Hello, Alice!"`);
});
```

### 3. Table-Driven Tests

```javascript
const testCases = [
  ['hello', 'HELLO'],
  ['world', 'WORLD'],
];

it.each(testCases)('uppercase(%s) = %s', (input, expected) => {
  expect(uppercase(input)).toBe(expected);
});
```

## When to Use File-Based Approvals

File-based approvals are preferred when:
- Output is complex (JSON, multi-line)
- You want diff tool integration
- Output may change and needs visual review
