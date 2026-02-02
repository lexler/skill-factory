# A-Frame Architecture

A-Frame separates Logic from Infrastructure so you can swap real infrastructure for nulled versions without touching Logic.

## The Problem: Logic Depends on Infrastructure

When Logic imports Infrastructure directly:

```
Logic → Infrastructure → Database/HTTP/FileSystem
```

You face a painful choice when testing:
- **Hit real infrastructure** — tests become slow (network, disk) and flaky (timeouts, service outages)
- **Mock the infrastructure** — tests become brittle (coupled to implementation, break on refactoring)

Either way, your feedback loop suffers. Slow tests mean you run them less. Brittle tests mean you trust them less.

## A-Frame: Peers, Not Layers

A-Frame makes Logic and Infrastructure **peers**:

```
        Application (coordinates)
            ↓              ↓
Logic (pure, tested)    Infrastructure (Nullables)

Both use Value Objects (shared types)
```

Neither depends on the other. Application coordinates between them.

## The Three Layers

**Logic** — Pure functions. No side effects, no I/O. Receives data, returns data.

**Infrastructure** — Handles external I/O. Wrapped with Nullables (`create()` / `createNull()`).

**Application** — Thin coordination. Reads from Infrastructure, calls Logic, writes results. Follows [Logic Sandwich](logic-sandwich.md) pattern. For event-driven code, see [Traffic Cop](event-driven.md).

## Key Rule

**Logic never imports Infrastructure directly.**

```javascript
// BAD: Logic imports infrastructure
import { Database } from "./database.js";

class OrderLogic {
  validate(orderId) {
    const order = Database.get(orderId);  // Infrastructure leak!
  }
}

// GOOD: Logic receives data, stays pure
class OrderLogic {
  static validate(order, inventory) {
    // Pure computation on data
  }
}
```

When Logic depends on Infrastructure, you can't test it without either hitting real systems or mocking. A-Frame eliminates this by keeping Logic pure.

## Value Objects

Logic and Infrastructure communicate through Value Objects—plain data with no behavior or dependencies.

```javascript
const order = {
  id: "123",
  items: [{ sku: "widget", quantity: 2 }],
  status: "pending"
};
```

Application reads Value Objects from Infrastructure, passes them to Logic, then writes results back. Neither Logic nor Infrastructure knows about the other.
