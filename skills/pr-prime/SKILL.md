---
name: pr-prime
description: Identify the Pull Request related to the current branch. Read the description and comments to understand the PR context.
---

# PR Prime

Identify the Pull Request related to the current branch. Read the description and comments to understand the changes made in the PR. Note that the description may be partial, outdated, or incomplete. If you need more information, you can ask the author of the PR for clarification or inspect the code changes. Use the command
`gh pr list --head <current_branch> --json number,title,url,state,body,comments,reviews,files --limit 5`
