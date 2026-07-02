from core.ldl.model import Chapter
from core.ldl.renderer import render_chapter_latex


def test_render_chapter():
    chapter = Chapter(title="Einführung")

    rendered = render_chapter_latex(chapter)

    assert rendered == r"\chapter{Einführung}"
