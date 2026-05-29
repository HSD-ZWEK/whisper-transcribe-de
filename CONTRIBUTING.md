# Mitwirken

Beiträge sind willkommen – Fehlerberichte, Verbesserungsvorschläge und Pull
Requests. Dieses Dokument beschreibt den Entwicklungsablauf.

## Entwicklungsumgebung

```bash
git clone https://github.com/HSD-ZWEK/whisper-transcribe-de.git
cd whisper-transcribe-de
python3 -m venv .venv
source .venv/bin/activate            # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
# Fuer echte Transkriptionen zusaetzlich das ASR-Backend:
# pip install -e ".[whisperx]"
```

## Tests und Linting

```bash
pytest                 # Testsuite (laeuft ohne WhisperX)
ruff check .           # Linting
ruff format .          # Formatierung
mypy                   # Typpruefung
```

Die CI führt Linting, Typprüfung und Tests auf Linux, macOS und Windows über mehrere
Python-Versionen aus. Die reine Logik (Vokabular, Formate, Metadaten) ist ohne das
WhisperX-Backend testbar; der Backend-Aufruf wird in Tests gemockt.

## Konventionen

- Code folgt PEP 8; Formatierung und Lint-Regeln werden über `ruff` durchgesetzt.
- Öffentliche Funktionen und Klassen erhalten Type-Hints und Docstrings.
- Netzwerk-/Backend-Code bleibt von der Kernlogik getrennt, damit Letztere ohne
  schwere Abhängigkeiten testbar bleibt.
- Neue Funktionalität wird durch Tests abgedeckt.
- `README.md` und `README.de.md` werden inhaltlich synchron gehalten.

## Sicherheitsrelevante Meldungen

Siehe [`SECURITY.md`](SECURITY.md).
