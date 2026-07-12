<p align="center">
  <strong>loclass</strong><br>
  <em>Write here • Read everywhere</em>
</p>

# loclass-starter

`loclass-starter` ist die LaTeX/PDF-Referenzintegration für Dokumente aus der **loclass document language (LDL)**.

Das Repository enthält keine eigene LDL-Implementierung. Parsing, Dokumentmodell, Paketplanung und backendneutrale Verarbeitung stammen aus den eigenständigen Projekten `loclass-ldl` und `loclass`.

---

## loclass-Ökosystem

| Projekt | Aufgabe |
| --- | --- |
| `loclass` | Backendneutraler Kern, Paketmodell und Renderer |
| `loclass-ldl` | LDL-Syntax, Manifest, Parser und Loader |
| `loclass-starter` | LaTeX-Klasse, Layout und vollständiger PDF-Build |
| `loclass-tlp` | Optionales externes Paket für TLP-Seitenmarkierungen |
| `loclass-branding` | Gemeinsame Farben, Wortmarke und Branding-Assets |
| `loclass-review` | Review-Hinweise für TODO, FIXME, QUESTION und NOTE |
| `loclass-versioning` | Versionshistorien aus strukturierten Quelldaten |
| `loclass-acronyms` | Gemeinsame Abkürzungsverzeichnisse |

---

## Architektur

Der produktive PDF-Pfad lautet:

```text
LDL-Datei
→ loclass-ldl lädt Manifest und Inhalt
→ loclass entdeckt und plant angeforderte Pakete
→ das LaTeX-Backend rendert Inhalt und Paketbeiträge
→ loclass-starter stellt Klasse, Theme und Layout
→ latexmk erzeugt das PDF
```

Der Starter besitzt keinen parallelen Parser, keinen eigenen Dokumentbaum und keinen zweiten Renderer.

---

## Voraussetzungen

Erforderlich sind:

- Python 3.14 oder neuer
- `uv`
- eine TeX-Distribution mit `latexmk` und pdfLaTeX
- die von der loclass-Klasse verwendeten LaTeX-Pakete

Im aktuellen Entwicklungsaufbau liegen die Repositories nebeneinander:

```text
loclass/
├── loclass-base/
├── loclass-ldl/
├── loclass-starter/
└── loclass-tlp/
```

Dabei gilt:

| Ebene | Name |
| --- | --- |
| Repository-Ordner des Kerns | `loclass-base` |
| Python-Distribution des Kerns | `loclass` |
| Python-Modul des Kerns | `loclass` |

Die lokalen Entwicklungsquellen sind in `pyproject.toml` über `tool.uv.sources` eingebunden.

---

## Installation

Grundsystem installieren:

```bash
uv sync
```

Das optionale TLP-Paket zusätzlich installieren:

```bash
uv sync --extra tlp
```

---

## Schnellstart

Tests ausführen:

```bash
uv run pytest
```

Ein LDL-Dokument bauen:

```bash
./loclass build examples/full_document.ldl
```

Alternativ direkt über den Python-Einstiegspunkt:

```bash
uv run loclass-pdf examples/full_document.ldl
```

Das Ergebnis liegt unter:

```text
build/full_document.pdf
```

PDF öffnen:

```bash
./loclass open examples/full_document.ldl
```

Build-Ausgaben entfernen:

```bash
./loclass clean
```

`ldl` bleibt als Alias für `build` verfügbar:

```bash
./loclass ldl examples/full_document.ldl
```

---

## LDL-Dokument

Eine Hauptdatei besitzt genau ein Manifest.

```ldl
---
title: Sicherheitsbericht
subtitle: Technische Dokumentation
author: Frank Sieger
company: Beispiel GmbH
customer: Beispielkunde
version: 1.0.0
date: 2026-07-12
---

chapter
  Einführung

Dies ist ein LDL-Dokument.

section
  Ausführung

Starte die Tests mit __cmd{uv run pytest}.
```

---

## Modulare Dokumente

Ein Dokument kann aus mehreren LDL-Dateien bestehen:

```text
examples/
├── full_document.ldl
└── content/
    └── 10_chapterone.ldl
```

Hauptdatei:

```ldl
---
title: Modulares Dokument
---

input
  content/10_chapterone.ldl
```

Eingebundene Datei:

```ldl
chapter
  Einführung

Dies ist ein Inhaltsmodul.
```

Dabei gelten folgende Regeln:

- Das Manifest steht ausschließlich in der Hauptdatei.
- Ein Dokument besitzt genau ein Manifest.
- Eingebundene Dateien enthalten nur Inhalt.
- Relative Pfade beziehen sich auf die jeweils einbindende Datei.
- Fehlende Dateien werden als Fehler gemeldet.
- Zirkuläre Einbindungen werden erkannt.

---

## Optionale Pakete

Pakete werden im Manifest angefordert und über Python Entry Points entdeckt.

Beispiel für `loclass-tlp`:

```ldl
---
title: Sicherheitsbericht
packages:
  loclass.tlp:
    label: amber+strict
---

chapter
  Einführung

Dieses Dokument trägt eine TLP-Seitenmarkierung.
```

Im Entwicklungsaufbau kann das enthaltene Beispiel so gebaut werden:

```bash
uv sync --extra tlp

./loclass build \
  ../loclass-tlp/examples/tlp-amber-strict.ldl
```

Dabei sind drei Namen bewusst voneinander getrennt:

| Ebene | Name |
| --- | --- |
| Manifest-Paket-ID | `loclass.tlp` |
| Python-Distribution | `loclass-tlp` |
| Python-Modul | `loclass_tlp` |

Der Starter enthält keinen TLP-spezifischen Code. Das Paket liefert backendneutrale Beiträge; der jeweilige Backend-Renderer setzt sie um.

---

## Optionale LaTeX-Erweiterungen

Für technische Sonderfälle dürfen backendgebundene LaTeX-Erweiterungen angelegt werden:

```text
project/
├── macros.tex
└── environments.tex
```

Beide Dateien und das gesamte Verzeichnis sind optional.

Die Ladefolge lautet:

```text
loclass-Klasse
→ Paketbeiträge
→ project/macros.tex
→ project/environments.tex
→ generierte Dokumentmetadaten
→ Dokumentinhalt
```

Es gibt keine manuell gepflegte `project/packages.tex`, keine `project/metadata.tex` und keine generierte `project/_inputs.tex`.

---

## Repository-Struktur

```text
.
├── assets/
├── core/
│   ├── commands/
│   ├── docs/
│   ├── examples/
│   ├── modules/
│   │   ├── components/
│   │   └── themes/
│   ├── templates/
│   ├── tests/
│   └── tools/
├── examples/
├── loclass
├── pyproject.toml
├── uv.lock
└── README.md
```

| Pfad | Aufgabe |
| --- | --- |
| `core/commands/` | Öffentliche LaTeX-Kommandos |
| `core/modules/` | Klasse, Theme, Komponenten und Seitenlayout |
| `core/templates/` | Dokumentvorlagen wie die Titelseite |
| `core/tools/ldl_pdf.py` | Vollständiger LDL-zu-PDF-Build |
| `core/tests/` | Integrationstests des Starters |
| `core/docs/` | Dokumentation und Spezifikationsmaterial |
| `core/examples/` | Kleine LDL-Beispiele |
| `examples/` | Vollständige Beispieldokumente |
| `loclass` | Lokaler Kommandozeilen-Wrapper |
| `build/` | Generierte Dateien; nicht versioniert |

---

## Tests und Qualitätsprüfungen

```bash
uv run ruff format --check core
uv run ruff check core
uv run pytest
```

Ein vollständiger PDF-Test:

```bash
rm -rf build

./loclass build examples/full_document.ldl

test -f build/full_document.pdf \
  && echo "OK: full_document.pdf erzeugt"
```

Ein vollständiger TLP-Test:

```bash
./loclass build \
  ../loclass-tlp/examples/tlp-amber-strict.ldl

test -f build/tlp-amber-strict.pdf \
  && echo "OK: TLP-PDF erzeugt"

pdftotext -layout \
  build/tlp-amber-strict.pdf - \
  | grep -n 'TLP:AMBER+STRICT'
```

Die vollständigen Parser-, Loader-, Backend- und Pakettests befinden sich in den jeweils zuständigen Repositories `loclass-ldl`, `loclass` und den Erweiterungspaketen.

---

## Designprinzipien

- Ein Dokument besitzt genau ein Manifest.
- Eingebundene LDL-Dateien sind reine Inhaltsmodule.
- Sprache, Dokumentmodell und Backends bleiben getrennt.
- Erweiterungen werden als eigenständige Pakete integriert.
- Paketkonfiguration bleibt im Manifest.
- Backendgebundene Escape-Hatches sind optional.
- Der Starter enthält nur die für LaTeX/PDF erforderliche Integration.
- Es gibt genau einen produktiven PDF-Buildpfad.
