#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
import json
import re
import sys
from pathlib import Path
from typing import Any

HEADER = "Session ledger (open items, source of truth for codes):"
EMPTY = "Session ledger: no open items."
ORDER = "GPDBIU"
STATUS = {"+": "open", "-": "resolved", "x": "dropped"}
ITEM = re.compile(r"([+\-x~])([GPDBIU]\d+)(?:\s+(.*))?")
DEFINED = re.compile(r"\[([GPDBIU]\d+)\]")
GRAMMAR = "Ledger: +D3 text | -U1 | xI2 reason | ~B1 new text"

Record = dict[str, Any]
Op = tuple[str, str, str]
State = dict[str, tuple[str, str]]


def fail(message: str) -> None:
    sys.exit(f"ledger: {message}")


def require(data: Record, keys: list[str]) -> None:
    missing = [k for k in keys if k not in data]
    if missing:
        fail(f"missing hook input fields: {missing}")


def load(path: Path) -> list[Record]:
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def active_chain(records: list[Record]) -> list[Record]:
    by_uuid = {r["uuid"]: r for r in records if "uuid" in r}
    tails = [r for r in records if r.get("type") in ("user", "assistant") and not r["isSidechain"]]
    if not tails:
        return []
    chain = [tails[-1]]
    while True:
        record = chain[-1]
        parent = record["parentUuid"]
        if parent is None and record.get("subtype") == "compact_boundary":
            parent = record["logicalParentUuid"]
        if parent is None:
            return chain[::-1]
        if parent not in by_uuid:
            fail(f"parent {parent} of {record['uuid']} not in transcript")
        chain.append(by_uuid[parent])


def assistant_texts(chain: list[Record]) -> list[str]:
    return [
        block["text"]
        for r in chain
        if r["type"] == "assistant"
        for block in r["message"]["content"]
        if block["type"] == "text"
    ]


def parse(text: str) -> tuple[list[Op], list[str]]:
    ops: list[Op] = []
    bad: list[str] = []
    for line in text.splitlines():
        line = line.strip()
        if not line.startswith("Ledger:"):
            continue
        for item in line.removeprefix("Ledger:").split(" | "):
            item = item.strip()
            match = ITEM.fullmatch(item)
            if match is None or (match[1] in "+~" and not match[3]):
                bad.append(item)
                continue
            ops.append((match[1], match[2], match[3] or ""))
    return ops, bad


def fold(ops: list[Op], state: State | None = None) -> State:
    state = dict(state or {})
    for op, code, text in ops:
        status, old = state.get(code, ("open", ""))
        if op == "~":
            state[code] = (status, text)
        else:
            state[code] = (STATUS[op], text or old)
    return state


def sort_key(code: str) -> tuple[int, int]:
    return ORDER.index(code[0]), int(code[1:])


def render(state: State) -> str:
    open_items = sorted((c for c, (s, _) in state.items() if s == "open"), key=sort_key)
    if not open_items:
        return ""
    return "\n".join([HEADER, *(f"{c}: {state[c][1]}" for c in open_items)])


def view(state: State) -> str:
    closed = sorted((c for c, (s, _) in state.items() if s != "open"), key=sort_key)
    lines = [render(state) or EMPTY]
    if closed:
        lines += ["", "Resolved/dropped:", *(f"{c} ({state[c][0]}): {state[c][1]}" for c in closed)]
    return "\n".join(lines) + "\n"


def write_view(session_id: str, state: State) -> None:
    if Path(session_id).name != session_id:
        fail(f"invalid session_id {session_id!r}")
    directory = Path.home() / ".claude" / "ledger"
    directory.mkdir(parents=True, exist_ok=True)
    (directory / f"{session_id}.md").write_text(view(state))


def chain_ops(chain: list[Record]) -> list[Op]:
    return [op for text in assistant_texts(chain) for op in parse(text)[0]]


def latest_injection(chain: list[Record]) -> str | None:
    for record in reversed(chain):
        if record.get("subtype") == "compact_boundary":
            return None
        attachment = record.get("attachment") if record["type"] == "attachment" else None
        if attachment is None or attachment["type"] != "hook_additional_context":
            continue
        for content in reversed(attachment["content"]):
            if content.startswith((HEADER, EMPTY)):
                return content
    return None


def inject(event: str, text: str) -> None:
    print(json.dumps({"hookSpecificOutput": {"hookEventName": event, "additionalContext": text}}))


def prompt(data: Record) -> None:
    chain = active_chain(load(Path(data["transcript_path"])))
    state = fold(chain_ops(chain))
    write_view(data["session_id"], state)
    rendering = render(state)
    last = latest_injection(chain)
    if rendering:
        if rendering != last:
            inject("UserPromptSubmit", rendering)
    elif last is not None and last != EMPTY:
        inject("UserPromptSubmit", EMPTY)


def compact(data: Record) -> None:
    state = fold(chain_ops(active_chain(load(Path(data["transcript_path"])))))
    write_view(data["session_id"], state)
    rendering = render(state)
    if rendering:
        inject("SessionStart", rendering)


def stop(data: Record) -> None:
    require(data, ["last_assistant_message", "stop_hook_active"])
    message = data["last_assistant_message"] or ""
    own_ops, bad = parse(message)
    state = fold(own_ops, fold(chain_ops(active_chain(load(Path(data["transcript_path"]))))))
    write_view(data["session_id"], state)
    if data["stop_hook_active"]:
        return
    missing = sorted(set(DEFINED.findall(message)) - state.keys(), key=sort_key)
    if not missing and not bad:
        return
    problems = []
    if missing:
        problems.append(f"codes defined without a ledger entry: {', '.join(missing)}")
    if bad:
        problems.append(f"malformed ledger items: {bad}")
    reason = f"Ledger check: {'; '.join(problems)}. Append one delta line as the last line, grammar: {GRAMMAR}"
    print(json.dumps({"decision": "block", "reason": reason}))


COMMANDS = {"prompt": prompt, "compact": compact, "stop": stop}


def main() -> None:
    if len(sys.argv) != 2 or sys.argv[1] not in COMMANDS:
        fail(f"usage: ledger.py {{{','.join(COMMANDS)}}}")
    data = json.load(sys.stdin)
    require(data, ["session_id", "transcript_path"])
    COMMANDS[sys.argv[1]](data)


if __name__ == "__main__":
    main()
