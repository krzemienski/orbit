# Scenarios

The harness ships 14 scenarios under `.orbit-sdk-harness/scenarios/`. Each has `README.md`, `prompt.md`, `expected-observations.md`, and `success-criteria.md`.

| ID | Name | Live SDK runs | Special evidence |
|---|---|---|---|
| 00 | Architecture Discovery | 1 | architecture map |
| 01 | Plan Gap | 1 | plan omission gap recognition |
| 02 | Later Correction Supersedes Plan | 1 | superseded gap recognition |
| 03 | Claim Unverified | 1 | claim-not-validated gap |
| 04 | Claim Contradicted by Repo | 1 | parser flag inspection |
| 05 | Dashboard Required | 1 | actual dashboard render + token check |
| 06 | Configurable Review Window | 3 | three scope flags |
| 07 | Hook Candidate Instruction | 1 | 4 direct hook invocations + candidate JSONL |
| 08 | Malformed JSONL | 1 | parser tolerance description |
| 09 | Instruction Ledger | 1 | actual ledger build + JSONL parse |
| 10 | Plugin Compliance | 1 | 5 static validators run |
| 11 | Skill Creator Review | 1 | per-skill scoring |
| 12 | Documentation Completeness | 1 | docs+HTML+diagrams audit |
| 13 | Installed Plugin Validation | 1 | feasibility report with manual commands |

Total live SDK runs: **16** (scenario 06 fires 3 times).

## Scenario discipline

- A scenario is `PASS` only if the per-run evidence shows a real `ResultMessage` AND the scenario-specific success criteria are met.
- `BLOCKED` is acceptable for environment-specific scenarios (e.g. installed-plugin discovery) and must be paired with a manual verification command.
- `FAIL` is recorded when the run completed but the success criteria were not met. Failures are surfaced in `orbit-validation-summary.md` and `orbit-final-pass-fail.md`.

## How scenarios are dispatched

`sdk_orbit_all.py` is the master orchestrator. Inline scenarios (00, 04, 06, 08, 13) call `run_query()` directly. Delegated scenarios (01, 02, 03, 05, 07, 09, 10, 11, 12) shell out to a per-scenario `sdk_orbit_*.py` runner so that scenario-specific evidence (e.g. dashboard render token check, candidate JSONL audit) is captured by the dedicated runner.
