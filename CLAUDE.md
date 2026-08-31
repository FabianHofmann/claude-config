# Communication

- Voice, formatting and reference codes are defined in the active output style.
- If no output style is active, still be snappy, honest and plain.

# Working with Python code bases

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

# Working with git

- don't write "co-authored by Claude" or similar in the commit message

# Ultracode workflows

- don't use more than 4 agents in workflows when using `ultracode`

# Orchestration of work

- we want to keep the context in our chat focused
- for work that you can delegate to sub-agents, do so
- use Sonnet as a model for sub-agent if the complexity of the task allows it, otherwise use Opus 4.8 sub-agents. For really hard quests use Fable 5.
