#!/usr/bin/env python3
"""Validate Orbit hooks/hooks.json + hook scripts (parsing, executable bit, JSON I/O smoke).

Exits 0 on PASS, 1 on FAIL. Writes JSON report to stdout (and optional file).
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

ALLOWED_EVENTS = {
    "PreToolUse",
    "PostToolUse",
    "UserPromptSubmit",
    "UserPromptExpansion",
    "SessionStart",
    "Stop",
    "SubagentStart",
    "SubagentStop",
    "Notification",
}


def _expand(cmd: str, plugin_root: Path) -> str:
    return cmd.replace("${CLAUDE_PLUGIN_ROOT}", str(plugin_root)).replace("$CLAUDE_PLUGIN_ROOT", str(plugin_root))


def validate(plugin_root: Path) -> dict:
    hooks_file = plugin_root / "hooks" / "hooks.json"
    report: dict = {"plugin_root": str(plugin_root), "hooks_file": str(hooks_file), "checks": [], "status": "PASS"}

    def add(check, status, **kw):
        rec = {"check_name": check, "status": status}
        rec.update(kw)
        report["checks"].append(rec)
        if status == "FAIL":
            report["status"] = "FAIL"

    if not hooks_file.exists():
        add(
            "hooks_file_present",
            "FAIL",
            evidence_path=str(hooks_file),
            observed_value="missing",
            expected_value="present",
            failure_reason="hooks/hooks.json not found",
        )
        return report

    add("hooks_file_present", "PASS", evidence_path=str(hooks_file), observed_value="present", expected_value="present")

    try:
        data = json.loads(hooks_file.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        add(
            "hooks_file_parses",
            "FAIL",
            evidence_path=str(hooks_file),
            observed_value=f"JSONDecodeError: {exc}",
            expected_value="valid JSON",
            failure_reason="hooks.json is not valid JSON",
        )
        return report

    add("hooks_file_parses", "PASS", evidence_path=str(hooks_file), observed_value="valid JSON", expected_value="valid JSON")

    hooks_section = data.get("hooks") if isinstance(data, dict) else None
    if not isinstance(hooks_section, dict) or not hooks_section:
        add(
            "hooks_section_present",
            "FAIL",
            evidence_path=str(hooks_file),
            observed_value=type(hooks_section).__name__,
            expected_value="non-empty 'hooks' object",
            failure_reason="missing or empty 'hooks' object",
        )
        return report

    add("hooks_section_present", "PASS", evidence_path=str(hooks_file), observed_value=f"{len(hooks_section)} events", expected_value="non-empty 'hooks' object")

    for event_name, groups in hooks_section.items():
        if event_name not in ALLOWED_EVENTS:
            add(
                f"event_recognized_{event_name}",
                "FAIL",
                evidence_path=str(hooks_file),
                observed_value=event_name,
                expected_value=f"one of {sorted(ALLOWED_EVENTS)}",
                failure_reason="unrecognized hook event name",
            )
            continue
        add(f"event_recognized_{event_name}", "PASS", evidence_path=str(hooks_file), observed_value=event_name, expected_value="known event")
        if not isinstance(groups, list):
            add(
                f"event_groups_list_{event_name}",
                "FAIL",
                evidence_path=str(hooks_file),
                observed_value=type(groups).__name__,
                expected_value="list",
                failure_reason="event must map to a list of matcher groups",
            )
            continue
        for idx, group in enumerate(groups):
            if not isinstance(group, dict) or "hooks" not in group:
                add(
                    f"group_shape_{event_name}_{idx}",
                    "FAIL",
                    evidence_path=str(hooks_file),
                    observed_value=str(group),
                    expected_value="object with 'hooks' list",
                    failure_reason="malformed matcher group",
                )
                continue
            for hidx, hook in enumerate(group.get("hooks", [])):
                cmd = hook.get("command", "")
                expanded = _expand(cmd, plugin_root)
                cmd_path = Path(expanded.split()[0]) if expanded else Path("")
                exists = cmd_path.exists()
                add(
                    f"hook_command_exists_{event_name}_{idx}_{hidx}",
                    "PASS" if exists else "FAIL",
                    evidence_path=str(cmd_path),
                    observed_value="present" if exists else "missing",
                    expected_value="present",
                    failure_reason="" if exists else f"hook script missing: {cmd_path}",
                )
                if exists:
                    is_x = os.access(cmd_path, os.X_OK)
                    add(
                        f"hook_command_executable_{event_name}_{idx}_{hidx}",
                        "PASS" if is_x else "FAIL",
                        evidence_path=str(cmd_path),
                        observed_value="executable" if is_x else "not executable",
                        expected_value="executable",
                        failure_reason="" if is_x else f"chmod +x missing: {cmd_path}",
                    )
                    smoke = _smoke_hook(cmd_path)
                    add(
                        f"hook_command_smoke_{event_name}_{idx}_{hidx}",
                        "PASS" if smoke["ok"] else "FAIL",
                        evidence_path=str(cmd_path),
                        observed_value=smoke["observed"],
                        expected_value="exit 0 with optional stdout JSON",
                        failure_reason="" if smoke["ok"] else smoke["reason"],
                    )

    return report


def _smoke_hook(cmd_path: Path) -> dict:
    """Send a benign payload to the hook on stdin. Hook must exit 0 and not block."""
    payload = json.dumps({
        "prompt": "smoke test for orbit hook",
        "cwd": str(cmd_path.parent),
    })
    try:
        proc = subprocess.run(
            [sys.executable, str(cmd_path)],
            input=payload,
            capture_output=True,
            text=True,
            timeout=10,
        )
    except subprocess.TimeoutExpired:
        return {"ok": False, "observed": "timeout", "reason": "hook did not exit within 10s"}
    if proc.returncode != 0:
        return {
            "ok": False,
            "observed": f"exit={proc.returncode}",
            "reason": f"non-zero exit. stderr={proc.stderr[:240]}",
        }
    if proc.stdout.strip():
        try:
            json.loads(proc.stdout)
        except json.JSONDecodeError as exc:
            return {
                "ok": False,
                "observed": f"non-json stdout: {proc.stdout[:120]}",
                "reason": f"hook stdout must be JSON when present: {exc}",
            }
    return {"ok": True, "observed": f"exit=0 stdout_chars={len(proc.stdout)}", "reason": ""}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate Orbit hooks.")
    parser.add_argument("--plugin-root", default=str(Path(__file__).resolve().parents[1]))
    parser.add_argument("--output", help="Optional output path.")
    args = parser.parse_args(argv)
    plugin_root = Path(args.plugin_root).expanduser().resolve()
    report = validate(plugin_root)
    text = json.dumps(report, indent=2, ensure_ascii=False) + "\n"
    print(text)
    if args.output:
        Path(args.output).expanduser().write_text(text, encoding="utf-8")
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
