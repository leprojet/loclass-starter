"""LaTeX rendering for LDL inline elements.

Inline lexing belongs to ``loclass_ldl``. The rendering functions remain
local because they produce LaTeX-specific output.
"""

from collections.abc import Callable

from loclass_ldl import lex_inline
from loclass_ldl.model import (
    Bold,
    Cmd,
    InlineCode,
    Italic,
    Keys,
    Path,
    Strike,
    Text,
    Underline,
    Url,
)


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


def _render_text(token: Text) -> str:
    return latex_escape(token.text)


def _render_bold(token: Bold) -> str:
    return rf"\textbf{{{latex_escape(token.text)}}}"


def _render_italic(token: Italic) -> str:
    return rf"\textit{{{latex_escape(token.text)}}}"


def _render_underline(token: Underline) -> str:
    return rf"\underline{{{latex_escape(token.text)}}}"


def _render_strike(token: Strike) -> str:
    return rf"\sout{{{latex_escape(token.text)}}}"


def _render_path(token: Path) -> str:
    return rf"\locPath{{{latex_escape(token.text)}}}"


def _render_cmd(token: Cmd) -> str:
    return rf"\locCmd{{{latex_escape(token.text)}}}"


def _render_keys(token: Keys) -> str:
    return rf"\locKeys{{{latex_escape(token.text)}}}"


def _render_url(token: Url) -> str:
    return rf"\locUrl{{{latex_escape(token.text)}}}"


def _render_inline_code(token: InlineCode) -> str:
    return rf"\locCode{{{latex_escape(token.text)}}}"


INLINE_TOKEN_RENDERERS: dict[type, Callable[..., str]] = {
    Text: _render_text,
    Bold: _render_bold,
    Italic: _render_italic,
    Underline: _render_underline,
    Strike: _render_strike,
    Path: _render_path,
    Cmd: _render_cmd,
    Keys: _render_keys,
    Url: _render_url,
    InlineCode: _render_inline_code,
}


def render_inline(text: str) -> str:
    rendered: list[str] = []

    for token in lex_inline(text):
        renderer = INLINE_TOKEN_RENDERERS[type(token)]
        rendered.append(renderer(token))

    return "".join(rendered)


__all__ = [
    "INLINE_TOKEN_RENDERERS",
    "latex_escape",
    "lex_inline",
    "render_inline",
]
