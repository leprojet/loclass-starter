from loclass_ldl.model import Raw
from core.backends.latex import render_raw_latex


def test_render_raw_latex():
    raw = Raw(text=r"\LaTeX{} bleibt unverändert.")

    assert render_raw_latex(raw) == r"\LaTeX{} bleibt unverändert."


def test_render_raw_with_inline_directive():
    raw = Raw("Die Konfiguration liegt unter __path{/etc/nginx/nginx.conf}.")

    assert (
        render_raw_latex(raw)
        == r"Die Konfiguration liegt unter \locPath{/etc/nginx/nginx.conf}."
    )
