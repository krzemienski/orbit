# Orbit Documentation

**Find drift. Close gaps. Restore alignment.**

Orbit is a native Claude Code plugin for intent mining, gap analysis, claim validation, codebase truth checks, remediation planning, and dashboard visualization. This documentation suite covers installation, usage, the evidence model, the SDK validation harness, every scenario the harness exercises, and how to validate Orbit both as files on disk and as an installed plugin.

## Index

| Doc | Purpose |
|---|---|
| [install.md](install.md) | Plugin install + dependency setup |
| [usage.md](usage.md) | Day-to-day usage and command examples |
| [commands.md](commands.md) | Every `/orbit:*` slash command |
| [hooks.md](hooks.md) | The `UserPromptSubmit` and `UserPromptExpansion` hooks |
| [skills.md](skills.md) | The four Orbit skills |
| [evidence-model.md](evidence-model.md) | The evidence schema and ranking rules |
| [validation.md](validation.md) | What Orbit means by "validated" |
| [sdk-harness.md](sdk-harness.md) | The `.orbit-sdk-harness/` runner |
| [scenarios.md](scenarios.md) | All 14 SDK scenarios |
| [dashboard.md](dashboard.md) | Dashboard sections + brand palette |
| [reports.md](reports.md) | Reports written by the harness |
| [compliance.md](compliance.md) | Plugin compliance checks |
| [plugin-validation.md](plugin-validation.md) | Plugin manifest + structure validation |
| [skill-creator-review.md](skill-creator-review.md) | How Orbit skills score on the Skill Creator rubric |
| [troubleshooting.md](troubleshooting.md) | Common failure modes and fixes |
| [diagrams.md](diagrams.md) | Mermaid diagrams index |
| [validation-research.md](validation-research.md) | Documentation sources consulted |
| [architecture.md](architecture.md) | Local architecture map |
| [installed-plugin-validation.md](installed-plugin-validation.md) | What can and cannot be checked non-interactively |

## Brand

Flat black base, hyper-accent palette: lime `#C6FF00`, orange `#FF8A00`, red `#FF4D36`, purple `#8B3DFF`, blue `#1E6BFF`. The dashboard, every doc HTML draft, and every report follow this palette.

## Iron Rule

Plans are evidence, not the complete historical record. Assistant claims are claims, not proof. Codebase validation is required before completion is trusted.
