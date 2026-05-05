# Reports

`sdk_orbit_all.py` writes 13 reports under `.orbit-sdk-harness/reports/`:

| Report | Purpose |
|---|---|
| `orbit-validation-summary.md` | Executive summary with every section and final verdict |
| `orbit-validation-results.json` | Machine-readable check-by-check results + payloads |
| `orbit-architecture-discovery.md` | Local architecture map + per-check status |
| `orbit-plugin-compliance.md` | Static validator roll-up |
| `orbit-installed-plugin-validation.md` | Installed-plugin checks (with BLOCKED rows + manual commands) |
| `orbit-skill-compliance.md` | Frontmatter validator detail |
| `orbit-command-compliance.md` | Command markdown audit |
| `orbit-hook-compliance.md` | Hooks.json + per-hook smoke detail |
| `orbit-docs-compliance.md` | Markdown + HTML + diagram completeness |
| `orbit-skill-creator-review.md` | Per-skill scoring under the Skill Creator rubric |
| `orbit-scenario-matrix.csv` | One row per SDK scenario with status + evidence path |
| `orbit-dashboard-verification.md` | Dashboard token-by-token verification |
| `orbit-final-pass-fail.md` | Section-level PASS/FAIL/BLOCKED roll-up + overall |

## Reading the summary

`orbit-validation-summary.md` always contains:

- Generated timestamp, plugin root, overall status.
- Section status table (8 sections).
- Architecture discovery reference.
- Documentation research source list.
- Per-section status with evidence paths.
- Test prompts used (per-run `prompt.md` references).
- Observed artifact list (`transcript.json`, `session-id.txt`, `jsonl-pointer.txt`, etc.).
- Known failures (from FAIL rows).
- Blocked checks with manual verification commands.
- Recommended fixes.
- Final pass/fail.

## Evidence rules

Every PASS in every report cites a real evidence path. Every FAIL cites the same. Every BLOCKED cites the manual verification command needed to resolve the block. There are no rows without evidence references.
