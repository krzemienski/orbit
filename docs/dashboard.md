# Dashboard

`scripts/orbit_audit.py::render_dashboard()` writes `.claude/audits/latest/dashboard.html` — a self-contained static page that opens directly in any browser. No server. No external CDN.

## Sections

1. **Hero** — `ORBIT` logo, tagline ("Find drift. Close gaps. Restore alignment."), scope chip (window, sessions mined, plan sources, generated-at timestamp).
2. **Summary cards** — counts for intents, plan items, claims, gaps.
3. **Intent → Plan → Claim → Tool → Repo Matrix** — five-row table with counts and status hints.
4. **Intent Timeline** — most recent ≤20 intents with timestamp, kind, text.
5. **Claim Validation** — most recent ≤25 claims with id, status (color-coded), text. Validated=lime, contradicted/failed=red, else orange.
6. **Gaps** — gap cards colored by severity. High=red, medium=orange, low=blue.
7. **Uncertainty** — explicit list of unverified claims and ambiguous-evidence gaps.

## Brand palette

```css
--black:  #0A0A0B
--carbon: #0F1012
--white:  #F4F7FB
--light:  #C7CDD8
--lime:   #C6FF00   /* active, valid, complete */
--orange: #FF8A00   /* pending, attention */
--red:    #FF4D36   /* contradiction, severe */
--purple: #8B3DFF   /* analysis, session-only */
--blue:   #1E6BFF   /* plans, structure */
```

The hero uses lime + purple in the orb glyph. Dashboard sections use the palette consistently for severity and status semantics.

## Render-on-demand

```bash
bin/orbit-audit render-dashboard --evidence .claude/audits/latest/evidence.json --output /tmp/dashboard.html
```

`render-dashboard` is idempotent — same evidence in, same HTML out.

## Verification tokens

`validate_outputs.py` and `sdk_orbit_render_dashboard.py` verify the rendered HTML contains every required token: `ORBIT`, `Find drift`, all five brand color hex codes, `Timeline`, `Claim Validation`, `Uncertainty`, `Scope`, `Matrix`. A missing token is a `FAIL`.
