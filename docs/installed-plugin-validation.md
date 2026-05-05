# Installed Plugin Validation

This is the validation surface that asks: "is Orbit actually loaded into the user's Claude Code environment?" — not just "are the files on disk correct?"

## What can be checked non-interactively

| Check | Method |
|---|---|
| `claude` CLI on PATH | `shutil.which("claude")` |
| `~/.claude/plugins/installed_plugins.json` exists | filesystem |
| Orbit referenced in installed-plugins payload | parse the JSON, search for `"orbit"` (case-insensitive) |
| Orbit install dir under `~/.claude/plugins/` | filesystem walk |
| Local plugin path resolves | `discover_layout()` |

## What is BLOCKED non-interactively

| Check | Why BLOCKED | Manual verification |
|---|---|---|
| Slash command discovery | Claude Code CLI does not enumerate installed slash commands non-interactively | `claude` then type `/orbit:audit-gaps` |
| Skill discovery | Skill discovery is internal to the agent loop | `claude` then type a trigger phrase like "audit this project for gaps" |
| Hook configuration | Hook activation is internal to the running agent | `cat ~/.claude/plugins/installed_plugins.json` and inspect `hooks` array; or `cat ~/.claude/settings.json` |
| Bin wrapper resolution from installed context | Requires running the installed plugin inside Claude Code | invoke `bin/orbit-audit` from inside `claude` shell with `${CLAUDE_PLUGIN_ROOT}` set |

## Discipline

- Every BLOCKED row in the report must include a manual verification command.
- BLOCKED is not silently upgraded to PASS.
- The harness never destructively installs or modifies the user's Claude Code plugin index.
- If the user wants to install Orbit from the local path, they run their own preferred install flow; the harness only inspects the result.

## Evidence

`reports/orbit-installed-plugin-validation.md` lists every check with status + evidence path + manual verification command for each BLOCKED row. `reports/orbit-validation-results.json` contains the same data in JSON.
