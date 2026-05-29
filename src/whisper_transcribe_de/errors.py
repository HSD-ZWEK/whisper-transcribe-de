# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) Hochschule Düsseldorf – University of Applied Sciences
# ZWEK – Centre for Training and Competence Development
# Developed within the KIVi-Azubi research project
"""Exception hierarchy for whisper-transcribe-de."""

from __future__ import annotations


class TranscribeError(Exception):
    """Base class for all errors raised by this package."""


class ConfigError(TranscribeError):
    """Configuration is missing or inconsistent."""


class BackendError(TranscribeError):
    """The ASR backend (WhisperX) is unavailable or failed."""


class InputError(TranscribeError):
    """No usable input files were given."""
