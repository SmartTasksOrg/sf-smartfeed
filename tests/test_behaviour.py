"""Behaviour of core.distill: the sample stream and your own items."""
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


import json

import pytest

from sf_smartfeed.models import Signal


def test_your_own_items_are_used():
    """Version 3.0 had no input: it always distilled the 8 sample signals."""
    items = [Signal("rss", 40, title="Model A released"), Signal("rss", 90, title="Chip export rules change")]
    b = core.distill(items=items)
    assert [s.title for s in b.items] == ["Chip export rules change", "Model A released"]


def test_same_url_is_a_duplicate_whatever_the_formatting():
    items = [Signal("hn", 80, url="https://www.example.com/post/1/"),
             Signal("reddit", 70, url="http://example.com/post/1?utm=x")]
    b = core.distill(items=items)
    assert len(b.items) == 1 and b.items[0].score == 80 and b.dedup_ratio == 0.5


def test_near_identical_titles_are_duplicates():
    items = [Signal("a", 80, title="OpenAI releases new model today"),
             Signal("b", 75, title="OpenAI releases new model"),
             Signal("c", 60, title="Regulators open AI inquiry")]
    assert [s.source for s in core.distill(items=items).items] == ["a", "c"]
    assert len(core.distill(items=items, title_similarity=0.95).items) == 3


def test_min_score_and_velocity_tiebreak():
    items = [Signal("a", 50, 1.0), Signal("b", 50, 9.0, title="x"), Signal("c", 10, title="low")]
    b = core.distill(items=items, min_score=20)
    assert [s.source for s in b.items] == ["b", "a"]


def test_items_load_from_json_jsonl_and_csv(tmp_path):
    rows = [{"source": "hn", "score": 80, "title": "One"}, {"score": "70", "url": "https://x.io/2"}]
    (tmp_path / "a.json").write_text(json.dumps({"items": rows}))
    (tmp_path / "a.jsonl").write_text("\n".join(json.dumps(r) for r in rows))
    (tmp_path / "a.csv").write_text("source,score,velocity,title,url\nhn,80,,One,\n,70,,,https://x.io/2\n")
    for name in ("a.json", "a.jsonl", "a.csv"):
        got = core.load_items(str(tmp_path / name))
        assert [(s.source, s.score, s.title, s.url) for s in got] == [
            ("hn", 80.0, "One", ""), ("unknown", 70.0, "", "https://x.io/2")]
    (tmp_path / "bad.json").write_text(json.dumps([{"title": "no score"}]))
    with pytest.raises(ValueError, match="numeric 'score'"):
        core.load_items(str(tmp_path / "bad.json"))


def test_empty_input_gives_an_empty_brief():
    assert core.distill(items=[]) .items == [] and core.distill(items=[]).dedup_ratio == 0.0


def test_cli_distills_a_file(tmp_path, capsys):
    from sf_smartfeed import cli
    f = tmp_path / "items.jsonl"
    f.write_text('{"score": 80, "title": "Big news"}\n{"score": 79, "title": "Big news!"}\n')
    assert cli.main([str(f), "--json"]) == 0
    out = json.loads(capsys.readouterr().out)
    assert len(out["items"]) == 1 and out["dedup_ratio"] == 0.5
