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
