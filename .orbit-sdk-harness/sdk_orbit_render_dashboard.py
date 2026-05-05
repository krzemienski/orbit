#!/usr/bin/env python3
"""Scenario 05 — Dashboard Required. Real Claude Agent SDK query() + dashboard render check."""
from __future__ import annotations

import json
import sys
import subprocess
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import main_sync, run_query, PLUGIN_ROOT, RUNS_ROOT, log

PROMPT = (
    "You are validating the Orbit Claude Code plugin.\n"
    "\n"
    "Orbit must render a static HTML dashboard at .claude/audits/latest/dashboard.html "
    "with summary cards, intent timeline, intent-plan-claim-tool-repo matrix, gaps, "
    "claim validation, and uncertainty sections, on a flat black background with the "
    "lime/orange/red/purple/blue accent palette.\n"
    "\n"
    "List the structural sections Orbit's dashboard contains and which color rules govern "
    "severity. Respond in <= 10 lines. Do not create files."
)


async def amain():
    summary = await run_query(label="05-dashboard-required", prompt=PROMPT, max_turns=4)
    # After the SDK run, ALSO physically render the dashboard from the bundled sample evidence
    # so this scenario captures functional dashboard verification, not only an agent description.
    sample_evidence = PLUGIN_ROOT / "examples" / "sample-evidence.json"
    if sample_evidence.exists():
        target = Path(summary["run_dir"]) / "rendered-dashboard.html"
        proc = subprocess.run(
            [
                sys.executable,
                str(PLUGIN_ROOT / "scripts" / "orbit_audit.py"),
                "render-dashboard",
                "--evidence", str(sample_evidence),
                "--output", str(target),
            ],
            capture_output=True, text=True, timeout=60,
        )
        (Path(summary["run_dir"]) / "render-dashboard-stderr.txt").write_text(proc.stderr or "", encoding="utf-8")
        if target.exists():
            html = target.read_text(encoding="utf-8")
            tokens = ["ORBIT", "Find drift", "#C6FF00", "#FF8A00", "#FF4D36", "#8B3DFF", "#1E6BFF",
                      "Timeline", "Claim Validation", "Uncertainty", "Scope"]
            present = {t: (t in html) for t in tokens}
            (Path(summary["run_dir"]) / "dashboard-token-check.json").write_text(
                json.dumps({"target": str(target), "present": present, "all_present": all(present.values())}, indent=2),
                encoding="utf-8",
            )
            summary["dashboard_render_returncode"] = proc.returncode
            summary["dashboard_target"] = str(target)
            summary["dashboard_tokens_all_present"] = all(present.values())
    return summary


if __name__ == "__main__":
    raise SystemExit(main_sync(amain))
