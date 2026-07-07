# Building Low-Level Wrappers — Duck-Typed Seam

The bottom layer: a wrapper for one communication *technology* (HTTP, database driver, filesystem, message bus, clock, random), made Nullable by stubbing the third-party library it calls. This is the only place two special things live: narrow integration tests against the real system, and an embedded stub. Duck typing keeps the seam simple: the stub is any object with the right method names. Examples are JavaScript.

## Contents

- Find the edge
- Adapting to your language
- Design the public interface
- Narrow integration tests first
- Wire the nullability seam
- Grow the stub by instrumentation
- The response ladder
- Match real behavior where it counts
- Output tracking
- Minimal example

## Find the edge

The stub cuts at code you **don't own** — the third-party library — never at your own class. Mocks mock code you own; Nullables stub only code you don't. That way your wrapper's real logic runs in every test, nulled or not, and a change to it is caught, not hidden.

Go all the way down: wrap `System.currentTimeMillis` / `Date`, not a convenience layer above it; wrap the HTTP library, not your service client. One low-level wrapper per technology — every service client speaking HTTP reuses the same `HttpClient`. A single-purpose dependency may get one combined high+low wrapper; the stub still cuts at the third-party edge.

Before building, search the codebase for an existing wrapper: `grep -r "createNull\|Stubbed" src/` and look for an `infrastructure/` directory. Building a duplicate wrapper for a technology is the expensive mistake here.

## Adapting to your language

The examples here are JavaScript; the pattern is not.

- Follow the codebase's naming idiom for the two factories (`create`/`createNull` shown here), and keep both on the wrapper.
- "Throw a detailed error" means the language's failure idiom — exceptions, returned errors, result types. The detail and the failing loudly are the point, not the mechanism.
- Keep the stub invisible to callers with the language's privacy unit — module-local class, unexported name.

## Design the public interface

From callers' needs, not the third-party shape: generic protocol verbs, plain data in and out. No third-party objects escape — consume them inside and reduce to plain values:

```javascript
// requestAsync({ url, method, headers, body }) → { status, headers, body }
```

## Narrow integration tests first

The wrapper abstracts a communication protocol, so test the protocol for real — against a real system the tests themselves start and stop (localhost server, temp directory, local database). The best tests are self-sufficient: nothing to launch by hand.

**Explore before you TDD.** Most of the work is figuring out the third-party API. Write one growing test with `console.log` and no assertions: start the server, make a request, complete the exchange, dump what the server saw and what the client got. Then convert:

1. Replace logs with `assert.deepEqual(response, { status, headers, body })`. Delete unstable fields first, with a comment: `delete response.headers.date; // unstable, unimportant`.
2. Factor the server into a **SpyServer** — the integration-test mirror of output tracking and configurable responses:
   - `startAsync()`/`stopAsync()` in `before()`/`after()` (started once), `reset()` in `beforeEach()`
   - `lastRequest` → `{ method, path, headers, body }` or `null` (strip noise headers: connection, content-length, host)
   - `setResponse({ status, headers, body })`, defaulting on reset to a loud `{ status: 501, body: "SpyServer response not specified" }`
3. Split into focused tests: `"performs request"` (what the server saw), `"returns response"` (what the client got), `"headers and body are optional"`.
4. Same technique for edge cases: connection refused (request to a closed port, assert the error), cancellation, and fail-fast guards for third-party footguns (e.g. throw on GET-with-body because the library silently drops it).

These tests do double duty: they verify the protocol works, and they *document the real library's behavior* — lowercased header names, auto-added headers — which the stub must later match.

## Wire the nullability seam

Start with the test that proves the negative:

```javascript
it("doesn't talk to network", async () => {
  const client = HttpClient.createNull();
  await requestAsync({ client });
  assert.equal(spyServer.lastRequest, null);
});
```

Then the seam: the constructor stores the library; `create()` injects the real one; `createNull()` injects an empty stub. Comment the failing test out while rewiring call sites, uncomment to finish.

```javascript
export class HttpClient {
  static create() {
    return new HttpClient(http);                       // real node:http
  }
  static createNull(responses) {
    return new HttpClient(new StubbedHttp(responses)); // embedded stub
  }
  constructor(http) {
    this._http = http;
  }
}
```

Duck typing means the stub is just a class with matching method names — implement only what your wrapper actually calls, nothing more. In TypeScript, declare a minimal interface (`interface NodeHttp { request(...): ... }`) and have both the real module and the stub satisfy it.

## Grow the stub by instrumentation

Don't guess the third-party protocol — record it:

1. Put numbered `console.log`s in *your wrapper* around the third-party calls (`1 BEFORE REQUEST`, `2 INSIDE RESPONSE EVENT`, `3 INSIDE DATA EVENT`…).
2. Run a real-path test with `it.only`; write down the sequence.
3. Run the nulled test; the first missing log or crash is the next stub increment.
4. Implement as little as possible; repeat until the sequences match; delete the logs.

This diff-the-logs technique transfers to any library — database drivers, SDKs, sockets.

Preserve asynchrony: the real library emits events and resolves promises asynchronously, so the stub must too — wrap emissions in `setImmediate()` (or `setTimeout(0)`), or code that works nulled will deadlock or race for real.

```javascript
class StubbedRequest extends EventEmitter {
  end() {                                   // real end() sends the request; nulled must not
    setImmediate(() => this.emit("response", new StubbedResponse(this._response)));
  }
}
class StubbedResponse extends EventEmitter {
  constructor(response) {
    super();
    this._response = response;
    setImmediate(() => {
      this.emit("data", this._response.body);
      if (!this._response.hang) this.emit("end");   // hang = never finish
    });
  }
}
```

## The response ladder

Grow `createNull()`'s configuration in this order, one test each:

1. **Loud default** — unconfigured Nullable returns an unmistakably fake constant: `{ status: 503, body: "Nulled HttpClient default body" }`. Accidental reliance fails visibly.
2. **Single configurable response** — `createNull({ status, headers, body })`.
3. **Per-endpoint** — `createNull({ "/a": {...}, "/b": {...} })`; high-level wrappers usually talk to several endpoints.
4. **Partial configuration** — unspecified fields get per-field defaults (`501`, `{}`, `""`).
5. **Repetition semantics** — a single configured response repeats forever; an array is consumed in order; exhaustion throws an informative error naming the endpoint. This is exactly `ConfigurableResponses` (see utilities.md) — use it rather than hand-rolling.
6. **Hang** — `{ hang: true }`: never emit `end` / never resolve, so timeout and cancellation logic upstream can be tested.

## Match real behavior where it counts

Stubs return hardcoded data; prefer that over reimplementing real behavior (a fake) — needing real logic in the stub usually means you're cutting at the wrong level. But where the stub *does* emulate behavior, it must match the real library exactly, because everything above tests against the nulled instance. Example: node's `http` lowercases header names, so the stub must too. Your narrow integration tests are the record of what "exactly" means; when the stub needs a behavior they don't cover, extend them first.

## Output tracking

Technically separate from nullability, usually built at the same time: emit in the shared request path (works real and nulled), return a tracker from `trackRequests()`. See utilities.md for `OutputListener`.

## Minimal example

A fetch-based HTTP wrapper — seam, stub, defaults, and normalization on one screen (illustrates the shape; adapt to your library). It covers ladder rungs 1–3 with single responses only; for lists and repetition, wire the endpoint values through `ConfigurableResponses`:

```javascript
import { OutputListener } from "./output_listener.js";

export class HttpClient {
  static create() {
    return new HttpClient(globalThis);                    // real fetch
  }
  static createNull(endpoints) {
    return new HttpClient(new StubbedGlobals(endpoints)); // embedded stub
  }
  constructor(globals) {
    this._globals = globals;
    this._listener = new OutputListener();
  }

  async requestAsync({ url, method, headers = {}, body = "" }) {
    method = method.toUpperCase();
    headers = normalizeHeaders(headers);                  // matches real fetch behavior
    this._listener.emit({ url, method, headers, body });  // output tracking, both modes

    const response = await this._globals.fetch(url, { method, headers, body });
    return {
      status: response.status,
      headers: Object.fromEntries(response.headers.entries()),
      body: await response.text(),
    };
  }

  trackRequests() {
    return this._listener.trackOutput();
  }
}

class StubbedGlobals {
  constructor(endpoints) {
    this._endpoints = endpoints;
  }
  async fetch(url) {
    const configured = this._endpoints?.[url] ?? {};
    // compact: collapses the loud whole-client default and the per-field defaults into one tier
    const response = new Response(configured.body ?? "Nulled HttpClient default body", {
      status: configured.status ?? 503,
      headers: configured.headers ?? { nulledhttpclient: "default header" },
    });
    return new Promise((resolve) => setTimeout(() => resolve(response), 0));  // async fidelity
  }
}
```
