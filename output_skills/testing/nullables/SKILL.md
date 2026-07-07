---
name: nullables
description: Nullables — testing technique alternative to using mocking libraries. Use when writing unit tests, when code touches external I/O or state (HTTP, databases, files, clock, random) anywhere in its dependency chain, when making a system testable, or when tests are slow or flaky.
---

# Nullables: Testing Without Mocks

STARTER_CHARACTER = ⭕️

Nullables are production code with an off switch: classes with external I/O anywhere in their dependencies offer `create()` (real) and `createNull()` (I/O disabled, everything else runs normally). Tests are narrow (focused on one class), sociable (dependencies run for real), and state-based (assert outputs and state, never method calls). Don't use mocking libraries or DI frameworks — Nullables make them unnecessary.

## The cut

Stub at the lowest point — the third-party edge — never your own code:

```
OrderService  →  PaymentClient  →  HttpClient  →  third-party lib
  app code       high-level        low-level       ✂ stubbed when nulled
                 wrapper           wrapper
```

- `PaymentClient` is a high-level wrapper: it abstracts one *service* and speaks domain language.
- `HttpClient` is a low-level wrapper: it abstracts one *technology* and is generic and highly reusable.
- The low-level wrapper holds the fork: `create()` wires the real library (node http, RestTemplate); `createNull()` wires an embedded stub — your code, returning canned data, doing no I/O.
- Everything left of the cut is your code and runs for real in tests.

With mocks, you only mock code you own; with Nullables, you only stub code you *don't* own. Only the bottom layer has a stub — one per technology. Everything above runs real in tests, so a bug anywhere in your code turns tests red. Mocking your own classes breaks that chain: mocked code never runs, and its bugs hide behind green tests.

## Two channels, plus events

Every class that talks to infrastructure anywhere in its dependencies offers the same two factory methods:

```javascript
Clock.create()                            // production: the real system clock
Clock.createNull({ now: "2024-01-01" })   // test: frozen time, no external state
```

Tests interact with a nulled instance through three moves:

- **Reads** — configure what the world answers, as `createNull(...)` parameters in the caller's domain terms: `PaymentClient.createNull({ approved: false })`, `DieRoller.createNull([3, 5, 1])`. A single value repeats forever; a list is consumed in order, then fails fast. An error is just another configured response: `createNull([{ error: "boom" }])`.
- **Writes** — observe what the code sent:

  ```javascript
  const emails = emailer.trackOutput();
  await service.register("a@b.com");
  assert.deepEqual(emails.data, [{ to: "a@b.com", subject: "Welcome" }]);
  ```

  The same tracker can prove a negative — a test where registration is refused asserts `emails.data` is `[]`: no email went out.
- **Pushed events** — fire a simulated incoming event through the same handler path a real event takes: `network.simulateMessage("client-1", "Hello")`.

These ride on two tiny utilities, `OutputListener`/`OutputTracker` and `ConfigurableResponses`. When the codebase lacks them, add them — example implementations in [utilities.md](references/utilities.md).

## Choose the recipe

Route by the dependency you need to control. For a whole service or system ("make this testable"), map its dependency tree first and convert bottom-up — the conversion orders in [migration.md](references/migration.md) apply whether or not mocks exist yet.

- **Already Nullable** (has `createNull()`) → consume it: [consuming-nullables.md](references/consuming-nullables.md)
- **Your class with infrastructure somewhere below** — app code, or a client for one service sitting on a lower wrapper → give it `createNull()` by composing nulled dependencies; it needs no stub and no integration tests: [building-high-level-wrappers.md](references/building-high-level-wrappers.md)
- **Third-party infrastructure with no wrapper yet** — HTTP lib, database driver, filesystem, clock, random. First search the codebase for an existing wrapper (`createNull`, `Stubbed*`); build only if none exists. One wrapper per technology, reused by every service client speaking it; a single-purpose dependency may combine high and low in one wrapper, with the stub still cutting at the third-party edge:
  - the seam is an interface you declare → [building-low-level-wrappers-static.md](references/building-low-level-wrappers-static.md)
  - the seam is duck-typed — any object with the right methods → [building-low-level-wrappers-dynamic.md](references/building-low-level-wrappers-dynamic.md)
- **Value object or config** → no off switch; `createTestInstance()` with safe overridable defaults
- **Pure logic, no infrastructure below** → no Nullables; test directly

Converting mock-based tests, or making an untested system testable → [migration.md](references/migration.md). Structuring an app or feature around this (optional) → [architecture.md](references/architecture.md).

## Rules that hold everywhere

- `create()` wires production, `createNull()` wires nulled — both factories live on the wrapped class, never on the stub. The plain constructor is the test seam: tests use it to inject dependencies they hold handles on.
- Configure and assert as the state of the world the caller wants to control, in the caller's language: `PaymentClient.createNull({ approved: false })`, not HTTP statuses. Each layer decomposes its configuration into its dependency's language.
- Nulled defaults are loud and absurd — `"Nulled HttpClient default body"`, status 503, port 42 — so accidental reliance on them fails visibly instead of passing by luck.
- Constructors do no work. Connecting, starting, listening happen in explicit methods, so instantiating the whole dependency tree is always safe.
- One test helper owns construction and wiring (signature shielding): optional named parameters with `IRRELEVANT_*` defaults, returning a bag of results and trackers. A signature change hits one place.
- Stay in consumer scope: assert that the request went out and the answer got used. The dependency's own tests cover its behavior.
- Wrappers validate external responses hard and throw detailed errors on anything unexpected (paranoic telemetry); callers decide how to recover. Test error paths as thoroughly as happy paths — they cost the same now.
- Only the lowest wrapper gets narrow integration tests against the real system. They document the third-party behavior the stub must match — that pairing keeps the stub honest.

## Anti-patterns

- Importing a mocking library (sinon, jest.mock, Mockito) — replaces exactly what Nullables provide and breaks the sociable chain.
- Stubbing your own class instead of the third-party edge.
- `createNull()` parameters that leak the layer below — HTTP details on a domain client.
- Stubs in test files — the embedded stub is production code and lives with its wrapper.
- A stub that reimplements the real system — stubs return canned data; needing real logic means you're cutting at the wrong level.
- Computing an assertion's expected value with the code under test — the test then verifies nothing.
