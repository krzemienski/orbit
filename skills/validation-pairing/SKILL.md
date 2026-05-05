---
name: validation-pairing
description: Validates assistant completion claims against tool evidence and codebase truth for requests like “did it actually do it,” “validate the claims,” “prove it was completed,” “check against the repo,” or “functional validation.”
---

# Orbit Validation Pairing

Use this skill when the user asks whether claimed work was actually completed.

## Validation Contract

For every completion claim:

1. Find the claim.
2. Find related tool evidence.
3. Inspect relevant files and artifacts.
4. Run safe configured validation commands only when explicitly configured.
5. Mark the claim as validated, partially validated, unverified, contradicted, stale, or uncertain.

## Default Safe Checks

Without a validation config, perform only non-destructive checks:

- file exists,
- text exists,
- symbol-like text exists,
- artifact exists,
- executable bit set.
