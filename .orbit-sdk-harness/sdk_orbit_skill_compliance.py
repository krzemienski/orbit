#!/usr/bin/env python3
"""Scenario 11 — Skill Creator-style Review.

Runs the frontmatter validator, then does a Skill Creator-style review of every
Orbit skill (trigger specificity, body clarity, overtrigger/undertrigger risk).
The SDK query() asks the agent to confirm the review criteria.
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import main_sync, run_query, PLUGIN_ROOT, HARNESS_ROOT, parse_yaml_frontmatter

SDK_PROMPT = (
    "You are reviewing Orbit's skills as if using Claude Code's Skill Creator.\n"
    "\n"
    "Each Orbit skill (gap-analysis, instruction-ledger, plan-execution-audit, "
    "validation-pairing) must have specific trigger phrases in its description, no XML "
    "tags, and a body describing the operational workflow. Confirm what a Skill Creator "
    "review checks for and how Orbit's skills score on trigger specificity.\n"
    "\n"
    "Respond in <= 10 lines."
)

TRIGGER_HINTS = {
    "gap-analysis": ["audit", "look back", "review-window", "what did we miss", "gap analysis", "compare to the plan"],
    "instruction-ledger": ["ledger", "rebuild the ledger", "what did i tell you", "project memory", "corrections"],
    "plan-execution-audit": ["compare to the plan", "does this match the plan", "missing", "superseded"],
    "validation-pairing": ["did it actually do it", "validate the claims", "prove it was completed", "check against the repo"],
}


def review_skill(name: str, skill_md: Path) -> dict:
    text = skill_md.read_text(encoding="utf-8", errors="replace")
    fields, body = parse_yaml_frontmatter(text)
    desc = fields.get("description", "") or ""
    triggers = [t for t in TRIGGER_HINTS.get(name, []) if t.lower() in desc.lower()]
    score = {
        "trigger_accuracy": 5 if len(triggers) >= 3 else 4 if len(triggers) >= 2 else 3 if triggers else 1,
        "clarity": 5 if 80 <= len(desc) <= 1024 else 3,
        "scope_fit": 5 if name in TRIGGER_HINTS and len(triggers) >= 2 else 3,
        "frontmatter_compliance": 5 if fields.get("name") == name else 1,
        "operational_completeness": 5 if "workflow" in body.lower() or "rule" in body.lower() else 3,
        "overtrigger_risk": "low" if len(desc) > 120 and triggers else "medium",
        "undertrigger_risk": "low" if triggers else "high",
    }
    score["overall"] = round(
        (score["trigger_accuracy"] + score["clarity"] + score["scope_fit"]
         + score["frontmatter_compliance"] + score["operational_completeness"]) / 5, 2
    )
    improvements: list[str] = []
    if not triggers:
        improvements.append(f"Add explicit trigger phrases (one of: {TRIGGER_HINTS.get(name)})")
    if len(desc) < 80:
        improvements.append("Description too short to disambiguate; add 1-2 example phrases.")
    if "<" in desc and ">" in desc:
        improvements.append("Remove XML tags from description.")
    return {
        "name": name,
        "skill_md": str(skill_md),
        "description_chars": len(desc),
        "triggers_matched": triggers,
        "score": score,
        "recommended_improvements": improvements,
    }


async def amain():
    summary = await run_query(label="11-skill-creator-review", prompt=SDK_PROMPT, max_turns=4)
    run_dir = Path(summary["run_dir"])
    fm_out = run_dir / "frontmatter.json"
    proc = subprocess.run(
        [sys.executable, str(HARNESS_ROOT / "validate_skill_frontmatter.py"),
         "--skills-dir", str(PLUGIN_ROOT / "skills"),
         "--output", str(fm_out)],
        capture_output=True, text=True, timeout=60,
    )
    (run_dir / "frontmatter-stderr.txt").write_text(proc.stderr or "", encoding="utf-8")
    reviews: list[dict] = []
    skills_dir = PLUGIN_ROOT / "skills"
    if skills_dir.exists():
        for child in sorted(skills_dir.iterdir()):
            skill_md = child / "SKILL.md"
            if child.is_dir() and skill_md.exists():
                reviews.append(review_skill(child.name, skill_md))
    (run_dir / "skill-creator-review.json").write_text(
        json.dumps({"reviews": reviews, "all_pass": all(r["score"]["overall"] >= 4.0 for r in reviews)}, indent=2),
        encoding="utf-8",
    )
    summary["skill_reviews"] = [{"name": r["name"], "overall": r["score"]["overall"], "improvements": len(r["recommended_improvements"])} for r in reviews]
    summary["skill_creator_all_pass"] = all(r["score"]["overall"] >= 4.0 for r in reviews)
    return summary


if __name__ == "__main__":
    raise SystemExit(main_sync(amain))
