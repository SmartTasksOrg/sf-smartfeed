"""SmartFeed core — distill the firehose into a brief."""
import json, os
from .models import Signal, Brief

def _stream():
    return [Signal("hn", 88, 9.1), Signal("hn", 86, 8.8), Signal("reddit", 62, 4.2),
            Signal("gtrends", 70, 6.0), Signal("reddit", 61, 4.0), Signal("arxiv", 55, 3.1),
            Signal("gtrends", 71, 6.2), Signal("news", 66, 5.0)]

def distill(top: int = 5) -> Brief:
    sigs = _stream()
    seen, deduped = set(), []
    for s in sorted(sigs, key=lambda x: -x.score):
        key = (s.source, round(s.score / 5))
        if key in seen:
            continue
        seen.add(key); deduped.append(s)
    dedup_ratio = round(1 - len(deduped) / len(sigs), 2)
    return Brief(deduped[:top], dedup_ratio)
