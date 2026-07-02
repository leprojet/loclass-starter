from __future__ import annotations

import argparse
from pathlib import Path

from core.ldl import (
    parse_image,
    parse_table,
    render_image_latex,
    render_table_latex,
)


def render_ldl(source: str) -> str:
    stripped = source.lstrip()

    if stripped.startswith("table"):
        return render_table_latex(parse_table(source))

    if stripped.startswith("image"):
        return render_image_latex(parse_image(source))

    raise ValueError("Unsupported LDL block. Currently supported: table, image")


def render_file(input_path: Path, output_path: Path | None = None) -> str:
    source = input_path.read_text(encoding="utf-8")
    rendered = render_ldl(source)

    if output_path is not None:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(rendered + "\n", encoding="utf-8")

    return rendered


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="ldl-renderer",
        description="Render LDL blocks to LaTeX.",
    )

    parser.add_argument("input", type=Path)
    parser.add_argument("-o", "--output", type=Path)

    args = parser.parse_args()

    rendered = render_file(args.input, args.output)

    if args.output is None:
        print(rendered)


if __name__ == "__main__":
    main()
