# GitHub Pages via gh CLI — exact recipe + gotchas (observed 2026-08)

Scenario: publish a STATIC site (index.html at repo root, no build step) to
`https://<user>.github.io/<repo>/` on a free GitHub plan.

## 0. Find / inspect the target repo
```bash
gh repo list <user> --limit 50        # spot portfolio/page/webpage repos
gh repo view OWNER/REPO --json name,isArchived,isPrivate,url
```

## 1. Unarchive if needed (archived repos reject push AND Pages)
```bash
gh api -X PATCH repos/OWNER/REPO -f archived=false
```

## 2. Make it PUBLIC (REQUIRED on free plan — Pages 422s on private)
```bash
gh api -X PATCH repos/OWNER/REPO -f private=false
```
Error you'll get on private:
`422 "Your current plan does not support GitHub Pages for this repository."`

## 3. Push (clone first if reusing an existing repo; strip old scaffold)
```bash
git clone --depth 1 https://github.com/OWNER/REPO.git portfolio
# ... replace files, git add -A, commit, push ...
git push origin master
```
Note: a push may print "This repository moved … new location: …/webpage.git" — the
push still succeeds (`master -> master`). The repo may be internally renamed; trust the tail.

## 4. Enable Pages (REST API — UI toggle may demand Pro)
```bash
gh api -X POST repos/OWNER/REPO/pages \
  -f build_type=legacy \
  -f "source[branch]=master" \
  -f "source[path]=/"
```
Success returns JSON with `"html_url": "https://<user>.github.io/<repo>/"`.
(PUT instead of POST if it already exists: `gh api -X PUT repos/OWNER/REPO/pages -f build_type=legacy -f "source[branch]=master" -f "source[path]=/"`.)

## 5. Wait ~1 min, then verify
```bash
curl -s -o /dev/null -w "%{http_code}\n" -L https://<user>.github.io/<repo>/
# expect 200
curl -s -L https://<user>.github.io/<repo>/ | grep -oE '<title>[^<]+</title>'
```

## Local pre-flight (run before pushing)
```bash
node --check assets/js/*.js
python3 -m http.server 8123 &   # background
curl -o /dev/null -w "%{http_code}\n" http://localhost:8123/assets/css/style.css
```

## Why the REST API and not the Settings UI
The browser "Pages" section's Enable button can gate behind GitHub Pro. The legacy
`/repos/{owner}/{repo}/pages` REST endpoint works on the free plan as long as the
repo is public and not archived.
