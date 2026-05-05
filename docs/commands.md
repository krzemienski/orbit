# Slash Commands

Orbit ships eight slash commands. Each one is a thin wrapper around `bin/orbit-audit` with a documented purpose and at least one usage example.

| Command | CLI helper | Purpose |
|---|---|---|
| `/orbit:audit-gaps` | `orbit-audit audit ... --dashboard --validate-codebase` | Full gap analysis with dashboard |
| `/orbit:mine-intent` | `orbit-audit build-ledger ... --days 30` | Append durable instructions to the ledger |
| `/orbit:validate-claims` | `orbit-audit validate-claims --evidence ...` | Re-validate existing evidence |
| `/orbit:render-dashboard` | `orbit-audit render-dashboard --evidence ...` | Re-render `dashboard.html` |
| `/orbit:compare-plan` | `orbit-audit compare-plan --plan PLAN.md ...` | Plan vs. sessions + repo state |
| `/orbit:review-window` | `orbit-audit audit --days/--since/--from/--to ...` | Configurable lookback window |
| `/orbit:review-last-3-days` | `orbit-audit audit --days 3 ...` | Legacy alias for `--days 3` |
| `/orbit:rebuild-ledger` | `orbit-audit build-ledger --replace --all` | Replace ledger by re-mining sessions |

## Review window flag matrix

| Flag | Effect |
|---|---|
| _no flag_ | Default `--days 3` |
| `--days N` | Last N days (mtime filter) |
| `--since YYYY-MM-DD` | From a specific date through now |
| `--from YYYY-MM-DD --to YYYY-MM-DD` | Explicit closed window |

`--from` and `--to` are also accepted as `--start`/`--end` shadow attrs in the parser (see `scripts/orbit_audit.py` lines 616-617).

## Compliance

Every command is verified by `validate_commands.py`:
- markdown body non-empty
- markdown leading heading
- at least one fenced example block
- helper or skill mapping (`orbit-audit` or `skill` mentioned)
- `review-window` documents `--days`, `--since`, `--from`, `--to`
- `review-last-3-days` documents itself as alias for `--days 3`
