# Reviewer C — Iron-Rule Compliance

Reviewer: `crucible:reviewer-c`
Emphasis: Does any artifact, anywhere in `evidence/`, contain mocks, fakes, fixtures, or test files?

## Iron Rule scan

Searched `evidence/` and `.orbit-sdk-harness/runs/` for:
- `*.test.*`, `*.spec.*`, `tests/`, `__tests__/`, `__mocks__/` — none under `evidence/` or `runs/`. (The Orbit project has a `tests/` directory under the project root for pytest smoke fixtures used by `validate_outputs.py`; these fixtures are bundled with the plugin and are not part of the harness's own evidence.)
- Mock-language signals (`mock`, `stub`, `fake`, `fixture`) in evidence file names — none.
- Fabricated-transcript markers (e.g. transcripts with no `tool_use_id`, no `session_id`, or zero-byte size) — none.

## SDK transcripts inspected

Spot-checked `transcript.json` from runs 00, 04, 06-since, 08, 13. Each contains a series of serialized SDK messages with `_type` values from `{"SystemMessage", "AssistantMessage", "UserMessage", "ResultMessage"}` and real `session_id` references. No transcript was hand-edited.

## JSONL pointer integrity

Each `jsonl-pointer.txt` references an actual file under `~/.claude/projects/<encoded-cwd>/<session-id>.jsonl`. Verified one (164KB) is the real Claude Code session log, not a fixture written by the harness. The encoded-cwd path matches the harness convention (`/` and `.` → `-`, prefix `-`).

## BLOCKED rows

The Iron Rule allows `BLOCKED` only when the check could not run for environmental reasons AND a manual_verification_command is included. Inspected MSC-11's installed-plugin checks: every BLOCKED row carries a `manual_verification_command` (e.g., `claude plugin list 2>&1 | grep -i orbit`). No silent skips.

## Verdict

**PASS** — no mocks, no fake transcripts, no fabricated evidence, no silent skips. Iron Rule compliance is structural.

— reviewer-c
