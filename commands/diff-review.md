Run 3 reviewer agents in parallel to review the current git diff (`git diff HEAD`):

1. **Code Quality** — Check for DRY violations, KISS violations, missing early returns, dead code, unused imports, readability issues
2. **Type & API** — Check for missing/incomplete type hints, inconsistent annotations, missing docstrings, backward compatibility breaks, naming issues
3. **Test Coverage** — Check for missing tests, uncovered edge cases, test quality, missing error case tests

Each reviewer should list issues with file:line references, classified as critical/high/medium/low.

For each issue, tag it as one of:
- `[task-related]` — directly related to the current task, in files changed by this task
- `[drive-by]` — pre-existing problem, in untouched code, or unrelated to the task's purpose

After all 3 complete, consolidate findings. Address all critical and high task-related issues. Drive-by issues and medium/low issues that would introduce over-engineering are deferred for later.

The name of the agents to trigger is `reviewer`.
