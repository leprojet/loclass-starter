"""Compatibility registry for LDL parsers and LaTeX renderers.

Parser registration belongs to ``loclass_ldl``.
The renderer registry remains local because it is LaTeX-specific.
"""

from collections.abc import Callable
from typing import Any

from loclass_ldl import PARSERS

from .model import (
    Code,
    Heading,
    Image,
    Input,
    List,
    Paragraph,
    Raw,
    Shell,
    Table,
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

Renderer = Callable[[Any], str]

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

__all__ = [
    "PARSERS",
    "RENDERERS",
]
