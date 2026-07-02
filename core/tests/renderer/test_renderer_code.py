from core.ldl.model import Code
from core.ldl.renderer import render_code_latex


def test_render_code():
    code = Code(
        label="lst:hello",
        caption="Hello World",
        language="python",
        body=[
            "def hello():",
            'print("Hello World")',
        ],
    )

    rendered = render_code_latex(code)

    assert r"\begin{locode}" in rendered
    assert "language=python" in rendered
    assert "caption={Hello World}" in rendered
    assert "label={lst:hello}" in rendered
    assert "def hello():" in rendered
    assert 'print("Hello World")' in rendered
    assert r"\end{locode}" in rendered
