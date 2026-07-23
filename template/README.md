# loclass-Dokument

Die Dokumentquelle befindet sich in `main.ldl`.

## PDF erzeugen

    ./loclass.lua build

Das Ergebnis liegt anschließend unter `build/main.pdf`.

## ODT erzeugen

    ./loclass.lua odt

Das Ergebnis liegt anschließend unter `build/document.odt`.

## Voraussetzungen prüfen

    ./loclass.lua doctor

## Erzeugte Dateien entfernen

    ./loclass.lua clean

Die Dokumentmetadaten und aktivierten loclass-Packages werden bei
jedem Build direkt aus dem Manifest in `main.ldl` übernommen.
