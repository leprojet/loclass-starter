from core.ldl.inline import render_inline

from core.ldl.inline import lex_inline
from core.ldl.model import Path, Text


def test_parse_path_inline_directive():
    result = lex_inline("Datei: __path{/etc/nginx/nginx.conf}")

    assert result == [
        Text("Datei: "),
        Path("/etc/nginx/nginx.conf"),
    ]


def test_render_path_inline_directive():
    result = render_inline("Datei: __path{/etc/nginx/nginx.conf}")

    assert result == r"Datei: \locPath{/etc/nginx/nginx.conf}"


def test_render_bold():
    assert render_inline("This is *bold* text.") == r"This is \textbf{bold} text."
    assert render_inline("/italic/") == r"\textit{italic}"


def test_render_underline():
    assert render_inline("+underline+") == r"\underline{underline}"


def test_render_strike():
    assert render_inline("--strike--") == r"\sout{strike}"
