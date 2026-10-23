"""Behaviour of core.distill on the built-in sample stream (the package has no input of its own yet)."""
from sf_smartfeed import core


def test_brief_is_sorted_by_score_and_capped_at_top():
    b = core.distill()
    scores = [s.score for s in b.items]
    assert len(b.items) == 5 and scores == sorted(scores, reverse=True)
    assert scores == [88, 86, 71, 66, 62]


def test_near_duplicates_from_one_source_are_dropped():
    # (source, score/5 rounded) is the duplicate key: reddit 62/61 and gtrends 71/70 collapse
    b = core.distill(top=100)
    keys = [(s.source, round(s.score / 5)) for s in b.items]
    assert len(keys) == len(set(keys)) == 6
    assert b.dedup_ratio == 0.25          # 2 of the 8 sample signals were duplicates


def test_the_higher_scored_duplicate_is_kept():
    b = core.distill(top=100)
    reddit = [s.score for s in b.items if s.source == "reddit"]
    assert reddit == [62]


def test_top_zero_gives_an_empty_brief_with_the_same_ratio():
    b = core.distill(top=0)
    assert b.items == [] and b.dedup_ratio == 0.25
