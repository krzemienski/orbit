#!/usr/bin/env python3
"""Orbit flat helper script for intent mining, gap analysis, validation, and dashboard output."""
from __future__ import annotations

import argparse
import csv
import html
import json
import logging
import os
import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

LOG = logging.getLogger("orbit")

COLORS = {
    "black": "#0A0A0B",
    "carbon": "#0F1012",
    "slate": "#171920",
    "panel": "#232734",
    "light": "#C7CDD8",
    "white": "#F4F7FB",
    "lime": "#C6FF00",
    "orange": "#FF8A00",
    "red": "#FF4D36",
    "purple": "#8B3DFF",
    "blue": "#1E6BFF",
}

INTENT_PATTERNS = [
    "actually", "instead", "we decided", "go with", "settled on", "from now on",
    "make sure", "must", "do not", "don't", "you forgot", "this is wrong",
    "changed our mind", "gap analysis", "dashboard", "validate", "audit", "remediate",
]

CLAIM_PATTERNS = [
    "i implemented", "i created", "i added", "i updated", "i fixed", "i built",
    "done", "completed", "this now works", "generated",
]

TOOL_HINTS = ["tool_use", "tool_result", "bash", "edit", "write", "read", "command", "file", "result"]


def configure_logging(verbose: bool = False) -> None:
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)sZ %(levelname)s %(name)s %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S",
    )
    logging.Formatter.converter = lambda *args: datetime.now(timezone.utc).timetuple()


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def parse_date(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        if value.endswith("Z"):
            value = value[:-1] + "+00:00"
        if re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
            return datetime.fromisoformat(value).replace(tzinfo=timezone.utc)
        parsed = datetime.fromisoformat(value)
        return (parsed if parsed.tzinfo else parsed.replace(tzinfo=timezone.utc)).astimezone(timezone.utc)
    except ValueError:
        return None


def compute_window(days: int | None, since: str | None, start: str | None, end: str | None) -> tuple[datetime | None, datetime | None]:
    end_dt = parse_date(end) if end else datetime.now(timezone.utc)
    if start:
        return parse_date(start), end_dt
    if since:
        return parse_date(since), end_dt
    return end_dt - timedelta(days=days or 3), end_dt


def default_session_root() -> Path:
    if os.name == "nt":
        return Path(os.environ.get("USERPROFILE", str(Path.home()))) / ".claude" / "projects"
    return Path.home() / ".claude" / "projects"


def flatten(value: Any) -> str:
    out: list[str] = []

    def visit(node: Any) -> None:
        if node is None:
            return
        if isinstance(node, str):
            out.append(node)
            return
        if isinstance(node, (int, float, bool)):
            out.append(str(node))
            return
        if isinstance(node, list):
            for item in node:
                visit(item)
            return
        if isinstance(node, dict):
            for key in ("content", "text", "message", "result", "toolUseResult", "tool_result", "summary", "name", "type", "role", "cwd", "command", "file_path", "path", "input", "output", "error"):
                if key in node:
                    visit(node[key])

    visit(value)
    return re.sub(r"\s+", " ", " ".join(out)).strip()


def get_role(raw: dict[str, Any]) -> str:
    if isinstance(raw.get("role"), str):
        return raw["role"]
    msg = raw.get("message")
    if isinstance(msg, dict) and isinstance(msg.get("role"), str):
        return msg["role"]
    typ = str(raw.get("type", "")).lower()
    if typ in {"user", "assistant", "system"}:
        return typ
    if "user" in typ:
        return "user"
    if "assistant" in typ:
        return "assistant"
    return ""


def get_timestamp(raw: dict[str, Any]) -> str:
    for key in ("timestamp", "createdAt", "created_at", "time", "datetime"):
        if raw.get(key):
            return str(raw[key])
    return ""


def get_type(raw: dict[str, Any]) -> str:
    for key in ("type", "event", "event_type"):
        if raw.get(key):
            return str(raw[key])
    return ""


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    events: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8", errors="replace") as handle:
        for line_no, line in enumerate(handle, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                raw = json.loads(line)
            except json.JSONDecodeError as exc:
                LOG.debug("Skipping malformed line path=%s line=%s error=%s", path, line_no, exc)
                continue
            if not isinstance(raw, dict):
                raw = {"value": raw}
            events.append({
                "source_file": str(path),
                "line_number": line_no,
                "event_index": len(events),
                "timestamp": get_timestamp(raw),
                "role": get_role(raw),
                "event_type": get_type(raw),
                "content_text": flatten(raw),
                "raw": raw,
            })
    return events


def discover_sessions(session_root: Path | None, project: Path, start_dt: datetime | None, end_dt: datetime | None, explicit_sessions: list[str] | None) -> list[Path]:
    if explicit_sessions:
        return [Path(item).expanduser() for item in explicit_sessions if Path(item).expanduser().exists()]
    root = (session_root or default_session_root()).expanduser()
    if not root.exists():
        return []
    project_filter = project.name.lower() if project and project.exists() else ""
    output: list[Path] = []
    for path in sorted(root.rglob("*.jsonl"), key=lambda p: p.stat().st_mtime):
        if project_filter and project_filter not in str(path).lower():
            # Keep filtering gentle: encoded paths can be different, but this avoids huge scans by default.
            continue
        mtime = datetime.fromtimestamp(path.stat().st_mtime, timezone.utc)
        if start_dt and mtime < start_dt:
            continue
        if end_dt and mtime > end_dt:
            continue
        output.append(path)
    return output


def load_events(session_files: list[Path]) -> list[dict[str, Any]]:
    events: list[dict[str, Any]] = []
    for path in session_files:
        events.extend(read_jsonl(path))
    return sorted(events, key=lambda e: (e.get("timestamp") or "", e["source_file"], e["line_number"]))


def matches_any(text: str, patterns: list[str]) -> list[str]:
    lower = text.lower()
    return [pattern for pattern in patterns if pattern in lower]


def classify_intent(text: str) -> str:
    lower = text.lower()
    if any(token in lower for token in ["dashboard", "visual", "diagram", "flowchart"]):
        return "visualization-request"
    if any(token in lower for token in ["validate", "prove", "actually completed", "check against"]):
        return "validation-request"
    if any(token in lower for token in ["actually", "instead", "wrong", "forgot"]):
        return "correction"
    if any(token in lower for token in ["go with", "settled on", "rename", "name"]):
        return "decision"
    if any(token in lower for token in ["do not", "don't", "must", "make sure"]):
        return "constraint"
    return "requirement"


def source_ref(event: dict[str, Any]) -> dict[str, Any]:
    return {
        "source_type": "session",
        "file": event["source_file"],
        "line": event["line_number"],
        "timestamp": event.get("timestamp", ""),
        "role": event.get("role", ""),
    }


def extract_intents(events: list[dict[str, Any]]) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for event in events:
        text = event.get("content_text", "")
        if event.get("role") != "user" or not text:
            continue
        matched = matches_any(text, INTENT_PATTERNS)
        if not matched and len(text) < 60:
            continue
        records.append({
            "id": f"intent_{len(records)+1:04d}",
            "kind": classify_intent(text),
            "text": text[:1200],
            "source": source_ref(event),
            "directness": "direct",
            "specificity": "high" if matched else "medium",
            "status": "active",
            "matched_patterns": matched,
        })
    return records


def extract_claims(events: list[dict[str, Any]]) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for event in events:
        text = event.get("content_text", "")
        if event.get("role") != "assistant" or not text:
            continue
        matched = matches_any(text, CLAIM_PATTERNS)
        if not matched:
            continue
        records.append({
            "id": f"claim_{len(records)+1:04d}",
            "text": text[:1200],
            "claim_type": "completion",
            "source": source_ref(event),
            "validation_status": "unverified",
        })
    return records


def extract_tool_evidence(events: list[dict[str, Any]]) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for event in events:
        hay = f"{event.get('event_type', '')} {event.get('content_text', '')}".lower()
        if not any(hint in hay for hint in TOOL_HINTS):
            continue
        raw = event.get("raw", {})
        target = ""
        for key in ("path", "file_path", "command"):
            if isinstance(raw.get(key), str):
                target = raw[key]
                break
        records.append({
            "id": f"tool_{len(records)+1:04d}",
            "tool_name": str(raw.get("tool", raw.get("name", event.get("event_type") or "unknown"))),
            "action": event.get("event_type") or "observed",
            "target": target,
            "status": "observed",
            "source": source_ref(event),
            "text": event.get("content_text", "")[:1200],
        })
    return records


def discover_plan_files(project: Path, plan_args: list[str] | None) -> list[Path]:
    files: list[Path] = []
    if plan_args:
        for item in plan_args:
            path = Path(item).expanduser()
            if not path.is_absolute():
                path = project / path
            if path.is_dir():
                files.extend(sorted(path.rglob("*.md")))
            elif path.exists():
                files.append(path)
        return files
    for name in ["PLAN.md", "PRD.md", "README.md", "TODO.md", "TASKS.md", "IMPLEMENTATION.md"]:
        path = project / name
        if path.exists():
            files.append(path)
    docs = project / "docs"
    if docs.exists():
        files.extend(sorted(docs.rglob("*.md")))
    return files


def extract_plan_items(project: Path, plan_args: list[str] | None) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    for path in discover_plan_files(project, plan_args):
        heading = ""
        try:
            lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
        except OSError:
            continue
        for line_no, line in enumerate(lines, start=1):
            stripped = line.strip()
            if not stripped:
                continue
            if stripped.startswith("#"):
                heading = stripped.lstrip("#").strip()
                items.append({"id": f"plan_{len(items)+1:04d}", "source_file": str(path), "line_number": line_no, "heading": heading, "text": stripped, "status_hint": "heading"})
            elif re.match(r"^([-*+] |\d+\. )", stripped):
                items.append({"id": f"plan_{len(items)+1:04d}", "source_file": str(path), "line_number": line_no, "heading": heading, "text": stripped, "status_hint": "planned"})
    return items


def token_similarity(a: str, b: str) -> float:
    aw = set(re.findall(r"[a-z0-9]+", a.lower()))
    bw = set(re.findall(r"[a-z0-9]+", b.lower()))
    return 0.0 if not aw or not bw else len(aw & bw) / max(1, len(aw | bw))


def validate_codebase(project: Path, claims: list[dict[str, Any]]) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    for rel in [".claude/audits/latest/dashboard.html", ".claude/audits/latest/evidence.json", ".claude/audits/latest/gap-analysis.md"]:
        exists = (project / rel).exists()
        results.append({
            "id": f"validation_{len(results)+1:04d}",
            "target_type": "artifact",
            "target_id": rel,
            "check": "artifact_exists",
            "path": rel,
            "status": "passed" if exists else "failed",
            "evidence": "Artifact exists." if exists else "Artifact not found in current repository.",
            "severity": "low" if exists else "medium",
        })
    path_re = re.compile(r"([\w./-]+\.(?:py|md|json|html|js|ts|tsx|jsx|css|yml|yaml|sh))")
    for claim in claims:
        paths = path_re.findall(claim.get("text", ""))
        if not paths:
            status, evidence, path_value, severity = "unverified", "No explicit file path found in claim.", "", "medium"
        else:
            exists = [p for p in paths if (project / p).exists()]
            status = "passed" if exists else "failed"
            evidence = "At least one mentioned path exists." if exists else "Mentioned paths were not found."
            path_value = ", ".join(paths)
            severity = "low" if exists else "high"
        results.append({
            "id": f"validation_{len(results)+1:04d}",
            "target_type": "claim",
            "target_id": claim["id"],
            "check": "claim_path_exists",
            "path": path_value,
            "status": status,
            "evidence": evidence,
            "severity": severity,
        })
    return results


def analyze_gaps(intents: list[dict[str, Any]], plans: list[dict[str, Any]], claims: list[dict[str, Any]], validations: list[dict[str, Any]]) -> list[dict[str, Any]]:
    gaps: list[dict[str, Any]] = []
    plan_texts = [item["text"] for item in plans]
    for intent in intents:
        best = max((token_similarity(intent["text"], plan) for plan in plan_texts), default=0.0)
        if best < 0.08:
            gaps.append({
                "id": f"gap_{len(gaps)+1:04d}",
                "category": "intent-not-planned",
                "severity": "medium",
                "title": "Intent appears session-only or absent from plans",
                "summary": f"No strong plan evidence matched intent: {intent['text'][:180]}",
                "evidence_ids": [intent["id"]],
                "recommended_next_action": "Review this intent and update the plan or mark it intentionally out of scope.",
            })
    by_claim = {v["target_id"]: v for v in validations if v.get("target_type") == "claim"}
    for claim in claims:
        validation = by_claim.get(claim["id"])
        if not validation or validation["status"] in {"unverified", "failed"}:
            gaps.append({
                "id": f"gap_{len(gaps)+1:04d}",
                "category": "claim-not-validated" if not validation or validation["status"] == "unverified" else "claim-contradicted",
                "severity": "high" if validation and validation["status"] == "failed" else "medium",
                "title": "Assistant claim requires validation",
                "summary": f"Claim is not fully validated: {claim['text'][:180]}",
                "evidence_ids": [claim["id"]] + ([validation["id"]] if validation else []),
                "recommended_next_action": "Inspect tool evidence and codebase state, then run configured safe validation checks.",
            })
    if not intents and not plans and not claims:
        gaps.append({
            "id": "gap_0001",
            "category": "ambiguous-evidence",
            "severity": "low",
            "title": "No audit evidence found",
            "summary": "Orbit did not find plan, session, or claim evidence in the selected scope.",
            "evidence_ids": [],
            "recommended_next_action": "Broaden the time window, provide plan paths, or point Orbit to the correct session root.",
        })
    return gaps


def make_evidence(args: argparse.Namespace) -> dict[str, Any]:
    project = Path(args.project).expanduser().resolve()
    start_dt, end_dt = compute_window(getattr(args, "days", None), getattr(args, "since", None), getattr(args, "start", None), getattr(args, "end", None))
    session_files = discover_sessions(Path(args.session_root).expanduser() if getattr(args, "session_root", None) else None, project, start_dt, end_dt, getattr(args, "sessions", None))
    events = load_events(session_files)
    intents = extract_intents(events)
    plans = extract_plan_items(project, getattr(args, "plans", None))
    claims = extract_claims(events)
    tools = extract_tool_evidence(events)
    validations = validate_codebase(project, claims) if getattr(args, "validate_codebase", False) else []
    gaps = analyze_gaps(intents, plans, claims, validations)
    return {
        "schema_version": "0.2",
        "generated_at": now_iso(),
        "project": {"cwd": str(project), "name": project.name},
        "scope": {"days": getattr(args, "days", None) or 3, "since": getattr(args, "since", None), "from": getattr(args, "start", None), "to": getattr(args, "end", None), "query": getattr(args, "query", ""), "plans": getattr(args, "plans", None) or []},
        "sources": {"sessions": [str(p) for p in session_files], "plans": sorted({p["source_file"] for p in plans})},
        "intents": intents,
        "plan_items": plans,
        "claims": claims,
        "tool_evidence": tools,
        "validations": validations,
        "gaps": gaps,
        "conflicts": [],
        "uncertainties": [],
    }


def render_markdown(evidence: dict[str, Any]) -> str:
    counts = {k: len(evidence.get(k, [])) for k in ["intents", "plan_items", "claims", "tool_evidence", "validations", "gaps"]}
    scope = evidence.get("scope", {}) or {}
    scope_str = ", ".join(f"{k}={v}" for k, v in [
        ("days", scope.get("days")),
        ("since", scope.get("since")),
        ("from", scope.get("from")),
        ("to", scope.get("to")),
    ] if v not in (None, "")) or "default"
    lines = [
        "# Orbit Gap Analysis", "", f"Generated: {evidence['generated_at']}", f"Project: `{evidence['project']['cwd']}`",
        f"Scope: `{scope_str}`", "",
        "## Executive Summary", "",
        f"Orbit found {counts['intents']} intent records, {counts['plan_items']} plan items, {counts['claims']} assistant claims, {counts['tool_evidence']} tool evidence records, {counts['validations']} validation results, and {counts['gaps']} gaps.", "",
        "## Gaps", "",
    ]
    for gap in evidence.get("gaps", []):
        lines += [f"### {gap['title']}", "", f"- Category: `{gap['category']}`", f"- Severity: `{gap['severity']}`", f"- Summary: {gap['summary']}", f"- Next action: {gap['recommended_next_action']}", ""]
    lines += ["## Current Controlling Principle", "", "Plans are evidence, not the complete historical record. Assistant claims are claims, not proof. Codebase validation is required before completion is trusted."]
    return "\n".join(lines).rstrip() + "\n"


def render_flow() -> str:
    return """flowchart TD
  U[Direct User Instruction] --> I[Intent Record]
  C[User Correction / Pivot] --> I
  P[Written Plan Item] --> PM[Plan Mapping]
  A[Assistant Completion Claim] --> CL[Claim Record]
  T[Tool Use / Tool Result] --> TE[Tool Evidence]
  R[Current Repository State] --> V[Validation Result]
  I --> G[Gap Analyzer]
  PM --> G
  CL --> G
  TE --> G
  V --> G
  G --> OK[Validated Complete]
  G --> GP[Confirmed Gap]
  G --> CF[Conflict]
  G --> UN[Uncertainty]
  GP --> N[Recommended Next Action]
"""


def render_timeline() -> str:
    return """timeline
  title Orbit Session Drift Timeline
  Audit : Scope detected
        : Plans searched
        : Sessions mined
        : Claims extracted
        : Repo validation checked
        : Gaps produced
"""


def render_dashboard(evidence: dict[str, Any]) -> str:
    counts = {k: len(evidence.get(k, [])) for k in ["intents", "plan_items", "claims", "tool_evidence", "validations", "gaps"]}
    gap_cards = []
    for gap in evidence.get("gaps", []):
        sev = gap.get("severity", "medium")
        accent = COLORS["red"] if sev == "high" else COLORS["orange"] if sev == "medium" else COLORS["blue"]
        gap_cards.append(f"""
        <article class="gap-card" style="border-color:{accent}">
          <div class="gap-meta">{html.escape(gap.get('category', 'gap'))} · {html.escape(sev)}</div>
          <h3>{html.escape(gap.get('title', 'Gap'))}</h3>
          <p>{html.escape(gap.get('summary', ''))}</p>
          <strong>Next:</strong> {html.escape(gap.get('recommended_next_action', 'Review evidence.'))}
        </article>
        """)
    scope = evidence.get("scope", {}) or {}
    scope_summary = ", ".join(
        f"{k}={v}" for k, v in [
            ("days", scope.get("days")),
            ("since", scope.get("since")),
            ("from", scope.get("from")),
            ("to", scope.get("to")),
        ] if v not in (None, "")
    ) or "default"
    sources = evidence.get("sources", {}) or {}
    session_count = len(sources.get("sessions", []) or [])
    plan_source_count = len(sources.get("plans", []) or [])
    claim_rows = []
    for claim in evidence.get("claims", [])[:25]:
        status = claim.get("validation_status", "unverified")
        accent = COLORS["lime"] if status == "validated" else COLORS["red"] if status in {"contradicted", "failed"} else COLORS["orange"]
        claim_rows.append(
            "<tr><td>{cid}</td><td style=\"color:{accent}\">{status}</td><td>{text}</td></tr>".format(
                cid=html.escape(str(claim.get("id", ""))),
                accent=accent,
                status=html.escape(str(status)),
                text=html.escape(str(claim.get("text", ""))[:240]),
            )
        )
    if not claim_rows:
        claim_rows.append('<tr><td colspan="3" class="muted">No assistant claims observed in scope.</td></tr>')
    timeline_items = []
    for evt in evidence.get("intents", [])[:20]:
        ts = (evt.get("source") or {}).get("timestamp", "")
        timeline_items.append(
            "<li><span class=\"ts\">{ts}</span><span class=\"kind\">{kind}</span><span class=\"text\">{text}</span></li>".format(
                ts=html.escape(ts or "—"),
                kind=html.escape(str(evt.get("kind", "intent"))),
                text=html.escape(str(evt.get("text", ""))[:200]),
            )
        )
    if not timeline_items:
        timeline_items.append('<li class="muted">No intents recorded in scope.</li>')
    uncertainties = evidence.get("uncertainties", []) or []
    if not uncertainties:
        # Surface unverified claims and ambiguous-evidence gaps as uncertainty rows
        for claim in evidence.get("claims", []):
            if claim.get("validation_status") == "unverified":
                uncertainties.append({
                    "id": f"unc_{claim.get('id', '')}",
                    "summary": "Claim not yet validated against repo or tool evidence.",
                    "evidence": claim.get("id"),
                })
        for gap in evidence.get("gaps", []):
            if gap.get("category") in {"ambiguous-evidence", "missing-validation"}:
                uncertainties.append({
                    "id": f"unc_{gap.get('id', '')}",
                    "summary": gap.get("summary", "Ambiguous evidence."),
                    "evidence": gap.get("id"),
                })
    uncertainty_items = []
    for unc in uncertainties[:20]:
        uncertainty_items.append(
            "<li><strong>{uid}</strong> {summary} <span class=\"muted\">{ev}</span></li>".format(
                uid=html.escape(str(unc.get("id", ""))),
                summary=html.escape(str(unc.get("summary", ""))),
                ev=html.escape(str(unc.get("evidence", ""))),
            )
        )
    if not uncertainty_items:
        uncertainty_items.append('<li class="muted">No uncertainty surfaced in scope.</li>')
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Orbit Gap Analysis</title>
<style>
:root {{ --black:{COLORS['black']}; --carbon:{COLORS['carbon']}; --white:{COLORS['white']}; --light:{COLORS['light']}; --lime:{COLORS['lime']}; --purple:{COLORS['purple']}; --orange:{COLORS['orange']}; --blue:{COLORS['blue']}; --red:{COLORS['red']}; }}
* {{ box-sizing:border-box; }}
body {{ margin:0; background:var(--black); color:var(--white); font-family:Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; }}
main {{ max-width:1180px; margin:0 auto; padding:36px 22px 56px; }}
.hero {{ border:1px solid #252936; border-radius:28px; padding:30px; background:#0F1012; }}
.logo {{ display:flex; align-items:center; gap:14px; letter-spacing:.18em; font-weight:900; font-size:34px; }}
.orb {{ width:34px; height:34px; border:3px solid var(--lime); border-radius:999px; position:relative; box-shadow:0 0 22px rgba(198,255,0,.28); }}
.orb:after {{ content:''; position:absolute; width:54px; height:16px; border:2px solid var(--purple); border-left:0; border-right:0; border-radius:999px; top:6px; left:-12px; transform:rotate(-24deg); }}
.tagline {{ color:var(--lime); margin-top:8px; font-size:13px; letter-spacing:.2em; text-transform:uppercase; }}
.grid {{ display:grid; grid-template-columns:repeat(4,1fr); gap:14px; margin:22px 0; }}
.card, .gap-card {{ background:#0F1012; border:1px solid #242835; border-radius:22px; padding:18px; }}
.card span {{ color:var(--light); font-size:12px; text-transform:uppercase; letter-spacing:.12em; }}
.card b {{ display:block; font-size:32px; margin-top:10px; }}
.section {{ margin-top:24px; }}
.section h2 {{ border-bottom:1px solid #252936; padding-bottom:12px; }}
table {{ width:100%; border-collapse:collapse; }}
th,td {{ border-bottom:1px solid #242835; padding:12px; text-align:left; vertical-align:top; }}
th {{ color:var(--lime); font-size:12px; letter-spacing:.1em; text-transform:uppercase; }}
.gaps {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(260px,1fr)); gap:14px; }}
.gap-meta {{ color:var(--purple); font-size:12px; text-transform:uppercase; letter-spacing:.1em; }}
.scope-line {{ color:var(--lime); margin-top:14px; font-size:13px; letter-spacing:.05em; }}
.scope-line span {{ color:var(--light); }}
.timeline {{ list-style:none; padding:0; margin:0; display:flex; flex-direction:column; gap:8px; }}
.timeline li {{ background:#0F1012; border-left:3px solid var(--purple); padding:10px 14px; border-radius:10px; display:flex; gap:12px; align-items:baseline; flex-wrap:wrap; }}
.timeline .ts {{ color:var(--blue); min-width:160px; font-variant-numeric:tabular-nums; font-size:12px; }}
.timeline .kind {{ color:var(--orange); font-size:12px; text-transform:uppercase; letter-spacing:.08em; min-width:120px; }}
.timeline .text {{ color:var(--light); flex:1 1 320px; }}
.uncertainty {{ list-style:none; padding:0; margin:0; display:grid; gap:8px; }}
.uncertainty li {{ background:#0F1012; border-left:3px solid var(--orange); padding:10px 14px; border-radius:10px; }}
.muted {{ color:var(--light); opacity:.7; font-style:italic; }}
code {{ color:var(--lime); }}
@media(max-width:800px){{.grid{{grid-template-columns:repeat(2,1fr);}}}}
</style>
</head>
<body>
<main>
  <section class="hero"><div class="logo"><div class="orb"></div>ORBIT</div><div class="tagline">Find drift. Close gaps. Restore alignment.</div>
    <div class="scope-line">Scope: <span>{html.escape(scope_summary)}</span> · Sessions mined: <span>{session_count}</span> · Plan sources: <span>{plan_source_count}</span> · Generated: <span>{html.escape(evidence.get('generated_at', ''))}</span></div>
  </section>
  <section class="grid">
    <div class="card"><span>Intents</span><b>{counts['intents']}</b></div>
    <div class="card"><span>Plan Items</span><b>{counts['plan_items']}</b></div>
    <div class="card"><span>Claims</span><b>{counts['claims']}</b></div>
    <div class="card"><span>Gaps</span><b>{counts['gaps']}</b></div>
  </section>
  <section class="section"><h2>Intent → Plan → Claim → Tool → Repo Matrix</h2><table><thead><tr><th>Layer</th><th>Count</th><th>Status</th></tr></thead><tbody>
    <tr><td>User intent</td><td>{counts['intents']}</td><td>mined</td></tr>
    <tr><td>Plan evidence</td><td>{counts['plan_items']}</td><td>extracted</td></tr>
    <tr><td>Assistant claims</td><td>{counts['claims']}</td><td>requires validation</td></tr>
    <tr><td>Tool evidence</td><td>{counts['tool_evidence']}</td><td>observed</td></tr>
    <tr><td>Repo validation</td><td>{counts['validations']}</td><td>checked</td></tr>
  </tbody></table></section>
  <section class="section"><h2>Intent Timeline</h2><ul class="timeline">{''.join(timeline_items)}</ul></section>
  <section class="section"><h2>Claim Validation</h2><table><thead><tr><th>Claim</th><th>Status</th><th>Text</th></tr></thead><tbody>{''.join(claim_rows)}</tbody></table></section>
  <section class="section"><h2>Gaps</h2><div class="gaps">{''.join(gap_cards) if gap_cards else '<p>No gaps detected in selected scope.</p>'}</div></section>
  <section class="section"><h2>Uncertainty</h2><ul class="uncertainty">{''.join(uncertainty_items)}</ul></section>
</main>
</body>
</html>
"""


def write_outputs(output: Path, evidence: dict[str, Any]) -> None:
    output.mkdir(parents=True, exist_ok=True)
    (output / "evidence.json").write_text(json.dumps(evidence, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (output / "gap-analysis.md").write_text(render_markdown(evidence), encoding="utf-8")
    (output / "dashboard.html").write_text(render_dashboard(evidence), encoding="utf-8")
    (output / "intent-gap-flow.mmd").write_text(render_flow(), encoding="utf-8")
    (output / "intent-timeline.mmd").write_text(render_timeline(), encoding="utf-8")
    with (output / "plan-execution-matrix.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["Intent", "Plan Coverage", "Assistant Claim", "Status", "Next Action"])
        for intent in evidence.get("intents", []):
            writer.writerow([intent.get("text", "")[:180], "see plan items", "see claims", "review", "Validate and remediate."])
        if not evidence.get("intents"):
            writer.writerow(["No intent found", "unknown", "unknown", "uncertain", "Broaden search scope."])


def build_ledger(output: Path, evidence: dict[str, Any], replace: bool) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    mode = "w" if replace else "a"
    with output.open(mode, encoding="utf-8") as handle:
        for intent in evidence.get("intents", []):
            src = intent.get("source", {})
            handle.write(json.dumps({
                "schema_version": "0.2",
                "id": intent.get("id"),
                "timestamp": src.get("timestamp") or now_iso(),
                "project": evidence.get("project", {}).get("name", ""),
                "kind": intent.get("kind"),
                "text": intent.get("text"),
                "source_type": src.get("source_type", "session"),
                "source_ref": f"{src.get('file', '')}:{src.get('line', '')}",
                "confidence": "high" if intent.get("specificity") == "high" else "medium",
                "status": intent.get("status", "active"),
                "tags": intent.get("matched_patterns", []),
                "supersedes": [],
                "superseded_by": [],
            }, ensure_ascii=False) + "\n")
    md = output.with_suffix(".md")
    lines = ["# Orbit Intent Ledger", "", f"Generated: {now_iso()}", ""]
    for intent in evidence.get("intents", []):
        lines.append(f"- **{intent.get('kind')}**: {intent.get('text', '')[:240]}")
    md.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def add_common_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--project", default=".", help="Project/repo root.")
    parser.add_argument("--plans", nargs="*", help="Plan files or directories to inspect.")
    parser.add_argument("--session-root", help="Root containing Claude Code session JSONL files.")
    parser.add_argument("--sessions", nargs="*", help="Explicit session JSONL files.")
    parser.add_argument("--days", type=int, default=3, help="Lookback window in days. Defaults to 3.")
    parser.add_argument("--since", help="Start date/time, e.g. 2026-05-01.")
    parser.add_argument("--from", dest="start", help="Explicit start date/time.")
    parser.add_argument("--to", dest="end", help="Explicit end date/time.")
    parser.add_argument("--query", default="", help="Human audit query for the evidence scope.")
    parser.add_argument("--validate-codebase", action="store_true", help="Run safe, non-destructive repo validation checks.")
    parser.add_argument("--verbose", action="store_true")


def cmd_audit(args: argparse.Namespace) -> int:
    configure_logging(args.verbose)
    evidence = make_evidence(args)
    output = Path(args.output).expanduser()
    write_outputs(output, evidence)
    LOG.info("Wrote Orbit audit outputs to %s", output)
    print(output)
    return 0


def cmd_build_ledger(args: argparse.Namespace) -> int:
    configure_logging(args.verbose)
    args.validate_codebase = False
    evidence = make_evidence(args)
    output = Path(args.output).expanduser()
    build_ledger(output, evidence, args.replace)
    LOG.info("Wrote Orbit ledger to %s", output)
    print(output)
    return 0


def cmd_compare_plan(args: argparse.Namespace) -> int:
    return cmd_audit(args)


def cmd_validate_claims(args: argparse.Namespace) -> int:
    configure_logging(args.verbose)
    project = Path(args.project).expanduser().resolve()
    if args.evidence and Path(args.evidence).exists():
        evidence = json.loads(Path(args.evidence).read_text(encoding="utf-8"))
        evidence["validations"] = validate_codebase(project, evidence.get("claims", []))
        evidence["gaps"] = analyze_gaps(evidence.get("intents", []), evidence.get("plan_items", []), evidence.get("claims", []), evidence.get("validations", []))
    else:
        args.validate_codebase = True
        evidence = make_evidence(args)
    output = Path(args.output).expanduser()
    write_outputs(output, evidence)
    print(output)
    return 0


def cmd_render_dashboard(args: argparse.Namespace) -> int:
    configure_logging(args.verbose)
    evidence_path = Path(args.evidence).expanduser()
    evidence = json.loads(evidence_path.read_text(encoding="utf-8"))
    output = Path(args.output).expanduser()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_dashboard(evidence), encoding="utf-8")
    print(output)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Orbit intent gap auditor helper script.")
    sub = parser.add_subparsers(dest="command", required=True)

    audit = sub.add_parser("audit", help="Run full Orbit audit.")
    add_common_args(audit)
    audit.add_argument("--dashboard", action="store_true", help="Accepted for command parity; dashboard is always written.")
    audit.add_argument("--output", default=".claude/audits/latest")
    audit.set_defaults(func=cmd_audit)

    ledger = sub.add_parser("build-ledger", help="Build durable instruction ledger.")
    add_common_args(ledger)
    ledger.add_argument("--output", default=".claude/audits/intent-ledger.jsonl")
    ledger.add_argument("--replace", action="store_true")
    ledger.add_argument("--all", action="store_true", help="Accepted for command parity.")
    ledger.set_defaults(func=cmd_build_ledger)

    compare = sub.add_parser("compare-plan", help="Compare plan to sessions and repo truth.")
    add_common_args(compare)
    compare.add_argument("--plan", action="append", help="Plan file. Can be supplied multiple times.")
    compare.add_argument("--dashboard", action="store_true")
    compare.add_argument("--output", default=".claude/audits/latest")
    compare.set_defaults(func=lambda args: (setattr(args, "plans", (args.plans or []) + (args.plan or [])) or cmd_compare_plan(args)))

    validate = sub.add_parser("validate-claims", help="Validate claims from evidence or current sessions.")
    add_common_args(validate)
    validate.add_argument("--evidence", help="Existing evidence JSON file.")
    validate.add_argument("--output", default=".claude/audits/latest")
    validate.set_defaults(func=cmd_validate_claims)

    dash = sub.add_parser("render-dashboard", help="Render dashboard from evidence JSON.")
    dash.add_argument("--evidence", required=True)
    dash.add_argument("--output", default=".claude/audits/latest/dashboard.html")
    dash.add_argument("--verbose", action="store_true")
    dash.set_defaults(func=cmd_render_dashboard)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
