# Quick Context Checkpoint

Save current working context for later restoration. No arguments needed.

---

## Steps

1. **Create context directory** if needed:
   ```bash
   mkdir -p .claude-context
   ```

2. **Gather state**:
   ```bash
   git branch --show-current
   git log --oneline -5
   git diff --stat HEAD
   ```

3. **Extract from conversation**:
   - Current task/goal (infer from recent messages)
   - Files read or modified this session
   - Key decisions or insights discovered
   - Current todo list items
   - Blockers or open questions

4. **Write checkpoint** to `.claude-context/checkpoint-<timestamp>.md`:

```markdown
# Checkpoint: <task summary>
**Saved**: <ISO timestamp>
**Branch**: <branch name>

## Current Goal
<one sentence>

## Files Touched
| File | Status |
|------|--------|
| path | read / modified / created |

## Key Insights
- <insight 1>
- <insight 2>

## Decisions Made
- <decision>: <rationale>

## Open Questions
- [ ] <question 1>
- [ ] <question 2>

## Next Steps
1. <next action>
2. <following action>

## Recent Commits (for context)
<git log output>

## Uncommitted Changes
<git diff --stat output>
```

5. **Confirm**: Report checkpoint file path and summary.

---

## Usage

Run before:
- `/compact` to preserve context
- Switching to unrelated work
- Ending a session
- Spawning long-running sub-agents

Restore with `/resume`.
