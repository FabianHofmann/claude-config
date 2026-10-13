---
name: sub-implement
description: Delegate a task to the `implement-review-revise` lead agent, which runs implementer, reviewer and reviser sub-agents and returns a compact report. Use when the user wants a task implemented, reviewed and revised without filling the main context.
---

# Implement, review, revise

Spawn one `implement-review-revise` agent for the specified task. Give it the task, all context it needs from this chat (relevant files, decisions, constraints) and clear acceptance criteria. It does not see this chat.

For several independent tasks, spawn one lead per task in parallel. Use `isolation: "worktree"` only if their files overlap.

Relay its report to the user. Do not redo or re-review its work unless the report says `blocked` or lists open decisions.
