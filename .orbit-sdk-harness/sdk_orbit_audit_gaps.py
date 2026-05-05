#!/usr/bin/env python3
"""Scenario 01 — Plan Gap. Real Claude Agent SDK query()."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import main_sync, run_query

PROMPT = (
    "You are validating the Orbit Claude Code plugin.\n"
    "\n"
    "Use Orbit to audit this project. The written plan mentions skills and commands, "
    "but recent sessions include a user request for first-class dashboard visualization.\n"
    "\n"
    "Determine whether the dashboard request is captured by the plan, implemented in the "
    "codebase, and validated by current artifacts.\n"
    "\n"
    "Respond in <= 8 lines. Cite the gap category (e.g. intent-not-planned, plan-omission). "
    "Do not create new files; only describe what Orbit would emit."
)


async def main():
    return await run_query(label="01-plan-gap", prompt=PROMPT, max_turns=4)


if __name__ == "__main__":
    raise SystemExit(main_sync(main))
