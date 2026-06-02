"""
core/policy.py

Explicit OODA policy evaluation for campaign automation.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Literal, Optional

from .promotion import AuthorFeedbackSummary


PolicyAction = Literal["CONTINUE", "SLOW_DOWN", "PAUSE", "REQUIRE_REVIEW"]


@dataclass(frozen=True)
class OODAControlPolicy:
    """Configurable policy gates for human-approved OODA automation."""

    min_ctr_continue: float = 0.02
    min_engagement_continue: float = 0.05
    negative_sentiment_pause: float = -0.35
    cooldown_hours_after_pause: int = 24
    required_consent_scope: str = "promotion"


@dataclass(frozen=True)
class PolicyDecision:
    """Decision returned by the policy engine."""

    action: PolicyAction
    reason: str
    cadence_minutes: int
    cooldown_until: Optional[datetime] = None


class PolicyEngine:
    """Evaluate feedback summaries into explicit OODA control decisions."""

    def __init__(self, policy: OODAControlPolicy | None = None) -> None:
        self.policy = policy or OODAControlPolicy()

    def evaluate(
        self,
        summary: AuthorFeedbackSummary,
        *,
        now: Optional[datetime] = None,
        physical_action: Optional[str] = None,
    ) -> PolicyDecision:
        current = (now or datetime.now(timezone.utc)).astimezone(timezone.utc)
        if physical_action == "DISCARD":
            return PolicyDecision("PAUSE", "physical aliasing risk", 1440, current + timedelta(hours=1))
        if physical_action == "THROTTLE":
            return PolicyDecision("SLOW_DOWN", "physical overload throttle", 720)
        if summary.average_sentiment <= self.policy.negative_sentiment_pause:
            return PolicyDecision(
                "PAUSE",
                "negative feedback threshold crossed",
                1440,
                current + timedelta(hours=self.policy.cooldown_hours_after_pause),
            )
        if summary.total_impressions > 0 and summary.click_through_rate < self.policy.min_ctr_continue:
            return PolicyDecision("REQUIRE_REVIEW", "click-through below continuation threshold", 720)
        if summary.total_impressions > 0 and summary.engagement_rate < self.policy.min_engagement_continue:
            return PolicyDecision("SLOW_DOWN", "engagement below continuation threshold", 360)
        return PolicyDecision("CONTINUE", "policy thresholds satisfied", 180)


if __name__ == "__main__":
    summary = AuthorFeedbackSummary(100, 1, 0, 0, 0.01, 0.01, 0.0, ())
    assert PolicyEngine().evaluate(summary).action == "REQUIRE_REVIEW"
    hot = AuthorFeedbackSummary(100, 5, 5, 5, 0.05, 0.15, 0.1, ())
    assert PolicyEngine().evaluate(hot).action == "CONTINUE"
    print("All policy tests passed.")
