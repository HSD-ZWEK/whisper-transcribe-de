# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) Hochschule Düsseldorf – University of Applied Sciences
# ZWEK – Centre for Training and Competence Development
# Developed within the KIVi-Azubi research project
"""Runtime configuration for a transcription run."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .errors import ConfigError
from .formats import VALID_FORMATS


@dataclass
class Config:
    """Fully resolved configuration for a transcription run."""

    model: str = "large-v3"
    language: str = "de"
    device: str | None = None  # None → auto-detect in the backend
    compute_type: str | None = None
    beam_size: int = 5
    temperature: float = 0.0
    vad: bool = True
    align: bool = True  # WhisperX word-level timestamps
    diarize: bool = False
    out_dir: str = "transcripts"
    formats: list[str] = field(default_factory=lambda: ["vtt", "txt", "json"])
    vocab_file: str | None = None
    source_id: str | None = None
    max_cue_seconds: float = 6.0
    max_cue_chars: int = 84

    def __post_init__(self) -> None:
        invalid = [f for f in self.formats if f not in VALID_FORMATS]
        if invalid:
            raise ConfigError(
                f"Unknown output format(s): {', '.join(invalid)}. "
                f"Valid: {', '.join(VALID_FORMATS)}."
            )

    def decoding_parameters(self) -> dict[str, Any]:
        """The decoding settings recorded in each transcript's metadata."""
        return {
            "beam_size": self.beam_size,
            "temperature": self.temperature,
            "vad": self.vad,
            "align": self.align,
            "diarize": self.diarize,
        }
