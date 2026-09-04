---
name: git-worktree
description: Create a git worktree on a new branch and open it in Zed, so the editor surface and Claude both move to the worktree. Use when the user explicitly asks to branch off development into another worktree.
---

# Git Worktree Management

Create a worktree on a new branch at Zed's default worktree location, then re-root
the current Zed window onto it. This keeps the Zed surface (file tree, tabs, git
panel) and Claude on the same checkout, without spawning a new window.

Do not use `/cd` for this. `/cd` moves Claude's working directory but leaves the
Zed window rooted on the original repo, so the two surfaces drift apart.

## Steps

1. Pick a sensible branch name from the task. Base off `origin/main` unless the
   user names another base.

2. Create the worktree with the user-defined `create_worktree` shell function. It
   creates the worktree at `../worktrees/<branch>` (Zed's `git.worktree_directory`
   default) and copies untracked files over.

   ```bash
   create_worktree <branch> origin/main
   ```

3. Re-root the current Zed window onto the worktree with `zed -e` (open in the
   existing window, not a new one). Its path is `../worktrees/<branch>` relative to
   the repo root.

   ```bash
   repo_root=$(git rev-parse --show-toplevel)
   zed -e "$(dirname "$repo_root")/worktrees/<branch>"
   ```

4. Re-rooting kills this terminal thread, but the re-rooted window auto-starts a
   fresh Claude in the worktree's agent panel. Copy the `/resume <id>` slash command
   to the clipboard so the user pastes it straight into that Claude input.
   `/resume <id>` finds the session from any directory (Claude Code 2.1.223+), so it
   switches the fresh session to this chat with full history.

   ```bash
   printf '/resume %s' "$CLAUDE_CODE_SESSION_ID" | wl-copy
   ```

   Tell the user: in the re-rooted window, paste into the Claude input and press
   enter. The chat resumes, now rooted in the worktree.
