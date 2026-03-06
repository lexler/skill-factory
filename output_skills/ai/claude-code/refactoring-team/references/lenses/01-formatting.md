# Lens: Formatting

The surface layer. Dead code, unused imports, inconsistent formatting — noise that obscures what matters.

## The Question

What in this code is just noise that can be removed?

## Look For

- Unused imports
- Dead code, commented-out code
- Inconsistent indentation or spacing
- Redundant wrappers (try/except that just re-raises)

## Process

Scan each file. What can be deleted without changing behavior? What formatting inconsistencies stand out?

## Go Deeper

What else is noise? What other formatting issues exist?
