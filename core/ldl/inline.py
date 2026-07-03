from collections.abc import Callable

from .model import Bold, Text


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

    i = 0

    while i < len(text):
        if text[i] == "*":
            if buffer:
                tokens.append(Text("".join(buffer)))
                buffer = []

            end = text.find("*", i + 1)

            if end == -1:
                buffer.append(text[i])
                i += 1
                continue

            tokens.append(Bold(text[i + 1 : end]))
            i = end + 1
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


INLINE_TOKEN_RENDERERS: dict[type, Callable[[object], str]] = {
    Text: _render_text,
    Bold: _render_bold,
}


def render_inline(text: str) -> str:
    tokens = lex_inline(text)

    rendered: list[str] = []

    for token in tokens:
        renderer = INLINE_TOKEN_RENDERERS[type(token)]
        rendered.append(renderer(token))

    return "".join(rendered)
