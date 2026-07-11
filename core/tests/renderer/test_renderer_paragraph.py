from loclass_ldl.model import Document, Paragraph
from core.backends.latex import render_document_latex


def test_render_paragraph():
    document = Document(
        elements=[
            Paragraph(text="Dies ist ein Absatz."),
        ],
    )

    assert render_document_latex(document) == "Dies ist ein Absatz."
