# Component Diagram

Source: https://c4model.com/diagrams/component

## Scope
A single container — zoomed in to show its internal organization.

## Audience
Developers working on or with that specific container.

## Should You Create One?
Usually not. Only create a Component diagram when:
- The container's internal structure is complex and non-obvious
- You need to communicate how responsibilities are divided within the container
- The diagram will be actively maintained (or auto-generated)

If the container is a straightforward CRUD API or a standard framework app, a component diagram adds little over reading the code.

## Elements

**Primary:** Components within the container — modules, packages, service layers, major classes or groups of classes behind a defined interface.

**Supporting:** Other containers in the system that the components interact with, plus any people or external systems that connect directly.

## What to Include
- Distinct functional groupings within the container
- Technology and implementation details for each component (e.g., "Spring MVC Controller", "JPA Repository")
- Relationships between components and to external containers

## What to Exclude
- Code-level details — individual classes, methods, fields
- Every internal class — group related classes into a single component

## Common Mistakes
- Creating Component diagrams for every container — only for the ones where it adds value
- Showing every class as a separate component — components are groups of related code, not individual classes
- Not showing the surrounding containers — components don't exist in isolation
