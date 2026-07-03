from core.ldl.inline import render_inline


def test_render_bold():
    assert render_inline("This is *bold* text.") == r"This is \textbf{bold} text."
