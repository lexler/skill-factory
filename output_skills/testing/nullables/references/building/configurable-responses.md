# Configurable Responses

Configurable Responses control what your Nullable returns. They let tests specify external system behavior at the caller's abstraction level.

## Contents

- [Basic Patterns](#basic-patterns)
- [Implementation: ConfigurableResponses Helper](#implementation-configurableresponses-helper)
- [Using ConfigurableResponses in a Wrapper](#using-configurableresponses-in-a-wrapper)
- [Abstraction Level](#abstraction-level)
- [Error Simulation](#error-simulation)
- [Hanging/Timeout Simulation](#hangingtimeout-simulation)
- [Multiple Response Types](#multiple-response-types)

## Basic Patterns

### Single Response (Repeats Forever)

```javascript
const clock = Clock.createNull("2020-01-01T00:00:00Z");

clock.now();  // "2020-01-01T00:00:00Z"
clock.now();  // "2020-01-01T00:00:00Z" (same)
clock.now();  // "2020-01-01T00:00:00Z" (same)
```

### Response Sequence (Exhaustible)

```javascript
const idGenerator = IdGenerator.createNull(["id-1", "id-2", "id-3"]);

idGenerator.next();  // "id-1"
idGenerator.next();  // "id-2"
idGenerator.next();  // "id-3"
idGenerator.next();  // throws Error("No more configured responses")
```

### Named Responses (For Different Endpoints)

```javascript
const http = HttpClient.createNull({
  "/users": { status: 200, body: '[{"name":"Alice"}]' },
  "/orders": { status: 200, body: '[]' }
});

await http.get("/users");   // Returns users response
await http.get("/orders");  // Returns orders response
```

## Implementation: ConfigurableResponses Helper

```javascript
export class ConfigurableResponses {
  static create(responses, name = "ConfigurableResponses") {
    if (!Array.isArray(responses)) {
      return new RepeatingResponse(responses);
    }
    return new SequenceResponse(responses, name);
  }

  static mapObject(responsesByKey, name) {
    const result = {};
    for (const [key, responses] of Object.entries(responsesByKey)) {
      result[key] = ConfigurableResponses.create(responses, `${name}[${key}]`);
    }
    return result;
  }
}

class RepeatingResponse {
  constructor(response) {
    this._response = response;
  }

  next() {
    return this._response;
  }
}

class SequenceResponse {
  constructor(responses, name) {
    this._responses = [...responses];
    this._name = name;
    this._index = 0;
  }

  next() {
    if (this._index >= this._responses.length) {
      throw new Error(`${this._name}: No more responses (exhausted ${this._responses.length})`);
    }
    return this._responses[this._index++];
  }
}
```

## Using ConfigurableResponses in a Wrapper

```javascript
class DieRoller {
  static create() {
    return new DieRoller(Math.random);
  }

  static createNull(rolls = [1]) {
    const responses = ConfigurableResponses.create(rolls, "DieRoller");
    return new DieRoller(() => (responses.next() - 1) / 6);
  }

  constructor(randomFn) {
    this._random = randomFn;
  }

  roll() {
    return Math.floor(this._random() * 6) + 1;
  }
}
```

Test:

```javascript
it("returns configured rolls", () => {
  const die = DieRoller.createNull([3, 5, 1]);

  assert.equal(die.roll(), 3);
  assert.equal(die.roll(), 5);
  assert.equal(die.roll(), 1);
});
```

## Abstraction Level

Define responses at the caller's abstraction level, not the implementation level:

```javascript
// BAD: HTTP-level details leak to high-level wrapper
LoginClient.createNull({
  response: {
    status: 200,
    headers: { "content-type": "application/json" },
    body: JSON.stringify({ email: "user@test.com", email_verified: true })
  }
});

// GOOD: Domain-level abstraction
LoginClient.createNull({
  email: "user@test.com",
  verified: true
});
```

Implementation translates internally:

```javascript
class LoginClient {
  static createNull({ email = "null@test.com", verified = true } = {}) {
    // Translate to HTTP response internally
    const httpResponse = {
      status: 200,
      body: JSON.stringify({ email, email_verified: verified })
    };

    return new LoginClient(
      HttpClient.createNull({ "/userinfo": httpResponse })
    );
  }
}
```

## Error Simulation

Include error cases in your configurable responses:

```javascript
class ApiClient {
  static createNull(responses = [{}]) {
    return new ApiClient(new StubbedHttp(responses));
  }
}

// Usage
const api = ApiClient.createNull([
  { status: 200, body: "success" },     // First call succeeds
  { status: 500, body: "server error" }, // Second fails
  { error: "ECONNREFUSED" }              // Third: network error
]);
```

## Hanging/Timeout Simulation

For async operations, support simulating slow or hanging requests:

```javascript
class HttpClient {
  static createNull(responses) {
    return new HttpClient(new StubbedHttp(responses));
  }
}

class StubbedHttp {
  constructor(responses) {
    this._responses = ConfigurableResponses.create(responses, "HTTP");
  }

  request(options) {
    const response = this._responses.next();

    if (response.hang) {
      // Return a promise that never resolves
      return { promise: new Promise(() => {}), cancel: () => {} };
    }

    return {
      promise: Promise.resolve(response),
      cancel: () => {}
    };
  }
}
```

Test timeout handling:

```javascript
it("cancels request on timeout", async () => {
  const http = HttpClient.createNull([{ hang: true }]);

  const { promise, cancel } = http.request("/slow");
  setTimeout(cancel, 100);

  await assert.rejects(promise, { message: "Request cancelled" });
});
```

## Multiple Response Types

When a wrapper has different response types, use separate parameters:

```javascript
class Database {
  static createNull({
    queryResults = [],
    insertIds = [1],
    errors = []
  } = {}) {
    return new Database(new StubbedDb(queryResults, insertIds, errors));
  }
}

// Usage
const db = Database.createNull({
  queryResults: [
    [{ id: 1, name: "Alice" }],
    []  // Empty result for second query
  ],
  insertIds: [42, 43]
});
```
