from core.ldl.model import Heading, Raw
from core.ldl.parser import parse_document


def test_parse_document_with_raw_text():
    source = r"""chapter
  Einführung

Das ist normaler LaTeX-Text.

\begin{itemize}
\item Eins
\item Zwei
\end{itemize}

section
  Danach
"""

    document = parse_document(source)

    assert document == [
        Heading(level="chapter", title="Einführung"),
        Raw(
            text=r"""Das ist normaler LaTeX-Text.

\begin{itemize}
\item Eins
\item Zwei
\end{itemize}"""
        ),
        Heading(level="section", title="Danach"),
    ]
