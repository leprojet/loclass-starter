from core.ldl.inline import render_inline


def test_render_bold():
    assert render_inline("This is *bold* text.") == r"This is \textbf{bold} text."
    assert render_inline("/italic/") == r"\textit{italic}"


def test_render_underline():
    assert render_inline("+underline+") == r"\underline{underline}"
