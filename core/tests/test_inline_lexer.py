from core.ldl.inline import lex_inline
from core.ldl.model import Bold, Italic, Text


def test_lex_plain_text():
    assert lex_inline("Hello") == [
        Text("Hello"),
    ]
    assert lex_inline("/italic/") == [
        Italic("italic"),
    ]


def test_lex_bold():
    assert lex_inline("Hello *World*!") == [
        Text("Hello "),
        Bold("World"),
        Text("!"),
    ]
