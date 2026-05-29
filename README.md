# whisper-transcribe-de

🇩🇪 German documentation: [README.de.md](README.de.md)

[![CI](https://github.com/HSD-ZWEK/whisper-transcribe-de/actions/workflows/ci.yml/badge.svg)](https://github.com/HSD-ZWEK/whisper-transcribe-de/actions/workflows/ci.yml)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12-blue.svg)](pyproject.toml)

whisper-transcribe-de is a command-line tool for reproducible German speech transcription
of technical and mathematical audio and video, built on
[WhisperX](https://github.com/m-bain/whisperx).

> **Disclaimer.** This tool is intended for recordings that the operator or their
> institution is permitted to process. Transcription runs locally (no cloud API), which
> supports data protection for recordings containing identifiable persons. Machine
> transcripts are drafts and require human review before scholarly use. Use is at the
> operator's own responsibility and subject to the applicable copyright and data
> protection rules.

## Overview

The tool transcribes audio/video files locally with WhisperX (a faster-whisper backend
with voice-activity detection and word-level alignment). It is geared towards German
technical and mathematical content: a curated domain vocabulary is supplied to the model
as a prompt to bias decoding towards the correct terminology. Each transcript is written
in standard formats alongside a reproducibility metadata sidecar.

## Features

- Local German transcription via WhisperX (faster-whisper backend); no cloud API.
- Domain vocabulary prompting from an editable term list (per course or learning unit).
- Word-level timestamps through WhisperX alignment; optional speaker diarization.
- Output as TXT, VTT, SRT and JSON, plus a `.meta.json` reproducibility sidecar.
- Deterministic decoding defaults (`temperature = 0`) and recorded parameters.
- Provenance link to a source id (e.g. a Panopto video id), complementing
  [moodle-panopto-downloader](https://github.com/HSD-ZWEK/moodle-panopto-downloader).

## Requirements

- Python 3.10 or newer.
- `ffmpeg` available on `PATH`.
- The WhisperX backend (optional dependency) for actual transcription; the package
  installs and runs its tests without it.

## Installation

```bash
pip install .                 # core (pure logic, CLI)
pip install ".[whisperx]"     # add the WhisperX backend (pulls torch + faster-whisper)
```

`ffmpeg` is provided per platform:

```bash
# Linux (Debian/Ubuntu)
sudo apt install ffmpeg
# macOS (Homebrew)
brew install ffmpeg
# Windows (winget)
winget install Gyan.FFmpeg
```

After installation the command `whisper-transcribe-de` is available; the tool can also be
invoked through `python -m whisper_transcribe_de`.

## Configuration

A curated domain vocabulary improves recognition of technical terms. The vocabulary is a
plain-text file (one term per line; `#` comments and blank lines are ignored). A template
is provided in [`vocab.example.txt`](vocab.example.txt):

```text
Zustandsgleichung
ideale Gase
isotherm
isobar
```

Decoding behaviour is controlled by CLI options (`--model`, `--beam-size`,
`--temperature`, `--no-align`, `--diarize`, `--device`, `--compute-type`).

## Usage

```bash
# Transcribe one file with a domain vocabulary, write VTT/TXT/JSON:
whisper-transcribe-de lecture.mp4 --vocab vocab.txt --formats vtt,txt,json --out transcripts

# Transcribe every media file in a directory:
whisper-transcribe-de ./videos --vocab vocab.txt

# Attach a provenance id (e.g. the Panopto video id) for a single input:
whisper-transcribe-de lecture.mp4 --source-id 0be13721-4a31-4f1d-b812-aba00144ccda
```

For each input, the tool writes `<name>.<format>` for every requested format and a
`<name>.meta.json` sidecar recording engine, model, decoding parameters and source. With
`--source-id` (single input) the source id is used as the base name and recorded as
provenance.

### Options

| Option | Description |
|---|---|
| `--model NAME` | Whisper model (default `large-v3`). |
| `--lang CODE` | Language code (default `de`). |
| `--vocab FILE` | Domain vocabulary file (one term per line). |
| `--out DIR` | Output directory (default `transcripts`). |
| `--formats LIST` | Comma-separated: `txt,vtt,srt,json` (default `vtt,txt,json`). |
| `--device NAME` | `cpu` or `cuda` (default: auto-detect). |
| `--compute-type T` | e.g. `float16` or `int8` (default per device). |
| `--beam-size N` | Beam size (default 5). |
| `--temperature F` | Decoding temperature (default 0.0). |
| `--no-align` | Disable WhisperX word-level alignment. |
| `--max-cue-seconds F` | Max subtitle cue length in seconds (default 6.0). |
| `--max-cue-chars N` | Max subtitle cue length in characters (default 84). |
| `--diarize` | Enable speaker diarization. |
| `--source-id ID` | Provenance id for a single input. |
| `--no-id-from-name` | Do not infer a Panopto id from UUID-named files. |
| `-v`, `--verbose` | Increase log verbosity (repeatable). |
| `-q`, `--quiet` | Log warnings and errors only. |

## Examples

A typical research workflow combined with the companion downloader:

```bash
# 1) Retrieve the course recordings, named by Panopto id (separate tool):
moodle-panopto-downloader 210 --id-filenames --out videos

# 2) Transcribe them with the learning-unit vocabulary:
whisper-transcribe-de ./videos --vocab vocab_kurs210.txt --formats vtt,txt,json --out transcripts
```

Because the recordings are named by their Panopto id, each transcript's `.meta.json`
records that id as provenance automatically. The resulting transcripts and sidecars
provide a reproducible, reviewable text basis for the didactic analysis.

## Troubleshooting

- **`WhisperX is not installed`.** Install the backend: `pip install ".[whisperx]"`.
- **`ffmpeg` not found.** Install ffmpeg and ensure it is on `PATH`.
- **Slow on CPU.** Use a smaller model (`--model medium`) or a CUDA device
  (`--device cuda`); WhisperX is markedly faster on a GPU.
- **Technical terms misrecognized.** Extend the `--vocab` file with the relevant terms.

## Privacy and Legal Considerations

Transcription runs locally; audio is not sent to a third-party service, which supports
data protection for recordings containing identifiable persons. Recordings and resulting
transcripts are subject to the copyright, terms of use and data protection rules of the
respective institution. Responsibility for lawful processing rests with the operator.

## Project Background

This software was developed at Hochschule Düsseldorf (University of Applied Sciences) by
ZWEK – Centre for Training and Competence Development (Zentrum für Weiterbildung und
Kompetenzentwicklung) within the KIVi-Azubi research project.

```
Copyright (c) Hochschule Düsseldorf – University of Applied Sciences
ZWEK – Centre for Training and Competence Development
Developed within the KIVi-Azubi research project
```

## Research Context

The tool was developed within the KIVi-Azubi research project at Hochschule Düsseldorf,
ZWEK – Centre for Training and Competence Development. The project conducts a
media-pedagogical analysis of digital teaching and learning infrastructures and analyses
Moodle learning units through the revised Bloom taxonomy (Anderson & Krathwohl) and TPACK
(Mishra & Koehler).

Explanatory videos are part of the analysed course material. Transcribing them produces a
reviewable text basis for assessing how far they support concept understanding, and — with
local processing and reproducibility metadata — supports research data management with
stable references to the analysed media. Authorship and provenance are documented in
[`CITATION.cff`](CITATION.cff) and [`AUTHORS.md`](AUTHORS.md).

## AI use

Parts of this software were developed, refactored, and reviewed with the assistance of
generative AI tools (2026). All output was reviewed, tested, and validated by the author,
who takes sole responsibility for the software.

## Citation

Machine-readable citation metadata are provided in [`CITATION.cff`](CITATION.cff),
validated against CFF schema 1.2.0. For a persistently verifiable reference, a release is
archived on [Zenodo](https://zenodo.org); the resulting DOI is then added to
`CITATION.cff` and referenced here.

## License

Released under the [GNU General Public License v3.0 or later](LICENSE). As a copyleft
license, the GPL requires that redistributions and modified versions are also licensed
under the GPL.
