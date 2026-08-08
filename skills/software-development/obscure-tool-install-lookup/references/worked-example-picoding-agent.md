# Worked Example: "how do I install picoding agent?"

Trace that motivated the `obscure-tool-install-lookup` skill. Real facts, verified.

## User phrasing vs. reality
- User said: "picoding agent"
- Actual project: **Pi Coding Agent** by Earendil Inc.
- Upstream repo: `github.com/earendil-works/pi` (72k stars, very active)
- Published npm package: `@earendil-works/pi-coding-agent`
- CLI binary name: `pi`
- Official site / docs: `https://pi.dev/` and `https://pi.dev/docs/latest`

## Why search failed
- `web_search` tool: not available in this deployment.
- Google: returned a CAPTCHA / "sorry/index" page on first query.
- DuckDuckGo HTML: returned a verification iframe, no results.
- npmjs.com (browser): returned "Just a moment..." (Cloudflare block).

## Successful chain
1. GitHub repo search: `https://github.com/search?q=picoding+agent&type=repositories`
   → 1 result: `YUBIZ/PiCodingAgent` (a Nix flake, 0 stars).
2. Opened `github.com/YUBIZ/PiCodingAgent`. Files: `flake.nix`, `flake.lock`,
   `pi-coding-agent.nix`, `README.md`. README admits "This Flake was written by AI."
   → clearly a *wrapper*, not upstream.
3. Read `https://raw.githubusercontent.com/YUBIZ/PiCodingAgent/main/pi-coding-agent.nix`.
   The `src` block revealed the truth:
   ```
   src = fetchFromGitHub {
     owner = "earendil-works";
     repo  = "pi";
     rev   = "v0.75.3";
     ...
   };
   meta = {
     homepage = "https://pi.dev/";
     mainProgram = "pi";
   };
   ```
   → upstream is `earendil-works/pi`, CLI is `pi`, homepage `pi.dev`.
4. Opened `github.com/earendil-works/pi` → README pointed to
   `packages/coding-agent` and docs at `pi.dev/docs/latest`.
5. Fetched official docs: `https://pi.dev/docs/latest` → "Quick start" section
   gave the canonical commands.

## Canonical install commands (from official docs)
```bash
# Preferred: script installer (Linux/macOS)
curl -fsSL https://pi.dev/install.sh | sh

# Or npm global (--ignore-scripts skips dependency lifecycle scripts;
# Pi does not need them for a normal install)
npm install -g --ignore-scripts @earendil-works/pi-coding-agent

# Uninstall
npm uninstall -g @earendil-works/pi-coding-agent

# Run inside a project dir
pi
```
Auth: `pi login` for subscription providers, or set an API key
(e.g. `ANTHROPIC_API_KEY`, `OPENAI_API_KEY`) before launching.

## Lessons reinforced
- Wrapper repos (Nix/Homebrew/Docker) name the real upstream inside their
  packaging file — read it instead of assuming the repo IS the project.
- `raw.githubusercontent.com` READMEs are the cleanest, never bot-walled source.
- Docs sites (`/docs`) are lighter and more readable than npm's Cloudflare wall.
