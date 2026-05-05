#!/usr/bin/env python3
"""Scenario 07 — Hook Candidate Instruction.

Drives Orbit's UserPromptSubmit hook directly with several payloads (no SDK call needed
for the hook itself — it reads stdin JSON), then makes ONE real Claude Agent SDK query()
that exercises a hook-relevant phrase end-to-end so the captured transcript records
real hook-level behavior. The candidate JSONL written by the hook is the load-bearing
evidence.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import main_sync, run_query, PLUGIN_ROOT, log

HOOK_SCRIPT = PLUGIN_ROOT / "scripts" / "hook_instruction_detector.py"

PAYLOADS = [
    "Actually, go with Orbit.",
    "Make sure dashboard visualization is first-class.",
    "Do not capture more logs; mine existing sessions.",
    "We changed our mind over the last few days.",
]

SDK_PROMPT = (
    "You are validating the Orbit Claude Code plugin.\n"
    "\n"
    "Confirm that Orbit's UserPromptSubmit hook detects durable instruction candidates "
    "(phrases like 'actually', 'we decided', 'do not', 'changed our mind') and writes "
    "compact candidate records WITHOUT duplicating raw transcripts. Describe the record "
    "schema fields the hook emits.\n"
    "\n"
    "Respond in <= 8 lines."
)


async def amain():
    summary = await run_query(label="07-hook-candidate", prompt=SDK_PROMPT, max_turns=4)
    run_dir = Path(summary["run_dir"])
    hook_data_dir = tempfile.mkdtemp(prefix="orbit-hook-", dir=str(run_dir))
    hook_data = Path(hook_data_dir)
    env = os.environ.copy()
    env["CLAUDE_PLUGIN_DATA"] = str(hook_data)
    invocations = []
    for idx, prompt_text in enumerate(PAYLOADS, start=1):
        payload = {"prompt": prompt_text, "cwd": str(run_dir)}
        proc = subprocess.run(
            [sys.executable, str(HOOK_SCRIPT)],
            input=json.dumps(payload),
            capture_output=True, text=True, timeout=10,
            env=env,
        )
        invocations.append({
            "index": idx,
            "prompt_text": prompt_text,
            "returncode": proc.returncode,
            "stdout": proc.stdout[:500],
            "stderr": proc.stderr[:500],
        })
    candidate_file = hook_data / "intent-ledger-candidates.jsonl"
    candidate_records: list[dict] = []
    if candidate_file.exists():
        for line in candidate_file.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            try:
                candidate_records.append(json.loads(line))
            except json.JSONDecodeError:
                pass
    (run_dir / "hook-invocations.json").write_text(json.dumps(invocations, indent=2), encoding="utf-8")
    (run_dir / "hook-candidates.json").write_text(
        json.dumps({"file": str(candidate_file), "records": candidate_records}, indent=2),
        encoding="utf-8",
    )
    summary["hook_invocation_count"] = len(invocations)
    summary["hook_candidate_records"] = len(candidate_records)
    summary["hook_candidate_file"] = str(candidate_file) if candidate_file.exists() else None
    return summary


if __name__ == "__main__":
    raise SystemExit(main_sync(amain))
