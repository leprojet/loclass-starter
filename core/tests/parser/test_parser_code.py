import pytest

from core.ldl.parser import parse_code


def test_parse_code():
    source = """
code
  params
    label: lst:hello
    caption: Hello World
    language: python

  body
    def hello():
        print("Hello World")
"""

    code = parse_code(source)

    assert code.label == "lst:hello"
    assert code.caption == "Hello World"
    assert code.language == "python"
    assert code.body == [
        "def hello():",
        'print("Hello World")',
    ]


def test_code_requires_language():
    source = """
code
  params
    caption: Hello World

  body
    print("Hello")
"""

    with pytest.raises(ValueError):
        parse_code(source)


def test_code_requires_body():
    source = """
code
  params
    language: python
"""

    with pytest.raises(ValueError):
        parse_code(source)
