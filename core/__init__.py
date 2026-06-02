"""
AGI-Lux-Ferox · Core Package
Thermodynamic information engine — KLD / Landauer primitives.
"""

from .audit import AuditEvent, AuditLedger
from .connectors import ConnectorResult, DryRunConnector, FileOutboxConnector
from .controller import PhysicalOODAController, PhysicalOODAResult
from .guardian import HardScienceGuardian, SignalDecision
from .policy import OODAControlPolicy, PolicyDecision, PolicyEngine
from .report import AuthorReport, ReportBuilder
from .simulation import AdversarialPressure, CampaignSimulator, SimulationResult, SyntheticAudience
from .state import JSONLStateStore, SQLiteStateStore, persist_operational_snapshot
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
    "AuditEvent",
    "AuditLedger",
    "ConnectorResult",
    "DryRunConnector",
    "FileOutboxConnector",
    "PhysicalOODAController",
    "PhysicalOODAResult",
    "OODAControlPolicy",
    "PolicyDecision",
    "PolicyEngine",
    "AuthorReport",
    "ReportBuilder",
    "AdversarialPressure",
    "CampaignSimulator",
    "SimulationResult",
    "SyntheticAudience",
    "JSONLStateStore",
    "SQLiteStateStore",
    "persist_operational_snapshot",
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
