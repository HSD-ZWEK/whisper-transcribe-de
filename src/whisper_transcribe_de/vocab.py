# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) Hochschule Düsseldorf – University of Applied Sciences
# ZWEK – Centre for Training and Competence Development
# Developed within the KIVi-Azubi research project
"""Domain vocabulary handling.

Whisper tends to flatten specialised terminology. Providing the domain terms as an
``initial_prompt`` (and, where supported, as ``hotwords``) biases decoding towards the
correct domain terms (of any subject). The vocabulary is kept in an editable plain-text
file so it can be curated per course or learning unit.
"""

from __future__ import annotations

from pathlib import Path


def load_vocabulary(path: str | Path) -> list[str]:
    """Read a vocabulary file: one term per line, ``#`` comments and blanks ignored.

    Order is preserved and duplicates are removed (first occurrence wins).
    """
    terms: list[str] = []
    seen: set[str] = set()
    for raw in Path(path).read_text(encoding="utf-8").splitlines():
        term = raw.strip()
        if not term or term.startswith("#"):
            continue
        key = term.casefold()
        if key not in seen:
            seen.add(key)
            terms.append(term)
    return terms


def build_initial_prompt(terms: list[str]) -> str:
    """Build a German priming prompt that lists the domain terms.

    The prompt is plain text that Whisper treats as preceding context, nudging the
    decoder towards the listed vocabulary. Returns an empty string for no terms.
    """
    if not terms:
        return ""
    return "Fachbegriffe: " + ", ".join(terms) + "."


def build_hotwords(terms: list[str]) -> str:
    """Build a space-separated hotword string (used by faster-whisper's ``hotwords``)."""
    return " ".join(terms)
