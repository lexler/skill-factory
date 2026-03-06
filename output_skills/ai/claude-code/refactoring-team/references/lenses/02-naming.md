# Lens: Naming

Names are the primary way code communicates. A good name eliminates the need to read the implementation.

## The Question

Do the names in this code communicate clearly, or do they obscure meaning?

## How to Spot

- Names that describe HOW (implementation) rather than WHAT (intent)
- Vague verbs: "get" when it's really "parse" or "calculate"
- Generic placeholders: data, info, result, temp, value
- Replace abbreviations. They obscure understanding
- Names that lie — don't match what the code actually does
- Very long names. Prefer shorter clear names over verbose names when a longer name doesn't add value
- No double negatives in names
- Names should preference consistency and language standards, i.e. instead of retrieveWith, getTheHeight, findTheVolume prefer the same verb
- Missing names - sometimes there's no variable where there should be - there's an inline block of code that would be better if we gave it a name

## Process

Read names as if you're new to this codebase. What confuses you? What makes you look at the implementation to understand?

## Go Deeper

What other naming issues exist? What names would you change if you had to explain this code to someone?
