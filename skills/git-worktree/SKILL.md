---
name: git-worktree
description: Create git worktrees for parallel development. Use when the user wants to work on multiple branches simultaneously, review PRs without stashing, create isolated environments for hotfixes, or compare implementations side-by-side.
---

# Git Worktree Management

The user has a `create_worktree` shell function for creating git worktrees in a parallel directory structure.

## Command

```bash
create_worktree <branch-name> [base-branch]
```

## Behavior

- Creates worktrees at `../<repo-name>-worktrees/<branch-name>` (parallel to main repo)
- Creates the `-worktrees` parent directory if it doesn't exist
- Creates a new git branch with the given name
- Copies untracked files to the new worktree via rsync
- Opens the worktree in Zed

## Examples

```bash
# Branch from current HEAD
create_worktree fix-memory-leak

# Branch from master
create_worktree new-api-endpoint master
```

## Related Commands

```bash
git worktree list          # List all worktrees
git worktree remove <path> # Remove a worktree
git worktree prune         # Clean up stale references
```
