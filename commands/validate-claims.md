# Validate Claims

Validate assistant completion claims against tool evidence and current repo state.

```bash
orbit-audit validate-claims --project . --evidence .claude/audits/latest/evidence.json $ARGUMENTS
```

`$ARGUMENTS` may override `--evidence <path>` or add scope flags.
