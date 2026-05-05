# Plugin Compliance

Orbit's compliance posture combines five static validators with the live SDK harness. All five validators must pass before any SDK scenario is trusted.

## Static validators

| Script | Checks | Exits 0 when |
|---|---|---|
| `validate_plugin_manifest.py` | manifest exists + parses, name=`orbit`, version present, description present, every recognized sub-path resolves | every check PASS |
| `validate_skill_frontmatter.py` | per-skill: frontmatter present, name regex, description present + no XML + ≤1024 chars, body non-empty | every skill PASS |
| `validate_hooks.py` | hooks.json parses, recognized event names, each command path exists + executable + accepts JSON stdin + exits 0 | every hook PASS |
| `validate_commands.py` | per-command: file present, body non-empty, leading heading, fenced example, helper/skill mapping; review-window documents the four flags; review-last-3-days documents the alias | every command PASS |
| `validate_outputs.py` | smoke `audit`, `build-ledger`, `render-dashboard` against bundled fixtures; verify every artifact + every dashboard token + every evidence field | every check PASS |

## Brand compliance

The dashboard must contain every brand color hex (`#C6FF00`, `#FF8A00`, `#FF4D36`, `#8B3DFF`, `#1E6BFF`) and the `Find drift` tagline. Missing any token is a `FAIL`, not a warning.

## Approval scope (PRD)

- No Dockerfile.
- No docker-compose.
- No Python package layout.
- Flat helper scripts only.

`validate_plugin_manifest.py` and `validate_outputs.py` together enforce this — anything that wires up a package layout would fail manifest path resolution or break the bundled fixture flow.
