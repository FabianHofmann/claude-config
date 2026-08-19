#!/bin/bash
# Warns when the session context grows past a threshold (default 150k tokens).
set -uo pipefail

THRESHOLD=${CLAUDE_CONTEXT_WARN_TOKENS:-150000}
STEP=${CLAUDE_CONTEXT_WARN_STEP:-25000}

INPUT=$(cat)
TRANSCRIPT=$(jq -r '.transcript_path // empty' <<<"$INPUT")
SESSION=$(jq -r '.session_id // "unknown"' <<<"$INPUT")
[ -f "$TRANSCRIPT" ] || exit 0

TOKENS=$(tac "$TRANSCRIPT" | grep -m1 '"usage"' \
  | jq -r '(.message.usage // .usage) | (.input_tokens + .cache_creation_input_tokens + .cache_read_input_tokens)' 2>/dev/null)
[[ "$TOKENS" =~ ^[0-9]+$ ]] || exit 0
[ "$TOKENS" -lt "$THRESHOLD" ] && exit 0

STATE_DIR="${TMPDIR:-/tmp}/claude-context-warn"
mkdir -p "$STATE_DIR"
STATE="$STATE_DIR/$SESSION"
LAST=$(cat "$STATE" 2>/dev/null || echo 0)
[ "$TOKENS" -lt "$((LAST + STEP))" ] && exit 0
echo "$TOKENS" > "$STATE"

PRETTY=$(awk -v t="$TOKENS" 'BEGIN{printf "%.0fk", t/1000}')
LIMIT=$(awk -v t="$THRESHOLD" 'BEGIN{printf "%.0fk", t/1000}')
jq -n --arg m "⚠ Context is at $PRETTY tokens (threshold $LIMIT). Consider /compact, /clear, or offloading to a subagent." \
  '{systemMessage: $m}'
