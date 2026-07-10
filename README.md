<p align="center">
  <img src="assets/images/banner.png" alt="loclass – Write here • Read everywhere" width="100%">
</p>

# loclass Starter-Paket

Ein praktisches Starter-Projekt für strukturierte technische Dokumentation mit **loclass** und **LDL**.

`loclass-starter` zeigt, wie aus einer einfachen LDL-Quelle ein vollständiges PDF-Dokument gebaut wird. Das Repository dient gleichzeitig als Referenzstruktur für spätere loclass-Dokumente.

---

## loclass-Ökosystem

| Projekt              | Zweck                                              | Status    |
| -------------------- | -------------------------------------------------- | --------- |
| `loclass-starter`    | Beispiel- und Starterprojekt für loclass-Dokumente | aktiv     |
| `loclass-branding`   | Farben, Wortmarke, Logo und gemeinsame Assets      | aktiv     |
| `loclass-review`     | Review-Boxen für TODO, FIXME, QUESTION und NOTE    | nutzbar   |
| `loclass-versioning` | Versionshistorien aus YAML erzeugen                | nutzbar   |
| `loclass-acronyms`   | Gemeinsame Abkürzungsverzeichnisse für Dokumente   | nutzbar   |
| `loclass`            | späterer Kern für Parser, Renderer und CLI         | im Aufbau |

---

## Was ist loclass?

**loclass** ist ein schlankes Dokumentationssystem für technische Dokumente.

Die Grundidee:

- Inhalte werden in einer einfachen, lesbaren Textsyntax geschrieben.
- Metadaten, Struktur und Darstellung bleiben getrennt.
- Dokumente können modular aufgebaut werden.
- Der erste produktive Ausgabepfad ist aktuell LaTeX/PDF.
- Weitere Ausgabeformate bleiben perspektivisch möglich.

LDL steht für **loclass document language**.

---

## Was ist dieses Repository?

`loclass-starter` ist aktuell ein kombiniertes Starter- und Arbeitsrepository.

Es enthält:

- eine LaTeX-Projektstruktur
- einen LDL-Prototyp
- Parser, Model, Registry, Loader und Renderer
- ein PDF-Build-Werkzeug
- ein vollständiges Beispieldokument
- Tests für die LDL-Grundfunktionen
- ein einheitliches Entwicklungs-Script

Das Repository ist damit noch kein reiner Endanwender-Template-Stand, sondern der aktuelle praktische Entwicklungsstand von loclass für PDF-Dokumente.

---

## Aktueller Funktionsumfang

Aktuell unterstützt LDL in diesem Repository:

- Manifest mit Dokument-Metadaten
- Kapitel und Abschnitte
- Rohtext
- Tabellen
- Bilder
- Code-Blöcke
- Listen
- Shell-Blöcke
- Inline-Auszeichnungen
- modulare LDL-Dateien über `input`
- PDF-Erzeugung über LaTeX

Unterstützte Inline-Auszeichnungen:

```ldl
__cmd{uv run pytest}
__keys{Ctrl+Alt+T}
__url{https://example.org/docs}
__code{None}
```

---

## Schnellstart

Projekt prüfen:

```bash
./dev doctor
```

Tests ausführen:

```bash
./dev test
```

Beispieldokument bauen:

```bash
./loclass ldl examples/full_document.ldl
```

Allgemeinen PDF-Build ausführen:

```bash
./dev build
```

Vollständigen Entwicklungscheck ausführen:

```bash
./dev release-check
```

Ergebnis:

```text
build/full_document.pdf
```

---

## LDL Beispiel

Eine LDL-Hauptdatei besteht aus genau einem Manifest und anschließendem Inhalt.

```ldl
---
title: LDL Beispieldokument
subtitle: Direkt aus LDL gebaut
author: Frank Sieger
company: LogObject
customer: Beispielkunde
language: de
theme: default
version: 0.1.0
revision: 1
date: 2026-07-09
---

input
  content/chapterone.ldl

Starte die Tests mit __cmd{uv run pytest}.

Drücke __keys{Ctrl+Alt+T}.

Weitere Informationen stehen unter __url{https://example.org/docs}.

Der Rückgabewert ist __code{None}.
```

Eine eingebundene Datei kann zum Beispiel so aussehen:

```ldl
chapter
  Einführung

Dies ist ein LDL-Testdokument.

section
  Ausführung

Die Konfiguration liegt unter __code{/etc/nginx/nginx.conf}.
```

---

## LDL `input`

Mit `input` können LDL-Dokumente modular aufgebaut werden.

```ldl
input
  content/chapterone.ldl
```

Regeln:

- Pfade werden relativ zu der Datei aufgelöst, in der das `input` steht.
- Eingebundene Dateien enthalten nur Inhalt.
- Das Manifest steht ausschließlich in der Hauptdatei.
- Ein Dokument hat genau ein Manifest.
- Fehlende Dateien werden verständlich gemeldet.
- Zirkuläre Includes werden erkannt und abgebrochen.

Beispielstruktur:

```text
examples/
├── full_document.ldl
└── content/
    └── chapterone.ldl
```

---

## Projektstruktur

```text
.
├── assets/
│   └── images/
├── content/
├── core/
│   ├── ldl/
│   └── tools/
├── examples/
│   └── content/
├── project/
├── dev
├── main.tex
├── latexmkrc
├── loclass
├── pyproject.toml
└── README.md
```

| Pfad             | Zweck                                               |
| ---------------- | --------------------------------------------------- |
| `assets/images/` | Bilder, Logos und Branding-Assets                   |
| `content/`       | LaTeX-Content-Bereich für den Build                 |
| `core/ldl/`      | LDL-Model, Parser, Registry, Loader und Renderer    |
| `core/tools/`    | Build-Werkzeuge, aktuell insbesondere PDF-Erzeugung |
| `examples/`      | LDL-Beispieldokumente                               |
| `project/`       | projektbezogene LaTeX-Konfiguration                 |
| `dev`            | einheitliches Entwicklungs-Script für Checks/Builds |
| `main.tex`       | LaTeX-Haupteinstieg                                 |
| `latexmkrc`      | latexmk-Konfiguration                               |
| `loclass`        | lokaler Build-Wrapper                               |
| `pyproject.toml` | Python-Projektkonfiguration                         |

---

## Entwicklung

Das Repository verwendet ein einheitliches Entwicklungs-Script:

```bash
./dev doctor
./dev test
./dev lint
./dev typecheck
./dev build
./dev release-check
```

Die projektspezifische Konfiguration liegt in `pyproject.toml`.

Für dieses Repository sind insbesondere relevant:

```toml
[tool.pytest.ini_options]
testpaths = [
    "core/tests",
]

[tool.loclass.dev]
tex_main = "main.tex"
build_dir = "build"
typecheck = ["core"]
lint = ["."]
```

`./dev release-check` führt die wichtigsten Prüfungen gesammelt aus:

```text
doctor
→ tests
→ ruff
→ mypy
→ PDF-Build
→ TODO/FIXME-Kommentarprüfung
→ git status
```

---

## Build-Ablauf

Beim Aufruf

```bash
./loclass ldl examples/full_document.ldl
```

passiert grob:

```text
LDL-Datei laden
→ input-Dateien rekursiv auflösen
→ Dokumentbaum erzeugen
→ LaTeX-Dateien generieren
→ latexmk ausführen
→ PDF schreiben
```

---

## Roadmap

| Version | Ziel                              | Status   |
| ------- | --------------------------------- | -------- |
| `v0.1`  | bereinigter LaTeX-Startpunkt      | erledigt |
| `v0.2`  | modulare LaTeX-Struktur           | erledigt |
| `v0.3`  | LDL-Grundsyntax                   | erledigt |
| `v0.4`  | LDL-Renderer nach LaTeX           | erledigt |
| `v0.5`  | modulares LDL über `input`        | erledigt |
| `v1.0`  | produktiv nutzbarer Dokumentenbau | offen    |

---

## Designprinzipien

loclass folgt einigen einfachen Regeln:

- Dokumente sollen lesbar bleiben.
- LDL soll einfacher sein als direktes LaTeX.
- Struktur und Darstellung bleiben getrennt.
- Ein Dokument besitzt genau ein Manifest.
- Eingebundene LDL-Dateien sind Inhaltsmodule.
- Der LaTeX-Backendpfad bleibt nachvollziehbar.
- Erweiterungen sollen modular bleiben.
