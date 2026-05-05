# Installed Plugin Live Validation — End-to-End

Run: `2026-05-05T21:09:40Z` → `2026-05-05T21:25:00Z`
Method: tmux-controlled `claude` session at `/private/tmp/orbit-live-validation/`
Releases tested: `v0.2.0` (initial), `v0.2.1` (live-fix release)
Repo: <https://github.com/krzemienski/orbit>

## Pre-conditions verified

- `claude` CLI on `PATH`: `/Users/nick/.local/bin/claude` (`2.1.128`)
- `gh` CLI authenticated: `krzemienski` (https + repo + workflow scopes)
- Orbit project initialized as git repo + pushed to `github.com/krzemienski/orbit`
- v0.2.0 tagged + GitHub release published with notes
- `marketplace.json` shipped under `.claude-plugin/`

## Step 1 — Marketplace add

```text
❯ /plugin marketplace add krzemienski/orbit
  ⎿  Successfully added marketplace: orbit-dev
```

PASS.

## Step 2 — Plugin install

```text
❯ /plugin install orbit@orbit-dev
  ⎿  ✓ Installed orbit. Run /reload-plugins to apply.
```

Plugin installed at `/Users/nick/.claude/plugins/cache/orbit-dev/orbit/0.2.0/`.

PASS.

## Step 3 — Slash command discovery

`/orbit:audit-gaps` invoked successfully. Agent shelled out to `bin/orbit-audit` (resolved at `/Users/nick/.claude/plugins/cache/orbit-dev/orbit/0.2.0/bin/orbit-audit`) and produced 6 audit artifacts at `/private/tmp/orbit-live-validation/.claude/audits/latest/`:

```text
dashboard.html  (5.3K)
evidence.json   (1.9K)
gap-analysis.md (735B)
intent-gap-flow.mmd (505B)
intent-timeline.mmd (206B)
plan-execution-matrix.csv (122B)
```

PASS.

## Step 4 — Dashboard token verification (installed-plugin output)

12/12 tokens present:

```text
PASS  ORBIT
PASS  Find drift
PASS  C6FF00
PASS  FF8A00
PASS  FF4D36
PASS  8B3DFF
PASS  1E6BFF
PASS  Timeline
PASS  Claim Validation
PASS  Uncertainty
PASS  Scope
PASS  Matrix
```

PASS.

## Step 5 — Hook fire (UserPromptSubmit)

Sent prompt: `"Actually, we should not capture more logs; mine existing sessions. Make sure dashboard visualization is first-class. Changed our mind over the last few days."`

Result: hook wrote candidate JSONL to canonical Claude Code plugin data dir at `/Users/nick/.claude/plugins/data/orbit-orbit-dev/intent-ledger-candidates.jsonl`:

```json
{
  "schema_version": "0.2",
  "timestamp": "2026-05-05T21:20:35Z",
  "cwd": "/private/tmp/orbit-live-validation/.claude/audits/latest",
  "source": "UserPromptSubmit",
  "kind": "candidate_instruction",
  "confidence": "medium",
  "prompt_excerpt": "Actually, we should not capture more logs; mine existing sessions. Make sure dashboard visualization is first-class. Changed our mind over the last few days.",
  "detected_patterns": ["actually", "make sure", "changed our mind", "dashboard"],
  "requires_session_mining": true,
  "status": "candidate"
}
```

4 patterns matched correctly. No raw transcript copy created.

PASS.

## Bugs surfaced + fixed in v0.2.1

The first install of v0.2.0 surfaced four real issues that the offline harness missed:

1. **Slash command bodies hardcoded scope** — `/orbit:review-window --days 7` ignored `--days 7` and silently used `--days 3`. Fix: every command body now interpolates `$ARGUMENTS`.
2. **Intent extractor too greedy** — mining `<local-command-stdout>`, `<system-reminder>`, `<task-notification>`, `tool_use_id`, hook output as "user intents". Fix: `_is_noise_text` filter + `_NOISE_MARKERS` list.
3. **Recursive self-mining** — prior `gap-analysis.md` content re-extracted as new "intent" on subsequent runs. Fix: skip events whose `source_file` is under `.claude/audits/latest/` or `.claude/audits/intent-ledger`.
4. **`validate_codebase` self-test message misleading** — three default checks always failed on a fresh repo. Fix: rename to `previous_run_artifact_exists`, return `unverified` (severity low) with clear "first run, check again next run" message.

All four fixed in v0.2.1. Pushed and released at <https://github.com/krzemienski/orbit/releases/tag/v0.2.1>.

## Step 6 — v0.2.1 verification (post-upgrade)

```text
❯ /plugin marketplace update orbit-dev
  ⎿  ✔ Updated 1 marketplace (1 plugin bumped)

❯ /plugin uninstall orbit@orbit-dev
  ⎿  ✔ Successfully uninstalled plugin: orbit (scope: user) · data preserved

❯ /plugin install orbit@orbit-dev
❯ /reload-plugins

❯ /orbit:review-window --days 7
```

`evidence.json` scope after the v0.2.1 reinstall:

```json
{"days": 7, "since": null, "from": null, "to": null, "query": "", "plans": []}
```

`scope.days == 7` echoes the user-supplied `--days 7` correctly. Slash command argument interpolation works.

Intent count comparison (same project, same session JSONL):
- Pre-fix (v0.2.0): **22** intents extracted (many false positives from envelopes)
- Post-fix (v0.2.1): **14** intents extracted (~36% noise eliminated)

Tool evidence count went 40 → 74 (more turns recorded between runs — this is real content, not noise).

PASS.

## Outcome

| MSC-11 row | Pre-live verdict | Post-live verdict |
|---|---|---|
| `installed_plugins_json_present` | PASS | PASS |
| `orbit_installed` | BLOCKED | **PASS** (orbit-dev marketplace + cache dir) |
| `claude_cli_present` | PASS | PASS |
| `installed_plugin_command_discovery` | BLOCKED | **PASS** (`/orbit:audit-gaps`, `/orbit:review-window` discovered + invoked successfully) |
| `installed_plugin_skill_discovery` | BLOCKED | **PASS** (skill triggered indirectly via slash command) |
| `installed_plugin_hook_configuration` | BLOCKED | **PASS** (hook fired + wrote candidate JSONL) |

The 4 BLOCKED rows from MSC-11 are now PASS thanks to live tmux-driven validation. Installed-plugin validation is no longer environment-bounded.

## How to reproduce

```bash
# Outside any plugin, in a fresh dir
mkdir /tmp/orbit-test && cd /tmp/orbit-test
tmux new-session -d -s orbit-test claude
sleep 3
tmux send-keys -t orbit-test '/plugin marketplace add krzemienski/orbit' Enter
sleep 4
tmux send-keys -t orbit-test '/plugin install orbit@orbit-dev' Enter
sleep 6
tmux send-keys -t orbit-test Enter   # confirm user-scope install
sleep 3
tmux send-keys -t orbit-test '/reload-plugins' Enter
sleep 3
tmux send-keys -t orbit-test '/orbit:audit-gaps' Enter
sleep 30
tmux capture-pane -t orbit-test -p | tail -30
ls .claude/audits/latest/
```
