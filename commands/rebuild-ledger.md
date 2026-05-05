# Rebuild Ledger

Replace the local durable instruction ledger by mining project sessions again.

```bash
orbit-audit build-ledger --project . --replace $ARGUMENTS
```

`$ARGUMENTS` may include scope flags (`--days N`, `--since YYYY-MM-DD`, `--from ... --to ...`).
