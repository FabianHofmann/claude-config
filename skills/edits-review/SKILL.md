---
name: edits-review
description: "Review uncommitted edits the user made manually. Infer intent, review the implementation, and suggest fixes and follow-ups. Use when the user says 'review my edits', 'review my changes', or 'look at what I just changed'."
---

# Review My Edits

Review the user's uncommitted changes, infer what they were trying to do, critique the implementation, and propose fixes plus non-blocking follow-ups.

## Args

- `--fix` — after the review, apply trivial fixes directly (still ask before applying anything non-trivial).
- `--focus <description>` — user-supplied hint about what to pay attention to (e.g. `--focus "error handling in the retry path"`). Bias attention toward this area; still flag critical issues outside it.

## Scope

Default scope is `git diff HEAD` (staged + unstaged). If the working tree is clean, stop and say so.

Sub-scopes via args:
- `--staged` → `git diff --cached`
- `--unstaged` → `git diff`
- bare positional argument → **auto-detect**:
  - If it resolves to an existing file or directory on disk, treat it as a path scope.
  - Otherwise, treat it as `--focus <text>` (free-text attention hint).
  - When ambiguous (e.g. a single token that could be either), prefer the path interpretation only if the path exists; otherwise focus.

## Workflow

1. **Gather context**
   - Run `git status`, `git diff HEAD`, `git log -5 --oneline`, current branch.
   - For each changed file, Read the full file (not just hunks) for surrounding context.
   - Read CLAUDE.md and any nearby convention files.

2. **Infer intent**
   - Cluster the diff into logical groups (e.g. "added retry to API client", "renamed foo→bar in 3 files").
   - State each group's inferred *what* and *why* in one sentence.
   - If `--focus` is provided, treat it as the stated intent for the primary group — do not override it with guesses.

3. **Review** along these axes:
   - **Correctness** — bugs, off-by-one, wrong types, broken invariants.
   - **Consistency** — surrounding patterns, naming, reuse of existing helpers.
   - **Project rules** — CLAUDE.md principles (DRY, KISS, fail-fast, no gentle exception handling, no needless comments, typing, no `getattr`/`hasattr`, etc.).
   - **Tests** — behavior changes without test updates.
   - **Leftovers** — debug prints, commented-out blocks, unused imports.

   With `--focus`: prioritize issues inside the focus area; out-of-focus issues go under a separate "Other observations" subsection and only if non-trivial. Spend more reasoning on focused files/symbols (read callers, check invariants); skim the rest.

4. **Output**

   ```
   ## Intent (inferred)
   - <group 1>: <one-line summary>
   - <group 2>: ...

   ## Issues
   - path/file.py:42 — <problem> → <suggested fix>
   ...

   ## Follow-ups
   - [ ] <non-blocking improvement>
   ...
   ```

   Use `path:line` references so the user can jump. Keep it terse.

5. **Offer, don't auto-apply.** End with: "Want me to apply any of these fixes?" Unless `--fix` was passed, in which case apply trivial fixes immediately and ask about the rest.
