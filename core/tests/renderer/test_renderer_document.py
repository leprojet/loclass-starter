from core.ldl.model import Code, Document, Heading
from core.ldl.renderer import render_document_latex


from core.ldl.model import Code, Document, Heading

document = Document(
    metadata={},
    elements=[
        Heading(level="chapter", title="Einführung"),
        Heading(level="section", title="Beispiel"),
        Code(
            label=None,
            caption="Hello",
            language="python",
            body=['print("Hallo")'],
        ),
    ],
)
rendered = render_document_latex(document)

expected = r"""\chapter{Einführung}
\section{Beispiel}
\begin{locode}[language=python, caption={Hello}]
print("Hallo")
\end{locode}"""

assert rendered == expected
