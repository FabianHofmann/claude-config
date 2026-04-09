---
name: context-preservation
description: Preserve and restore working context across compactions and sessions. Use before /compact, when context is getting full, to save session state, or when resuming work on a task.
---

# Context Preservation

Techniques for managing context in long-running or multi-session work.

## Core Commands

| Command | Purpose |
|---------|---------|
| `/checkpoint` | Quick-save current context to file |
| `/resume` | Restore from latest or specified checkpoint |

## Context Directory Structure

```
.claude-context/
├── checkpoint-2024-01-15T10-30.md    # Quick checkpoints
├── checkpoint-2024-01-15T14-45.md
├── investigation-auth-system.md       # Deep investigation results
├── investigation-api-routes.md
├── exploration-<branch>.md            # Branch-specific context
└── archive/                           # Completed task checkpoints
```

## When to Checkpoint

### Mandatory
- Before running `/compact`
- Before spawning sub-agents that might fill context
- Before switching to unrelated work
- End of work session

### Recommended
- After completing exploration phase
- After making key architectural decisions
- After successful test run (known good state)
- Every ~30 minutes of active work

## Checkpoint Content Hierarchy

### Essential (always save)
1. Current task/goal in one sentence
2. Branch name and recent commits
3. 3-5 most important file paths
4. Uncommitted changes summary

### Important (save when relevant)
5. Key decisions with rationale
6. Patterns discovered
7. Open questions/blockers
8. Next steps ordered by priority

### Optional (save for complex tasks)
9. Dependency map
10. Test status
11. Related issues/PRs
12. Performance notes

## Restoration Strategy

### Quick Resume (< 5 min break)
1. Read checkpoint summary
2. Continue from next steps

### Session Resume (hours/days gap)
1. Read checkpoint fully
2. Verify git state matches
3. Re-read top 2-3 key files
4. Validate assumptions still hold

### Context Recovery (after /compact)
1. Read checkpoint
2. Prime with: "Resuming: [task]. Context: [key files]. Continue with: [next step]"
3. Avoid re-exploring already-discovered information

## Integration with Other Commands

### With `/investigate`
Investigation results are auto-saved to `.claude-context/investigation-<topic>.md`.
Reference these in checkpoints rather than duplicating.

### With `/implement-feature`
The workflow should auto-checkpoint after:
- Phase 1 (exploration)
- Phase 3 (implementation)
- Phase 5 (review)

### With `/fan-out`
Before parallel agent spawn, checkpoint the plan.
After integration, checkpoint the result.

## Anti-Patterns

- Checkpointing every small change (overhead)
- Giant checkpoints with full file contents (defeats purpose)
- Not checking git state on resume (stale context)
- Ignoring checkpoints and re-exploring (wasted work)

## Quick Reference

```bash
# Save context
/checkpoint

# Resume from latest
/resume

# Resume from specific checkpoint
/resume .claude-context/checkpoint-2024-01-15T10-30.md

# List checkpoints
ls -lt .claude-context/checkpoint-*.md

# Clean old checkpoints (keep last 5)
ls -t .claude-context/checkpoint-*.md | tail -n +6 | xargs rm -f
```
