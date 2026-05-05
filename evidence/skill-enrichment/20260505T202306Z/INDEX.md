# Skill Enrichment Index

Run ID: `20260505T202306Z`

| File | Purpose |
|---|---|
| `INDEX.md` | This file — top-level summary + ranked table |
| `CANDIDATES.md` | Per-candidate rationale (≥3 sentences each) |
| `SKIPPED.md` | Audit trail of skipped/below-floor skills |
| `raw-inventory.txt` | Full enumerated skill list pre-filter |

Result: **10 candidates above floor** (≥5 required). Refusal NOT triggered.

Top three (required for plan):
1. `testing-cc-plugins-python-sdk`
2. `superpowers-developing-for-claude-code:developing-claude-code-plugins`
3. `python-agent-sdk`

## Ranked candidates

| Rank | Skill | Score | SKILL.md path |
|---|---|---|---|
| 1 | `testing-cc-plugins-python-sdk` | 0.58 | `~/.claude/skills/testing-cc-plugins-python-sdk/SKILL.md` |
| 2 | `superpowers-developing-for-claude-code:developing-claude-code-plugins` | 0.55 | `~/.claude/plugins/cache/superpowers-marketplace/superpowers-developing-for-claude-code/0.3.1/skills/developing-claude-code-plugins/SKILL.md` |
| 3 | `python-agent-sdk` | 0.42 | `~/.claude/skills/python-agent-sdk/SKILL.md` |
| 4 | `claude-api` | 0.38 | `~/.claude/skills/claude-api/SKILL.md` |
| 5 | `functional-validation` | 0.36 | `~/.claude/skills/functional-validation/SKILL.md` |
| 6 | `validationforge:no-mocking-validation-gates` | 0.34 | `~/.claude/plugins/validationforge/skills/no-mocking-validation-gates/SKILL.md` |
| 7 | `validationforge:e2e-validate` | 0.31 | `~/.claude/plugins/validationforge/skills/e2e-validate/SKILL.md` |
| 8 | `validationforge:create-validation-plan` | 0.28 | `~/.claude/plugins/validationforge/skills/create-validation-plan/SKILL.md` |
| 9 | `validationforge:gate-validation-discipline` | 0.25 | `~/.claude/plugins/validationforge/skills/gate-validation-discipline/SKILL.md` |
| 10 | `validationforge:verification-before-completion` | 0.22 | `~/.claude/plugins/validationforge/skills/verification-before-completion/SKILL.md` |

## Correction note

Initial enumeration omitted two highest-relevance candidates: `testing-cc-plugins-python-sdk` (the canonical pattern for testing Claude Code plugins via the Python Agent SDK — exactly what this harness does) and `superpowers-developing-for-claude-code:developing-claude-code-plugins` (the canonical guide for plugin structure, manifest, marketplace, and lifecycle). Both should rank above the previously-listed top entries; ranking re-issued accordingly. The user surfaced this gap during execution — credit to the human-in-the-loop check.
