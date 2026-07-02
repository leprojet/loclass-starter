from .model import Table, Image


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


def render_table_latex(table: Table) -> str:
    column_spec = " ".join(["L"] * len(table.header))
    label = table.label or ""

    header = " & ".join(
        rf"\loTableHeadCell{{{_latex_escape(cell)}}}" for cell in table.header
    )

    rows = [
        "    " + " & ".join(_latex_escape(cell) for cell in row) + r" \\"
        for row in table.rows
    ]

    lines = [
        rf"\begin{{lotable}}{{{_latex_escape(label)}}}{{{_latex_escape(table.caption)}}}{{{column_spec}}}",
        "    \\loTableHead{",
        f"        {header}",
        "    }",
        *rows,
        r"\end{lotable}",
    ]

    return "\n".join(lines)


def render_image_latex(image: Image) -> str:
    label = image.label or ""

    return f"""\\begin{{figure}}[H]
    \\centering
    \\includegraphics[width=\\textwidth]{{assets/images/{image.file}}}
    \\caption{{{_latex_escape(image.caption)}}}
    \\label{{{_latex_escape(label)}}}
\\end{{figure}}"""
