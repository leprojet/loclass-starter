from collections.abc import Callable

from .model import Bold, Italic, Strike, Text, Underline


INLINE_MARKERS = {
    "--": Strike,
    "*": Bold,
    "/": Italic,
    "+": Underline,
}


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


def _find_marker_at(text: str, position: int) -> str | None:
    for marker in INLINE_MARKERS:
        if text.startswith(marker, position):
            return marker

    return None


def lex_inline(text: str) -> list[object]:
    tokens: list[object] = []
    buffer: list[str] = []

    i = 0

    while i < len(text):
        marker = _find_marker_at(text, i)

        if marker is not None:
            if buffer:
                tokens.append(Text("".join(buffer)))
                buffer = []

            end = text.find(marker, i + len(marker))

            if end == -1:
                buffer.append(marker)
                i += len(marker)
                continue

            content = text[i + len(marker) : end]
            token_class = INLINE_MARKERS[marker]
            tokens.append(token_class(content))

            i = end + len(marker)
            continue

        buffer.append(text[i])
        i += 1

    if buffer:
        tokens.append(Text("".join(buffer)))

    return tokens


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


INLINE_TOKEN_RENDERERS: dict[type, Callable[[object], str]] = {
    Text: _render_text,
    Bold: _render_bold,
    Italic: _render_italic,
    Underline: _render_underline,
    Strike: _render_strike,
}


def render_inline(text: str) -> str:
    tokens = lex_inline(text)

    rendered: list[str] = []

    for token in tokens:
        renderer = INLINE_TOKEN_RENDERERS[type(token)]
        rendered.append(renderer(token))

    return "".join(rendered)
