---
name: plan-voice-handoff
description: Summarize the current session and open it as a prefilled chat in Claude Desktop, to continue the discussion by voice. Use when the user wants to talk through the session in the desktop app, continue by voice, or hand the context over to Claude Desktop.
---

# Voice handoff to Claude Desktop

Write a summary of this session that a conversation partner in Claude Desktop can discuss with the user. The partner cannot read local files. Everything it needs to look up must be reachable on the internet, so the summary carries URLs.

## Content

Write plain Markdown, under 10,000 characters. Claude Desktop cuts the prefill at 14,336 characters. Open with one line telling the partner its role: "You are my sparring partner. Here is the context of a coding session. Help me think through the open questions. Fetch the linked URLs whenever you need details."

Then, dropping empty sections:

1. **Goal** — what the user wants to achieve, in plain words.
2. **Done** — what works now.
3. **Decisions** — settled choices and their rationale.
4. **Open questions** — the unresolved points, the core of the conversation.
5. **Next steps** — short, ordered.
6. **Links** — one line per URL with what the partner finds there.

Explain concepts instead of pointing at local paths or line numbers. Put a URL next to every file, function, issue, PR or library the discussion needs.

## Links

Collect URLs the partner can open without logging in:

- **Repo, issue, PR**: `gh repo view --json url,visibility`, `gh pr view --json url`, and issue URLs already in context.
- **Code**: raw permalinks pinned to a pushed commit, `https://raw.githubusercontent.com/<owner>/<repo>/<sha>/<path>`. Raw files fetch cleaner than the GitHub HTML view. Use the latest commit that `git branch -r --contains <sha>` shows on the remote.
- **Docs**: official documentation pages of the libraries, APIs and tools involved.

Only use URLs you saw in this session or got from `gh` or `git`. Never guess a URL. Local-only changes have no URL: describe them in the text, and list them under Open questions as "not pushed yet". If the repo is private, say so in the Links section, because the partner cannot fetch its files.

## Open

Write the summary to `<scratchpad>/voice-handoff.md`, then run:

```bash
f=<scratchpad>/voice-handoff.md
[ "$(wc -m < "$f")" -le 10000 ] || { echo "voice-handoff.md exceeds 10000 characters, shorten it" >&2; exit 1; }
xdg-open "claude://claude.ai/new?surface=chat&q=$(jq -sRr @uri < "$f")"
```

Tell the user the chat is prefilled in Claude Desktop. Voice mode cannot start from the link: they click the microphone after sending.
