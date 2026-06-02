"""
core/controller.py

Fusion layer between physical constraints, policy decisions, and promotion OODA.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Iterable, Optional

from .guardian import HardScienceGuardian, SignalDecision
from .policy import PolicyDecision, PolicyEngine
from .promotion import AudienceSegment, CampaignBrief, FeedbackEvent, OODACycleReport, PromotionAgent


@dataclass(frozen=True)
class PhysicalOODAResult:
    """Combined physical guard, policy, and OODA result."""

    signal: SignalDecision
    policy: PolicyDecision
    ooda: Optional[OODACycleReport]


class PhysicalOODAController:
    """Subordinate promotion automation to physical runtime constraints."""

    def __init__(
        self,
        guardian: HardScienceGuardian,
        agent: PromotionAgent,
        policy_engine: PolicyEngine | None = None,
    ) -> None:
        self.guardian = guardian
        self.agent = agent
        self.policy_engine = policy_engine or PolicyEngine()

    def cycle(
        self,
        brief: CampaignBrief,
        segments: Iterable[AudienceSegment],
        feedback_events: Iterable[FeedbackEvent],
        *,
        compute_load: float,
        arrival_hz: float,
        now: datetime | None = None,
    ) -> PhysicalOODAResult:
        current = now or datetime.now(timezone.utc)
        signal = self.guardian.process_signal(compute_load, arrival_hz)
        summary = self.agent.summarize_feedback()
        policy = self.policy_engine.evaluate(summary, now=current, physical_action=signal.action)
        if signal.action == "DISCARD" or policy.action == "PAUSE":
            return PhysicalOODAResult(signal, policy, None)
        if signal.action == "THROTTLE" and policy.action == "SLOW_DOWN":
            # Keep the loop closed, but let policy cadence slow generation.
            pass
        ooda = self.agent.run_ooda_cycle(brief, segments, feedback_events, now=current)
        return PhysicalOODAResult(signal, policy, ooda)


if __name__ == "__main__":
    from datetime import datetime, timezone
    from .promotion import ConsentReceipt

    now = datetime(2026, 6, 2, tzinfo=timezone.utc)
    agent = PromotionAgent("author", ["mastodon"])
    segment = AudienceSegment("subscribers", "research", "opt-in", ConsentReceipt("r1", "s1", "promotion", now))
    result = PhysicalOODAController(HardScienceGuardian(latency_penalty=0), agent).cycle(
        CampaignBrief("Lux", "share", "https://example.org"),
        [segment],
        (),
        compute_load=0.1,
        arrival_hz=1.0,
        now=now,
    )
    assert result.signal.action == "PASS"
    assert result.ooda is not None
    print("All controller tests passed.")
