"""awesomeskills — CLI for the awesome-skills catalog.

Commands:
  awesomeskills install Multi-agent interactive skill installer
  awesomeskills index   Generate README.md from skills/**/SKILL.md
  awesomeskills catalog Generate the installed-skills inventory from ~/.hermes
"""
from __future__ import annotations
import argparse
import sys
from pathlib import Path

from . import gen_index, gen_catalog, installer


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="awesomeskills", description=__doc__)
    sub = p.add_subparsers(dest="cmd", required=True)

    p_inst = sub.add_parser("install", help="Interactive multi-agent skill installer")
    p_inst.add_argument("--quick", action="store_true", help="Quick install elite pack")
    p_inst.add_argument("--uninstall", action="store_true", help="Uninstall / clean installed skills")
    p_inst.add_argument("--agent", help="Target agent(s) comma-separated (agy, hermes, claude, cursor, windsurf, roo, opencode, all)")
    p_inst.add_argument("--scope", choices=["global", "local"], default="global", help="Installation scope")
    p_inst.add_argument("--pack", choices=["fullstack", "devops", "ai", "academic", "creative", "all"], help="Install curated pack")
    p_inst.add_argument("--category", help="Install specific categories comma-separated")
    p_inst.add_argument("--skills", help="Install specific skills comma-separated")
    p_inst.add_argument("--symlink", action="store_true", default=True, help="Use symlinks (default)")
    p_inst.add_argument("--copy", action="store_true", help="Copy files instead of symlinks")
    p_inst.add_argument("--list", action="store_true", help="List all available skills")
    p_inst.add_argument("--repos", action="store_true", help="List curated open source repositories")
    p_inst.add_argument("--ollama", action="store_true", help="List curated Ollama models")

    pi = sub.add_parser("index", help="Generate README.md from skills/**/SKILL.md")
    pi.add_argument("--root", default=".", help="Repo root (default: cwd)")

    pc = sub.add_parser("catalog", help="Generate the installed-skills inventory")
    pc.add_argument("--hermes", default=None, help="Path to ~/.hermes (default: ~/.hermes)")

    args = p.parse_args(argv)

    if args.cmd == "install":
        sys.argv = [sys.argv[0]] + (argv or sys.argv[2:])
        return installer.main()
    if args.cmd == "index":
        return gen_index.main(root=Path(args.root))
    if args.cmd == "catalog":
        return gen_catalog.main(hermes=args.hermes)
    p.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
