# Output Tracking

Output Tracking observes what your code writes to external systems without performing real I/O. It answers: "What did my code do?" rather than "Did my code call this method?"

## Contents

- [The OutputListener Utility](#the-outputlistener-utility)
- [Using OutputListener in Wrappers](#using-outputlistener-in-wrappers)
- [Usage in Tests](#usage-in-tests)
- [Track at the Right Level](#track-at-the-right-level)
- [Multiple Trackers](#multiple-trackers)
- [Testing Sequences](#testing-sequences)
- [Combining with Configurable Responses](#combining-with-configurable-responses)

## The OutputListener Utility

Extract tracking logic into a reusable utility (recommended for all projects):

```javascript
import { EventEmitter } from "node:events";

export class OutputListener {
  static create() {
    return new OutputListener();
  }

  constructor() {
    this._emitter = new EventEmitter();
  }

  emit(data) {
    this._emitter.emit("output", data);
  }

  trackOutput() {
    return new OutputTracker(this._emitter);
  }
}

class OutputTracker {
  constructor(emitter) {
    this._emitter = emitter;
    this._data = [];
    this._listener = (item) => this._data.push(item);
    this._emitter.on("output", this._listener);
  }

  get data() {
    return this._data;
  }

  clear() {
    const result = [...this._data];
    this._data.length = 0;
    return result;
  }

  stop() {
    this._emitter.off("output", this._listener);
  }
}
```

## Using OutputListener in Wrappers

```javascript
import { OutputListener } from "./output_listener.js";

class Logger {
  static create() {
    return new Logger(process.stdout);
  }

  static createNull() {
    return new Logger({ write() {} });
  }

  constructor(stdout) {
    this._stdout = stdout;
    this._listener = new OutputListener();
  }

  info(message) {
    const entry = { level: "info", message, timestamp: Date.now() };
    this._stdout.write(JSON.stringify(entry) + "\n");
    this._listener.emit(entry);
  }

  error(message, error) {
    const entry = { level: "error", message, error: error?.message };
    this._stdout.write(JSON.stringify(entry) + "\n");
    this._listener.emit(entry);
  }

  trackOutput() {
    return this._listener.trackOutput();
  }
}
```

## Usage in Tests

```javascript
it("logs successful operations", async () => {
  const logger = Logger.createNull();
  const output = logger.trackOutput();

  const service = new PaymentService(logger);
  await service.processPayment({ amount: 100 });

  assert.deepEqual(output.data, [
    { level: "info", message: "Processing payment", timestamp: expect.any(Number) },
    { level: "info", message: "Payment successful", timestamp: expect.any(Number) }
  ]);
});

it("logs errors on failure", async () => {
  const logger = Logger.createNull();
  const output = logger.trackOutput();
  const paymentGateway = PaymentGateway.createNull({ error: "Card declined" });

  const service = new PaymentService(logger, paymentGateway);
  await service.processPayment({ amount: 100 });

  assert.deepEqual(output.data[1], {
    level: "error",
    message: "Payment failed",
    error: "Card declined"
  });
});
```

## Track at the Right Level

Track behavioral-level information, not implementation details:

```javascript
// BAD: Tracking raw bytes
this._emitter.emit("output", buffer);

// GOOD: Tracking meaningful data
this._emitter.emit("output", {
  type: "http_request",
  method: "POST",
  path: "/api/users",
  body: { name: "Alice" }
});
```

## Multiple Trackers

Sometimes you need separate trackers for different concerns:

```javascript
import { OutputListener } from "./output_listener.js";

class HttpClient {
  constructor(http) {
    this._http = http;
    this._requestListener = new OutputListener();
    this._responseListener = new OutputListener();
  }

  async request(options) {
    this._requestListener.emit(options);
    const response = await this._http.request(options);
    this._responseListener.emit(response);
    return response;
  }

  trackRequests() {
    return this._requestListener.trackOutput();
  }

  trackResponses() {
    return this._responseListener.trackOutput();
  }
}
```

## Testing Sequences

Output tracking naturally captures sequences:

```javascript
it("processes items in order", async () => {
  const db = Database.createNull();
  const writes = db.trackWrites();

  await batchProcessor.process(["a", "b", "c"]);

  assert.deepEqual(writes.data.map(w => w.id), ["a", "b", "c"]);
});
```

## Combining with Configurable Responses

Often you track outputs while also configuring inputs:

```javascript
it("retries on failure then succeeds", async () => {
  const api = ApiClient.createNull([
    { error: "timeout" },
    { error: "timeout" },
    { response: { success: true } }
  ]);
  const requests = api.trackRequests();

  const result = await service.fetchWithRetry();

  assert.equal(requests.data.length, 3);  // Verify retry count
  assert.deepEqual(result, { success: true });
});
```
