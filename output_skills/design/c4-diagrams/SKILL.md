---
name: c4-diagrams
description: Creates C4 architecture diagrams for designing, documenting, or understanding software architecture. Use when working through system design, mapping existing codebases, or visualizing structure at any level from system landscape down to code.
---

STARTER_CHARACTER = 🏗️

## C4 Model

C4 is a hierarchical approach to diagramming software architecture. Four core levels of zoom, each showing more detail:

```
System Context (one system + its users and external dependencies)
  └── Container (deployable units inside the system)
        └── Component (logical groupings inside a container)
              └── Code (classes, interfaces, functions inside a component)
```

Three supplementary diagram types complement this hierarchy:
- **System Landscape** — zooms out wider than Context, shows all systems in an org
- **Dynamic** — shows runtime behavior for a specific use case
- **Deployment** — shows how containers map to infrastructure

## Core Abstractions

- **Person** — a user, actor, or role that interacts with software systems
- **Software System** — the highest level of abstraction; a thing that delivers value to users. Can be yours (in scope) or external
- **Container** — a separately deployable/runnable unit within a system. Web apps, APIs, databases, message queues, file systems, serverless functions. NOT Docker containers — "container" here means "thing that runs code or stores data"
- **Component** — a logical grouping within a container. In practice: a module, package, namespace, or set of related classes
- **Relationship** — a unidirectional dependency or data flow between elements

## Choosing the Diagram Type

Pick the level that matches the conversation. Load the reference for the type you're creating.

**Static structure (the zoom hierarchy):**
- **System Context** — starting point for any architecture discussion. One system, its users, external dependencies. Both technical and non-technical audiences. → [system-context.md](references/diagrams/system-context.md)
- **Container** — inside one system. Shows major technology choices, how deployable units communicate. Technical audience. → [container.md](references/diagrams/container.md)
- **Component** — inside one container. Shows logical structure. Only when it adds value for understanding. → [component.md](references/diagrams/component.md)
- **Code** — inside one component. Classes, interfaces, relationships. For understanding a specific component's internals, or when the user requests it. → [code.md](references/diagrams/code.md)

**Wider or orthogonal views:**
- **System Landscape** — all systems in an org/department. Like System Context but without focus on one system. For portfolio views. → [system-landscape.md](references/diagrams/system-landscape.md)
- **Dynamic** — how elements interact at runtime for a specific use case. Numbered interactions. Use sparingly, for complex or non-obvious flows. → [dynamic.md](references/diagrams/dynamic.md)
- **Deployment** — how containers map to infrastructure (servers, cloud, Docker). Per environment. → [deployment.md](references/diagrams/deployment.md)

Most teams need only System Context + Container. Add others when they earn their place.

## Choosing the Output Format

Ask the user which format they prefer. If no preference stated, choose based on context:

- **ASCII** — works everywhere: inline docs, chat, code review comments. No tooling needed. → [ascii.md](references/formats/ascii.md)
- **Structurizr DSL** — architecture as code. Model once, generate multiple views. Render at structurizr.com/dsl or locally. Best for living documentation. → [structurizr.md](references/formats/structurizr.md)
- **Mermaid** — renders natively in GitHub, GitLab, many markdown tools. Good for embedding in docs/READMEs. → [mermaid.md](references/formats/mermaid.md)

## Notation Rules

**Every diagram must have:**
- A title stating the diagram type and scope (e.g., "Container diagram for Payment Service")

**Every element must have:**
- A name
- Its type explicitly stated (Person, Software System, Container, Component)

**Every container and component must also have:**
- Technology explicitly stated (e.g., "Spring Boot", "PostgreSQL", "React SPA")

**Every relationship must:**
- Be unidirectional (one arrow direction)
- Have a label describing the intent, not just "Uses" — say what it does ("Sends orders to", "Reads credentials from", "Queries customer data via")
- Include technology/protocol for inter-container communication ("JSON/HTTPS", "JDBC", "gRPC")

**Descriptions and legends are format-dependent:**
- Structurizr DSL — descriptions go in element definitions, render as tooltips
- Mermaid — descriptions go in element parameters, render below the name
- ASCII — keep boxes minimal (name + technology only). No descriptions inside boxes, no legend block. The conventions are simple enough to be self-evident.

## Review Checklist

After creating any diagram, verify:

- Title present, states diagram type and scope
- Every element has name and type (descriptions where the format supports them — see Notation Rules)
- Technology labeled on containers, components, and inter-container relationships
- Relationship labels describe intent and match arrow direction
- No vague labels ("Uses", "Connects to") — be specific about what flows
- Acronyms either universally understood or explained
- Notation consistent (colors, shapes, line styles mean the same thing across the diagram)
- For ASCII diagrams: run `uv run ${CLAUDE_SKILL_DIR}/scripts/check_ascii_alignment.py <file>` to validate box alignment. Fix any issues before presenting.

## Anti-Patterns

**One giant diagram** — if a Container diagram has 20+ containers, split into focused views by domain area or user journey. Each view should tell one story.

**Mixing abstraction levels** — don't show components and software systems on the same diagram. Each diagram operates at one zoom level.

**Missing technology labels** — "Web App" tells the reader nothing. "React SPA" or "Spring Boot API" tells them what stack they're looking at.

**Vague relationship labels** — "Uses" between every element makes the diagram useless. Be specific: "Authenticates via", "Publishes events to", "Reads from".

**Deployment details in Container diagrams** — clustering, load balancers, replication belong in Deployment diagrams, not Container diagrams.

## Workflows

### From Existing Code

When analyzing a codebase to generate diagrams:

1. Explore the codebase to identify the system boundary, external dependencies, and internal structure
2. Start at System Context level — identify users and external systems
3. Zoom into Container level — identify deployable units, data stores, and inter-container communication
4. Ask the user if deeper levels (Component, Code) are needed before going further
5. For large systems, create multiple focused views by domain area or user journey rather than one giant diagram
6. Verify the diagram against actual code — don't guess at relationships

**Recognizing C4 elements in code:**
- Separately deployed processes, services, or apps → Containers
- Databases, message brokers, file stores with their own process/lifecycle → Containers
- Modules, packages, or namespaces within one deployable → Components
- External APIs, third-party SaaS, systems you don't control → External Software Systems
- A monolith is one Container with many Components inside — don't split it into multiple Containers unless the parts deploy independently

### From Designs Being Planned

When the user wants to work through architecture for a system that doesn't exist yet — or only partially exists — first figure out where they are in the design process:

1. Look for existing design artifacts before asking. Check `docs/`, `architecture/`, `design/`, ADRs, RFCs, README files, anywhere design might already be captured. If you find them, read them and base the diagrams on what's there.
2. If partial designs exist, draft diagrams from them and ask the user only about gaps.
3. If no design exists, interview the user: what is the system, who uses it, what does it integrate with, what are the major moving parts.
4. Draft a System Context diagram and validate with the user before going deeper
5. Discuss containers — what tech, what responsibilities, how they communicate
6. Draft a Container diagram
7. Go deeper only if the user wants to explore a specific container's internals

The diagrams are a tool for thinking, not just documentation. Surface architectural decisions as you draft — "I'm assuming the queue decouples ingestion from processing — is that intentional?" — rather than just transcribing what the user said.

### After the First Draft

- Does any single view have too many elements? Split by domain area or user journey
- Are the abstraction levels consistent? Don't mix containers and components in one diagram
- Are relationship labels specific or vague?
- Would someone unfamiliar with the system understand the diagram without narration?
