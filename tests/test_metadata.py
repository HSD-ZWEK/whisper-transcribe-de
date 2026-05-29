"""Tests for reproducibility metadata."""

from __future__ import annotations

from whisper_transcribe_de.metadata import build_metadata


def test_metadata_core_fields():
    meta = build_metadata(
        source="lecture.mp4",
        engine="whisperx+align",
        model="large-v3",
        language="de",
        parameters={"beam_size": 5, "temperature": 0.0},
    )
    assert meta["tool"] == "whisper-transcribe-de"
    assert meta["engine"] == "whisperx+align"
    assert meta["model"] == "large-v3"
    assert meta["parameters"]["beam_size"] == 5
    assert "asr_note" in meta  # human-review reminder
    assert "tool_version" in meta


def test_metadata_optional_fields():
    meta = build_metadata(
        source="s.mp4",
        engine="whisperx",
        model="large-v3",
        language="de",
        parameters={},
        created="2026-05-29T08:00:00+00:00",
        source_id="abc-123",
        vocabulary=["isotherm", "isobar"],
    )
    assert meta["created"] == "2026-05-29T08:00:00+00:00"
    assert meta["source_id"] == "abc-123"
    assert meta["vocabulary_terms"] == 2
