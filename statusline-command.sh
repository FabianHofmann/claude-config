
#!/bin/bash

# Read JSON input from stdin
INPUT=$(cat)
MODEL=$(echo "$INPUT" | jq -r '.model.display_name // "Claude"')
CWD=$(echo "$INPUT" | jq -r '.workspace.current_dir // .cwd')
DIR=$(basename "$CWD")

# Get git branch
BRANCH=$(cd "$CWD" 2>/dev/null && git branch --show-current 2>/dev/null)

# Start building statusline
printf "\033[1m$MODEL\033[0m in \033[36m$DIR\033[0m"
[ -n "$BRANCH" ] && printf " on \033[33m⎇ $BRANCH\033[0m"

# Context usage (warn threshold: CLAUDE_CONTEXT_WARN_TOKENS, default 150k)
CTX=$(echo "$INPUT" | jq -r '.context_window.total_input_tokens // 0')
WARN=${CLAUDE_CONTEXT_WARN_TOKENS:-150000}
if [ "$CTX" -gt 0 ]; then
  CTX_K=$(awk -v t="$CTX" 'BEGIN{printf "%.0f", t/1000}')
  if [ "$CTX" -ge "$WARN" ]; then
    printf "  \033[31m⚠ ctx ${CTX_K}k\033[0m"
  elif [ "$CTX" -ge $((WARN * 2 / 3)) ]; then
    printf "  \033[33m◉ ctx ${CTX_K}k\033[0m"
  else
    printf "  \033[32m◉ ctx ${CTX_K}k\033[0m"
  fi
fi

LEDGER="$HOME/.claude/ledger/$(echo "$INPUT" | jq -r '.session_id').md"
if [ -f "$LEDGER" ]; then
  printf "  \033]8;;file://%s\033\\\\\033[35m📋 ledger\033[0m\033]8;;\033\\\\" "$LEDGER"
else
  printf "  \033[2m📋 no ledger\033[0m"
fi

echo
