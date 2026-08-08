---
name: obscure-tool-install-lookup
description: "Use when a user asks how to install or use an obscure CLI tool, agent, or package and search engines are blocked, CAPTCHA-walled, or unhelpful. Resolves canonical install commands via GitHub repo search, raw README fetches, and official docs — without relying on web_search or bot-walled search engines."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [install, package-lookup, no-web-search, github, docs, tooling]
    related_skills: [github-repo-management, plan]
---

# Obscure Tool / Agent Install Lookup

## Overview

Users often ask "how do I install X?" for tools that are too new, too niche, or
too vaguely named for a normal web search to surface authoritative
instructions. This is especially common for AI "agent" projects that have a
fan-facing name (e.g. "picoding agent") which does not match the canonical
package name on npm/GitHub.

The trap: `web_search` is unavailable in many Hermes deployments, and the
browser route through Google/DuckDuckGo frequently hits CAPTCHA or
"verification" walls. The npm registry website is behind Cloudflare and also
blocks automated browsers. You must reach the same facts through endpoints that
are NOT bot-walled.

This skill documents the reliable fallback chain that resolves install
instructions end-to-end without a working search engine.

## When to Use

- User asks to install/use a tool, CLI, or agent whose exact package name is
  unknown or ambiguous.
- A web search engine (Google/DuckDuckGo/Bing) returns a CAPTCHA or
  verification page instead of results.
- npmjs.com / registries block the browser with "Just a moment..." (Cloudflare).
- You need the *canonical* install command, not a blog post reproducing it.

**Don't use for:** widely-known packages (just run `npm i`/read the well-known
docs), or tasks that need live web data rather than install steps.

## The Primary Recipe (ordered)

Work the chain top to bottom. Stop as soon as you have a verified install
command from an authoritative source.

1. **Name disambiguation via GitHub repo search (not web search).**
   - `browser_navigate` to `https://github.com/search?q=<name>&type=repositories`
   - Scan the result list for a repo whose name/description matches the tool.
     Fan names rarely equal package names — look for the *description* and the
     actual code (is it npm/Nix/PyPI?).
   - *Completion:* you have 1–3 candidate repos with owner/name.

2. **Open the most promising repo and read its README.**
   - `browser_navigate` to `https://github.com/<owner>/<repo>`.
   - If the README is truncated in the snapshot, fetch the raw file directly:
     `https://raw.githubusercontent.com/<owner>/<repo>/<branch>/README.md`
     (branch is usually `main` or `master`; the repo page shows it).
   - *Completion:* you understand what the package actually is and where it
     installs from (npm scope, PyPI, cargo, etc.).

3. **Decode "wrapper" / repackaging repos.**
   - Some repos are NOT the upstream project — they just repackage it (common
     patterns: a Nix flake, a Homebrew formula, a Dockerfile). The REAL install
     command lives in the upstream it points to.
   - Tell-tale signs: tiny repo, 100% Nix/Shell/Dockerfile, a `fetchFromGitHub`
     / `src` block with a different `owner`/`repo`. Open that file
     (e.g. `pi-coding-agent.nix`) and read the `src` declaration — it names the
     true upstream repo and often the npm package + `homepage`.
   - *Completion:* you have the upstream repo URL and/or npm package name.

4. **Fetch the upstream package's raw README for the install command.**
   - Go to `raw.githubusercontent.com/<upstream-owner>/<upstream-repo>/<branch>/README.md`
     or the package-specific README (monorepos put it under
     `packages/<name>/README.md`).
   - These raw endpoints return clean text — no JS, no bot wall.
   - *Completion:* you have the literal install command(s).

5. **Confirm against the official docs site (preferred over README).**
   - Most mature projects have a docs site (e.g. `pi.dev/docs/latest`).
     `browser_navigate` there and read the Quickstart/Install page. Docs are
     usually lighter and less bot-walled than npm.
   - *Completion:* install command corroborated by the canonical docs site.

6. **Avoid the npm *website*; use the registry JSON or docs instead.**
   - `https://registry.npmjs.org/@scope/name/latest` returns JSON (may render
     as a near-empty form in the browser snapshot — that's fine, the data is
     there). Prefer the docs site for the human-readable command.
   - *Completion:* you did not waste a turn on the Cloudflare-walled npm page.

7. **Report.** Give the user: the canonical install command, the `--ignore-scripts`
   / supply-chain caveat if the project recommends it, the run command, and the
   auth/env step. Offer to run it.

## Tiered Fallback When Search Itself Is Blocked

If even GitHub search is slow, the order of reliability is:

1. GitHub repo search (rarely bot-walled) — best for name disambiguation.
2. `raw.githubusercontent.com` READMEs — clean, never bot-walled.
3. Official docs site `/docs` path — usually light, often readable.
4. npm registry JSON (`registry.npmjs.org/.../latest`) — data-only fallback.
5. Last resort: `curl` the docs/README from the terminal (use `terminal`, not
   the browser) — `curl -fsSL https://raw.githubusercontent.com/.../README.md`.

Never rely on Google/DuckDuckGo HTML in this environment; they return CAPTCHA
or verification iframes within 1–2 attempts.

## Common Pitfalls

1. **Trusting the fan name.** "picoding agent" → actual package
   `@earendil-works/pi-coding-agent`, run as `pi`. Always resolve to the real
   package name before giving a command.
2. **Stopping at a wrapper repo.** A Nix flake repo with 0 stars is almost
   never the upstream. Read its packaging file to find the true source.
3. **Hitting npmjs.com in the browser.** It shows "Just a moment..." (Cloudflare).
   Use the registry JSON or the project's own docs site instead.
4. **Giving a blog/medium command as canonical.** Only report commands sourced
   from the upstream README or official docs.
5. **Forgetting the supply-chain caveat.** Many modern CLIs recommend
   `npm install -g --ignore-scripts` to skip dependency lifecycle scripts.
   State it when the docs do.

## Verification Checklist

- [ ] Resolved the *real* package/repo name (not just the user's phrasing).
- [ ] Install command comes from upstream README or official docs, not a third party.
- [ ] If a wrapper repo was found, the upstream it points to was identified.
- [ ] Supply-chain flags (`--ignore-scripts`, etc.) included when the docs recommend them.
- [ ] Run command + auth/env setup step included in the answer.
- [ ] Offered to actually execute the install.

## Worked Example

See `references/worked-example-picoding-agent.md` for the full trace that
produced this skill (resolving "picoding agent" → Pi Coding Agent →
`@earendil-works/pi-coding-agent`), including the exact URLs and the Nix-flake
decode that revealed the upstream.
