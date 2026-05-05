# Changelog

## 0.2.1

- Fixed slash command bodies hardcoded to default scope — every command now interpolates `$ARGUMENTS` so user-provided flags (`/orbit:review-window --days 7`) reach `orbit-audit`.
- Fixed intent extractor mining tool-result envelopes, `<local-command-stdout>`, `<system-reminder>`, and other non-instruction text as "user intents". New `_is_noise_text` filter rejects these; `_NOISE_MARKERS` is the exact list.
- Fixed recursive contamination — the engine now skips events whose `source_file` points at `.claude/audits/latest/` or `.claude/audits/intent-ledger`, so prior audit output is no longer mined as new intent in subsequent runs.
- Improved `validate_codebase` self-test messaging — the three default `previous_run_artifact_exists` checks now report `unverified` (severity low) on a fresh repo with a clear "first run, check again next run" message instead of a misleading `failed` status.
- Added `.claude-plugin/marketplace.json` so the plugin can be installed via `claude /plugin marketplace add krzemienski/orbit` directly from GitHub.

## 0.2.0

- Renamed product to Orbit.
- Added brand system: flat black base with lime, orange, red, purple, and blue hyper-accent colors.
- Added configurable `review-window` command.
- Kept `review-last-3-days` as a legacy alias for `review-window --days 3`.
- Defined intent → plan → claim → tool evidence → repo truth → gap flow.
- Added dashboard, evidence JSON, Markdown report, and Mermaid output requirements.
- Removed Docker and full Python package structure.
- Implemented flat Python helper scripts.
