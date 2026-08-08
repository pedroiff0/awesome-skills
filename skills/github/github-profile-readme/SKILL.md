---
name: github-profile-readme
description: Build or rewrite a GitHub profile README (the username/username special repo) with a personalized theme — animated SVG banner, stats cards, contribution snake, tech badges, project/research tables. Includes the git conflict pitfall when the local clone is stale vs GitHub web edits, and the PyYAML `on:` quirk for workflow verification.
---

# GitHub Profile README (astronomy × computing theme)

Trigger: user asks to "personalize my GitHub profile README", "make my profile cool/fancy", "add stats/banner/snake to my profile", or any task touching `github.com/<user>/<user>` README.md.

## Pre-flight
- Profile repo is `github.com/<user>/<user>`, branch `main`.
- ALWAYS check remote first: `git fetch origin && git show origin/main:README.md`. The user often edits README.md directly on github.com web after your last clone — a stale local clone is the #1 pitfall (see below).

## Anatomy of a rich profile README
1. Animated banner (SVG) at top — see references/starfield-banner.md for a self-contained Python generator writing `assets/starfield.svg` (twinkling stars + constellation lines + shooting star). Embed via raw.githubusercontent URL.
2. Identity header: name, tagline, contact badges (shields.io `for-the-badge` with emoji).
3. "Mission"/status block — terminal-style ASCII box is a nice touch.
4. Stats cards. **ALWAYS 200-check every external URL before embedding** (see Pitfall below —
   popular services go down). Anchors that currently work:
   - `https://github-readme-activity-graph.vercel.app/graph?username=USER&theme=radical` — contribution-area graph (reliable).
   - `https://github-readme-streak-stats.herokuapp.com/?user=USER&theme=radical` — streak card (reliable).
   - `https://readme-typing-svg.herokuapp.com/?lines=...` — animated typing headline (reliable).
   - `https://skillicons.dev/icons?i=python,js,nodejs,...&theme=dark&perline=9` — tech-stack icon grid (reliable; cleaner than shields badges).
   - `https://komarev.com/ghpvc/?username=USER&label=views` — visitor counter (reliable).
   ⚠️ The public `github-readme-stats.vercel.app` (stats + top-langs) and `github-profile-trophy.vercel.app`
   instances are FREQUENTLY PAUSED/PAYWALLED (503 `DEPLOYMENT_PAUSED`, 402 `Payment required`).
   Do NOT embed them unless you 200-verify first. If down, self-host (fork → Vercel) or leave a hidden
   HTML comment with the self-host path. Full status + check loop: references/stat-services.md.
5. Contribution snake — GitHub Action (see references/snake-workflow.md). Publishes SVGs to an `output` branch; embed with `<picture>` + `prefers-color-scheme` for light/dark.
6. Tech badges grid (shields.io `for-the-badge`).
7. Project constellation table (markdown: project | stack | visibility | link) + research/grants table.
8. Footer: visitor counter (komarev.com/ghpvc), quote, links.

## Language rule (Pedro, explicit)
The GitHub profile README is **English-only**. There is no i18n/translation system on a
GitHub README, so do NOT maintain PT/ES/FR blocks here — the multilingual version already
lives on Quartz (`phrandrade.com`, multilíngue) and the portfolio. Past session tried
PT+EN+ES+FR; user said: "deixe o ptbr/es/fr de fora desse readme (já q nao tem como colocar
pra renderizar de acordo com sistema de traducao)". Single-language, clean.

## WakaTime (optional coding-time stats)
- Add `.github/workflows/waka-readme.yml` (template in this skill) + README markers
  `<!--START_SECTION:waka-->` / `<!--END_SECTION:waka-->` around the "Recent activity" block.
- ⚠️ **Action `anmol098/waka-readme` was DELETED (repo 404)** → fails with
  "Unable to resolve action anmol098/waka-readme, repository not found". Use
  **`Athul/waka-readme@master`** instead (same inputs, repo live as of 2026-08).
- `with:` `WAKATIME_API_KEY: ${{ secrets.WAKATIME_API_KEY }}`,
  `GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}`, `SECTION_NAME: waka`, `TIME_RANGE: last_7_days`, `LANG_COUNT: 8`.
- User's key lives in `~/.wakaime.cfg` as a single line `waka_<uuid>` (no `[section]` header).
  Wire it non-interactively: `KEY=$(grep -v '^\[' ~/.wakaime.cfg | head -1 | tr -d '[:space:]') &&
  gh secret set WAKATIME_API_KEY --body "$KEY" --repo <user>/<user>`. `gh secret list` shows
  only names, never the value — safe.
- Needs repo secret `WAKATIME_API_KEY`. Until the secret exists the job fails gracefully.
- **Placeholder badge pitfall**: do NOT embed a guessed/fake WakaTime badge URL (e.g. invented UUID) —
  it 404s. Use a static `img.shields.io/badge/⏱️%20WakaTime-setup%20via%20secret-7B2FBF?...`
  placeholder so the README never breaks. Real stats appear once the secret is set.

## Extra animated assets
- `orbit.svg` — SMIL animated system: pulsing central star + 3 orbiting planets (no JS, renders
  on GitHub). Nice "telemetry" header. Generator pattern: build `<g transform="rotate(...)">`
  wrapping each planet and animate `transform` `from="0 cx cy" to="360 cx cy"`. Dark space bg.
- Starfield (`starfield.svg`) + name GIF (`pedroiff0.gif`, Pillow) already covered in references/scripts.
  User liked the GIFs ("Mantenha os gifs eu gostei, mas pode fazer o svg tbm") — keep both.

## Theme consistency
Pedro's aesthetic = astronomy × computing ("constelação de código"): dark space gradient, twinkling stars, constellation lines, cosmic emoji (☄️ 🌌 🛰️ 🔭 ⭐ 🪐). Mirror across portfolio + Quartz site. Colors: radical purple (#c678dd) / blue (#61afef) on near-black (#0d1117).

## Verify assets resolve (after push)
`curl -s -o /dev/null -w "%{http_code}\n" <raw URL>` for banner SVG + both snake SVGs + every external
stat/badge URL — expect 200. Run this BEFORE embedding too: if a service returns 503/402/404/500,
drop or swap it (see references/stat-services.md). The `scripts/verify-readme-assets.py` checker does
a batch 200-check of the URLs found in a README plus the local workflow SVG.

## Pitfall: stale local clone vs GitHub web edits
Symptom: `git push` rejected (non-fast-forward) — remote has a newer commit (user edited in browser).
- DO NOT blindly `git pull --rebase` and fight conflicts.
- If your rewrite already incorporates the remote's richer content:
  `git fetch origin && git merge -X ours origin/main --no-edit` then `git push`.
  `-X ours` keeps YOUR version on conflict (safe: you folded remote facts into your new README).
- If you haven't read remote content yet, read `git show origin/main:README.md` first and fold its unique facts into your draft before merging.

## Pitfall: verifying workflow YAML
PyYAML `yaml.safe_load` parses `on:` as boolean `True` (YAML 1.1). A check `"on" in data` FAILS silently. Test `(True in data) or ("on" in data)`. Reusable checker: scripts/verify-readme-assets.py.

## Don't fabricate
- No WakaTime/Spotify/Now-playing badges unless user actually uses them.
- No skill/tool the user hasn't confirmed.

## Support files in this skill
- `references/starfield-banner.md` — self-contained Python generator for `assets/starfield.svg`.
- `references/snake-workflow.md` — contribution-snake GitHub Action (publishes to `output` branch).
- `templates/waka-readme.yml` — known-good WakaTime readme workflow (needs `WAKATIME_API_KEY` secret).
- `references/stat-services.md` — live status of third-party stat/badge services + the 200-check loop.
- `scripts/verify-readme-assets.py` — batch 200-check of URLs in a README + local workflow SVG.
- `scripts/gen_name_gif.py` — animated space-theme "name" GIF generator (Pillow) for the footer.
