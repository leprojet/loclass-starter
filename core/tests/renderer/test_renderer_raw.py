from core.ldl.model import Raw
from core.ldl.renderer import render_raw_latex


def test_render_raw_latex():
    raw = Raw(text=r"\LaTeX{} bleibt unverändert.")

    assert render_raw_latex(raw) == r"\LaTeX{} bleibt unverändert."
