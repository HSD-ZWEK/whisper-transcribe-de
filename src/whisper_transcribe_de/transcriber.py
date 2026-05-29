# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) Hochschule Düsseldorf – University of Applied Sciences
# ZWEK – Centre for Training and Competence Development
# Developed within the KIVi-Azubi research project
"""WhisperX backend wrapper.

WhisperX (and its torch/faster-whisper dependencies) is imported lazily inside the
methods, so the package can be imported and unit-tested without these heavy packages
installed. Install the backend with ``pip install ".[whisperx]"`` to run transcriptions.
"""

from __future__ import annotations

from typing import Any

from .config import Config
from .errors import BackendError
from .utils import get_logger
from .vocab import build_initial_prompt, load_vocabulary

_log = get_logger()


def _auto_device(preferred: str | None) -> str:
    if preferred:
        return preferred
    try:
        import torch

        return "cuda" if torch.cuda.is_available() else "cpu"
    except Exception:  # pragma: no cover - torch optional at import time
        return "cpu"


def _default_compute_type(device: str, preferred: str | None) -> str:
    if preferred:
        return preferred
    return "float16" if device == "cuda" else "int8"


class Transcriber:
    """Loads a WhisperX model once and transcribes audio/video files.

    The model is loaded lazily on first use.
    """

    def __init__(self, config: Config) -> None:
        self.config = config
        self.device = _auto_device(config.device)
        self.compute_type = _default_compute_type(self.device, config.compute_type)
        self.terms = load_vocabulary(config.vocab_file) if config.vocab_file else []
        self._model: Any | None = None

    def _load_model(self) -> Any:
        if self._model is not None:
            return self._model
        try:
            import whisperx
        except ImportError as exc:  # pragma: no cover - exercised only without backend
            raise BackendError(
                'WhisperX is not installed. Install it with: pip install ".[whisperx]" '
                "(this pulls in torch and faster-whisper). ffmpeg must also be available."
            ) from exc

        asr_options = {
            "beam_size": self.config.beam_size,
            "temperatures": [self.config.temperature],
            "initial_prompt": build_initial_prompt(self.terms) or None,
        }
        _log.info("Loading model %s on %s (%s)…", self.config.model, self.device, self.compute_type)
        self._model = whisperx.load_model(
            self.config.model,
            self.device,
            compute_type=self.compute_type,
            language=self.config.language,
            asr_options=asr_options,
        )
        return self._model

    def transcribe(self, audio_path: str) -> list[dict[str, Any]]:
        """Transcribe one file and return a list of ``{start, end, text}`` segments."""
        import whisperx

        model = self._load_model()
        audio = whisperx.load_audio(audio_path)
        result = model.transcribe(audio, language=self.config.language)
        segments: list[dict[str, Any]] = list(result.get("segments", []))

        if self.config.align and segments:
            align_model, meta = whisperx.load_align_model(
                language_code=self.config.language, device=self.device
            )
            aligned = whisperx.align(
                segments, align_model, meta, audio, self.device, return_char_alignments=False
            )
            segments = list(aligned.get("segments", segments))

        return segments
