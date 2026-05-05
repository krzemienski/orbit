# Expected Observations

- The agent identifies `.claude-plugin/plugin.json` as the manifest.
- The agent enumerates the four skills: `gap-analysis`, `instruction-ledger`, `plan-execution-audit`, `validation-pairing`.
- The agent enumerates at least the eight required slash commands.
- The agent identifies `scripts/orbit_audit.py` as the engine and the three `bin/orbit-*` wrappers as thin shims.
- The agent identifies `.claude/audits/latest/` as the per-run output directory.
- The agent declares any unknowns instead of fabricating answers.
