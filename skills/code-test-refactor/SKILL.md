---
name: code-test-refactor
description: Refactor recently added or modified tests for conciseness, parametrization, and fixture reuse. Use when cleaning up, refactoring, or expanding a Python test suite.
---

Refactor the tests changed in this session. If unsure which those are, scope to `git diff HEAD` (or the staged tests); ask the user if still ambiguous.

Steps:
1. Identify the target tests — recently added or modified test files and functions.
2. Apply the guidelines below.
3. Run the affected tests to confirm they still pass before finishing.

Guidelines:
- Keep tests concise *and* readable — don't trade one for the other.
- Prefer pytest parametrization over repetitive test cases.
- USE TEST CLASSES to group related tests.
- Reuse existing fixtures and helpers; don't duplicate covered scenarios.
- Test behavior and outcomes, not implementation details.
- Avoid mocks except at external boundaries.
- Prefer Arrange / Act / Assert when it improves clarity.
- Watch test execution performance and avoid needlessly slow setups.
