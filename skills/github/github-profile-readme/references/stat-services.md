# Third-party GitHub README stat/badge services

GitHub profile READMEs lean heavily on free external services that generate an image
from your username. These public instances go down or get paywalled WITHOUT warning.
**Always 200-check before embedding** — never trust "everyone uses it".

## 200-check loop (run before embedding each URL)
```bash
for u in \
  "https://github-readme-stats.vercel.app/api?username=pedroiff0" \
  "https://github-profile-trophy.vercel.app/?username=pedroiff0" \
  "https://github-readme-activity-graph.vercel.app/graph?username=pedroiff0&theme=radical" \
  "https://github-readme-streak-stats.herokuapp.com/?user=pedroiff0" \
  "https://skillicons.dev/icons?i=python,js,nodejs" \
  "https://readme-typing-svg.herokuapp.com/?lines=hi" \
  "https://komarev.com/ghpvc/?username=pedroiff0" ; do
  code=$(curl -s -o /dev/null -w "%{http_code}" "$u"); echo "$code  $u";
done
```
Anything not `200` → drop it or swap.

## Status snapshot (2026-08-05) — RE-VERIFY each time
### Working (returned 200)
- `readme-typing-svg.herokuapp.com` — animated typing headline. Reliable.
- `skillicons.dev` — clean tech-stack icon grid (`?i=python,js,...&theme=dark&perline=9`). Reliable.
- `github-readme-activity-graph.vercel.app` — contribution-area graph. Reliable.
- `github-readme-streak-stats.herokuapp.com` — contribution streak card. Reliable.
  ⚠️ Transient: if GitHub's API rate-limits, the card renders "Failed to retrieve contributions"
  for one render — that is GitHub's API glitch, NOT a README bug. Re-check later; usually 200.
- `ghchart.rshah.org` — colored contribution "bar-code" chart (`https://ghchart.rshah.org/COLOR/USER`).
  Reliable (added 2026-08). Good extra telemetry block.
- `komarev.com/ghpvc` — visitor counter badge. Reliable.
- `raw.githubusercontent.com/<user>/<user>/...` — your own self-hosted SVG/GIF assets. Most reliable.

### Down / paywalled (do NOT use the public instance)
- `github-readme-stats.vercel.app` — `503 DEPLOYMENT_PAUSED` (stats + top-langs).
- `github-profile-trophy.vercel.app` — `402 Payment required` / `DEPLOYMENT_DISABLED`.
- `gh-readme-tech-stack.vercel.app` — `404` for most users.
- `api.star-history.com` — `500` flaky. Avoid.
- `anmol098/waka-readme` (GitHub Action) — **repo DELETED (404)**. Action fails with
  "Unable to resolve action anmol098/waka-readme, repository not found". Use
  **`Athul/waka-readme@master`** instead (same inputs; repo live). User's WakaTime key is
  in `~/.wakaime.cfg` as a single line `waka_<uuid>` (no `[section]`) — wire it headless via
  `KEY=$(grep -v '^\[' ~/.wakaime.cfg | head -1 | tr -d '[:space:]') &&
  gh secret set WAKATIME_API_KEY --body "$KEY" --repo <user>/<user>` (`gh secret list` shows
  only names, never the value). Once set, the job shows "No activity tracked" until the IDE
  WakaTime extension records coding time — expected, not an error.

## Self-host fallback (definitive fix for the down stats cards)
1. Fork `github.com/anuraghazra/github-readme-stats`.
2. Deploy to your own Vercel (one click) — you do the login in the browser.
3. Swap the URL to `https://YOUR-DEPLOY.vercel.app/api?username=<user>&theme=radical`.
Leave a hidden HTML comment in the README documenting this so future-you knows why the
card is absent and how to re-enable it.
