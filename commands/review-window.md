# Review Window

Run a configurable recent-window Orbit audit. Default: `--days 3`. Supports `--days N`, `--since YYYY-MM-DD`, and `--from YYYY-MM-DD --to YYYY-MM-DD`.

The user-supplied arguments after the command name are passed through verbatim. If no scope flags are provided, fall back to `--days 3`.

Run this exact helper, substituting `$ARGUMENTS` with whatever the user typed after the slash command:

```bash
orbit-audit audit --project . --validate-codebase --dashboard $ARGUMENTS
```

If `$ARGUMENTS` is empty, default to `--days 3`:

```bash
orbit-audit audit --project . --validate-codebase --dashboard --days 3
```

Examples:

```text
/orbit:review-window --days 7                                         → orbit-audit audit ... --days 7
/orbit:review-window --since 2026-05-01                               → orbit-audit audit ... --since 2026-05-01
/orbit:review-window --from 2026-05-01 --to 2026-05-04                → orbit-audit audit ... --from 2026-05-01 --to 2026-05-04
/orbit:review-window                                                  → orbit-audit audit ... --days 3
```

After the helper finishes, read `.claude/audits/latest/evidence.json` and confirm the `scope` object echoes the user's selection (`scope.days`, `scope.since`, `scope.from`, `scope.to`).
