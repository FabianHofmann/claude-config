First, identify the files that changed by running `git diff main --name-only`. If the `main` branch doesn't exist, try `git diff master --name-only`. If neither exists, fall back to `git diff HEAD~1 --name-only`. Ignore generated/binary files (*.min.js, dist/, build/, __pycache__, *.pyc, etc.) and focus on source code. For each changed file, read the full current implementation using the read tool.

Then run 3 reviewers in parallel to review the complete implementations against the baseline:

1. **Code Quality** — Review the complete code for DRY violations, KISS violations, missing early returns, dead code, unused imports, readability issues. Judge based on the full context and how it compares to the baseline branch.

2. **Type & API** — Check for missing/incomplete type hints, inconsistent annotations, missing docstrings, backward compatibility concerns, naming issues.

3. **Test Coverage** — Check for missing tests, uncovered edge cases, test quality, missing error case tests.

## Output Schema
Each reviewer should output a structured report:
- List all issues with **file:line** references
- Classify each issue as **critical** (breaks functionality), **high** (significant concern), **medium** (important improvement), or **low** (nice to have)
- Format: `| Issue | file.ts:123 | SEVERITY |`

## Fallback Behavior
If git diff fails entirely (not a git repo or detached HEAD with no fallback branches), review all source files in the working directory as-is.

After all 3 complete, consolidate findings. Address all critical and high issues. Document medium/low issues deferred for later.

The name of the agents to trigger is `reviewer`.
