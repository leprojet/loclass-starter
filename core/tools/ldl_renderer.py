from __future__ import annotations

import argparse
from pathlib import Path

from core.ldl import parse_table, render_table_latex


def render_ldl(source: str) -> str:
    stripped = source.lstrip()

    if stripped.startswith("table"):
        table = parse_table(source)
        return render_table_latex(table)

    raise ValueError("Unsupported LDL block. Currently supported: table")


def render_file(input_path: Path, output_path: Path | None = None) -> str:
    source = input_path.read_text(encoding="utf-8")
    rendered = render_ldl(source)

    if output_path is not None:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(rendered + "\n", encoding="utf-8")

    return rendered


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="ldl-render",
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
