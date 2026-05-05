# Scenario 04 — Claim Contradicted by Repo

Verify Orbit can detect a claim that contradicts current repo state. The orbit-audit CLI does support `--from` and `--to` (lines 616-617 of `scripts/orbit_audit.py`); the agent should report the claim as VALIDATED, but recognize that *if* the flags were absent the gap category would be `claim-contradicted` with severity medium-high.
