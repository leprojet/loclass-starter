from .model import Code, Image, Table


IMAGE_BASE_PATH = "assets/images"


def _latex_escape(value: str) -> str:
    replacements = {
        "\\": r"\textbackslash{}",
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
    }

    for old, new in replacements.items():
        value = value.replace(old, new)

    return value


def _render_label(label: str | None) -> str:
    return _latex_escape(label or "")


def render_table_latex(table: Table) -> str:
    column_spec = " ".join(["L"] * len(table.header))

    header = " & ".join(
        rf"\loTableHeadCell{{{_latex_escape(cell)}}}" for cell in table.header
    )

    rows = [
        "    " + " & ".join(_latex_escape(cell) for cell in row) + r" \\"
        for row in table.rows
    ]

    lines = [
        rf"\begin{{lotable}}{{{_render_label(table.label)}}}{{{_latex_escape(table.caption)}}}{{{column_spec}}}",
        "    \\loTableHead{",
        f"        {header}",
        "    }",
        *rows,
        r"\end{lotable}",
    ]

    return "\n".join(lines)


def render_image_latex(image: Image) -> str:
    return "\n".join(
        [
            r"\begin{figure}[H]",
            r"    \centering",
            rf"    \includegraphics[width=\textwidth]{{{IMAGE_BASE_PATH}/{_latex_escape(image.file)}}}",
            rf"    \caption{{{_latex_escape(image.caption)}}}",
            rf"    \label{{{_render_label(image.label)}}}",
            r"\end{figure}",
        ]
    )


def render_code_latex(code: Code) -> str:
    options = [f"language={_latex_escape(code.language)}"]

    if code.caption:
        options.append(f"caption={{{_latex_escape(code.caption)}}}")

    if code.label:
        options.append(f"label={{{_render_label(code.label)}}}")

    body = "\n".join(code.body)

    return "\n".join(
        [
            rf"\begin{{locode}}[{', '.join(options)}]",
            body,
            r"\end{locode}",
        ]
    )
