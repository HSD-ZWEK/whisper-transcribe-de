"""Tests for the pure output formatters."""

from __future__ import annotations

import json

import pytest

from whisper_transcribe_de.formats import render, to_json, to_srt, to_txt, to_vtt

SEGMENTS = [
    {"start": 0.0, "end": 2.5, "text": " Hallo Welt "},
    {"start": 2.5, "end": 3661.0, "text": "Zustandsgleichung"},
]


def test_to_txt_strips_and_joins():
    assert to_txt(SEGMENTS) == "Hallo Welt\nZustandsgleichung\n"


def test_to_vtt_header_and_timestamps():
    out = to_vtt(SEGMENTS)
    assert out.startswith("WEBVTT")
    assert "00:00:00.000 --> 00:00:02.500" in out
    # 3661 s = 01:01:01.000
    assert "01:01:01.000" in out


def test_to_srt_indices_and_comma_millis():
    out = to_srt(SEGMENTS)
    assert out.startswith("1\n")
    assert "00:00:00,000 --> 00:00:02,500" in out
    assert "\n2\n" in out


def test_to_json_with_and_without_metadata():
    payload = json.loads(to_json(SEGMENTS, {"model": "large-v3"}))
    assert payload["metadata"]["model"] == "large-v3"
    assert len(payload["segments"]) == 2
    assert "metadata" not in json.loads(to_json(SEGMENTS))


def test_render_dispatch_and_unknown():
    assert render("txt", SEGMENTS).startswith("Hallo")
    with pytest.raises(ValueError):
        render("docx", SEGMENTS)
