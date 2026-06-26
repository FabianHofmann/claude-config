---
name: diff-review
description: "Run parallel reviewer agents to review the current git diff (`git diff HEAD`). Use when reviewing staged or recent changes for correctness, security, code quality, types, and test coverage."
---

# Diff Review

Review the current git diff (`git diff HEAD`).

## Scope & context

1. Run `git diff HEAD --name-only` to list changed files; apply the ignore filter in the shared rubric.
2. Run `git diff HEAD` for the changes. The diff alone is rarely enough context — reviewers must read surrounding code, call sites, and tests as needed to satisfy the evidence requirement.

## Apply the shared rubric

Read **`/home/fabian/.claude/skills/_review-rubric.md`** and follow it in full:
- Section 2 — risk-tier the number of reviewers to the diff size and sensitivity.
- Section 3 — the reviewer dimensions and their "do NOT flag" lists. Reviewer agents are named `reviewer`; run the selected dimensions in parallel.
- Sections 4–5 — evidence requirement and `must-fix`/`nice-to-have` + `[task-related]`/`[drive-by]` classification.
- Section 6 — coordinator pass: dedupe, reproduce evidence, drop unreproducible issues, emit a verdict.
- Section 7 — flag architectural/cross-system/concurrency concerns as "needs human judgment".

Address surviving `must-fix` `[task-related]` issues; document the rest as deferred.
