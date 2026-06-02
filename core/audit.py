"""
core/audit.py

Hash-chained audit ledger for Lux Ferox operational events.

The ledger records deterministic JSON payloads and links each event to the
previous hash. It is intentionally dependency-free and suitable for local audit
trails around consent receipts, OODA decisions, dispatch records, feedback, and
physical guard actions.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, is_dataclass
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
from typing import Any, Iterable, Optional


GENESIS_HASH = "0" * 64


@dataclass(frozen=True)
class AuditEvent:
    """One immutable hash-linked audit event."""

    index: int
    event_type: str
    payload: dict[str, Any]
    timestamp: str
    previous_hash: str
    event_hash: str


class AuditLedger:
    """Append-only in-memory ledger with JSONL import/export and verification."""

    def __init__(self, events: Optional[Iterable[AuditEvent]] = None) -> None:
        self._events: list[AuditEvent] = list(events or ())
        if self._events and not self.verify():
            raise ValueError("AuditLedger initialized with invalid hash chain.")

    @property
    def events(self) -> tuple[AuditEvent, ...]:
        """Immutable view of ledger events."""
        return tuple(self._events)

    @property
    def latest_hash(self) -> str:
        """Hash of the latest event, or genesis hash when empty."""
        return self._events[-1].event_hash if self._events else GENESIS_HASH

    def append(
        self,
        event_type: str,
        payload: Any,
        *,
        timestamp: Optional[datetime] = None,
    ) -> AuditEvent:
        """Append an event and return the hash-linked record."""
        if not event_type.strip():
            raise ValueError("event_type cannot be empty.")
        index = len(self._events)
        ts = (timestamp or datetime.now(timezone.utc)).astimezone(timezone.utc).isoformat()
        normalized = _normalize_payload(payload)
        previous_hash = self.latest_hash
        event_hash = self.compute_hash(index, event_type, normalized, ts, previous_hash)
        event = AuditEvent(
            index=index,
            event_type=event_type,
            payload=normalized,
            timestamp=ts,
            previous_hash=previous_hash,
            event_hash=event_hash,
        )
        self._events.append(event)
        return event

    def verify(self) -> bool:
        """Return true when indexes and hash links are intact."""
        previous = GENESIS_HASH
        for expected_index, event in enumerate(self._events):
            if event.index != expected_index or event.previous_hash != previous:
                return False
            expected_hash = self.compute_hash(
                event.index,
                event.event_type,
                event.payload,
                event.timestamp,
                event.previous_hash,
            )
            if event.event_hash != expected_hash:
                return False
            previous = event.event_hash
        return True

    def to_jsonl(self, path: str | Path) -> None:
        """Write the ledger to JSONL."""
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8") as handle:
            for event in self._events:
                handle.write(json.dumps(asdict(event), sort_keys=True) + "\n")

    @classmethod
    def from_jsonl(cls, path: str | Path) -> "AuditLedger":
        """Load and verify a ledger from JSONL."""
        path = Path(path)
        if not path.exists():
            return cls()
        events = []
        with path.open("r", encoding="utf-8") as handle:
            for line in handle:
                if line.strip():
                    events.append(AuditEvent(**json.loads(line)))
        return cls(events)

    @staticmethod
    def compute_hash(
        index: int,
        event_type: str,
        payload: dict[str, Any],
        timestamp: str,
        previous_hash: str,
    ) -> str:
        body = {
            "index": index,
            "event_type": event_type,
            "payload": payload,
            "timestamp": timestamp,
            "previous_hash": previous_hash,
        }
        encoded = json.dumps(body, sort_keys=True, separators=(",", ":")).encode("utf-8")
        return hashlib.sha256(encoded).hexdigest()


def _normalize_payload(payload: Any) -> dict[str, Any]:
    if is_dataclass(payload):
        payload = asdict(payload)
    elif hasattr(payload, "__dict__") and not isinstance(payload, dict):
        payload = dict(payload.__dict__)
    if not isinstance(payload, dict):
        payload = {"value": payload}
    return _jsonable(payload)


def _jsonable(value: Any) -> Any:
    if isinstance(value, datetime):
        return value.astimezone(timezone.utc).isoformat() if value.tzinfo else value.replace(tzinfo=timezone.utc).isoformat()
    if isinstance(value, dict):
        return {str(key): _jsonable(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_jsonable(item) for item in value]
    if is_dataclass(value):
        return _jsonable(asdict(value))
    return value


if __name__ == "__main__":
    ledger = AuditLedger()
    first = ledger.append("consent", {"receipt_id": "r1"})
    second = ledger.append("dispatch", {"message_id": "m1"})
    assert first.previous_hash == GENESIS_HASH
    assert second.previous_hash == first.event_hash
    assert ledger.verify()
    tampered = AuditEvent(
        index=0,
        event_type="consent",
        payload={"receipt_id": "evil"},
        timestamp=first.timestamp,
        previous_hash=GENESIS_HASH,
        event_hash=first.event_hash,
    )
    try:
        AuditLedger([tampered])
        raise AssertionError("tampered ledger must fail")
    except ValueError:
        pass
    print("All audit tests passed.")
