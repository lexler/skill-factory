# Building High-Level Wrappers and Nullable App Code

Giving `createNull()` to code you own: clients for one specific service (sitting on a low-level wrapper), and app code composing nullable dependencies. These need no stub and no integration tests — that machinery exists only at the bottom layer.

## Contents

- The shape
- Recipe: a service client
- Decomposing configurable responses
- App-level composition
- Static-typing variants

## The shape

```
PaymentClient.createNull({ approved: false })
      │  translates domain config → transport config
      ▼
HttpClient.createNull({ "/v1/charges": { status: 402, body: ... } })
      │  already Nullable — has the only stub
      ▼
(no network)
```

A high-level wrapper's `createNull()` is real production code wired to a nulled dependency, plus a translation function. Everything it does — building requests, parsing responses, validating — runs for real in every test above it. This is Fake It Once You Make It: confirm the real service's behavior once (call it manually, or develop against `create()` until confident), encode what you learned into the translation, then test against the nulled instance.

## Recipe: a service client

Build it fully working and tested *before* it's Nullable — nullability arrives last, as one more feature.

**1. Constructor takes the lower wrapper; `create()` wires the real one.**

```javascript
export class TranslationClient {
  static create() {
    return new TranslationClient(HttpClient.create());
  }
  constructor(httpClient) {
    this._httpClient = httpClient;
    this._listener = new OutputListener();
  }
}
```

**2. Design the interface from what callers need, not what the service exposes.** A subscription service's entire API might collapse to `isSubscribed(userId)`. Accept and return domain values; no HTTP shapes escape.

**3. Test-drive the real logic against the nulled dependency.** Assert the exact outgoing request (via the lower wrapper's tracker) and the parsed return value:

```javascript
it("makes request", async () => {
  const httpClient = HttpClient.createNull();
  const httpRequests = httpClient.trackRequests();
  const client = new TranslationClient(httpClient);

  await client.translateAsync(9999, "text_to_translate");

  assert.deepEqual(httpRequests.data, [{
    host: HOST, port: 9999, method: "post", path: "/translate",
    headers: { "content-type": "application/json" },
    body: JSON.stringify({ text: "text_to_translate" }),
  }]);
});

it("parses response", async () => {
  const httpClient = HttpClient.createNull({
    "/translate": [{ status: 200, body: JSON.stringify({ translated: "my_response" }) }],
  });
  const client = new TranslationClient(httpClient);

  const response = await client.translateAsync(9999, "some text");
  assert.equal(response, "my_response");
});
```

**4. Track outputs at the domain level.** Emit in the request path — shared by real and nulled modes — with the data callers care about, not transport details:

```javascript
async translateAsync(port, text) {
  this._listener.emit({ port, text });        // domain-level, not HTTP-level
  const response = await this._httpClient.requestAsync({ /* ... */ });
  // ...
}
trackRequests() {
  return this._listener.trackOutput();
}
```

**5. Validate hard (paranoic telemetry).** External systems change and fail at will. Check status, parse the body, check its shape; throw one detailed, multi-line error on anything unexpected — the caller has the context to recover:

```javascript
if (response.status !== 200) {
  throwError("Unexpected status from translation service", port, response);
}
// also: empty body, unparseable body, wrong shape, extra fields you choose to tolerate
```

**6. Add `createNull()` last — by decomposition** (next section). Then test the nulled instance itself: default response, configured responses, configured errors.

## Decomposing configurable responses

Design the options as the *state of the outside world* callers want to control — "which books are out", "the account is unverified" — not as scripted method return values; scripting returns is a mock in disguise. When there's no meaningful world-state to model (a die roller), specifying responses directly is fine: use judgment, default to state. Give each concern its own named parameter with a default, so a test states only what it cares about and stays silent on the rest.

`createNull()` accepts options in the *caller's* language and translates them into the *dependency's* language:

```javascript
static createNull(options = [{}]) {
  const httpResponses = options.map((response) => nulledHttpResponse(response));
  const httpClient = HttpClient.createNull({ [TRANSLATE_ENDPOINT]: httpResponses });
  return new TranslationClient(httpClient);
}

function nulledHttpResponse({ response = "Nulled TranslationClient response", error, hang = false } = {}) {
  if (error !== undefined) return { status: 500, headers: {}, body: error, hang };
  return {
    status: 200,
    headers: { "content-type": "application/json" },
    body: JSON.stringify({ translated: response }),
    hang,
  };
}
```

Callers say `{ response: "x" }`, `{ error: "boom" }`, `{ hang: true }`; the translation produces the HTTP responses the real service would return. Error configs deliberately reuse the telemetry path built in step 5 — a configured error exercises the same parsing and throwing as a real one.

## App-level composition

App code with nullable dependencies gets `createNull()` the same way — build nulled children in one call. No translation function needed when there's nothing to decompose:

```javascript
static createNull() {
  return new TranslationController(TranslationClient.createNull(), Clock.createNull());
}
```

This is for *consumers* of the class (one-call nulling from above). The class's own tests keep using the constructor with dependencies they hold handles on.

## Static-typing variants

Without named optional parameters, use overloaded factories, varargs, or an options builder:

```java
public static AverageScoreFetcher createNull() {
    return createNull(Collections.emptyMap());
}

public static AverageScoreFetcher createNull(Map<ScoreCategory, Double> map) {
    return new AverageScoreFetcher(JsonHttpClient.createNull(nulledHttpResponses(map)));
}

private static Map<String, Object> nulledHttpResponses(Map<ScoreCategory, Double> fetcherResponses) {
    // decompose: domain map → endpoint URL → response object the real API would return
}
```

Named factories make meaningful states discoverable:

```java
GameDatabase.createNull();                 // sensible default game
GameDatabase.createNull(snapshot);         // configured
GameDatabase.createEmptyNull();            // no saved game
GameDatabase.createCorruptedNull();        // load throws GameCorrupted
```

A builder collects configuration for classes with several nullable dependencies:

```java
public static GameService createNull(NulledResponses responses) {
    return new GameService(ScoreCategoryNotifier.createNull(),
                           AverageScoreFetcher.createNull(responses.averageScoreResponses),
                           DieRoller.createNull(responses.dieRolls),
                           responses.gameDatabase);
}
// GameService.createNull(new NulledResponses().withDieRolls(1,2,3,4,5).withGame(game))
```
