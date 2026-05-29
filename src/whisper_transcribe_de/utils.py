# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) Hochschule Düsseldorf – University of Applied Sciences
# ZWEK – Centre for Training and Competence Development
# Developed within the KIVi-Azubi research project
"""Logging setup and small helpers."""

from __future__ import annotations

import logging
import sys

LOGGER_NAME = "whisper_transcribe_de"

# Media extensions WhisperX / ffmpeg can read.
MEDIA_SUFFIXES = (
    ".mp4",
    ".m4a",
    ".mkv",
    ".webm",
    ".mov",
    ".avi",
    ".mp3",
    ".wav",
    ".flac",
    ".ogg",
    ".opus",
    ".aac",
)


def get_logger() -> logging.Logger:
    """Return the package logger."""
    return logging.getLogger(LOGGER_NAME)


def configure_logging(verbosity: int = 0) -> None:
    """Configure logging to stderr (-1 quiet, 0 info, >=1 debug)."""
    if verbosity < 0:
        level = logging.WARNING
    elif verbosity == 0:
        level = logging.INFO
    else:
        level = logging.DEBUG
    handler = logging.StreamHandler(sys.stderr)
    handler.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))
    logger = get_logger()
    logger.handlers.clear()
    logger.addHandler(handler)
    logger.setLevel(level)
    logger.propagate = False
