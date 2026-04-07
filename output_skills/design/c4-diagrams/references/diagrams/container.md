# Container Diagram

Zooms into a single software system to show its high-level technical structure: the deployable/runnable units and how they communicate.

## Scope

A single software system.

## Elements

- **Primary**: Containers within the system (web apps, APIs, databases, message queues, file stores, etc.)
- **Supporting**: People and external software systems that interact with the containers

## Audience

Technical people — developers, architects, operations staff. Answers: "What are the major technical building blocks, and how do they talk to each other?"

## What "Container" Means

A container is a separately deployable or runnable thing:
- Server-side web application (Spring Boot, Express, Django)
- Client-side application (React SPA, iOS app, Android app)
- API service (REST API, GraphQL API, gRPC service)
- Database (PostgreSQL schema, MongoDB database, Redis)
- Message broker/queue (RabbitMQ, Kafka topic, SQS)
- File storage (S3 bucket, local filesystem)
- Serverless function (Lambda, Cloud Function)
- Background worker/job processor

NOT Docker containers (though a Docker container might host a C4 container).

## What to Include

- Every container with its name, technology, and responsibility
- Inter-container communication with protocol/technology ("JSON/HTTPS", "JDBC", "AMQP", "gRPC")
- External people and systems from the Context diagram, now connected to specific containers
- System boundary drawn around all containers to show what's in scope

## What NOT to Include

- Deployment infrastructure (load balancers, clustering, CDNs) — that's for Deployment diagrams
- Internal structure of containers (components, classes) — that's the next zoom level
- Replication or failover details

## Common Mistakes

- Showing deployment nodes (servers, Kubernetes pods) — this is logical architecture, not physical
- Missing technology labels on containers ("Database" is not enough; say "PostgreSQL 15")
- Missing protocol labels on inter-container relationships
- Making it too big — if you have 20+ containers, split into focused views by domain or user journey
- Confusing containers with components — if it's not separately deployable, it's probably a component
