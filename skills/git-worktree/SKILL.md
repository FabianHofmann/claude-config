---
name: git-worktree
description: Create a git worktree on a new branch, move this chat's recorded directory to it, then re-root the current Zed window onto it. The editor surface and the resumed Claude both land on the worktree, aligned, with no manual resume step. Use when the user explicitly asks to branch off development into another worktree.
---

# Git Worktree Management

Create a worktree on a new branch at Zed's default worktree location, then re-root
the current Zed window onto it. The Zed surface (file tree, tabs, git panel) and the
resumed Claude end up on the same checkout, with matching working directories.

The flow has two phases with one pause. The pause is unavoidable: re-rooting kills
this terminal thread, and only a `/cd` typed by the user can move the session's
recorded directory onto the worktree before it dies. Everything else is automatic.
The re-rooted window auto-resumes this chat, so there is no manual resume step.

Run each phase as a single bash call. Do not inspect or verify between steps.

## Phase 1: create and hand off `/cd`

Pick a sensible branch name from the task. Base off `origin/main` unless the user
names another base. Then run one call: create the worktree with the user-defined
`create_worktree` shell function, capture the path it reports, and copy a ready `/cd`
command to the clipboard. Never recompute the path yourself; the function is the
single source of truth.

```bash
worktree=$(create_worktree <branch> origin/main | sed -n 's/^WORKTREE_PATH=//p')
[ -n "$worktree" ] || echo "STALE: no WORKTREE_PATH. Open a fresh terminal so the updated shell function loads, then retry."
printf '/cd %s' "$worktree" | wl-copy
```

`create_worktree` places the worktree at `../worktrees/<branch>` relative to the main
repo (Zed's `git.worktree_directory` default), copies uncommitted changes over
(modified tracked files and untracked files), and prints its final path as a
`WORKTREE_PATH=...` line.

If the command prints `STALE`, the running shell still has an old snapshot of the
function. Stop and tell the user to open a fresh terminal, then rerun the skill. Do
not paste an empty `/cd`.

Tell the user: paste the clipboard into this Claude input and press enter. This moves
the chat's transcript and recorded directory onto the worktree, keeping full history.
Do not re-root yet. Then stop and wait. Control returns on the next turn.

## Phase 2: re-root, auto-resume

After `/cd`, `git rev-parse --show-toplevel` returns the worktree. Run one call: drop
a single-use resume sentinel for the `co` wrapper, then re-root the current Zed window
with `zed -e` (open in the existing window, not a new one).

```bash
worktree=$(git rev-parse --show-toplevel)
printf '%s\t%s\t%s' "$CLAUDE_CODE_SESSION_ID" "$worktree" "$(date +%s)" \
    > "${XDG_RUNTIME_DIR:-/tmp}/claude-resume-next"
zed -e "$worktree"
```

Re-rooting kills this terminal thread. The re-rooted window auto-starts `co` in the
worktree. The `co` wrapper sees the fresh sentinel for this directory and boots
straight into `claude --resume`, so the chat comes back with full history, rooted on
the worktree, aligned with the editor. No paste is needed.

The sentinel is single-use and expires in 90 seconds, so an unrelated new window never
picks it up. If `co` was started before the sentinel was written, or later than 90
seconds, the window starts a fresh Claude instead; recover by pasting
`/resume <CLAUDE_CODE_SESSION_ID>` into it.
