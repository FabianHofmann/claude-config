First, identify the files that changed by running `git diff HEAD --name-only`. Ignore generated/binary files (*.min.js, dist/, build/, __pycache__, *.pyc, etc.) and focus on source code. For each changed file, read the full current implementation using the read tool.

Then run 3 reviewers in parallel to review the complete implementations:

1. **Code Quality** — Review the complete code for DRY violations, KISS violations, missing early returns, dead code, unused imports, readability issues. Judge based on the full context of the changed files. Note that DRY violations are such that repeat blocks of code should be refactored into a shared utility function. Short and efficient statements that are repeated from time to time can stay.

2. **Type & API** — Check for missing/incomplete type hints, inconsistent annotations, missing docstrings, backward compatibility concerns, naming issues.

3. **Test Coverage** — Check for missing tests, uncovered edge cases, test quality, missing error case tests.

## Output Schema
Each reviewer should output a structured report:
- List all issues with **file:line** references
- Classify each issue as **critical** (breaks functionality), **high** (significant concern), **medium** (important improvement), or **low** (nice to have)
- Format: `| Issue | file.ts:123 | SEVERITY |`

## Fallback Behavior
If unable to determine changed files with `git diff HEAD` (not a git repo or git not available), review all source files in the working directory as-is.

After all 3 complete, consolidate findings. Address all critical and high issues. Document medium/low issues deferred for later.

The name of the agents to trigger is `reviewer`.
