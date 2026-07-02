from core.ldl.model import Code, Heading
from core.ldl.renderer import render_document_latex


def test_render_document():
    document = [
        Heading(level="chapter", title="Einführung"),
        Heading(level="section", title="Beispiel"),
        Code(
            label=None,
            caption="Hello",
            language="python",
            body=['print("Hallo")'],
        ),
    ]

    rendered = render_document_latex(document)

    expected = r"""\chapter{Einführung}
\section{Beispiel}
\begin{locode}[language=python, caption={Hello}]
print("Hallo")
\end{locode}"""

    assert rendered == expected
