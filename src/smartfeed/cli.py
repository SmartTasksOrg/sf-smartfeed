"""SmartFeed CLI — run `smartfeed --demo`."""
import os, sys, json
from . import core
from ._version import __version__


def _demo_dir():
    return os.path.join(os.path.dirname(__file__), "..", "..", "demo")


def main(argv=None):
    argv = argv if argv is not None else sys.argv[1:]
    if "--version" in argv:
        print(f"SmartFeed {__version__}"); return 0
    demo = "--demo" in argv or not argv
    print(f"\n🦔 SmartFeed {__version__}  ·  IAIso §9 · Awareness")
    result = core_demo()
    print(result)
    print(f"\nBacked by IAIso §9 · Awareness · part of the Smart* family · https://smarttasks.cloud\n")
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
