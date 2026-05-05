# Success Criteria

- `runs/<id>-00-architecture-discovery/transcript.json` exists, non-empty, and contains a `ResultMessage`.
- `runs/<id>-00-architecture-discovery/got-result.txt` is `true`.
- `runs/<id>-00-architecture-discovery/jsonl-pointer.txt` references a real `~/.claude/projects/<encoded-cwd>/<session-id>.jsonl` path.
- The agent's response references at least three of: `.claude-plugin/plugin.json`, `scripts/orbit_audit.py`, `skills/`, `commands/`, `hooks/hooks.json`, `bin/orbit-audit`.
