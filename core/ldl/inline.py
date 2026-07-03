import re
from collections.abc import Callable


def latex_escape(value: str) -> str:
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


def _render_bold(text: str) -> str:
    return re.sub(
        r"\*(.+?)\*",
        r"\\textbf{\1}",
        text,
    )


INLINE_RENDERERS: list[Callable[[str], str]] = [
    _render_bold,
]


def render_inline(text: str) -> str:
    text = latex_escape(text)

    for renderer in INLINE_RENDERERS:
        text = renderer(text)

    return text
