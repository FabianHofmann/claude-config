Run 3 reviewer agents in parallel to review the current git diff against master/main (`git diff master` or `git diff main`):

1. **Code Quality** — Check for DRY violations, KISS violations, missing early returns, dead code, unused imports, readability issues
2. **Type & API** — Check for missing/incomplete type hints, inconsistent annotations, missing docstrings, backward compatibility breaks, naming issues
3. **Test Coverage** — Check for missing tests, uncovered edge cases, test quality, missing error case tests

Each reviewer should list issues with file:line references, classified as critical/high/medium/low.

After all 3 complete, consolidate findings. Address all critical and high issues. Document medium/low issues deferred for later.

The name of the agents to trigger is `reviewer`.
