from core.ldl.model import Code, Document, List, Paragraph, Table
from core.ldl.parser import parse_document


def test_code_block_may_be_followed_by_paragraph():
    document = parse_document(
        """code
  params
    caption: Beispiel
    language: yaml
  body
    ---
    title: Beispiel
    ---

Dieser Satz ist wieder normaler Fließtext.
"""
    )

    assert document == Document(
        elements=[
            Code(
                label=None,
                caption="Beispiel",
                language="yaml",
                body=[
                    "title: Beispiel",
                ],
            ),
            Paragraph(text="Dieser Satz ist wieder normaler Fließtext."),
        ],
    )


def test_table_block_may_be_followed_by_paragraph():
    document = parse_document(
        """table
  params
    caption: Beispiel-Tabelle
  head
    Name | Wert
  body
    Alpha | 1
    Beta | 2

Dieser Satz steht nach der Tabelle.
"""
    )

    assert document == Document(
        elements=[
            Table(
                label=None,
                caption="Beispiel-Tabelle",
                header=["Name", "Wert"],
                rows=[
                    ["Alpha", "1"],
                    ["Beta", "2"],
                ],
            ),
            Paragraph(text="Dieser Satz steht nach der Tabelle."),
        ],
    )


def test_list_block_may_be_followed_by_paragraph():
    document = parse_document(
        """list
  params
    type: unordered
  body
    ---
    Eins
    Zwei
    ---

Dieser Satz steht nach der Liste.
"""
    )

    assert document == Document(
        elements=[
            List(
                type="unordered",
                items=[
                    "Eins",
                    "Zwei",
                ],
            ),
            Paragraph(text="Dieser Satz steht nach der Liste."),
        ],
    )
