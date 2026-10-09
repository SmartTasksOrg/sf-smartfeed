"""UML data objects for SmartFeed — the diagram in the README is these classes."""
from __future__ import annotations
from dataclasses import dataclass, field

@dataclass
class Signal:
    source: str
    score: float
    velocity: float

@dataclass
class Brief:
    items: list[Signal]
    dedup_ratio: float
