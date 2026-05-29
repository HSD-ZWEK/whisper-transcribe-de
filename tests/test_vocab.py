"""Tests for domain vocabulary handling."""

from __future__ import annotations

from whisper_transcribe_de.vocab import build_hotwords, build_initial_prompt, load_vocabulary


def test_load_vocabulary_skips_comments_blanks_and_dups(tmp_path):
    path = tmp_path / "vocab.txt"
    path.write_text(
        "# Thermodynamik\nisotherm\nisobar\n\nisotherm\n  isochor  \n# comment\n",
        encoding="utf-8",
    )
    assert load_vocabulary(path) == ["isotherm", "isobar", "isochor"]


def test_build_initial_prompt():
    assert build_initial_prompt(["isotherm", "isobar"]) == "Fachbegriffe: isotherm, isobar."
    assert build_initial_prompt([]) == ""


def test_build_hotwords():
    assert build_hotwords(["isotherm", "isobar"]) == "isotherm isobar"
    assert build_hotwords([]) == ""
