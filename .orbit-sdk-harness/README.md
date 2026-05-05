# Orbit SDK Harness

Real Claude Agent SDK harness for validating the **Orbit** plugin from outside an interactive Claude Code session. No mocks. No fake transcripts. No synthetic pass results. Every byte in the captured evidence comes from a live `claude_agent_sdk.query()` invocation against subscription-mode Claude Code on the local machine.

## What this validates

Orbit is a Claude Code plugin (located at the repository root) for intent mining, gap analysis, claim validation, codebase truth checks, remediation recommendations, and dashboard rendering. This harness exercises:

1. The plugin **as files on disk** (manifest, skills, commands, hooks, bin wrappers, helper scripts).
2. The plugin **as installed Claude Code behavior** (slash commands and skill discovery, when feasible to query non-interactively).
3. The plugin **as runtime** (real `query()` against the live agent loop, with the resulting JSONL session log mined as Orbit's own load-bearing evidence).

## Authentication

Subscription-mode. Each script passes `setting_sources=["user"]` so Claude Code reads `~/.claude/settings.json` and uses subscription credentials. No `ANTHROPIC_API_KEY` needed.

## Layout

```text
.orbit-sdk-harness/
  README.md                            this file
  requirements.txt                     pinned: claude-agent-sdk>=0.1.68
  _common.py                           shared helpers (run_harness, JSON/MD writers, plugin detection)
  sdk_orbit_all.py                     master runner (compliance + scenarios + reports)
  sdk_orbit_audit_gaps.py              scenario 01 wrapper (plan gap)
  sdk_orbit_review_window.py           scenario 06 wrapper (configurable window)
  sdk_orbit_mine_intent.py             scenario 09 wrapper (instruction ledger)
  sdk_orbit_validate_claims.py         scenario 03 wrapper (claim unverified)
  sdk_orbit_compare_plan.py            scenario 02 wrapper (correction supersedes)
  sdk_orbit_render_dashboard.py        scenario 05 wrapper (dashboard required)
  sdk_orbit_hook_candidate.py          scenario 07 wrapper (hook candidate)
  sdk_orbit_plugin_compliance.py       scenario 10 wrapper (plugin packaging)
  sdk_orbit_skill_compliance.py        scenario 11 wrapper (skill creator review)
  sdk_orbit_docs_compliance.py         scenario 12 wrapper (docs completeness)
  validate_skill_frontmatter.py        static: YAML frontmatter validator
  validate_plugin_manifest.py          static: plugin.json validator
  validate_hooks.py                    static + smoke: hooks.json + hook script JSON I/O
  validate_commands.py                 static: command markdown coverage
  validate_outputs.py                  static + smoke: orbit-audit subcommand outputs
  scenarios/                           per-scenario READMEs, prompts, expected obs, success criteria
  reports/                             generated reports (markdown, JSON, CSV)
  runs/                                generated per-run evidence dirs (transcript.json etc.)
```

## Running

```bash
# Install SDK
python3 -m pip install -r .orbit-sdk-harness/requirements.txt

# Master pipeline
python3 .orbit-sdk-harness/sdk_orbit_all.py --plugin-root . --output .orbit-sdk-harness/reports

# Individual scenario
python3 .orbit-sdk-harness/sdk_orbit_audit_gaps.py
python3 .orbit-sdk-harness/sdk_orbit_review_window.py --days 7
python3 .orbit-sdk-harness/sdk_orbit_mine_intent.py
```

## Per-run evidence (Iron Rule)

Each `query()` invocation writes to `runs/<UTC-timestamp>-<scenario>/` and captures:

```text
prompt.md           the exact prompt sent to query()
transcript.json     all messages emitted by the SDK, JSON-serialized
session-id.txt      session_id reported by SystemMessage / ResultMessage
jsonl-pointer.txt   ~/.claude/projects/<encoded-cwd>/<session-id>.jsonl
summary.json        run metadata (got_result_message, transcript_msg_count, paths)
started-at.txt      ISO UTC start time
finished-at.txt     ISO UTC finish time
got-result.txt      "true" if a ResultMessage arrived, else "false"
exception.txt       only if the SDK stream raised
debug.log           SDK debug log (--debug-file)
```

Path encoding rule for the JSONL pointer (matches Claude Code on macOS/Linux):
replace `/` and `.` with `-`, prefix with `-`. Example:
`/Users/nick/Desktop/orbit/.orbit-sdk-harness/runs/20260505T202306Z-plan-gap`
becomes
`-Users-nick-Desktop-orbit--orbit-sdk-harness-runs-20260505T202306Z-plan-gap`.

## Iron Rule

Real SDK call. Real claude-code subprocess (the SDK launches one in-process). Real session JSONL written to `~/.claude/projects/`. No mocks. No `requests.post`. No pre-populated transcripts. If a run produces empty `transcript.json` or empty `session-id.txt`, that run is invalid evidence and must be re-executed; the harness will mark it `FAIL`, never `PASS`.

## Reports

After `sdk_orbit_all.py` completes, the following are written under `reports/`:

```text
orbit-validation-summary.md
orbit-validation-results.json
orbit-architecture-discovery.md
orbit-plugin-compliance.md
orbit-installed-plugin-validation.md
orbit-skill-compliance.md
orbit-command-compliance.md
orbit-hook-compliance.md
orbit-docs-compliance.md
orbit-skill-creator-review.md
orbit-scenario-matrix.csv
orbit-dashboard-verification.md
orbit-final-pass-fail.md
```

Every line in every report cites a real evidence path under `runs/`, `reports/`, or the local Orbit codebase.
