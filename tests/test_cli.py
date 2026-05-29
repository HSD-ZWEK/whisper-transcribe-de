"""CLI orchestration tests with a fake transcriber (no WhisperX required)."""

from __future__ import annotations

import json

import pytest

from whisper_transcribe_de import cli
from whisper_transcribe_de.config import Config
from whisper_transcribe_de.errors import ConfigError


class FakeTranscriber:
    terms = ["isotherm", "isobar"]

    def transcribe(self, audio_path: str):
        return [
            {"start": 0.0, "end": 1.0, "text": "Hallo"},
            {"start": 1.0, "end": 2.0, "text": "Welt"},
        ]


def test_config_from_args_parses_formats():
    args = cli.build_parser().parse_args(["a.mp4", "--formats", "txt, json"])
    cfg = cli.config_from_args(args)
    assert cfg.formats == ["txt", "json"]


def test_config_rejects_unknown_format():
    args = cli.build_parser().parse_args(["a.mp4", "--formats", "txt,docx"])
    with pytest.raises(ConfigError):
        cli.config_from_args(args)


def test_collect_inputs_expands_dirs(tmp_path):
    (tmp_path / "a.mp4").write_text("x")
    (tmp_path / "b.wav").write_text("x")
    (tmp_path / "notes.txt").write_text("x")  # ignored (not media)
    found = cli.collect_inputs([str(tmp_path)])
    assert [p.name for p in found] == ["a.mp4", "b.wav"]


def test_run_writes_outputs_and_metadata(tmp_path):
    media = tmp_path / "lecture.mp4"
    media.write_text("x")
    out = tmp_path / "out"
    args = cli.build_parser().parse_args(
        [str(media), "--out", str(out), "--formats", "vtt,txt,json"]
    )
    rc = cli.run(args, transcriber=FakeTranscriber())
    assert rc == 0
    assert (out / "lecture.vtt").read_text().startswith("WEBVTT")
    assert (out / "lecture.txt").read_text() == "Hallo\nWelt\n"
    meta = json.loads((out / "lecture.meta.json").read_text())["metadata"]
    assert meta["engine"] == "whisperx+align"
    assert meta["vocabulary_terms"] == 2
    assert "created" in meta


def test_run_uses_source_id_for_single_input(tmp_path):
    media = tmp_path / "lecture.mp4"
    media.write_text("x")
    out = tmp_path / "out"
    args = cli.build_parser().parse_args(
        [str(media), "--out", str(out), "--source-id", "panopto-42", "--formats", "txt"]
    )
    cli.run(args, transcriber=FakeTranscriber())
    assert (out / "panopto-42.txt").is_file()
    meta = json.loads((out / "panopto-42.meta.json").read_text())["metadata"]
    assert meta["source_id"] == "panopto-42"


def test_run_autodetects_panopto_id_from_filename(tmp_path):
    uid = "0be13721-4a31-4f1d-b812-aba00144ccda"
    media = tmp_path / f"{uid}.mp4"
    media.write_text("x")
    out = tmp_path / "out"
    args = cli.build_parser().parse_args([str(media), "--out", str(out), "--formats", "txt"])
    cli.run(args, transcriber=FakeTranscriber())
    meta = json.loads((out / f"{uid}.meta.json").read_text())["metadata"]
    assert meta["source_id"] == uid


def test_main_returns_1_on_no_inputs(tmp_path):
    assert cli.main([str(tmp_path / "does_not_exist")]) == 1


def test_config_post_init_default_formats_ok():
    assert Config().formats == ["vtt", "txt", "json"]
