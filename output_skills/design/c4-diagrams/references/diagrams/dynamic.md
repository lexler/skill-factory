# Dynamic Diagram

Source: https://c4model.com/diagrams/dynamic

## Purpose
Shows how elements interact at runtime to accomplish a specific feature, use case, or workflow. Complements the static structure diagrams by showing behavior over time.

## Scope
A particular feature, story, or use case — not the whole system.

## Audience
Technical and non-technical people. The numbered interactions make sequences understandable to anyone.

## Elements
Flexible — choose the abstraction level that fits the story. A dynamic diagram can show software systems, containers, or components interacting. Pick the level where the interactions are meaningful.

## Two Presentation Styles

**Collaboration style** — elements arranged freely, interactions numbered to show order. Better when spatial layout matters (grouping related elements).

**Sequence style** — elements in columns, interactions flowing top to bottom. Better when timing and order are the main point.

Both show the same information — pick whichever communicates more clearly for the specific scenario.

## When to Use
Sparingly. Dynamic diagrams are for interactions that aren't obvious from the static structure:
- Complex multi-step workflows across several containers
- Recurring patterns worth documenting (e.g., how authentication flows across services)
- Scenarios where the order of interactions matters and isn't intuitive

Not every use case needs a dynamic diagram. If the static Container diagram already makes the interaction obvious, skip it.

## Relationship Labels
Number each interaction to show sequence. Include what happens at each step.

Good: "1. Submits credentials", "2. Validates against user store", "3. Returns JWT token"
Bad: "calls", "sends request"
