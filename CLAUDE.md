# Think before coding

- State your assumptions explicitly. If uncertain, ask.
- Present multiple interpretations rather than choosing silently.
- Advocate for simpler approaches when they exist.
- Stop and identify confusion rather than proceeding with unclear requirements.

# Instructions for working with Python code bases

- Follow DRY and KISS principles.
- Follow FAIL FAST principle.
- AVOID GENTLE HANDLING of exceptions and errors
- Keep the code changes LEAN and EFFICIENT, DON'T ADD BOILERPLATE CODE.
- DON'T ADD comments in the code.
- DON'T BE VERBOSE in the documentation

In Python language:
- Use typing annotations for better code clarity.
- AVOID FUNCTIONS like `hasattr` or `getattr` and make sure to use type-specific and consistent operations instead
- Make sure data models and workflows are consistent and streamlined, rather look at the bigger picture than smaller case fixes.
- Don't write comments that repeat our principles.
- Write tests that are concise, readable, deterministic and aligned with the existing suite.
- Prefer pytest parametrization over repetitive test cases.
- Reuse existing fixtures and helpers; do not duplicate covered scenarios.
- Test behavior and outcomes, not internal implementation details.
- Avoid mocks except at external boundaries.
- Prefer Arrange / Act / Assert (AAA) when it improves clarity.

Formatting / readability:
- Avoid long multi-line bracketed expressions with non-trivial nested calls. Extract intermediates into named local variables so each line is a complete, named thought and arguments can be debugged individually.
- Aim for compact *and* clear: prefer single-line statements, each a complete thought. Compactness targets needless line *spread* (wrapped nested calls), not readable line count — extracting intermediates is line count well spent, but never collapse distinct logic into one dense line. Shorter is only better when it stays clearer; stop when fewer lines start to obscure intent.
- Only extract when the name adds meaning. Trivial args (`timeout=30`, `index=df.index`) stay inline; if no good name comes to mind, leave it inline.
- Keyword arguments split across lines are fine — the keyword already names the value. The pain is with positional nested calls.
