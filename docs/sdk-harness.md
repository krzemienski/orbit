# SDK Validation Harness

The `.orbit-sdk-harness/` directory contains a real Claude Agent SDK runner that exercises Orbit end-to-end without an interactive Claude Code session.

## Layout

```text
.orbit-sdk-harness/
  README.md
  requirements.txt              claude-agent-sdk>=0.1.68
  _common.py                    helpers (run_query, layout discovery, JSON/MD writers)
  sdk_orbit_all.py              master pipeline runner
  sdk_orbit_*.py                per-scenario runners (9 of them)
  validate_*.py                 static validators (manifest, frontmatter, hooks, commands, outputs)
  scenarios/                    14 per-scenario fixture dirs (README, prompt, expected, success criteria)
  reports/                      generated reports
  runs/                         per-run evidence (transcript, session-id, jsonl pointer, etc.)
```

## Auth

Subscription mode. Each call passes `setting_sources=["user"]` to `ClaudeAgentOptions`, so the SDK reads `~/.claude/settings.json` and uses subscription credentials. No `ANTHROPIC_API_KEY` required.

## Per-run artifacts

Every `query()` invocation writes to `runs/<UTC-timestamp>-<scenario>/`:

```text
prompt.md                      exact prompt sent to query()
transcript.json                JSON-serialized SDK message stream
session-id.txt                 session_id reported by SystemMessage / ResultMessage
jsonl-pointer.txt              ~/.claude/projects/<encoded-cwd>/<session-id>.jsonl
summary.json                   { run_id, run_dir, transcript_msg_count, got_result_message, ... }
started-at.txt                 ISO UTC start
finished-at.txt                ISO UTC finish
got-result.txt                 "true" or "false"
exception.txt                  only if the SDK stream raised
debug.log                      claude-code subprocess --debug-file output
```

The JSONL pointer is the load-bearing artifact: Orbit itself mines `~/.claude/projects/`, so the harness must verify that real session JSONL is being produced.

## Path encoding

Claude Code encodes the per-project log dir as: replace `/` and `.` with `-`, then prefix with `-`.

For run dir `/Users/nick/Desktop/orbit/.orbit-sdk-harness/runs/20260505T202306Z-plan-gap`, the JSONL pointer is:

```text
~/.claude/projects/-Users-nick-Desktop-orbit--orbit-sdk-harness-runs-20260505T202306Z-plan-gap/<session-id>.jsonl
```

## Running

```bash
# Master pipeline (all 13 scenarios + static validators + reports)
python3 .orbit-sdk-harness/sdk_orbit_all.py --plugin-root . --output .orbit-sdk-harness/reports

# Static-only (no API calls)
python3 .orbit-sdk-harness/sdk_orbit_all.py --plugin-root . --output .orbit-sdk-harness/reports --no-live-runs

# One scenario
python3 .orbit-sdk-harness/sdk_orbit_audit_gaps.py
python3 .orbit-sdk-harness/sdk_orbit_review_window.py --days 7
python3 .orbit-sdk-harness/sdk_orbit_render_dashboard.py
```

## Iron Rule

Real SDK call. Real `claude-code` subprocess. Real session JSONL. No mocks. No pre-populated transcripts. If a run produces an empty `transcript.json` or empty `session-id.txt`, that run is invalid evidence and the corresponding scenario is reported `FAIL` — never `PASS`.
