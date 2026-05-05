# Skill Creator-style Review

Each Orbit skill is reviewed against six criteria modeled on the Claude Code Skill Creator rubric. The Orbit-specific scoring is implemented in `sdk_orbit_skill_compliance.py` and `sdk_orbit_all.py::skill_creator_review()`.

## Criteria

| Criterion | What it measures | 5-point scale |
|---|---|---|
| `trigger_accuracy` | How many concrete trigger phrases the skill description names | 5 if ≥3 phrases match, 4 if ≥2, 3 if 1, 1 otherwise |
| `clarity` | Is the description in the sweet spot (80–1024 chars)? | 5 if yes, 3 otherwise |
| `scope_fit` | Does the description disambiguate vs. other skills? | 5 if ≥2 trigger phrases, 3 otherwise |
| `frontmatter_compliance` | Does `name` match the directory? Frontmatter parse cleanly? | 5 if yes, 1 if not |
| `operational_completeness` | Body describes a workflow, rule, contract, or outputs? | 5 if any of those tokens present, 3 otherwise |

`overall = round(mean(criteria), 2)`. A skill is PASS at `overall ≥ 4.0` AND no improvement actions outstanding.

## Per-skill expectations

| Skill | Expected trigger hints |
|---|---|
| `gap-analysis` | "audit", "look back", "review-window", "what did we miss", "gap analysis", "compare to the plan" |
| `instruction-ledger` | "ledger", "rebuild the ledger", "what did I tell you", "project memory", "corrections" |
| `plan-execution-audit` | "compare to the plan", "does this match the plan", "missing", "superseded" |
| `validation-pairing` | "did it actually do it", "validate the claims", "prove it was completed", "check against the repo" |

## Output

`reports/orbit-skill-creator-review.md` contains a per-skill scoring table and recommended improvements. The matching JSON payload is at `reports/evidence/skill-creator-review.json`.

A failing review is a `FAIL`, not a warning. The fix is to broaden the description's trigger phrases or restructure the body — the review then re-runs.
