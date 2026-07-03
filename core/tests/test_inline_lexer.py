from core.ldl.inline import lex_inline
from core.ldl.model import Bold, Text


def test_lex_plain_text():
    assert lex_inline("Hello") == [
        Text("Hello"),
    ]


def test_lex_bold():
    assert lex_inline("Hello *World*!") == [
        Text("Hello "),
        Bold("World"),
        Text("!"),
    ]
