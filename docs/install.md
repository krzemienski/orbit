# Installing Orbit

Orbit is a native Claude Code plugin. There is no Dockerfile, no `pyproject.toml`, and no Python package step.

## Prerequisites

- macOS or Linux (Windows path encoding is supported but not the focus of this validation harness).
- Python 3.10+ (Orbit's helper scripts are stdlib-only).
- Claude Code CLI (`claude` on `PATH`). Verify with `claude --version`.
- For the SDK validation harness only: `claude-agent-sdk>=0.1.68` (`pip install -r .orbit-sdk-harness/requirements.txt`).

## Plugin install

Place the Orbit folder under your Claude Code plugin location, or install through your local marketplace flow. The expected on-disk shape is:

```text
orbit/
  .claude-plugin/plugin.json
  skills/
    gap-analysis/SKILL.md
    instruction-ledger/SKILL.md
    plan-execution-audit/SKILL.md
    validation-pairing/SKILL.md
  commands/
    audit-gaps.md
    mine-intent.md
    validate-claims.md
    render-dashboard.md
    compare-plan.md
    review-window.md
    review-last-3-days.md
    rebuild-ledger.md
  hooks/
    hooks.json
  scripts/
    orbit_audit.py
    hook_instruction_detector.py
    hook_prompt_context.py
  bin/
    orbit-audit
    orbit-dashboard
    orbit-ledger
```

## Verify the install

Two complementary verifications:

```bash
# 1. As files (works without Claude Code running)
python3 .orbit-sdk-harness/validate_plugin_manifest.py --plugin-root .
python3 .orbit-sdk-harness/validate_skill_frontmatter.py --skills-dir ./skills
python3 .orbit-sdk-harness/validate_hooks.py --plugin-root .
python3 .orbit-sdk-harness/validate_commands.py --plugin-root .
python3 .orbit-sdk-harness/validate_outputs.py --plugin-root .

# 2. As an installed plugin (interactive)
claude  # then type a trigger phrase, e.g. "audit this project for missed instructions"
```

`bin/orbit-*` are shell wrappers that resolve `CLAUDE_PLUGIN_ROOT` (set by Claude Code at runtime) or fall back to the parent of the script directory. Both modes work.

## No Docker, no package layout

The PRD explicitly forbids a Dockerfile, docker-compose, or Python package project. Helpers are run as `python3 scripts/orbit_audit.py ...` or `bin/orbit-audit ...`. If you're tempted to add one, the PRD is the source of truth.
