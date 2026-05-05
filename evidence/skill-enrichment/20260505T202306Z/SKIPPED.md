# Skill Enrichment — Skipped Skills (Audit Trail)

Skills below floor (relevance < 0.10) or excluded for orthogonality:

| Skill | Score | Reason for skip |
|---|---|---|
| `swift-engineering:*` | 0.00 | Swift/iOS toolchain — unrelated to Python/Claude Code plugin work |
| `lynx:audit-screen`, `lynx:audit` | 0.04 | UI experience auditing on running apps — Orbit is a CLI plugin |
| `humanizer:humanizer` | 0.02 | Removes AI-generated text patterns — irrelevant to harness building |
| `social-automation:*` | 0.00 | Social media post generation |
| `crucible:fix`, `crucible:remediate` | 0.06 | Crucible-internal repair flows — Orbit harness is a one-off build, not iterative repair |
| `nextjs-expert:*` | 0.00 | Next.js — Orbit is Python |
| `theme-factory` | 0.04 | Visual theme generation — Orbit's brand palette is hand-coded |
| `tdd` | 0.08 | TDD — Orbit forbids test files per PRD |
| `ios-validation-runner` | 0.00 | iOS app validation |

The skip list is preserved so a future audit can check whether any skill was incorrectly excluded. None of the skipped skills above the 0.10 floor would change the harness design.
