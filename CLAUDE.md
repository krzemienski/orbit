# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Repo Is

Orbit is a **Claude Code plugin** (not a Python package, not a Docker app). Layout matches the Claude Code plugin contract:

```
.claude-plugin/plugin.json   plugin manifest (name, version, skills/commands/hooks paths)
skills/<name>/SKILL.md       skill activation files with YAML frontmatter
commands/<name>.md           slash-command bodies for /orbit:<name>
hooks/hooks.json             UserPromptSubmit + UserPromptExpansion hook wiring
scripts/                     flat Python helpers invoked by hooks/CLI wrappers
bin/                         thin bash wrappers around scripts/orbit_audit.py
tests/                       pytest smoke tests against scripts + fixtures
examples/                    sample evidence/ledger/dashboard outputs
```

**No Docker. No `pyproject.toml`. No package install.** Helpers are run as `python3 scripts/orbit_audit.py ...` or via the `bin/orbit-*` shims. Approval scope (PRD.md) explicitly forbids adding either.

## Core Mental Model

The plugin compares evidence layers in this fixed order — every command, skill, and helper output is structured around it:

```
user intent → plan evidence → assistant claims → tool evidence → codebase truth → gaps
```

Iron rule (`skills/gap-analysis/SKILL.md`, README "Core Principle"):
- Plans are evidence, not historical truth.
- Assistant claims are claims, not proof.
- Codebase validation is required before completion is trusted.
- Plan omission ≠ proof never requested. Mark missing evidence as `uncertainty`, not absence.

Evidence ranking (PRD §"Evidence Ranking", 1–12) goes: later user instruction > correction > direct session evidence > tool-use > tool-result > codebase state > validation result > earlier instruction > written plan > assistant claim > inference > history metadata. Honor this order in any new analyzer.

## How The Pieces Connect

`scripts/orbit_audit.py` is the engine. Every other surface delegates to it.

| Surface | Entrypoint | Calls |
|---|---|---|
| Slash command `/orbit:audit-gaps` etc. | `commands/*.md` | suggests `orbit-audit audit ...` |
| `bin/orbit-audit` | bash wrapper | `python3 scripts/orbit_audit.py "$@"` |
| `bin/orbit-dashboard` | bash wrapper | `python3 scripts/orbit_audit.py render-dashboard "$@"` |
| `bin/orbit-ledger` | bash wrapper | `python3 scripts/orbit_audit.py build-ledger "$@"` |
| Hook `hook_instruction_detector.py` | `UserPromptSubmit` | appends candidate intents to `intent-ledger-candidates.jsonl`; injects `additionalContext` for audit-like prompts |
| Hook `hook_prompt_context.py` | `UserPromptExpansion` | injects Orbit workflow context when prompt mentions orbit/audit/gap/etc. |

Subcommands of `scripts/orbit_audit.py` (see `build_parser`):

- `audit` → full pipeline → writes `evidence.json`, `gap-analysis.md`, `dashboard.html`, `intent-gap-flow.mmd`, `intent-timeline.mmd`, `plan-execution-matrix.csv` to `--output` (default `.claude/audits/latest`).
- `build-ledger` → writes `intent-ledger.jsonl` + sibling `.md` (default `.claude/audits/intent-ledger.jsonl`); `--replace` truncates, otherwise appends.
- `compare-plan` → audit aliased; `--plan` accumulates into `args.plans`.
- `validate-claims` → if `--evidence <path>` is given, re-runs `validate_codebase` + `analyze_gaps` against existing JSON; otherwise forces `validate_codebase=True` and runs full audit.
- `render-dashboard` → reads `evidence.json`, writes `dashboard.html` only.

Pipeline inside `make_evidence` (the function to read first when changing audit behavior):
1. `compute_window` resolves `--days|--since|--from/--to` to a UTC `[start_dt, end_dt]`.
2. `discover_sessions` walks `~/.claude/projects/**/*.jsonl` (override with `--session-root`/`--sessions`); filters by mtime + a *gentle* substring match against the project dir name (`project_filter`). The substring filter is intentionally loose because Claude Code encodes paths weirdly — do not tighten without verifying against real session paths.
3. `read_jsonl` is forgiving — malformed lines are skipped at DEBUG, not raised. Each event normalizes to `{source_file, line_number, event_index, timestamp, role, event_type, content_text, raw}` via `flatten()` (recursive walk over a fixed key allowlist).
4. `extract_intents` (user-role only), `extract_claims` (assistant-role only), `extract_tool_evidence` (event_type/content keyword sniff) run over sorted events.
5. `extract_plan_items` falls back to `PLAN.md, PRD.md, README.md, TODO.md, TASKS.md, IMPLEMENTATION.md` + `docs/**/*.md` when `--plans` is absent.
6. `validate_codebase` (only if `--validate-codebase`) checks two things: presence of the three default audit artifacts, and existence of any `*.py|md|json|html|js|ts|tsx|jsx|css|yml|yaml|sh` paths name-dropped in claim text.
7. `analyze_gaps` produces gaps where intent has <0.08 token-Jaccard with any plan item, or claim is unverified/failed, plus the empty-everything fallback.

Output schema is `schema_version: "0.2"`. If you change any record shape (`intents`, `plan_items`, `claims`, `tool_evidence`, `validations`, `gaps`), bump it.

## Brand / Dashboard

`render_dashboard` is hand-written HTML+CSS using the `COLORS` dict. The brand palette is fixed (README/PRD): black `#0A0A0B` base, lime `#C6FF00` (active/valid), orange `#FF8A00` (pending), red `#FF4D36` (contradictions), purple `#8B3DFF` (analysis), blue `#1E6BFF` (plans). Severity → color mapping in `render_dashboard`: `high`=red, `medium`=orange, else blue. Tagline `Find drift. Close gaps. Restore alignment.` is canonical.

## Common Commands

```bash
# Run tests (pytest, no extra deps — uses stdlib + subprocess)
python3 -m pytest tests/

# Run a single test
python3 -m pytest tests/test_orbit_scripts.py::test_audit_smoke -v

# Compile-check the engine without running
python3 -m py_compile scripts/orbit_audit.py

# Smoke against bundled fixtures (mirrors test_audit_smoke)
python3 scripts/orbit_audit.py audit \
  --project tests/fixtures/sample-repo \
  --plans tests/fixtures/sample-plan.md \
  --sessions tests/fixtures/sample-session.jsonl \
  --validate-codebase \
  --output /tmp/orbit-out

# Real audit against current project (3-day default window)
bin/orbit-audit audit --project . --validate-codebase --dashboard

# Custom window
bin/orbit-audit audit --project . --days 7
bin/orbit-audit audit --project . --since 2026-05-01
bin/orbit-audit audit --project . --from 2026-05-01 --to 2026-05-04

# Re-validate existing evidence without re-mining sessions
bin/orbit-audit validate-claims --project . --evidence .claude/audits/latest/evidence.json

# Append today's intents to durable ledger
bin/orbit-audit build-ledger --days 30 --project .
```

`bin/*` resolve `CLAUDE_PLUGIN_ROOT` first, falling back to the script's parent dir, so they work both as plugin and as a checkout.

## Conventions When Editing

- Keep `scripts/` flat. New helpers = new top-level `.py`, not packages. PRD §"Approval Scope" forbids package layout.
- `INTENT_PATTERNS` and `CLAIM_PATTERNS` (top of `orbit_audit.py`) are duplicated in `hook_instruction_detector.py::PATTERNS` for hook-time detection. Any new pattern added to one should be considered for the other; they intentionally diverge slightly because the hook doesn't have session context.
- `flatten()`'s key allowlist (`content`, `text`, `message`, `result`, `toolUseResult`, `tool_result`, `summary`, `name`, `type`, `role`, `cwd`, `command`, `file_path`, `path`, `input`, `output`, `error`) is the contract for which JSONL fields become `content_text`. Anything outside this list is invisible to extractors.
- Hooks return JSON on stdout via `hookSpecificOutput.additionalContext` — keep that shape; do not switch to `decision: "block"`/`approve` (deprecated per `~/.claude/rules/hooks-and-integrations.md`).
- Default outputs go under `.claude/audits/latest/` (per-run) and `.claude/audits/intent-ledger.{jsonl,md}` (durable). Don't break those paths — `validate_codebase` literally checks for those three artifacts as a self-test.
- All datetimes are UTC ISO with a trailing `Z` (`now_iso`). `parse_date` accepts both `YYYY-MM-DD` and full ISO; preserve that.
- Tests are smoke + compile only. There is no mocking framework in scope; tests shell out to `scripts/orbit_audit.py` against `tests/fixtures/`. New tests should follow the same pattern.

## Slash Commands Available

`/orbit:audit-gaps`, `/orbit:mine-intent`, `/orbit:validate-claims`, `/orbit:compare-plan`, `/orbit:render-dashboard`, `/orbit:review-window`, `/orbit:review-last-3-days` (legacy alias for `--days 3`), `/orbit:rebuild-ledger`. Bodies are in `commands/*.md` and just suggest `bin/orbit-audit ...` invocations.

## Skills

Four skills under `skills/`: `gap-analysis`, `instruction-ledger`, `plan-execution-audit`, `validation-pairing`. Each is a directory with `SKILL.md` (YAML frontmatter `name` + `description` triggers activation) plus `references/`. The frontmatter `description` is what Claude Code matches against — keep trigger phrases broad ("look back", "what did we miss", "compare to plan", etc.).
