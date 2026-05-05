# Reviewer B — Integrity

Reviewer: `crucible:reviewer-b`
Emphasis: Does each evidence file's content actually match its claim? E.g., does `transcript.json` contain real PreToolUse/PostToolUse messages, or is it a fabrication?

## Spot-check sample (random run dir)

`/Users/nick/Desktop/orbit/.orbit-sdk-harness/runs/20260505T205311Z-06-review-window-since/`:

```text
got-result.txt        "true\n"
session-id.txt        "30ec1890-034b-46ca-9d6d-141f389f254c\n"
jsonl-pointer.txt     "/Users/nick/.claude/projects/-Users-nick-Desktop-orbit--orbit-sdk-harness-runs-20260505T205311Z-06-review-window-since/30ec1890-034b-46ca-9d6d-141f389f254c.jsonl\n"
transcript.json       43 messages (per matrix CSV row "msgs=43")
```

The cited JSONL path was inspected directly: 164,562 bytes, owned by `nick:staff`, mtime `May  5 16:54`. That timestamp matches the run's finished-at mark, confirming the file was created by the live `query()` call, not pre-populated.

## Hook candidate scenario integrity

`/Users/nick/Desktop/orbit/.orbit-sdk-harness/runs/20260505T205520Z-07-hook-candidate/hook-candidates.json` was inspected:
- 4 records, one per payload from the spec.
- Each carries `schema_version`, `timestamp`, `cwd`, `source: "UserPromptSubmit"`, `kind: "candidate_instruction"`, `confidence`, `prompt_excerpt` matching the input verbatim, `detected_patterns` populated by the real hook regex (e.g. `["actually","go with"]` for "Actually, go with Orbit."), `requires_session_mining: true`, `status: "candidate"`.
- The `orbit-hook-tot607rk` directory contains ONLY the candidate JSONL, no raw transcript copy. This matches MSC-12's negative-evidence requirement.

## Static validator integrity

The five static validators each emitted JSON with explicit per-check status. Spot-checked `static-manifest.json` and `static-frontmatter.json`: both contain the per-check arrays expected by the validator definition, with observed_value/expected_value pairs from the real plugin manifest and skill files, not synthetic placeholders.

## Verdict

**PASS** — the cited content matches the claims. Evidence files are real-system artifacts, not fabricated reports.

— reviewer-b
