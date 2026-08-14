"""awesomeskills — CLI for the awesome-skills catalog.

Commands:
  awesomeskills index   Generate README.md from skills/**/SKILL.md
  awesomeskills catalog Generate the installed-skills inventory from ~/.hermes
"""
from __future__ import annotations
import argparse
import sys

from . import gen_index, gen_catalog


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="awesomeskills", description=__doc__)
    sub = p.add_subparsers(dest="cmd", required=True)

    pi = sub.add_parser("index", help="Generate README.md from skills/**/SKILL.md")
    pi.add_argument("--root", default=".", help="Repo root (default: cwd)")

    pc = sub.add_parser("catalog", help="Generate the installed-skills inventory")
    pc.add_argument("--hermes", default=None, help="Path to ~/.hermes (default: ~/.hermes)")

    args = p.parse_args(argv)

    if args.cmd == "index":
        return gen_index.main(root=args.root)
    if args.cmd == "catalog":
        return gen_catalog.main(hermes=args.hermes)
    p.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
