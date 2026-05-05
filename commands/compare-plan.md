# Compare Plan

Compare a plan with session evidence, assistant claims, tool evidence, and current codebase state.

```bash
orbit-audit compare-plan --plan PLAN.md --project . --validate-codebase $ARGUMENTS
```

If `$ARGUMENTS` already contains a `--plan PATH`, use that instead of the default `PLAN.md`. Pass through any scope flags.
