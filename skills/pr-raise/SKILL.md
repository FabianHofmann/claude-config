---
name: pr-raise
description: Raise a pull request with the implemented changes. Prioritize pushing to origin and not raising from a personal fork.
---

# Raise Pull Request

Raise a pull request with the implemented changes. Prioritize pushing to origin and not raising from a personal fork. If you are unsure about which uncommitted changes to include, ask to the user for confirmation. In the body of the pull request, write a summary in solid text form or bullet points, following the PR template of the repo (most likely in .github/templates/pull_request_template.md). Use easy readable language but professional tone. Insert a note at the top that the content was created by AI.

For a stacked PR (the branch builds on another unmerged branch), pass `--base <parent-branch>` and open it as a draft while the parent PR is open. Add a line below the AI note: "Stack <n>/<total>, depends on #<parent-pr>". Edit the parent PR body to link this PR as the next layer. Use `gh stack` only if the user or repo asks for it.
