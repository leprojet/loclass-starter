from .model import Code, Image, Table
from .parser import parse_code, parse_image, parse_table
from .renderer import (
    render_code_latex,
    render_image_latex,
    render_table_latex,
)

PARSERS = {
    "table": parse_table,
    "image": parse_image,
    "code": parse_code,
}

RENDERERS = {
    Table: render_table_latex,
    Image: render_image_latex,
    Code: render_code_latex,
}
