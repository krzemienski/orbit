---
name: gap-analysis
description: Mines local session transcripts, written plans, assistant claims, tool evidence, and codebase state for Orbit audits, retrospectives, lookbacks, review-window requests, gap analysis, validation, remediation planning, and questions like “what did we miss,” “what changed,” “check sessions,” “compare to the plan,” or “did it actually get done.”
---

# Orbit Gap Analysis

Use this skill when the user asks to audit a project, look back through sessions, identify missed work, compare intent to plans, validate assistant claims, or produce remediation recommendations.

## Core Rule

Plans are evidence, not the complete historical record. Assistant claims are claims, not proof. Validate against tool evidence and current repo state before marking work complete.

## Workflow

1. Detect scope: project, plan, feature, alias, time window, and requested output.
2. Search written plans and specs when relevant.
3. Search local session transcripts under `~/.claude/projects/**/*.jsonl` when available.
4. Parse JSONL as ordered event streams.
5. Extract direct user intent, corrections, pivots, renames, constraints, and validation requests.
6. Extract assistant completion claims.
7. Extract tool-use evidence and tool results.
8. Validate claims against current codebase state.
9. Produce gap records and remediation recommendations.
10. Render Markdown, JSON, Mermaid, CSV, and dashboard outputs when requested.

## Evidence Layers

Compare:

```text
user intent → plan evidence → assistant claims → tool evidence → codebase truth → gaps
```

## Time Windows

Default review window is 3 days. Support explicit windows:

```text
--days N
--since YYYY-MM-DD
--from YYYY-MM-DD --to YYYY-MM-DD
```

## Required Output Discipline

Separate:

- confirmed findings,
- plan evidence,
- session evidence,
- assistant claims,
- tool evidence,
- codebase validation,
- gaps,
- conflicts,
- uncertainty,
- recommended next actions.

Never treat a plan omission as proof that something was never requested. Mark missing evidence as uncertainty.

## Helper Scripts

Use flat scripts when useful:

```bash
orbit-audit audit --days 3 --project . --validate-codebase --dashboard
orbit-audit compare-plan --plan PLAN.md --project . --validate-codebase
orbit-audit validate-claims --project . --evidence .claude/audits/latest/evidence.json
```
