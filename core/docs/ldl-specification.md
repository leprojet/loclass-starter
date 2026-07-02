# LDL Specification

LDL steht für **loclass Description Language**.

LDL beschreibt Dokumentinhalte backendagnostisch. Renderer erzeugen daraus konkrete Ausgaben, zum Beispiel LaTeX.

## Grundstruktur

Eine LDL-Direktive beginnt mit ihrem Namen.

```ldl
directive
  params
    key: value

  body
    ...

Einrückung erfolgt mit zwei Leerzeichen.

Unterstützte Direktiven

Aktuell unterstützt LDL:

- table
- image
- code

table
  params
    label: tab:ports
    caption: Netzwerkports

  head
    Dienst | Port | Protokoll

  body
    HTTP  | 80  | TCP
    HTTPS | 443 | TCP
    DNS   | 53  | UDP


| Parameter | Pflicht | Bedeutung            |
| --------- | ------: | -------------------- |
| `caption` |      ja | Tabellenbeschriftung |
| `label`   |    nein | Referenzlabel        |

Regeln
- head enthält genau eine Kopfzeile.
- Spalten werden mit | getrennt.
- Jede Zeile in body muss dieselbe Spaltenanzahl wie head haben.

image
  params
    label: fig:logo
    caption: Firmenlogo

  file
    LogObject_Logo.png
```

| Parameter | Pflicht | Bedeutung              |
| --------- | ------: | ---------------------- |
| `caption` |      ja | Abbildungsbeschriftung |
| `label`   |    nein | Referenzlabel          |

Regeln

- file enthält nur den Dateinamen.
- Der LaTeX-Renderer sucht Bilder unter assets/images/.

code
params
label: lst:hello
caption: Hello World
language: python

body
---
def hello():
print("Hello World")
---

| Parameter  | Pflicht | Bedeutung          |
| ---------- | ------: | ------------------ |
| `language` |      ja | Programmiersprache |
| `caption`  |    nein | Code-Beschriftung  |
| `label`    |    nein | Referenzlabel      |

Regeln

- Der Code steht im body zwischen --- und ---.
- Einrückungen bleiben erhalten.
- Leerzeilen bleiben erhalten.
- Der Inhalt des Codeblocks wird vom Parser nicht interpretiert.

| LDL     | LaTeX     |
| ------- | --------- |
| `table` | `lotable` |
| `image` | `figure`  |
| `code`  | `locode`  |

Danach:

```bash
git add docs/ldl-specification.md
git commit -m "Add initial LDL specification"
```
