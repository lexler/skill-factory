# Migrating from Mocks to Nullables

Strategies for converting existing mock-based codebases to Nullables.

## Contents

- [Descend the Ladder](#descend-the-ladder)
- [Climb the Ladder](#climb-the-ladder)
- [Replace Mocks with Nullables](#replace-mocks-with-nullables)
- [Throwaway Stubs](#throwaway-stubs)

## Descend the Ladder

Convert incrementally from top down. Make direct dependencies Nullable while leaving deeper dependencies unconverted.

```
Before:
  App → Service → Repository → Database
  (all mocked in tests)

Step 1: Make Service Nullable
  App (tests use Service.createNull())
    → Service → Repository → Database

Step 2: Make Repository Nullable
  App → Service (tests use Repository.createNull())
         → Repository → Database

Step 3: Make Database wrapper Nullable
  App → Service → Repository (tests use Database.createNull())
                    → Database wrapper
```

**When to use:** Large codebases where converting everything at once is impractical.

**Process:**
1. Pick the highest-level class with mocked dependencies
2. Create `createNull()` factory for that class
3. Update its tests to use `createNull()` instead of mocks
4. Repeat for the next level down

## Climb the Ladder

For simpler dependency trees, convert the entire tree at once using post-order depth-first traversal (leaves first, then parents).

```
Dependency tree:
  App
  ├── UserService
  │   └── Database
  └── EmailService
      └── SmtpClient

Conversion order:
1. Database (leaf)
2. SmtpClient (leaf)
3. UserService (depends on Database)
4. EmailService (depends on SmtpClient)
5. App (depends on both services)
```

**When to use:** Smaller codebases, new features, or when you want complete conversion.

## Replace Mocks with Nullables

Substitute test doubles one at a time:

**Before (with mocks):**
```javascript
it("sends welcome email", async () => {
  const mockEmailer = mock(Emailer);
  when(mockEmailer.send).thenResolve({ sent: true });

  const service = new UserService(mockEmailer);
  await service.createUser({ email: "test@example.com" });

  verify(mockEmailer.send).calledWith({
    to: "test@example.com",
    subject: "Welcome"
  });
});
```

**After (with Nullables):**
```javascript
it("sends welcome email", async () => {
  const emailer = Emailer.createNull();
  const emails = emailer.trackOutput();

  const service = new UserService(emailer);
  await service.createUser({ email: "test@example.com" });

  assert.deepEqual(emails.data[0], {
    to: "test@example.com",
    subject: "Welcome"
  });
});
```

**Key changes:**
- `mock()` → `createNull()`
- `when().thenResolve()` → Configurable Responses
- `verify().calledWith()` → Output Tracking assertions

## Throwaway Stubs

During migration, you may need temporary stubs for unconverted dependencies.

```javascript
class UserService {
  static create() {
    return new UserService(Database.create(), Emailer.create());
  }

  static createNull({
    users = [],
    // Throwaway stub config - will be replaced when Database becomes Nullable
    dbStub = new ThrowawayDatabaseStub()
  } = {}) {
    return new UserService(dbStub, Emailer.createNull());
  }
}

// Temporary - delete when Database gets proper Nullable support
class ThrowawayDatabaseStub {
  constructor() {
    this._users = new Map();
  }
  async getUser(id) {
    return this._users.get(id);
  }
  async saveUser(user) {
    this._users.set(user.id, user);
  }
}
```

**Rules for Throwaway Stubs:**
- Mark clearly as temporary (comment, naming)
- Keep minimal - only what current tests need
- Delete as soon as the real dependency becomes Nullable
- Don't let them grow into permanent fixtures

## Migration Checklist

- [ ] Identify all mock usages in test files (`grep -r "mock\|jest.fn\|sinon"`)
- [ ] Map dependency tree
- [ ] Choose strategy: Descend (large) or Climb (small)
- [ ] For each class:
  - [ ] Add `create()` factory method
  - [ ] Add `createNull()` factory method
  - [ ] Add Output Tracking where needed
  - [ ] Add Configurable Responses where needed
  - [ ] Update tests to use Nullables
  - [ ] Remove mock imports
- [ ] Delete throwaway stubs when no longer needed
- [ ] Remove mock library from dependencies
