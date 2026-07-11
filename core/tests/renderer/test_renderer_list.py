from loclass_ldl.model import List
from loclass.backends.latex import render_list_latex


def test_render_unordered_list():
    result = render_list_latex(List(type="unordered", items=["Eins", "Zwei"]))

    assert (
        result
        == r"""\begin{itemize}
\item Eins
\item Zwei
\end{itemize}"""
    )


def test_render_ordered_list():
    result = render_list_latex(List(type="ordered", items=["Installation", "Test"]))

    assert (
        result
        == r"""\begin{enumerate}
\item Installation
\item Test
\end{enumerate}"""
    )
