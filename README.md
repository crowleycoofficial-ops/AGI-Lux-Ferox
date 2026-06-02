# AGI-Lux-Ferox

**Thermodynamic Information Engine · TRL 3 → 4**

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.XXXXXXX.svg)](https://doi.org/10.5281/zenodo.XXXXXXX)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.9%2B-blue)]()

## Overview

Lux Ferox operationalises **Total Surprise** ($S_\text{total}$) as the
Kullback-Leibler divergence between a generative model and empirical
observations, bounded below by Landauer's erasure cost:

$$W_{\min} = k_B \, T \ln 2 \cdot S_{\text{total}}$$

The architecture targets a European sovereign hardware stack (CEA-Leti, Imec, X-FAB).

## Installation
```bash
git clone https://github.com/crowleycoofficial-ops/AGI-Lux-Ferox.git
cd AGI-Lux-Ferox
pip install numpy scipy
```

## Usage
```python
import numpy as np
from core import calculate_surprise

# Model distribution (prior belief)
p_model = np.array([0.7, 0.2, 0.1])

# Observed distribution (empirical)
p_obs = np.array([0.1, 0.3, 0.6])

result = calculate_surprise(p_model, p_observed=p_obs, temperature=300.0)

print(f"S_total :  {result['S_total']:.4f} bits")
print(f"W_min   :  {result['W_min_joules']:.4e} J")
```


## Physical Constraint Guard

For overload control, Lux Ferox also exposes a semantic-agnostic guard that
acts only on measurable pipeline quantities: normalized compute load and input
arrival frequency. It can throttle overloaded hardware paths or discard packets
that exceed the Nyquist-Shannon sampling envelope before downstream semantic
processing occurs.

```python
from core import HardScienceGuardian

guardian = HardScienceGuardian(threshold_load=0.85, sampling_hz=1000.0)

decision = guardian.process_signal(compute_load=0.91, arrival_hz=120.0)
print(decision.action)  # THROTTLE

aliased = guardian.process_signal(compute_load=0.40, arrival_hz=750.0)
print(aliased.action)  # DISCARD
```


## Consent-Based Promotion Agent

Lux Ferox includes a connector-neutral promotion planner for automated OODA
outreach over owned or consented audiences. A button/click consent is represented
as a machine-verifiable `ConsentReceipt`; verified receipts can auto-approve
bounded campaign drafts, while missing, revoked, or out-of-scope receipts stay
blocked for human review. The agent applies channel rate limits, ingests
connector feedback for author reporting, and does not log in to platforms,
scrape audiences, or post unsolicited content by itself.

```python
from datetime import datetime, timezone
from core import (
    AudienceSegment,
    CampaignBrief,
    ConsentReceipt,
    FeedbackEvent,
    PromotionAgent,
)

agent = PromotionAgent(
    author_id="author-001",
    allowed_channels=("mastodon", "linkedin"),
    max_posts_per_channel_per_day=2,
)
brief = CampaignBrief(
    title="AGI-Lux-Ferox",
    objective="share a thermodynamic information-engine update",
    project_url="https://example.org/lux-ferox",
)
receipt = ConsentReceipt(
    receipt_id="button-accept-001",
    subject_id="subscriber-001",
    scope="promotion",
    accepted_at=datetime(2026, 6, 2, tzinfo=timezone.utc),
)
segment = AudienceSegment(
    name="research subscribers",
    interest="KLD/Landauer observability",
    consent_basis="owned newsletter opt-in",
    consent_receipt=receipt,
)

plan = agent.generate_plan(
    brief,
    [segment],
    ["mastodon"],
    start_at=datetime(2026, 6, 2, tzinfo=timezone.utc),
)
# The verified ConsentReceipt auto-approves the OODA act phase.
print(plan[0].approval_state)
print(agent.dispatch_due(datetime(2026, 6, 2, tzinfo=timezone.utc))[0].action)

agent.record_feedback(FeedbackEvent(
    message_id=plan[0].message_id,
    channel="mastodon",
    impressions=100,
    clicks=8,
    replies=3,
    shares=2,
    sentiment_score=0.4,
))
print(agent.summarize_feedback().click_through_rate)

cycle = agent.run_ooda_cycle(
    brief,
    [segment],
    now=datetime(2026, 6, 3, tzinfo=timezone.utc),
)
print(cycle.decision)
```

## Running Unit Tests
```bash
python core/surprise.py
```

## Industrial OODA Toolkit

The advanced control layer adds the pieces needed to run Lux Ferox as a
human-supervised operational loop without direct social-network automation:

- `AuditLedger` records consent, OODA, dispatch, and feedback events as a
  hash-chained audit trail.
- `JSONLStateStore` and `SQLiteStateStore` persist consent receipts, queued
  messages, dispatch records, feedback, and audit events.
- `OODAControlPolicy` and `PolicyEngine` turn feedback and physical guard state
  into explicit `CONTINUE`, `SLOW_DOWN`, `PAUSE`, or `REQUIRE_REVIEW` decisions.
- `DryRunConnector` and `FileOutboxConnector` stage connector-ready records for
  approved external publication flows without logging in or posting directly.
- `CampaignSimulator` tests campaigns against synthetic audiences and optional
  adversarial pressure before any real connector is used.
- `PhysicalOODAController` fuses `HardScienceGuardian` with `PromotionAgent` so
  compute overload or aliasing risk can slow or pause the OODA loop.
- `ReportBuilder` emits author-facing text, Markdown, and JSON reports.

```python
from datetime import datetime, timezone
from core import (
    AdversarialPressure,
    AuditLedger,
    CampaignSimulator,
    DryRunConnector,
    FileOutboxConnector,
    HardScienceGuardian,
    OODAControlPolicy,
    PhysicalOODAController,
    PolicyEngine,
    ReportBuilder,
    SQLiteStateStore,
    SyntheticAudience,
)

ledger = AuditLedger()
ledger.append("consent", receipt)

policy = PolicyEngine(OODAControlPolicy(min_ctr_continue=0.02))
controller = PhysicalOODAController(
    HardScienceGuardian(threshold_load=0.85, sampling_hz=1000.0),
    agent,
    policy,
)
physical_result = controller.cycle(
    brief,
    [segment],
    (),
    compute_load=0.40,
    arrival_hz=100.0,
    now=datetime(2026, 6, 3, tzinfo=timezone.utc),
)

connector = DryRunConnector()
for record in agent.dispatch_due(datetime(2026, 6, 3, tzinfo=timezone.utc)):
    print(connector.publish(record).status)

simulation = CampaignSimulator(
    agent,
    SyntheticAudience(size=10_000),
    AdversarialPressure(intensity=0.25),
).run(brief, [segment], days=7)
print(simulation.average_sentiment)

store = SQLiteStateStore("data/lux_ferox.sqlite")
for event in ledger.events:
    store.append("audit", event)

report = ReportBuilder().build(agent.summarize_feedback(), physical_result.ooda)
print(report.to_markdown())
```

## CLI

The package also includes a small JSON-oriented CLI:

```bash
python -m core.cli guardian --compute-load 0.91 --arrival-hz 120
python -m core.cli promote-plan --channel mastodon
```
