"""Tests for caption re-segmentation."""

from __future__ import annotations

from whisper_transcribe_de.captions import to_cues


def _words(*triples):
    return [{"word": w, "start": s, "end": e} for (w, s, e) in triples]


def test_passthrough_without_word_timings():
    segs = [{"start": 0.0, "end": 30.0, "text": "Ein langer Block."}]
    cues = to_cues(segs)
    assert len(cues) == 1
    assert cues[0]["text"] == "Ein langer Block."


def test_splits_on_max_seconds():
    seg = {
        "start": 0.0,
        "end": 12.0,
        "words": _words(("Eins", 0.0, 1.0), ("zwei", 5.0, 6.0), ("drei", 10.0, 11.0)),
    }
    cues = to_cues([seg], max_seconds=4.0, max_chars=999)
    # 0–6s exceeds 4s once "zwei" lands → split before it; etc.
    assert len(cues) >= 2
    assert cues[0]["start"] == 0.0
    assert all(c["end"] - c["start"] <= 6.0 for c in cues)


def test_splits_on_max_chars():
    seg = {
        "start": 0.0,
        "end": 3.0,
        "words": _words(("Donaudampfschiff", 0.0, 1.0), ("fahrtskapitän", 1.0, 2.0)),
    }
    cues = to_cues([seg], max_seconds=999, max_chars=20)
    assert len(cues) == 2
    assert cues[0]["text"] == "Donaudampfschiff"


def test_word_timings_drive_cue_bounds():
    seg = {"start": 0.0, "end": 9.0, "words": _words(("Hallo", 1.0, 1.5), ("Welt", 8.0, 8.5))}
    cues = to_cues([seg], max_seconds=3.0, max_chars=999)
    assert cues[0]["start"] == 1.0
    assert cues[-1]["end"] == 8.5
