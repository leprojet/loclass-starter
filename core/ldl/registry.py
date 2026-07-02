# core/ldl/registry.py
from .model import Code, Heading, Image, Table, Raw
from .parser import parse_code, parse_heading, parse_image, parse_table
from .renderer import (
    render_code_latex,
    render_heading_latex,
    render_image_latex,
    render_table_latex,
    render_raw_latex,
)

PARSERS = {
    "chapter": parse_heading,
    "section": parse_heading,
    "subsection": parse_heading,
    "table": parse_table,
    "image": parse_image,
    "code": parse_code,
}

RENDERERS = {
    Heading: render_heading_latex,
    Table: render_table_latex,
    Image: render_image_latex,
    Code: render_code_latex,
    Raw: render_raw_latex,
}
