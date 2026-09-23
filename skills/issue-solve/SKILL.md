---
name: issue-solve
description: Read a GitHub issue and drive it to a fix. Use when the user references an issue number or URL and wants it resolved, or asks to solve, fix, or close an issue.
---

# Solve GitHub Issue

Read the referenced GitHub issue and drive it to a fix.

1. Fetch the issue with `gh issue view <number> --json number,title,body,comments,labels,state,url`. If no number is given, ask which issue.
2. Read the body and every comment. Extract the reported behavior, the expected behavior, and any reproduction steps.
3. Checkout a branch whose names includes the issue number. If possible rename the current session to the same name.  
4. Reproduce the problem first. If you cannot reproduce it, report that with the evidence and stop; do not guess a fix.
5. Locate the root cause in the code. State it in one sentence before you change anything.
6. Fix it in a production-ready way. Follow the fail-fast principle and the repository's own style. Don't commit changes.
7. Run the new and related tests, plus the project's linters and type checks if configured.
8. Fix type hints.
9. Run the /review-diff skill. Fix all major issues, pick the nice-to-have you think are sensible.
10. Commit changes.
11. Report back a summary of changes and remaining (un)related issues. Ask to raise a pull request + the /ci-monitor skill or do potential follow-ups. 

Do not close the issue yourself. Leave that to the merge.
