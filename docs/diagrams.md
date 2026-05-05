# Diagrams

Mermaid sources live under `docs/diagrams/`. Each begins with a recognized Mermaid diagram type so any compliant viewer (GitHub, Mermaid Live, mermaid-cli) renders them without preprocessing.

| File | Diagram type | Topic |
|---|---|---|
| `orbit-system-flow.mmd` | flowchart | End-to-end Orbit pipeline from user question to outputs |
| `evidence-pipeline.mmd` | flowchart | Normalization + ranking of evidence layers |
| `intent-to-gap-model.mmd` | flowchart | Mapping every intent/claim/plan/evidence shape to gap categories |
| `sdk-harness-flow.mmd` | flowchart | Master harness pipeline + scenarios + reports |
| `plugin-compliance-flow.mmd` | flowchart | Static validators + aggregation |
| `review-window-flow.mmd` | flowchart | Review window flag handling + scope echo |
| `hook-candidate-flow.mmd` | flowchart | UserPromptSubmit hook decision flow |
| `claim-validation-flow.mmd` | flowchart | Claim → tool evidence → repo path → gap |
| `dashboard-output-flow.mmd` | flowchart | Dashboard sections rendered from evidence |
| `installed-plugin-validation-flow.mmd` | flowchart | What can / cannot be checked non-interactively |
| `local-architecture-discovery-flow.mmd` | flowchart | `discover_layout` walk |

## Render

GitHub renders Mermaid in markdown automatically. To render to SVG:

```bash
npx @mermaid-js/mermaid-cli -i docs/diagrams/orbit-system-flow.mmd -o /tmp/orbit-system-flow.svg
```

## Validation

`sdk_orbit_docs_compliance.py` and `sdk_orbit_all.py::docs_completeness()` confirm each `.mmd` file is non-empty AND begins with one of: `flowchart`, `graph`, `sequencediagram`, `statediagram`, `classdiagram`, `timeline`, `journey`, `gantt`, `erdiagram`, `pie`, `mindmap`. A missing or empty diagram is a `FAIL`.
