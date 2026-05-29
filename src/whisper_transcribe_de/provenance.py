# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) Hochschule Düsseldorf – University of Applied Sciences
# ZWEK – Centre for Training and Competence Development
# Developed within the KIVi-Azubi research project
"""Provenance helpers linking transcripts to their source recording.

When recordings are downloaded with ``moodle-panopto-downloader --id-filenames``, each
file is named after its Panopto session id (a UUID). Detecting that id from the file
name lets the transcriber record provenance automatically.
"""

from __future__ import annotations

import re

_UUID = re.compile(r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$", re.IGNORECASE)


def panopto_id_from_name(stem: str) -> str | None:
    """Return the Panopto id if ``stem`` is exactly a UUID, else ``None``."""
    return stem.lower() if _UUID.match(stem) else None
