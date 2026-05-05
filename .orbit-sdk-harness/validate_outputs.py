#!/usr/bin/env python3
"""Smoke-run orbit-audit subcommands against the local fixtures and verify outputs.

Invokes:
    python3 scripts/orbit_audit.py audit ... --output <tmp>
    python3 scripts/orbit_audit.py build-ledger ... --output <tmp>/intent-ledger.jsonl --replace

Then verifies that the expected artifacts exist, are non-empty, and contain the
required structural markers (Orbit dashboard sections, evidence schema fields,
review-window scope echo).

Exits 0 on PASS, 1 on FAIL. JSON report to stdout / optional --output.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from tempfile import TemporaryDirectory

REQUIRED_DASHBOARD_TOKENS = (
    "ORBIT",
    "Find drift",
    "#C6FF00",  # lime
    "#FF8A00",  # orange
    "#FF4D36",  # red
    "#8B3DFF",  # purple
    "#1E6BFF",  # blue
    "Intents",
    "Plan",
    "Claim",
    "Tool",
    "Gaps",
    "Timeline",
    "Uncertainty",
    "Scope",
)

REQUIRED_EVIDENCE_KEYS = (
    "schema_version",
    "generated_at",
    "scope",
    "intents",
    "plan_items",
    "claims",
    "tool_evidence",
    "validations",
    "gaps",
)


def _orbit_audit_cmd(plugin_root: Path) -> list[str]:
    return [sys.executable, str(plugin_root / "scripts" / "orbit_audit.py")]


def smoke(plugin_root: Path) -> dict:
    fixtures = plugin_root / "tests" / "fixtures"
    sample_repo = fixtures / "sample-repo"
    sample_session = fixtures / "sample-session.jsonl"
    sample_plan = fixtures / "sample-plan.md"
    report: dict = {"plugin_root": str(plugin_root), "checks": [], "status": "PASS"}

    def add(check, status, **kw):
        rec = {"check_name": check, "status": status}
        rec.update(kw)
        report["checks"].append(rec)
        if status == "FAIL":
            report["status"] = "FAIL"

    for path in (sample_repo, sample_session, sample_plan):
        if not path.exists():
            add(
                f"fixture_present_{path.name}",
                "FAIL",
                evidence_path=str(path),
                observed_value="missing",
                expected_value="present",
                failure_reason=f"missing harness/test fixture: {path}",
            )
        else:
            add(f"fixture_present_{path.name}", "PASS", evidence_path=str(path), observed_value="present", expected_value="present")
    if report["status"] == "FAIL":
        return report

    with TemporaryDirectory(prefix="orbit-smoke-") as tmp:
        tmp_path = Path(tmp)

        audit_out = tmp_path / "audit"
        audit_cmd = _orbit_audit_cmd(plugin_root) + [
            "audit",
            "--project", str(sample_repo),
            "--plans", str(sample_plan),
            "--sessions", str(sample_session),
            "--validate-codebase",
            "--days", "30",
            "--output", str(audit_out),
        ]
        proc = subprocess.run(audit_cmd, capture_output=True, text=True, timeout=120)
        add(
            "audit_subcommand_exit_zero",
            "PASS" if proc.returncode == 0 else "FAIL",
            evidence_path=str(audit_out),
            observed_value=f"returncode={proc.returncode}",
            expected_value="returncode=0",
            failure_reason="" if proc.returncode == 0 else f"audit subcommand failed: {proc.stderr[:400]}",
        )
        if proc.returncode != 0:
            return report

        evidence_path = audit_out / "evidence.json"
        for art in ("evidence.json", "gap-analysis.md", "dashboard.html", "intent-gap-flow.mmd", "intent-timeline.mmd", "plan-execution-matrix.csv"):
            ap = audit_out / art
            ok = ap.exists() and ap.stat().st_size > 0
            add(
                f"audit_artifact_{art}",
                "PASS" if ok else "FAIL",
                evidence_path=str(ap),
                observed_value=f"size={ap.stat().st_size if ap.exists() else 0}",
                expected_value="exists and non-empty",
                failure_reason="" if ok else f"missing or empty: {ap}",
            )

        if evidence_path.exists():
            data = json.loads(evidence_path.read_text(encoding="utf-8"))
            for key in REQUIRED_EVIDENCE_KEYS:
                ok = key in data
                add(
                    f"evidence_field_{key}",
                    "PASS" if ok else "FAIL",
                    evidence_path=str(evidence_path),
                    observed_value="present" if ok else "missing",
                    expected_value=f"{key} present",
                    failure_reason="" if ok else f"evidence.json missing required key '{key}'",
                )
            scope = data.get("scope", {}) if isinstance(data, dict) else {}
            scope_days_ok = scope.get("days") == 30
            add(
                "evidence_scope_days_echo",
                "PASS" if scope_days_ok else "FAIL",
                evidence_path=str(evidence_path),
                observed_value=str(scope.get("days")),
                expected_value="30",
                failure_reason="" if scope_days_ok else "scope.days does not echo --days input",
            )

        dashboard_path = audit_out / "dashboard.html"
        if dashboard_path.exists():
            html = dashboard_path.read_text(encoding="utf-8", errors="replace")
            for token in REQUIRED_DASHBOARD_TOKENS:
                ok = token in html
                add(
                    f"dashboard_token_{token}".replace(" ", "_").replace("#", "hex"),
                    "PASS" if ok else "FAIL",
                    evidence_path=str(dashboard_path),
                    observed_value="present" if ok else "missing",
                    expected_value=f"contains '{token}'",
                    failure_reason="" if ok else f"dashboard missing required marker '{token}'",
                )

        ledger_out = tmp_path / "intent-ledger.jsonl"
        ledger_cmd = _orbit_audit_cmd(plugin_root) + [
            "build-ledger",
            "--project", str(sample_repo),
            "--sessions", str(sample_session),
            "--days", "30",
            "--output", str(ledger_out),
            "--replace",
        ]
        ledger_proc = subprocess.run(ledger_cmd, capture_output=True, text=True, timeout=120)
        add(
            "build_ledger_exit_zero",
            "PASS" if ledger_proc.returncode == 0 else "FAIL",
            evidence_path=str(ledger_out),
            observed_value=f"returncode={ledger_proc.returncode}",
            expected_value="returncode=0",
            failure_reason="" if ledger_proc.returncode == 0 else f"build-ledger failed: {ledger_proc.stderr[:400]}",
        )

        if ledger_out.exists():
            content = ledger_out.read_text(encoding="utf-8")
            valid = True
            count = 0
            for line in content.splitlines():
                if not line.strip():
                    continue
                try:
                    json.loads(line)
                    count += 1
                except json.JSONDecodeError:
                    valid = False
                    break
            add(
                "ledger_lines_valid_json",
                "PASS" if valid and count > 0 else "FAIL",
                evidence_path=str(ledger_out),
                observed_value=f"valid_lines={count} all_valid={valid}",
                expected_value="all lines parse as JSON, count>=1",
                failure_reason="" if valid and count > 0 else "ledger jsonl invalid or empty",
            )
            md_companion = ledger_out.with_suffix(".md")
            md_ok = md_companion.exists() and md_companion.stat().st_size > 0
            add(
                "ledger_md_companion",
                "PASS" if md_ok else "FAIL",
                evidence_path=str(md_companion),
                observed_value="present" if md_ok else "missing",
                expected_value="markdown companion present",
                failure_reason="" if md_ok else "ledger markdown companion missing",
            )

        # render-dashboard subcommand smoke
        if evidence_path.exists():
            dash_out = tmp_path / "rendered.html"
            rd = subprocess.run(
                _orbit_audit_cmd(plugin_root) + [
                    "render-dashboard",
                    "--evidence", str(evidence_path),
                    "--output", str(dash_out),
                ],
                capture_output=True, text=True, timeout=60,
            )
            add(
                "render_dashboard_exit_zero",
                "PASS" if rd.returncode == 0 else "FAIL",
                evidence_path=str(dash_out),
                observed_value=f"returncode={rd.returncode}",
                expected_value="returncode=0",
                failure_reason="" if rd.returncode == 0 else f"render-dashboard failed: {rd.stderr[:400]}",
            )

    return report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Smoke-validate Orbit outputs.")
    parser.add_argument("--plugin-root", default=str(Path(__file__).resolve().parents[1]))
    parser.add_argument("--output")
    args = parser.parse_args(argv)
    root = Path(args.plugin_root).expanduser().resolve()
    report = smoke(root)
    text = json.dumps(report, indent=2, ensure_ascii=False) + "\n"
    print(text)
    if args.output:
        Path(args.output).expanduser().write_text(text, encoding="utf-8")
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
