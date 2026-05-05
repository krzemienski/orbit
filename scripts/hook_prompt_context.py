#!/usr/bin/env python3
"""Orbit UserPromptExpansion hook: prime audit commands with the Orbit workflow."""
from __future__ import annotations

import json
import sys


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError:
        payload = {}
    prompt = str(payload.get("prompt", ""))
    lower = prompt.lower()
    if "orbit" in lower or any(term in lower for term in ["audit", "gap", "review-window", "validate-claims", "compare-plan"]):
        print(json.dumps({
            "hookSpecificOutput": {
                "hookEventName": "UserPromptExpansion",
                "additionalContext": "Orbit workflow: mine existing sessions; extract user intent, corrections, pivots, assistant claims, and tool evidence; compare against plans; validate against repo truth; emit gaps, conflicts, uncertainty, remediation actions, and dashboard artifacts."
            }
        }))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
