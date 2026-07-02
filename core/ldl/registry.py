# core/ldl/registry.py
from .model import Chapter, Code, Image, Table
from .parser import parse_chapter, parse_code, parse_image, parse_table
from .renderer import (
    render_chapter_latex,
    render_code_latex,
    render_image_latex,
    render_table_latex,
)

PARSERS = {
    "chapter": parse_chapter,
    "table": parse_table,
    "image": parse_image,
    "code": parse_code,
}

RENDERERS = {
    Chapter: render_chapter_latex,
    Table: render_table_latex,
    Image: render_image_latex,
    Code: render_code_latex,
}
