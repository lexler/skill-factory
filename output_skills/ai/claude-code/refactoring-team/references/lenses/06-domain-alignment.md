# Lens: Domain Alignment

Code should speak the language of the problem, not just the solution. Implementation details should fade; domain concepts should shine.

## The Question

Does this code speak the language of the problem domain, or is it trapped in implementation language?

## How to Spot

If you'd explain the code differently than it reads, there's a gap.

Listen for implementation words: "nested," "parse," "split," "loop," "array," "handler," "processor." These describe HOW, not WHAT. The domain has its own vocabulary — is the code using it?

## Process

Read the code and ask: what is this code ABOUT? What problem domain does it live in? Do the names and structures reflect that domain?

## Go Deeper

What domain concepts are missing from this code? What words would you use to explain it that don't appear anywhere?
