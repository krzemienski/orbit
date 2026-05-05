# Crucible Evidence Tree

Run ID: `20260505T202306Z`
Project: `/Users/nick/Desktop/orbit`
Forge invocation: `/crucible:forge "<orbit harness build instructions>"`

## Subdirectories

| Subdir | Phase | Purpose |
|---|---|---|
| `codebase-analysis/20260505T202306Z/` | Phase 1 | Local plugin map (manifest, skills, commands, hooks, scripts, bin) |
| `documentation-research/` | Phase 2 | Documentation source survey (5 sources × ≥3 facts each) |
| `skill-enrichment/20260505T202306Z/` | Phase 2.5 | 10 ranked skill candidates with rationale + skipped audit |
| `oracle-plan-reviews/20260505T202306Z/` | Phase 3+4 | PLAN.md (15 MSCs) + oracle-1 APPROVE verdict |
| `session-receipts/` | Phase 5 | Pre/PostToolUse session hook receipts (auto-emitted by Crucible hooks) |
| `validation-artifacts/20260505T202306Z.md` | Phase 6 | Per-MSC PASS/FAIL with cited evidence paths |
| `reviewer-consensus/` | Phase 8 | reviewer-a/b/c.md + decision.md (UNANIMOUS PASS) |
| `final-oracle-evidence-audit/` | Phase 9 | oracle-1/2/3.md + decision.md (APPROVED) + blockers/ |
| `completion-gate/report.json` | Phase 10 | gate.py output: overall=COMPLETE if all MSCs cited + reviewer + oracle gates passed |
