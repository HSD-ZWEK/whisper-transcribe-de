# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) Hochschule Düsseldorf – University of Applied Sciences
# ZWEK – Centre for Training and Competence Development
# Developed within the KIVi-Azubi research project
"""whisper-transcribe-de — reproducible German speech transcription for audio/video,
built on WhisperX, with domain-vocabulary prompting that adapts it to any subject.

The package separates pure, testable logic (vocabulary/prompt handling, output
formatting, reproducibility metadata) from the WhisperX backend, which is imported
lazily so the package can be installed, imported and tested without the heavy ASR
dependencies present.
"""

from __future__ import annotations

__all__ = ["__version__"]
__version__ = "0.1.0"
