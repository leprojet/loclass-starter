from core.ldl.model import Image
from core.ldl.renderer import render_image_latex


def test_render_image():
    image = Image(
        label="fig:logo",
        caption="Firmenlogo",
        file="logo.png",
    )

    rendered = render_image_latex(image)

    assert r"\begin{figure}[H]" in rendered
    assert r"\includegraphics[width=\textwidth]{assets/images/logo.png}" in rendered
    assert r"\caption{Firmenlogo}" in rendered
    assert r"\label{fig:logo}" in rendered
    assert r"\end{figure}" in rendered
