---
name: ci-monitor
description: Get the latest status from the CI build on Github related to the pull request (PR) associated with this branch. Monitor and fix until all checks pass.
---

# CI Monitor

Get the latest status from the CI build on Github related to the pull request (PR) associated with this branch. If you don't find a PR or all checks are passing, return and report your findings. Otherwise, identify the failing check(s) and fix them. Run the whole test suite locally to confirm the fix. Push your changes and monitor the CI build on Github. Only stop when all checks are passing. After all checks pass, write a summary of commits and return.
