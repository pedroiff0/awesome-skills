# GitHub Pages — gotchas (durable, platform-level)

## Free tier requires a PUBLIC repo
- Private repo → enabling Pages via API returns: `{"message":"Your current plan does not support GitHub Pages for this repository.","status":422}`.
- Fix (after user confirms): `gh api -X PATCH repos/USER/REPO -f private=false`
- A static portfolio contains no secrets, so going public is normally safe. If the user insists on private, Pages needs GitHub Pro.

## Archived repo blocks everything
- An archived repo rejects pushes AND `gh api .../pages` (422). Even read/edit API is limited.
- Unarchive: `gh api -X PATCH repos/USER/REPO -f archived=false`
- Symptom that tipped this off: `gh repo view` showed `isArchived:true` while the repo still appeared in `gh repo list`.

## Renames redirect pushes
- If the repo was renamed (e.g. `portfolio` → `webpage`), pushes to the old URL print:
  `remote: This repository moved. Please use the new location: https://github.com/USER/webpage.git`
  and still succeed. Verify canonical name with `gh repo view USER/REPO --json name,isPrivate`.

## Enabling Pages (legacy / static)
`gh api -X POST repos/USER/REPO/pages -f build_type=legacy -f "source[branch]=master" -f "source[path]="/`
- Response includes `html_url` like `https://USER.github.io/REPO/`.
- First build takes ~1 min. Poll with `curl -o /dev/null -w '%{http_code}' https://USER.github.io/REPO/`.

## Update flow after a rename/enable
Non-fast-forward on push is normal right after enabling Pages or a rename:
`git pull --rebase origin <branch>` then `git push origin <branch>`.
