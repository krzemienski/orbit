#!/usr/bin/env python3
"""Validate orbit/.claude-plugin/plugin.json against the Claude Code plugin manifest contract.

Exits 0 on PASS. Exits 1 if any required check FAILs. Prints a JSON report on stdout.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REQUIRED_TOP_LEVEL = ("name",)
RECOGNIZED_SUB_PATHS = ("skills", "commands", "agents", "hooks", "mcps")


def validate(plugin_root: Path) -> dict:
    manifest_path = plugin_root / ".claude-plugin" / "plugin.json"
    report = {
        "plugin_root": str(plugin_root),
        "manifest_path": str(manifest_path),
        "checks": [],
        "status": "PASS",
    }

    def add(check_name: str, status: str, **kw):
        rec = {"check_name": check_name, "status": status}
        rec.update(kw)
        report["checks"].append(rec)
        if status == "FAIL":
            report["status"] = "FAIL"

    if not manifest_path.exists():
        add(
            "manifest_exists",
            "FAIL",
            evidence_path=str(manifest_path),
            observed_value="missing",
            expected_value="present",
            failure_reason="plugin.json not found",
        )
        return report

    add("manifest_exists", "PASS", evidence_path=str(manifest_path), observed_value="present", expected_value="present")

    try:
        data = json.loads(manifest_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        add(
            "manifest_parses",
            "FAIL",
            evidence_path=str(manifest_path),
            observed_value=f"JSONDecodeError: {exc}",
            expected_value="valid JSON object",
            failure_reason="manifest is not valid JSON",
        )
        return report

    if not isinstance(data, dict):
        add(
            "manifest_is_object",
            "FAIL",
            evidence_path=str(manifest_path),
            observed_value=type(data).__name__,
            expected_value="object",
            failure_reason="manifest must be a JSON object",
        )
        return report

    add("manifest_parses", "PASS", evidence_path=str(manifest_path), observed_value="valid JSON object", expected_value="valid JSON object")

    name = data.get("name")
    if not isinstance(name, str) or not name.strip():
        add(
            "manifest_name_present",
            "FAIL",
            evidence_path=str(manifest_path),
            observed_value=repr(name),
            expected_value="non-empty string",
            failure_reason="manifest 'name' missing or empty",
        )
    else:
        add("manifest_name_present", "PASS", evidence_path=str(manifest_path), observed_value=name, expected_value="non-empty string")

    if name == "orbit":
        add("manifest_name_orbit", "PASS", evidence_path=str(manifest_path), observed_value="orbit", expected_value="orbit")
    else:
        add(
            "manifest_name_orbit",
            "FAIL",
            evidence_path=str(manifest_path),
            observed_value=str(name),
            expected_value="orbit",
            failure_reason="plugin name must be 'orbit'",
        )

    version = data.get("version")
    if isinstance(version, str) and version.strip():
        add("manifest_version_present", "PASS", evidence_path=str(manifest_path), observed_value=version, expected_value="non-empty string")
    else:
        add("manifest_version_present", "FAIL", evidence_path=str(manifest_path), observed_value=repr(version), expected_value="non-empty string", failure_reason="missing version")

    description = data.get("description")
    if isinstance(description, str) and description.strip():
        add("manifest_description_present", "PASS", evidence_path=str(manifest_path), observed_value="present", expected_value="non-empty string")
    else:
        add("manifest_description_present", "FAIL", evidence_path=str(manifest_path), observed_value=repr(description), expected_value="non-empty string", failure_reason="missing description")

    for key in RECOGNIZED_SUB_PATHS:
        if key not in data:
            continue
        rel = data[key]
        if not isinstance(rel, str):
            add(
                f"manifest_path_{key}",
                "FAIL",
                evidence_path=str(manifest_path),
                observed_value=repr(rel),
                expected_value="string path relative to plugin root",
                failure_reason=f"{key} field must be a string path",
            )
            continue
        target = (plugin_root / rel).resolve()
        if target.exists():
            add(
                f"manifest_path_{key}",
                "PASS",
                evidence_path=str(target),
                observed_value=str(target),
                expected_value="path exists",
            )
        else:
            add(
                f"manifest_path_{key}",
                "FAIL",
                evidence_path=str(target),
                observed_value="missing",
                expected_value="path exists",
                failure_reason=f"manifest references missing path for '{key}': {rel}",
            )

    return report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate Orbit plugin.json manifest.")
    parser.add_argument("--plugin-root", default=str(Path(__file__).resolve().parents[1]))
    parser.add_argument("--output", help="Optional report path (json).")
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
