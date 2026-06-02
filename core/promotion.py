"""
core/promotion.py

Consent-based promotion planning and feedback loops for Lux Ferox.

This module intentionally does not automate unsolicited posting, scraping,
credential use, or direct platform manipulation. It provides agentic planning,
human-review queues, rate-limit gates, connector-ready dispatch records, and
feedback aggregation so an author can operate compliant promotional campaigns
through approved channels.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
import hashlib
import math
from typing import Iterable, Literal, Optional


ApprovalState = Literal["PENDING_REVIEW", "APPROVED", "REJECTED"]
ConsentState = Literal["VERIFIED", "REVOKED", "EXPIRED"]
DispatchAction = Literal[
    "READY_FOR_CONNECTOR",
    "NEEDS_HUMAN_APPROVAL",
    "BLOCKED_RATE_LIMIT",
    "BLOCKED_CHANNEL",
]


@dataclass(frozen=True)
class CampaignBrief:
    """Author-approved campaign objective and public project metadata."""

    title: str
    objective: str
    project_url: str
    disclosure: str = "Author-approved Lux Ferox project update."


@dataclass(frozen=True)
class ConsentReceipt:
    """Machine-verifiable consent artifact produced by a user action.

    In an automated OODA pipeline this is the technical equivalent of the
    consent button: automation may proceed only while the receipt is verified,
    not revoked, in scope, and at or above the required consent version.
    """

    receipt_id: str
    subject_id: str
    scope: str
    accepted_at: datetime
    version: str = "1.0"
    state: ConsentState = "VERIFIED"


@dataclass(frozen=True)
class AutomationPolicy:
    """Bounds for closed-loop promotional automation."""

    auto_approve_verified_consent: bool = True
    required_consent_scope: str = "promotion"
    minimum_consent_version: str = "1.0"
    max_posts_per_ooda_cycle: int = 3
    negative_sentiment_pause: float = -0.35


@dataclass(frozen=True)
class OODACycleReport:
    """Trace of one automated observe-orient-decide-act campaign cycle."""

    observed_events: int
    orientation: AuthorFeedbackSummary
    decision: str
    generated_messages: tuple[str, ...]
    dispatch_actions: tuple[DispatchAction, ...]


@dataclass(frozen=True)
class AudienceSegment:
    """A consented or owned audience segment for campaign planning."""

    name: str
    interest: str
    consent_basis: str
    consent_receipt: Optional[ConsentReceipt] = None


@dataclass
class PromotionMessage:
    """One proposed promotional post pending author approval."""

    message_id: str
    channel: str
    segment: AudienceSegment
    text: str
    scheduled_at: datetime
    approval_state: ApprovalState = "PENDING_REVIEW"
    metadata: dict[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class DispatchRecord:
    """Connector-ready publication decision for one promotion message."""

    message_id: str
    channel: str
    action: DispatchAction
    reason: str
    text: str
    scheduled_at: datetime


@dataclass(frozen=True)
class FeedbackEvent:
    """Observable feedback returned by an approved platform connector."""

    message_id: str
    channel: str
    impressions: int = 0
    clicks: int = 0
    replies: int = 0
    shares: int = 0
    sentiment_score: float = 0.0


@dataclass(frozen=True)
class AuthorFeedbackSummary:
    """Aggregated campaign feedback for the author."""

    total_impressions: int
    total_clicks: int
    total_replies: int
    total_shares: int
    click_through_rate: float
    engagement_rate: float
    average_sentiment: float
    recommendations: tuple[str, ...]


class PromotionAgent:
    """Plan, gate, and summarize author-approved social promotion flows.

    The agent is deliberately connector-neutral. ``dispatch_due`` returns records
    that an external, authenticated, policy-compliant connector can publish; this
    class never logs in to a social network or posts by itself.
    """

    def __init__(
        self,
        author_id: str,
        allowed_channels: Iterable[str],
        *,
        max_posts_per_channel_per_day: int = 3,
        require_human_approval: bool = True,
        automation_policy: Optional[AutomationPolicy] = None,
    ) -> None:
        channels = tuple(dict.fromkeys(channel.strip() for channel in allowed_channels if channel.strip()))
        if not author_id.strip():
            raise ValueError("author_id cannot be empty.")
        if not channels:
            raise ValueError("allowed_channels must contain at least one channel.")
        if max_posts_per_channel_per_day <= 0:
            raise ValueError("max_posts_per_channel_per_day must be positive.")

        policy = automation_policy or AutomationPolicy()
        if policy.max_posts_per_ooda_cycle <= 0:
            raise ValueError("max_posts_per_ooda_cycle must be positive.")
        if not math.isfinite(policy.negative_sentiment_pause):
            raise ValueError("negative_sentiment_pause must be finite.")

        self.author_id = author_id.strip()
        self.allowed_channels = channels
        self.max_posts_per_channel_per_day = int(max_posts_per_channel_per_day)
        self.require_human_approval = require_human_approval
        self.automation_policy = policy
        self._queue: dict[str, PromotionMessage] = {}
        self._dispatch_log: list[DispatchRecord] = []
        self._feedback: list[FeedbackEvent] = []

    def generate_plan(
        self,
        brief: CampaignBrief,
        segments: Iterable[AudienceSegment],
        channels: Optional[Iterable[str]] = None,
        *,
        start_at: Optional[datetime] = None,
        cadence_minutes: int = 240,
    ) -> list[PromotionMessage]:
        """Generate a review queue of promotional messages.

        Messages are deterministic, transparent, and restricted to authorized
        channels. They are not dispatched until explicitly approved when human
        approval is required.
        """
        if cadence_minutes <= 0:
            raise ValueError("cadence_minutes must be positive.")

        active_channels = self._validate_channels(channels or self.allowed_channels)
        scheduled = self._coerce_datetime(start_at) if start_at else datetime.now(timezone.utc)
        messages: list[PromotionMessage] = []

        for segment in segments:
            self._validate_segment(segment)
            for channel in active_channels:
                text = self._compose_message(brief, segment, channel)
                approval_state: ApprovalState = (
                    "APPROVED" if self._automation_allowed(segment) else "PENDING_REVIEW"
                )
                metadata = {
                    "author_id": self.author_id,
                    "consent_basis": segment.consent_basis,
                    "project_url": brief.project_url,
                }
                if segment.consent_receipt:
                    metadata["consent_receipt_id"] = segment.consent_receipt.receipt_id
                    metadata["consent_scope"] = segment.consent_receipt.scope
                message = PromotionMessage(
                    message_id=self._message_id(channel, segment.name, text, scheduled),
                    channel=channel,
                    segment=segment,
                    text=text,
                    scheduled_at=scheduled,
                    approval_state=approval_state,
                    metadata=metadata,
                )
                self._queue[message.message_id] = message
                messages.append(message)
                scheduled += timedelta(minutes=cadence_minutes)

        return messages

    def approve(self, message_id: str) -> PromotionMessage:
        """Mark a queued message as author-approved."""
        message = self._get_message(message_id)
        message.approval_state = "APPROVED"
        return message

    def reject(self, message_id: str) -> PromotionMessage:
        """Mark a queued message as rejected by the author."""
        message = self._get_message(message_id)
        message.approval_state = "REJECTED"
        return message

    def dispatch_due(self, now: Optional[datetime] = None) -> list[DispatchRecord]:
        """Return connector-ready dispatch records for messages due now.

        The returned records are decisions only. A separate platform connector
        must handle authenticated, terms-compliant publication.
        """
        current_time = self._coerce_datetime(now) if now else datetime.now(timezone.utc)
        due_messages = sorted(
            (message for message in self._queue.values() if message.scheduled_at <= current_time),
            key=lambda message: message.scheduled_at,
        )
        records: list[DispatchRecord] = []

        for message in due_messages:
            record = self._dispatch_decision(message, current_time)
            records.append(record)
            self._dispatch_log.append(record)

        return records

    def record_feedback(self, event: FeedbackEvent) -> None:
        """Ingest feedback from an approved connector for author reporting."""
        if event.message_id not in self._queue:
            raise ValueError(f"Unknown message_id: {event.message_id}")
        if event.channel not in self.allowed_channels:
            raise ValueError(f"Channel is not allowed: {event.channel}")
        for metric_name in ("impressions", "clicks", "replies", "shares"):
            metric_value = getattr(event, metric_name)
            if metric_value < 0:
                raise ValueError(f"{metric_name} cannot be negative.")
        if not math.isfinite(event.sentiment_score):
            raise ValueError("sentiment_score must be finite.")
        self._feedback.append(event)

    def summarize_feedback(self) -> AuthorFeedbackSummary:
        """Aggregate feedback and produce operational recommendations."""
        impressions = sum(event.impressions for event in self._feedback)
        clicks = sum(event.clicks for event in self._feedback)
        replies = sum(event.replies for event in self._feedback)
        shares = sum(event.shares for event in self._feedback)
        interactions = clicks + replies + shares
        event_count = len(self._feedback)

        ctr = clicks / impressions if impressions else 0.0
        engagement = interactions / impressions if impressions else 0.0
        sentiment = (
            sum(event.sentiment_score for event in self._feedback) / event_count
            if event_count
            else 0.0
        )

        return AuthorFeedbackSummary(
            total_impressions=impressions,
            total_clicks=clicks,
            total_replies=replies,
            total_shares=shares,
            click_through_rate=ctr,
            engagement_rate=engagement,
            average_sentiment=sentiment,
            recommendations=self._recommendations(ctr, engagement, sentiment),
        )

    def run_ooda_cycle(
        self,
        brief: CampaignBrief,
        segments: Iterable[AudienceSegment],
        feedback_events: Iterable[FeedbackEvent] = (),
        channels: Optional[Iterable[str]] = None,
        *,
        now: Optional[datetime] = None,
    ) -> OODACycleReport:
        """Automate one bounded Observe-Orient-Decide-Act loop.

        The cycle observes connector feedback, orients through aggregate metrics,
        decides whether to continue or pause, and acts by generating due messages.
        Auto-approval is granted only for segments carrying valid consent receipts
        under the configured :class:`AutomationPolicy`.
        """
        observed = 0
        for event in feedback_events:
            self.record_feedback(event)
            observed += 1

        orientation = self.summarize_feedback()
        current_time = self._coerce_datetime(now) if now else datetime.now(timezone.utc)

        if orientation.average_sentiment <= self.automation_policy.negative_sentiment_pause:
            return OODACycleReport(
                observed_events=observed,
                orientation=orientation,
                decision="PAUSE_NEGATIVE_FEEDBACK",
                generated_messages=(),
                dispatch_actions=(),
            )

        cadence = 360 if orientation.engagement_rate < 0.05 else 180
        planned = self.generate_plan(
            brief,
            list(segments)[: self.automation_policy.max_posts_per_ooda_cycle],
            channels,
            start_at=current_time,
            cadence_minutes=cadence,
        )
        dispatch_records = self.dispatch_due(current_time)

        return OODACycleReport(
            observed_events=observed,
            orientation=orientation,
            decision="GENERATE_AND_DISPATCH_APPROVED_CONNECTOR_RECORDS",
            generated_messages=tuple(message.message_id for message in planned),
            dispatch_actions=tuple(record.action for record in dispatch_records),
        )

    @property
    def queue(self) -> tuple[PromotionMessage, ...]:
        """Immutable view of queued messages."""
        return tuple(self._queue.values())

    def _automation_allowed(self, segment: AudienceSegment) -> bool:
        if not self.automation_policy.auto_approve_verified_consent:
            return not self.require_human_approval
        return self._valid_consent(segment.consent_receipt)

    def _valid_consent(self, receipt: Optional[ConsentReceipt]) -> bool:
        if receipt is None:
            return False
        if receipt.state != "VERIFIED":
            return False
        if receipt.scope != self.automation_policy.required_consent_scope:
            return False
        return self._version_at_least(
            receipt.version,
            self.automation_policy.minimum_consent_version,
        )

    @staticmethod
    def _version_at_least(version: str, minimum: str) -> bool:
        def parts(value: str) -> tuple[int, ...]:
            try:
                return tuple(int(part) for part in value.split("."))
            except ValueError as exc:
                raise ValueError(f"Invalid consent version: {value}") from exc

        return parts(version) >= parts(minimum)

    def _dispatch_decision(self, message: PromotionMessage, now: datetime) -> DispatchRecord:
        if message.channel not in self.allowed_channels:
            return self._record(message, "BLOCKED_CHANNEL", "Channel is not in allowed_channels.")
        if self.require_human_approval and message.approval_state != "APPROVED":
            return self._record(message, "NEEDS_HUMAN_APPROVAL", "Message requires author approval.")
        if not self._within_daily_rate_limit(message.channel, now):
            return self._record(message, "BLOCKED_RATE_LIMIT", "Daily channel quota reached.")
        return self._record(message, "READY_FOR_CONNECTOR", "Ready for approved platform connector.")

    @staticmethod
    def _record(message: PromotionMessage, action: DispatchAction, reason: str) -> DispatchRecord:
        return DispatchRecord(
            message_id=message.message_id,
            channel=message.channel,
            action=action,
            reason=reason,
            text=message.text,
            scheduled_at=message.scheduled_at,
        )

    def _within_daily_rate_limit(self, channel: str, now: datetime) -> bool:
        day_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        ready_today = sum(
            1
            for record in self._dispatch_log
            if record.channel == channel
            and record.action == "READY_FOR_CONNECTOR"
            and day_start <= record.scheduled_at <= now
        )
        return ready_today < self.max_posts_per_channel_per_day

    def _compose_message(self, brief: CampaignBrief, segment: AudienceSegment, channel: str) -> str:
        tagged_url = f"{brief.project_url}?utm_source={channel}&utm_campaign=lux_ferox"
        return (
            f"{brief.disclosure} {brief.title}: {brief.objective} "
            f"for {segment.name} interested in {segment.interest}. "
            f"Read more: {tagged_url}"
        )

    def _message_id(self, channel: str, segment: str, text: str, scheduled_at: datetime) -> str:
        payload = f"{self.author_id}|{channel}|{segment}|{scheduled_at.isoformat()}|{text}"
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]

    def _validate_channels(self, channels: Iterable[str]) -> tuple[str, ...]:
        active_channels = tuple(dict.fromkeys(channel.strip() for channel in channels if channel.strip()))
        if not active_channels:
            raise ValueError("channels must contain at least one channel.")
        blocked = [channel for channel in active_channels if channel not in self.allowed_channels]
        if blocked:
            raise ValueError(f"Channels are not allowed: {', '.join(blocked)}")
        return active_channels

    @staticmethod
    def _validate_segment(segment: AudienceSegment) -> None:
        if not segment.name.strip():
            raise ValueError("segment.name cannot be empty.")
        if not segment.interest.strip():
            raise ValueError("segment.interest cannot be empty.")
        if not segment.consent_basis.strip():
            raise ValueError("segment.consent_basis cannot be empty.")

    @staticmethod
    def _coerce_datetime(value: datetime) -> datetime:
        if value.tzinfo is None:
            return value.replace(tzinfo=timezone.utc)
        return value.astimezone(timezone.utc)

    @staticmethod
    def _recommendations(ctr: float, engagement: float, sentiment: float) -> tuple[str, ...]:
        recommendations: list[str] = []
        if ctr < 0.02:
            recommendations.append("Clarify the call-to-action before the next approved wave.")
        if engagement < 0.05:
            recommendations.append("Add a concrete technical artifact or benchmark to improve engagement.")
        if sentiment < -0.2:
            recommendations.append("Route the next draft through author review with a calmer explanatory tone.")
        if not recommendations:
            recommendations.append("Maintain cadence and continue collecting connector feedback.")
        return tuple(recommendations)

    def _get_message(self, message_id: str) -> PromotionMessage:
        try:
            return self._queue[message_id]
        except KeyError as exc:
            raise ValueError(f"Unknown message_id: {message_id}") from exc


if __name__ == "__main__":
    print("=" * 60)
    print("core/promotion.py - Unit Tests")
    print("=" * 60)

    agent = PromotionAgent(
        author_id="author-001",
        allowed_channels=("mastodon", "linkedin"),
        max_posts_per_channel_per_day=1,
    )
    brief = CampaignBrief(
        title="AGI-Lux-Ferox",
        objective="publish a thermodynamic information engine update",
        project_url="https://example.org/lux-ferox",
    )
    start = datetime(2026, 6, 2, 12, 0, tzinfo=timezone.utc)
    receipt = ConsentReceipt(
        receipt_id="btn-accept-001",
        subject_id="subscriber-001",
        scope="promotion",
        accepted_at=start,
    )
    segment = AudienceSegment(
        name="research subscribers",
        interest="KLD/Landauer observability",
        consent_basis="owned newsletter opt-in",
        consent_receipt=receipt,
    )
    plan = agent.generate_plan(brief, [segment], ["mastodon"], start_at=start)
    assert len(plan) == 1
    assert plan[0].approval_state == "APPROVED"
    print("Test 1 PASSED: verified consent auto-approves reviewable message")

    ready = agent.dispatch_due(start)[0]
    assert ready.action == "READY_FOR_CONNECTOR"
    print("Test 2 PASSED: consented message becomes connector-ready")

    unconsented = AudienceSegment(
        name="manual review audience",
        interest="formal methods",
        consent_basis="pending opt-in",
    )
    manual_plan = agent.generate_plan(brief, [unconsented], ["linkedin"], start_at=start)
    blocked = [record for record in agent.dispatch_due(start) if record.message_id == manual_plan[0].message_id][0]
    assert blocked.action == "NEEDS_HUMAN_APPROVAL"
    print("Test 3 PASSED: missing consent still requires human approval")

    rate_limited = agent.dispatch_due(start)[0]
    assert rate_limited.action == "BLOCKED_RATE_LIMIT"
    print("Test 4 PASSED: daily channel rate limit blocks repeats")

    agent.record_feedback(
        FeedbackEvent(
            message_id=plan[0].message_id,
            channel="mastodon",
            impressions=100,
            clicks=8,
            replies=3,
            shares=2,
            sentiment_score=0.4,
        )
    )
    summary = agent.summarize_feedback()
    assert summary.total_impressions == 100
    assert abs(summary.click_through_rate - 0.08) < 1e-12
    assert summary.average_sentiment == 0.4
    print("Test 5 PASSED: feedback is aggregated for the author")

    ooda = agent.run_ooda_cycle(brief, [segment], now=start + timedelta(days=1))
    assert ooda.decision == "GENERATE_AND_DISPATCH_APPROVED_CONNECTOR_RECORDS"
    assert ooda.generated_messages
    print("Test 6 PASSED: bounded OODA cycle generates consented automation records")

    print("=" * 60)
    print("All promotion tests passed.")
    print("=" * 60)
