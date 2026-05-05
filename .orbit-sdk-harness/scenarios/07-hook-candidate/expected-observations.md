# Expected Observations

- Candidate JSONL records are appended for each matching prompt.
- Each record carries timestamp, cwd, detected_patterns, prompt_excerpt, status.
- No raw transcript copy is created.
- The hook does not block the user prompt.
