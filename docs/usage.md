# Using Orbit

Orbit answers questions like:

- "What did we miss in the last week?"
- "Did the assistant actually do what it claimed?"
- "Does the current code reflect the latest user instructions?"
- "Show me a dashboard of drift between intent and execution."

## Day-to-day flow

```bash
# Default 3-day window
bin/orbit-audit audit --project . --validate-codebase --dashboard

# Last week
bin/orbit-audit audit --project . --days 7 --validate-codebase --dashboard

# Since a specific date
bin/orbit-audit audit --project . --since 2026-05-01 --validate-codebase

# Explicit window
bin/orbit-audit audit --project . --from 2026-05-01 --to 2026-05-04

# Append today's intent candidates to the ledger
bin/orbit-audit build-ledger --project . --days 30

# Re-validate existing evidence (faster — skips session re-mining)
bin/orbit-audit validate-claims --project . --evidence .claude/audits/latest/evidence.json

# Re-render dashboard from existing evidence
bin/orbit-audit render-dashboard --evidence .claude/audits/latest/evidence.json
```

## Slash commands inside Claude Code

```text
/orbit:audit-gaps                Run full gap analysis on the current project
/orbit:mine-intent               Build/append the durable instruction ledger
/orbit:validate-claims           Validate assistant completion claims
/orbit:render-dashboard          Re-render dashboard.html from latest evidence
/orbit:compare-plan              Compare PLAN.md against sessions and repo state
/orbit:review-window             Configurable lookback (--days/--since/--from/--to)
/orbit:review-last-3-days        Legacy alias for --days 3
/orbit:rebuild-ledger            Replace the local ledger by re-mining
```

## Output paths

```text
.claude/audits/latest/evidence.json
.claude/audits/latest/gap-analysis.md
.claude/audits/latest/dashboard.html
.claude/audits/latest/intent-gap-flow.mmd
.claude/audits/latest/intent-timeline.mmd
.claude/audits/latest/plan-execution-matrix.csv
.claude/audits/intent-ledger.jsonl
.claude/audits/intent-ledger.md
```
