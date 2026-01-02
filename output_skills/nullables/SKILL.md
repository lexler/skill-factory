---
name: nullables
description: Writes tests without mocks using James Shore's Nullables pattern. Use when writing tests and designing code for testability.
---

# Nullables: Testing Without Mocks

STARTER_CHARACTER = ⭕️

External I/O is slow and flaky. Tests that hit real databases, APIs, or file systems run slow and fail randomly. We want tests that run in milliseconds and never fail due to network issues. Fast tests mean fast feedback loops.

Nullables are production code with an "off switch" for infrastructure - not test doubles, but real code you can ship (useful for dry-run modes, cache warming, offline operation). 
They enable **narrow, sociable, state-based tests**:
- **Narrow**: Each test focuses on a specific class or module, not broad end-to-end flows
- **Sociable**: Tests use real dependencies, not mocks—only infrastructure I/O is neutralized
- **State-based**: Assert on outputs and state, not on which methods were called

Nullables are solving the problem that using mocking libraries introduces: mocking libraries often couple tests to implementation (by verifying specific method calls).
Test code using mocking libraries is brittle and breaks when code is refactored, even when behavior is unchanged.

## When to Use Nullables

Use Nullables when:
- Testing code that talks to external systems (HTTP, files, databases, clocks)
- You want tests that validate behavior, not implementation details
- Mock setup is becoming complex or brittle
- You need tests that run fast without real I/O

Do NOT use when:
- Testing pure logic (no infrastructure) — just test directly
- The external system is simple enough to use directly in tests

## Getting Started

**Greenfield code**: Start with hardcoded implementations. Add infrastructure wrappers incrementally as tests demand them—don't over-engineer upfront. See [infrastructure-wrappers.md](references/building/infrastructure-wrappers.md#when-not-to-create-a-wrapper) for when NOT to create a wrapper.

**Existing codebase with mocks**: See [migration.md](references/migration.md) for incremental conversion strategies (Descend the Ladder, Climb the Ladder, Throwaway Stubs).

## Structure Your Code: A-Frame

Traditional layered architecture stacks Logic on top of Infrastructure. This causes problems: Logic depends on slow and brittle infrastructure, making it hard to test. With nullables, logic never imports Infrastructure directly. This is the approach that makes Nullables work well - you can swap real infrastructure for nulled versions without touching Logic.

A-Frame makes Logic and Infrastructure **peers** instead of layers. Neither depends on the other. Logic stays pure, Infrastructure is isolated behind Nullables.

```
        Application (coordinates)
            ↓              ↓
Logic (pure, tested)    Infrastructure (Nullables)
```

**Key rule:** Logic never imports Infrastructure directly. Application coordinates between them.

- **Logic** — pure functions, test directly
- **Infrastructure** — wrapped with Nullables, test with `createNull()`
- **Application** — coordinates via [Logic Sandwich](references/architecture/logic-sandwich.md): read → process → write

For full architecture details, see [a-frame.md](references/architecture/a-frame.md). For event-driven code, see [event-driven.md](references/architecture/event-driven.md).

## Core Pattern: Two Factory Methods

Unlike mocks, Nullables are production code. They can power real features like dry-run mode or cache warming.

Every infrastructure wrapper has two creation paths:

```javascript
class Clock {
  static create() {
    return new Clock(Date);  // Real system clock
  }

  static createNull(now = "2020-01-01T00:00:00Z") {
    return new Clock(new StubbedDate(now));  // Controlled clock
  }

  constructor(dateClass) {
    this._dateClass = dateClass;
  }

  now() {
    return new this._dateClass().toISOString();
  }
}

class StubbedDate {
  constructor(isoString) {
    this._time = new Date(isoString).getTime();
  }
  
  toISOString() {
    return new Date(this._time).toISOString();
  }
}
```

**Key principle**: `createNull()` takes parameters at the caller's abstraction level. Clock accepts ISO strings, not milliseconds.

**Common mistakes with `createNull()`:**

```javascript
// BAD: Parameter exposes implementation (milliseconds instead of ISO string)
static createNull(timestamp = Date.now()) {
  return new Clock(new StubbedDate(timestamp));
}

// BAD: createNull still calls real infrastructure
static createNull() {
  return new Clock(Date);  // This defeats the purpose - still uses real Date
}

// BAD: No factory method - forces tests to know about StubbedDate
const clock = new Clock(new StubbedDate("2020-01-01"));  // Leaks internals to callers
```

## Complete Example: Command Line Wrapper

```javascript
import { OutputListener } from "./output_listener.js";  // Records what was written; see output-tracking.md for implementation

export class CommandLine {
  static create() {
    return new CommandLine(process);
  }

  static createNull({ args = [] } = {}) {
    return new CommandLine(new StubbedProcess(args));
  }

  constructor(proc) {
    this._process = proc;
    this._listener = new OutputListener();
  }

  args() {
    return this._process.argv.slice(2);
  }

  writeOutput(text) {
    this._process.stdout.write(text);
    this._listener.emit(text);
  }

  trackOutput() {
    return this._listener.trackOutput();
  }
}

class StubbedProcess {
  constructor(args) {
    this._args = args;
  }
  get argv() {
    return ["node", "script.js", ...this._args];
  }
  get stdout() {
    return { write() {} };
  }
}
```

For step-by-step wrapper construction and when NOT to wrap, see [infrastructure-wrappers.md](references/building/infrastructure-wrappers.md).

## Testing with Nullables

```javascript
describe("App", () => {
  it("transforms input and writes result", () => {
    const { output } = run({ args: ["hello"] });
    assert.deepEqual(output.data, ["uryyb\n"]);  // ROT-13 of "hello"
  });

  it("shows usage when no args", () => {
    const { output } = run({ args: [] });
    assert.deepEqual(output.data, ["Usage: run <text>\n"]);
  });

  function run({ args = [] } = {}) {
    const commandLine = CommandLine.createNull({ args });
    const output = commandLine.trackOutput();

    const app = new App(commandLine);
    app.run();

    return { output };
  }
});
```

**Notice**: Tests exercise real `App` code. Only infrastructure I/O is neutralized.

### Testing Philosophy

Nullables enable a different approach:

- **State-based, not interaction-based** — verify what was produced, not which methods were called
- **Sociable, not solitary** — tests use real dependencies; only infrastructure is nulled
- **Overlapping coverage** — when tests share real code, bugs cause multiple failures, pinpointing the problem
- **Paranoic Telemetry** — assume everything will eventually fail. Test error paths, timeouts, and network failures as thoroughly as happy paths. Configure Nullables to return errors, simulate hanging requests, and exhaust retry limits. If your infrastructure can fail in production, test that failure mode.
- **Collaborator-Based Isolation** — use dependencies' own tracking methods in assertions rather than hardcoding expectations; tests stay resilient when implementation changes

### Testing Techniques

See [test-patterns.md](references/test-patterns.md) for details and examples:

- **Arrange-Act-Assert**: Structure tests as setup, execute, verify
- **Signature Shielding**: Helper functions (like `run()` above) protect tests from constructor changes
- **Narrow Integration Tests**: Test wrappers against real systems in isolation — sociable tests verify logic, but you need a few tests hitting real infrastructure to verify the wrapper actually works
- **Testing Sequences**: Response arrays for retries, pagination
- **Testing Time-Dependent Code**: Nulled Clock with `advance()`
- **Behavior Simulation**: `simulateX()` methods for event-driven code
- **Testing Error Paths**: Configure Nullables to return errors, timeouts

## Supporting Patterns

### 1. [Output Tracking](references/building/output-tracking.md)

Test what was *produced*, not what methods were *called*. Refactoring internals won't break your tests because they are not coupled to implementation details.

```javascript
const log = Log.createNull();
const output = log.trackOutput();

myService.doWork(log);

assert.deepEqual(output.data, [
  { level: "info", message: "Starting work" },
  { level: "info", message: "Work complete" }
]);
```

### 2. [Configurable Responses](references/building/configurable-responses.md)

Configure at *your* abstraction level, not the implementation's. When internals change, tests stay meaningful.

```javascript
// Single response (repeats forever)
const client = HttpClient.createNull({ status: 200, body: "OK" });

// Multiple responses (sequence)
const client = HttpClient.createNull([
  { status: 200, body: "first" },
  { status: 500, body: "error" },
]);
```

### 3. [Embedded Stubs](references/building/embedded-stubs.md)

Stubs live in production code, not test files. They're maintained alongside the wrapper and implement only what's actually used.

```javascript
class HttpClient {
  static createNull(responses) {
    return new HttpClient(new StubbedHttp(responses));
  }
  // ...
}

class StubbedHttp {  // Implements only what HttpClient actually uses
  request(options) {
    return new StubbedRequest(this._nextResponse());
  }
}
```

### 4. [Wrapper Composition](references/building/infrastructure-wrappers.md#wrapper-composition-fake-it-once-you-make-it)

High-level code doesn't need its own stubs—it composes from lower-level Nullables. Only infrastructure leaves have embedded stubs; everything above just wires up `createNull()` calls.

## Anti-Patterns

**Using mock libraries** - Often couples tests to implementation (specific method calls), making tests brittle. Don't import sinon, jest.mock, etc. Nullables replace them entirely.

**Writing broad integration tests** - Sociable unit tests with Nullables provide coverage without slow, flaky end-to-end tests.

**Testing interactions instead of outcomes**
Problem: couple tests to implementation, resulting in brittle tests. 

```javascript
// BAD: Verifying method calls (mock-style thinking)
verify(logger).info("message");

// GOOD: Verifying what was produced
assert.deepEqual(logOutput.data, [{ level: "info", message: "message" }]);
```

**Constructor connects to infrastructure** (Zero-Impact Instantiation)
Problem: makes it impossible to decouple your logic from brittle slow infrastructure.
Constructors should perform no work—no connections, no I/O, no side effects. Defer to explicit methods. See [infrastructure-wrappers.md](references/building/infrastructure-wrappers.md#zero-impact-instantiation).

```javascript
// BAD: Constructor connects to db
constructor(connectionString) {
  this._db = new Database(connectionString);  // Immediate connection
}

// GOOD: Deferred connection
constructor(db) {
  this._db = db;
}
async connect() {
  await this._db.connect();
}
```

**Parameters at wrong abstraction level**
Problem: exposes internal infrastructure considerations to your code, violating information hiding.
```javascript
// BAD: Leaking implementation details
LoginClient.createNull({ httpResponse: { status: 200, body: '{"email":"x"}' } });

// GOOD: Caller's abstraction level
LoginClient.createNull({ email: "user@example.com", verified: true });
```

**Stubs in test files** - Stubs should be embedded in production code alongside the wrapper (at the end of file, after production code), not scattered in test files. This keeps them maintained and discoverable. See [embedded-stubs.md](references/building/embedded-stubs.md).

**Mocking your own code** - Only wrap third-party code and infrastructure. Your own classes don't need stubs—either make them Nullable directly, or null their dependencies. If you're writing a stub for your own class, you're probably doing it wrong.

## Signs You're Over-Engineering

- **Wrapping pure code** — pure functions and immutable data don't need Nullables; test them directly
- **Stub is as complex as the real thing** — if your stub needs significant logic, reconsider the abstraction
