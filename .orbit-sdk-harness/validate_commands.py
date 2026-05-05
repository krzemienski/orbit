#!/usr/bin/env python3
"""Validate Orbit slash command markdown files.

Each command must:
- exist under commands/<name>.md
- be non-empty
- contain a purpose section (heading or first paragraph)
- contain at least one usage example (```bash or ```text fenced block)
- map to an Orbit skill or CLI workflow (mention orbit-audit or skill name)

The review-window command additionally must mention --days, --since, --from, --to.
The review-last-3-days command must declare itself as alias for --days 3.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

REQUIRED_COMMANDS = (
    "audit-gaps",
    "mine-intent",
    "validate-claims",
    "render-dashboard",
    "compare-plan",
    "review-window",
    "review-last-3-days",
    "rebuild-ledger",
)


def validate(plugin_root: Path) -> dict:
    commands_dir = plugin_root / "commands"
    report: dict = {"plugin_root": str(plugin_root), "commands_dir": str(commands_dir), "checks": [], "status": "PASS"}

    def add(check, status, **kw):
        rec = {"check_name": check, "status": status}
        rec.update(kw)
        report["checks"].append(rec)
        if status == "FAIL":
            report["status"] = "FAIL"

    if not commands_dir.exists():
        add("commands_dir_present", "FAIL", evidence_path=str(commands_dir), observed_value="missing", expected_value="present", failure_reason="commands directory missing")
        return report

    add("commands_dir_present", "PASS", evidence_path=str(commands_dir), observed_value="present", expected_value="present")

    for name in REQUIRED_COMMANDS:
        path = commands_dir / f"{name}.md"
        if not path.exists():
            add(
                f"command_present_{name}",
                "FAIL",
                evidence_path=str(path),
                observed_value="missing",
                expected_value="present",
                failure_reason=f"command markdown missing for /{name}",
            )
            continue

        text = path.read_text(encoding="utf-8", errors="replace")
        add(f"command_present_{name}", "PASS", evidence_path=str(path), observed_value="present", expected_value="present")

        body_non_empty = bool(text.strip())
        add(
            f"command_body_non_empty_{name}",
            "PASS" if body_non_empty else "FAIL",
            evidence_path=str(path),
            observed_value=f"chars={len(text.strip())}",
            expected_value="non-empty",
            failure_reason="" if body_non_empty else "empty command body",
        )

        has_heading = re.search(r"^#\s+\S+", text, flags=re.MULTILINE) is not None
        add(
            f"command_has_purpose_heading_{name}",
            "PASS" if has_heading else "FAIL",
            evidence_path=str(path),
            observed_value="heading present" if has_heading else "no leading heading",
            expected_value="markdown heading present",
            failure_reason="" if has_heading else "command needs a leading purpose heading",
        )

        fenced = re.findall(r"```(?:bash|text|sh|shell)?\n(.*?)\n```", text, flags=re.DOTALL)
        has_example = bool(fenced)
        add(
            f"command_has_example_{name}",
            "PASS" if has_example else "FAIL",
            evidence_path=str(path),
            observed_value=f"fenced_blocks={len(fenced)}",
            expected_value=">=1 fenced example block",
            failure_reason="" if has_example else "no usage example",
        )

        joined = " ".join(fenced).lower()
        mapped = ("orbit-audit" in text.lower()) or ("orbit-audit" in joined) or ("skill" in joined)
        add(
            f"command_maps_to_workflow_{name}",
            "PASS" if mapped else "FAIL",
            evidence_path=str(path),
            observed_value="mentions orbit-audit or skill" if mapped else "no helper or skill mentioned",
            expected_value="mentions orbit-audit or skill",
            failure_reason="" if mapped else "command must map to an Orbit skill or orbit-audit invocation",
        )

        if name == "review-window":
            for flag in ("--days", "--since", "--from", "--to"):
                ok = flag in text
                add(
                    f"review_window_documents_{flag.lstrip('-')}",
                    "PASS" if ok else "FAIL",
                    evidence_path=str(path),
                    observed_value="present" if ok else "missing",
                    expected_value=f"{flag} documented",
                    failure_reason="" if ok else f"review-window must document {flag}",
                )

        if name == "review-last-3-days":
            alias_doc = "--days 3" in text or "days 3" in text
            add(
                "review_last_3_days_alias",
                "PASS" if alias_doc else "FAIL",
                evidence_path=str(path),
                observed_value="alias documented" if alias_doc else "alias not documented",
                expected_value="documents alias for --days 3",
                failure_reason="" if alias_doc else "review-last-3-days must document itself as alias for --days 3",
            )

    return report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate Orbit commands.")
    parser.add_argument("--plugin-root", default=str(Path(__file__).resolve().parents[1]))
    parser.add_argument("--output")
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
