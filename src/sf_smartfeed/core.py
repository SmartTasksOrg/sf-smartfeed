"""SmartFeed core — distill the firehose into a brief.

Give `distill()` your own items (from `load_items()` or built in code); with
none, it uses the 8 sample signals shown by `--demo`. Items are ranked by
score, then velocity, and near-duplicates are dropped, keeping the
higher-scored copy:

* the same URL (ignoring scheme, "www.", trailing "/" and query string) is a duplicate;
* titles whose word sets overlap by at least `title_similarity` (Jaccard) are duplicates;
* items with neither a title nor a URL fall back to the sample rule: same
  source and a score in the same band of 5.
"""
from __future__ import annotations

import csv
import json
import re
from typing import Iterable
from urllib.parse import urlsplit

from .models import Brief, Signal

_WORD = re.compile(r"[a-z0-9一-鿿]+")


def _stream() -> list[Signal]:
    """The 8 sample signals used by the demo."""
    return [Signal("hn", 88, 9.1), Signal("hn", 86, 8.8), Signal("reddit", 62, 4.2),
            Signal("gtrends", 70, 6.0), Signal("reddit", 61, 4.0), Signal("arxiv", 55, 3.1),
            Signal("gtrends", 71, 6.2), Signal("news", 66, 5.0)]


def _norm_url(url: str) -> str:
    parts = urlsplit(url.strip().lower())
    host = parts.netloc[4:] if parts.netloc.startswith("www.") else parts.netloc
    return host + parts.path.rstrip("/")


def _words(title: str) -> frozenset[str]:
    return frozenset(_WORD.findall(title.lower()))


def _similar(a: frozenset[str], b: frozenset[str], threshold: float) -> bool:
    if not a or not b:
        return False
    return len(a & b) / len(a | b) >= threshold


def distill(top: int = 5, items: Iterable[Signal] | None = None, *,
            min_score: float | None = None, title_similarity: float = 0.8) -> Brief:
    """Rank, dedupe and cap `items`. `dedup_ratio` is the share of items dropped as duplicates."""
    sigs = list(_stream() if items is None else items)
    if min_score is not None:
        sigs = [s for s in sigs if s.score >= min_score]
    kept: list[Signal] = []
    seen_urls: set[str] = set()
    seen_titles: list[frozenset[str]] = []
    seen_keys: set[tuple] = set()
    for s in sorted(sigs, key=lambda x: (-x.score, -x.velocity)):
        url = _norm_url(s.url) if s.url else ""
        words = _words(s.title) if s.title else frozenset()
        if url and url in seen_urls:
            continue
        if words and any(_similar(words, w, title_similarity) for w in seen_titles):
            continue
        if not url and not words:
            key = (s.source, round(s.score / 5))
            if key in seen_keys:
                continue
            seen_keys.add(key)
        if url:
            seen_urls.add(url)
        if words:
            seen_titles.append(words)
        kept.append(s)
    dedup_ratio = round(1 - len(kept) / len(sigs), 2) if sigs else 0.0
    return Brief(kept[:max(0, top)], dedup_ratio)


def _signal(d: dict, where: str) -> Signal:
    try:
        score = float(d["score"])
    except (KeyError, TypeError, ValueError):
        raise ValueError(f"{where}: needs a numeric 'score'") from None
    try:
        velocity = float(d.get("velocity") or 0)
    except (TypeError, ValueError):
        raise ValueError(f"{where}: 'velocity' must be a number") from None
    return Signal(str(d.get("source") or "unknown"), score, velocity,
                  str(d.get("title") or ""), str(d.get("url") or ""))


def load_items(path: str) -> list[Signal]:
    """Read items from .json (a list, or {"items": [...]}), .jsonl or .csv.

    Each item needs `score`; `source`, `velocity`, `title` and `url` are optional.
    """
    with open(path, encoding="utf-8", newline="") as fh:
        if path.endswith(".csv"):
            rows = list(csv.DictReader(fh))
        elif path.endswith(".jsonl"):
            rows = [json.loads(line) for line in fh if line.strip()]
        else:
            data = json.load(fh)
            rows = data.get("items", []) if isinstance(data, dict) else data
    if not isinstance(rows, list):
        raise ValueError("expected a list of items")
    return [_signal(r, f"item {i + 1}") for i, r in enumerate(rows)]
