# Resume from Checkpoint

Restore context from the latest checkpoint or a specified file.

**Usage**: `/resume` or `/resume <checkpoint-file>`

---

## Steps

1. **Find checkpoint**:
   ```bash
   # If no argument, find latest
   ls -t .claude-context/checkpoint-*.md 2>/dev/null | head -1

   # Or use specified file
   ```

2. **If no checkpoint found**: Report and offer to run `/investigate` instead.

3. **Read checkpoint file** and extract:
   - Task/goal description
   - Key files and their status
   - Decisions already made
   - Open questions
   - Next steps

4. **Verify current state matches**:
   ```bash
   git branch --show-current
   git status --short
   ```

   Flag if branch differs or significant uncommitted changes exist.

5. **Prime context** with a summary:

   ```
   Resuming work on: <task>

   Context restored:
   - Key files: <list>
   - Last insight: <most recent insight>
   - Decisions made: <count> decisions preserved

   Ready to continue with: <first next step>
   ```

6. **Load relevant files**: Read the top 2-3 most relevant files from checkpoint to warm up context.

7. **Restore todos**: If checkpoint contains next steps, populate TodoWrite.

---

## Checkpoint Cleanup

After successful task completion, offer to archive old checkpoints:
```bash
mv .claude-context/checkpoint-*.md .claude-context/archive/
```
