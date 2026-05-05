---
name: instruction-ledger
description: Builds and uses Orbit’s local durable-instruction ledger for requests about project memory, prior instructions, corrections, pivots, renames, “what did I tell you,” “rebuild the ledger,” or extracting user intent from session history.
---

# Orbit Instruction Ledger

Use this skill to mine durable user instructions and maintain a compact local ledger.

## Durable Instruction Signals

Look for:

- actually
- no, instead
- we decided
- go with
- settled on
- from now on
- make sure
- must include
- do not
- you forgot
- this is wrong
- changed our mind

## Ledger Outputs

```text
.claude/audits/intent-ledger.jsonl
.claude/audits/intent-ledger.md
```

## Rules

- The ledger is an index, not proof by itself.
- Promote candidates only when supported by session or user-provided evidence.
- Track superseded instructions.
- Prefer later direct user corrections over older broad assumptions.
