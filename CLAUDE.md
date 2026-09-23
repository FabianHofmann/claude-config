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
- work in the current worktree, so I see changes here in my Zed editor.  
- when raising issues on Github, use the "issue-raise" skill. always add minimial reproducabel examples for bugs.

# Ultracode workflows

- don't use more than 4 agents in workflows when using `ultracode`

# Orchestration of work

- we want to keep the context in our chat focused
- for work that you can delegate to sub-agents, do so
- for sub-agents default to Opus. Use Sonnet for low complexity tasks. For hard quests use Fable.
- for reviewing (with or without review skills), prefer Opus models over Fable models to save tokens.
