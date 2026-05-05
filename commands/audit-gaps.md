# Audit Gaps

Run Orbit gap analysis for the current project.

Use this command when the user asks to audit, find missed work, compare intent to execution, validate claims, or generate remediation recommendations.

User-supplied arguments after the slash command name are passed through verbatim. If none are provided, run with the defaults.

```bash
orbit-audit audit --project . --validate-codebase --dashboard $ARGUMENTS
```

If `$ARGUMENTS` is empty:

```bash
orbit-audit audit --project . --validate-codebase --dashboard
```
