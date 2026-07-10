# loclass Architekturentscheidungen

Stand: 2026-07-10

Diese Datei sammelt zentrale Architekturentscheidungen im loclass-Umfeld.

Ziel ist nicht, jede Kleinigkeit zu dokumentieren, sondern Entscheidungen festzuhalten, die später sonst erneut diskutiert würden.

---

## 1. Ein Dokument hat genau ein Manifest

### Entscheidung

Ein LDL-Dokument besitzt genau ein Manifest.

Das Manifest steht ausschließlich in der Hauptdatei.

Eingebundene LDL-Dateien enthalten nur Inhalt.

### Grund

Mehrere Manifeste in eingebundenen Dateien würden das Dokumentmodell unnötig kompliziert machen.

Unklar wäre insbesondere:

- welches Manifest Vorrang hat
- ob Metadaten gemerged werden
- wie Konflikte behandelt werden
- ob eingebundene Dateien eigenständige Dokumente oder Inhaltsmodule sind

Für loclass ist die einfachere Regel besser:

```text
Hauptdatei = Dokument
eingebundene Dateien = Inhalt
```

### Konsequenz

`input` löst nur Inhaltsmodule auf.

Metadaten werden ausschließlich aus der Hauptdatei gelesen.

Fehlende Dateien und zirkuläre Includes werden erkannt und verständlich gemeldet.

---

## 2. LDL bleibt einfacher als LaTeX

### Entscheidung

LDL soll eine einfache, lesbare Dokumentensprache bleiben.

LDL ersetzt LaTeX nicht vollständig, sondern kapselt typische technische Dokumentationsstrukturen.

### Grund

Der Zweck von loclass ist nicht, eine zweite Programmiersprache zu bauen.

LDL soll technische Dokumente einfacher wartbar machen:

- weniger LaTeX-Syntax im Inhalt
- klare Dokumentstruktur
- einfache Module
- verständliche Inline-Auszeichnungen
- spätere alternative Ausgabeformate möglich

### Konsequenz

LDL bekommt nur Konstrukte, die dokumentarisch sinnvoll sind.

Komplexe Gestaltung bleibt Aufgabe des jeweiligen Backends, zunächst LaTeX.

---

## 3. Der erste produktive Backendpfad ist LaTeX/PDF

### Entscheidung

Der erste stabile Ausgabepfad ist LaTeX/PDF.

Andere Ausgabeformate wie HTML, DOCX oder ODT bleiben perspektivisch möglich, sind aber nicht der aktuelle Fokus.

### Grund

LaTeX/PDF ist für technische Dokumentation unmittelbar nutzbar und passt gut zu den bisherigen Anforderungen.

PDF-Erzeugung ist außerdem ein guter Prüfstein für:

- Layout
- Inhaltsstruktur
- Tabellen
- Bilder
- Codeblöcke
- Inhaltsmodule

### Konsequenz

Der LaTeX-Renderer darf zunächst führend sein.

Das Modell soll trotzdem nicht unnötig LaTeX-spezifisch werden.

---

## 4. `loclass-starter` ist Integrationspunkt und Arbeitsrepository

### Entscheidung

`loclass-starter` ist aktuell kein reines Endanwender-Template, sondern der praktische Integrationspunkt für LDL, LaTeX-Struktur und PDF-Build.

### Grund

Das Projekt enthält derzeit bewusst mehrere Dinge gemeinsam:

- LaTeX-Projektstruktur
- LDL-Prototyp
- Parser
- Model
- Registry
- Loader
- Renderer
- PDF-Build-Werkzeug
- Tests
- Beispieldokumente

Das ist für die aktuelle Entwicklungsphase sinnvoll, weil Änderungen sofort praktisch geprüft werden können.

### Konsequenz

Spätere Auslagerungen bleiben möglich.

Aktuell zählt praktische Nutzbarkeit mehr als perfekte Pakettrennung.

---

## 5. Das loclass-Ökosystem wird in kleine Pakete getrennt

### Entscheidung

Wiederverwendbare Funktionen werden in eigene kleine Projekte ausgelagert, wenn sie unabhängig nützlich sind.

Beispiele:

- `loclass-branding`
- `loclass-review`
- `loclass-versioning`
- `loclass-acronyms`

### Grund

Nicht alles gehört in den Kern.

Kleine Pakete sind leichter zu verstehen, zu testen und wiederzuverwenden.

Außerdem kann jedes Paket für sich stabil werden, ohne den Kern unnötig aufzublähen.

### Konsequenz

`loclass` bleibt konzeptionell schlank.

Spezialfunktionen dürfen eigene Repositories oder Pakete bekommen.

---

## 6. `pyproject.toml` ist der Point of Truth für Projektkonfiguration

### Entscheidung

Projektspezifische Entwicklungsinformationen werden in `pyproject.toml` abgelegt, soweit das Projekt Python oder Python-nahe Werkzeuge verwendet.

Beispiel:

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

### Grund

Das Entwicklungs-Script soll generisch bleiben.

Projektwissen gehört nicht hart codiert in Shell-Scripte.

### Konsequenz

Das `dev`-Script kann unverändert in andere Repositories kopiert werden.

Projektabweichungen werden deklarativ in `pyproject.toml` beschrieben.

---

## 7. Ein einheitliches `./dev`-Script erleichtert Entwicklung

### Entscheidung

loclass-nahe Projekte verwenden nach Möglichkeit ein einheitliches `./dev`-Script.

Standardbefehle:

```bash
./dev doctor
./dev test
./dev lint
./dev typecheck
./dev build
./dev release-check
```

### Grund

Alle Repositories sollen sich gleich bedienen lassen.

Man soll nicht jedes Mal überlegen müssen, ob ein Projekt über `pytest`, `latexmk`, `ruff`, `mypy`, `uv run` oder projektspezifische Kommandos geprüft wird.

### Konsequenz

Neue Projekte sollten möglichst früh ein `dev`-Script erhalten.

`./dev release-check` ist der bevorzugte lokale Komplettcheck vor einem Commit oder Release.

---

## 8. README-Dateien folgen einer gemeinsamen Struktur

### Entscheidung

loclass-nahe Repositories sollen einen ähnlichen README-Aufbau verwenden.

Typische Struktur:

```text
Brand-Kopf
Kurzbeschreibung
loclass-Ökosystem
Zweck
Schnellstart
Verwendung
Projektstruktur
Entwicklung
Roadmap
Designprinzipien
```

### Grund

Einheitliche README-Dateien erhöhen Wiedererkennung und Orientierung.

Wer ein loclass-Repository kennt, soll sich im nächsten schnell zurechtfinden.

### Konsequenz

Die loclass-Ökosystem-Tabelle darf bewusst wiederholt werden.

Der Entwicklungsabschnitt dokumentiert den Standardweg über `./dev`.

---

## 9. Templates werden zunächst als eine zentrale Datei gepflegt

### Entscheidung

Vorlagen werden zunächst in einer einzigen Datei gesammelt:

```text
templates/loclass-template-pack.md
```

### Grund

Viele kleine Template-Dateien erzeugen in der frühen Phase unnötige Unordnung.

Eine zentrale Datei ist leichter zu lesen, zu reviewen und zu pflegen.

### Konsequenz

Aus dem Template Pack können später echte Generatoren oder Skeleton-Verzeichnisse abgeleitet werden.

Aktuell bleibt es bewusst eine Sammlung zum Kopieren.

---

## 10. Branding ist Teil der Wiedererkennbarkeit

### Entscheidung

loclass-nahe Projekte sollen gemeinsame Branding-Elemente verwenden.

Dazu gehören insbesondere:

- Banner
- Wortmarke
- Slogan
- Farben
- Ökosystem-Tabelle

### Grund

loclass soll als zusammengehöriges Ökosystem erkennbar sein.

Ein einheitlicher Kopf in README, Website und Dokumentation hilft bei Orientierung und Wiedererkennung.

### Konsequenz

Branding-Assets werden zentral in `loclass-branding` gepflegt.

Andere Repositories verwenden diese Assets, duplizieren aber nicht unnötig deren Quellen.

---

## 11. Entscheidungen bleiben pragmatisch

### Entscheidung

Diese Datei ersetzt kein großes Architekturhandbuch.

Sie hält nur Entscheidungen fest, die für die weitere Entwicklung relevant sind.

### Grund

Zu viel Dokumentation wird selbst zur Last.

Zu wenig Dokumentation führt dazu, dass bereits getroffene Entscheidungen erneut diskutiert werden.

### Konsequenz

Neue Einträge werden ergänzt, wenn eine Entscheidung längerfristige Wirkung hat.

Kleine Tagesentscheidungen gehören nicht hierher.
