from collections.abc import Callable
from typing import Any

from .model import (
    Code,
    Element,
    Heading,
    Image,
    Input,
    List,
    Paragraph,
    Raw,
    Shell,
    Table,
)

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
    render_input_latex,
    render_list_latex,
    render_paragraph_latex,
    render_raw_latex,
    render_shell_latex,
    render_table_latex,
)

Parser = Callable[[str], Element]
Renderer = Callable[[Any], str]

PARSERS: dict[str, Parser] = {
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

RENDERERS: dict[type[Any], Renderer] = {
    Heading: render_heading_latex,
    Paragraph: render_paragraph_latex,
    Table: render_table_latex,
    Image: render_image_latex,
    Input: render_input_latex,
    Code: render_code_latex,
    List: render_list_latex,
    Shell: render_shell_latex,
    Raw: render_raw_latex,
}
