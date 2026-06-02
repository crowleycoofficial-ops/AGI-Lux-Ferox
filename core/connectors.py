"""
core/connectors.py

Connector interface for promotion dispatch decisions.

No connector here logs into a social network. Dry-run and file-outbox connectors
turn READY_FOR_CONNECTOR records into traceable local results that can be handed
to an approved external publisher.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
import json
from pathlib import Path
from typing import Protocol

from .promotion import DispatchRecord


@dataclass(frozen=True)
class ConnectorResult:
    """Result of handing a dispatch record to a connector."""

    message_id: str
    channel: str
    status: str
    location: str
    timestamp: str


class SocialConnector(Protocol):
    """Protocol implemented by approved publishing connectors."""

    def publish(self, record: DispatchRecord) -> ConnectorResult:
        """Publish or stage one dispatch record."""


class DryRunConnector:
    """Connector that validates flow without writing or posting anything."""

    def publish(self, record: DispatchRecord) -> ConnectorResult:
        status = "DRY_RUN_READY" if record.action == "READY_FOR_CONNECTOR" else "DRY_RUN_BLOCKED"
        return ConnectorResult(
            message_id=record.message_id,
            channel=record.channel,
            status=status,
            location="dry-run",
            timestamp=datetime.now(timezone.utc).isoformat(),
        )


class FileOutboxConnector:
    """Stage connector-ready records as JSON files in an outbox directory."""

    def __init__(self, outbox_dir: str | Path = "outbox") -> None:
        self.outbox_dir = Path(outbox_dir)

    def publish(self, record: DispatchRecord) -> ConnectorResult:
        self.outbox_dir.mkdir(parents=True, exist_ok=True)
        if record.action != "READY_FOR_CONNECTOR":
            return ConnectorResult(
                message_id=record.message_id,
                channel=record.channel,
                status="BLOCKED_NOT_READY",
                location=str(self.outbox_dir),
                timestamp=datetime.now(timezone.utc).isoformat(),
            )
        path = self.outbox_dir / f"{record.scheduled_at.date()}-{record.channel}-{record.message_id}.json"
        path.write_text(json.dumps(asdict(record), indent=2, sort_keys=True, default=str), encoding="utf-8")
        return ConnectorResult(
            message_id=record.message_id,
            channel=record.channel,
            status="STAGED_TO_OUTBOX",
            location=str(path),
            timestamp=datetime.now(timezone.utc).isoformat(),
        )


if __name__ == "__main__":
    from datetime import datetime, timezone

    record = DispatchRecord(
        message_id="m1",
        channel="mastodon",
        action="READY_FOR_CONNECTOR",
        reason="test",
        text="hello",
        scheduled_at=datetime.now(timezone.utc),
    )
    assert DryRunConnector().publish(record).status == "DRY_RUN_READY"
    out = FileOutboxConnector("/tmp/lux-ferox-outbox-test").publish(record)
    assert out.status == "STAGED_TO_OUTBOX"
    print("All connector tests passed.")
