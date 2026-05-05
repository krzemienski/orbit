# Review Last 3 Days

Legacy alias for `/orbit:review-window --days 3`.

```bash
orbit-audit audit --project . --validate-codebase --dashboard --days 3 $ARGUMENTS
```

`$ARGUMENTS` is appended after the fixed `--days 3` so a user typing `/orbit:review-last-3-days --validate-codebase` does not break, but the canonical scope is always `--days 3`.
