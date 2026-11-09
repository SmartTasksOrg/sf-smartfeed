"""SmartFeed CLI.

    sf-smartfeed --demo
    sf-smartfeed ITEMS [--top 5] [--min-score 50] [--json]

ITEMS is a .json, .jsonl or .csv file of items with a `score` and optional
`source`, `velocity`, `title` and `url`.
"""
import argparse
import json
import os
import sys
from dataclasses import asdict

from . import core
from ._version import __version__

BANNER = f"\n🦔 SmartFeed {__version__}  ·  IAIso §9 · Awareness"
FOOTER = "\nBacked by IAIso §9 · Awareness · part of the Smart* family · https://smarttasks.cloud\n"


def _demo_dir():
    return os.path.join(os.path.dirname(__file__), "..", "..", "demo")


def main(argv=None):
    argv = argv if argv is not None else sys.argv[1:]
    if "--version" in argv:
        print(f"SmartFeed {__version__}"); return 0
    if not argv or "--demo" in argv:
        print(BANNER); print(core_demo()); print(FOOTER); return 0

    ap = argparse.ArgumentParser(prog="sf-smartfeed")
    ap.add_argument("items", help=".json, .jsonl or .csv file of items")
    ap.add_argument("--top", type=int, default=5)
    ap.add_argument("--min-score", type=float, default=None)
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)

    b = core.distill(a.top, core.load_items(a.items), min_score=a.min_score)
    if a.json:
        print(json.dumps(asdict(b), indent=2, ensure_ascii=False))
    else:
        print(f"brief: {len(b.items)} items (dropped {b.dedup_ratio:.0%} as duplicates)")
        for s in b.items:
            label = s.title or s.url or f"[{s.source}]"
            print(f"  • {label}  score {s.score:g}  ({s.source})")
    return 0


def core_demo() -> str:
    return _DEMO()


def _DEMO():
    b = core.distill()
    out = [f"distilled brief (dedup {int(b.dedup_ratio*100)}%):"]
    for s in b.items:
        out.append(f"  • [{s.source}] score {s.score} (v{s.velocity})")
    return "\n".join(out)

if __name__ == "__main__":
    sys.exit(main())
