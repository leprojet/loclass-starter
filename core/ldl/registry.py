from .model import Code, Heading, Image, List, Table, Raw
from .parser import (
    parse_code,
    parse_heading,
    parse_image,
    parse_list,
    parse_shell,
    parse_table,
)

from .renderer import (
    render_code_latex,
    render_heading_latex,
    render_image_latex,
    render_list_latex,
    render_table_latex,
    render_raw_latex,
)

PARSERS = {
    "chapter": parse_heading,
    "section": parse_heading,
    "subsection": parse_heading,
    "table": parse_table,
    "image": parse_image,
    "list": parse_list,
    "code": parse_code,
    "shell": parse_shell,
}

RENDERERS = {
    Heading: render_heading_latex,
    Table: render_table_latex,
    Image: render_image_latex,
    List: render_list_latex,
    Code: render_code_latex,
    Raw: render_raw_latex,
}
