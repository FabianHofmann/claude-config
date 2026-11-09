---
name: plan-orchestrate
description: "Turn an implementation plan into an orchestration plan: how Claude Code should drive it with subagents, teams, and skills. Use when the user has a plan (file or description) and asks for an orchestration plan, execution strategy, subagent breakdown, or how to drive a multi-phase implementation."
---

# Orchestrate a plan

Append an orchestration strategy to an implementation plan. A later session follows it to drive the work from a lean coordinator context.

## Input and output

- Plan in a file: read it fully, append the strategy to the same file.
- Plan only in conversation: develop plan and strategy in plan mode, get approval, then write one file. Ask for the path if unclear.
- Top of file: `**Baseline commit:** <short-sha> — <subject>`.
- Separate plan and strategy with `---` and a `# Orchestration strategy` heading.
- Open the strategy with: "Follow this strategy; diverge only for a compelling reason, and say why."

## Core rule

Do not default to fan-out. Parallelise only phases whose files are truly independent, at most 4 agents at once. Phases that share invariants (signs, masks, predicates, types, conventions) go to one agent whose prompt lists every invariant and the plan's line references for each file. Phases under ~3 files: one plain subagent, not a fan-out or a review-revise lead.

## What the strategy must say

1. **Dependency shape**: a small ASCII graph and the one concrete reason for each hard ordering.
2. **Per phase**: who executes it (one subagent, parallel subagents, or fork for noisy exploration/baseline capture), which model (Opus default, Sonnet for mechanical work, Fable for hard design), why, and the exit criterion (tests or commands that must pass).
3. **Review gates**: only where phases meet (shared invariants or interfaces) and once before `pr-raise`. Phases run via `sub-implement` are already reviewed. Default `review-full-branch`; `review-diff-branch` for large mechanical diffs.
4. **Commits and isolation**: the coordinator commits after each phase's exit criterion passes; subagents don't commit. Parallel subagents with overlapping files get `isolation: "worktree"`; otherwise everything stays in the current worktree.
5. **PR cut**: one PR, sibling PRs off `main`, or a stack. Stack only phases that depend on each other in order, are each reviewable alone (roughly 300+ diff lines) and leave the code working. Independent phases become siblings, not layers. Per PR: its phases, branch name and base branch. In a stack, each layer's exit criterion includes the full test suite on that branch.
6. **Coordinator context**: what it keeps (plan, phase diff summaries, key artifacts); everything else stays in subagent transcripts.
7. **Kickoff sequence**: numbered steps from branch to `pr-raise`, naming existing skills only (`sub-implement` per phase, `sub-run` for plain tasks, `git-commit`, `ci-monitor`, …) or a plain `general-purpose` or `Explore` agent. For a stack, repeat per layer: branch off the parent layer, implement, commit, review gate with the parent as base, `pr-raise` as draft against the parent. Layers run in order in the current worktree; parallelism stays within a layer. Use plain git (`git rebase --update-refs` to cascade fixes); `gh stack` only if the user asks. `plan-implement` runs this kickoff sequence when it finds the strategy.
8. **Main tradeoff**: one paragraph on the chosen sequencing and PR cut versus the obvious alternative.

Keep it short. Name files and line references from the plan instead of restating them.

## When not to use

- Single small change: implement it.
- No phases or dependency structure: ask the user to firm up the plan first.
- User wants the implementation, not a strategy: use `plan-implement`. It calls this skill itself for phased plans.
