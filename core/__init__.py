"""
AGI-Lux-Ferox · Core Package
Thermodynamic information engine — KLD / Landauer primitives.
"""

from .guardian import HardScienceGuardian, SignalDecision
from .promotion import (
    AudienceSegment,
    AuthorFeedbackSummary,
    AutomationPolicy,
    CampaignBrief,
    ConsentReceipt,
    DispatchRecord,
    FeedbackEvent,
    OODACycleReport,
    PromotionAgent,
    PromotionMessage,
)

__all__ = [
    "calculate_surprise",
    "HardScienceGuardian",
    "SignalDecision",
    "AudienceSegment",
    "AuthorFeedbackSummary",
    "AutomationPolicy",
    "CampaignBrief",
    "ConsentReceipt",
    "DispatchRecord",
    "FeedbackEvent",
    "OODACycleReport",
    "PromotionAgent",
    "PromotionMessage",
]
__version__ = "0.1.0"


def __getattr__(name: str):
    """Lazily expose numerical primitives without loading optional stacks early."""
    if name == "calculate_surprise":
        from .surprise import calculate_surprise

        return calculate_surprise
    raise AttributeError(f"module 'core' has no attribute {name!r}")
