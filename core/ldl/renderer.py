from .inline import latex_escape, render_inline_latex
from .model import Code, Heading, Image, List, Raw, Shell, Table


IMAGE_BASE_PATH = "assets/images"


def _render_label(label: str | None) -> str:
    return latex_escape(label or "")


def render_table_latex(table: Table) -> str:
    column_spec = " ".join(["L"] * len(table.header))

    header = " & ".join(
        rf"\loTableHeadCell{{{render_inline_latex(cell)}}}" for cell in table.header
    )

    rows = [
        "    " + " & ".join(render_inline_latex(cell) for cell in row) + r" \\"
        for row in table.rows
    ]

    lines = [
        rf"\begin{{lotable}}{{{_render_label(table.label)}}}{{{render_inline_latex(table.caption)}}}{{{column_spec}}}",
        r"    \loTableHead{",
        f"        {header}",
        r"    }",
        *rows,
        r"\end{lotable}",
    ]

    return "\n".join(lines)


def render_image_latex(image: Image) -> str:
    return "\n".join(
        [
            r"\begin{figure}[H]",
            r"    \centering",
            rf"    \includegraphics[width=\textwidth]{{{IMAGE_BASE_PATH}/{latex_escape(image.file)}}}",
            rf"    \caption{{{render_inline_latex(image.caption)}}}",
            rf"    \label{{{_render_label(image.label)}}}",
            r"\end{figure}",
        ]
    )


def render_code_latex(code: Code) -> str:
    options = [f"language={latex_escape(code.language)}"]

    if code.caption:
        options.append(f"caption={{{render_inline_latex(code.caption)}}}")

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


def render_heading_latex(heading: Heading) -> str:
    commands = {
        "chapter": "chapter",
        "section": "section",
        "subsection": "subsection",
    }

    command = commands[heading.level]

    return rf"\{command}{{{render_inline_latex(heading.title)}}}"


def render_document_latex(document: list[object]) -> str:
    from .registry import RENDERERS

    parts: list[str] = []

    for element in document:
        renderer = RENDERERS[type(element)]
        parts.append(renderer(element))

    return "\n".join(parts)


def render_raw_latex(raw: Raw) -> str:
    return raw.text


def render_list_latex(lst: List) -> str:
    environments = {
        "unordered": "itemize",
        "ordered": "enumerate",
    }

    environment = environments[lst.type]

    lines = [
        rf"\begin{{{environment}}}",
        *[rf"\item {render_inline_latex(item)}" for item in lst.items],
        rf"\end{{{environment}}}",
    ]

    return "\n".join(lines)


def render_shell_latex(shell: Shell) -> str:
    options = [f"style={latex_escape(shell.style)}"]

    if shell.title:
        options.append(f"title={{{render_inline_latex(shell.title)}}}")

    return "\n".join(
        [
            rf"\begin{{loshell}}[{','.join(options)}]",
            *shell.body,
            r"\end{loshell}",
        ]
    )
