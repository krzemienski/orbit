#!/usr/bin/env python3
"""Scenario 06 — Configurable Review Window. Real Claude Agent SDK query().

This script also accepts CLI args mirroring orbit-audit time-window flags so a human
can drive it with --days/--since/--from/--to. The arg values are echoed into the
prompt so the captured transcript reflects the requested scope.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import main_sync, run_query

BASE_PROMPT = (
    "You are validating the Orbit Claude Code plugin.\n"
    "\n"
    "Orbit's review-window command must be configurable. The default is --days 3, "
    "but it must also support --days N, --since YYYY-MM-DD, and --from YYYY-MM-DD --to YYYY-MM-DD.\n"
    "\n"
    "Selected scope for this run: {scope}.\n"
    "\n"
    "Describe what scope Orbit would record in evidence.json and how the dashboard would "
    "echo that scope. Confirm that /orbit:review-last-3-days is documented as a legacy alias "
    "for --days 3, not a hardcoded behavior.\n"
    "\n"
    "Respond in <= 10 lines."
)


def build_prompt(args) -> tuple[str, str]:
    parts = []
    label_parts = []
    if args.days is not None:
        parts.append(f"--days {args.days}")
        label_parts.append(f"days{args.days}")
    if args.since:
        parts.append(f"--since {args.since}")
        label_parts.append(f"since-{args.since}")
    if args.start:
        parts.append(f"--from {args.start}")
        label_parts.append(f"from-{args.start}")
    if args.end:
        parts.append(f"--to {args.end}")
        label_parts.append(f"to-{args.end}")
    scope = " ".join(parts) if parts else "default (--days 3)"
    label_suffix = "-".join(label_parts) if label_parts else "default"
    return BASE_PROMPT.format(scope=scope), f"06-review-window-{label_suffix}"


async def amain(args):
    prompt, label = build_prompt(args)
    return await run_query(label=label, prompt=prompt, max_turns=4)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Scenario 06 — review window")
    parser.add_argument("--days", type=int)
    parser.add_argument("--since")
    parser.add_argument("--from", dest="start")
    parser.add_argument("--to", dest="end")
    args = parser.parse_args(argv)
    return main_sync(lambda: amain(args))


if __name__ == "__main__":
    raise SystemExit(main())
