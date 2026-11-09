---
name: code-compactify
description: Make a specific function or code block leaner, more modular and more elegant without changing behavior. Use when the user points at code and says make this more elegant, tighten, shorten, compactify, or make it more readable.
allowed-tools: Read, Edit, Bash, Grep, Agent
---

# Compactify

Make the code lean, modular and elegant. Keep behavior identical.

## Aim

- **Kick what is not needed**: dead branches, redundant guards, unused vars and imports, impossible type-hint members, prose that restates the code.
- **Don't repeat**: fold duplicated logic into one place; compute a value once at its definition instead of refining it later.
- **Modular**: split a function that does two things; lift a sprawling nested expression into named one-line locals.
- **Look beyond the lines handed to you**: the best cut may be in the caller, or deleting the concept the code works around. Keep the public contract unless asked.
- **Elegant, not dense**: fewer lines only when intent stays obvious. Names must match what they hold.

## How

Try a few forms, keep the clearest. Prove each by running the tests that cover the code, not by reading it. If nothing covers it, add a test first. Delegate side questions ("is this guard ever hit?") to subagents using scratch scripts. Finish with lint, type-check and the affected suite green, and report which forms you tried and why one won.

## Close

First, end with one sentence a non-expert could repeat out loud to a colleague
and be correct. Skip it when the answer is already one or two sentences.
Then, propose next steps in a enumerated list as "Options for next steps (select)"
