<p align="center">
  <img src="assets/images/loclass-readme-header.svg" alt="loclass – Write here • Read everywhere" width="100%">
</p>

# loclass Starter Paket

Ein praktisches Starter-Projekt für strukturierte technische Dokumentation mit **loclass** und **LDL**.

**Write here • Read everywhere**

`loclass-starter` zeigt, wie aus einer einfachen LDL-Quelle ein vollständiges PDF-Dokument gebaut wird. Das Projekt dient gleichzeitig als Referenzstruktur für spätere loclass-Dokumente.

---

## loclass Ökosystem

| Projekt              | Zweck                                              | Status    |
| -------------------- | -------------------------------------------------- | --------- |
| `loclass-starter`    | Beispiel- und Starterprojekt für loclass-Dokumente | aktiv     |
| `loclass-branding`   | Farben, Wortmarke, Logo und gemeinsame Assets      | aktiv     |
| `loclass-review`     | Review-Boxen für TODO, FIXME, QUESTION und NOTE    | nutzbar   |
| `loclass-versioning` | Versionshistorien aus YAML erzeugen                | nutzbar   |
| `loclass-acronyms`   | Gemeinsame Abkürzungsverzeichnisse für Dokumente   | nutzbar   |
| `loclass`            | Parser, Renderer und CLI für LDL                   | im Aufbau |

---

## Was ist loclass?

**loclass** ist ein schlankes Dokumentationssystem für technische Dokumente.

Die Idee:

- Inhalte werden in einer einfachen Textsyntax geschrieben.
- Layout, Metadaten und Rendering werden zentral gesteuert.
- Dokumente können später in verschiedene Zielformate gerendert werden.
- Der erste produktive Backend-Pfad ist aktuell LaTeX/PDF.

LDL steht dabei für **loclass document language**.

---

## Was kann dieses Starter-Paket aktuell?

Aktuell unterstützt das Projekt:

- Manifest mit Dokument-Metadaten
- Kapitel und Abschnitte
- Rohtext
- Tabellen
- Bilder
- Code-Blöcke
- Listen
- Shell-Blöcke
- Inline-Auszeichnungen wie `__cmd{...}`, `__keys{...}`, `__url{...}` und `__code{...}`
- modulare LDL-Dateien über `input`
- PDF-Erzeugung über LaTeX

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

Die eingebundene Datei kann zum Beispiel so aussehen:

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
- Eingebundene Dateien liefern nur Inhaltselemente.
- Das Manifest steht nur in der Hauptdatei.
- Ein Dokument hat genau ein Manifest.
- Zirkuläre Includes werden erkannt und abgebrochen.
- Fehlende Dateien werden mit einer verständlichen Fehlermeldung gemeldet.

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
│   ├── full_document.ldl
│   └── content/
├── project/
├── main.tex
├── latexmkrc
├── loclass
├── pyproject.toml
└── README.md
```

Wichtige Bereiche:

| Pfad             | Zweck                                            |
| ---------------- | ------------------------------------------------ |
| `core/ldl/`      | LDL-Model, Parser, Registry, Loader und Renderer |
| `core/tools/`    | Werkzeuge für den Build, z. B. PDF-Erzeugung     |
| `examples/`      | Beispielhafte LDL-Dokumente                      |
| `project/`       | Projektbezogene LaTeX-Anpassungen                |
| `content/`       | LaTeX-Content für klassische Dokumentstruktur    |
| `assets/images/` | Bilder und Branding-Assets                       |
| `main.tex`       | LaTeX-Einstiegspunkt                             |
| `loclass`        | lokaler Build-Wrapper                            |

---

## Build

Ein LDL-Dokument wird so gebaut:

```bash
./loclass ldl examples/full_document.ldl
```

Das erzeugt:

```text
build/full_document.pdf
```

Intern wird dabei das LDL-Dokument geladen, rekursiv aufgelöst, nach LaTeX gerendert und anschließend mit `latexmk` gebaut.

---

## Entwicklung

Tests ausführen:

```bash
uv run pytest
```

PDF direkt über das Tool bauen:

```bash
uv run python core/tools/ldl_pdf.py examples/full_document.ldl
```

Typischer Arbeitsablauf:

```bash
uv run pytest
./loclass ldl examples/full_document.ldl
```

---

## Roadmap

| Version | Ziel                                 |
| ------- | ------------------------------------ |
| `v0.1`  | `main.tex` bereinigt                 |
| `v0.2`  | erste modulare LaTeX-Struktur        |
| `v0.3`  | erste `loclass.tex`-Struktur         |
| `v0.4`  | `loclass.cls`                        |
| `v0.5`  | erstes Dokument komplett mit loclass |
| `v1.0`  | produktiv nutzbarer Dokumentenbau    |

---

## Designprinzipien

loclass folgt einigen einfachen Regeln:

- Dokumente sollen lesbar bleiben.
- Die Syntax soll kleiner sein als LaTeX.
- Struktur und Darstellung bleiben getrennt.
- Ein Dokument besitzt genau ein Manifest.
- Eingebundene Dateien sind Inhaltsmodule.
- Der LaTeX-Backendpfad bleibt transparent und nachvollziehbar.
- Erweiterungen sollen modular bleiben.

---

## Status

Dieses Repository ist ein Arbeitsstand.

Der aktuelle Schwerpunkt liegt auf:

- stabiler LDL-Grundsyntax
- modularem Dokumentbaum über `input`
- PDF-Erzeugung über LaTeX
- einheitlichem loclass-Branding
