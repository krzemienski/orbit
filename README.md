# Orbit

**Orbit** is a local Claude Code plugin for intent mining, gap analysis, claim validation, and dashboard visualization.

Orbit does not duplicate raw transcript capture. Claude Code already stores sessions locally. Orbit mines what already exists, then compares:

```text
user intent → plan evidence → assistant claims → tool evidence → codebase truth → gaps
```

## Brand

Orbit uses a flat black visual system with high-energy accents:

- Orbit Lime `#C6FF00` for active, valid, live, complete
- Orbit Orange `#FF8A00` for pending or attention
- Orbit Red `#FF4D36` for contradictions and severe gaps
- Orbit Purple `#8B3DFF` for intelligence, analysis, session-only decisions
- Orbit Blue `#1E6BFF` for plans, systems, and structure

Tagline:

```text
Find drift. Close gaps. Restore alignment.
```

## Install

Place the `orbit/` folder in your Claude Code plugin location or install it through your Claude Code plugin workflow.

Expected shape:

```text
orbit/
  .claude-plugin/plugin.json
  skills/
  commands/
  hooks/
  scripts/
  bin/
```

## Commands

Plugin slash commands:

```text
/orbit:audit-gaps
/orbit:mine-intent
/orbit:validate-claims
/orbit:compare-plan
/orbit:render-dashboard
/orbit:review-window
/orbit:review-last-3-days
/orbit:rebuild-ledger
```

Native executable helpers:

```bash
bin/orbit-audit audit --days 3 --project . --dashboard --validate-codebase
bin/orbit-audit build-ledger --days 30 --project .
bin/orbit-audit compare-plan --plan PLAN.md --project . --validate-codebase
bin/orbit-audit render-dashboard --evidence .claude/audits/latest/evidence.json
```

## Review Windows

`review-window` defaults to 3 days, but accepts explicit windows:

```text
/orbit:review-window --days 7 Find what changed this week.
/orbit:review-window --since 2026-05-01 Find missed instructions since May 1.
/orbit:review-window --from 2026-05-01 --to 2026-05-04 Audit this exact window.
```

Legacy alias:

```text
/orbit:review-last-3-days
```

Equivalent to:

```text
/orbit:review-window --days 3
```

## Outputs

By default Orbit writes:

```text
.claude/audits/latest/gap-analysis.md
.claude/audits/latest/evidence.json
.claude/audits/latest/dashboard.html
.claude/audits/latest/intent-gap-flow.mmd
.claude/audits/latest/intent-timeline.mmd
.claude/audits/latest/plan-execution-matrix.csv
.claude/audits/intent-ledger.jsonl
.claude/audits/intent-ledger.md
```

## Core Principle

Plans are evidence, not the complete historical record. Assistant claims are claims, not proof. Codebase validation is required before completion is trusted.

## No Docker

Orbit is intentionally a native plugin with flat Python helper scripts. It does not include a Dockerfile, compose file, or Python package project.
