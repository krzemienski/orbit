# Mine Intent

Build or update Orbit's durable instruction ledger from sessions and candidate instructions.

```bash
orbit-audit build-ledger --project . --days 30 $ARGUMENTS
```

`$ARGUMENTS` may include scope flags (`--days N`, `--since YYYY-MM-DD`, `--from ... --to ...`) and/or `--replace` to truncate before appending. If `$ARGUMENTS` is empty, the helper above runs as-is.
