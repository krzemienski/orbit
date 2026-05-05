# Orbit Architecture Discovery

Status: **PASS** · Generated: `2026-05-05T20:58:45Z` · Root: `/Users/nick/Desktop/orbit`

## Inventory

```json

{
  "plugin_root": "/Users/nick/Desktop/orbit",
  "exists": true,
  "manifest": "/Users/nick/Desktop/orbit/.claude-plugin/plugin.json",
  "skills_dir": "/Users/nick/Desktop/orbit/skills",
  "commands_dir": "/Users/nick/Desktop/orbit/commands",
  "hooks_dir": "/Users/nick/Desktop/orbit/hooks",
  "scripts_dir": "/Users/nick/Desktop/orbit/scripts",
  "bin_dir": "/Users/nick/Desktop/orbit/bin",
  "skills": [
    {
      "name": "gap-analysis",
      "skill_md": "/Users/nick/Desktop/orbit/skills/gap-analysis/SKILL.md"
    },
    {
      "name": "instruction-ledger",
      "skill_md": "/Users/nick/Desktop/orbit/skills/instruction-ledger/SKILL.md"
    },
    {
      "name": "plan-execution-audit",
      "skill_md": "/Users/nick/Desktop/orbit/skills/plan-execution-audit/SKILL.md"
    },
    {
      "name": "validation-pairing",
      "skill_md": "/Users/nick/Desktop/orbit/skills/validation-pairing/SKILL.md"
    }
  ],
  "commands": [
    {
      "name": "audit-gaps",
      "path": "/Users/nick/Desktop/orbit/commands/audit-gaps.md"
    },
    {
      "name": "compare-plan",
      "path": "/Users/nick/Desktop/orbit/commands/compare-plan.md"
    },
    {
      "name": "mine-intent",
      "path": "/Users/nick/Desktop/orbit/commands/mine-intent.md"
    },
    {
      "name": "rebuild-ledger",
      "path": "/Users/nick/Desktop/orbit/commands/rebuild-ledger.md"
    },
    {
      "name": "render-dashboard",
      "path": "/Users/nick/Desktop/orbit/commands/render-dashboard.md"
    },
    {
      "name": "review-last-3-days",
      "path": "/Users/nick/Desktop/orbit/commands/review-last-3-days.md"
    },
    {
      "name": "review-window",
      "path": "/Users/nick/Desktop/orbit/commands/review-window.md"
    },
    {
      "name": "validate-claims",
      "path": "/Users/nick/Desktop/orbit/commands/validate-claims.md"
    }
  ],
  "hooks_file": "/Users/nick/Desktop/orbit/hooks/hooks.json",
  "scripts": [
    "/Users/nick/Desktop/orbit/scripts/hook_instruction_detector.py",
    "/Users/nick/Desktop/orbit/scripts/hook_prompt_context.py",
    "/Users/nick/Desktop/orbit/scripts/orbit_audit.py"
  ],
  "bin": [
    {
      "name": "orbit-audit",
      "path": "/Users/nick/Desktop/orbit/bin/orbit-audit",
      "executable": true
    },
    {
      "name": "orbit-dashboard",
      "path": "/Users/nick/Desktop/orbit/bin/orbit-dashboard",
      "executable": true
    },
    {
      "name": "orbit-ledger",
      "path": "/Users/nick/Desktop/orbit/bin/orbit-ledger",
      "executable": true
    }
  ],
  "readme": "/Users/nick/Desktop/orbit/README.md",
  "changelog": "/Users/nick/Desktop/orbit/CHANGELOG.md",
  "prd": "/Users/nick/Desktop/orbit/PRD.md",
  "claude_md": "/Users/nick/Desktop/orbit/CLAUDE.md",
  "tests_dir": "/Users/nick/Desktop/orbit/tests",
  "examples_dir": "/Users/nick/Desktop/orbit/examples"
}

```

## Checks

| Check | Status | Evidence | Observed | Expected | Notes |
|---|---|---|---|---|---|
| `architecture_plugin_root_exists` | **PASS** | `/Users/nick/Desktop/orbit` | present | plugin root exists | - |
| `architecture_manifest_present` | **PASS** | `/Users/nick/Desktop/orbit/.claude-plugin/plugin.json` | present | manifest discoverable | - |
| `architecture_skills_dir_present` | **PASS** | `/Users/nick/Desktop/orbit/skills` | present | skills_dir discoverable | - |
| `architecture_commands_dir_present` | **PASS** | `/Users/nick/Desktop/orbit/commands` | present | commands_dir discoverable | - |
| `architecture_hooks_file_present` | **PASS** | `/Users/nick/Desktop/orbit/hooks/hooks.json` | present | hooks_file discoverable | - |
| `architecture_scripts_dir_present` | **PASS** | `/Users/nick/Desktop/orbit/scripts` | present | scripts_dir discoverable | - |
| `architecture_bin_dir_present` | **PASS** | `/Users/nick/Desktop/orbit/bin` | present | bin_dir discoverable | - |
| `architecture_readme_present` | **PASS** | `/Users/nick/Desktop/orbit/README.md` | present | readme discoverable | - |
| `architecture_changelog_present` | **PASS** | `/Users/nick/Desktop/orbit/CHANGELOG.md` | present | changelog discoverable | - |
| `architecture_prd_present` | **PASS** | `/Users/nick/Desktop/orbit/PRD.md` | present | prd discoverable | - |
| `architecture_skill_count` | **PASS** | `/Users/nick/Desktop/orbit/skills` | 4 skills | >=4 skills | - |
| `architecture_command_count` | **PASS** | `/Users/nick/Desktop/orbit/commands` | 8 commands | >=8 commands | - |
| `architecture_bin_wrappers` | **PASS** | `/Users/nick/Desktop/orbit/bin` | 3 bin wrappers | >=1 bin wrapper | - |
