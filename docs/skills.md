# Skills

Orbit ships four skills. Each lives at `skills/<name>/SKILL.md` with YAML frontmatter and an operational body.

## `gap-analysis`

Trigger: any audit-like or look-back request — "audit", "look back", "review-window", "what did we miss", "gap analysis", "compare to the plan", "did it actually get done".

Workflow: scope → plan extract → session mine → intent extract → claim extract → tool evidence → codebase validate → gap synthesize → output `evidence.json`, `gap-analysis.md`, `dashboard.html`, `intent-gap-flow.mmd`, `intent-timeline.mmd`, `plan-execution-matrix.csv`.

## `instruction-ledger`

Trigger: project-memory and intent-corpus requests — "ledger", "rebuild the ledger", "what did I tell you", "project memory", "corrections".

Watches signal phrases: actually, no instead, we decided, go with, settled on, from now on, make sure, must include, do not, you forgot, this is wrong, changed our mind.

Outputs: `.claude/audits/intent-ledger.jsonl` plus a markdown companion.

## `plan-execution-audit`

Trigger: "compare to the plan", "does this match the plan", "what plan items are missing", "what got superseded".

Marks each plan item as complete, partial, unverified, contradicted, stale, or superseded. Plan omission means "not found in the plan" — never proof the user did not request it.

## `validation-pairing`

Trigger: "did it actually do it", "validate the claims", "prove it was completed", "check against the repo", "functional validation".

For every completion claim: locate it, find related tool evidence, inspect relevant files, run safe configured validation, and tag `validated`, `partially validated`, `unverified`, `contradicted`, `stale`, or `uncertain`. No destructive checks unless explicitly configured.

## Compliance

`validate_skill_frontmatter.py` verifies for every skill:
- frontmatter delimited by `---`
- `name` matches `^[a-z0-9-]+$` and length ≤ 64
- `description` is non-empty, has no XML tags, length ≤ 1024
- body is non-empty
