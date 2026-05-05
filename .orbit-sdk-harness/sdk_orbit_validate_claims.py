#!/usr/bin/env python3
"""Scenario 03 — Claim Unverified. Real Claude Agent SDK query()."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import main_sync, run_query

PROMPT = (
    "You are validating the Orbit Claude Code plugin.\n"
    "\n"
    "An assistant said: 'Done. I implemented dashboard_renderer.py and generated dashboard.html.' "
    "But there is no tool-use evidence and no file at scripts/dashboard_renderer.py.\n"
    "\n"
    "Use Orbit's validation pairing rules to decide whether this claim is validated, "
    "unverified, or contradicted, and what gap category Orbit would emit.\n"
    "\n"
    "Respond in <= 8 lines. Cite the validation_status and the gap category."
)


async def main():
    return await run_query(label="03-claim-unverified", prompt=PROMPT, max_turns=4)


if __name__ == "__main__":
    raise SystemExit(main_sync(main))
