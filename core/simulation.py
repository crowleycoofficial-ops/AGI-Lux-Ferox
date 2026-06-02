"""
core/simulation.py

Deterministic campaign simulation with optional adversarial pressure.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
import random
from typing import Iterable

from .promotion import AudienceSegment, CampaignBrief, ConsentReceipt, FeedbackEvent, PromotionAgent


@dataclass(frozen=True)
class SyntheticAudience:
    """Synthetic audience parameters for dry-run campaign evaluation."""

    size: int
    base_ctr: float = 0.03
    base_engagement: float = 0.06
    sentiment: float = 0.2


@dataclass(frozen=True)
class AdversarialPressure:
    """Noise model that degrades campaign observables."""

    intensity: float = 0.0
    sentiment_drag: float = 0.3


@dataclass(frozen=True)
class SimulationResult:
    """Aggregated simulation outputs."""

    days: int
    generated_messages: int
    impressions: int
    clicks: int
    replies: int
    shares: int
    average_sentiment: float
    ooda_decisions: tuple[str, ...]


class CampaignSimulator:
    """Run dry campaign loops without publishing to human networks."""

    def __init__(
        self,
        agent: PromotionAgent,
        audience: SyntheticAudience,
        adversary: AdversarialPressure | None = None,
        *,
        seed: int = 7,
    ) -> None:
        if audience.size <= 0:
            raise ValueError("audience.size must be positive.")
        self.agent = agent
        self.audience = audience
        self.adversary = adversary or AdversarialPressure()
        self.random = random.Random(seed)

    def run(
        self,
        brief: CampaignBrief,
        segments: Iterable[AudienceSegment],
        *,
        days: int = 14,
        start_at: datetime | None = None,
    ) -> SimulationResult:
        if days <= 0:
            raise ValueError("days must be positive.")
        current = start_at or datetime.now(timezone.utc)
        decisions: list[str] = []
        generated = 0
        total_impressions = total_clicks = total_replies = total_shares = 0
        sentiments: list[float] = []

        for day in range(days):
            feedback = self._feedback_for_day(day)
            total_impressions += feedback.impressions
            total_clicks += feedback.clicks
            total_replies += feedback.replies
            total_shares += feedback.shares
            sentiments.append(feedback.sentiment_score)
            try:
                self.agent.record_feedback(feedback)
                cycle_feedback = ()
            except ValueError:
                cycle_feedback = ()
            report = self.agent.run_ooda_cycle(brief, segments, cycle_feedback, now=current)
            decisions.append(report.decision)
            generated += len(report.generated_messages)
            current += timedelta(days=1)

        return SimulationResult(
            days=days,
            generated_messages=generated,
            impressions=total_impressions,
            clicks=total_clicks,
            replies=total_replies,
            shares=total_shares,
            average_sentiment=sum(sentiments) / len(sentiments),
            ooda_decisions=tuple(decisions),
        )

    def _feedback_for_day(self, day: int) -> FeedbackEvent:
        pressure = max(0.0, min(1.0, self.adversary.intensity))
        impressions = max(1, int(self.audience.size * (0.05 + self.random.random() * 0.05)))
        ctr = max(0.0, self.audience.base_ctr * (1.0 - pressure * 0.5))
        engagement = max(0.0, self.audience.base_engagement * (1.0 - pressure * 0.4))
        clicks = int(impressions * ctr)
        replies = int(impressions * engagement * 0.4)
        shares = int(impressions * engagement * 0.3)
        sentiment = self.audience.sentiment - pressure * self.adversary.sentiment_drag
        return FeedbackEvent(
            message_id=next((message.message_id for message in self.agent.queue), "synthetic"),
            channel=self.agent.allowed_channels[0],
            impressions=impressions,
            clicks=clicks,
            replies=replies,
            shares=shares,
            sentiment_score=sentiment,
        )


if __name__ == "__main__":
    start = datetime(2026, 6, 2, tzinfo=timezone.utc)
    agent = PromotionAgent("author", ["mastodon"])
    receipt = ConsentReceipt("r1", "s1", "promotion", start)
    segment = AudienceSegment("subscribers", "research", "opt-in", receipt)
    brief = CampaignBrief("Lux", "share update", "https://example.org")
    result = CampaignSimulator(agent, SyntheticAudience(1000), AdversarialPressure(0.2)).run(
        brief, [segment], days=3, start_at=start
    )
    assert result.days == 3
    assert result.generated_messages > 0
    print("All simulation tests passed.")
