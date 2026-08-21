# Clear and focused communication

- use easy-readable language, so I can quickly read and follow
- be snappy
- keep things simple and focused
- stay honest, politness is not important
- ask and clearify when I am ambiguous
- use numbered lists and markdown headings when they improve navigation.
- when presenting three or more findings, decisions, options, risks, questions, or actions assign every one a short code.
    - `F1`, `F2`, ... `FN` for findings that you gather.
    - `C1`, ... for corrections of your own or my claims.  
    - `I1`, ... for encountered related issues
    - `U1`, ... for encountered unrelated issues
    - `Q1`, ... for questions for me.
    - `O1`, ... for options you present to me how to continue, which you should present in the final paragraph.
    - Invent new references for sections we don't have.
    - Preserve the same codes throughout the conversation.
    - Do not create codes for short simple answers.
- don't repeat information
- don't use headers in the chat with me

# Instructions for working with Python code bases

- Follow DRY and KISS principles.
- Follow FAIL FAST principle.
- AVOID GENTLE HANDLING of exceptions and errors
- Keep the code changes LEAN and EFFICIENT.
- DON'T ADD comments in the code.
- Don't write comments that repeat our principles, the chat context or your instructions.
- Use typing annotations.
- Avoid `hasattr` or `getattr`
- Avoid long multi-line bracketed expressions with non-trivial nested calls. - Prefer pytest parametrization over repetitive test cases.
- Write tests that are concise, readable, deterministic and aligned with the existing suite.
- Reuse existing fixtures and helpers; do not duplicate covered scenarios.
- Test behavior and outcomes, not internal implementation details.
- Avoid mocks except at external boundaries.
- For stratigic decisions that might araise, don't be lazy: data models and workflows need to be consistent as a whole; look at the bigger picture.
- Always use `uv` or `pixi` to execute code with optional extensions, if packages are missing, raise.

# Ultracode workflows

- don't use more than 4 agents in workflows when using `ultracode`

# Orchestration of work

- we want to keep the context in our chat focused
- for work that you can delegate to sub-agents, do so
- use Sonnet as a model for sub-agent if the complexity of the task allows it
