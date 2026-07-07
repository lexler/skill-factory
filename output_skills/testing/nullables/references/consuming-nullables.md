# Consuming Nullables

Testing code whose dependencies already have `createNull()`.

## Contents

- Test anatomy
- Configuring reads
- Tracking writes
- Signature shielding
- Error paths
- Time
- Simulating incoming events
- Assertion discipline

## Test anatomy

Instantiate the class under test with its **constructor**, injecting nulled dependencies you hold handles on. `createNull()` on the class under test is for *its* consumers — it builds default children you can't reach from the test.

```javascript
it("declines checkout when payment is refused", async () => {
  const payments = PaymentClient.createNull({ approved: false });
  const paymentRequests = payments.trackRequests();
  const log = Log.createNull();
  const logOutput = log.trackOutput();
  const service = new CheckoutService(payments, log);   // constructor = test seam

  const result = await service.checkout(cart);

  assert.equal(result.status, "declined");
  assert.deepEqual(logOutput.data, [{ alert: "monitor", message: "payment refused" }]);
});
```

Real `CheckoutService` code runs, including its real collaborators — only external I/O is switched off.

## Configuring reads

`createNull(...)` parameters state what the world answers, in the caller's domain terms:

```javascript
LoginClient.createNull({ email: "user@example.com", verified: true });     // domain terms
DieRoller.createNull([3, 5, 1]);                                           // sequence
TranslationClient.createNull([{ response: "hola" }, { error: "boom" }]);   // per-call variety
```

Semantics to rely on:

- A single value repeats forever.
- A list is consumed in order, then the Nullable throws ("No more responses configured…") — a test that consumes too much fails fast instead of passing on stale data.
- An error is just another configured response: `createNull([{ error: "my_error" }])`.

Pass every parameter the test cares about; never let an assertion depend on a default.

In languages without named optional parameters, configuration comes as an options builder or overloaded factories:

```java
GameService service = GameService.createNull(
    new NulledResponses()
        .withDieRolls(1, 2, 3, 4, 5)
        .withGame(game));
```

## Tracking writes

`trackX()` returns a tracker whose `data` is the writes recorded so far, as domain-level objects:

```javascript
const emails = emailer.trackOutput();
await service.completeOrder("123");
assert.deepEqual(emails.data, [{ to: "customer@example.com", subject: "Order Confirmed" }]);
```

- Order is preserved — sequence assertions come free: `writes.data.map(w => w.id)`.
- **Prove a negative**: assert `[]` to show nothing was sent — trivially, unlike with mocks.

```javascript
assert.deepEqual(translationRequests.data, [], "shouldn't call translation service");
```

- `clear()` returns-and-resets — useful between phases of a longer test. `stop()` unsubscribes.
- Start tracking before the act step; trackers only see what happens after they're created.
- Tracker methods are named after the writes they record — `trackRequests()`, `trackSaves()`; `trackOutput()` is the generic fallback.

## Signature shielding

One helper owns construction and wiring; every test calls it. When a constructor or signature changes, one place changes.

```javascript
it("logs warning when form field not found", async () => {
  const { response, logOutput, translationRequests } = await postAsync({ body: "" });
  // assertions...
});

async function postAsync({
  body = `text=${IRRELEVANT_INPUT}`,
  translationServicePort = IRRELEVANT_PORT,
  translationResponse = "irrelevant translation",
  translationError = undefined,
} = {}) {
  const translationClient = TranslationClient.createNull([
    { response: translationResponse, error: translationError },
  ]);
  const translationRequests = translationClient.trackRequests();
  const log = Log.createNull();
  const logOutput = log.trackOutput();
  const controller = new TranslationController(translationClient, Clock.createNull());
  const request = HttpServerRequest.createNull({ body });
  const config = WwwConfig.createTestInstance({ log, translationServicePort });

  const response = await controller.postAsync(request, config);
  return { response, logOutput, translationRequests };
}
```

- Optional named parameters, defaulting to `IRRELEVANT_*` constants — the name signals "this test doesn't care".
- The helper returns a bag; each test destructures what it needs, so the bag can grow without breaking existing tests.
- Prefer helpers over `beforeEach` — setup stays visible at the call site.
- Some duplication between similar tests is fine when it makes them easier to read.
- `createTestInstance()` on a value object defaults any boundary-crosser it holds to the nulled version — `WwwConfig` above defaults its `log` to `Log.createNull()`.

## Error paths

Errors cost the same as happy paths — one configuration argument:

```javascript
const { response, logOutput } = await postAsync({ translationError: "my_error" });

assert.deepEqual(response, translationView.page("Translation service failed"), "should render error page");
assert.equal(logOutput.data[0].alert, "emergency", "should log emergency");
```

Test them as thoroughly as happy paths: failures, invalid responses, and (for async I/O) hangs and cancellation.

## Time

A nulled Clock freezes time at a configured instant and moves only when told:

```javascript
const clock = Clock.createNull({ now: "2024-01-01T00:00:00Z" });
await clock.advanceNulledClockAsync(60_000);
```

Method names vary by codebase. A real clock throws on advance calls — time travel is nulled-only.

Timeout tests combine a hanging dependency with time travel — act *without awaiting*, advance, then await:

```javascript
const translationClient = TranslationClient.createNull([{ hang: true }]);
const { responsePromise, clock } = post({ translationHang: true });   // non-awaiting helper variant

await clock.advanceNulledClockUntilTimersExpireAsync();

const response = await responsePromise;
assert.deepEqual(response, translationView.page("Translation service timed out"));
```

Where possible, prefer passing time in as a value: a clock for *actions* ("what time is it now?"), a plain parameter for *questions* (`isOverdue(book, today)`). Logic that receives time as data needs no Nullable at all.

## Simulating incoming events

For dependencies that push data (sockets, queues, UI events), `simulateX()` fires a simulated incoming event through the same handler path a real event takes:

```javascript
const network = Network.createNull();
const sent = network.trackMessages();
const server = new ChatServer(network);
await server.startAsync();

network.simulateConnection("client-1");
network.simulateConnection("client-2");
network.simulateMessage("client-1", "Hello!");

assert.deepEqual(sent.data, [{ to: "client-2", message: "Hello!" }]);
```

## Assertion discipline

- Assert whole domain objects with deep equality; label each assertion when a test has several (`"should log a warning"`).
- Unstable fields (timestamps, generated IDs): configure the source instead — nulled Clock, nulled UuidGenerator. When the field comes from outside your control, remove it before comparing and say why:

```javascript
delete response.headers.date;   // unstable, and not important to this test
assert.deepEqual(response, expected);
```

- Assert against a collaborator's own output rather than hand-typing its format: `assert.deepEqual(response, translationView.page("my_response"))` — the test isn't about the view's HTML. But never *recompute* the expected value with the code under test; that verifies nothing. Use this sparingly, only when the collaborator's format is genuinely irrelevant to the test.
- Stay in consumer scope: assert that the right request went out and that whatever came back got used. The dependency's behavior (does the translator translate correctly?) belongs to the dependency's own tests.
- One real bug turning several tests red is the sociable chain working, not a smell — the overlap is what replaces end-to-end tests. The failing set points at the shared code.
- Keep one or two end-to-end smoke tests as a safety net. When a smoke test catches something, the narrow suite has a gap — fill it with narrow tests rather than growing the smoke suite.
