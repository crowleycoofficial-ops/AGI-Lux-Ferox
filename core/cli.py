"""
core/cli.py

Small JSON-oriented command line interface for Lux Ferox primitives.
"""

from __future__ import annotations

import argparse
from dataclasses import asdict
from datetime import datetime, timezone
import json

from .guardian import HardScienceGuardian
from .promotion import AudienceSegment, CampaignBrief, ConsentReceipt, PromotionAgent


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="lux-ferox")
    sub = parser.add_subparsers(dest="command", required=True)

    guardian = sub.add_parser("guardian")
    guardian.add_argument("--compute-load", type=float, required=True)
    guardian.add_argument("--arrival-hz", type=float, required=True)
    guardian.add_argument("--sampling-hz", type=float, default=1000.0)

    promote = sub.add_parser("promote-plan")
    promote.add_argument("--channel", default="mastodon")
    promote.add_argument("--title", default="AGI-Lux-Ferox")
    promote.add_argument("--objective", default="share project update")
    promote.add_argument("--url", default="https://example.org/lux-ferox")

    args = parser.parse_args(argv)
    if args.command == "guardian":
        decision = HardScienceGuardian(sampling_hz=args.sampling_hz).process_signal(
            args.compute_load, args.arrival_hz
        )
        print(json.dumps(asdict(decision), indent=2, sort_keys=True))
        return 0
    if args.command == "promote-plan":
        now = datetime.now(timezone.utc)
        agent = PromotionAgent("cli-author", [args.channel])
        receipt = ConsentReceipt("cli-receipt", "cli-subject", "promotion", now)
        segment = AudienceSegment("cli audience", "Lux Ferox", "cli verified", receipt)
        brief = CampaignBrief(args.title, args.objective, args.url)
        plan = agent.generate_plan(brief, [segment], [args.channel], start_at=now)
        print(json.dumps([asdict(message) for message in plan], indent=2, sort_keys=True, default=str))
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
