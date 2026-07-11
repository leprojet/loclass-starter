from loclass_ldl.model import Code, Document, Heading, Metadata
from loclass.backends.latex import render_document_latex


document = Document(
    metadata=Metadata(),
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
