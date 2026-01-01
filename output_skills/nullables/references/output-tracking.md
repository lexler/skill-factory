# Output Tracking

Output Tracking observes what your code writes to external systems without performing real I/O. It answers: "What did my code do?" rather than "Did my code call this method?"

## Basic Pattern

```javascript
import { EventEmitter } from "node:events";

class Logger {
  constructor(stdout) {
    this._stdout = stdout;
    this._emitter = new EventEmitter();
  }

  static create() {
    return new Logger(process.stdout);
  }

  static createNull() {
    return new Logger({ write() {} });  // Discards output
  }

  info(message) {
    const entry = { level: "info", message, timestamp: Date.now() };
    this._stdout.write(JSON.stringify(entry) + "\n");
    this._emitter.emit("output", entry);
  }

  error(message, error) {
    const entry = { level: "error", message, error: error?.message };
    this._stdout.write(JSON.stringify(entry) + "\n");
    this._emitter.emit("output", entry);
  }

  trackOutput() {
    const data = [];
    const listener = (entry) => data.push(entry);
    this._emitter.on("output", listener);
    return {
      data,
      clear: () => { data.length = 0; },
      stop: () => { this._emitter.off("output", listener); }
    };
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
class HttpClient {
  constructor(http) {
    this._http = http;
    this._requestEmitter = new EventEmitter();
    this._responseEmitter = new EventEmitter();
  }

  async request(options) {
    this._requestEmitter.emit("output", options);
    const response = await this._http.request(options);
    this._responseEmitter.emit("output", response);
    return response;
  }

  trackRequests() {
    return this._createTracker(this._requestEmitter);
  }

  trackResponses() {
    return this._createTracker(this._responseEmitter);
  }

  _createTracker(emitter) {
    const data = [];
    const listener = (item) => data.push(item);
    emitter.on("output", listener);
    return {
      data,
      clear: () => { data.length = 0; },
      stop: () => { emitter.off("output", listener); }
    };
  }
}
```

## Reusable OutputTracker

Extract the tracking logic into a reusable class:

```javascript
export class OutputTracker {
  static create(emitter, eventName = "output") {
    return new OutputTracker(emitter, eventName);
  }

  constructor(emitter, eventName) {
    this._emitter = emitter;
    this._eventName = eventName;
    this._data = [];
    this._listener = (item) => this._data.push(item);
    this._emitter.on(this._eventName, this._listener);
  }

  get data() {
    return this._data;
  }

  clear() {
    this._data.length = 0;
  }

  stop() {
    this._emitter.off(this._eventName, this._listener);
  }
}
```

Usage:

```javascript
class NetworkClient {
  constructor(socket) {
    this._socket = socket;
    this._emitter = new EventEmitter();
  }

  send(message) {
    this._socket.write(JSON.stringify(message));
    this._emitter.emit("sent", message);
  }

  trackSentMessages() {
    return OutputTracker.create(this._emitter, "sent");
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
