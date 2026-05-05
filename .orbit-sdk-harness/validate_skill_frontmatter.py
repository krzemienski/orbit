#!/usr/bin/env python3
"""Validate every Orbit SKILL.md against the Claude Code skill frontmatter contract.

Each SKILL.md must:
- start with a YAML frontmatter block delimited by --- ... ---
- declare a `name` (lowercase letters, digits, hyphens; <= 64 chars)
- declare a non-empty `description` with no XML tags and length <= 1024 chars
- be followed by a non-empty body that describes the operational workflow

Exits 0 on PASS, 1 on any FAIL. Prints a JSON report on stdout.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

NAME_RE = re.compile(r"^[a-z0-9-]+$")
XML_TAG_RE = re.compile(r"<[^>]+>")
MAX_NAME_LEN = 64
MAX_DESC_LEN = 1024


def parse_frontmatter(text: str) -> tuple[dict, str, str | None]:
    if not text.startswith("---"):
        return {}, text, "missing leading ---"
    end = text.find("\n---", 3)
    if end == -1:
        return {}, text, "missing trailing ---"
    raw = text[3:end].strip("\n")
    body = text[end + 4 :].lstrip("\n")
    fields: dict[str, str] = {}
    current = None
    for line in raw.splitlines():
        if not line.strip():
            continue
        if line.startswith((" ", "\t")) and current:
            fields[current] = (fields.get(current, "") + " " + line.strip()).strip()
            continue
        if ":" in line:
            key, _, value = line.partition(":")
            current = key.strip()
            fields[current] = value.strip()
    return fields, body, None


def validate_skill(skill_md: Path) -> list[dict]:
    text = skill_md.read_text(encoding="utf-8", errors="replace")
    fields, body, parse_err = parse_frontmatter(text)
    checks: list[dict] = []

    def add(check, status, **kw):
        rec = {"check_name": check, "status": status, "evidence_path": str(skill_md)}
        rec.update(kw)
        checks.append(rec)

    if parse_err:
        add(
            "frontmatter_present",
            "FAIL",
            observed_value=parse_err,
            expected_value="--- ... --- block at top of file",
            failure_reason=parse_err,
        )
        return checks

    add("frontmatter_present", "PASS", observed_value="parsed", expected_value="--- ... --- block at top of file")

    name = fields.get("name", "")
    if not name:
        add("frontmatter_name_present", "FAIL", observed_value="missing", expected_value="present", failure_reason="frontmatter missing 'name'")
    else:
        add("frontmatter_name_present", "PASS", observed_value=name, expected_value="present")
        if NAME_RE.match(name) and len(name) <= MAX_NAME_LEN:
            add("frontmatter_name_format", "PASS", observed_value=name, expected_value="^[a-z0-9-]+$ and <=64 chars")
        else:
            add(
                "frontmatter_name_format",
                "FAIL",
                observed_value=name,
                expected_value="^[a-z0-9-]+$ and <=64 chars",
                failure_reason="invalid skill name format",
            )

    desc = fields.get("description", "")
    if not desc.strip():
        add("frontmatter_description_present", "FAIL", observed_value="missing or empty", expected_value="non-empty string", failure_reason="missing description")
    else:
        add("frontmatter_description_present", "PASS", observed_value=f"len={len(desc)}", expected_value="non-empty string")
        if XML_TAG_RE.search(desc):
            add(
                "frontmatter_description_no_xml",
                "FAIL",
                observed_value="contains XML-like tags",
                expected_value="no XML tags",
                failure_reason="description contains <...> tags",
            )
        else:
            add("frontmatter_description_no_xml", "PASS", observed_value="no XML tags", expected_value="no XML tags")
        if len(desc) <= MAX_DESC_LEN:
            add("frontmatter_description_length", "PASS", observed_value=f"len={len(desc)}", expected_value=f"<= {MAX_DESC_LEN}")
        else:
            add(
                "frontmatter_description_length",
                "FAIL",
                observed_value=f"len={len(desc)}",
                expected_value=f"<= {MAX_DESC_LEN}",
                failure_reason="description too long",
            )

    if body.strip():
        add("body_non_empty", "PASS", observed_value=f"body_chars={len(body)}", expected_value="non-empty body")
    else:
        add("body_non_empty", "FAIL", observed_value="empty", expected_value="non-empty body", failure_reason="skill body is empty")

    return checks


def validate_all(skills_dir: Path) -> dict:
    report: dict = {"skills_dir": str(skills_dir), "skills": [], "status": "PASS"}
    if not skills_dir.exists():
        report["status"] = "FAIL"
        report["error"] = f"skills dir not found: {skills_dir}"
        return report
    for child in sorted(skills_dir.iterdir()):
        if not child.is_dir():
            continue
        skill_md = child / "SKILL.md"
        if not skill_md.exists():
            report["skills"].append({
                "name": child.name,
                "status": "FAIL",
                "checks": [{
                    "check_name": "skill_md_present",
                    "status": "FAIL",
                    "evidence_path": str(skill_md),
                    "observed_value": "missing",
                    "expected_value": "present",
                    "failure_reason": "SKILL.md not found",
                }],
            })
            report["status"] = "FAIL"
            continue
        checks = validate_skill(skill_md)
        skill_status = "PASS" if all(c["status"] == "PASS" for c in checks) else "FAIL"
        if skill_status == "FAIL":
            report["status"] = "FAIL"
        report["skills"].append({"name": child.name, "skill_md": str(skill_md), "status": skill_status, "checks": checks})
    return report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate Orbit skill frontmatter.")
    parser.add_argument("--skills-dir", default=str(Path(__file__).resolve().parents[1] / "skills"))
    parser.add_argument("--output", help="Optional output path.")
    args = parser.parse_args(argv)
    skills_dir = Path(args.skills_dir).expanduser().resolve()
    report = validate_all(skills_dir)
    text = json.dumps(report, indent=2, ensure_ascii=False) + "\n"
    print(text)
    if args.output:
        Path(args.output).expanduser().write_text(text, encoding="utf-8")
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
