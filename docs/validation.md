# Validation

Orbit distinguishes three things commonly confused:

| | Compilation | Execution | Validation |
|---|---|---|---|
| What it proves | Syntax is parseable | Code ran without crashing | The user's intent is satisfied AND the output matches expectations |
| Orbit treats it as | Necessary, not sufficient | Necessary, not sufficient | Sufficient when paired with cited evidence |

A passing build does not validate a feature. A green run does not validate a feature. Only an evidence-backed cross-check against intent, plan, claim, tool evidence, AND codebase state validates a feature.

## Default safe checks

Without an explicit validation config, Orbit performs only non-destructive checks:

- `file_exists`
- `text_exists`
- `symbol-like text exists`
- `artifact_exists`
- `script_executable`

Any check that would *run* a command requires explicit configuration. Orbit will never auto-execute a build, deploy, or shell command.

## Evidence rules for the SDK harness

Every PASS verdict produced by the SDK harness must:

- Cite a specific evidence path (file or directory).
- Reference an observed value (read from disk or returned by a real subprocess).
- Reference an expected value (written into the check definition before the run).

Statuses:

- `PASS` — check ran, observed value matches expected.
- `FAIL` — check ran, observed value does not match expected. Includes a `failure_reason`.
- `BLOCKED` — check could not run for environmental, permissions, missing-install, missing-documentation, or safety reasons. Includes a `blocker_reason` and a `manual_verification_command`.

`BLOCKED` is never silently upgraded to `PASS`. `FAIL` is never silently downgraded to a warning.

## Functional validation in plans

Every Orbit plan must include a functional validation phase with evidence checkpoints. Plans must NOT include "write tests" or "add coverage" — Orbit validates by running the real system, not by inserting harness scaffolding into source code.
