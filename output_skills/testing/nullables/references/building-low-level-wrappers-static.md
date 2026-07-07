# Building Low-Level Wrappers — Declared-Interface Seam

The bottom layer: a wrapper for one communication *technology* (HTTP, database driver, filesystem, clock, random), made Nullable by stubbing the third-party library it calls. This is the only place two special things live: narrow integration tests against the real system, and an embedded stub. Swapping the seam behind a declared interface adds one pattern — the Thin Wrapper; everything else follows the same recipe. Examples are Java.

## Contents

- Find the edge
- Adapting to your language
- The Thin Wrapper pattern
- The build ladder
- Design the public interface
- Narrow integration tests
- Grow the stub by instrumentation
- The response ladder
- Named null factories
- Exceptions at the boundary
- Complete examples

## Find the edge

The stub cuts at code you **don't own** — the third-party library — never at your own class. Mocks mock code you own; Nullables stub only code you don't. That way your wrapper's real logic runs in every test, nulled or not, and a change to it is caught, not hidden.

Go all the way down: wrap `System.currentTimeMillis()`, not a convenience layer above it; wrap `RestTemplate`, not your service client. One low-level wrapper per technology — every service client speaking HTTP reuses the same `JsonHttpClient`. A single-purpose dependency may get one combined high+low wrapper; the stub still cuts at the third-party edge.

Before building, search the codebase for an existing wrapper (`createNull`, `Stubbed`, an `adapter/` or `infrastructure/` package). Building a duplicate wrapper for a technology is the expensive mistake here.

## Adapting to your language

The examples here are Java; the pattern is not.

- Follow the codebase's naming idiom for the two factories (`create`/`createNull` shown here), and keep both on the wrapper.
- "Throw a detailed error" means the language's failure idiom — exceptions, returned errors, result types. The detail and the failing loudly are the point, not the mechanism.
- Where classes can't nest, keep the stub invisible with the language's privacy unit — package-private, module-local, unexported.

## The Thin Wrapper pattern

Declare a **seam interface that mirrors the third-party signatures exactly, containing only the methods your wrapper uses** — plus two implementations: a Real one that forwards, and a Stubbed one that returns canned data.

```java
public class DieRoller {
    private final RandomInt random;

    public static DieRoller create() {
        return new DieRoller(new RealRandom());
    }
    public static DieRoller createNull(Integer... rolls) {
        return new DieRoller(new StubbedRandom(List.of(rolls)));
    }
    private DieRoller(RandomInt random) {
        this.random = random;
    }

    public int roll() {
        return random.nextInt(6) + 1;      // real wrapper logic — runs in both modes
    }

    // ---- nullability machinery, invisible to callers ----

    private interface RandomInt {          // mirrors java.util.Random, only what the wrapper uses
        int nextInt(int bound);
    }
    private static class RealRandom implements RandomInt {
        private final Random random = new Random();
        @Override public int nextInt(int bound) { return random.nextInt(bound); }
    }
    private static class StubbedRandom implements RandomInt {
        // canned values, exhaustion error — see response ladder
    }
}
```

Rules:

- Match the third-party signatures *exactly* — the Real implementation must be pure forwarding, no logic to get wrong.
- Include only methods your wrapper calls. Don't implement the library's own interface; it's far bigger than you need.
- If the third-party methods return third-party types, wrap those types the same way (`ResponseEntityWrapper<T>` with `getBody()` — Real holds the `ResponseEntity`, Stubbed holds the canned value).
- Everything nests privately inside the wrapper class: factories on the wrapper, never on the stub; the stub invisible to callers.

## The build ladder

Making an existing class Nullable takes five small steps, each compilable:

1. Private constructor; `create()` factory — both paths identical.
2. Extract the thin interface around the third-party calls; add Real implementation; wrapper logic now calls the interface.
3. Add Stubbed implementation and `createNull()`.
4. Add configurable responses (`createNull(Integer... rolls)`).
5. Switch tests from any hand-written test double to `createNull()`; delete the double.

## Design the public interface

From callers' needs, not the third-party shape: generic protocol verbs, plain values or your own types in and out. No third-party types escape the wrapper.

```java
public <R> R get(String urlTemplate, Class<R> responseType, String... urlVariables)
public void post(String url, Object body)
```

## Narrow integration tests

The wrapper abstracts a protocol, so test the protocol for real — against a real system the tests start and stop themselves: an embedded/localhost server for HTTP, H2 or a containerized database for JDBC, a temp directory for files. The best tests are self-sufficient — nothing to launch by hand.

Explore first (not TDD): most of the work is learning the third-party API. Use `println`/debugger in one growing test until the exchange works, then convert to assertions:

- Assert both directions once each: what the server/database saw, and what the wrapper returned.
- Remove or pin unstable data (timestamps, generated keys), with a comment saying why.
- Keep a resettable test double of the *system* (the SpyServer idea): started once per suite, `reset()` per test, `lastRequest`-style inspection, configurable next response with a loud unconfigured default ("response not specified", 501).

These tests document the real library's behavior — case normalization, auto-added headers, driver quirks. That record is what the stub must match.

## Grow the stub by instrumentation

Don't guess the third-party protocol — record it:

1. Put numbered log lines in *your wrapper* around the third-party calls.
2. Run a real-path integration test; write down the sequence.
3. Run the nulled test; the first missing log or exception is the next stub increment.
4. Implement as little as possible; repeat until green; delete the logs.

The technique transfers to any library — JDBC, SDK clients, messaging. If the real library behaves asynchronously (callbacks, futures completing later), the stub must reproduce that timing, not complete synchronously.

## The response ladder

Grow `createNull()`'s configuration in this order, one test each:

1. **Loud default** — an unconfigured Nullable returns unmistakably fake data (`"Nulled JsonHttpClient response"`, 42.0) so accidental reliance fails visibly.
2. **Single configurable response**.
3. **Per-endpoint** — a `Map<String, Object>` from endpoint to response.
4. **Partial configuration** — unspecified fields of a configured response get loud per-field defaults.
5. **Repetition semantics** — a single value repeats forever; a `List` is consumed in order; exhaustion throws an informative error naming the endpoint:

```java
private static Iterator<Object> normalizeResponses(Map.Entry<String, Object> entry) {
    if (entry.getValue() instanceof List) {
        return ((List<Object>) entry.getValue()).iterator();       // in order, then fails
    }
    return Stream.generate(entry::getValue).iterator();            // repeats forever
}
// on exhaustion / unknown endpoint:
throw new NoSuchElementException("No more responses configured for URL: " + url);
```

6. **Validate configuration** — reject impossible configured values (a die roll of 7) instead of decoding them silently.

## Named null factories

Without named optional parameters, make meaningful nulled states discoverable as factories (implemented as named constructors on the stub):

```java
GameDatabase.createNull();               // sensible default game
GameDatabase.createNull(snapshot);       // configured state
GameDatabase.createEmptyNull();          // nothing saved yet
GameDatabase.createCorruptedNull();      // load throws GameCorrupted
```

For a class with several nullable dependencies, collect configuration in a builder (`createNull(new NulledResponses().withDieRolls(1,2,3).withGame(game))`) — see building-high-level-wrappers.md.

## Exceptions at the boundary

Checked exceptions die at the wrapper: catch the third-party exception, rethrow your own meaningful type (`GameCorrupted`), or a `RuntimeException` with a detailed message. Callers above the wrapper never handle third-party exception types.

## Complete examples

Stubbing a Spring `RestTemplate` — thin interface + wrapped return type + per-endpoint responses:

```java
public class JsonHttpClient {
    private final RestTemplateWrapper restTemplate;
    private final OutputListener<JsonHttpRequest> listener = new OutputListener<>();

    public static JsonHttpClient create() {
        return new JsonHttpClient(new RealRestTemplate());
    }
    public static JsonHttpClient createNull(Map<String, Object> endpointsResponses) {
        return new JsonHttpClient(new StubbedRestTemplate(endpointsResponses));
    }
    private JsonHttpClient(RestTemplateWrapper restTemplate) {
        this.restTemplate = restTemplate;
    }

    public <R> R get(String urlTemplate, Class<R> responseType, String... urlVariables) {
        listener.emit(JsonHttpRequest.createGet(interpolateUrl(urlTemplate, urlVariables)));
        return restTemplate.getForEntity(urlTemplate, responseType, (Object[]) urlVariables)
                           .getBody();
    }
    public OutputTracker<JsonHttpRequest> trackRequests() {
        return listener.trackOutput();
    }

    // ---- nullability machinery ----

    interface RestTemplateWrapper {   // exactly RestTemplate's signatures, only what the wrapper uses
        <T> ResponseEntityWrapper<T> getForEntity(String url, Class<T> type, Object... vars);
    }
    interface ResponseEntityWrapper<T> {   // wraps the third-party return type
        T getBody();
    }
    private static class RealRestTemplate implements RestTemplateWrapper { /* forwards */ }
    private static class StubbedRestTemplate implements RestTemplateWrapper {
        /* endpoint map + normalizeResponses iterator, as above */
    }
}
```

Stubbing works for anything with an interface-shaped seam — even a Spring Data JPA repository:

```java
public class GameDatabase {
    interface Jpa {                            // mirrors the repository methods the wrapper uses
        GameRow save(GameRow gameRow);
        Optional<GameRow> findById(Long id);
    }
    // RealJpa forwards to the @Autowired repository; StubbedJpa returns configured GameRows
}
```
