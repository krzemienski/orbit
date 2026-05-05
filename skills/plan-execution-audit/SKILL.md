---
name: plan-execution-audit
description: Compares written plans against session evidence, assistant claims, tool evidence, and current codebase state for requests like “compare to the plan,” “does this match the plan,” “what plan items are missing,” or “what got superseded.”
---

# Orbit Plan Execution Audit

Use this skill when the user wants to compare a plan to what actually happened.

## Workflow

1. Extract plan requirements, headings, checklists, and acceptance criteria.
2. Mine sessions for later user corrections and session-only decisions.
3. Extract assistant claims of completion.
4. Link plan items to tool evidence and repo validation.
5. Mark each item as complete, partial, unverified, contradicted, stale, or superseded.

## Rule

A plan omission means only “not found in the plan.” It does not prove the user never requested it.
