# Orbit Validation Summary

Generated: `2026-05-05T21:41:18Z` · Plugin root: `/Users/nick/Desktop/orbit` · Overall: **BLOCKED**

## Executive Summary

Orbit validation produced 112 checks across 8 sections. PASS=98, FAIL=0, BLOCKED=14.



## Local Architecture Discovery

Status: **PASS** — see `.orbit-sdk-harness/reports/orbit-architecture-discovery.md`.



## GitHub or External Context Boundary

No GitHub repository context was assumed. The local filesystem is the source of truth. Documentation research used locally available material only — claude-agent-sdk imports were verified by `import claude_agent_sdk` against the installed package; plugin/hook/skill/command contracts were derived from observed manifest, hooks.json, SKILL.md, and command markdown files in the local Orbit project.



## Documentation Research

Status: **PASS**

```json

{
  "claude-agent-sdk": [
    "installed at /Users/nick/Library/Python/3.12/lib/python/site-packages/claude_agent_sdk",
    "version 0.1.68",
    "exports query() and ClaudeAgentOptions (verified by import)",
    "ClaudeAgentOptions accepts setting_sources for subscription auth (per harness usage in this repo)",
    "ResultMessage marks substantive completion of a query() stream (per Crucible reference harness)"
  ],
  "claude-code-plugin-manifest": [
    "manifest path is .claude-plugin/plugin.json (observed at /Users/nick/Desktop/orbit/.claude-plugin/plugin.json)",
    "required key 'name' present: yes",
    "recognized sub-paths in this manifest: ['commands', 'hooks', 'skills']",
    "manifest 'hooks' field points at hooks/hooks.json (observed in this manifest)",
    "manifest 'skills' and 'commands' fields are directory references relative to plugin root"
  ],
  "claude-code-hooks-io": [
    "hooks.json contains events: ['UserPromptExpansion', 'UserPromptSubmit']",
    "hooks read JSON payload from stdin and exit 0 on success (observed in scripts/hook_*.py)",
    "hooks may emit JSON on stdout under hookSpecificOutput.additionalContext (observed in hook_prompt_context.py)",
    "blocking patterns ({decision: 'block'} or 'approve') are deprecated; Orbit uses additionalContext for non-blocking hints",
    "available hook scripts: ['hook_prompt_context.py', 'hook_instruction_detector.py']"
  ],
  "claude-code-skill-frontmatter": [
    "observed 4 SKILL.md files",
    "each begins with --- ... --- YAML frontmatter (verified by file inspection)",
    "frontmatter declares 'name' and 'description' keys (verified by validate_skill_frontmatter.py)",
    "name pattern is lowercase letters, digits, hyphens only; max 64 chars (enforced by validator)",
    "description is plain text, no XML tags, max 1024 chars (enforced by validator)"
  ],
  "claude-code-slash-commands": [
    "observed 8 command markdown files",
    "each command file is a markdown document; filename is the slash command stem (e.g. audit-gaps.md => /orbit:audit-gaps)",
    "file content is the body of the slash command (heading + usage examples)",
    "Orbit commands suggest helper invocations using fenced code blocks (verified by validate_commands.py)",
    "no front matter is required for slash commands in Claude Code (observed in Orbit's command files)"
  ]
}

```



## Plugin Compliance

Status: **PASS**. See `orbit-plugin-compliance.md`.



## Installed-Plugin Validation

Status: **PASS**. See `orbit-installed-plugin-validation.md`.



## Skill Compliance

Frontmatter status: **PASS**. Skill Creator-style review status: **PASS**. See `orbit-skill-compliance.md` and `orbit-skill-creator-review.md`.



## Command Compliance

Status: **PASS**. See `orbit-command-compliance.md`.



## Hook Compliance

Status: **PASS**. See `orbit-hook-compliance.md`.



## Frontmatter Compliance

Status: **PASS**.



## SDK Scenario Results

Status: **BLOCKED**.

| Check | Status | Evidence | Observed | Expected | Notes |
|---|---|---|---|---|---|
| `sdk_scenario_00-architecture-discovery` | **BLOCKED** | `-` | --no-live-runs flag passed | real ResultMessage observed in transcript.json | live SDK runs disabled |
| `sdk_scenario_01-plan-gap` | **BLOCKED** | `-` | --no-live-runs flag passed | real ResultMessage observed in transcript.json | live SDK runs disabled |
| `sdk_scenario_02-correction-supersedes` | **BLOCKED** | `-` | --no-live-runs flag passed | real ResultMessage observed in transcript.json | live SDK runs disabled |
| `sdk_scenario_03-claim-unverified` | **BLOCKED** | `-` | --no-live-runs flag passed | real ResultMessage observed in transcript.json | live SDK runs disabled |
| `sdk_scenario_04-claim-contradicted` | **BLOCKED** | `-` | --no-live-runs flag passed | real ResultMessage observed in transcript.json | live SDK runs disabled |
| `sdk_scenario_05-dashboard-required` | **BLOCKED** | `-` | --no-live-runs flag passed | real ResultMessage observed in transcript.json | live SDK runs disabled |
| `sdk_scenario_06-review-window` | **BLOCKED** | `-` | --no-live-runs flag passed | real ResultMessage observed in transcript.json | live SDK runs disabled |
| `sdk_scenario_07-hook-candidate` | **BLOCKED** | `-` | --no-live-runs flag passed | real ResultMessage observed in transcript.json | live SDK runs disabled |
| `sdk_scenario_08-malformed-jsonl` | **BLOCKED** | `-` | --no-live-runs flag passed | real ResultMessage observed in transcript.json | live SDK runs disabled |
| `sdk_scenario_09-instruction-ledger` | **BLOCKED** | `-` | --no-live-runs flag passed | real ResultMessage observed in transcript.json | live SDK runs disabled |
| `sdk_scenario_10-plugin-compliance` | **BLOCKED** | `-` | --no-live-runs flag passed | real ResultMessage observed in transcript.json | live SDK runs disabled |
| `sdk_scenario_11-skill-creator-review` | **BLOCKED** | `-` | --no-live-runs flag passed | real ResultMessage observed in transcript.json | live SDK runs disabled |
| `sdk_scenario_12-docs-completeness` | **BLOCKED** | `-` | --no-live-runs flag passed | real ResultMessage observed in transcript.json | live SDK runs disabled |
| `sdk_scenario_13-installed-plugin` | **BLOCKED** | `-` | --no-live-runs flag passed | real ResultMessage observed in transcript.json | live SDK runs disabled |



## Test Prompts Used

See per-scenario `prompt.md` files under `.orbit-sdk-harness/runs/` for the exact prompts dispatched to `query()`.



## Observed Artifacts

Each run directory contains `transcript.json`, `session-id.txt`, `jsonl-pointer.txt`, `summary.json`, `started-at.txt`, `finished-at.txt`, `got-result.txt`, optional `exception.txt`, and `debug.log`. The JSONL pointer references `~/.claude/projects/<encoded-cwd>/<session-id>.jsonl` — the load-bearing artifact Orbit itself mines.



## Dashboard Verification

Status: **PASS**. See `orbit-dashboard-verification.md`.



## Documentation Completeness

Status: **PASS**. See `orbit-docs-compliance.md`.



## Known Failures

None.



## Blocked Checks (Manual Verification Required)

- `sdk_scenario_00-architecture-discovery` — live SDK runs disabled Manual: `python3 .orbit-sdk-harness/sdk_orbit_all.py --plugin-root . --output .orbit-sdk-harness/reports` (evidence: `-`)
- `sdk_scenario_01-plan-gap` — live SDK runs disabled Manual: `python3 .orbit-sdk-harness/sdk_orbit_all.py --plugin-root . --output .orbit-sdk-harness/reports` (evidence: `-`)
- `sdk_scenario_02-correction-supersedes` — live SDK runs disabled Manual: `python3 .orbit-sdk-harness/sdk_orbit_all.py --plugin-root . --output .orbit-sdk-harness/reports` (evidence: `-`)
- `sdk_scenario_03-claim-unverified` — live SDK runs disabled Manual: `python3 .orbit-sdk-harness/sdk_orbit_all.py --plugin-root . --output .orbit-sdk-harness/reports` (evidence: `-`)
- `sdk_scenario_04-claim-contradicted` — live SDK runs disabled Manual: `python3 .orbit-sdk-harness/sdk_orbit_all.py --plugin-root . --output .orbit-sdk-harness/reports` (evidence: `-`)
- `sdk_scenario_05-dashboard-required` — live SDK runs disabled Manual: `python3 .orbit-sdk-harness/sdk_orbit_all.py --plugin-root . --output .orbit-sdk-harness/reports` (evidence: `-`)
- `sdk_scenario_06-review-window` — live SDK runs disabled Manual: `python3 .orbit-sdk-harness/sdk_orbit_all.py --plugin-root . --output .orbit-sdk-harness/reports` (evidence: `-`)
- `sdk_scenario_07-hook-candidate` — live SDK runs disabled Manual: `python3 .orbit-sdk-harness/sdk_orbit_all.py --plugin-root . --output .orbit-sdk-harness/reports` (evidence: `-`)
- `sdk_scenario_08-malformed-jsonl` — live SDK runs disabled Manual: `python3 .orbit-sdk-harness/sdk_orbit_all.py --plugin-root . --output .orbit-sdk-harness/reports` (evidence: `-`)
- `sdk_scenario_09-instruction-ledger` — live SDK runs disabled Manual: `python3 .orbit-sdk-harness/sdk_orbit_all.py --plugin-root . --output .orbit-sdk-harness/reports` (evidence: `-`)
- `sdk_scenario_10-plugin-compliance` — live SDK runs disabled Manual: `python3 .orbit-sdk-harness/sdk_orbit_all.py --plugin-root . --output .orbit-sdk-harness/reports` (evidence: `-`)
- `sdk_scenario_11-skill-creator-review` — live SDK runs disabled Manual: `python3 .orbit-sdk-harness/sdk_orbit_all.py --plugin-root . --output .orbit-sdk-harness/reports` (evidence: `-`)
- `sdk_scenario_12-docs-completeness` — live SDK runs disabled Manual: `python3 .orbit-sdk-harness/sdk_orbit_all.py --plugin-root . --output .orbit-sdk-harness/reports` (evidence: `-`)
- `sdk_scenario_13-installed-plugin` — live SDK runs disabled Manual: `python3 .orbit-sdk-harness/sdk_orbit_all.py --plugin-root . --output .orbit-sdk-harness/reports` (evidence: `-`)



## Recommended Fixes

No outstanding fixes.



## Final Pass/Fail

**Overall: BLOCKED**
