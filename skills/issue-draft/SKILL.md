---
name: issue-draft
description: Draft one or more GitHub issues locally as Markdown files, one per issue, without filing them. Use when the user wants to write up a discussed or referenced issue for review before raising it.
---

# Draft GitHub Issues Locally

Turn the discussed or referenced issue context into local Markdown draft files. Do not file anything on GitHub; that is what `issue-raise` does.

## Target directory

Pick where the drafts go:

1. If `./dev-scripts` exists, use it.
2. Else if `./dev` exists, use it.
3. Else create `./dev` and add a `dev/` line to `.gitignore` (create `.gitignore` if missing). Do not commit the drafts.

## Output

- Write one file per issue. If several issues are discussed, split them; do not merge unrelated problems into one file.
- Name each file `issue-<short-slug>.md`, where the slug comes from the issue title (lowercase, hyphenated).
- If a file with that name already exists, add a numeric suffix rather than overwrite it.

## Content of each draft

Follow the repository's issue template if there is one (look under `.github/`, for example `.github/ISSUE_TEMPLATE/`). If there is none, add a minimal reproducible example anyway.

Be concise, not verbose. Each file contains:

- A `# <title>` line: a short, specific problem statement.
- A one-line note at the top that the draft was written by AI.
- **Context** — what was discussed or referenced, and where it came from.
- **Steps to reproduce** or a minimal reproducible example, when the issue is a bug.
- **Expected vs. actual** behavior, when applicable.
- **Proposed direction**, if one was discussed. Keep it brief; do not over-specify a fix.

After writing, list the file paths you created.
