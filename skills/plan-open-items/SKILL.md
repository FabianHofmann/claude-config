---
name: plan-open-items
description: Summarize all unaddressed and open items of the current session, such as open PRs, open issues, untracked related and unrelated issues, unconfirmed decisions, breaking changes and cleanup. Use when the user asks what is still open, unaddressed, pending or left to do in this session, or wants a wrap-up before closing it.
---

# Open items of the session

List everything from **this session** that is not yet closed. Do not report finished and confirmed work.

## Gather

1. Start from the latest injected "Session ledger" in context. Then scan the whole conversation, including earlier summarized context, for anything the ledger misses: every PR, issue, finding and `[D<n>]` / `[I<n>]` / `[U<n>]` / `[B<n>]` / `[P<n>]` code.
2. Check the live state of each referenced PR and issue with one `gh` call each: `gh pr view <n> --json state,title,url,reviewDecision,statusCheckRollup` or `gh issue view <n> --json state,title,url`. Drop items that are merged or closed, unless they belong to a section below.
3. Check local leftovers: `git status --short`, `git stash list`, `git worktree list`, `git branch --no-merged`, running background tasks and monitors, scratch files you created.

## Report

Use these sections in this order. Write `None.` for an empty section. Keep one line per item.

1. **Open PRs**: number, title, link, and what blocks it (review, failing CI, conflicts, unpushed commits).
2. **Open issues**: number, title, link, and the next step.
3. **Related issues not on GitHub**: reuse the existing `I<n>` codes from the session. Give new ones the next free number. Add one line on impact.
4. **Unrelated issues not on GitHub**: same with `U<n>` codes.
5. **Merged or implemented without an explicit decision from me**: every change, merge, push, design choice or default you picked that the user did not explicitly approve. Say what you chose and the alternative.
6. **Breaking changes**: API, config, data model or behavior changes that affect users or callers. Mark if release notes or a migration note is still missing.
7. **Cleanup**: uncommitted files, stashes, stale worktrees and branches, background tasks, temporary files, debug code, TODOs you left.

## Rules

- Be honest. Include items you deferred, skipped or forgot. Do not soften them.
- Do not fix anything. Only report.
- Never invent items. Each item must trace back to the session or to a command output.
- End with a numbered list of proposed next steps, ordered by priority.
