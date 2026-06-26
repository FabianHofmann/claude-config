---
name: fan-out
description: "Fan-Out: Parallel Multi-File Editing. Split a multi-file change across parallel agents. Use when implementing changes that span multiple independent files."
---

# Fan-Out: Parallel Multi-File Editing

Split a multi-file change across parallel agents for maximum efficiency.

**Input**: The user describes the change to implement.

---

## Phase 1: Analysis (Single Agent)

Spawn a `Plan` agent:
```
Analyze this change request: <user's change description>

1. Identify ALL files needing modification
2. Determine dependencies between files (imports, shared types)
3. Group files into independent batches:
   - Files in same batch can be edited in parallel (no cross-imports)
   - Files that import each other must be in same batch
   - Shared types/interfaces go in first batch

Return as structured output:
{
  "summary": "<one sentence change description>",
  "shared_changes": ["<files with shared types, edit first>"],
  "batches": [
    {"id": 1, "files": ["file1.py", "file2.py"], "focus": "<what to change>"},
    {"id": 2, "files": ["file3.py"], "focus": "<what to change>"}
  ],
  "test_files": ["<related test files>"],
  "patterns": ["<patterns to follow from codebase>"]
}
```

---

## Phase 2: Shared Types First (If Needed)

If `shared_changes` is non-empty, edit those files first sequentially.
These define interfaces that parallel agents will depend on.

---

## Phase 3: Parallel Execution

Spawn one agent per batch **in a single message** (max 4 parallel):

### Agent Template (python-expert or appropriate)
```
Implement changes for batch <N>: <focus>

## Overall Task
<user's change description>

## Your Files (ONLY modify these)
<batch file list>

## Context
- Shared types already updated: <list or "none">
- Patterns to follow: <from Phase 1>
- Related files (read-only reference): <adjacent files>

## Requirements
1. Read your assigned files first
2. Implement the required changes
3. Ensure consistency with shared types
4. Add/update type hints
5. Do NOT modify files outside your batch

## Output
- List changes made per file
- Flag any blockers or questions
```

---

## Phase 4: Integration

After all agents complete:

1. **Check for conflicts**:
   ```bash
   git diff --check  # whitespace issues
   ```

2. **Run linter**:
   ```bash
   ruff check --fix . && ruff format .
   ```

3. **Run type checker**:
   ```bash
   mypy <changed files>
   ```

4. **Run related tests**:
   ```bash
   pytest <test_files from Phase 1> -v
   ```

5. **Report integration status**:
   - Files modified per agent
   - Any conflicts or issues
   - Test results

---

## Constraints

- Maximum 4 parallel agents (context limits)
- Each agent only sees its batch files
- Shared interfaces edited sequentially first
- If batching fails, fall back to sequential editing

---

## When NOT to Use

- Changes to < 3 files (just edit directly)
- Heavily interdependent files (can't parallelize)
- Changes requiring iterative refinement
