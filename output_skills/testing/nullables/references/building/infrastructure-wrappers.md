# Infrastructure Wrappers

Infrastructure wrappers isolate external systems behind clean interfaces. Each wrapper is a single-responsibility class that presents your application's view of an external system.

## Contents

- [Structure](#structure)
- [Common Mistakes with createNull()](#common-mistakes-with-createnull)
- [Building a Wrapper: Step by Step](#building-a-wrapper-step-by-step)
- [Wrapper Composition (Fake It Once You Make It)](#wrapper-composition-fake-it-once-you-make-it)
- [Zero-Impact Instantiation](#zero-impact-instantiation)
- [Parameterless Instantiation](#parameterless-instantiation)
- [When NOT to Create a Wrapper](#when-not-to-create-a-wrapper)

## Structure

```
┌─────────────────────────────────────────────────────────┐
│                    Your Application                      │
├─────────────────────────────────────────────────────────┤
│                  Infrastructure Wrapper                  │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────┐  │
│  │ create()    │  │ createNull()│  │ Business methods│  │
│  │ Real dep    │  │ Stubbed dep │  │ at your level   │  │
│  └─────────────┘  └─────────────┘  └─────────────────┘  │
├─────────────────────────────────────────────────────────┤
│              Third-party code / External system          │
└─────────────────────────────────────────────────────────┘
```

## Common Mistakes with createNull()

Avoid these patterns that defeat the purpose of Nullables:

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

The correct pattern:
- `createNull()` parameters should match the caller's abstraction level
- `createNull()` must use a stub, never real infrastructure
- Callers should only see `create()` and `createNull()`, never the stub class

## Building a Wrapper: Step by Step

### 1. Define Your Interface

Start with the methods your application needs, not what the external system provides:

```javascript
// Your app needs these operations
class FileSystem {
  readFile(path) { }
  writeFile(path, content) { }
  exists(path) { }
}
```

### 2. Implement with Real Dependency

```javascript
import fs from "node:fs/promises";

class FileSystem {
  static create() {
    return new FileSystem(fs);
  }

  constructor(fsModule) {
    this._fs = fsModule;
  }

  async readFile(path) {
    return await this._fs.readFile(path, "utf8");
  }

  async writeFile(path, content) {
    await this._fs.writeFile(path, content, "utf8");
  }

  async exists(path) {
    try {
      await this._fs.access(path);
      return true;
    } catch {
      return false;
    }
  }
}
```

### 3. Add Nullable Version

```javascript
import { EventEmitter } from "node:events";

class FileSystem {
  static create() {
    return new FileSystem(fs);
  }

  static createNull(files = {}) {
    return new FileSystem(new StubbedFs(files));
  }

  constructor(fsModule) {
    this._fs = fsModule;
    this._emitter = new EventEmitter();
  }

  async readFile(path) {
    return await this._fs.readFile(path, "utf8");
  }

  async writeFile(path, content) {
    await this._fs.writeFile(path, content, "utf8");
    this._emitter.emit("write", { path, content });
  }

  async exists(path) {
    try {
      await this._fs.access(path);
      return true;
    } catch {
      return false;
    }
  }

  trackWrites() {
    const data = [];
    this._emitter.on("write", (info) => data.push(info));
    return { data };
  }
}

class StubbedFs {
  constructor(files) {
    this._files = { ...files };
  }

  async readFile(path) {
    if (!(path in this._files)) {
      const error = new Error(`ENOENT: no such file: ${path}`);
      error.code = "ENOENT";
      throw error;
    }
    return this._files[path];
  }

  async writeFile(path, content) {
    this._files[path] = content;
  }

  async access(path) {
    if (!(path in this._files)) {
      const error = new Error(`ENOENT: no such file: ${path}`);
      error.code = "ENOENT";
      throw error;
    }
  }
}
```

### 4. Test Your Wrapper

```javascript
describe("FileSystem", () => {
  describe("Nullable", () => {
    it("reads pre-configured files", async () => {
      const fs = FileSystem.createNull({
        "/data/config.json": '{"key": "value"}'
      });

      const content = await fs.readFile("/data/config.json");
      assert.equal(content, '{"key": "value"}');
    });

    it("tracks writes", async () => {
      const fs = FileSystem.createNull();
      const writes = fs.trackWrites();

      await fs.writeFile("/output.txt", "hello");

      assert.deepEqual(writes.data, [
        { path: "/output.txt", content: "hello" }
      ]);
    });

    it("throws for missing files", async () => {
      const fs = FileSystem.createNull({});

      await assert.rejects(
        () => fs.readFile("/missing.txt"),
        { code: "ENOENT" }
      );
    });
  });
});
```

### Complete Example: CommandLine with Output Tracking

This example shows a wrapper with [Output Tracking](output-tracking.md) to observe what was written:

```javascript
import { OutputListener } from "./output_listener.js";

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

## Wrapper Composition (Fake It Once You Make It)

Once your low-level infrastructure has `createNull()`, higher-level code doesn't need its own stubs. It composes from the Nullables below it.

```
App                        ← No stub needed, composes from below
 └── OrderService          ← No stub needed, composes from below
      ├── Database         ← Nullable (has embedded stub)
      └── Emailer          ← Nullable (has embedded stub)
```

Only the leaves (Database, Emailer) have embedded stubs. Everything above just wires up `createNull()` calls.

### Multi-Layer Example

```javascript
// LEAF: Database has its own embedded stub
class Database {
  static create() {
    return new Database(mysql.createPool());
  }

  static createNull({ orders = [], users = [] } = {}) {
    return new Database(new StubbedPool(orders, users));
  }

  // ... methods ...
}

// LEAF: Emailer has its own embedded stub
class Emailer {
  static create() {
    return new Emailer(new SmtpClient());
  }

  static createNull() {
    return new Emailer(new StubbedSmtp());
  }

  // ... methods ...
}

// MIDDLE: OrderService has NO stub—it composes
class OrderService {
  static create() {
    return new OrderService(Database.create(), Emailer.create());
  }

  static createNull({ orders = [], users = [] } = {}) {
    const db = Database.createNull({ orders, users });
    const emailer = Emailer.createNull();
    return {
      service: new OrderService(db, emailer),
      emails: emailer.trackOutput(),
      dbWrites: db.trackWrites()
    };
  }

  constructor(database, emailer) {
    this._db = database;
    this._emailer = emailer;
  }

  async processOrder(orderId) {
    const order = await this._db.getOrder(orderId);
    // ... process ...
    await this._emailer.sendConfirmation(order);
  }
}

// TOP: App has NO stub—it composes
class App {
  static create() {
    return new App(OrderService.create(), Logger.create());
  }

  static createNull({ orders = [], users = [] } = {}) {
    const { service, emails, dbWrites } = OrderService.createNull({ orders, users });
    const logger = Logger.createNull();
    return {
      app: new App(service, logger),
      emails,
      dbWrites,
      logs: logger.trackOutput()
    };
  }

  constructor(orderService, logger) {
    this._orders = orderService;
    this._logger = logger;
  }
}
```

### Testing at Any Level

```javascript
it("sends confirmation email when order processed", async () => {
  const { app, emails } = App.createNull({
    orders: [{ id: "123", items: ["widget"] }]
  });

  await app.processOrder("123");

  assert.equal(emails.data.length, 1);
  assert.equal(emails.data[0].to, "customer@example.com");
});
```

The test creates `App` but verifies email behavior. No mocks, no stubs at the App level—just composition.

### Single-Level Composition

For simpler cases with one dependency:

```javascript
class LoginClient {
  static create() {
    return new LoginClient(HttpClient.create());
  }

  static createNull({ email = "null@example.com", verified = true } = {}) {
    const httpResponse = {
      status: 200,
      body: JSON.stringify({ email, email_verified: verified })
    };
    return new LoginClient(
      HttpClient.createNull({ "/userinfo": httpResponse })
    );
  }

  constructor(httpClient) {
    this._http = httpClient;
  }

  async getUserInfo(token) {
    const response = await this._http.get("/userinfo", {
      headers: { Authorization: `Bearer ${token}` }
    });
    return JSON.parse(response.body);
  }
}
```

`LoginClient.createNull()` accepts domain-level params (`email`, `verified`) and translates them to HTTP-level responses internally. Callers never see HTTP details.

## Zero-Impact Instantiation

Constructors should perform no work. Defer expensive operations:

```javascript
// BAD
class Database {
  constructor(connectionString) {
    this._connection = mysql.createConnection(connectionString);  // Work!
  }
}

// GOOD
class Database {
  constructor(connection) {
    this._connection = connection;
  }

  static create(connectionString) {
    return new Database(mysql.createConnection(connectionString));
  }

  async connect() {
    await this._connection.connect();  // Deferred
  }
}
```

## Parameterless Instantiation

Support creating with sensible defaults:

```javascript
class App {
  static create(
    commandLine = CommandLine.create(),
    config = Config.create(),
    logger = Logger.create()
  ) {
    return new App(commandLine, config, logger);
  }

  static createNull({
    args = [],
    config = {},
    logOutput
  } = {}) {
    const cl = CommandLine.createNull({ args });
    const cfg = Config.createNull(config);
    const log = Logger.createNull();
    const app = new App(cl, cfg, log);
    return {
      app,
      logOutput: log.trackOutput()
    };
  }
}
```

## When NOT to Create a Wrapper

Not everything needs a wrapper. Create wrappers for:
- External I/O (network, filesystem, databases)
- Non-deterministic operations (clocks, random numbers, UUIDs)
- Expensive operations you want to avoid in tests

Skip wrappers when:
- **The dependency is already testable** - Pure functions, immutable data structures
- **You're wrapping a wrapper** - Don't wrap your own abstractions; make them Nullable directly
