# Plugin Validation

Plugin validation = "the files on disk match the Claude Code plugin contract". This is distinct from installed-plugin validation (see `installed-plugin-validation.md`), which asks "is the plugin loaded into the user's Claude Code environment".

## Files-on-disk contract

Required:

```text
.claude-plugin/plugin.json    parses; { name: "orbit", description: "...", version: "...", skills: "./skills", commands: "./commands", hooks: "./hooks/hooks.json" }
skills/<name>/SKILL.md        per-skill, with valid frontmatter
commands/<name>.md            per-slash-command
hooks/hooks.json              parses, references existing executable scripts
scripts/orbit_audit.py        engine
scripts/hook_*.py             hook scripts (executable)
bin/orbit-*                   thin wrappers around scripts/orbit_audit.py
README.md, CHANGELOG.md, PRD.md
```

## Manifest checks

- `name` is `orbit`
- `version` is a non-empty string
- `description` is a non-empty string
- `skills`, `commands`, `hooks` paths all resolve to existing files/dirs

## Skill checks (per skill)

- `SKILL.md` present
- frontmatter delimited
- `name` matches `^[a-z0-9-]+$` and length ≤ 64
- `description` non-empty, no XML tags, length ≤ 1024
- body non-empty

## Hook checks

- `hooks.json` parses as JSON
- top-level `hooks` is a non-empty object
- every event name is one of the recognized Claude Code events
- every command resolves to an existing file
- every hook script is executable
- every hook script accepts a benign JSON stdin payload and exits 0

## Command checks (per command)

- markdown body non-empty
- leading heading present
- ≥1 fenced example block
- helper or skill mapping mentioned
- `review-window` documents `--days`, `--since`, `--from`, `--to`
- `review-last-3-days` documents alias for `--days 3`

## Output checks (orbit-audit)

- `audit` subcommand exits 0 against bundled fixtures
- writes every required artifact (`evidence.json`, `gap-analysis.md`, `dashboard.html`, two `.mmd`, one `.csv`)
- evidence has every required schema field
- evidence `scope.days` echoes the `--days` input
- dashboard contains every brand token and section heading
- `build-ledger` produces valid JSONL + markdown companion
- `render-dashboard` exits 0
