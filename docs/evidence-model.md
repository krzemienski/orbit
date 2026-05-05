# Evidence Model

Orbit's evidence is a single JSON document (`evidence.json`, `schema_version: "0.2"`) that normalizes everything Orbit observes into seven typed lists.

## Top-level shape

```json
{
  "schema_version": "0.2",
  "generated_at": "ISO UTC",
  "project": { "cwd": "...", "name": "..." },
  "scope":   { "days": 3, "since": null, "from": null, "to": null, "query": "...", "plans": [] },
  "sources": { "sessions": ["..."], "plans": ["..."] },
  "intents":        [ { "id": "intent_NNNN", "kind": "...", "text": "...", "source": {...}, "directness": "...", "specificity": "...", "status": "...", "matched_patterns": [...] } ],
  "plan_items":     [ { "id": "plan_NNNN", "source_file": "...", "line_number": 1, "heading": "...", "text": "...", "status_hint": "..." } ],
  "claims":         [ { "id": "claim_NNNN", "text": "...", "claim_type": "completion", "source": {...}, "validation_status": "unverified" } ],
  "tool_evidence":  [ { "id": "tool_NNNN", "tool_name": "...", "action": "...", "target": "...", "status": "observed", "source": {...}, "text": "..." } ],
  "validations":    [ { "id": "validation_NNNN", "target_type": "claim|artifact", "target_id": "...", "check": "artifact_exists|claim_path_exists", "path": "...", "status": "passed|failed|unverified", "evidence": "...", "severity": "low|medium|high" } ],
  "gaps":           [ { "id": "gap_NNNN", "category": "...", "severity": "low|medium|high", "title": "...", "summary": "...", "evidence_ids": [...], "recommended_next_action": "..." } ],
  "conflicts":      [],
  "uncertainties":  []
}
```

## Intent kinds

`requirement`, `correction`, `rename`, `preference`, `constraint`, `non-goal`, `validation-request`, `visualization-request`, `workflow-change`, `approval-gate`. The classifier in `orbit_audit.py::classify_intent` collapses these into the kinds visible in the JSON.

## Validation checks

`file_exists`, `symbol_exists`, `text_exists`, `artifact_exists`, `script_executable`, `command_succeeded`, `test_succeeded`, `build_succeeded`, `lint_succeeded`, `schema_valid`. The default safe set is `artifact_exists` + `claim_path_exists` (path mention in the claim text).

## Gap categories

`intent-not-planned`, `intent-not-implemented`, `claim-not-validated`, `claim-contradicted`, `plan-stale`, `plan-omission`, `session-only-decision`, `superseded-plan-item`, `missing-artifact`, `missing-validation`, `ambiguous-evidence`.

## Evidence ranking

When two pieces of evidence conflict, Orbit ranks (highest → lowest):

1. Later direct user instruction
2. Specific user correction
3. Direct session evidence tied to implementation
4. Tool-use evidence showing actual action
5. Tool-result evidence showing success or failure
6. Current codebase state
7. Test/build/lint validation result
8. Earlier direct user instruction
9. Written plan evidence
10. Assistant claim or summary
11. Inference across multiple sources
12. History metadata only

## Cardinal rule

A plan omission is "not found in the plan." It is not proof the user did not request it. Orbit always emits a gap, never a silent denial.
