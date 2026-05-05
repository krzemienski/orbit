#!/usr/bin/env python3
"""Scenario 12 — Documentation Completeness. Real Claude Agent SDK query() + static doc audit."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import main_sync, run_query, PLUGIN_ROOT

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

SDK_PROMPT = (
    "You are validating the Orbit Claude Code plugin documentation suite.\n"
    "\n"
    "Confirm that Orbit ships with markdown docs (install, usage, commands, hooks, skills, "
    "evidence-model, validation, sdk-harness, scenarios, dashboard, reports, compliance, "
    "plugin-validation, skill-creator-review, troubleshooting, diagrams, "
    "validation-research, architecture, installed-plugin-validation), HTML drafts of each, "
    "and Mermaid diagrams covering the system flow, evidence pipeline, intent-to-gap model, "
    "harness flow, compliance flow, review window, hook candidate, claim validation, "
    "dashboard output, installed-plugin validation, and local-architecture discovery.\n"
    "\n"
    "Respond in <= 8 lines."
)


async def amain():
    summary = await run_query(label="12-docs-completeness", prompt=SDK_PROMPT, max_turns=4)
    run_dir = Path(summary["run_dir"])
    docs_dir = PLUGIN_ROOT / "docs"
    html_dir = PLUGIN_ROOT / "docs-html"
    diagrams_dir = docs_dir / "diagrams"
    md_status = {n: (docs_dir / n).exists() and (docs_dir / n).stat().st_size > 0 for n in REQUIRED_MD}
    html_status = {n: (html_dir / n).exists() and (html_dir / n).stat().st_size > 0 for n in REQUIRED_HTML}
    diagram_status = {}
    for n in REQUIRED_DIAGRAMS:
        path = diagrams_dir / n
        ok = False
        if path.exists() and path.stat().st_size > 0:
            first_line = path.read_text(encoding="utf-8").splitlines()[0].strip().lower() if path.read_text(encoding="utf-8").strip() else ""
            ok = first_line.startswith(("flowchart", "graph", "sequencediagram", "statediagram", "classdiagram", "timeline", "journey", "gantt", "erdiagram", "pie", "mindmap"))
        diagram_status[n] = ok
    payload = {
        "docs_dir": str(docs_dir),
        "html_dir": str(html_dir),
        "diagrams_dir": str(diagrams_dir),
        "md": md_status,
        "html": html_status,
        "diagrams": diagram_status,
        "md_missing": [k for k, v in md_status.items() if not v],
        "html_missing": [k for k, v in html_status.items() if not v],
        "diagram_missing_or_invalid": [k for k, v in diagram_status.items() if not v],
    }
    payload["all_present"] = (
        not payload["md_missing"]
        and not payload["html_missing"]
        and not payload["diagram_missing_or_invalid"]
    )
    (run_dir / "docs-audit.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")
    summary["docs_all_present"] = payload["all_present"]
    summary["docs_md_missing"] = payload["md_missing"]
    summary["docs_html_missing"] = payload["html_missing"]
    summary["docs_diagrams_missing"] = payload["diagram_missing_or_invalid"]
    return summary


if __name__ == "__main__":
    raise SystemExit(main_sync(amain))
