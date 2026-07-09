from core.ldl.model import Document, Input
from core.ldl.parser import parse_document


def test_parse_input():
    document = parse_document(
        """input
  content/intro.ldl
"""
    )

    assert document == Document(
        elements=[
            Input(path="content/intro.ldl"),
        ],
    )
