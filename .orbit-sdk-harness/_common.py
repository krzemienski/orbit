"""Shared helpers for the Orbit SDK harness. No mocks. Real I/O only."""
from __future__ import annotations

import asyncio
import csv
import json
import os
import shutil
import subprocess
import sys
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

HARNESS_ROOT = Path(__file__).resolve().parent
PLUGIN_ROOT = HARNESS_ROOT.parent
RUNS_ROOT = HARNESS_ROOT / "runs"
REPORTS_ROOT = HARNESS_ROOT / "reports"
SCENARIOS_ROOT = HARNESS_ROOT / "scenarios"


# ----------------------------- Logging ---------------------------------------


def log(msg: str) -> None:
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    print(f"[{ts}] {msg}", file=sys.stderr, flush=True)


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def now_compact() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


# ----------------------------- Plugin discovery -------------------------------


def resolve_plugin_root(explicit: str | None = None) -> Path:
    if explicit:
        return Path(explicit).expanduser().resolve()
    env = os.environ.get("CLAUDE_PLUGIN_ROOT")
    if env:
        return Path(env).expanduser().resolve()
    return PLUGIN_ROOT


def discover_layout(root: Path) -> dict[str, Any]:
    """Inventory the local Orbit project layout. No assumptions, only observed paths."""
    layout: dict[str, Any] = {
        "plugin_root": str(root),
        "exists": root.exists(),
        "manifest": None,
        "skills_dir": None,
        "commands_dir": None,
        "hooks_dir": None,
        "scripts_dir": None,
        "bin_dir": None,
        "skills": [],
        "commands": [],
        "hooks_file": None,
        "scripts": [],
        "bin": [],
        "readme": None,
        "changelog": None,
        "prd": None,
        "claude_md": None,
        "tests_dir": None,
        "examples_dir": None,
    }
    if not root.exists():
        return layout

    manifest = root / ".claude-plugin" / "plugin.json"
    if manifest.exists():
        layout["manifest"] = str(manifest)

    for key, sub in [
        ("skills_dir", "skills"),
        ("commands_dir", "commands"),
        ("hooks_dir", "hooks"),
        ("scripts_dir", "scripts"),
        ("bin_dir", "bin"),
        ("tests_dir", "tests"),
        ("examples_dir", "examples"),
    ]:
        path = root / sub
        if path.exists() and path.is_dir():
            layout[key] = str(path)

    skills_root = root / "skills"
    if skills_root.exists():
        for child in sorted(skills_root.iterdir()):
            if child.is_dir() and (child / "SKILL.md").exists():
                layout["skills"].append({
                    "name": child.name,
                    "skill_md": str(child / "SKILL.md"),
                })

    commands_root = root / "commands"
    if commands_root.exists():
        for cmd in sorted(commands_root.glob("*.md")):
            layout["commands"].append({"name": cmd.stem, "path": str(cmd)})

    hooks_file = root / "hooks" / "hooks.json"
    if hooks_file.exists():
        layout["hooks_file"] = str(hooks_file)

    scripts_root = root / "scripts"
    if scripts_root.exists():
        for script in sorted(scripts_root.glob("*.py")):
            layout["scripts"].append(str(script))

    bin_root = root / "bin"
    if bin_root.exists():
        for entry in sorted(bin_root.iterdir()):
            if entry.is_file():
                layout["bin"].append({
                    "name": entry.name,
                    "path": str(entry),
                    "executable": os.access(entry, os.X_OK),
                })

    for key, name in [
        ("readme", "README.md"),
        ("changelog", "CHANGELOG.md"),
        ("prd", "PRD.md"),
        ("claude_md", "CLAUDE.md"),
    ]:
        candidate = root / name
        if candidate.exists():
            layout[key] = str(candidate)

    return layout


def installed_plugin_status() -> dict[str, Any]:
    """Inspect Claude Code installed-plugin state in a non-destructive way."""
    home = Path.home()
    installed_path = home / ".claude" / "plugins" / "installed_plugins.json"
    plugin_dirs = home / ".claude" / "plugins"
    status: dict[str, Any] = {
        "installed_plugins_json": str(installed_path) if installed_path.exists() else None,
        "plugin_dirs_root": str(plugin_dirs) if plugin_dirs.exists() else None,
        "orbit_installed": False,
        "orbit_install_dirs": [],
        "claude_cli": shutil.which("claude"),
    }
    if installed_path.exists():
        try:
            data = json.loads(installed_path.read_text(encoding="utf-8"))
            status["installed_plugins_payload_keys"] = sorted(list(data.keys())) if isinstance(data, dict) else []
            payload_str = json.dumps(data).lower()
            status["orbit_installed"] = "orbit" in payload_str
        except (OSError, json.JSONDecodeError) as exc:
            status["installed_plugins_payload_keys"] = []
            status["installed_plugins_read_error"] = f"{type(exc).__name__}: {exc}"
    if plugin_dirs.exists():
        for child in plugin_dirs.iterdir():
            if "orbit" in child.name.lower():
                status["orbit_install_dirs"].append(str(child))
    return status


# ----------------------------- Run dir + JSONL pointer -----------------------


def project_dir_name(run_dir: Path) -> str:
    """Mimic Claude Code per-project log dir convention."""
    return "-" + str(run_dir.resolve()).replace("/", "-").replace(".", "-").lstrip("-")


def make_run_dir(label: str) -> Path:
    RUNS_ROOT.mkdir(parents=True, exist_ok=True)
    run_id = f"{now_compact()}-{label}"
    run_dir = RUNS_ROOT / run_id
    run_dir.mkdir(parents=True, exist_ok=True)
    return run_dir


def jsonl_pointer_for(run_dir: Path, session_id: str) -> Path:
    return Path.home() / ".claude" / "projects" / project_dir_name(run_dir) / f"{session_id}.jsonl"


# ----------------------------- SDK helpers -----------------------------------


def _serialize(msg: Any) -> dict[str, Any]:
    cls = type(msg).__name__
    out: dict[str, Any] = {"_type": cls}
    if hasattr(msg, "__dict__"):
        for k, v in msg.__dict__.items():
            try:
                json.dumps(v)
                out[k] = v
            except TypeError:
                out[k] = repr(v)
    return out


async def run_query(
    *,
    label: str,
    prompt: str,
    max_turns: int = 6,
) -> dict[str, Any]:
    """Run a single live SDK query() and capture full evidence under runs/<id>/."""
    try:
        from claude_agent_sdk import query, ClaudeAgentOptions
        from claude_agent_sdk.types import SystemMessage, ResultMessage
    except Exception as exc:
        run_dir = make_run_dir(label)
        (run_dir / "exception.txt").write_text(
            f"ImportError: {type(exc).__name__}: {exc}\n", encoding="utf-8"
        )
        (run_dir / "transcript.json").write_text("[]\n", encoding="utf-8")
        (run_dir / "got-result.txt").write_text("false\n", encoding="utf-8")
        (run_dir / "summary.json").write_text(json.dumps({
            "label": label,
            "run_dir": str(run_dir),
            "got_result_message": False,
            "exception": f"ImportError: {exc}",
            "transcript_msg_count": 0,
        }, indent=2), encoding="utf-8")
        (run_dir / "prompt.md").write_text(prompt, encoding="utf-8")
        return {
            "label": label,
            "run_dir": str(run_dir),
            "got_result_message": False,
            "exception": f"ImportError: {exc}",
            "session_id": None,
            "jsonl_pointer": None,
            "transcript_msg_count": 0,
            "transcript_path": str(run_dir / "transcript.json"),
            "summary_path": str(run_dir / "summary.json"),
        }

    run_dir = make_run_dir(label)
    transcript_path = run_dir / "transcript.json"
    session_id_path = run_dir / "session-id.txt"
    jsonl_pointer_path = run_dir / "jsonl-pointer.txt"
    started_path = run_dir / "started-at.txt"
    finished_path = run_dir / "finished-at.txt"
    debug_log = run_dir / "debug.log"
    prompt_path = run_dir / "prompt.md"

    prompt_path.write_text(prompt, encoding="utf-8")
    started_path.write_text(now_iso() + "\n", encoding="utf-8")

    options = ClaudeAgentOptions(
        setting_sources=["user"],
        cwd=str(run_dir),
        permission_mode="bypassPermissions",
        max_turns=max_turns,
        extra_args={"debug-file": str(debug_log)},
    )

    transcript: list[dict[str, Any]] = []
    session_id: str | None = None
    exception: BaseException | None = None

    log(f"run start: {run_dir.name}")
    try:
        async for msg in query(prompt=prompt, options=options):
            rec = _serialize(msg)
            transcript.append(rec)
            sid = rec.get("session_id") or getattr(msg, "session_id", None)
            if sid and not session_id:
                session_id = sid
            if isinstance(msg, (SystemMessage, ResultMessage)):
                sid2 = getattr(msg, "session_id", None) or rec.get("session_id")
                if sid2:
                    session_id = sid2
    except BaseException as exc:  # noqa: BLE001
        exception = exc
        log(f"exception during stream: {type(exc).__name__}: {exc}")

    finished_path.write_text(now_iso() + "\n", encoding="utf-8")
    transcript_path.write_text(json.dumps(transcript, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    if session_id:
        session_id_path.write_text(session_id + "\n", encoding="utf-8")
        jsonl_pointer_path.write_text(str(jsonl_pointer_for(run_dir, session_id)) + "\n", encoding="utf-8")

    if exception is not None:
        (run_dir / "exception.txt").write_text(
            f"{type(exception).__name__}: {exception}\n", encoding="utf-8"
        )

    got_result = any(t.get("_type") == "ResultMessage" for t in transcript)
    (run_dir / "got-result.txt").write_text(("true" if got_result else "false") + "\n", encoding="utf-8")

    summary = {
        "label": label,
        "run_dir": str(run_dir),
        "prompt_chars": len(prompt),
        "transcript_msg_count": len(transcript),
        "got_result_message": got_result,
        "exception": (f"{type(exception).__name__}: {exception}" if exception else None),
        "session_id": session_id,
        "jsonl_pointer": str(jsonl_pointer_path) if session_id else None,
        "transcript_path": str(transcript_path),
        "summary_path": str(run_dir / "summary.json"),
        "started_at_path": str(started_path),
        "finished_at_path": str(finished_path),
        "debug_log_path": str(debug_log),
    }
    (run_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    log(f"run done: {run_dir.name} got_result={got_result} msgs={len(transcript)}")
    return summary


def main_sync(coro_factory) -> int:
    try:
        result = asyncio.run(coro_factory())
    except KeyboardInterrupt:
        log("interrupted by user")
        return 130
    except BaseException as exc:
        log(f"FATAL: {type(exc).__name__}: {exc}")
        return 2
    if isinstance(result, dict):
        print(json.dumps(result, indent=2))
        return 0 if result.get("got_result_message") else 1
    return 0


# ----------------------------- Output helpers --------------------------------


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def write_md(path: Path, body: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    text = body if body.endswith("\n") else body + "\n"
    path.write_text(text, encoding="utf-8")


def write_csv(path: Path, header: list[str], rows: Iterable[list[Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(header)
        for row in rows:
            writer.writerow(row)


# ----------------------------- Check record ----------------------------------


@dataclass
class CheckRecord:
    check_name: str
    status: str  # PASS, FAIL, BLOCKED
    evidence_path: str = ""
    observed_value: str = ""
    expected_value: str = ""
    failure_reason: str = ""
    blocker_reason: str = ""
    manual_verification_command: str = ""
    notes: str = ""

    def to_dict(self) -> dict[str, str]:
        return asdict(self)


def aggregate_status(records: list[CheckRecord]) -> str:
    if not records:
        return "BLOCKED"
    if any(r.status == "FAIL" for r in records):
        return "FAIL"
    if all(r.status == "PASS" for r in records):
        return "PASS"
    if any(r.status == "PASS" for r in records):
        # Mix of PASS + BLOCKED is BLOCKED unless all critical checks pass.
        return "BLOCKED"
    return "BLOCKED"


def render_check_table(records: list[CheckRecord]) -> str:
    lines = [
        "| Check | Status | Evidence | Observed | Expected | Notes |",
        "|---|---|---|---|---|---|",
    ]
    for r in records:
        lines.append(
            "| `{name}` | **{status}** | `{ev}` | {obs} | {exp} | {notes} |".format(
                name=r.check_name,
                status=r.status,
                ev=r.evidence_path or "-",
                obs=_md_cell(r.observed_value),
                exp=_md_cell(r.expected_value),
                notes=_md_cell(
                    r.failure_reason
                    or r.blocker_reason
                    or r.notes
                    or ("-" if r.status == "PASS" else "")
                ),
            )
        )
    return "\n".join(lines)


def _md_cell(value: str) -> str:
    if not value:
        return "-"
    cleaned = value.replace("|", "\\|").replace("\n", " ").strip()
    return cleaned if len(cleaned) <= 200 else cleaned[:197] + "..."


# ----------------------------- Subprocess helpers ----------------------------


def run_subprocess(cmd: list[str], cwd: Path | None = None, timeout: int = 120) -> dict[str, Any]:
    started = now_iso()
    try:
        proc = subprocess.run(
            cmd,
            cwd=str(cwd) if cwd else None,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        return {
            "cmd": cmd,
            "cwd": str(cwd) if cwd else None,
            "started_at": started,
            "finished_at": now_iso(),
            "returncode": proc.returncode,
            "stdout": proc.stdout,
            "stderr": proc.stderr,
            "timeout": False,
        }
    except subprocess.TimeoutExpired as exc:
        return {
            "cmd": cmd,
            "cwd": str(cwd) if cwd else None,
            "started_at": started,
            "finished_at": now_iso(),
            "returncode": -1,
            "stdout": exc.stdout or "",
            "stderr": (exc.stderr or "") + f"\nTIMEOUT after {timeout}s\n",
            "timeout": True,
        }
    except FileNotFoundError as exc:
        return {
            "cmd": cmd,
            "cwd": str(cwd) if cwd else None,
            "started_at": started,
            "finished_at": now_iso(),
            "returncode": 127,
            "stdout": "",
            "stderr": f"FileNotFoundError: {exc}",
            "timeout": False,
        }


def emit_subprocess_evidence(label: str, evidence_dir: Path, proc: dict[str, Any]) -> Path:
    evidence_dir.mkdir(parents=True, exist_ok=True)
    path = evidence_dir / f"{label}.json"
    path.write_text(json.dumps(proc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return path


# ----------------------------- Skill / manifest helpers ----------------------


def parse_yaml_frontmatter(text: str) -> tuple[dict[str, str], str]:
    """Tiny YAML frontmatter parser sufficient for SKILL.md (key: value pairs only)."""
    if not text.startswith("---"):
        return {}, text
    rest = text[3:]
    end = rest.find("\n---")
    if end == -1:
        return {}, text
    raw = rest[:end].strip("\n")
    body = rest[end + 4 :].lstrip("\n")
    fields: dict[str, str] = {}
    current_key: str | None = None
    for line in raw.splitlines():
        if not line.strip():
            continue
        if line.startswith((" ", "\t")) and current_key:
            fields[current_key] = (fields.get(current_key, "") + " " + line.strip()).strip()
            continue
        if ":" in line:
            key, _, value = line.partition(":")
            current_key = key.strip()
            fields[current_key] = value.strip()
    return fields, body
