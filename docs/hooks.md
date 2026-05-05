# Hooks

Orbit registers two lightweight hooks. Both are non-blocking. Neither duplicates raw transcript capture (Claude Code already stores sessions; Orbit mines them).

## `UserPromptSubmit` — durable instruction candidate detection

`scripts/hook_instruction_detector.py`:

- Reads JSON from stdin (`prompt`, `cwd`).
- Matches the prompt against `PATTERNS` (e.g. `actually`, `we decided`, `do not`, `make sure`).
- If matched: appends a compact JSONL record to `${CLAUDE_PLUGIN_DATA:-./.claude/audits/orbit-plugin-data}/intent-ledger-candidates.jsonl`.
- Record fields: `schema_version`, `timestamp`, `cwd`, `source`, `kind`, `confidence`, `prompt_excerpt`, `detected_patterns`, `requires_session_mining`, `status`.
- Independently, if the prompt looks audit-like (`audit`, `look back`, `gap analysis`, etc.) emits `additionalContext` priming so Claude leans into Orbit's workflow.

Exit code is always 0; the hook never blocks the prompt.

## `UserPromptExpansion` — workflow priming

`scripts/hook_prompt_context.py`:

- Reads JSON from stdin (`prompt`).
- If prompt mentions Orbit-relevant terms, emits `additionalContext` that summarizes Orbit's workflow ("mine existing sessions; extract user intent; compare against plans; validate against repo truth").
- Always exit 0.

## hooks.json

```json
{
  "hooks": {
    "UserPromptSubmit": [
      { "matcher": "", "hooks": [{ "type": "command", "command": "${CLAUDE_PLUGIN_ROOT}/scripts/hook_instruction_detector.py" }] }
    ],
    "UserPromptExpansion": [
      { "matcher": "", "hooks": [{ "type": "command", "command": "${CLAUDE_PLUGIN_ROOT}/scripts/hook_prompt_context.py" }] }
    ]
  }
}
```

## What the hooks do NOT do

- They do not write to stderr to block tool calls.
- They do not call back into the Anthropic API.
- They do not copy raw transcript content (Claude Code's own JSONL is the source of truth).
- They do not require Docker, network access, or any third-party dependency.

## Verification

```bash
python3 .orbit-sdk-harness/validate_hooks.py --plugin-root .
```

The validator parses `hooks.json`, confirms each command path exists and is executable, and runs each hook against a benign stdin payload to confirm exit-0 behavior.
