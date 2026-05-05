# Skill Enrichment — Per-Candidate Rationale

Each candidate includes ≥3 sentences of rationale linking the skill to the Orbit harness build task.

## 1. `testing-cc-plugins-python-sdk` (score 0.58)

This skill is the canonical guide for *exactly* what this harness does: programmatically testing a Claude Code plugin using the Python Agent SDK. It names the SDK lifecycle pattern (`async with ClaudeCodeSession`), the streaming message contract (`text`, `tool_use`, `tool_result`), the timeout pattern, and the plugin-test pattern (cwd + allowed_tools + verifying tool calls in the response). The Orbit harness uses every one of these primitives — `claude_agent_sdk.query()` is the older API equivalent of `ClaudeCodeSession.stream()`, and the per-scenario runners follow the prescribed pattern of capturing `tool_use` and `tool_result` messages from the live stream. Including this skill in the planner's required list ensures executors do not invent ad-hoc SDK consumption code when a documented pattern already exists.

## 2. `superpowers-developing-for-claude-code:developing-claude-code-plugins` (score 0.55)

This skill is the canonical reference for Claude Code plugin development end-to-end: the directory layout (`.claude-plugin/plugin.json`, `skills/`, `commands/`, `hooks/`), the marketplace pattern, the install/uninstall test loop, and the version-and-tag release workflow. Orbit IS a Claude Code plugin, and the harness must validate Orbit's structure against this exact contract. The skill's "critical rules" (`.claude-plugin/` contains ONLY manifests; use `${CLAUDE_PLUGIN_ROOT}` for portable paths; relative paths in plugin.json; executable scripts) are the basis for `validate_plugin_manifest.py`, `validate_hooks.py`, and the bin-wrapper convention.

## 3. `python-agent-sdk` (score 0.42)

The Orbit validation harness is built around real `claude_agent_sdk.query()` invocations, with subscription-mode auth via `setting_sources=["user"]` and per-run capture of `transcript.json`, `session-id.txt`, and the corresponding `~/.claude/projects/<encoded-cwd>/<session-id>.jsonl` pointer. The `python-agent-sdk` skill provides the broader best-practices surface (async stream consumption, `ResultMessage` detection, `ClaudeAgentOptions` configuration). Used together with #1 above, it ensures the harness consumes the SDK correctly and produces real session JSONL evidence.

## 4. `claude-api` (score 0.38)

Even though the harness uses `claude-agent-sdk` rather than the raw Anthropic SDK, the underlying calls are still Claude API calls. The `claude-api` skill provides the broader context for prompt caching, model selection, and session lifecycle that the harness must respect (e.g., prompt caching prefix invalidation, model ID format). Orbit also documents that its scenario prompts are short and reusable, which aligns with this skill's caching guidance.

## 5. `functional-validation` (score 0.36)

Orbit's PRD explicitly forbids test files, mocks, and stubs. Every validation must be a real run against the real system with captured evidence. The `functional-validation` skill is the canonical 4-step protocol (build → run → exercise → capture evidence) that this harness implements per scenario. Following this skill prevents the temptation to fall back on synthetic green checks when a real run is harder to wire up.

## 6. `validationforge:no-mocking-validation-gates` (score 0.34)

The Iron Rule for Orbit is "no mocks, no fake transcripts, no synthetic pass results, no placeholders." This ValidationForge skill encodes that exact rule and provides enforcement guidance: every PASS must cite a real evidence path; every FAIL must include a failure_reason; every BLOCKED must include a manual_verification_command. Orbit's `CheckRecord` dataclass and `aggregate_status()` aggregator implement this directly.

## 7. `validationforge:e2e-validate` (score 0.31)

The harness is end-to-end: it runs static validators, dispatches 16 live SDK queries across 13 scenarios (06 fires three times), and renders 13 reports. The `e2e-validate` skill provides the orchestration pattern for "start HERE when validating" — preflight, plan, execute, capture, verdict. Orbit's `sdk_orbit_all.py` follows this pattern step for step.

## 8. `validationforge:create-validation-plan` (score 0.28)

Before running anything, the harness must define MSCs (Mandatory Success Criteria) per feature. The `create-validation-plan` skill is the standard pattern for that — define each journey, its PASS criteria, and the evidence required. Orbit's PLAN.md mirrors this structure (one MSC per feature × scenario).

## 9. `validationforge:gate-validation-discipline` (score 0.25)

Crucible Phase 8 (3-reviewer consensus), Phase 9 (3-oracle quorum), and Phase 10 (completion gate) are gate evaluations. This skill provides the discipline for never silently downgrading a FAIL to a warning, and never silently upgrading a BLOCKED to PASS. Orbit's `aggregate_status()` follows this strictly: any FAIL → section FAIL; mixed PASS+BLOCKED → BLOCKED.

## 10. `validationforge:verification-before-completion` (score 0.22)

Before marking the entire forge run complete, the gate must verify every MSC has cited evidence and every cited path is non-empty. This skill enforces "evidence before completion." Orbit's completion gate (`evidence/completion-gate/report.json`) walks every MSC, verifies the cited path exists and is non-empty, and only then writes `overall=COMPLETE`.
