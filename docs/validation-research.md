# Validation Research

This file documents the documentation sources consulted before writing the Orbit validation harness. Local sources are preferred; the harness is offline-friendly.

## Sources used

### `claude-agent-sdk` (Python)

- **Path:** the import location of the locally installed package (`python3 -c "import claude_agent_sdk; print(claude_agent_sdk.__file__)"`).
- **Version:** `claude-agent-sdk==0.1.68` per `requirements.txt`.
- **Facts derived by importing and reading the package:**
  - `query()` is the entry point for streaming agent messages.
  - `ClaudeAgentOptions` carries `setting_sources`, `cwd`, `permission_mode`, `max_turns`, and an `extra_args` dict for forwarding `--debug-file`.
  - Subscription-mode auth is selected by passing `setting_sources=["user"]` so Claude Code reads `~/.claude/settings.json`.
  - Substantive completion is signaled by a `ResultMessage` in the message stream; absence of `ResultMessage` is treated as failure.

### Claude Code plugin manifest

- **Source of truth:** the local `.claude-plugin/plugin.json` for Orbit, validated by `validate_plugin_manifest.py`.
- **Facts:**
  - The manifest path is `.claude-plugin/plugin.json` relative to the plugin root.
  - The manifest is a JSON object.
  - Recognized sub-path keys include `skills`, `commands`, `hooks`, `agents`, `mcps`.
  - The `hooks` field points at `hooks/hooks.json` (a file), while `skills`/`commands` point at directories.

### Claude Code hook I/O

- **Source of truth:** the local `hooks/hooks.json` and `scripts/hook_*.py` files.
- **Facts:**
  - Each hook reads JSON from stdin and exits 0 on success.
  - Hooks may emit JSON on stdout under `hookSpecificOutput.additionalContext` for non-blocking context injection.
  - Blocking patterns (`{decision: "block"}` / `"approve"`) are deprecated; Orbit uses `additionalContext` instead.
  - Recognized event names include `UserPromptSubmit`, `UserPromptExpansion`, `PreToolUse`, `PostToolUse`, `SessionStart`, `Stop`, `SubagentStart`, `SubagentStop`, `Notification`.

### Skill YAML frontmatter

- **Source of truth:** the four local `SKILL.md` files, validated by `validate_skill_frontmatter.py`.
- **Facts:**
  - Frontmatter is delimited by `---` lines.
  - Required keys are `name` and `description`.
  - `name` is `^[a-z0-9-]+$` and ≤ 64 chars.
  - `description` is plain text, no XML tags, ≤ 1024 chars.

### Slash command file format

- **Source of truth:** the eight local `commands/*.md` files, validated by `validate_commands.py`.
- **Facts:**
  - Filename stem becomes the slash command (`audit-gaps.md` → `/orbit:audit-gaps`).
  - File body is the slash command body (heading + usage examples).
  - No frontmatter is required for slash commands in Orbit.

## Boundary

GitHub was NOT assumed to be the source of truth. The local Orbit project filesystem is the source of truth. Where remote docs would be helpful but are not available offline, the harness records `BLOCKED` rather than fabricating content.
