---
name: review-full-branch
description: "Absolute Code Review against baseline branch: read full implementations of changed files and run parallel reviewers. Use when doing a thorough review of branch changes with full file context."
---

# Absolute Code Review (Branch)

Thorough review of branch changes against the baseline with **full file context** — reviewers judge the complete implementation, not just the hunks.

## Scope & context

1. Run `git diff main --name-only` to list changed files. If `main` doesn't exist try `git diff master --name-only`; if neither exists fall back to `git diff HEAD~1 --name-only`. Apply the ignore filter in the shared rubric.
2. For each surviving source file, Read the **full current implementation**, not just the changed lines. Judge it in light of how it compares to the baseline.
3. Cross-file context (call sites, type defs elsewhere, existing tests) still must be verified to satisfy the evidence requirement.

## Apply the shared rubric

Read **`/home/fabian/.claude/skills/_review-rubric.md`** and follow it in full:
- Section 2 — risk-tier the number of reviewers to the size and sensitivity of the change.
- Section 3 — the reviewer dimensions and their "do NOT flag" lists. Reviewer agents are named `reviewer`; run the selected dimensions in parallel against the full implementations.
- Sections 4–5 — evidence requirement and `must-fix`/`nice-to-have` + `[task-related]`/`[drive-by]` classification.
- Section 6 — coordinator pass: dedupe, reproduce evidence, drop unreproducible issues, emit a verdict.
- Section 7 — flag architectural/cross-system/concurrency concerns as "needs human judgment".

Address surviving `must-fix` `[task-related]` issues; document the rest as deferred.

## Fallback

If git diff fails entirely (not a git repo, or detached HEAD with no fallback branch), review all source files in the working directory as-is.
