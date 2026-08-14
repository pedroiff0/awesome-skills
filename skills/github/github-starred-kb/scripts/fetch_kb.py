#!/usr/bin/env python3
"""github-starred-kb helper.

Maps pedroiff0's starred repos into knowledge domains and fetches the relevant
repo content on demand (raw README via GitHub, or via gh api).

Usage:
  python3 fetch_kb.py --match "api clima"          # list matching repos
  python3 fetch_kb.py --repo public-apis/public-apis --readme
  python3 fetch_kb.py --repo pedroiff0/financas-app --path app/src/services
  python3 fetch_kb.py --rebuild                    # rewrite references/starred-index.md
"""
from __future__ import annotations
import argparse, json, subprocess, sys, urllib.request, urllib.error
from pathlib import Path

HERE = Path(__file__).resolve().parent
INDEX = HERE / "references" / "starred-index.md"

# Heuristic domain classifier (mirrors SKILL.md).
def domains(r: dict) -> list[str]:
    fn = r["full_name"].lower()
    d = (r.get("description") or "").lower()
    tags = set()
    if "public-apis" in fn or ("free api" in d) or ("collective list of" in d and "api" in d):
        tags.add("Free APIs")
    if "awesome-sysadmin" in fn: tags.add("Sysadmin")
    if "awesome-selfhosted" in fn: tags.add("Self-hosted")
    if "awesome-python" in fn: tags.add("Python")
    if "algorithms" in fn: tags.add("Algorithms/CS")
    if any(k in fn for k in ["langflow","llm-apps","ai-apps","mcp-servers","hermes-skills","ai-creator","claude-night-market","hermes-workspace"]):
        tags.add("AI/Agents/RAG/MCP")
    if any(k in fn for k in ["manim","easyspec","calculo","formularios","sistema-academico","academico","guia-github"]):
        tags.add("Math/Edu/Video")
    if any(k in fn for k in ["spectra","anomaly","nasa","quartz"]) or "astronomy" in d:
        tags.add("Astronomy/Science")
    if any(k in fn for k in ["financas","projeto-profissional","portfolio","node-js","hermes-workspace","sistema-academico"]):
        tags.add("Web/Node/EJS")
    if any(k in fn for k in ["hermes-skills","hermes-workspace","claude-night-market"]):
        tags.add("Hermes ecosystem")
    if fn.startswith("pedroiff0/pedroiff0") or fn.endswith("/cv") or "guia-github" in fn:
        tags.add("Profile/Docs")
    if "parliament" in fn: tags.add("News/Misc")
    if fn.split("/")[1] == "awesome": tags.add("Meta awesome")
    if r.get("language") == "Python" and not tags:
        tags.add("Python")
    if not tags: tags.add("Other")
    return sorted(tags)


def get_starred() -> list[dict]:
    out = subprocess.run(["gh", "api", "users/pedroiff0/starred", "--paginate"],
                         capture_output=True, text=True)
    if out.returncode != 0:
        sys.exit("gh api failed: " + out.stderr.strip())
    return json.loads(out.stdout)


def raw_url(repo: str, branch: str, path: str = "README.md") -> str:
    return f"https://raw.githubusercontent.com/{repo}/{branch}/{path}"


def fetch_raw(repo: str, path: str = "README.md") -> str | None:
    for branch in ("master", "main"):
        url = raw_url(repo, branch, path)
        try:
            with urllib.request.urlopen(url, timeout=20) as r:
                return r.read().decode("utf-8", "replace")
        except urllib.error.HTTPError as e:
            if e.code != 404:
                return f"[HTTP {e.code}] {url}"
        except Exception as e:
            return f"[ERR] {e}"
    return None


def match_repos(repos: list[dict], query: str) -> list[dict]:
    q = query.lower()
    scored = []
    for r in repos:
        blob = (r["full_name"] + " " + (r.get("description") or "")).lower()
        dom = " ".join(domains(r)).lower()
        if q in blob or q in dom:
            scored.append(r)
    return scored


def rebuild(repos: list[dict]) -> None:
    lines = ["# Starred Knowledge Base — Index (pedroiff0)", "",
             f"Total starred: **{len(repos)}**. Generated from `gh api users/pedroiff0/starred`.",
             "Categories are heuristic; a repo may serve multiple domains.", "",
             "| # | Repo | Stars | Lang | Domain(s) | Desc |",
             "|---|---|---|---|---|---|"]
    for i, r in enumerate(sorted(repos, key=lambda x: -x["stargazers_count"]), 1):
        fn = r["full_name"]; stars = r["stargazers_count"]
        lang = r.get("language") or "-"; dom = ", ".join(domains(r))
        desc = (r.get("description") or "").replace("|", "/").replace("\n", " ")
        lines.append(f"| {i} | `{fn}` | {stars} | {lang} | {dom} | {desc} |")
    lines += ["", "## Raw README fetch pattern", "", "```bash",
              "curl -sL https://raw.githubusercontent.com/<owner>/<repo>/master/README.md",
              "curl -sL https://raw.githubusercontent.com/<owner>/<repo>/main/README.md",
              "```"]
    INDEX.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"rebuilt {INDEX} with {len(repos)} repos")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--match")
    ap.add_argument("--repo")
    ap.add_argument("--path", default="README.md")
    ap.add_argument("--readme", action="store_true")
    ap.add_argument("--rebuild", action="store_true")
    args = ap.parse_args()

    repos = get_starred()

    if args.rebuild:
        rebuild(repos); return 0

    if args.match:
        hits = match_repos(repos, args.match)
        if not hits:
            print("no match"); return 0
        for r in sorted(hits, key=lambda x: -x["stargazers_count"]):
            print(f"{r['full_name']}  [{', '.join(domains(r))}]  ★{r['stargazers_count']}")
        return 0

    if args.repo:
        content = fetch_raw(args.repo, args.path if not args.readme else "README.md")
        if content is None:
            print(f"[404] no README on master/main for {args.repo}")
            return 1
        print(content)
        return 0

    ap.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
