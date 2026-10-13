import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any

import pytest

SCRIPT = Path(__file__).parent.parent / "hooks" / "ledger.py"
HEADER = "Session ledger (open items, source of truth for codes):"
EMPTY = "Session ledger: no open items."


class Transcript:
    def __init__(self) -> None:
        self.records: list[dict[str, Any]] = []
        self.tail: str | None = None

    def add(self, kind: str, parent: str | None = None, **fields: Any) -> str:
        uuid = f"u{len(self.records)}"
        parent = self.tail if parent is None else parent
        record = {"type": kind, "uuid": uuid, "parentUuid": parent, "isSidechain": False, **fields}
        self.records.append(record)
        self.tail = uuid
        return uuid

    def user(self, text: str = "go", parent: str | None = None) -> str:
        return self.add("user", parent, message={"role": "user", "content": text})

    def assistant(self, *texts: str, parent: str | None = None) -> str:
        content = [{"type": "text", "text": t} for t in texts]
        return self.add("assistant", parent, message={"role": "assistant", "content": content})

    def injection(self, text: str) -> str:
        attachment = {"type": "hook_additional_context", "content": [text], "hookEvent": "UserPromptSubmit"}
        return self.add("attachment", attachment=attachment)

    def compact(self) -> str:
        uuid = f"u{len(self.records)}"
        record = {
            "type": "system",
            "subtype": "compact_boundary",
            "uuid": uuid,
            "parentUuid": None,
            "logicalParentUuid": self.tail,
            "isSidechain": False,
        }
        self.records.append(record)
        self.tail = uuid
        return uuid

    def write(self, path: Path) -> Path:
        path.write_text("\n".join(json.dumps(r) for r in self.records) + "\n")
        return path


def run(sub: str, transcript: Transcript, home: Path, **extra: Any) -> subprocess.CompletedProcess[str]:
    path = transcript.write(home / "t.jsonl")
    data = {"session_id": "s1", "transcript_path": str(path), **extra}
    env = {**os.environ, "HOME": str(home)}
    return subprocess.run(
        [sys.executable, str(SCRIPT), sub], input=json.dumps(data), capture_output=True, text=True, env=env
    )


def context(result: subprocess.CompletedProcess[str]) -> str | None:
    assert result.returncode == 0, result.stderr
    if not result.stdout:
        return None
    return json.loads(result.stdout)["hookSpecificOutput"]["additionalContext"]


@pytest.mark.parametrize(
    ("answers", "expected"),
    [
        (["Ledger: +D3 Pick store format"], [HEADER, "D3: Pick store format"]),
        (["Ledger: +U1 a | +D1 b | +P1 c | +I1 d | +B1 e | +G1 f"], [HEADER, "G1: f", "P1: c", "D1: b", "B1: e", "I1: d", "U1: a"]),
        (["Ledger: +D1 a | +D2 b", "Ledger: -D1 | xD2 gone"], None),
        (["Ledger: +B1 old", "text\nLedger: ~B1 new"], [HEADER, "B1: new"]),
        (["Ledger: +U1 a | +I1 b", "Ledger: >U1 org/repo#12"], [HEADER, "I1: b"]),
        (["Ledger: +U1 a | >U2"], [HEADER, "U1: a"]),
        (["Ledger: +D10 ten | +D2 two"], [HEADER, "D2: two", "D10: ten"]),
        (["mentions Ledger: +D1 inline", "Ledger: +D1"], None),
    ],
)
def test_fold_grammar(tmp_path: Path, answers: list[str], expected: list[str] | None) -> None:
    t = Transcript()
    for answer in answers:
        t.user()
        t.assistant(answer)
    assert context(run("prompt", t, tmp_path)) == (expected and "\n".join(expected))


def test_rewind_branch_ignored(tmp_path: Path) -> None:
    t = Transcript()
    t.user()
    fork = t.assistant("Ledger: +D1 kept")
    t.user()
    t.assistant("Ledger: +U1 abandoned")
    t.user(parent=fork)
    t.assistant("no ledger")
    assert context(run("prompt", t, tmp_path)) == f"{HEADER}\nD1: kept"


def test_walk_across_compact_boundary(tmp_path: Path) -> None:
    t = Transcript()
    t.user()
    t.assistant("Ledger: +D1 before | +U1 also")
    t.compact()
    t.user("summary")
    t.assistant("Ledger: -U1")
    assert context(run("prompt", t, tmp_path)) == f"{HEADER}\nD1: before"


@pytest.mark.parametrize(
    ("injected", "ledger", "expected"),
    [
        (None, "Ledger: +D1 a", f"{HEADER}\nD1: a"),
        (f"{HEADER}\nD1: a", "no change", None),
        (f"{HEADER}\nD1: a", "Ledger: +D2 b", f"{HEADER}\nD1: a\nD2: b"),
        (f"{HEADER}\nD1: a", "Ledger: -D1", EMPTY),
        (EMPTY, "Ledger: -D1", None),
    ],
)
def test_prompt_injects_on_change(tmp_path: Path, injected: str | None, ledger: str, expected: str | None) -> None:
    t = Transcript()
    t.user()
    t.assistant("Ledger: +D1 a")
    t.user()
    if injected:
        t.injection(injected)
    t.assistant(ledger)
    assert context(run("prompt", t, tmp_path)) == expected


def test_prompt_reinjects_after_compaction(tmp_path: Path) -> None:
    t = Transcript()
    t.user()
    t.assistant("Ledger: +D1 a")
    t.user()
    t.injection(f"{HEADER}\nD1: a")
    t.compact()
    t.user("summary")
    assert context(run("prompt", t, tmp_path)) == f"{HEADER}\nD1: a"


def test_prompt_without_transcript_file(tmp_path: Path) -> None:
    data = {"session_id": "s1", "transcript_path": str(tmp_path / "missing.jsonl")}
    env = {**os.environ, "HOME": str(tmp_path)}
    result = subprocess.run(
        [sys.executable, str(SCRIPT), "prompt"], input=json.dumps(data), capture_output=True, text=True, env=env
    )
    assert context(result) is None


def test_compact_always_injects(tmp_path: Path) -> None:
    t = Transcript()
    t.user()
    t.assistant("Ledger: +I1 flaky")
    t.user()
    t.injection(f"{HEADER}\nI1: flaky")
    assert context(run("compact", t, tmp_path)) == f"{HEADER}\nI1: flaky"


@pytest.mark.parametrize(
    ("message", "active", "blocked"),
    [
        ("Found [U2] a bug.", False, True),
        ("Found [U2] a bug.", True, False),
        ("Found [U2] a bug.\nLedger: +U2 bug", False, False),
        ("Again [D1] known.", False, False),
        ("Found [F1] and [C1].", False, False),
        ("Ledger: +D5", False, True),
    ],
)
def test_stop(tmp_path: Path, message: str, active: bool, blocked: bool) -> None:
    t = Transcript()
    t.user()
    t.assistant("Ledger: +D1 a")
    t.user()
    result = run("stop", t, tmp_path, last_assistant_message=message, stop_hook_active=active)
    assert result.returncode == 0, result.stderr
    assert bool(result.stdout) == blocked
    if blocked:
        assert json.loads(result.stdout)["decision"] == "block"


def test_view_file(tmp_path: Path) -> None:
    t = Transcript()
    t.user()
    t.assistant("Ledger: +D1 a | +U1 b | +I1 c | +U2 d")
    t.user()
    result = run("stop", t, tmp_path, last_assistant_message="Ledger: -U1 | xI1 gone | >U2 o/r#7", stop_hook_active=False)
    assert result.returncode == 0, result.stderr
    view = (tmp_path / ".claude" / "ledger" / "s1.md").read_text()
    assert view == f"{HEADER}\nD1: a\n\nResolved/dropped:\nI1 (dropped): gone\nU1 (resolved): b\nU2 (on GitHub): https://github.com/o/r/issues/7\n"


@pytest.mark.parametrize(
    ("data", "argv"),
    [({"transcript_path": "x"}, "prompt"), ({"session_id": "s1", "transcript_path": "x"}, "stop"), ({}, "bogus")],
)
def test_fails_loudly(tmp_path: Path, data: dict[str, Any], argv: str) -> None:
    result = subprocess.run([sys.executable, str(SCRIPT), argv], input=json.dumps(data), capture_output=True, text=True)
    assert result.returncode != 0
    assert "ledger:" in result.stderr
