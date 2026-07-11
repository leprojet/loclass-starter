from __future__ import annotations

import argparse
import shutil
import subprocess
from pathlib import Path

from core.backends.latex import latex_escape, render_document_latex
from loclass_ldl import Metadata, load_document


BUILD_DIR = Path("build")
LDL_BUILD_DIR = BUILD_DIR / "ldl"


def _metadata_command(command: str, value: str | None) -> str:
    if not value:
        return ""

    return rf"\{command}{{{latex_escape(value)}}}"


def render_metadata(metadata: Metadata) -> str:
    lines = [
        _metadata_command("Title", metadata.title),
        _metadata_command("Subtitle", metadata.subtitle),
        _metadata_command("author", metadata.author),
        _metadata_command("Company", metadata.company),
        _metadata_command("Customer", metadata.customer),
        _metadata_command("Version", metadata.version),
        _metadata_command("Date", metadata.date),
    ]

    return "\n".join(line for line in lines if line)


def render_wrapper(content_tex_path: Path, metadata: Metadata) -> str:
    content_input = content_tex_path.with_suffix("").name

    return rf"""\documentclass{{core/loclass}}


% Project overrides, if present.
\InputIfFileExists{{project/packages.tex}}{{}}{{}}
\InputIfFileExists{{project/macros.tex}}{{}}{{}}
\InputIfFileExists{{project/environments.tex}}{{}}{{}}

{render_metadata(metadata)}

\begin{{document}}

\input{{core/templates/titlepage}}

\tableofcontents

\input{{{content_input}}}

\end{{document}}
"""


def build_ldl_pdf(input_path: Path) -> Path:
    input_path = input_path.resolve()

    if not input_path.exists():
        raise FileNotFoundError(f"LDL file not found: {input_path}")

    if input_path.suffix != ".ldl":
        raise ValueError(f"Expected .ldl file, got: {input_path}")

    document = load_document(input_path)

    stem = input_path.stem

    LDL_BUILD_DIR.mkdir(parents=True, exist_ok=True)

    content_tex_path = LDL_BUILD_DIR / f"{stem}.tex"
    wrapper_tex_path = LDL_BUILD_DIR / f"{stem}-main.tex"
    internal_pdf_path = LDL_BUILD_DIR / f"{stem}-main.pdf"
    final_pdf_path = BUILD_DIR / f"{stem}.pdf"

    content_tex_path.write_text(
        render_document_latex(document),
        encoding="utf-8",
    )

    wrapper_tex_path.write_text(
        render_wrapper(content_tex_path, document.metadata),
        encoding="utf-8",
    )

    subprocess.run(
        [
            "latexmk",
            "-pdf",
            "-interaction=nonstopmode",
            "-halt-on-error",
            "-outdir=build/ldl",
            wrapper_tex_path.as_posix(),
        ],
        check=True,
    )

    if not internal_pdf_path.exists():
        raise RuntimeError(f"Expected PDF was not created: {internal_pdf_path}")

    shutil.copyfile(internal_pdf_path, final_pdf_path)

    return final_pdf_path


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="ldl_pdf",
        description="Render a complete LDL document to PDF.",
    )
    parser.add_argument("file", help="Path to a .ldl file")

    args = parser.parse_args()

    pdf_path = build_ldl_pdf(Path(args.file))

    print(f"PDF written: {pdf_path}")


if __name__ == "__main__":
    main()
