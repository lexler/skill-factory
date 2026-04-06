# Container Diagram

Source: https://c4model.com/diagrams/container

## Scope
A single software system — zoomed in to show its internals.

## Audience
Technical people: architects, developers, ops. People who need to understand the high-level technical shape of the system.

## Elements

**Primary:** Containers within the software system — web apps, APIs, databases, message queues, file stores, mobile apps, serverless functions.

**Supporting:** People and external software systems that connect directly to the containers. These provide context but aren't the focus.

## What to Include
- Every container (deployable/runnable unit) within the system boundary
- Technology choices for each container (e.g., "React SPA", "Node.js API", "PostgreSQL")
- A short responsibility description for each container
- Communication paths between containers and what flows through them
- The people and external systems that interact with specific containers

## What to Exclude
- Internal structure of containers — no classes, modules, or components at this level
- Deployment infrastructure — no load balancers, clusters, replicas, CDNs. Those go in Deployment diagrams.
- Low-level protocol details (mention "REST API" or "async messaging" but not specific endpoints)

## Relationship Labels
Include the communication mechanism at this level.

Good: "reads/writes data [SQL/TCP]", "sends events to [async, AMQP]", "makes API calls to [REST/HTTPS]"
Bad: "uses", "connects to"

## Drawing the System Boundary
Draw a clear boundary (dashed box or similar) around all containers that belong to the system in scope. People and external systems sit outside this boundary.

## Common Mistakes
- Calling databases "external systems" — if you own it and it's part of your system, it's a container inside the boundary
- Showing too many containers (20+) — consider whether some can be grouped, or whether you're modeling at too fine a grain. A container is something independently deployable, not every microservice endpoint.
- Omitting the supporting elements — containers without context (who uses them? what feeds them?) tell an incomplete story
- Including deployment topology — "3 instances behind a load balancer" is deployment, not architecture
