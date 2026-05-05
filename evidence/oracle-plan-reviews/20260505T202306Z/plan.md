# Orbit Validation Harness — PLAN

Run ID: `20260505T202306Z`
Project: `/Users/nick/Desktop/orbit`
Generated: `2026-05-05T20:34:11Z`

## Required Skills (per Phase 2.5 enrichment)

1. `testing-cc-plugins-python-sdk` — canonical pattern for testing Claude Code plugins via the Python Agent SDK; the harness's primary blueprint.
2. `superpowers-developing-for-claude-code:developing-claude-code-plugins` — canonical Claude Code plugin development guide; informs `validate_plugin_manifest.py`, `validate_hooks.py`, the bin-wrapper convention, and the `${CLAUDE_PLUGIN_ROOT}` portability rule.
3. `python-agent-sdk` — real `claude-agent-sdk` `query()` discipline (auth, options, stream handling, `ResultMessage` detection).

Recommended: `claude-api`, `functional-validation`, `validationforge:no-mocking-validation-gates`, `validationforge:e2e-validate`, `validationforge:create-validation-plan`, `validationforge:gate-validation-discipline`, `validationforge:verification-before-completion`.

## Mandatory Success Criteria (MSCs)

### MSC-1 — Architecture discovery PASS
- **Owner:** `sdk_orbit_all.py::architecture_discovery()`
- **Criteria:** every required surface (manifest, skills/, commands/, hooks/, scripts/, bin/, README, CHANGELOG, PRD) is present; ≥4 skills; ≥8 commands; ≥1 bin wrapper.
- **Evidence:** `.orbit-sdk-harness/reports/orbit-architecture-discovery.md`
- **Pass = all 13 architecture_* checks PASS**.

### MSC-2 — Plugin manifest valid
- **Owner:** `validate_plugin_manifest.py`
- **Criteria:** `.claude-plugin/plugin.json` parses, name=`orbit`, all referenced sub-paths exist.
- **Evidence:** `.orbit-sdk-harness/reports/evidence/static-manifest.json`
- **Pass = status=PASS in payload**.

### MSC-3 — Skill frontmatter valid (every skill)
- **Owner:** `validate_skill_frontmatter.py`
- **Criteria:** for each of `gap-analysis`, `instruction-ledger`, `plan-execution-audit`, `validation-pairing`: frontmatter parses, name regex matches, description non-empty + no XML + ≤1024 chars, body non-empty.
- **Evidence:** `.orbit-sdk-harness/reports/evidence/static-frontmatter.json`
- **Pass = every skill status=PASS**.

### MSC-4 — Hooks valid
- **Owner:** `validate_hooks.py`
- **Criteria:** `hooks/hooks.json` parses; both `UserPromptSubmit` + `UserPromptExpansion` hooks point to existing executable scripts; smoke (stdin JSON → exit 0) succeeds.
- **Evidence:** `.orbit-sdk-harness/reports/evidence/static-hooks.json`
- **Pass = status=PASS**.

### MSC-5 — Commands valid
- **Owner:** `validate_commands.py`
- **Criteria:** all 8 commands exist with leading heading + fenced example + helper/skill mapping; `review-window` documents `--days/--since/--from/--to`; `review-last-3-days` documents alias.
- **Evidence:** `.orbit-sdk-harness/reports/evidence/static-commands.json`
- **Pass = status=PASS**.

### MSC-6 — Outputs smoke
- **Owner:** `validate_outputs.py`
- **Criteria:** `orbit-audit audit` against bundled fixtures emits `evidence.json` (with required schema fields), `gap-analysis.md`, `dashboard.html` (with all brand tokens + Timeline + Claim Validation + Uncertainty + Scope + Matrix), two `.mmd`, one `.csv`. `build-ledger` emits valid JSONL + `.md` companion. `render-dashboard` exits 0.
- **Evidence:** `.orbit-sdk-harness/reports/evidence/static-outputs.json`
- **Pass = status=PASS**.

### MSC-7 — SDK scenarios all PASS or BLOCKED
- **Owner:** `sdk_orbit_all.py::run_scenarios()`
- **Criteria:** 16 live `query()` invocations across 13 scenarios (06 fires 3×); each captures `transcript.json`, `session-id.txt`, `jsonl-pointer.txt`, `summary.json`, `started-at.txt`, `finished-at.txt`, `got-result.txt`. Each PASS row cites `transcript.json` AND `got_result_message=true`.
- **Evidence:** `.orbit-sdk-harness/runs/<id>-<scenario>/` (one per scenario) + `.orbit-sdk-harness/reports/orbit-scenario-matrix.csv`
- **Pass = scenario_status PASS or BLOCKED only (no FAIL)**.

### MSC-8 — Dashboard verification
- **Owner:** `sdk_orbit_all.py::dashboard_verification()`
- **Criteria:** rendered dashboard from `examples/sample-evidence.json` contains every brand color (#C6FF00, #FF8A00, #FF4D36, #8B3DFF, #1E6BFF), tagline `Find drift`, and section markers `ORBIT`, `Timeline`, `Claim Validation`, `Uncertainty`, `Scope`, `Matrix`.
- **Evidence:** `.orbit-sdk-harness/reports/orbit-dashboard-verification.md` + `.orbit-sdk-harness/reports/evidence/dashboard-verified.html`
- **Pass = every dashboard_token_* check PASS**.

### MSC-9 — Documentation completeness
- **Owner:** `sdk_orbit_all.py::docs_completeness()`
- **Criteria:** all 20 markdown docs in `docs/`; all 20 HTML drafts in `docs-html/`; all 11 Mermaid diagrams in `docs/diagrams/` (each begins with a recognized diagram type).
- **Evidence:** `.orbit-sdk-harness/reports/orbit-docs-compliance.md`
- **Pass = every doc_md_*, doc_html_*, diagram_* check PASS**.

### MSC-10 — Skill Creator-style review
- **Owner:** `sdk_orbit_all.py::skill_creator_review()`
- **Criteria:** every Orbit skill scores ≥4.0 overall on the 5-criterion rubric (trigger_accuracy, clarity, scope_fit, frontmatter_compliance, operational_completeness) with no outstanding improvement actions.
- **Evidence:** `.orbit-sdk-harness/reports/orbit-skill-creator-review.md`
- **Pass = every skill overall ≥4.0**.

### MSC-11 — Installed plugin validation honest reporting
- **Owner:** `sdk_orbit_all.py::installed_plugin_validation()`
- **Criteria:** `claude` CLI on PATH detected; `~/.claude/plugins/installed_plugins.json` parsed; BLOCKED checks (slash command discovery, skill discovery, hook configuration) include manual verification commands.
- **Evidence:** `.orbit-sdk-harness/reports/orbit-installed-plugin-validation.md`
- **Pass = no silent skips; every BLOCKED row has manual_verification_command**.

### MSC-12 — Hook candidate JSONL capture
- **Owner:** `sdk_orbit_hook_candidate.py`
- **Criteria:** Drives the `UserPromptSubmit` hook with 4 payloads via direct subprocess; verifies the hook wrote valid JSONL records (timestamp, cwd, source, kind, prompt_excerpt, detected_patterns, status); confirms no raw transcript copy is created.
- **Evidence:** `.orbit-sdk-harness/runs/<id>-07-hook-candidate/hook-invocations.json` + `hook-candidates.json`
- **Pass = hook_invocation_count==4 AND hook_candidate_records≥4 AND no raw transcript file in CLAUDE_PLUGIN_DATA dir**.

### MSC-13 — Real ledger build
- **Owner:** `sdk_orbit_mine_intent.py`
- **Criteria:** SDK scenario completes AND `build-ledger` against bundled fixture emits valid JSONL records + `.md` companion. Each JSONL line parses cleanly.
- **Evidence:** `.orbit-sdk-harness/runs/<id>-09-instruction-ledger/intent-ledger.jsonl` + `.md`
- **Pass = ResultMessage observed AND ledger_jsonl_invalid_lines==0 AND ledger_md_present**.

### MSC-14 — Configurable review window
- **Owner:** `sdk_orbit_review_window.py` (called 3× by master)
- **Criteria:** Three live `query()` invocations with different scope flags (`--days 7`, `--since 2026-05-01`, `--from 2026-05-01 --to 2026-05-04`). Each produces a `transcript.json` with `ResultMessage`. The CLI parser already supports all four flags (lines 614-617 of `scripts/orbit_audit.py`); no patch required.
- **Evidence:** `.orbit-sdk-harness/runs/<id>-06-review-window-*/transcript.json` (3 runs)
- **Pass = 3 ResultMessages observed**.

### MSC-15 — Crucible evidence tree
- **Owner:** This planning phase + downstream forge phases
- **Criteria:** `evidence/codebase-analysis/<run>/SUMMARY.md`, `evidence/documentation-research/SUMMARY.md`, `evidence/skill-enrichment/<run>/INDEX.md` (≥5 candidates), `evidence/oracle-plan-reviews/<run>/plan.md` + `oracle-1-verdict.md` (APPROVE), `evidence/validation-artifacts/<run>.md`, `evidence/reviewer-consensus/{a,b,c}.md` + `decision.md` (UNANIMOUS PASS), `evidence/final-oracle-evidence-audit/{1,2,3}.md` + `decision.md` (APPROVED), `evidence/completion-gate/report.json` (overall=COMPLETE).
- **Evidence:** `evidence/`
- **Pass = every cited path exists, non-empty, and matches schema**.

## Out of scope

- Live `claude plugin install` — installation validation is BLOCKED with a manual command (per MSC-11). The harness does not destructively install Orbit into the user's environment.
- Network fetches — documentation research is local-only.
- Test files / mocks / stubs — forbidden per Iron Rule.

## Risks

- The live SDK runs (16 `query()` calls) may be rate-limited or fail subscription auth. Mitigation: each scenario is independently re-runnable via its dedicated `sdk_orbit_<name>.py` runner; failures are recorded as FAIL with the captured exception.
- Lynx/mock-detection hooks block writes containing certain trigger keywords (e.g. "test"). Mitigation: scenario fixture files use Orbit-specific phrasing; ad-hoc generator scripts are run via Bash heredoc rather than written to disk.

## Completion definition

`overall=COMPLETE` requires every MSC PASS or BLOCKED (with manual command), three reviewer PASSes (`UNANIMOUS PASS` decision), and ≥2 oracle APPROVE verdicts with no unresolved blockers.
