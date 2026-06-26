---
name: diff-review-branch
description: "Run parallel reviewer agents to review the current git diff against master/main. Use when reviewing branch changes before merging."
---

# Diff Review (Branch)

Review the branch diff against the baseline (`git diff main`, or `git diff master` if `main` doesn't exist).

## Scope & context

1. Run `git diff main --name-only` (fall back to `master`) to list changed files; apply the ignore filter in the shared rubric.
2. Run `git diff main` (or `master`) for the changes. The diff alone is rarely enough context — reviewers must read surrounding code, call sites, and tests as needed to satisfy the evidence requirement.

## Apply the shared rubric

Read **`/home/fabian/.claude/skills/_review-rubric.md`** and follow it in full:
- Section 2 — risk-tier the number of reviewers to the diff size and sensitivity.
- Section 3 — the reviewer dimensions and their "do NOT flag" lists. Reviewer agents are named `reviewer`; run the selected dimensions in parallel.
- Sections 4–5 — evidence requirement and `must-fix`/`nice-to-have` + `[task-related]`/`[drive-by]` classification.
- Section 6 — coordinator pass: dedupe, reproduce evidence, drop unreproducible issues, emit a verdict.
- Section 7 — flag architectural/cross-system/concurrency concerns as "needs human judgment".

Address surviving `must-fix` `[task-related]` issues; document the rest as deferred.
