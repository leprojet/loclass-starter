from collections.abc import Callable

from .model import Bold, Italic, Text

INLINE_MARKERS = {
    "*": Bold,
    "/": Italic,
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


def lex_inline(text: str) -> list[object]:
    tokens: list[object] = []
    buffer: list[str] = []
    tokens: list[object] = []
    buffer: list[str] = []

    i = 0

    while i < len(text):
        marker = text[i]

        if marker in INLINE_MARKERS:
            if buffer:
                tokens.append(Text("".join(buffer)))
                buffer = []

            end = text.find(marker, i + 1)

            if end == -1:
                buffer.append(marker)
                i += 1
                continue

            content = text[i + 1 : end]

            token_class = INLINE_MARKERS[marker]
            tokens.append(token_class(content))

            i = end + 1
            continue

        buffer.append(marker)
        i += 1

    if buffer:
        tokens.append(Text("".join(buffer)))

    return tokens

    i = 0

    while i < len(text):
        marker = text[i]

        if marker in ("*", "/"):
            if buffer:
                tokens.append(Text("".join(buffer)))
                buffer = []

            end = text.find(marker, i + 1)

            if end == -1:
                buffer.append(marker)
                i += 1
                continue

            content = text[i + 1 : end]

            if marker == "*":
                tokens.append(Bold(content))
            elif marker == "/":
                tokens.append(Italic(content))

            i = end + 1
            continue

        buffer.append(marker)
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


INLINE_TOKEN_RENDERERS: dict[type, Callable[[object], str]] = {
    Text: _render_text,
    Bold: _render_bold,
    Italic: _render_italic,
}


def render_inline(text: str) -> str:
    tokens = lex_inline(text)

    rendered: list[str] = []

    for token in tokens:
        renderer = INLINE_TOKEN_RENDERERS[type(token)]
        rendered.append(renderer(token))

    return "".join(rendered)
