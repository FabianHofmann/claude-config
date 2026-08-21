---
name: prompt-continuation
description: Write a prompt for a new session contextualizing the agent with the task and its continuation. Use when the user asks for a handoff prompt, a continuation prompt, or wants to resume this work in a fresh session.
---

# Prompt continuation

Write a self-contained prompt that lets a fresh agent with **zero context** continue the current task.

## Rules

- Address the new agent directly in the imperative ("Continue implementing X"). Not a changelog of this session.
- Absolute paths only. No "as we discussed", no pronouns pointing back at this conversation.
- Carry decisions already made, so the new agent does not re-litigate them.
- Keep it under ~40 lines. It costs the new session context.
- Output a single fenced code block, nothing else. Only write a file if the user asks.

## Content

Capture the baseline first: `git rev-parse --short HEAD` and `git status --short`.

If the task is tied to a GitHub issue or PR, add its number and URL, plus any review feedback or acceptance criteria still open. Do not go hunting: use what is already in context, or a single `gh pr view` on the current branch. Skip this entirely for local-only work.

Then cover, dropping any section that is genuinely empty:

1. **Goal** — the original request, restated.
2. **Baseline** — commit hash and uncommitted files.
3. **Done** — what already works.
4. **Remaining** — concrete next steps, ordered.
5. **Key files** — absolute paths with a one-line role each.
6. **Decisions** — settled choices and their rationale.
7. **Dead ends** — what was tried and rejected, so it is not retried.
8. **GitHub** — issue/PR number, URL, and open review points, when relevant.
9. **Verify** — the exact test or run command.
