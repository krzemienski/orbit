# Review Window

Run a configurable recent-window Orbit audit.

Default: `--days 3`.

Examples:

```text
/orbit:review-window --days 7 Find what changed over the last week.
/orbit:review-window --since 2026-05-01 Find missed instructions since May 1.
/orbit:review-window --from 2026-05-01 --to 2026-05-04 Audit this exact window.
```

Suggested helper:

```bash
orbit-audit audit --days 3 --project . --validate-codebase --dashboard
```
