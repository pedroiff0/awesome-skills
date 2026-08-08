# Contribution snake workflow

`.github/workflows/snake.yml` — generates the classic "contribution snake" SVG
and publishes to an `output` branch every day at midnight UTC (plus manual run).

```yaml
name: Generate Contribution Snake
on:
  schedule:
    - cron: "0 0 * * *"
  workflow_dispatch:
permissions:
  contents: write
jobs:
  generate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: Platane/snk@v3
        with:
          github_user_name: ${{ github.repository_owner }}
          outputs: |
            dist/github-contribution-grid-snake.svg
            dist/github-contribution-grid-snake-dark.svg?palette=github-dark
      - uses: crazy-max/ghaction-github-pages@v4
        with:
          target_branch: output
          build_dir: dist
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

After push, trigger first run manually: `gh workflow run snake.yml`.
Watch: `gh run watch <id>` — expect `✓ generate` in ~20s.
Embed in README (light/dark aware):

```html
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/USER/USER/output/github-contribution-grid-snake-dark.svg" />
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/USER/USER/output/github-contribution-grid-snake.svg" />
  <img alt="contribution snake" src="https://raw.githubusercontent.com/USER/USER/output/github-contribution-grid-snake.svg" />
</picture>
```

Verify both SVGs return 200 from the `output` branch before declaring done.
