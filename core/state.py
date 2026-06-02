"""
core/state.py

Persistent OODA state stores for consent, promotion, dispatch, feedback, and
audit trails. JSONL is optimized for transparent auditability; SQLite provides a
single-file industrial store without external dependencies.
"""

from __future__ import annotations

from dataclasses import asdict, is_dataclass
from datetime import datetime, timezone
import json
from pathlib import Path
import sqlite3
from typing import Any, Iterable, Literal

from .audit import AuditEvent
from .promotion import ConsentReceipt, DispatchRecord, FeedbackEvent, PromotionMessage

StateKind = Literal["consent", "message", "dispatch", "feedback", "audit"]


class JSONLStateStore:
    """Append/read state records by kind using JSONL files."""

    def __init__(self, root: str | Path = "data") -> None:
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)

    def append(self, kind: StateKind, record: Any) -> Path:
        path = self._path(kind)
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(_to_jsonable(record), sort_keys=True) + "\n")
        return path

    def read(self, kind: StateKind) -> list[dict[str, Any]]:
        path = self._path(kind)
        if not path.exists():
            return []
        with path.open("r", encoding="utf-8") as handle:
            return [json.loads(line) for line in handle if line.strip()]

    def _path(self, kind: StateKind) -> Path:
        return self.root / f"{kind}.jsonl"


class SQLiteStateStore:
    """Single-file SQLite state store for OODA operational records."""

    def __init__(self, path: str | Path = "data/lux_ferox.sqlite") -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._init_schema()

    def append(self, kind: StateKind, record: Any) -> int:
        payload = json.dumps(_to_jsonable(record), sort_keys=True)
        with sqlite3.connect(self.path) as conn:
            cur = conn.execute(
                "INSERT INTO records(kind, payload, created_at) VALUES (?, ?, ?)",
                (kind, payload, datetime.now(timezone.utc).isoformat()),
            )
            return int(cur.lastrowid)

    def read(self, kind: StateKind) -> list[dict[str, Any]]:
        with sqlite3.connect(self.path) as conn:
            rows = conn.execute(
                "SELECT payload FROM records WHERE kind = ? ORDER BY id ASC",
                (kind,),
            ).fetchall()
        return [json.loads(row[0]) for row in rows]

    def _init_schema(self) -> None:
        with sqlite3.connect(self.path) as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS records (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    kind TEXT NOT NULL,
                    payload TEXT NOT NULL,
                    created_at TEXT NOT NULL
                )
                """
            )
            conn.execute("CREATE INDEX IF NOT EXISTS idx_records_kind ON records(kind)")


def persist_operational_snapshot(
    store: JSONLStateStore | SQLiteStateStore,
    *,
    receipts: Iterable[ConsentReceipt] = (),
    messages: Iterable[PromotionMessage] = (),
    dispatches: Iterable[DispatchRecord] = (),
    feedback: Iterable[FeedbackEvent] = (),
    audit_events: Iterable[AuditEvent] = (),
) -> None:
    """Persist a complete OODA snapshot into the selected store."""
    for item in receipts:
        store.append("consent", item)
    for item in messages:
        store.append("message", item)
    for item in dispatches:
        store.append("dispatch", item)
    for item in feedback:
        store.append("feedback", item)
    for item in audit_events:
        store.append("audit", item)


def _to_jsonable(record: Any) -> Any:
    if is_dataclass(record):
        record = asdict(record)
    if isinstance(record, datetime):
        return record.astimezone(timezone.utc).isoformat() if record.tzinfo else record.replace(tzinfo=timezone.utc).isoformat()
    if isinstance(record, dict):
        return {str(key): _to_jsonable(value) for key, value in record.items()}
    if isinstance(record, (list, tuple)):
        return [_to_jsonable(value) for value in record]
    return record


if __name__ == "__main__":
    import tempfile

    with tempfile.TemporaryDirectory() as tmp:
        jsonl = JSONLStateStore(Path(tmp) / "jsonl")
        sqlite = SQLiteStateStore(Path(tmp) / "state.sqlite")
        receipt = ConsentReceipt("r1", "s1", "promotion", datetime.now(timezone.utc))
        jsonl.append("consent", receipt)
        sqlite.append("consent", receipt)
        assert jsonl.read("consent")[0]["receipt_id"] == "r1"
        assert sqlite.read("consent")[0]["receipt_id"] == "r1"
    print("All state store tests passed.")
