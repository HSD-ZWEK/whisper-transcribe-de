"""Tests for Panopto-id provenance detection."""

from __future__ import annotations

from whisper_transcribe_de.provenance import panopto_id_from_name


def test_uuid_stem_is_detected():
    uid = "0be13721-4a31-4f1d-b812-aba00144ccda"
    assert panopto_id_from_name(uid) == uid
    assert panopto_id_from_name(uid.upper()) == uid  # normalised to lower-case


def test_non_uuid_stem_returns_none():
    assert panopto_id_from_name("Lecture_1") is None
    assert panopto_id_from_name("") is None
    # A UUID embedded in a longer name is not an exact match.
    assert panopto_id_from_name("vid-0be13721-4a31-4f1d-b812-aba00144ccda") is None
