from loclass_ldl.model import Table
from loclass.backends.latex import render_table_latex


def test_render_table_latex():
    table = Table(
        label="tab:ports",
        caption="Netzwerkports",
        header=["Dienst", "Port", "Protokoll"],
        rows=[
            ["HTTP", "80", "TCP"],
            ["HTTPS", "443", "TCP"],
            ["DNS", "53", "UDP"],
        ],
    )

    rendered = render_table_latex(table)

    assert r"\begin{lotable}{tab:ports}{Netzwerkports}{L L L}" in rendered
    assert r"\loTableHeadCell{Dienst}" in rendered
    assert r"\loTableHeadCell{Port}" in rendered
    assert r"\loTableHeadCell{Protokoll}" in rendered
    assert r"HTTP & 80 & TCP \\" in rendered
    assert r"HTTPS & 443 & TCP \\" in rendered
    assert r"DNS & 53 & UDP \\" in rendered
    assert r"\end{lotable}" in rendered


def test_render_table_latex_escapes_special_characters():
    table = Table(
        label="tab:test",
        caption="A&B_%",
        header=["Key", "Value"],
        rows=[["path_to_file", "A&B"]],
    )

    rendered = render_table_latex(table)

    assert r"A\&B\_\%" in rendered
    assert r"path\_to\_file" in rendered
    assert r"A\&B" in rendered
