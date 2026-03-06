# Lens: Semantic Clarity

Code should communicate the problem and solution space, not just the implementation. The goal is utmost readability — readers understand WHAT and WHY before HOW.

## The Question

Does this code tell the story of the problem it solves and how it solves it? Or does it just describe implementation mechanics?

## Process

1. Step back. What problem does this code solve? How does it solve it?

2. Use the `refinement-loop` skill to distill your understanding:
   - Goal: get to the gist of the gist — what IS the problem space? How are we solving it?
   - Express it in the highest-level English possible. It can have some bullet points
   - Look critically at what you wrote. Is there implementation details in your English?
   - Refine until you've captured what the code does and how, and someone unfamiliar with codebase can quickly understand it from your English

3. With that clarity, look at the actual code:
   - Where does readability focus on implementation instead of the story?
   - Where is the problem space obscured by solution mechanics?
   - Where is the solution space buried in implementation details?

4. Come up with the list of refactorings we need to do to have the code express problem and solution space the same way our English does.

5. Refactor to make the code tell the story you distilled.

## Go Deeper

What else obscures the semantic story? Where else is implementation drowning out meaning?
