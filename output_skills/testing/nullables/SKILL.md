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

## Procedure

Start from the code you need to test. For a whole system, pick one class and repeat; conversion order across many classes is in [migration.md](references/migration.md).

1. List the dependencies of the class under test. Classify each one you need to control:
   - Pure logic, nothing external below → test directly, nothing to null.
   - Value object or config → `createTestInstance()` with safe overridable defaults. If it holds an infrastructure object, default it to the nulled version.
   - Already has `createNull()` → go to step 4.
   - Touches infrastructure below but has no `createNull()` → step 2.
2. Follow that dependency's chain down until you reach code you don't own — a third-party library doing I/O. That is the edge.
   - The codebase already has a wrapper for this technology (search `createNull`, `Stubbed`, `infrastructure/`) → reuse it, go to step 3.
   - No wrapper → build one: [building-low-level-wrappers-static.md](references/building-low-level-wrappers-static.md) when the seam is an interface you declare, [building-low-level-wrappers-dynamic.md](references/building-low-level-wrappers-dynamic.md) when any object with the right methods will do. One wrapper per technology.
3. Walk back up the chain. Give each class on the way `create()` and `createNull()`, composing its nulled dependencies: [building-high-level-wrappers.md](references/building-high-level-wrappers.md). At each layer, keep the configuration in that layer's own language and decompose it downward — this is where abstractions leak if you rush.
4. Write the tests: [consuming-nullables.md](references/consuming-nullables.md).

Converting a mock-based suite → [migration.md](references/migration.md). Improving existing nullables → walk their layers and check each against the rules below, plus: the stub sits at the true edge, one stub per technology (no duplicates), no leftover throwaway stubs, each layer's `createNull()` speaks that layer's language. Structuring a new app around this (optional) → [architecture.md](references/architecture.md).

## Rules at every layer

- `create()` wires production, `createNull()` wires nulled — both factories live on the wrapped class, never on the stub. The plain constructor is the test seam: tests use it to inject dependencies they hold handles on.
- Configure and assert as the state of the world the caller wants to control, in the caller's language: `PaymentClient.createNull({ approved: false })`, not HTTP statuses. Each layer decomposes its configuration into its dependency's language.
- Bare `createNull()` always works: every parameter has a safe default, so one call nulls the whole dependency chain from the top (parameterless instantiation). Nulling is a safe operation, like a null object.
- The data those defaults return is loud and absurd — `"Nulled HttpClient default body"`, status 503, port 42. Nothing breaks on it, but a test that accidentally depends on it sees obviously fake values instead of passing by luck. Failing fast is reserved for overrunning explicit configuration: an exhausted response list throws "No more responses configured…".
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
