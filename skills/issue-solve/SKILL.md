---
name: issue-solve
description: Read a GitHub issue and drive it to a fix. Use when the user references an issue number or URL and wants it resolved, or asks to solve, fix, or close an issue.
---

# Solve GitHub Issue

Read the referenced GitHub issue and drive it to a fix.

1. Fetch the issue with `gh issue view <number> --json number,title,body,comments,labels,state,url`. If no number is given, ask which issue.
2. Read the body and every comment. Extract the reported behavior, the expected behavior, and any reproduction steps.
3. Reproduce the problem first. If you cannot reproduce it, report that with the evidence and stop; do not guess a fix.
4. Locate the root cause in the code. State it in one sentence before you change anything.
5. Fix it in a production-ready way. Follow the fail-fast principle and the repository's own style.
6. Run the new and related tests, plus the project's linters and type checks if configured.
7. Reference the issue number in the branch name and, later, in the commit and PR so GitHub links them.

Do not close the issue yourself. Leave that to the merge.
