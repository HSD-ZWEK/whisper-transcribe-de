# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) Hochschule Düsseldorf – University of Applied Sciences
# ZWEK – Centre for Training and Competence Development
# Developed within the KIVi-Azubi research project
"""Pure output formatters for transcription segments.

A *segment* is a mapping with ``start`` and ``end`` (seconds, float) and ``text``
(str). These functions contain no I/O so they can be unit-tested directly.
"""

from __future__ import annotations

import json
from collections.abc import Mapping, Sequence
from typing import Any

Segment = Mapping[str, Any]

VALID_FORMATS = ("txt", "vtt", "srt", "json")


def _clock(seconds: float, sep: str) -> str:
    """Format seconds as HH:MM:SS<sep>mmm (sep is '.' for VTT, ',' for SRT)."""
    if seconds < 0:
        seconds = 0.0
    millis = int(round(seconds * 1000))
    hours, millis = divmod(millis, 3_600_000)
    minutes, millis = divmod(millis, 60_000)
    secs, millis = divmod(millis, 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d}{sep}{millis:03d}"


def to_txt(segments: Sequence[Segment]) -> str:
    """Plain text, one line per segment."""
    return "\n".join(str(s.get("text", "")).strip() for s in segments) + "\n"


def to_vtt(segments: Sequence[Segment]) -> str:
    """WebVTT subtitles."""
    lines = ["WEBVTT", ""]
    for s in segments:
        lines.append(f"{_clock(float(s['start']), '.')} --> {_clock(float(s['end']), '.')}")
        lines.append(str(s.get("text", "")).strip())
        lines.append("")
    return "\n".join(lines)


def to_srt(segments: Sequence[Segment]) -> str:
    """SubRip subtitles."""
    lines: list[str] = []
    for i, s in enumerate(segments, start=1):
        lines.append(str(i))
        lines.append(f"{_clock(float(s['start']), ',')} --> {_clock(float(s['end']), ',')}")
        lines.append(str(s.get("text", "")).strip())
        lines.append("")
    return "\n".join(lines)


def to_json(segments: Sequence[Segment], metadata: Mapping[str, Any] | None = None) -> str:
    """Structured JSON with segments and optional reproducibility metadata."""
    payload: dict[str, Any] = {"segments": list(segments)}
    if metadata is not None:
        payload["metadata"] = dict(metadata)
    return json.dumps(payload, indent=2, ensure_ascii=False)


def render(fmt: str, segments: Sequence[Segment], metadata: Mapping[str, Any] | None = None) -> str:
    """Render ``segments`` in the requested format."""
    if fmt == "txt":
        return to_txt(segments)
    if fmt == "vtt":
        return to_vtt(segments)
    if fmt == "srt":
        return to_srt(segments)
    if fmt == "json":
        return to_json(segments, metadata)
    raise ValueError(f"Unknown format: {fmt!r}. Valid: {', '.join(VALID_FORMATS)}")
