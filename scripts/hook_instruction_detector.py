#!/usr/bin/env python3
"""Orbit UserPromptSubmit hook: detect durable instruction candidates without duplicating transcripts."""
from __future__ import annotations

import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

PATTERNS = [
    "actually", "no, instead", "we decided", "go with", "settled on", "from now on",
    "remember this", "make sure", "must include", "do not", "you forgot",
    "this is wrong", "changed our mind", "gap analysis", "validate", "dashboard",
]


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def plugin_data_dir() -> Path:
    value = os.environ.get("CLAUDE_PLUGIN_DATA")
    if value:
        return Path(value)
    return Path.cwd() / ".claude" / "audits" / "orbit-plugin-data"


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError:
        payload = {}
    prompt = str(payload.get("prompt", ""))
    lower = prompt.lower()
    matches = [pattern for pattern in PATTERNS if pattern in lower]
    if matches:
        data_dir = plugin_data_dir()
        data_dir.mkdir(parents=True, exist_ok=True)
        record = {
            "schema_version": "0.2",
            "timestamp": now_iso(),
            "cwd": payload.get("cwd") or os.getcwd(),
            "source": "UserPromptSubmit",
            "kind": "candidate_instruction",
            "confidence": "medium",
            "prompt_excerpt": prompt[:1000],
            "detected_patterns": matches,
            "requires_session_mining": True,
            "status": "candidate",
        }
        with (data_dir / "intent-ledger-candidates.jsonl").open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")

    audit_like = any(term in lower for term in ["audit", "look back", "review sessions", "what did we miss", "gap analysis", "validate claims", "compare to the plan"])
    if audit_like:
        print(json.dumps({
            "hookSpecificOutput": {
                "hookEventName": "UserPromptSubmit",
                "additionalContext": "Use Orbit. Do not rely only on plans. Mine session transcripts, compare user intent against plan evidence, assistant claims, tool evidence, and repo truth. Validate completion claims before marking items complete. Return gaps, conflicts, and uncertainty separately."
            }
        }))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
