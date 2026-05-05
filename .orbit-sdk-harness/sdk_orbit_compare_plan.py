#!/usr/bin/env python3
"""Scenario 02 — Later Correction Supersedes Plan. Real Claude Agent SDK query()."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import main_sync, run_query

PROMPT = (
    "You are validating the Orbit Claude Code plugin.\n"
    "\n"
    "An older capture-oriented plan said the project should record raw transcripts. "
    "The user later corrected this and said: 'do not capture more logs; mine existing sessions.'\n"
    "\n"
    "Use Orbit to determine whether the older plan is still controlling. State which "
    "instruction wins per Orbit's evidence ranking, and what gap Orbit would emit.\n"
    "\n"
    "Respond in <= 8 lines. Reference the relevant gap category (plan-stale, "
    "superseded-plan-item, or session-only-decision)."
)


async def main():
    return await run_query(label="02-correction-supersedes", prompt=PROMPT, max_turns=4)


if __name__ == "__main__":
    raise SystemExit(main_sync(main))
