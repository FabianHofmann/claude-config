---
name: plan-voice-handoff
description: Summarize the current session and open it as a prefilled chat in Claude Desktop, to continue the discussion by voice. Use when the user wants to talk through the session in the desktop app, continue by voice, or hand the context over to Claude Desktop.
---

# Voice handoff to Claude Desktop

Write a summary of this session that a conversation partner in Claude Desktop can discuss with the user. The partner has no access to the files or the repo.

## Content

Write plain Markdown, under 10,000 characters. Claude Desktop cuts the prefill at about 14,000 characters. Open with one line telling the partner its role: "You are my sparring partner. Here is the context of a coding session. Help me think through the open questions."

Then, dropping empty sections:

1. **Goal** — what the user wants to achieve, in plain words.
2. **Done** — what works now.
3. **Decisions** — settled choices and their rationale.
4. **Open questions** — the unresolved points, the core of the conversation.
5. **Next steps** — short, ordered.

Explain concepts instead of pointing at file paths or line numbers. Mention a file or function only by name when the discussion needs it.

## Open

Write the summary to `<scratchpad>/voice-handoff.md`, then run:

```bash
f=<scratchpad>/voice-handoff.md
[ "$(wc -m < "$f")" -le 10000 ] || { echo "voice-handoff.md exceeds 10000 characters, shorten it" >&2; exit 1; }
xdg-open "claude://claude.ai/new?surface=chat&q=$(jq -sRr @uri < "$f")"
```

Tell the user the chat is prefilled in Claude Desktop and they can send it or switch to voice.
