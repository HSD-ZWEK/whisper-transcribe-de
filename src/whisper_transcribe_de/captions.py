# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) Hochschule Düsseldorf – University of Applied Sciences
# ZWEK – Centre for Training and Competence Development
# Developed within the KIVi-Azubi research project
"""Re-segment transcript segments into short, readable caption cues.

For subtitles (VTT/SRT placed in Moodle or imported into Panopto), long segments are
hard to read. When word-level timings are available (WhisperX alignment), segments are
split into cues bounded by a maximum duration and character length. Without word timings
the original segments are passed through unchanged.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any

Segment = Mapping[str, Any]


def _word_bounds(
    word: Mapping[str, Any], fallback_start: float, fallback_end: float
) -> tuple[float, float]:
    start = word.get("start")
    end = word.get("end")
    start = float(start) if start is not None else fallback_start
    end = float(end) if end is not None else max(start, fallback_end)
    return start, end


def to_cues(
    segments: Sequence[Segment],
    max_seconds: float = 6.0,
    max_chars: int = 84,
) -> list[dict[str, Any]]:
    """Split ``segments`` into caption cues bounded by duration and character length."""
    cues: list[dict[str, Any]] = []
    for seg in segments:
        seg_start = float(seg.get("start", 0.0))
        seg_end = float(seg.get("end", seg_start))
        words = seg.get("words") or []
        if not words:
            text = str(seg.get("text", "")).strip()
            if text:
                cues.append({"start": seg_start, "end": seg_end, "text": text})
            continue

        cur_words: list[str] = []
        cur_start: float | None = None
        cur_end = seg_start
        for word in words:
            wtext = str(word.get("word", "")).strip()
            if not wtext:
                continue
            wstart, wend = _word_bounds(word, cur_end, cur_end)
            if cur_start is None:
                cur_start = wstart
            candidate = (" ".join(cur_words + [wtext])).strip()
            too_long = len(candidate) > max_chars or (wend - cur_start) > max_seconds
            if cur_words and too_long:
                cues.append({"start": cur_start, "end": cur_end, "text": " ".join(cur_words)})
                cur_words = [wtext]
                cur_start = wstart
                cur_end = wend
            else:
                cur_words.append(wtext)
                cur_end = wend
        if cur_words and cur_start is not None:
            cues.append({"start": cur_start, "end": cur_end, "text": " ".join(cur_words)})
    return cues
