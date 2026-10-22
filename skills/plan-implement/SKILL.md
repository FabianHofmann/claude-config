---
name: plan-implement
description: Implement an implementation plan by splitting it into areas and delegating each to sub-agents. Use when the user has a plan (file or chat) and wants it implemented, not just strategized. For a single task use `sub-implement`; for an execution strategy use `plan-orchestrate`.
---

Implement the referenced plan. If no plan is in your context or referenced as a file, stop and ask the user for it. If the plan exists only in chat, write it to a plan file as `plan-prepare` does. Read the plan file fully.

If the plan contains an `# Orchestration strategy` section, run its kickoff sequence exactly and skip the steps below.

You are the coordinator. Keep your context lean: do not read source files, diffs or test output, and do not redo or re-review agent work. You keep the plan, the area split and the agent reports. Spawn agents with `model: opus`, except the step 5 test runner with `model: sonnet`.

0. Record `git status --porcelain` as the baseline. Files listed there are not part of this run. Pass the list to the agents in steps 4 and 5.
1. Split the plan into areas. Areas are independent only if they share no files, including shared tests, fixtures, `__init__.py` and changelogs, and do not depend on each other's results. If the plan does not name the files per area, have one `Explore` agent return them as a list.
2. Delegate each area. If the plan has a single area, or an area spans about 3 files or more, give it to one `implement-review-revise` lead. Other areas go to one plain `general-purpose` agent. Run at most 4 agents at once. Run dependent areas, and areas that might touch the same files, in order. All agents work in the current worktree.
3. Brief each agent with the plan file path and the line ranges of its area instead of restating them, plus the context from this chat and acceptance criteria. The agents do not see this chat. Require a report of at most 300 words. Tell parallel agents that other agents edit the same worktree: run only their area's tests, do not change git state (stash, checkout, restore, commit), do not format beyond their own files, and report failures outside their area instead of fixing them.
4. If more than one area was implemented, have one `general-purpose` agent review the files the agents report changed for cross-area issues. It reads `/home/fabian/.claude/skills/_review-rubric.md`, applies sections 1 and 3 to 5 itself without spawning agents, reports findings only and edits nothing. Delegate all `must-fix [task-related]` findings to one more `implement-review-revise` lead.
5. Have one `general-purpose` agent run the relevant tests over the combined result and return pass or fail with the failing test names only. If tests fail, delegate the fix to one more lead and repeat this step once. Report remaining failures.
6. Report to the user per area: status, deferred issues and open decisions from the agent reports, plus the final test result.

If an agent returns `blocked`, do not start areas that depend on it. Ask the user, then re-dispatch the area with the answer.
