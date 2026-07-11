from collections.abc import Callable
from typing import Any

from loclass_ldl.model import (
    Code,
    Heading,
    Image,
    List,
    Paragraph,
    Shell,
    Table,
)

from .renderer import (
    render_code_latex,
    render_heading_latex,
    render_image_latex,
    render_list_latex,
    render_paragraph_latex,
    render_shell_latex,
    render_table_latex,
)

Renderer = Callable[[Any], str]

RENDERERS: dict[type[Any], Renderer] = {
    Heading: render_heading_latex,
    Paragraph: render_paragraph_latex,
    Table: render_table_latex,
    Image: render_image_latex,
    Code: render_code_latex,
    List: render_list_latex,
    Shell: render_shell_latex,
}

__all__ = [
    "RENDERERS",
    "Renderer",
]
