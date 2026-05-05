# Documentation Research Summary

Run ID: `20260505T202306Z`
Generated: `2026-05-05T20:34:11Z`

This research used **only locally available material** — installed Python packages, the Orbit project files, and Claude Code's on-disk configuration. No remote fetches were performed; the harness must run offline.

## Source 1 — `claude-agent-sdk` (Python)

- Local path: the import location of the installed `claude_agent_sdk` package (`python3 -c "import claude_agent_sdk; print(claude_agent_sdk.__file__)"`).
- Version: `0.1.68` (matches `.orbit-sdk-harness/requirements.txt`).
- Verified by: `python3 -c "from claude_agent_sdk import query, ClaudeAgentOptions; from claude_agent_sdk.types import ResultMessage, SystemMessage, AssistantMessage, UserMessage; print('IMPORTS_OK')"` (returns `0.1.68\nIMPORTS_OK`).

Cited facts (≥3):

1. `query()` is the entry point for the streaming agent loop; the harness consumes its async iterator of messages.
2. `ClaudeAgentOptions` accepts `setting_sources`, `cwd`, `permission_mode`, `max_turns`, and an `extra_args` dict (the harness uses `extra_args={"debug-file": str(...)}` to capture the SDK debug log).
3. Subscription-mode auth is selected by `setting_sources=["user"]` so the SDK reads `~/.claude/settings.json`; no `ANTHROPIC_API_KEY` is required.
4. Substantive completion is signaled by a `ResultMessage` in the stream; absence of `ResultMessage` is treated as failure (`got-result.txt = false`).
5. Each `query()` invocation produces a per-project session JSONL at `~/.claude/projects/<encoded-cwd>/<session-id>.jsonl` (encoding rule: replace `/` and `.` with `-`, prefix with `-`).

## Source 2 — Claude Code plugin manifest contract

- Local path: `/Users/nick/Desktop/orbit/.claude-plugin/plugin.json`.
- Verified by: `python3 .orbit-sdk-harness/validate_plugin_manifest.py --plugin-root .` (exits 0; PASS on every check).

Cited facts:

1. The manifest must live at `.claude-plugin/plugin.json` relative to the plugin root.
2. The manifest is a JSON object with required `name` field; recognized sub-path keys include `skills`, `commands`, `hooks`, `agents`, `mcps`.
3. The `hooks` field is a path to a JSON file (`./hooks/hooks.json` in Orbit), while `skills` and `commands` are paths to directories (`./skills`, `./commands`).
4. Orbit's manifest declares `name: "orbit"`, `version: "0.2.0"`, `description: "Mines local Claude Code session transcripts..."`.

## Source 3 — Claude Code hook I/O contract

- Local path: `/Users/nick/Desktop/orbit/hooks/hooks.json` and `scripts/hook_*.py`.
- Verified by: `python3 .orbit-sdk-harness/validate_hooks.py --plugin-root .` (exits 0; smoke runs each hook with stdin payload).

Cited facts:

1. Each hook reads JSON from stdin and exits 0 on success; non-zero exit is reserved for blocking-style behavior (Orbit never blocks).
2. Hooks may emit JSON on stdout under `hookSpecificOutput.additionalContext` for non-blocking context injection (observed in `hook_prompt_context.py`).
3. Deprecated patterns (`{"decision": "block"}`, `{"decision": "approve"}`) are NOT used by Orbit; Orbit uses `additionalContext` for soft hints and silence for non-matches.
4. Recognized event names: `UserPromptSubmit`, `UserPromptExpansion`, `PreToolUse`, `PostToolUse`, `SessionStart`, `Stop`, `SubagentStart`, `SubagentStop`, `Notification`.
5. Hook commands in `hooks.json` are interpolated with `${CLAUDE_PLUGIN_ROOT}` at load time (verified by `validate_hooks.py::_expand`).

## Source 4 — Skill YAML frontmatter contract

- Local path: `/Users/nick/Desktop/orbit/skills/<name>/SKILL.md`.
- Verified by: `python3 .orbit-sdk-harness/validate_skill_frontmatter.py --skills-dir ./skills` (exits 0; per-skill PASS).

Cited facts:

1. Frontmatter is delimited by `---` on its own line; the body follows immediately after the closing delimiter.
2. Required keys: `name` (lowercase, digits, hyphens; ≤ 64 chars) and `description` (non-empty, no XML tags, ≤ 1024 chars).
3. The body must be non-empty and describes the operational workflow (`workflow`, `rule`, `contract`, or `outputs` keywords expected for completeness scoring).
4. Frontmatter `name` should match the parent directory name (`gap-analysis/SKILL.md` declares `name: gap-analysis`).

## Source 5 — Slash command file format

- Local path: `/Users/nick/Desktop/orbit/commands/<name>.md`.
- Verified by: `python3 .orbit-sdk-harness/validate_commands.py --plugin-root .` (exits 0; per-command PASS).

Cited facts:

1. Filename stem becomes the slash command (`audit-gaps.md` → `/orbit:audit-gaps`).
2. File body is the slash command body — a leading markdown heading plus usage example fenced blocks.
3. No frontmatter is required for slash commands in Orbit (none of Orbit's eight commands declare frontmatter).
4. Orbit conventions: each command file mentions `orbit-audit` (the helper) or a skill name so the invocation is unambiguous.
5. `review-window` documents `--days`, `--since`, `--from`, `--to` flags (verified by validator); `review-last-3-days` documents itself as alias for `--days 3`.

## GitHub / external context boundary

GitHub was NOT consulted as the source of truth. The harness explicitly prefers local code and observed runtime artifacts over remote-repository assumptions. Where official documentation would be helpful but is offline-unavailable, the harness records `BLOCKED` rather than fabricating content.

## Verification fingerprint

```text
$ python3 -c "import claude_agent_sdk; print(claude_agent_sdk.__version__)"
0.1.68
$ which claude
/Users/nick/.local/bin/claude
$ claude --version
2.1.128 (Claude Code)
$ python3 .orbit-sdk-harness/validate_plugin_manifest.py --plugin-root .  # → status PASS
$ python3 .orbit-sdk-harness/validate_skill_frontmatter.py                 # → status PASS
$ python3 .orbit-sdk-harness/validate_hooks.py --plugin-root .             # → status PASS
$ python3 .orbit-sdk-harness/validate_commands.py --plugin-root .          # → status PASS
$ python3 .orbit-sdk-harness/validate_outputs.py --plugin-root .           # → status PASS
```
