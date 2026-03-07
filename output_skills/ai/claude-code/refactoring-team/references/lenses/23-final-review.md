# Lens: Final Review

Last pass. The reviewer will assess the code holistically and may send you back through specific lenses that deserve a second look.

## Process

1. Read through the refactored code from start to finish
2. Find anything that still bothers you
3. For each issue, ask: "Can I fix this without changing behavior?"
   - Yes → implement the refactoring now
   - No → note it for future improvements

## Re-applying Lenses

The reviewer may send you back through specific lenses. When they do:

Read the lens file again. Then apply it as if seeing this code for the first time — forget what you decided in the earlier pass. Design lenses have changed the landscape: new names exist, new types have been introduced, responsibilities have shifted. Functions you left alone may now have obvious extraction points because the vocabulary to name those extractions didn't exist before.

Method-length in particular: every design lens changes what's extractable. A function that looked fine before may now clearly contain phases that have names, or can benefit from methods being extracted to make the narrative cleaner. Carefully and thoroughly challenge every function's length.

## When Done

Declare done when you have implemented all refactorings you can find. Note what is beyond refactoring's reach:
- Current problems that require behavior changes
- Improvements that would change what the code actually does
- Recommendations for the human to consider
