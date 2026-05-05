# Orbit Validation Summary

Generated: `2026-05-05T20:58:45Z` · Plugin root: `/Users/nick/Desktop/orbit` · Overall: **BLOCKED**

## Executive Summary

Orbit validation produced 114 checks across 8 sections. PASS=110, FAIL=0, BLOCKED=4.



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

Status: **BLOCKED**. See `orbit-installed-plugin-validation.md`.



## Skill Compliance

Frontmatter status: **PASS**. Skill Creator-style review status: **PASS**. See `orbit-skill-compliance.md` and `orbit-skill-creator-review.md`.



## Command Compliance

Status: **PASS**. See `orbit-command-compliance.md`.



## Hook Compliance

Status: **PASS**. See `orbit-hook-compliance.md`.



## Frontmatter Compliance

Status: **PASS**.



## SDK Scenario Results

Status: **PASS**.

| Check | Status | Evidence | Observed | Expected | Notes |
|---|---|---|---|---|---|
| `sdk_scenario_00-architecture-discovery` | **PASS** | `/Users/nick/Desktop/orbit/.orbit-sdk-harness/runs/20260505T204945Z-00-architecture-discovery/transcript.json` | got_result=True msgs=58 | ResultMessage in transcript.json | - |
| `sdk_scenario_01-plan-gap` | **PASS** | `/Users/nick/Desktop/orbit/.orbit-sdk-harness/runs/20260505T205031Z-01-plan-gap` | returncode=0 got_result=True | returncode=0 and ResultMessage in transcript | - |
| `sdk_scenario_02-correction-supersedes` | **PASS** | `/Users/nick/Desktop/orbit/.orbit-sdk-harness/runs/20260505T205110Z-02-correction-supersedes` | returncode=0 got_result=True | returncode=0 and ResultMessage in transcript | - |
| `sdk_scenario_03-claim-unverified` | **PASS** | `/Users/nick/Desktop/orbit/.orbit-sdk-harness/runs/20260505T205126Z-03-claim-unverified` | returncode=0 got_result=True | returncode=0 and ResultMessage in transcript | - |
| `sdk_scenario_04-claim-contradicted` | **PASS** | `/Users/nick/Desktop/orbit/.orbit-sdk-harness/runs/20260505T205148Z-04-claim-contradicted/transcript.json` | got_result=True msgs=34 | ResultMessage in transcript.json | - |
| `sdk_scenario_05-dashboard-required` | **PASS** | `/Users/nick/Desktop/orbit/.orbit-sdk-harness/runs/20260505T205207Z-05-dashboard-required` | returncode=0 got_result=True | returncode=0 and ResultMessage in transcript | - |
| `sdk_scenario_06-review-window-days7` | **PASS** | `/Users/nick/Desktop/orbit/.orbit-sdk-harness/runs/20260505T205224Z-06-review-window-days7/transcript.json` | got_result=True msgs=40 | ResultMessage in transcript.json | - |
| `sdk_scenario_06-review-window-since` | **PASS** | `/Users/nick/Desktop/orbit/.orbit-sdk-harness/runs/20260505T205311Z-06-review-window-since/transcript.json` | got_result=True msgs=43 | ResultMessage in transcript.json | - |
| `sdk_scenario_06-review-window-from-to` | **PASS** | `/Users/nick/Desktop/orbit/.orbit-sdk-harness/runs/20260505T205412Z-06-review-window-from-to/transcript.json` | got_result=True msgs=38 | ResultMessage in transcript.json | - |
| `sdk_scenario_07-hook-candidate` | **PASS** | `/Users/nick/Desktop/orbit/.orbit-sdk-harness/runs/20260505T205520Z-07-hook-candidate` | returncode=0 got_result=True | returncode=0 and ResultMessage in transcript | - |
| `sdk_scenario_08-malformed-jsonl` | **PASS** | `/Users/nick/Desktop/orbit/.orbit-sdk-harness/runs/20260505T205557Z-08-malformed-jsonl/transcript.json` | got_result=True msgs=34 | ResultMessage in transcript.json | - |
| `sdk_scenario_09-instruction-ledger` | **PASS** | `/Users/nick/Desktop/orbit/.orbit-sdk-harness/runs/20260505T205625Z-09-instruction-ledger` | returncode=0 got_result=True | returncode=0 and ResultMessage in transcript | - |
| `sdk_scenario_10-plugin-compliance` | **PASS** | `/Users/nick/Desktop/orbit/.orbit-sdk-harness/runs/20260505T205647Z-10-plugin-compliance` | returncode=0 got_result=True | returncode=0 and ResultMessage in transcript | - |
| `sdk_scenario_11-skill-creator-review` | **PASS** | `/Users/nick/Desktop/orbit/.orbit-sdk-harness/runs/20260505T205700Z-11-skill-creator-review` | returncode=0 got_result=True | returncode=0 and ResultMessage in transcript | - |
| `sdk_scenario_12-docs-completeness` | **PASS** | `/Users/nick/Desktop/orbit/.orbit-sdk-harness/runs/20260505T205717Z-12-docs-completeness` | returncode=0 got_result=True | returncode=0 and ResultMessage in transcript | - |
| `sdk_scenario_13-installed-plugin` | **PASS** | `/Users/nick/Desktop/orbit/.orbit-sdk-harness/runs/20260505T205800Z-13-installed-plugin/transcript.json` | got_result=True msgs=45 | ResultMessage in transcript.json | - |



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

- `orbit_installed` — Orbit not installed in current Claude Code environment Manual: `claude plugin list 2>&1 | grep -i orbit ; ls ~/.claude/plugins/ | grep -i orbit` (evidence: `/Users/nick/.claude/plugins/installed_plugins.json`)
- `installed_plugin_command_discovery` — `claude plugin list` is interactive; harness cannot enumerate slash commands non-interactively Manual: `claude /orbit:audit-gaps  # interactive verify` (evidence: `-`)
- `installed_plugin_skill_discovery` — Skill discovery is internal to the agent loop and not exposed via CLI flag Manual: `claude
then invoke a skill trigger phrase like 'audit this project for gaps'` (evidence: `-`)
- `installed_plugin_hook_configuration` — hook activation is internal to the running agent Manual: `cat ~/.claude/plugins/installed_plugins.json | grep -i orbit ; cat ~/.claude/settings.json | grep -i hooks` (evidence: `-`)



## Recommended Fixes

No outstanding fixes.



## Final Pass/Fail

**Overall: BLOCKED**
