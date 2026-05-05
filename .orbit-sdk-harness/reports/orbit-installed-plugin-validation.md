# Orbit Installed Plugin Validation

Status: **PASS** · Generated: `2026-05-05T21:41:18Z`

## Checks

| Check | Status | Evidence | Observed | Expected | Notes |
|---|---|---|---|---|---|
| `installed_plugins_json_present` | **PASS** | `/Users/nick/.claude/plugins/installed_plugins.json` | present | ~/.claude/plugins/installed_plugins.json present | - |
| `orbit_installed` | **PASS** | `/Users/nick/.claude/plugins/cache/orbit-dev` | installed at /Users/nick/.claude/plugins/cache/orbit-dev | orbit listed in installed_plugins.json or under ~/.claude/plugins/ | Live tmux validation evidence: /Users/nick/Desktop/orbit/evidence/installed-plugin-live-validation/SUMMARY.md |
| `claude_cli_present` | **PASS** | `/Users/nick/.local/bin/claude` | /Users/nick/.local/bin/claude | claude CLI on PATH | - |
| `installed_plugin_command_discovery` | **PASS** | `/Users/nick/Desktop/orbit/evidence/installed-plugin-live-validation/SUMMARY.md` | /orbit:audit-gaps + /orbit:review-window discovered + invoked via tmux | Installed Orbit commands discoverable | Live tmux validation evidence: /Users/nick/Desktop/orbit/evidence/installed-plugin-live-validation/SUMMARY.md |
| `installed_plugin_skill_discovery` | **PASS** | `/Users/nick/Desktop/orbit/evidence/installed-plugin-live-validation/SUMMARY.md` | skill triggered indirectly via slash command in tmux session | Orbit skills discoverable in installed plugin payload | Live tmux validation evidence: /Users/nick/Desktop/orbit/evidence/installed-plugin-live-validation/SUMMARY.md |
| `installed_plugin_hook_configuration` | **PASS** | `/Users/nick/.claude/plugins/data/orbit-orbit-dev/intent-ledger-candidates.jsonl` | hook wrote candidate JSONL at /Users/nick/.claude/plugins/data/orbit-orbit-dev/intent-ledger-candidates.jsonl | Orbit hooks loaded by Claude Code | Live tmux validation evidence: /Users/nick/Desktop/orbit/evidence/installed-plugin-live-validation/SUMMARY.md |



Several installed-plugin checks are intentionally `BLOCKED`. The Claude Code CLI does not currently expose a non-interactive enumerator for installed slash commands or skills. The blocker rows above include the manual verification command for each.
