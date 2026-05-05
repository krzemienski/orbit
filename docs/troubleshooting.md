# Troubleshooting

## Symptoms and resolutions

### `claude_agent_sdk` import fails

```
ImportError: No module named 'claude_agent_sdk'
```

Install: `python3 -m pip install -r .orbit-sdk-harness/requirements.txt`. Verify with `python3 -c "from claude_agent_sdk import query; print('ok')"`.

### `validate_outputs.py` reports `dashboard_token_*FAIL`

The dashboard renderer is missing a section. Confirm `scripts/orbit_audit.py::render_dashboard()` includes hero (with scope chip), summary cards, matrix, intent timeline, claim validation, gaps, uncertainty. Re-run after the fix.

### `validate_hooks.py` reports `hook_command_executable_*FAIL`

```bash
chmod +x scripts/hook_instruction_detector.py scripts/hook_prompt_context.py
```

### SDK runner exits 1 with no `transcript.json`

The `query()` stream raised before any message arrived. Check `runs/<id>/exception.txt` for the underlying error. Common causes: subscription auth not configured, `~/.claude/settings.json` missing, network issue.

### Scenario reports `got_result=false`

The SDK stream completed without a `ResultMessage`. This is treated as `FAIL`. Re-run the single scenario (`python3 .orbit-sdk-harness/sdk_orbit_<name>.py`) and inspect `runs/<id>/transcript.json` for the message types received.

### Installed-plugin validation reports `BLOCKED` for slash command discovery

This is expected. The Claude Code CLI does not currently expose a non-interactive enumerator for installed slash commands. Use the manual command from the BLOCKED row.

### `evidence.json` `intents` is empty even though sessions exist

Check `scope`. If `--days 3` is used but the relevant sessions are older than 3 days, no events match the mtime filter. Use `--since` or `--from`/`--to`.

### Dashboard opens but shows no gaps

`gap-analysis.md` always emits at least one `ambiguous-evidence` gap if the audit found no intents/plans/claims. If the dashboard is empty in real usage, broaden the time window or point Orbit to the correct session root with `--session-root`.

## Where evidence lives

| Artifact | Path |
|---|---|
| Per-run audit | `.claude/audits/latest/` |
| Durable ledger | `.claude/audits/intent-ledger.{jsonl,md}` |
| Per-prompt hook candidate | `${CLAUDE_PLUGIN_DATA:-./.claude/audits/orbit-plugin-data}/intent-ledger-candidates.jsonl` |
| SDK harness runs | `.orbit-sdk-harness/runs/<id>/` |
| SDK harness reports | `.orbit-sdk-harness/reports/` |
| Crucible evidence | `evidence/` (forge phases) |
