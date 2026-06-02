"""
core/report.py

Author-facing campaign reports in text, Markdown, and JSON-ready form.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
import json

from .promotion import AuthorFeedbackSummary, OODACycleReport


@dataclass(frozen=True)
class AuthorReport:
    """Human-readable report generated from feedback and OODA state."""

    title: str
    summary: AuthorFeedbackSummary
    ooda_decision: str
    recommendations: tuple[str, ...]

    def to_text(self) -> str:
        lines = [
            self.title,
            "-" * len(self.title),
            f"Total impressions: {self.summary.total_impressions}",
            f"Total clicks: {self.summary.total_clicks}",
            f"CTR: {self.summary.click_through_rate:.2%}",
            f"Engagement: {self.summary.engagement_rate:.2%}",
            f"Average sentiment: {self.summary.average_sentiment:.3f}",
            f"OODA decision: {self.ooda_decision}",
            "Recommendations:",
        ]
        lines.extend(f"- {item}" for item in self.recommendations)
        return "\n".join(lines)

    def to_markdown(self) -> str:
        return (
            f"# {self.title}\n\n"
            f"| Metric | Value |\n|---|---:|\n"
            f"| Total impressions | {self.summary.total_impressions} |\n"
            f"| Total clicks | {self.summary.total_clicks} |\n"
            f"| CTR | {self.summary.click_through_rate:.2%} |\n"
            f"| Engagement | {self.summary.engagement_rate:.2%} |\n"
            f"| Average sentiment | {self.summary.average_sentiment:.3f} |\n"
            f"| OODA decision | {self.ooda_decision} |\n\n"
            "## Recommendations\n"
            + "\n".join(f"- {item}" for item in self.recommendations)
        )

    def to_json(self) -> str:
        return json.dumps(asdict(self), indent=2, sort_keys=True)


class ReportBuilder:
    """Build reports from feedback summaries and optional OODA reports."""

    def build(
        self,
        summary: AuthorFeedbackSummary,
        ooda_report: OODACycleReport | None = None,
        *,
        title: str = "Lux Ferox Campaign Report",
    ) -> AuthorReport:
        decision = ooda_report.decision if ooda_report else "NO_OODA_CYCLE"
        return AuthorReport(title, summary, decision, summary.recommendations)


if __name__ == "__main__":
    summary = AuthorFeedbackSummary(100, 8, 3, 2, 0.08, 0.13, 0.4, ("continue",))
    report = ReportBuilder().build(summary)
    assert "CTR: 8.00%" in report.to_text()
    assert "# Lux Ferox" in report.to_markdown()
    assert "click_through_rate" in report.to_json()
    print("All report tests passed.")
