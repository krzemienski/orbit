#!/usr/bin/env python3
"""Scenario 10 — Plugin Compliance.

Runs the static manifest + hook + command + skill + outputs validators in a single
sweep, then makes ONE real SDK query() asking the agent to describe Orbit packaging
expectations. The static validator JSON files are the load-bearing evidence; the SDK
transcript is the live confirmation.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import main_sync, run_query, PLUGIN_ROOT, HARNESS_ROOT, log

SDK_PROMPT = (
    "You are validating the Orbit Claude Code plugin packaging.\n"
    "\n"
    "List Orbit's required packaging surfaces (.claude-plugin/plugin.json, skills/, "
    "commands/, hooks/hooks.json, scripts/, bin/, README.md, CHANGELOG.md, PRD.md), "
    "and confirm that Orbit ships WITHOUT a Dockerfile, docker-compose, or Python "
    "package layout (per PRD approval scope).\n"
    "\n"
    "Respond in <= 8 lines."
)


async def amain():
    summary = await run_query(label="10-plugin-compliance", prompt=SDK_PROMPT, max_turns=4)
    run_dir = Path(summary["run_dir"])
    static_results: dict[str, dict] = {}
    for name, script in [
        ("manifest", "validate_plugin_manifest.py"),
        ("frontmatter", "validate_skill_frontmatter.py"),
        ("commands", "validate_commands.py"),
        ("hooks", "validate_hooks.py"),
        ("outputs", "validate_outputs.py"),
    ]:
        out_path = run_dir / f"{name}.json"
        cmd = [sys.executable, str(HARNESS_ROOT / script), "--output", str(out_path)]
        if name in {"manifest", "commands", "hooks", "outputs"}:
            cmd += ["--plugin-root", str(PLUGIN_ROOT)]
        else:
            cmd += ["--skills-dir", str(PLUGIN_ROOT / "skills")]
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
        try:
            static_results[name] = json.loads(out_path.read_text(encoding="utf-8")) if out_path.exists() else {"status": "FAIL"}
        except json.JSONDecodeError:
            static_results[name] = {"status": "FAIL", "stderr": proc.stderr[:500]}
        static_results[name]["_returncode"] = proc.returncode
    (run_dir / "static-summary.json").write_text(json.dumps(static_results, indent=2), encoding="utf-8")
    summary["static_validators"] = {k: v.get("status") for k, v in static_results.items()}
    summary["static_validators_all_pass"] = all(v.get("status") == "PASS" for v in static_results.values())
    return summary


if __name__ == "__main__":
    raise SystemExit(main_sync(amain))
