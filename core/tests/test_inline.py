from core.backends.latex import render_inline
from loclass_ldl import lex_inline
from loclass_ldl.model import Cmd, InlineCode, Keys, Path, Text, Url


def test_parse_path_inline_directive():
    result = lex_inline("Datei: __path{/etc/nginx/nginx.conf}")

    assert result == [
        Text("Datei: "),
        Path("/etc/nginx/nginx.conf"),
    ]


def test_render_path_inline_directive():
    result = render_inline("Datei: __path{/etc/nginx/nginx.conf}")

    assert result == r"Datei: \locPath{/etc/nginx/nginx.conf}"


def test_parse_cmd_inline_directive():
    result = lex_inline("Ausführen: __cmd{uv run pytest}")

    assert result == [
        Text("Ausführen: "),
        Cmd("uv run pytest"),
    ]


def test_render_cmd_inline_directive():
    result = render_inline("Ausführen: __cmd{uv run pytest}")

    assert result == r"Ausführen: \locCmd{uv run pytest}"


def test_parse_keys_inline_directive():
    result = lex_inline("Drücke __keys{Ctrl+Alt+T}")

    assert result == [
        Text("Drücke "),
        Keys("Ctrl+Alt+T"),
    ]


def test_render_keys_inline_directive():
    result = render_inline("Drücke __keys{Ctrl+Alt+T}")

    assert result == r"Drücke \locKeys{Ctrl+Alt+T}"


def test_parse_url_inline_directive():
    result = lex_inline("Siehe __url{https://example.org/docs}")

    assert result == [
        Text("Siehe "),
        Url("https://example.org/docs"),
    ]


def test_render_url_inline_directive():
    result = render_inline("Siehe __url{https://example.org/docs}")

    assert result == r"Siehe \locUrl{https://example.org/docs}"


def test_parse_code_inline_directive():
    result = lex_inline("Wert: __code{None}")

    assert result == [
        Text("Wert: "),
        InlineCode("None"),
    ]


def test_render_code_inline_directive():
    result = render_inline("Wert: __code{None}")

    assert result == r"Wert: \locCode{None}"
