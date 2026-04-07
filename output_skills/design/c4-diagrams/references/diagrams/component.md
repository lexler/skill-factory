# Component Diagram

Zooms into a single container to show its internal logical structure: the major building blocks and their relationships.

## Scope

A single container.

## Elements

- **Primary**: Components within the container
- **Supporting**: Other containers in the same system, people and external systems that connect to these components

## Audience

Developers and architects working on or reviewing this container. Answers: "What are the major pieces inside this container, and how do they relate?"

## What "Component" Means

A component is a logical grouping within a container:
- A module or package
- A namespace
- A set of related classes behind an interface
- A layer or bounded context within the container

The granularity depends on the container. For a Spring Boot API, components might be controllers, services, repositories. For a React app, they might be feature modules or state management layers.

## What to Include

- Each component with name, technology/implementation, and responsibility
- Relationships between components showing what flows
- External connections: which components talk to other containers or external systems
- Container boundary drawn around all components

## What NOT to Include

- Internal implementation of components (classes, functions) — that's Code level
- Components from other containers on the same diagram
- Every tiny utility class — focus on the architecturally significant groupings

## When to Create

Only when it adds value. The C4 model explicitly says: don't create component diagrams by default. Create them when:
- The container's internal structure is non-obvious
- You're onboarding someone to a complex container
- You're planning a significant refactoring
- You need to understand dependencies between modules

For long-lived documentation, consider automating generation from code.
