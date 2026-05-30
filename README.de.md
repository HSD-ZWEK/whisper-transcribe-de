# whisper-transcribe-de

🇬🇧 English documentation: [README.md](README.md)

[![CI](https://github.com/HSD-ZWEK/whisper-transcribe-de/actions/workflows/ci.yml/badge.svg)](https://github.com/HSD-ZWEK/whisper-transcribe-de/actions/workflows/ci.yml)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12-blue.svg)](pyproject.toml)

whisper-transcribe-de ist ein Kommandozeilenwerkzeug für die reproduzierbare deutsche
Transkription von Audio- und Videoinhalten, aufgebaut auf
[WhisperX](https://github.com/m-bain/whisperx). Ein gepflegtes Fachvokabular passt die
Erkennung an beliebige Themengebiete an.

> **Hinweis.** Dieses Werkzeug ist für Aufzeichnungen gedacht, die die ausführende Person
> bzw. ihre Einrichtung verarbeiten darf. Die Transkription läuft lokal (keine Cloud-API),
> was den Datenschutz bei Aufzeichnungen mit erkennbaren Personen unterstützt. Maschinelle
> Transkripte sind Entwürfe und erfordern vor wissenschaftlicher Nutzung eine menschliche
> Prüfung. Die Nutzung erfolgt in eigener Verantwortung und unter Vorbehalt des Urheber-
> und Datenschutzrechts.

## Überblick

Das Werkzeug transkribiert deutsche Audio-/Videodateien lokal mit WhisperX
(faster-whisper-Backend mit Sprachaktivitätserkennung und wortgenauer Ausrichtung). Ein
gepflegtes Fachvokabular wird dem Modell als Prompt übergeben, um die Dekodierung zu den
korrekten Termini des jeweiligen Themengebiets zu lenken — das kann ein beliebiges Feld
sein (etwa technische und mathematische Inhalte, ebenso aber Medizin, Recht oder
Geisteswissenschaften). Jedes Transkript wird in Standardformaten zusammen mit einer
Reproduzierbarkeits-Metadatendatei abgelegt.

## Funktionen

- Lokale deutsche Transkription via WhisperX (faster-whisper-Backend); keine Cloud-API.
- Fachvokabular-Prompting aus einer editierbaren Begriffsliste (pro Kurs/Lerneinheit).
- Wortgenaue Timestamps durch WhisperX-Ausrichtung; optionale Sprecher-Diarisierung.
- Ausgabe als TXT, VTT, SRT und JSON sowie eine `.meta.json`-Reproduzierbarkeitsdatei.
- Deterministische Dekodier-Vorgaben (`temperature = 0`) und protokollierte Parameter.
- Provenienz-Verknüpfung mit einer Quell-ID (z. B. Panopto-Video-ID), ergänzend zu
  [moodle-panopto-downloader](https://github.com/HSD-ZWEK/moodle-panopto-downloader).

## Voraussetzungen

- Python 3.10 oder neuer.
- `ffmpeg` im Suchpfad (`PATH`).
- Das WhisperX-Backend (optionale Abhängigkeit) für die eigentliche Transkription; das
  Paket lässt sich ohne dieses installieren und testen.

## Installation

```bash
pip install .                 # Kern (reine Logik, CLI)
pip install ".[whisperx]"     # WhisperX-Backend ergänzen (zieht torch + faster-whisper)
```

`ffmpeg` wird je Plattform bereitgestellt:

```bash
# Linux (Debian/Ubuntu)
sudo apt install ffmpeg
# macOS (Homebrew)
brew install ffmpeg
# Windows (winget)
winget install Gyan.FFmpeg
```

Nach der Installation steht der Befehl `whisper-transcribe-de` zur Verfügung; der Aufruf
über `python -m whisper_transcribe_de` ist ebenfalls möglich.

## Konfiguration

Ein gepflegtes Fachvokabular verbessert die Erkennung von Fachbegriffen. Das Vokabular ist
eine Textdatei (ein Begriff pro Zeile; `#`-Kommentare und Leerzeilen werden ignoriert).
Eine Vorlage liegt in [`vocab.example.txt`](vocab.example.txt):

```text
Zustandsgleichung
ideale Gase
isotherm
isobar
```

Das Dekodierverhalten wird über CLI-Optionen gesteuert (`--model`, `--beam-size`,
`--temperature`, `--no-align`, `--diarize`, `--device`, `--compute-type`).

## Verwendung

```bash
# Eine Datei mit Fachvokabular transkribieren, VTT/TXT/JSON schreiben:
whisper-transcribe-de lecture.mp4 --vocab vocab.txt --formats vtt,txt,json --out transcripts

# Alle Mediendateien eines Verzeichnisses transkribieren:
whisper-transcribe-de ./videos --vocab vocab.txt

# Eine Provenienz-ID (z. B. die Panopto-Video-ID) für eine einzelne Datei anhängen:
whisper-transcribe-de lecture.mp4 --source-id 0be13721-4a31-4f1d-b812-aba00144ccda
```

Pro Eingabe schreibt das Werkzeug `<Name>.<Format>` für jedes gewünschte Format sowie eine
`<Name>.meta.json`-Datei mit Engine, Modell, Dekodierparametern und Quelle. Mit
`--source-id` (eine Datei) wird die Quell-ID als Basisname verwendet und als Provenienz
festgehalten.

### Optionen

| Option | Beschreibung |
|---|---|
| `--model NAME` | Whisper-Modell (Vorgabe `large-v3`). |
| `--lang CODE` | Sprachcode (Vorgabe `de`). |
| `--vocab DATEI` | Fachvokabular-Datei (ein Begriff pro Zeile). |
| `--out ORDNER` | Zielordner (Vorgabe `transcripts`). |
| `--formats LISTE` | Kommagetrennt: `txt,vtt,srt,json` (Vorgabe `vtt,txt,json`). |
| `--device NAME` | `cpu` oder `cuda` (Vorgabe: Auto-Erkennung). |
| `--compute-type T` | z. B. `float16` oder `int8` (Vorgabe je Gerät). |
| `--beam-size N` | Beam-Größe (Vorgabe 5). |
| `--temperature F` | Dekodier-Temperatur (Vorgabe 0.0). |
| `--no-align` | WhisperX-Wortausrichtung deaktivieren. |
| `--max-cue-seconds F` | Max. Untertitel-Cue-Länge in Sekunden (Vorgabe 6.0). |
| `--max-cue-chars N` | Max. Untertitel-Cue-Länge in Zeichen (Vorgabe 84). |
| `--diarize` | Sprecher-Diarisierung aktivieren. |
| `--source-id ID` | Provenienz-ID für eine einzelne Eingabe. |
| `--no-id-from-name` | Keine Panopto-ID aus UUID-benannten Dateien ableiten. |
| `-v`, `--verbose` | Höhere Protokollausführlichkeit (mehrfach steigerbar). |
| `-q`, `--quiet` | Nur Warnungen und Fehler protokollieren. |

## Beispiele

Ein typischer Forschungsablauf zusammen mit dem ergänzenden Downloader:

```bash
# 1) Kursaufzeichnungen beschaffen, benannt nach Panopto-ID (separates Werkzeug):
moodle-panopto-downloader 210 --id-filenames --out videos

# 2) Mit dem Lerneinheits-Vokabular transkribieren:
whisper-transcribe-de ./videos --vocab vocab_kurs210.txt --formats vtt,txt,json --out transcripts
```

Da die Aufzeichnungen nach ihrer Panopto-ID benannt sind, hält jedes `.meta.json` diese
ID automatisch als Provenienz fest. Die entstehenden Transkripte und Sidecar-Dateien
bilden eine reproduzierbare, prüfbare Textgrundlage für die didaktische Analyse.

## Fehlerbehebung

- **`WhisperX is not installed`.** Backend installieren: `pip install ".[whisperx]"`.
- **`ffmpeg` nicht gefunden.** ffmpeg installieren und im `PATH` bereitstellen.
- **Langsam auf der CPU.** Kleineres Modell (`--model medium`) oder ein CUDA-Gerät
  (`--device cuda`) nutzen; WhisperX ist auf einer GPU deutlich schneller.
- **Fachbegriffe falsch erkannt.** Die `--vocab`-Datei um die relevanten Begriffe ergänzen.

## Datenschutz und rechtliche Hinweise

Die Transkription läuft lokal; Audio wird nicht an einen Drittdienst gesendet, was den
Datenschutz bei Aufzeichnungen mit erkennbaren Personen unterstützt. Aufzeichnungen und
resultierende Transkripte unterliegen dem Urheberrecht, den Nutzungsbedingungen und dem
Datenschutzrecht der jeweiligen Einrichtung. Die Verantwortung für eine rechtmäßige
Verarbeitung liegt bei der ausführenden Person.

## Projekthintergrund

Diese Software wurde an der Hochschule Düsseldorf durch ZWEK – Zentrum für Weiterbildung
und Kompetenzentwicklung im Forschungsprojekt KIVi-Azubi entwickelt.

```
Copyright (c) Hochschule Düsseldorf
ZWEK – Zentrum für Weiterbildung und Kompetenzentwicklung
Entwickelt im Forschungsprojekt KIVi-Azubi
```

## Forschungskontext

Das Werkzeug wurde im Forschungsprojekt KIVi-Azubi an der Hochschule Düsseldorf, ZWEK –
Zentrum für Weiterbildung und Kompetenzentwicklung, entwickelt. Das Projekt führt eine
medienpädagogische Analyse digitaler Lehr-/Lerninfrastrukturen durch und analysiert
Moodle-Lerneinheiten anhand der revidierten Bloom-Taxonomie (Anderson & Krathwohl) und
TPACK (Mishra & Koehler).

Erklärvideos sind Teil des analysierten Kursmaterials. Ihre Transkription liefert eine
prüfbare Textgrundlage, um zu bewerten, inwieweit sie das Begriffsverständnis stützen, und
unterstützt — mit lokaler Verarbeitung und Reproduzierbarkeits-Metadaten — ein
Forschungsdatenmanagement mit stabilen Referenzen auf die analysierten Medien.
Autorenschaft und Herkunft sind in [`CITATION.cff`](CITATION.cff) und
[`AUTHORS.md`](AUTHORS.md) dokumentiert.

## KI-Einsatz

Teile dieser Software wurden mit Unterstützung generativer KI-Werkzeuge entwickelt,
überarbeitet und geprüft (2026). Alle Ergebnisse wurden vom Autor überprüft, getestet und
validiert; die Verantwortung für die Software liegt allein beim Autor.

## Zitation

Die maschinenlesbaren Zitationsmetadaten liegen in [`CITATION.cff`](CITATION.cff),
validiert gegen das CFF-Schema 1.2.0. Für eine dauerhaft verifizierbare Referenz wird ein
Release über [Zenodo](https://zenodo.org) archiviert; die resultierende DOI wird
anschließend in `CITATION.cff` eingetragen und hier referenziert.

## Lizenz

Veröffentlicht unter der [GNU General Public License v3.0 oder später](LICENSE). Als
Copyleft-Lizenz verpflichtet die GPL dazu, dass Weitergaben und abgewandelte Versionen
ebenfalls unter der GPL stehen.
