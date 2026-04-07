# Code Diagram

The deepest zoom level. Shows how a single component is implemented: classes, interfaces, functions, database tables, and their relationships.

## Scope

A single component.

## Elements

- **Primary**: Code elements — classes, interfaces, objects, functions, database tables
- **Supporting**: Other components that these code elements interact with

## Audience

Developers trying to understand or reason about a component's internals.

## What to Include

- Classes/interfaces with their key attributes and methods
- Relationships: inheritance, composition, dependency, association
- Database tables and their relationships (if the component is data-centric)
- Only the attributes and methods that tell the story — not every field and getter

## When to Create

Generate Code diagrams when:
- Investigating a specific component to understand its internals
- The user explicitly asks for a code-level view
- Reasoning about class relationships during design
- Understanding a complex piece of unfamiliar code

Be selective about scope — show the component under investigation, not every component in the container. Focus on the elements that matter for the current question.

## Style

Use UML class diagram style for object-oriented code:
- Classes with compartments (name, key attributes, key methods)
- Relationship arrows (inheritance, composition, dependency)

Use ER diagram style for data-centric components:
- Tables with key columns
- Foreign key relationships

Mix styles when a component spans both concerns.

## Common Mistakes

- Showing every attribute and method — filter to what tells the story
- Trying to diagram an entire container at code level — stay focused on one component
- Including implementation details that change frequently (private methods, internal state) unless they're the point of the diagram
