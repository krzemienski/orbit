from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "orbit_audit.py"
FIXTURES = ROOT / "tests" / "fixtures"


def test_compile_script():
    result = subprocess.run([sys.executable, "-m", "py_compile", str(SCRIPT)], capture_output=True, text=True)
    assert result.returncode == 0, result.stderr


def test_audit_smoke(tmp_path: Path):
    out = tmp_path / "audit"
    result = subprocess.run([
        sys.executable, str(SCRIPT), "audit",
        "--project", str(FIXTURES / "sample-repo"),
        "--plans", str(FIXTURES / "sample-plan.md"),
        "--sessions", str(FIXTURES / "sample-session.jsonl"),
        "--validate-codebase",
        "--output", str(out),
    ], capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    assert (out / "evidence.json").exists()
    assert (out / "dashboard.html").exists()
    evidence = json.loads((out / "evidence.json").read_text())
    assert evidence["intents"]
    assert evidence["gaps"]


def test_ledger_smoke(tmp_path: Path):
    out = tmp_path / "intent-ledger.jsonl"
    result = subprocess.run([
        sys.executable, str(SCRIPT), "build-ledger",
        "--project", str(FIXTURES / "sample-repo"),
        "--sessions", str(FIXTURES / "sample-session.jsonl"),
        "--output", str(out),
        "--replace",
    ], capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    assert out.exists()
    assert "plug-and-play plugin" in out.read_text()
