---
name: hexagonal-architecture
description: Applies hexagonal (ports & adapters) architecture. Use when designing application structure, separating domain from infrastructure, creating testable boundaries, or when user mentions ports, adapters, hexagonal, or clean architecture.
---

# Hexagonal Architecture

## The Core Decision Rule

To decide if something belongs inside or outside the hexagon, ask:

> "Does it do I/O or run out-of-process?"

- **No** → Inside the hexagon (domain or application layer)
- **Yes** → Outside (adapter)

**Critical:** Consider ALL dependencies. A component's dependencies disqualify it even if the component itself doesn't do I/O. If it depends on Spring, a database driver, or any framework—it's outside.

## Layer Responsibilities

**Common misconception:** The hexagon is NOT just the domain. The hexagon contains both domain AND application layers. Adapters sit outside.

```
┌─────────────────────────────────────────┐
│           ADAPTERS (outside)            │
│  Web, CLI, Database, External APIs      │
│  ┌───────────────────────────────────┐  │
│  │     APPLICATION SERVICES          │  │
│  │  ┌─────────────────────────────┐  │  │
│  │  │         DOMAIN              │  │  │
│  │  └─────────────────────────────┘  │  │
│  └───────────────────────────────────┘  │
└─────────────────────────────────────────┘
        Dependencies flow INWARD only
```

**Domain** — Business constraints (what CAN happen). Contains Entities, Value Objects, Domain Services.

**Application** — Orchestration (HOW things happen). Contains Use Cases, Application Services.

**Adapters** — Translation to/from external world. Contains Controllers, Repositories, API clients.

**Domain defines ports (interfaces). Adapters implement them.**

## Naming Conventions

- Display/response: `*View` or `*Response` → `MemberView`, `OrderResponse`
- Incoming request: `*Request` → `CreateMemberRequest`
- Database entity: `*Dbo` → `MemberDbo`
- Domain → DTO: `static from(domain)` → `MemberView.from(member)`
- DTO → Domain: `as*()` method → `request.asMember()`

## Anti-Patterns

### Brittle Interfaces
```
register(username, password)  // Breaks when email required
```
Use wrapper objects that can evolve without breaking signatures.

### Domain Scope Pollution
Third-party types (`GoogleUser`, `StripePayment`) leaking into domain. Keep external types in adapters; map to domain types at the boundary.

### Use-Case Interdependencies
Use cases calling other use cases creates coupling. Each use case should be self-contained, orchestrating domain objects directly.

### Anemic Domain
Entities as data bags with logic scattered in services. Business rules belong IN entities and value objects.

### Premature Database Design
Designing schema before domain model. Domain model comes first; database adapter maps to it.

### Over-Complicated Adapters
Adapters adding logic beyond translation. Adapters should be thin—just implement the port interface.

## Testing Strategy

- **Domain**: Unit tests, no doubles needed (pure logic)
- **Application**: Unit tests with port doubles (fake repositories, stub notifiers)
- **Adapters**: Integration tests against real infrastructure (real database, real HTTP)

Ports give clean seams for test doubles. Test the domain exhaustively with fast unit tests; test adapters against real infrastructure sparingly.

## When NOT to Use

- Small/simple projects, especially CRUD-based apps (overhead not worth it)
