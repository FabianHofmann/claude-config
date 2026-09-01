---
name: review-full
description: "Absolute Code Review: read full implementations of changed files and run parallel reviewers. Use when doing a thorough review of HEAD changes with full file context."
---

# Absolute Code Review

Thorough review of HEAD changes with **full file context** — reviewers judge the complete implementation, not just the hunks.

## Scope & context

1. Run `git diff HEAD --name-only` to list changed files; apply the ignore filter in the shared rubric.
2. For each surviving source file, Read the **full current implementation**, not just the changed lines.
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

If changed files can't be determined via `git diff HEAD` (not a git repo, git unavailable), review all source files in the working directory as-is.
