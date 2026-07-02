from core.ldl.parser import parse_chapter


def test_parse_chapter():
    source = """
chapter
  Einführung
"""

    chapter = parse_chapter(source)

    assert chapter.title == "Einführung"
