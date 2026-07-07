# Migrating an Existing Codebase to Nullables

Converting an existing codebase incrementally — replacing mock-based tests, or making untested code testable. The conversion orders below apply either way. Mocks and Nullables coexist in the same suite and even the same test, so every step ships green — no big-bang rewrite. Convert where testing hurts; skip code that's already easy to maintain.

## Contents

- Replace mocks in one test
- Choose a conversion order
- Throwaway stubs
- Checklist

## Replace mocks in one test

Substitute one double at a time; run tests after each swap.

Order within a test: doubles that are only *configured* first, the ones you `verify()` against last.

1. Replace the double with a nulled real instance.
2. Its `when().thenReturn()` configuration becomes `createNull(...)` arguments (Configurable Responses).
3. Its event-emission setup becomes `simulateX()` calls (Behavior Simulation).
4. Its `verify(...)` assertions become tracker assertions (Output Tracking).

```javascript
// Before
const emailer = mock(Emailer);
when(emailer.send).thenResolve({ sent: true });
const service = new UserService(emailer);
await service.createUser({ email: "test@example.com" });
verify(emailer.send).calledWith({ to: "test@example.com", subject: "Welcome" });

// After
const emailer = Emailer.createNull();
const emails = emailer.trackOutput();
const service = new UserService(emailer);
await service.createUser({ email: "test@example.com" });
assert.deepEqual(emails.data, [{ to: "test@example.com", subject: "Welcome" }]);
```

Each replacement requires the dependency to *be* Nullable — that's the conversion-order question.

## Choose a conversion order

Map the dependency tree first. Each class falls into one of three cases:

- **No infrastructure anywhere below** → nothing to convert; plain tests.
- **Low-level wrapper on third-party infrastructure** → narrow integration tests + embedded stub (see the building-low-level-wrappers file for your language).
- **Everything else** → make its direct dependencies Nullable, then compose (see building-high-level-wrappers.md).

**Climb the ladder** (small tree): convert the whole tree bottom-up — leaves first, then each parent by composition, converting tests as you go. No temporary work.

```
1. HttpClient      — embedded stub + narrow integration tests
2. Auth0Client     — createNull() by composition; replace mocks in its tests
3. LoginController — createNull() by composition; replace mocks in its tests
4. Router          — same
```

**Descend the ladder** (large tree): convert one class and its *direct* dependencies only, top-down, spreading the work across many sessions. Direct dependencies that aren't Nullable yet get throwaway stubs.

```
1. Router first: give LoginController a throwaway stub, make Router Nullable,
   replace mocks in Router's tests.
2. Later, LoginController: its dependency Auth0Client gets converted (or stubbed),
   LoginController's throwaway stub is replaced by real composition.
3. Repeat downward as time allows.
```

## Throwaway stubs

A temporary embedded stub for a dependency you aren't ready to convert. It breaks the sociable chain (changes in the stubbed dependency no longer reach these tests), so:

- Mark it clearly as temporary; keep it minimal — only what current tests need.
- It stays an implementation detail: callers still see only `create()`/`createNull()`, never a stub parameter.
- Replace it with real composition as soon as the dependency becomes Nullable; delete it.

## Checklist

- [ ] Find mock usage: `grep -rE "mock|jest\.fn|sinon|Mockito|td\.instance" test/`
- [ ] Map the dependency tree; pick climb (small) or descend (large)
- [ ] Per class: `create()` + `createNull()`, output tracking and configurable responses as its tests demand
- [ ] Per test: replace doubles one at a time, configured ones first, verified ones last; green after each
- [ ] Replace throwaway stubs as their dependencies become Nullable
- [ ] When a package is mock-free, drop the mocking library from it
