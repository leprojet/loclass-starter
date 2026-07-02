from core.ldl.model import Heading
from core.ldl.renderer import render_heading_latex


def test_render_chapter():
    assert (
        render_heading_latex(Heading("chapter", "Kapitel 1")) == r"\chapter{Kapitel 1}"
    )


def test_render_section():
    assert (
        render_heading_latex(Heading("section", "Motivation"))
        == r"\section{Motivation}"
    )


def test_render_subsection():
    assert (
        render_heading_latex(Heading("subsection", "Parser")) == r"\subsection{Parser}"
    )
