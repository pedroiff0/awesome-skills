## B. Missing-translation issue watcher (GitHub Action)

A static site (GitHub Pages) CANNOT open an issue on every 404 visit — there is no
backend, and doing so would spam issues. Use a SCHEDULED GitHub Action instead.

`.github/workflows/translation-issues.yml` (cron daily):
```yaml
name: translation-issues
on:
  schedule: [{cron: "17 6 * * *"}]
  workflow_dispatch:
permissions: {issues: write}
jobs:
  scan:
    runs-on: ubuntu-latest
    env: {GH_TOKEN: "${{ secrets.GITHUB_TOKEN }}", REPO: "${{ github.repository }}"}
    steps:
      - uses: actions/checkout@v4
      - run: |
          mapfile -t slugs < <(find content/pt-br -name '*.md' ! -name 'index.md' \
            | sed 's#^content/pt-br/##; s#\.md$##' | sort -u)
          for slug in "${slugs[@]}"; do
            for lang in en es fr; do
              if [ ! -f "content/$lang/$slug.md" ] && [ ! -f "content/$lang/$slug/index.md" ]; then
                title="Tradução em falta: $lang/$slug"
                exists=$(gh issue list --repo "$REPO" --state open --search "$title" --json number --jq 'length' || echo 0)
                if [ "$exists" = "0" ]; then
                  gh issue create --repo "$REPO" --title "$title" \
                    --body "Falta a tradução de \`pt-br/$slug\` em \`$lang/\`." \
                    --label translation || true
                fi
              fi
            done
          done
```
- Create the label once: `gh label create translation --repo <repo> --color 0E8A16`.
- The `404.tsx` (client-side) shows the "translation missing" message + a pre-filled
  "open issue" link + a 5s redirect to the `pt-br` equivalent. The Action is the
  durable backlog; the 404 link is the on-demand request path.
