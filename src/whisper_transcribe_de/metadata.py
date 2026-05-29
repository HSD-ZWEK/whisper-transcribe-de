# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) Hochschule Düsseldorf – University of Applied Sciences
# ZWEK – Centre for Training and Competence Development
# Developed within the KIVi-Azubi research project
"""Reproducibility metadata for each transcript.

A sidecar metadata object records exactly how a transcript was produced (engine,
model, decoding parameters, source) so that results are reproducible and the
transcript can be traced back to its source recording.
"""

from __future__ import annotations

from typing import Any

from . import __version__


def build_metadata(
    *,
    source: str,
    engine: str,
    model: str,
    language: str,
    parameters: dict[str, Any],
    created: str | None = None,
    source_id: str | None = None,
    vocabulary: list[str] | None = None,
) -> dict[str, Any]:
    """Assemble the reproducibility metadata for one transcript.

    ``created`` (an ISO timestamp) and ``source_id`` (e.g. a Panopto video id) are
    passed in by the caller to keep this function pure and deterministic.
    """
    meta: dict[str, Any] = {
        "tool": "whisper-transcribe-de",
        "tool_version": __version__,
        "engine": engine,
        "model": model,
        "language": language,
        "parameters": dict(parameters),
        "source": source,
        "asr_note": "Machine-generated draft; requires human review before scholarly use.",
    }
    if created is not None:
        meta["created"] = created
    if source_id is not None:
        meta["source_id"] = source_id
    if vocabulary is not None:
        meta["vocabulary_terms"] = len(vocabulary)
    return meta
