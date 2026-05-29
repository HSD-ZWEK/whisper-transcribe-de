# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) Hochschule Düsseldorf – University of Applied Sciences
# ZWEK – Centre for Training and Competence Development
# Developed within the KIVi-Azubi research project
"""Command-line interface and run orchestration."""

from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from . import __version__
from .captions import to_cues
from .config import Config
from .errors import InputError, TranscribeError
from .formats import render
from .metadata import build_metadata
from .provenance import panopto_id_from_name
from .transcriber import Transcriber
from .utils import MEDIA_SUFFIXES, configure_logging, get_logger

_log = get_logger()


def build_parser() -> argparse.ArgumentParser:
    """Construct the argument parser."""
    p = argparse.ArgumentParser(
        prog="whisper-transcribe-de",
        description="Reproducible German transcription of technical audio/video (WhisperX).",
    )
    p.add_argument("inputs", nargs="*", help="Audio/video files or directories.")
    p.add_argument("--model", default="large-v3", help="Whisper model (default: large-v3).")
    p.add_argument("--lang", dest="language", default="de", help="Language code (default: de).")
    p.add_argument("--vocab", help="Domain vocabulary file (one term per line).")
    p.add_argument("--out", default="transcripts", help="Output directory (default: transcripts).")
    p.add_argument("--formats", default="vtt,txt,json", help="Comma-separated: txt,vtt,srt,json.")
    p.add_argument("--device", help="cpu | cuda (default: auto-detect).")
    p.add_argument("--compute-type", help="e.g. float16 | int8 (default: per device).")
    p.add_argument("--beam-size", type=int, default=5, help="Beam size (default: 5).")
    p.add_argument(
        "--temperature", type=float, default=0.0, help="Decoding temperature (default: 0.0)."
    )
    p.add_argument(
        "--no-align",
        dest="align",
        action="store_false",
        help="Disable WhisperX word-level alignment.",
    )
    p.add_argument(
        "--max-cue-seconds", type=float, default=6.0, help="Max caption cue length in seconds."
    )
    p.add_argument(
        "--max-cue-chars", type=int, default=84, help="Max caption cue length in characters."
    )
    p.add_argument("--diarize", action="store_true", help="Enable speaker diarization.")
    p.add_argument("--source-id", help="Provenance id for a single input (e.g. a Panopto id).")
    p.add_argument(
        "--no-id-from-name",
        dest="id_from_name",
        action="store_false",
        help="Do not infer a Panopto id from UUID-named files.",
    )
    p.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=0,
        help="Increase verbosity (repeatable).",
    )
    p.add_argument("-q", "--quiet", action="store_true", help="Only log warnings and errors.")
    p.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    return p


def config_from_args(args: argparse.Namespace) -> Config:
    """Build a :class:`Config` from parsed CLI arguments."""
    formats = [f.strip() for f in str(args.formats).split(",") if f.strip()]
    return Config(
        model=args.model,
        language=args.language,
        device=args.device,
        compute_type=args.compute_type,
        beam_size=args.beam_size,
        temperature=args.temperature,
        align=args.align,
        diarize=args.diarize,
        out_dir=args.out,
        formats=formats,
        vocab_file=args.vocab,
        source_id=args.source_id,
        max_cue_seconds=args.max_cue_seconds,
        max_cue_chars=args.max_cue_chars,
    )


def collect_inputs(paths: Sequence[str]) -> list[Path]:
    """Expand the given paths into a sorted list of media files."""
    files: list[Path] = []
    for raw in paths:
        path = Path(raw)
        if path.is_dir():
            files.extend(sorted(c for c in path.rglob("*") if c.suffix.lower() in MEDIA_SUFFIXES))
        elif path.is_file():
            files.append(path)
        else:
            _log.warning("Skipping missing path: %s", raw)
    # De-duplicate, preserve order.
    seen: set[Path] = set()
    unique: list[Path] = []
    for f in files:
        if f not in seen:
            seen.add(f)
            unique.append(f)
    return unique


def _write_outputs(
    base: str,
    segments: list[dict[str, Any]],
    metadata: dict[str, Any],
    config: Config,
    out_dir: Path,
) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    # Subtitle formats use short caption cues; txt/json keep the full segments.
    cues = to_cues(segments, config.max_cue_seconds, config.max_cue_chars)
    for fmt in config.formats:
        source = cues if fmt in ("vtt", "srt") else segments
        (out_dir / f"{base}.{fmt}").write_text(render(fmt, source, metadata), encoding="utf-8")
    # Always write the reproducibility sidecar.
    (out_dir / f"{base}.meta.json").write_text(render("json", [], metadata), encoding="utf-8")


def run(args: argparse.Namespace, transcriber: Transcriber | None = None) -> int:
    """Execute a configured run. Returns a process exit code."""
    config = config_from_args(args)
    inputs = collect_inputs(args.inputs)
    if not inputs:
        raise InputError("No audio/video files found. Provide files or directories.")

    engine = "whisperx" + ("+align" if config.align else "")
    worker = transcriber if transcriber is not None else Transcriber(config)
    _log.info("Transcribing %d file(s) → %s/", len(inputs), config.out_dir)

    id_from_name = getattr(args, "id_from_name", True)
    for path in inputs:
        _log.info("Transcribing: %s", path.name)
        segments = worker.transcribe(str(path))
        explicit = config.source_id if (config.source_id and len(inputs) == 1) else None
        detected = panopto_id_from_name(path.stem) if id_from_name else None
        source_id = explicit or detected
        base = explicit or path.stem
        metadata = build_metadata(
            source=str(path),
            engine=engine,
            model=config.model,
            language=config.language,
            parameters=config.decoding_parameters(),
            created=datetime.now(timezone.utc).isoformat(timespec="seconds"),
            source_id=source_id,
            vocabulary=worker.terms,
        )
        _write_outputs(base, segments, metadata, config, Path(config.out_dir))
        _log.info("  %d segment(s) → %s.{%s}", len(segments), base, ",".join(config.formats))

    _log.info("Done. Transcripts in: %s/", config.out_dir)
    return 0


def main(argv: Sequence[str] | None = None) -> int:
    """Entry point: parse arguments, configure logging and run."""
    args = build_parser().parse_args(argv)
    configure_logging(-1 if args.quiet else args.verbose)
    try:
        return run(args)
    except TranscribeError as exc:
        _log.error("%s", exc)
        return 1
    except KeyboardInterrupt:  # pragma: no cover
        _log.error("Interrupted.")
        return 130


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
