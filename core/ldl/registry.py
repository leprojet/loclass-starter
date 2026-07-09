from .model import Code, Heading, Image, List, Raw, Shell, Table
from .parser import (
    parse_code,
    parse_heading,
    parse_image,
    parse_input,
    parse_list,
    parse_shell,
    parse_table,
)
from .renderer import (
    render_code_latex,
    render_heading_latex,
    render_image_latex,
    render_list_latex,
    render_raw_latex,
    render_shell_latex,
    render_table_latex,
)

PARSERS = {
    "chapter": parse_heading,
    "section": parse_heading,
    "subsection": parse_heading,
    "table": parse_table,
    "image": parse_image,
    "input": parse_input,
    "code": parse_code,
    "list": parse_list,
    "shell": parse_shell,
}

RENDERERS = {
    Heading: render_heading_latex,
    Table: render_table_latex,
    Image: render_image_latex,
    Code: render_code_latex,
    List: render_list_latex,
    Shell: render_shell_latex,
    Raw: render_raw_latex,
}
