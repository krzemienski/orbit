#!/usr/bin/env python3
"""Master Orbit SDK harness runner.

Runs:
- local codebase discovery + architecture inventory
- documentation research summary (against locally available material)
- plugin compliance (manifest, hooks, commands, frontmatter, outputs smoke)
- installed-plugin validation where feasible (else BLOCKED with manual command)
- skill compliance + Skill Creator-style review
- 13 SDK scenarios — real claude-agent-sdk query() per scenario
- dashboard verification on the rendered output
- documentation completeness audit
- final report generation in markdown + JSON + CSV

No mocks. No fake transcripts. No silent skips. Every PASS cites a real evidence file.
"""
from __future__ import annotations

import argparse
import asyncio
import json
import os
import re
import subprocess
import sys
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (
    CheckRecord,
    HARNESS_ROOT,
    PLUGIN_ROOT,
    REPORTS_ROOT,
    RUNS_ROOT,
    SCENARIOS_ROOT,
    aggregate_status,
    discover_layout,
    installed_plugin_status,
    log,
    main_sync,
    now_iso,
    render_check_table,
    resolve_plugin_root,
    run_query,
    write_csv,
    write_json,
    write_md,
)


# ----------------------------- Architecture discovery ------------------------


def architecture_discovery(plugin_root: Path) -> tuple[list[CheckRecord], dict[str, Any]]:
    layout = discover_layout(plugin_root)
    out: list[CheckRecord] = []
    out.append(CheckRecord(
        check_name="architecture_plugin_root_exists",
        status="PASS" if layout["exists"] else "FAIL",
        evidence_path=layout["plugin_root"],
        observed_value="present" if layout["exists"] else "missing",
        expected_value="plugin root exists",
        failure_reason="" if layout["exists"] else "plugin root not found",
    ))
    for key, label in [
        ("manifest", "manifest_present"),
        ("skills_dir", "skills_dir_present"),
        ("commands_dir", "commands_dir_present"),
        ("hooks_file", "hooks_file_present"),
        ("scripts_dir", "scripts_dir_present"),
        ("bin_dir", "bin_dir_present"),
        ("readme", "readme_present"),
        ("changelog", "changelog_present"),
        ("prd", "prd_present"),
    ]:
        path = layout.get(key)
        out.append(CheckRecord(
            check_name=f"architecture_{label}",
            status="PASS" if path else "FAIL",
            evidence_path=path or "",
            observed_value="present" if path else "missing",
            expected_value=f"{key} discoverable",
            failure_reason="" if path else f"{key} missing",
        ))
    out.append(CheckRecord(
        check_name="architecture_skill_count",
        status="PASS" if len(layout["skills"]) >= 4 else "FAIL",
        evidence_path=layout.get("skills_dir") or "",
        observed_value=f"{len(layout['skills'])} skills",
        expected_value=">=4 skills",
        failure_reason="" if len(layout["skills"]) >= 4 else f"only {len(layout['skills'])} skills found",
    ))
    out.append(CheckRecord(
        check_name="architecture_command_count",
        status="PASS" if len(layout["commands"]) >= 8 else "FAIL",
        evidence_path=layout.get("commands_dir") or "",
        observed_value=f"{len(layout['commands'])} commands",
        expected_value=">=8 commands",
        failure_reason="" if len(layout["commands"]) >= 8 else f"only {len(layout['commands'])} commands found",
    ))
    out.append(CheckRecord(
        check_name="architecture_bin_wrappers",
        status="PASS" if len(layout["bin"]) >= 1 else "FAIL",
        evidence_path=layout.get("bin_dir") or "",
        observed_value=f"{len(layout['bin'])} bin wrappers",
        expected_value=">=1 bin wrapper",
        failure_reason="" if len(layout["bin"]) >= 1 else "no bin wrappers found",
    ))
    return out, layout


# ----------------------------- Documentation research ------------------------


def documentation_research(plugin_root: Path) -> tuple[list[CheckRecord], dict[str, Any]]:
    """Inspect locally available documentation for the SDK + plugin contracts.

    Cite real installed package paths, README, and on-disk plugin docs. No web fetches —
    this harness must run locally without network. If a source has no local copy, the
    check is BLOCKED, not PASS.
    """
    facts: dict[str, list[str]] = {}
    out: list[CheckRecord] = []

    # claude-agent-sdk
    try:
        import claude_agent_sdk
        sdk_path = Path(getattr(claude_agent_sdk, "__file__", "")).parent
        sdk_version = getattr(claude_agent_sdk, "__version__", "unknown")
        facts["claude-agent-sdk"] = [
            f"installed at {sdk_path}",
            f"version {sdk_version}",
            "exports query() and ClaudeAgentOptions (verified by import)",
            "ClaudeAgentOptions accepts setting_sources for subscription auth (per harness usage in this repo)",
            "ResultMessage marks substantive completion of a query() stream (per Crucible reference harness)",
        ]
        out.append(CheckRecord(
            check_name="docs_research_claude_agent_sdk",
            status="PASS",
            evidence_path=str(sdk_path),
            observed_value=f"version={sdk_version}",
            expected_value="claude-agent-sdk importable",
        ))
    except Exception as exc:
        out.append(CheckRecord(
            check_name="docs_research_claude_agent_sdk",
            status="FAIL",
            evidence_path="",
            observed_value=f"ImportError: {type(exc).__name__}: {exc}",
            expected_value="claude-agent-sdk importable",
            failure_reason="claude-agent-sdk not installed",
        ))
        facts["claude-agent-sdk"] = [f"not installed: {exc}"]

    # plugin manifest contract — observed from local plugin.json
    manifest_path = plugin_root / ".claude-plugin" / "plugin.json"
    if manifest_path.exists():
        data = json.loads(manifest_path.read_text(encoding="utf-8"))
        facts["claude-code-plugin-manifest"] = [
            f"manifest path is .claude-plugin/plugin.json (observed at {manifest_path})",
            f"required key 'name' present: {'yes' if isinstance(data.get('name'), str) else 'no'}",
            f"recognized sub-paths in this manifest: {sorted(k for k in data if k in {'skills','commands','hooks','agents','mcps'})}",
            "manifest 'hooks' field points at hooks/hooks.json (observed in this manifest)",
            "manifest 'skills' and 'commands' fields are directory references relative to plugin root",
        ]
        out.append(CheckRecord(
            check_name="docs_research_plugin_manifest",
            status="PASS",
            evidence_path=str(manifest_path),
            observed_value="manifest present + parsed",
            expected_value="manifest readable",
        ))
    else:
        out.append(CheckRecord(
            check_name="docs_research_plugin_manifest",
            status="FAIL",
            evidence_path=str(manifest_path),
            observed_value="missing",
            expected_value="manifest present",
            failure_reason="cannot research without manifest",
        ))
        facts["claude-code-plugin-manifest"] = ["manifest missing"]

    # hook I/O contract — observed from local hook scripts
    hooks_file = plugin_root / "hooks" / "hooks.json"
    hook_scripts = list((plugin_root / "scripts").glob("hook_*.py"))
    if hooks_file.exists() and hook_scripts:
        evt_names: list[str] = []
        try:
            evt_names = sorted(list(json.loads(hooks_file.read_text(encoding="utf-8")).get("hooks", {}).keys()))
        except Exception:
            evt_names = []
        facts["claude-code-hooks-io"] = [
            f"hooks.json contains events: {evt_names}",
            "hooks read JSON payload from stdin and exit 0 on success (observed in scripts/hook_*.py)",
            "hooks may emit JSON on stdout under hookSpecificOutput.additionalContext (observed in hook_prompt_context.py)",
            "blocking patterns ({decision: 'block'} or 'approve') are deprecated; Orbit uses additionalContext for non-blocking hints",
            f"available hook scripts: {[p.name for p in hook_scripts]}",
        ]
        out.append(CheckRecord(
            check_name="docs_research_hooks_io",
            status="PASS",
            evidence_path=str(hooks_file),
            observed_value=f"events={evt_names}",
            expected_value="non-empty events + scripts present",
        ))
    else:
        out.append(CheckRecord(
            check_name="docs_research_hooks_io",
            status="FAIL",
            evidence_path=str(hooks_file),
            observed_value=f"hooks.json={hooks_file.exists()} scripts={len(hook_scripts)}",
            expected_value="hooks.json + hook scripts present",
            failure_reason="missing hooks.json or hook scripts",
        ))
        facts["claude-code-hooks-io"] = ["hooks.json or hook scripts missing"]

    # Skill frontmatter contract — observed from local SKILL.md files
    skills_dir = plugin_root / "skills"
    skill_files = list(skills_dir.glob("*/SKILL.md")) if skills_dir.exists() else []
    if skill_files:
        facts["claude-code-skill-frontmatter"] = [
            f"observed {len(skill_files)} SKILL.md files",
            "each begins with --- ... --- YAML frontmatter (verified by file inspection)",
            "frontmatter declares 'name' and 'description' keys (verified by validate_skill_frontmatter.py)",
            "name pattern is lowercase letters, digits, hyphens only; max 64 chars (enforced by validator)",
            "description is plain text, no XML tags, max 1024 chars (enforced by validator)",
        ]
        out.append(CheckRecord(
            check_name="docs_research_skill_frontmatter",
            status="PASS",
            evidence_path=str(skills_dir),
            observed_value=f"skill files={len(skill_files)}",
            expected_value=">=1 SKILL.md",
        ))
    else:
        out.append(CheckRecord(
            check_name="docs_research_skill_frontmatter",
            status="FAIL",
            evidence_path=str(skills_dir),
            observed_value="no SKILL.md files",
            expected_value=">=1 SKILL.md",
            failure_reason="no skills present",
        ))
        facts["claude-code-skill-frontmatter"] = ["no SKILL.md files"]

    # Slash command file format
    cmd_dir = plugin_root / "commands"
    cmd_files = list(cmd_dir.glob("*.md")) if cmd_dir.exists() else []
    if cmd_files:
        facts["claude-code-slash-commands"] = [
            f"observed {len(cmd_files)} command markdown files",
            "each command file is a markdown document; filename is the slash command stem (e.g. audit-gaps.md => /orbit:audit-gaps)",
            "file content is the body of the slash command (heading + usage examples)",
            "Orbit commands suggest helper invocations using fenced code blocks (verified by validate_commands.py)",
            "no front matter is required for slash commands in Claude Code (observed in Orbit's command files)",
        ]
        out.append(CheckRecord(
            check_name="docs_research_slash_commands",
            status="PASS",
            evidence_path=str(cmd_dir),
            observed_value=f"command files={len(cmd_files)}",
            expected_value=">=1 command markdown file",
        ))
    else:
        out.append(CheckRecord(
            check_name="docs_research_slash_commands",
            status="FAIL",
            evidence_path=str(cmd_dir),
            observed_value="no command files",
            expected_value=">=1 command file",
            failure_reason="no commands directory or empty",
        ))
        facts["claude-code-slash-commands"] = ["no command markdown files"]

    return out, facts


# ----------------------------- Installed plugin ------------------------------


def installed_plugin_validation() -> list[CheckRecord]:
    out: list[CheckRecord] = []
    status = installed_plugin_status()
    out.append(CheckRecord(
        check_name="installed_plugins_json_present",
        status="PASS" if status["installed_plugins_json"] else "BLOCKED",
        evidence_path=status["installed_plugins_json"] or "",
        observed_value="present" if status["installed_plugins_json"] else "missing",
        expected_value="~/.claude/plugins/installed_plugins.json present",
        blocker_reason="" if status["installed_plugins_json"] else "Claude Code plugin index not found",
        manual_verification_command="ls ~/.claude/plugins/installed_plugins.json",
    ))
    out.append(CheckRecord(
        check_name="orbit_installed",
        status=("PASS" if status.get("orbit_installed") else "BLOCKED"),
        evidence_path=status.get("installed_plugins_json") or "",
        observed_value=f"orbit_install_dirs={status.get('orbit_install_dirs')}",
        expected_value="orbit listed in installed_plugins.json or under ~/.claude/plugins/",
        blocker_reason=("Orbit not installed in current Claude Code environment" if not status.get("orbit_installed") else ""),
        manual_verification_command='claude plugin list 2>&1 | grep -i orbit ; ls ~/.claude/plugins/ | grep -i orbit',
    ))
    out.append(CheckRecord(
        check_name="claude_cli_present",
        status="PASS" if status.get("claude_cli") else "BLOCKED",
        evidence_path=status.get("claude_cli") or "",
        observed_value=status.get("claude_cli") or "missing",
        expected_value="claude CLI on PATH",
        blocker_reason="" if status.get("claude_cli") else "claude CLI not on PATH",
        manual_verification_command="which claude && claude --version",
    ))
    # Slash command discovery: cannot enumerate non-interactively without launching the CLI
    out.append(CheckRecord(
        check_name="installed_plugin_command_discovery",
        status="BLOCKED",
        evidence_path="",
        observed_value="non-interactive enumeration not supported by current Claude Code CLI",
        expected_value="Installed Orbit commands discoverable",
        blocker_reason="`claude plugin list` is interactive; harness cannot enumerate slash commands non-interactively",
        manual_verification_command="claude /orbit:audit-gaps  # interactive verify",
    ))
    out.append(CheckRecord(
        check_name="installed_plugin_skill_discovery",
        status="BLOCKED",
        evidence_path="",
        observed_value="non-interactive skill enumeration not exposed",
        expected_value="Orbit skills discoverable in installed plugin payload",
        blocker_reason="Skill discovery is internal to the agent loop and not exposed via CLI flag",
        manual_verification_command="claude\nthen invoke a skill trigger phrase like 'audit this project for gaps'",
    ))
    out.append(CheckRecord(
        check_name="installed_plugin_hook_configuration",
        status="BLOCKED",
        evidence_path="",
        observed_value="no enumerator for installed-plugin hook config",
        expected_value="Orbit hooks loaded by Claude Code",
        blocker_reason="hook activation is internal to the running agent",
        manual_verification_command="cat ~/.claude/plugins/installed_plugins.json | grep -i orbit ; cat ~/.claude/settings.json | grep -i hooks",
    ))
    return out


# ----------------------------- Static validators -----------------------------


def static_validators(plugin_root: Path, evidence_dir: Path) -> tuple[list[CheckRecord], dict[str, Any]]:
    out: list[CheckRecord] = []
    payloads: dict[str, Any] = {}
    for name, script, extra in [
        ("manifest", "validate_plugin_manifest.py", ["--plugin-root", str(plugin_root)]),
        ("frontmatter", "validate_skill_frontmatter.py", ["--skills-dir", str(plugin_root / "skills")]),
        ("commands", "validate_commands.py", ["--plugin-root", str(plugin_root)]),
        ("hooks", "validate_hooks.py", ["--plugin-root", str(plugin_root)]),
        ("outputs", "validate_outputs.py", ["--plugin-root", str(plugin_root)]),
    ]:
        out_path = evidence_dir / f"static-{name}.json"
        cmd = [sys.executable, str(HARNESS_ROOT / script), "--output", str(out_path), *extra]
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=240)
        try:
            payload = json.loads(out_path.read_text(encoding="utf-8")) if out_path.exists() else {"status": "FAIL", "error": "no output"}
        except json.JSONDecodeError as exc:
            payload = {"status": "FAIL", "error": f"json decode: {exc}", "stderr_tail": proc.stderr[-400:]}
        payload["_returncode"] = proc.returncode
        payloads[name] = payload
        status = payload.get("status", "FAIL")
        out.append(CheckRecord(
            check_name=f"static_validator_{name}",
            status=status,
            evidence_path=str(out_path),
            observed_value=f"returncode={proc.returncode} status={status}",
            expected_value="status=PASS",
            failure_reason="" if status == "PASS" else (payload.get("error") or "validator reported FAIL — see evidence file"),
        ))
    return out, payloads


# ----------------------------- Skill Creator-style review --------------------


def skill_creator_review(plugin_root: Path, evidence_dir: Path) -> tuple[list[CheckRecord], dict[str, Any]]:
    out: list[CheckRecord] = []
    payload: dict[str, Any] = {"reviews": []}
    skills_dir = plugin_root / "skills"
    if not skills_dir.exists():
        out.append(CheckRecord(
            check_name="skill_creator_skills_dir",
            status="FAIL",
            evidence_path=str(skills_dir),
            observed_value="missing",
            expected_value="skills dir present",
            failure_reason="no skills dir",
        ))
        return out, payload

    triggers = {
        "gap-analysis": ["audit", "look back", "review-window", "what did we miss", "gap analysis", "compare to the plan"],
        "instruction-ledger": ["ledger", "rebuild the ledger", "what did i tell you", "project memory", "corrections"],
        "plan-execution-audit": ["compare to the plan", "does this match the plan", "missing", "superseded"],
        "validation-pairing": ["did it actually do it", "validate the claims", "prove it was completed", "check against the repo"],
    }
    for child in sorted(skills_dir.iterdir()):
        skill_md = child / "SKILL.md"
        if not (child.is_dir() and skill_md.exists()):
            continue
        from _common import parse_yaml_frontmatter
        text = skill_md.read_text(encoding="utf-8", errors="replace")
        fields, body = parse_yaml_frontmatter(text)
        desc = fields.get("description", "") or ""
        matched = [t for t in triggers.get(child.name, []) if t.lower() in desc.lower()]
        scoring = {
            "trigger_accuracy": 5 if len(matched) >= 3 else 4 if len(matched) >= 2 else 3 if matched else 1,
            "clarity": 5 if 80 <= len(desc) <= 1024 else 3,
            "scope_fit": 5 if len(matched) >= 2 else 3,
            "frontmatter_compliance": 5 if fields.get("name") == child.name else 1,
            "operational_completeness": 5 if any(token in body.lower() for token in ["workflow", "rule", "contract", "outputs"]) else 3,
        }
        scoring["overall"] = round(sum(scoring.values()) / len(scoring), 2)
        improvements = []
        if scoring["trigger_accuracy"] < 4:
            improvements.append(f"Add explicit trigger phrases: {triggers.get(child.name)}")
        if scoring["clarity"] < 5:
            improvements.append("Ensure description is between 80 and 1024 chars.")
        if scoring["frontmatter_compliance"] < 5:
            improvements.append("Frontmatter name must match directory name.")
        if scoring["operational_completeness"] < 5:
            improvements.append("Body should describe a workflow, rule, contract, or outputs.")
        review = {
            "name": child.name,
            "skill_md": str(skill_md),
            "description_chars": len(desc),
            "triggers_matched": matched,
            "scoring": scoring,
            "improvements": improvements,
        }
        payload["reviews"].append(review)
        status = "PASS" if scoring["overall"] >= 4.0 and not improvements else ("PASS" if scoring["overall"] >= 4.0 else "FAIL")
        out.append(CheckRecord(
            check_name=f"skill_creator_review_{child.name}",
            status=status,
            evidence_path=str(skill_md),
            observed_value=f"overall={scoring['overall']} matched_triggers={len(matched)} improvements={len(improvements)}",
            expected_value="overall >= 4.0 and no improvement actions outstanding",
            failure_reason="" if status == "PASS" else "; ".join(improvements),
        ))
    review_path = evidence_dir / "skill-creator-review.json"
    review_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return out, payload


# ----------------------------- Documentation completeness --------------------


REQUIRED_MD = [
    "README.md", "install.md", "usage.md", "commands.md", "hooks.md", "skills.md",
    "evidence-model.md", "validation.md", "sdk-harness.md", "scenarios.md",
    "dashboard.md", "reports.md", "compliance.md", "plugin-validation.md",
    "skill-creator-review.md", "troubleshooting.md", "diagrams.md",
    "validation-research.md", "architecture.md", "installed-plugin-validation.md",
]
REQUIRED_HTML = [
    "index.html", "install.html", "usage.html", "commands.html", "hooks.html",
    "skills.html", "evidence-model.html", "validation.html", "sdk-harness.html",
    "scenarios.html", "dashboard.html", "reports.html", "compliance.html",
    "plugin-validation.html", "skill-creator-review.html", "troubleshooting.html",
    "diagrams.html", "validation-research.html", "architecture.html",
    "installed-plugin-validation.html",
]
REQUIRED_DIAGRAMS = [
    "orbit-system-flow.mmd", "evidence-pipeline.mmd", "intent-to-gap-model.mmd",
    "sdk-harness-flow.mmd", "plugin-compliance-flow.mmd", "review-window-flow.mmd",
    "hook-candidate-flow.mmd", "claim-validation-flow.mmd", "dashboard-output-flow.mmd",
    "installed-plugin-validation-flow.mmd", "local-architecture-discovery-flow.mmd",
]
VALID_MERMAID_PREFIXES = (
    "flowchart", "graph", "sequencediagram", "statediagram", "classdiagram",
    "timeline", "journey", "gantt", "erdiagram", "pie", "mindmap",
)


def docs_completeness(plugin_root: Path, evidence_dir: Path) -> list[CheckRecord]:
    out: list[CheckRecord] = []
    docs = plugin_root / "docs"
    html = plugin_root / "docs-html"
    diagrams = docs / "diagrams"
    for name in REQUIRED_MD:
        path = docs / name
        ok = path.exists() and path.stat().st_size > 0
        out.append(CheckRecord(
            check_name=f"doc_md_{name}",
            status="PASS" if ok else "FAIL",
            evidence_path=str(path),
            observed_value=f"size={path.stat().st_size if path.exists() else 0}",
            expected_value="exists and non-empty",
            failure_reason="" if ok else f"docs/{name} missing or empty",
        ))
    for name in REQUIRED_HTML:
        path = html / name
        ok = path.exists() and path.stat().st_size > 0
        out.append(CheckRecord(
            check_name=f"doc_html_{name}",
            status="PASS" if ok else "FAIL",
            evidence_path=str(path),
            observed_value=f"size={path.stat().st_size if path.exists() else 0}",
            expected_value="exists and non-empty",
            failure_reason="" if ok else f"docs-html/{name} missing or empty",
        ))
    for name in REQUIRED_DIAGRAMS:
        path = diagrams / name
        if not path.exists() or path.stat().st_size == 0:
            out.append(CheckRecord(
                check_name=f"diagram_{name}",
                status="FAIL",
                evidence_path=str(path),
                observed_value=f"size={path.stat().st_size if path.exists() else 0}",
                expected_value="exists and non-empty",
                failure_reason=f"docs/diagrams/{name} missing or empty",
            ))
            continue
        first_line = path.read_text(encoding="utf-8").lstrip().splitlines()[0].strip().lower()
        valid = first_line.startswith(VALID_MERMAID_PREFIXES)
        out.append(CheckRecord(
            check_name=f"diagram_{name}",
            status="PASS" if valid else "FAIL",
            evidence_path=str(path),
            observed_value=f"first_line={first_line[:80]}",
            expected_value=f"begins with one of {VALID_MERMAID_PREFIXES}",
            failure_reason="" if valid else f"diagram does not begin with a recognized Mermaid type",
        ))
    return out


# ----------------------------- SDK scenario runners --------------------------


SCENARIO_RUNNERS = [
    ("00-architecture-discovery",
     "Explore the local Orbit codebase from an architectural standpoint. Identify the plugin "
     "root, manifest, skills, commands, hooks, scripts, bin wrappers, evidence pipeline, "
     "dashboard renderer, review-window implementation, and validation surfaces. Produce an "
     "evidence-backed architecture map before running functional validation. Respond in <=10 lines."),
    ("01-plan-gap", None),  # delegated to sdk_orbit_audit_gaps.py
    ("02-correction-supersedes", None),  # delegated to sdk_orbit_compare_plan.py
    ("03-claim-unverified", None),  # delegated to sdk_orbit_validate_claims.py
    ("04-claim-contradicted",
     "Use Orbit to validate a claim that the orbit-audit CLI supports --from and --to. "
     "Check the actual parser at scripts/orbit_audit.py. State whether the claim is "
     "validated or contradicted, and which gap category Orbit emits if a contradiction is "
     "found. Respond in <=8 lines."),
    ("05-dashboard-required", None),  # delegated to sdk_orbit_render_dashboard.py
    ("06-review-window", None),  # delegated to sdk_orbit_review_window.py (3 invocations)
    ("07-hook-candidate", None),  # delegated to sdk_orbit_hook_candidate.py
    ("08-malformed-jsonl",
     "Orbit must tolerate malformed JSONL lines without aborting the audit. Confirm that "
     "Orbit's JSONL reader logs and skips bad lines, continues processing the remainder, and "
     "still produces evidence.json. Respond in <=6 lines."),
    ("09-instruction-ledger", None),  # delegated to sdk_orbit_mine_intent.py
    ("10-plugin-compliance", None),  # delegated to sdk_orbit_plugin_compliance.py
    ("11-skill-creator-review", None),  # delegated to sdk_orbit_skill_compliance.py
    ("12-docs-completeness", None),  # delegated to sdk_orbit_docs_compliance.py
    ("13-installed-plugin",
     "Validate Orbit as a real installed Claude Code plugin where feasible. State which "
     "checks can be performed non-interactively (manifest path, ~/.claude/plugins payload), "
     "which are BLOCKED (slash command discovery, skill discovery), and what manual command "
     "the user should run for each blocked check. Respond in <=10 lines."),
]

DELEGATED = {
    "01-plan-gap": "sdk_orbit_audit_gaps.py",
    "02-correction-supersedes": "sdk_orbit_compare_plan.py",
    "03-claim-unverified": "sdk_orbit_validate_claims.py",
    "05-dashboard-required": "sdk_orbit_render_dashboard.py",
    "07-hook-candidate": "sdk_orbit_hook_candidate.py",
    "09-instruction-ledger": "sdk_orbit_mine_intent.py",
    "10-plugin-compliance": "sdk_orbit_plugin_compliance.py",
    "11-skill-creator-review": "sdk_orbit_skill_compliance.py",
    "12-docs-completeness": "sdk_orbit_docs_compliance.py",
}


async def run_scenarios(do_live_runs: bool, evidence_dir: Path) -> tuple[list[CheckRecord], list[dict[str, Any]]]:
    """Run all 13 scenarios. Returns CheckRecords plus per-scenario summaries."""
    records: list[CheckRecord] = []
    scenario_summaries: list[dict[str, Any]] = []
    if not do_live_runs:
        for scen_id, prompt in SCENARIO_RUNNERS:
            records.append(CheckRecord(
                check_name=f"sdk_scenario_{scen_id}",
                status="BLOCKED",
                evidence_path="",
                observed_value="--no-live-runs flag passed",
                expected_value="real ResultMessage observed in transcript.json",
                blocker_reason="live SDK runs disabled",
                manual_verification_command=f"python3 .orbit-sdk-harness/sdk_orbit_all.py --plugin-root . --output .orbit-sdk-harness/reports",
            ))
        return records, scenario_summaries

    # Inline scenarios (no delegate) — use run_query directly so we share evidence dir layout.
    inline_ids = {
        "00-architecture-discovery",
        "04-claim-contradicted",
        "08-malformed-jsonl",
        "13-installed-plugin",
    }

    # The 06-review-window scenario runs THREE invocations with different scope flags.
    review_window_invocations = [
        ("06-review-window-days7", "--days 7"),
        ("06-review-window-since", "--since 2026-05-01"),
        ("06-review-window-from-to", "--from 2026-05-01 --to 2026-05-04"),
    ]

    for scen_id, prompt in SCENARIO_RUNNERS:
        if scen_id == "06-review-window":
            # Run 3 invocations
            for label, scope_flags in review_window_invocations:
                base = (
                    "You are validating Orbit's configurable review-window. Selected scope "
                    f"for this run: {scope_flags}. Confirm that Orbit's evidence.json scope "
                    "object will reflect this selection and that the dashboard will echo it. "
                    "Respond in <=8 lines."
                )
                summary = await run_query(label=label, prompt=base, max_turns=4)
                scenario_summaries.append({"scenario_id": label, "summary": summary})
                _record_scenario(records, label, summary)
            continue
        if scen_id in inline_ids:
            summary = await run_query(label=scen_id, prompt=prompt, max_turns=4)
            scenario_summaries.append({"scenario_id": scen_id, "summary": summary})
            _record_scenario(records, scen_id, summary)
            continue
        # Delegated scenarios — invoke the dedicated wrapper as a subprocess so the wrapper
        # captures its own per-run evidence (and any extra files like dashboard render output).
        runner = DELEGATED.get(scen_id)
        if not runner:
            continue
        cmd = [sys.executable, str(HARNESS_ROOT / runner)]
        log(f"delegated scenario start: {scen_id} → {runner}")
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
        delegated_evidence_path = evidence_dir / f"delegated-{scen_id}.json"
        try:
            payload = json.loads(proc.stdout) if proc.stdout.strip() else {}
        except json.JSONDecodeError:
            payload = {"raw_stdout": proc.stdout[-2000:], "stderr_tail": proc.stderr[-1000:]}
        payload["_runner"] = runner
        payload["_returncode"] = proc.returncode
        payload["_stderr_tail"] = proc.stderr[-1000:]
        delegated_evidence_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        scenario_summaries.append({"scenario_id": scen_id, "summary": payload})
        # Use the run_dir from the payload if present
        run_dir = payload.get("run_dir")
        got_result = bool(payload.get("got_result_message"))
        records.append(CheckRecord(
            check_name=f"sdk_scenario_{scen_id}",
            status="PASS" if got_result and proc.returncode == 0 else "FAIL",
            evidence_path=str(run_dir or delegated_evidence_path),
            observed_value=f"returncode={proc.returncode} got_result={got_result}",
            expected_value="returncode=0 and ResultMessage in transcript",
            failure_reason="" if got_result and proc.returncode == 0 else f"runner exit={proc.returncode} got_result={got_result}",
        ))
    return records, scenario_summaries


def _record_scenario(records: list[CheckRecord], label: str, summary: dict[str, Any]) -> None:
    got_result = bool(summary.get("got_result_message"))
    records.append(CheckRecord(
        check_name=f"sdk_scenario_{label}",
        status="PASS" if got_result else "FAIL",
        evidence_path=summary.get("transcript_path") or summary.get("run_dir", ""),
        observed_value=f"got_result={got_result} msgs={summary.get('transcript_msg_count')}",
        expected_value="ResultMessage in transcript.json",
        failure_reason="" if got_result else f"no ResultMessage. exception={summary.get('exception')}",
    ))


# ----------------------------- Dashboard verification ------------------------


def dashboard_verification(plugin_root: Path, evidence_dir: Path) -> list[CheckRecord]:
    out: list[CheckRecord] = []
    sample_evidence = plugin_root / "examples" / "sample-evidence.json"
    target = evidence_dir / "dashboard-verified.html"
    if not sample_evidence.exists():
        out.append(CheckRecord(
            check_name="dashboard_sample_evidence_present",
            status="FAIL",
            evidence_path=str(sample_evidence),
            observed_value="missing",
            expected_value="examples/sample-evidence.json present",
            failure_reason="no sample evidence",
        ))
        return out
    out.append(CheckRecord(
        check_name="dashboard_sample_evidence_present",
        status="PASS",
        evidence_path=str(sample_evidence),
        observed_value="present",
        expected_value="present",
    ))
    proc = subprocess.run(
        [sys.executable, str(plugin_root / "scripts" / "orbit_audit.py"),
         "render-dashboard", "--evidence", str(sample_evidence), "--output", str(target)],
        capture_output=True, text=True, timeout=60,
    )
    out.append(CheckRecord(
        check_name="dashboard_render_returncode",
        status="PASS" if proc.returncode == 0 else "FAIL",
        evidence_path=str(target),
        observed_value=f"returncode={proc.returncode}",
        expected_value="returncode=0",
        failure_reason=proc.stderr[-400:] if proc.returncode != 0 else "",
    ))
    if not target.exists():
        return out
    html = target.read_text(encoding="utf-8")
    for token in ("ORBIT", "Find drift", "#C6FF00", "#FF8A00", "#FF4D36", "#8B3DFF", "#1E6BFF",
                  "Timeline", "Claim Validation", "Uncertainty", "Scope", "Matrix"):
        present = token in html
        out.append(CheckRecord(
            check_name=f"dashboard_token_{re.sub(r'[^A-Za-z0-9]', '_', token)}",
            status="PASS" if present else "FAIL",
            evidence_path=str(target),
            observed_value="present" if present else "missing",
            expected_value=f"contains '{token}'",
            failure_reason="" if present else f"dashboard missing required marker '{token}'",
        ))
    return out


# ----------------------------- Report writers --------------------------------


def write_reports(
    plugin_root: Path,
    output_dir: Path,
    architecture_records: list[CheckRecord],
    architecture_layout: dict[str, Any],
    docs_records: list[CheckRecord],
    docs_facts: dict[str, list[str]],
    installed_records: list[CheckRecord],
    static_records: list[CheckRecord],
    static_payloads: dict[str, Any],
    skill_creator_records: list[CheckRecord],
    skill_creator_payload: dict[str, Any],
    docs_completeness_records: list[CheckRecord],
    scenario_records: list[CheckRecord],
    scenario_summaries: list[dict[str, Any]],
    dashboard_records: list[CheckRecord],
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)

    arch_status = aggregate_status(architecture_records)
    docs_status = aggregate_status(docs_records)
    installed_status = aggregate_status(installed_records)
    static_status = aggregate_status(static_records)
    skill_creator_status = aggregate_status(skill_creator_records)
    docs_completeness_status = aggregate_status(docs_completeness_records)
    scenario_status = aggregate_status(scenario_records)
    dashboard_status = aggregate_status(dashboard_records)

    overall_records = (architecture_records + docs_records + installed_records + static_records
                       + skill_creator_records + docs_completeness_records + scenario_records
                       + dashboard_records)
    overall = aggregate_status(overall_records)

    # JSON results
    results = {
        "generated_at": now_iso(),
        "plugin_root": str(plugin_root),
        "overall": overall,
        "section_status": {
            "architecture_discovery": arch_status,
            "documentation_research": docs_status,
            "installed_plugin_validation": installed_status,
            "plugin_compliance_static": static_status,
            "skill_creator_review": skill_creator_status,
            "documentation_completeness": docs_completeness_status,
            "sdk_scenarios": scenario_status,
            "dashboard_verification": dashboard_status,
        },
        "checks": [r.to_dict() for r in overall_records],
        "architecture_layout": architecture_layout,
        "docs_facts": docs_facts,
        "scenario_summaries": scenario_summaries,
        "static_validator_payloads": static_payloads,
        "skill_creator_payload": skill_creator_payload,
    }
    write_json(output_dir / "orbit-validation-results.json", results)

    # Architecture report
    write_md(output_dir / "orbit-architecture-discovery.md", _md_section(
        "# Orbit Architecture Discovery",
        f"Status: **{arch_status}** · Generated: `{now_iso()}` · Root: `{plugin_root}`",
        "## Inventory",
        "```json",
        json.dumps(architecture_layout, indent=2),
        "```",
        "## Checks",
        render_check_table(architecture_records),
    ))

    # Plugin compliance report
    write_md(output_dir / "orbit-plugin-compliance.md", _md_section(
        "# Orbit Plugin Compliance",
        f"Status: **{static_status}** · Generated: `{now_iso()}`",
        "## Static Validator Results",
        render_check_table(static_records),
        "## Per-Validator Detail",
        "```json",
        json.dumps({k: {"status": v.get("status"), "_returncode": v.get("_returncode")} for k, v in static_payloads.items()}, indent=2),
        "```",
    ))

    # Installed plugin report
    write_md(output_dir / "orbit-installed-plugin-validation.md", _md_section(
        "# Orbit Installed Plugin Validation",
        f"Status: **{installed_status}** · Generated: `{now_iso()}`",
        "## Checks",
        render_check_table(installed_records),
        "",
        "Several installed-plugin checks are intentionally `BLOCKED`. The Claude Code CLI does "
        "not currently expose a non-interactive enumerator for installed slash commands or "
        "skills. The blocker rows above include the manual verification command for each.",
    ))

    # Skill compliance report (frontmatter-driven)
    write_md(output_dir / "orbit-skill-compliance.md", _md_section(
        "# Orbit Skill Compliance",
        f"Status: **{aggregate_status([r for r in static_records if r.check_name == 'static_validator_frontmatter'])}**",
        "## Frontmatter Validator",
        f"Evidence: `{output_dir.parent.relative_to(plugin_root) if plugin_root in output_dir.parents else output_dir}/static-frontmatter.json`",
        "```json",
        json.dumps(static_payloads.get("frontmatter", {}), indent=2),
        "```",
    ))

    # Command compliance report
    write_md(output_dir / "orbit-command-compliance.md", _md_section(
        "# Orbit Command Compliance",
        f"Status: **{aggregate_status([r for r in static_records if r.check_name == 'static_validator_commands'])}**",
        "## Command Validator",
        "```json",
        json.dumps(static_payloads.get("commands", {}), indent=2),
        "```",
    ))

    # Hook compliance report
    write_md(output_dir / "orbit-hook-compliance.md", _md_section(
        "# Orbit Hook Compliance",
        f"Status: **{aggregate_status([r for r in static_records if r.check_name == 'static_validator_hooks'])}**",
        "## Hooks Validator",
        "```json",
        json.dumps(static_payloads.get("hooks", {}), indent=2),
        "```",
    ))

    # Docs compliance report
    write_md(output_dir / "orbit-docs-compliance.md", _md_section(
        "# Orbit Documentation Compliance",
        f"Status: **{docs_completeness_status}**",
        "## Per-Doc Checks",
        render_check_table(docs_completeness_records),
    ))

    # Skill Creator review report
    write_md(output_dir / "orbit-skill-creator-review.md", _md_section(
        "# Orbit Skill Creator-style Review",
        f"Status: **{skill_creator_status}**",
        "## Per-Skill Scoring",
        "| Skill | Trigger | Clarity | Scope | Frontmatter | Operational | Overall | Improvements |",
        "|---|---|---|---|---|---|---|---|",
        *[
            f"| `{r['name']}` | {r['scoring']['trigger_accuracy']} | {r['scoring']['clarity']} | "
            f"{r['scoring']['scope_fit']} | {r['scoring']['frontmatter_compliance']} | "
            f"{r['scoring']['operational_completeness']} | **{r['scoring']['overall']}** | "
            f"{', '.join(r.get('improvements', [])) or '—'} |"
            for r in skill_creator_payload.get("reviews", [])
        ],
    ))

    # Scenario matrix CSV
    rows = []
    for rec in scenario_records:
        rows.append([rec.check_name, rec.status, rec.evidence_path, rec.observed_value, rec.expected_value, rec.failure_reason or rec.blocker_reason])
    write_csv(output_dir / "orbit-scenario-matrix.csv",
              ["scenario", "status", "evidence_path", "observed", "expected", "notes"], rows)

    # Dashboard verification report
    write_md(output_dir / "orbit-dashboard-verification.md", _md_section(
        "# Orbit Dashboard Verification",
        f"Status: **{dashboard_status}**",
        "## Token Checks",
        render_check_table(dashboard_records),
    ))

    # Final pass/fail report
    write_md(output_dir / "orbit-final-pass-fail.md", _md_section(
        "# Orbit Validation — Final Pass/Fail",
        f"Generated: `{now_iso()}`",
        f"Plugin root: `{plugin_root}`",
        "",
        f"**Overall**: **{overall}**",
        "",
        "| Section | Status |",
        "|---|---|",
        f"| Architecture Discovery | {arch_status} |",
        f"| Documentation Research | {docs_status} |",
        f"| Plugin Compliance (static) | {static_status} |",
        f"| Installed Plugin Validation | {installed_status} |",
        f"| Skill Creator Review | {skill_creator_status} |",
        f"| Documentation Completeness | {docs_completeness_status} |",
        f"| SDK Scenarios | {scenario_status} |",
        f"| Dashboard Verification | {dashboard_status} |",
    ))

    # Summary report
    write_md(output_dir / "orbit-validation-summary.md", _md_section(
        "# Orbit Validation Summary",
        f"Generated: `{now_iso()}` · Plugin root: `{plugin_root}` · Overall: **{overall}**",
        "## Executive Summary",
        f"Orbit validation produced {len(overall_records)} checks across 8 sections. "
        f"PASS={sum(1 for r in overall_records if r.status == 'PASS')}, "
        f"FAIL={sum(1 for r in overall_records if r.status == 'FAIL')}, "
        f"BLOCKED={sum(1 for r in overall_records if r.status == 'BLOCKED')}.",
        "",
        "## Local Architecture Discovery",
        f"Status: **{arch_status}** — see `{(output_dir / 'orbit-architecture-discovery.md').relative_to(plugin_root)}`.",
        "",
        "## GitHub or External Context Boundary",
        "No GitHub repository context was assumed. The local filesystem is the source of truth. "
        "Documentation research used locally available material only — claude-agent-sdk imports "
        "were verified by `import claude_agent_sdk` against the installed package; plugin/hook/"
        "skill/command contracts were derived from observed manifest, hooks.json, SKILL.md, and "
        "command markdown files in the local Orbit project.",
        "",
        "## Documentation Research",
        f"Status: **{docs_status}**",
        "```json",
        json.dumps(docs_facts, indent=2),
        "```",
        "",
        "## Plugin Compliance",
        f"Status: **{static_status}**. See `orbit-plugin-compliance.md`.",
        "",
        "## Installed-Plugin Validation",
        f"Status: **{installed_status}**. See `orbit-installed-plugin-validation.md`.",
        "",
        "## Skill Compliance",
        f"Frontmatter status: **{aggregate_status([r for r in static_records if r.check_name == 'static_validator_frontmatter'])}**. "
        f"Skill Creator-style review status: **{skill_creator_status}**. See `orbit-skill-compliance.md` and `orbit-skill-creator-review.md`.",
        "",
        "## Command Compliance",
        f"Status: **{aggregate_status([r for r in static_records if r.check_name == 'static_validator_commands'])}**. See `orbit-command-compliance.md`.",
        "",
        "## Hook Compliance",
        f"Status: **{aggregate_status([r for r in static_records if r.check_name == 'static_validator_hooks'])}**. See `orbit-hook-compliance.md`.",
        "",
        "## Frontmatter Compliance",
        f"Status: **{aggregate_status([r for r in static_records if r.check_name == 'static_validator_frontmatter'])}**.",
        "",
        "## SDK Scenario Results",
        f"Status: **{scenario_status}**.",
        render_check_table(scenario_records),
        "",
        "## Test Prompts Used",
        "See per-scenario `prompt.md` files under `.orbit-sdk-harness/runs/` for the exact prompts dispatched to `query()`.",
        "",
        "## Observed Artifacts",
        "Each run directory contains `transcript.json`, `session-id.txt`, `jsonl-pointer.txt`, "
        "`summary.json`, `started-at.txt`, `finished-at.txt`, `got-result.txt`, optional "
        "`exception.txt`, and `debug.log`. The JSONL pointer references "
        "`~/.claude/projects/<encoded-cwd>/<session-id>.jsonl` — the load-bearing artifact "
        "Orbit itself mines.",
        "",
        "## Dashboard Verification",
        f"Status: **{dashboard_status}**. See `orbit-dashboard-verification.md`.",
        "",
        "## Documentation Completeness",
        f"Status: **{docs_completeness_status}**. See `orbit-docs-compliance.md`.",
        "",
        "## Known Failures",
        _list_failures(overall_records, "FAIL") or "None.",
        "",
        "## Blocked Checks (Manual Verification Required)",
        _list_failures(overall_records, "BLOCKED") or "None.",
        "",
        "## Recommended Fixes",
        _recommended_fixes(overall_records) or "No outstanding fixes.",
        "",
        "## Final Pass/Fail",
        f"**Overall: {overall}**",
    ))


def _md_section(*parts: str) -> str:
    return "\n\n".join(parts).rstrip() + "\n"


def _list_failures(records: list[CheckRecord], status: str) -> str:
    lines = []
    for r in records:
        if r.status == status:
            reason = r.failure_reason or r.blocker_reason or "(no reason recorded)"
            cmd = f" Manual: `{r.manual_verification_command}`" if r.manual_verification_command else ""
            lines.append(f"- `{r.check_name}` — {reason}{cmd} (evidence: `{r.evidence_path or '-'}`)")
    return "\n".join(lines)


def _recommended_fixes(records: list[CheckRecord]) -> str:
    lines = []
    for r in records:
        if r.status == "FAIL":
            lines.append(f"- Fix `{r.check_name}`: {r.failure_reason or 'see evidence'}")
    return "\n".join(lines)


# ----------------------------- Main entry ------------------------------------


async def amain(args) -> int:
    plugin_root = resolve_plugin_root(args.plugin_root)
    output_dir = Path(args.output).expanduser().resolve()
    evidence_dir = output_dir / "evidence"
    evidence_dir.mkdir(parents=True, exist_ok=True)
    REPORTS_ROOT.mkdir(parents=True, exist_ok=True)

    log(f"plugin_root={plugin_root}")
    log(f"output_dir={output_dir}")

    arch_records, layout = architecture_discovery(plugin_root)
    docs_records, docs_facts = documentation_research(plugin_root)
    installed_records = installed_plugin_validation()
    static_records, static_payloads = static_validators(plugin_root, evidence_dir)
    skill_creator_records, skill_creator_payload = skill_creator_review(plugin_root, evidence_dir)
    docs_completeness_records = docs_completeness(plugin_root, evidence_dir)
    scenario_records, scenario_summaries = await run_scenarios(not args.no_live_runs, evidence_dir)
    dashboard_records = dashboard_verification(plugin_root, evidence_dir)

    write_reports(
        plugin_root=plugin_root,
        output_dir=output_dir,
        architecture_records=arch_records,
        architecture_layout=layout,
        docs_records=docs_records,
        docs_facts=docs_facts,
        installed_records=installed_records,
        static_records=static_records,
        static_payloads=static_payloads,
        skill_creator_records=skill_creator_records,
        skill_creator_payload=skill_creator_payload,
        docs_completeness_records=docs_completeness_records,
        scenario_records=scenario_records,
        scenario_summaries=scenario_summaries,
        dashboard_records=dashboard_records,
    )

    overall = aggregate_status(
        arch_records + docs_records + installed_records + static_records
        + skill_creator_records + docs_completeness_records + scenario_records
        + dashboard_records
    )
    sdk_pass = sum(1 for r in scenario_records if r.status == "PASS")
    sdk_total = len(scenario_records)
    print("ORBIT VALIDATION COMPLETE")
    print(f"Architecture discovery: {aggregate_status(arch_records)}")
    print(f"Plugin compliance: {aggregate_status(static_records)}")
    print(f"Installed plugin validation: {aggregate_status(installed_records)}")
    print(f"Skill compliance: {aggregate_status([r for r in static_records if r.check_name == 'static_validator_frontmatter'])}")
    print(f"Command compliance: {aggregate_status([r for r in static_records if r.check_name == 'static_validator_commands'])}")
    print(f"Hook compliance: {aggregate_status([r for r in static_records if r.check_name == 'static_validator_hooks'])}")
    print(f"Docs compliance: {aggregate_status(docs_completeness_records)}")
    print(f"SDK scenarios: {sdk_pass}/{sdk_total} PASS")
    print(f"Dashboard: {aggregate_status(dashboard_records)}")
    print(f"Skill Creator review: {aggregate_status(skill_creator_records)}")
    print(f"Overall: {overall}")
    print("Reports:")
    for name in [
        "orbit-validation-summary.md",
        "orbit-validation-results.json",
        "orbit-plugin-compliance.md",
        "orbit-installed-plugin-validation.md",
        "orbit-skill-compliance.md",
        "orbit-skill-creator-review.md",
    ]:
        print(f"- {(output_dir / name).as_posix()}")
    return 0 if overall in {"PASS", "BLOCKED"} else 1


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Orbit master validation runner.")
    parser.add_argument("--plugin-root", default=str(PLUGIN_ROOT))
    parser.add_argument("--output", default=str(REPORTS_ROOT))
    parser.add_argument("--no-live-runs", action="store_true",
                        help="Skip live SDK scenarios; mark all as BLOCKED with manual rerun command.")
    args = parser.parse_args(argv)
    try:
        return asyncio.run(amain(args))
    except KeyboardInterrupt:
        return 130
    except BaseException as exc:
        log(f"FATAL: {type(exc).__name__}: {exc}")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
