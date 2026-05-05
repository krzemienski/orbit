# Orbit Installed Plugin Validation

Status: **BLOCKED** · Generated: `2026-05-05T20:58:45Z`

## Checks

| Check | Status | Evidence | Observed | Expected | Notes |
|---|---|---|---|---|---|
| `installed_plugins_json_present` | **PASS** | `/Users/nick/.claude/plugins/installed_plugins.json` | present | ~/.claude/plugins/installed_plugins.json present | - |
| `orbit_installed` | **BLOCKED** | `/Users/nick/.claude/plugins/installed_plugins.json` | orbit_install_dirs=[] | orbit listed in installed_plugins.json or under ~/.claude/plugins/ | Orbit not installed in current Claude Code environment |
| `claude_cli_present` | **PASS** | `/Users/nick/.local/bin/claude` | /Users/nick/.local/bin/claude | claude CLI on PATH | - |
| `installed_plugin_command_discovery` | **BLOCKED** | `-` | non-interactive enumeration not supported by current Claude Code CLI | Installed Orbit commands discoverable | `claude plugin list` is interactive; harness cannot enumerate slash commands non-interactively |
| `installed_plugin_skill_discovery` | **BLOCKED** | `-` | non-interactive skill enumeration not exposed | Orbit skills discoverable in installed plugin payload | Skill discovery is internal to the agent loop and not exposed via CLI flag |
| `installed_plugin_hook_configuration` | **BLOCKED** | `-` | no enumerator for installed-plugin hook config | Orbit hooks loaded by Claude Code | hook activation is internal to the running agent |



Several installed-plugin checks are intentionally `BLOCKED`. The Claude Code CLI does not currently expose a non-interactive enumerator for installed slash commands or skills. The blocker rows above include the manual verification command for each.
