#!/usr/bin/env python3
"""Scenario 09 — Instruction Ledger. Real Claude Agent SDK query() + ledger build."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import main_sync, run_query, PLUGIN_ROOT, log

PROMPT = (
    "You are validating the Orbit Claude Code plugin.\n"
    "\n"
    "Describe Orbit's durable instruction ledger: which signals it watches "
    "('actually', 'we decided', 'go with', 'from now on', 'do not', 'changed our mind', etc.), "
    "the JSONL record fields it writes, and how it differentiates active from superseded entries.\n"
    "\n"
    "Respond in <= 10 lines."
)


async def amain():
    summary = await run_query(label="09-instruction-ledger", prompt=PROMPT, max_turns=4)
    fixtures = PLUGIN_ROOT / "tests" / "fixtures"
    sample_session = fixtures / "sample-session.jsonl"
    sample_repo = fixtures / "sample-repo"
    if sample_session.exists() and sample_repo.exists():
        target = Path(summary["run_dir"]) / "intent-ledger.jsonl"
        proc = subprocess.run(
            [
                sys.executable,
                str(PLUGIN_ROOT / "scripts" / "orbit_audit.py"),
                "build-ledger",
                "--project", str(sample_repo),
                "--sessions", str(sample_session),
                "--days", "30",
                "--output", str(target),
                "--replace",
            ],
            capture_output=True, text=True, timeout=60,
        )
        (Path(summary["run_dir"]) / "build-ledger-stderr.txt").write_text(proc.stderr or "", encoding="utf-8")
        ledger_md = target.with_suffix(".md")
        if target.exists():
            valid = 0
            invalid = 0
            for line in target.read_text(encoding="utf-8").splitlines():
                if not line.strip():
                    continue
                try:
                    json.loads(line)
                    valid += 1
                except json.JSONDecodeError:
                    invalid += 1
            summary["ledger_jsonl"] = str(target)
            summary["ledger_jsonl_valid_lines"] = valid
            summary["ledger_jsonl_invalid_lines"] = invalid
            summary["ledger_md"] = str(ledger_md)
            summary["ledger_md_present"] = ledger_md.exists()
    return summary


if __name__ == "__main__":
    raise SystemExit(main_sync(amain))
