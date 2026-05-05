# Codebase Analysis — Orbit Plugin

Run ID: `20260505T202306Z`
Project: `/Users/nick/Desktop/orbit`
Generated: `2026-05-05T20:34:11Z`

## Plugin shape

The local Orbit project is a Claude Code plugin (not a Python package, not a Docker app). The `.claude-plugin/plugin.json` declares `name: "orbit"`, `version: "0.2.0"`, and points `skills`, `commands`, and `hooks` at the corresponding sibling directories/files.

```text
/Users/nick/Desktop/orbit/
├── .claude-plugin/plugin.json     manifest
├── skills/
│   ├── gap-analysis/SKILL.md
│   ├── instruction-ledger/SKILL.md
│   ├── plan-execution-audit/SKILL.md
│   └── validation-pairing/SKILL.md
├── commands/
│   ├── audit-gaps.md, mine-intent.md, validate-claims.md, render-dashboard.md
│   ├── compare-plan.md, review-window.md, review-last-3-days.md, rebuild-ledger.md
├── hooks/hooks.json
├── scripts/
│   ├── orbit_audit.py             single 700+-line engine — read this first when changing anything
│   ├── hook_instruction_detector.py
│   └── hook_prompt_context.py
├── bin/
│   ├── orbit-audit, orbit-dashboard, orbit-ledger   thin shells around scripts/orbit_audit.py
├── examples/                      bundled sample evidence + plan + gap report
├── tests/                         pytest smoke + fixtures (sample-session.jsonl, sample-repo/)
├── README.md, CHANGELOG.md, PRD.md, CLAUDE.md
└── .orbit-sdk-harness/            real SDK validation harness built by this audit
```

## Engine internals (`scripts/orbit_audit.py`)

| Function | Role |
|---|---|
| `compute_window` | Resolve `--days` / `--since` / `--from` / `--to` to UTC `[start_dt, end_dt]` |
| `discover_sessions` | Walk `~/.claude/projects/**/*.jsonl`, mtime + project-substring filter |
| `read_jsonl` | Forgiving line-by-line JSON parse, malformed lines logged + skipped |
| `flatten` | Recursive content extraction over a fixed allowlist of keys |
| `extract_intents` / `extract_claims` / `extract_tool_evidence` | Per-role extractors |
| `extract_plan_items` | Markdown plan parser (heading + checkbox/bullet) |
| `validate_codebase` | Default safe checks: `artifact_exists` + `claim_path_exists` |
| `analyze_gaps` | Token-Jaccard + claim status → gap records |
| `make_evidence` | Build the `evidence.json` schema (schema_version=0.2) |
| `render_dashboard` | Build `.claude/audits/latest/dashboard.html` |
| `render_markdown` | Build `gap-analysis.md` with scope echo |
| `build_ledger` | Append durable instructions to `intent-ledger.jsonl` + write `.md` companion |

## Subcommands

| Subcommand | Output dir |
|---|---|
| `audit` | `.claude/audits/latest/` (default) |
| `build-ledger` | `.claude/audits/intent-ledger.jsonl` (default) |
| `compare-plan` | `.claude/audits/latest/` (default) |
| `validate-claims` | `.claude/audits/latest/` (default) |
| `render-dashboard` | `.claude/audits/latest/dashboard.html` (default) |

## Time window flags (existing in parser, lines 614-617)

```python
parser.add_argument("--days", type=int, default=3, ...)
parser.add_argument("--since", ...)
parser.add_argument("--from", dest="start", ...)
parser.add_argument("--to", dest="end", ...)
```

The CLI already supports `--from` and `--to`. No patch was required for review-window flags.

## Required dashboard sections (per PRD)

`render_dashboard()` was patched in this audit run to add `Intent Timeline`, `Claim Validation`, and `Uncertainty` sections plus a `Scope` chip in the hero, and to declare `--red:#FF4D36` in the `:root` CSS so the brand palette is always present even when no high-severity gap is rendered. The pre-patch dashboard contained hero/cards/matrix/gaps; the post-patch dashboard contains hero+scope/cards/matrix/timeline/claim-validation/gaps/uncertainty.

## Hooks

`hooks/hooks.json` registers:
- `UserPromptSubmit` → `scripts/hook_instruction_detector.py` (writes candidate JSONL on match; non-blocking)
- `UserPromptExpansion` → `scripts/hook_prompt_context.py` (emits `additionalContext` on Orbit-relevant prompts; non-blocking)

Both hooks read JSON from stdin, exit 0, and never copy raw transcript content.

## bin wrappers

All three (`orbit-audit`, `orbit-dashboard`, `orbit-ledger`) follow the same pattern:

```bash
ROOT="${CLAUDE_PLUGIN_ROOT:-$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)}"
exec python3 "$ROOT/scripts/orbit_audit.py" [<subcommand>] "$@"
```

This makes them usable both as a checkout (no env var) and as an installed plugin (with `CLAUDE_PLUGIN_ROOT` provided by Claude Code).

## What the engine does NOT do

- It does not duplicate raw transcript capture (Claude Code already writes JSONL).
- It does not run destructive commands.
- It does not require Docker.
- It does not auto-execute a build, deploy, or shell command.
- Default safe validations are limited to artifact existence + claim-path-on-disk.

## Validation surfaces

| Surface | What it tests | Where |
|---|---|---|
| Manifest | JSON shape, paths resolve | `.orbit-sdk-harness/validate_plugin_manifest.py` |
| Skill frontmatter | YAML, name regex, description | `.orbit-sdk-harness/validate_skill_frontmatter.py` |
| Hooks | hooks.json + script smoke | `.orbit-sdk-harness/validate_hooks.py` |
| Commands | markdown shape + flag docs | `.orbit-sdk-harness/validate_commands.py` |
| Outputs | orbit-audit subcommands smoke | `.orbit-sdk-harness/validate_outputs.py` |
| End-to-end | 16 live SDK queries | `.orbit-sdk-harness/sdk_orbit_all.py` |

## Conclusion

The local Orbit project is a complete, self-contained Claude Code plugin. No remote fetch was used to map this architecture; every fact above is observed from the local filesystem.
