# Semantic Clarity

Does code tell the story of problem and solution, or just implementation?

## Process

1. Step back. What problem does this code solve? How?

2. Use `/refinement-loop` to distill your understanding:
   - Goal: get to the gist — what IS the problem space? How are we solving it?
   - Express in highest-level English possible
   - Refine until someone unfamiliar could understand

3. With that clarity, look at actual code:
   - Where does readability focus on implementation instead of the story?
   - Where is problem space obscured by solution mechanics?

4. Refactor to make code express problem/solution space the way your English does.
