# Embedded Stubs

Embedded Stubs are minimal implementations of third-party code that live inside your wrapper. They implement only the methods your wrapper actually uses.

## Contents

- [Placement](#placement)
- [Why Embed?](#why-embed)
- [Implement Only What You Use](#implement-only-what-you-use)
- [Async Patterns](#async-patterns)
- [Error Simulation](#error-simulation)
- [Thin Wrapper Pattern (Static Languages)](#thin-wrapper-pattern-static-languages)
- [Complex Stubs: File System Example](#complex-stubs-file-system-example)
- [Testing the Stub Itself](#testing-the-stub-itself)

## Placement

Embedded stubs belong in the same file as the wrapper, not in test files:

```javascript
// file: http_client.js

export class HttpClient {
  static create() {
    return new HttpClient(http);
  }

  static createNull(responses = {}) {
    return new HttpClient(new StubbedHttp(responses));
  }

  // ... wrapper methods ...
}

// Embedded stub - same file, not exported
class StubbedHttp {
  constructor(responses) {
    this._responses = responses;
  }

  request(options) {
    // Minimal implementation
  }
}
```

## Why Embed?

1. **Maintenance**: When the wrapper changes, the stub is right there to update
2. **Minimal surface**: Only implement what the wrapper uses
3. **No test pollution**: Production code, not test code
4. **Discoverability**: Reading the wrapper shows the full picture

## Implement Only What You Use

```javascript
// Real http module has: request, get, createServer, Agent, etc.
// Your wrapper only uses request()

class StubbedHttp {
  constructor(responses) {
    this._responses = ConfigurableResponses.mapObject(responses, "HTTP");
  }

  // Only this method - that's all HttpClient calls
  request(options) {
    const response = this._responses[options.path]?.next() ?? {
      status: 404,
      body: "Not found"
    };
    return new StubbedRequest(response);
  }
}
```

## Async Patterns

Real I/O is async. Stubs must mimic this timing:

### Event-Based (Node.js Streams)

```javascript
import { EventEmitter } from "node:events";

class StubbedRequest extends EventEmitter {
  constructor(response) {
    super();
    this._response = response;
  }

  end() {
    // Use setImmediate to mimic async behavior
    setImmediate(() => {
      this.emit("response", new StubbedResponse(this._response));
    });
  }
}

class StubbedResponse extends EventEmitter {
  constructor(data) {
    super();
    this.statusCode = data.status;

    setImmediate(() => {
      this.emit("data", Buffer.from(data.body));
      this.emit("end");
    });
  }
}
```

### Promise-Based

```javascript
class StubbedFetch {
  constructor(responses) {
    this._responses = responses;
  }

  async fetch(url, options) {
    const response = this._responses[url];
    if (!response) {
      throw new Error(`No response configured for ${url}`);
    }

    // Simulate network delay if needed
    if (response.delay) {
      await new Promise(resolve => setTimeout(resolve, response.delay));
    }

    return {
      ok: response.status >= 200 && response.status < 300,
      status: response.status,
      json: async () => JSON.parse(response.body),
      text: async () => response.body
    };
  }
}
```

## Error Simulation

Stubs should support error cases:

```javascript
class StubbedHttp {
  request(options) {
    const response = this._responses[options.path]?.next();

    if (response?.error) {
      return new StubbedErrorRequest(response.error);
    }

    return new StubbedRequest(response);
  }
}

class StubbedErrorRequest extends EventEmitter {
  constructor(error) {
    super();
    this._error = error;
  }

  end() {
    setImmediate(() => {
      this.emit("error", new Error(this._error));
    });
  }
}
```

## Thin Wrapper Pattern (Static Languages)

In statically-typed languages, use a thin interface:

```java
public class DieRoller {
    private final RandomWrapper random;

    public static DieRoller create() {
        return new DieRoller(new RealRandom());
    }

    public static DieRoller createNull(int... rolls) {
        return new DieRoller(new StubbedRandom(rolls));
    }

    private DieRoller(RandomWrapper random) {
        this.random = random;
    }

    public int roll() {
        return random.nextInt(6) + 1;
    }

    // Thin interface - only methods actually used
    private interface RandomWrapper {
        int nextInt(int bound);
    }

    private static class RealRandom implements RandomWrapper {
        private final Random random = new Random();

        public int nextInt(int bound) {
            return random.nextInt(bound);
        }
    }

    private static class StubbedRandom implements RandomWrapper {
        private final int[] rolls;
        private int index = 0;

        StubbedRandom(int[] rolls) {
            this.rolls = rolls;
        }

        public int nextInt(int bound) {
            return rolls[index++] - 1;  // Adjust for roll() adding 1
        }
    }
}
```

## Complex Stubs: File System Example

```javascript
class StubbedFs {
  constructor(initialFiles = {}) {
    this._files = new Map(Object.entries(initialFiles));
  }

  async readFile(path, encoding) {
    if (!this._files.has(path)) {
      const error = new Error(`ENOENT: no such file or directory: ${path}`);
      error.code = "ENOENT";
      throw error;
    }
    return this._files.get(path);
  }

  async writeFile(path, content) {
    this._files.set(path, content);
  }

  async unlink(path) {
    if (!this._files.has(path)) {
      const error = new Error(`ENOENT: no such file or directory: ${path}`);
      error.code = "ENOENT";
      throw error;
    }
    this._files.delete(path);
  }

  async readdir(dir) {
    const entries = [];
    for (const path of this._files.keys()) {
      if (path.startsWith(dir + "/")) {
        const relative = path.slice(dir.length + 1);
        const name = relative.split("/")[0];
        if (!entries.includes(name)) {
          entries.push(name);
        }
      }
    }
    return entries;
  }

  async mkdir(path, options) {
    // Directories are implicit in this simple implementation
  }

  async access(path) {
    if (!this._files.has(path)) {
      const error = new Error(`ENOENT: ${path}`);
      error.code = "ENOENT";
      throw error;
    }
  }
}
```

## Testing the Stub Itself

Test your embedded stub to ensure it behaves correctly:

```javascript
describe("StubbedFs", () => {
  it("reads configured files", async () => {
    const fs = new StubbedFs({ "/test.txt": "content" });
    assert.equal(await fs.readFile("/test.txt"), "content");
  });

  it("throws ENOENT for missing files", async () => {
    const fs = new StubbedFs({});
    await assert.rejects(
      () => fs.readFile("/missing.txt"),
      { code: "ENOENT" }
    );
  });

  it("persists writes", async () => {
    const fs = new StubbedFs({});
    await fs.writeFile("/new.txt", "data");
    assert.equal(await fs.readFile("/new.txt"), "data");
  });
});
```

## Avoid Over-Complicating Stubs

Embedded Stubs should stay minimal. If your stub is becoming complex:

1. **Test-drive through the wrapper's public interface** - Don't test the stub directly unless it has non-trivial logic
2. **Implement only what's called** - If your wrapper uses 3 methods, the stub needs only those 3
3. **Add complexity incrementally** - Start simple, add features as tests require them
4. **Consider if you're stubbing too much** - A very complex stub might mean your wrapper is doing too much
