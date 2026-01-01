# Infrastructure Wrappers

Infrastructure wrappers isolate external systems behind clean interfaces. Each wrapper is a single-responsibility class that presents your application's view of an external system.

## Contents

- [Structure](#structure)
- [Building a Wrapper: Step by Step](#building-a-wrapper-step-by-step)
- [Wrapper Composition](#wrapper-composition)
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

## Wrapper Composition

Higher-level wrappers can delegate to lower-level Nullables:

```javascript
class LoginClient {
  static create() {
    return new LoginClient(HttpClient.create());
  }

  static createNull({ email = "null@example.com", verified = true } = {}) {
    // Translate to HTTP-level responses
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
- **The dependency is fast and deterministic** - Math utilities, string formatters
- **You're wrapping a wrapper** - Don't wrap your own abstractions; make them Nullable directly
- **Tests can use the real thing** - In-memory databases, local file operations in temp directories

**Rule of thumb:** If using the real dependency in tests is fast, deterministic, and has no side effects, skip the wrapper.
