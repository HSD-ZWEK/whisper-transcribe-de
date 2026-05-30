# Changelog

All notable changes to this project are documented in this file. The format is based on
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and the project adheres to
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-05-29

Initial release.

### Added

- Command-line tool for German transcription of audio/video built on WhisperX
  (`whisper-transcribe-de`, `python -m whisper_transcribe_de`).
- Domain vocabulary prompting (editable term list) to bias decoding towards the
  terminology of any subject; word-level timestamps via WhisperX alignment.
- Output formats: TXT, VTT, SRT and JSON, plus a `.meta.json` reproducibility sidecar
  (engine, model, decoding parameters, source, optional provenance id).
- Local-only processing (no cloud API); WhisperX is an optional dependency and is
  imported lazily.
- Test suite (pytest) for the pure logic, linting (ruff), type checking (mypy) and CI on
  Linux, macOS and Windows for Python 3.10–3.12.
- Bilingual documentation (`README.md`, `README.de.md`) and citation metadata
  (`CITATION.cff`).

[0.1.0]: https://github.com/HSD-ZWEK/whisper-transcribe-de/releases/tag/v0.1.0
