---
name: implement-feature
description: Autonomous Feature/Bugfix Implementation Workflow. Use when implementing features, fixing bugs, or following a structured development workflow with exploration, implementation, review, and PR phases.
---

# Autonomous Feature/Bugfix Implementation Workflow

Strictly follow this procedure. Leverage sub-agents for parallelism and delegation.

---

## User Input

The user should provide a GitHub issue reference (e.g., "issue 376", "#376", or a full URL) or a description of the feature/bugfix as plain text or as reference to a file.

---

## Phase 1: Exploration & Planning

1. Rename the current session to a descriptive name using the /rename command.

2. **Explore codebase** (sub-agent): Spawn an `Explore` sub-agent to find relevant patterns, files, and dependencies related to the feature/bug.

3. **Clarify requirements**: If requirements are ambiguous, use `AskUserQuestion` to clarify scope, edge cases, and acceptance criteria.

4. **Create task breakdown**: Use `TodoWrite` to break the work into 5-10 discrete, testable tasks. Mark the first task as `in_progress`.

5. **Create branch**: Fetch the latest changes from the remote repository and if not already checked out, create and checkout a dedicated git branch. For the branch name, use `feature/`, `fix/`, or `refactor/` prefix as appropriate.

6. **/compact**: Reduce context after exploration.

---

## Phase 2: Design (Non-Trivial Features Only)

7. **Architecture review** (optional): For features touching 3+ files or introducing new patterns, spawn a `Plan` sub-agent to propose structure before implementation.

---

## Phase 3: Implementation

8. **For bugs (TDD)**:
   - Write a failing test that reproduces the issue
   - Implement the fix
   - Verify the test passes

9. **For features** - spawn sub-agents **in parallel in a single message**:
   - **Test Writer** (`python-expert`): Include the target files from exploration in the prompt. Ask to draft test cases only.
   - **Implementer** (`python-expert`): Include the target files and test expectations. Ask to draft implementation only.
   - Integrate outputs, resolve conflicts between test expectations and implementation.

10. **Update TodoWrite**: Mark completed tasks, add any discovered sub-tasks.

---

## Phase 4: Validation

11. **Run linter**:
    ```bash
    uv run ruff check --fix . && uv run ruff format .
    ```

12. **Run type checker**:
    ```bash
    uv run mypy .
    ```
    Fix type errors before proceeding.

13. **Run tests**:
    ```bash
    uv run pytest
    ```
    Fix failures. Max 3 fix-test iterations; if still failing, reassess approach.

14. **/compact**: Summarize context before review.

---

## Phase 5: Review (Parallel Sub-Agents)

15. **Spawn review sub-agents in parallel** (single message, use `model: sonnet`):

    - **Code Quality Reviewer** (`general-purpose`):
      "Review `git diff origin/master`. Check for DRY, KISS, FAIL FAST violations. List issues with file:line and severity."

    - **Type & API Reviewer** (`general-purpose`):
      "Review `git diff origin/master`. Check type hints, docstrings, public API consistency. List issues with file:line and severity."

    - **Security Reviewer** (`general-purpose`) - only if touching auth/input/DB:
      "Review `git diff origin/master` for OWASP top 10 vulnerabilities. List issues with file:line and severity."

16. **Address critical feedback**: Fix issues flagged as critical or high priority only. Ignore stylistic suggestions.

---

## Phase 6: Finalization

17. **Re-run tests**: Verify fixes didn't introduce regressions.
    ```bash
    uv run pytest
    ```

18. **/add-release-notes**: Document changes in release notes.

19. **Final sanity check**: Review all changes before committing.
    ```bash
    git diff origin/master
    ```

---

## Phase 7: Raise and Monitor Pull Request

20. Open the current worktree repository with `zed` so that the user can review the changes before raising the PR.

21. Ask user to confirm committing and raising PR using `AskUserQuestion`. If review is needed, update **Update TodoWrite** and JUMP BACK to Phase 3.

22. **/commit** and **/raise-pr**: Raise a pull request.

23. **CI monitoring** (sub-agent to isolate context): Spawn a `general-purpose` sub-agent with the prompt:
    "Run `/ci-fix <pr_number>` to monitor and fix CI failures. Report back when all checks pass or after 3 failed fix attempts."

    This isolates the potentially long CI fix loop from the main context.

---

## Sub-Agent Prompt Templates

### Exploration (Phase 1, `Explore` agent)
```
Explore the codebase for [feature/bug context]. Find:
- Existing patterns for similar functionality
- Files that will need modification (list exact paths)
- Test patterns used in this codebase
- Potential conflicts or dependencies
Return a concise summary with file paths. Keep output under 500 words.
```

### Test Writer (Phase 3, `python-expert` agent)
```
Write tests for [feature] in [target test file from exploration].
Reference implementation files: [list from exploration]
Follow existing test patterns. Include:
- Happy path tests
- Edge cases and error conditions
Do not implement the feature, only write tests.
```

### Implementer (Phase 3, `python-expert` agent)
```
Implement [feature] in [target files from exploration].
Tests expect: [brief summary of test expectations]
Follow existing code patterns. Keep changes minimal and focused.
Do not modify tests.
```

### Code Quality Review (Phase 5, `general-purpose` agent)
```
Run `git diff origin/master` and review for:
- DRY violations (duplicated logic)
- KISS violations (unnecessary complexity)
- FAIL FAST violations (silent failures)
List issues as: file:line - severity - description
Only report critical/high issues. Keep output concise.
```
