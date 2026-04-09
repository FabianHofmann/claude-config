# Quick Exploration

Quick exploration of a specific topic.
---

## Steps (Sequential, Fast)

1. **Find relevant files** (max 10):
   ```bash
   # By name
   find . -type f \( -name "*.py" -o -name "*.ts" -o -name "*.go" \) | xargs grep -l "$ARGUMENTS" 2>/dev/null | head -10

   # By content
   grep -r --include="*.py" --include="*.ts" -l "$ARGUMENTS" . | head -10
   ```

2. **Rank by relevance**:
   - Files with topic in name > files with topic in content
   - src/ files > test files
   - Recently modified > old files

3. **Quick scan top 3 files**:
   - Read first 50 lines of each
   - Identify main purpose
   - Note key functions/classes

4. **Output** (keep under 100 words):
   ```
   ## $ARGUMENTS

   **Primary**: path/to/main/file.py - <purpose>
   **Related**:
   - path/to/other.py - <purpose>
   - path/to/another.py - <purpose>

   **Key functions**: func1(), func2(), ClassName
   **Start here**: path/to/main/file.py:42 (function_name)
   ```

---

## When to Use

- Quick lookup before making a small change
- Verifying a pattern exists before implementing
- Finding where something is defined
- NOT for deep understanding (use `/investigate` for that)
