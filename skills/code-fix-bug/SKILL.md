---
name: code-fix-bug
description: Fix a reported bug in a production-ready way. Use when the user reports a bug, describes broken behavior, or asks for a bug fix.
---

# Bug Fix

## Instructions

1. Identify the issue and gather enough context. If the bug or its location is ambiguous, ask before proceeding. Fetch origin and branch off the latest `master`/`main`.
2. Follow TDD: first write a test that reproduces the bug, confirm it fails for the stated reason, then fix the bug and confirm the test passes.
3. Run the /code-compactify and /code-test-refactor skills. Run the new and related tests to check for regressions.
4. Run the /review-diff skill. Fix nice-to-have issues that are cheap and in-scope; defer the rest with a one-line reason.
5. Run /code-compactify again.
6. Run the full test suite, including mypy and ruff if configured in the project.
7. Run the /doc-release-notes skill.
8. Commit the changes.

## Report

Report to me in clear, readable language:
- what the issue was and the root cause
- what changes were made to fix the bug
- which nice-to-have points from the review were included, and which were deferred (with reasons)
