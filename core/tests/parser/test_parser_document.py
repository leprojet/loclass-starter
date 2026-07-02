from core.ldl.parser import parse_document
from core.ldl.model import Heading, Code


def test_parse_document_with_multiple_directives():
    source = """
chapter
  Einführung

section
  Beispiel

code
  params
    language: python
    caption: Hello

  body
    ---
    print("Hallo")
    ---
"""

    document = parse_document(source)

    assert document == [
        Heading(level="chapter", title="Einführung"),
        Heading(level="section", title="Beispiel"),
        Code(
            label=None,
            caption="Hello",
            language="python",
            body=['print("Hallo")'],
        ),
    ]
