"""Compatibility facade for LDL and the local LaTeX renderer.

The backend-neutral LDL implementation lives in ``loclass_ldl``.
This module preserves the existing imports used by loclass-starter.
"""

from loclass_ldl import (
    PARSERS,
    Code,
    Heading,
    Image,
    Input,
    List,
    Paragraph,
    Shell,
    Table,
    parse_code,
    parse_document,
    parse_heading,
    parse_image,
    parse_input,
    parse_list,
    parse_shell,
    parse_table,
)

from .registry import RENDERERS
from .renderer import (
    render_code_latex,
    render_document_latex,
    render_heading_latex,
    render_image_latex,
    render_list_latex,
    render_paragraph_latex,
    render_shell_latex,
    render_table_latex,
)

__all__ = [
    "Code",
    "Heading",
    "Image",
    "Input",
    "List",
    "PARSERS",
    "Paragraph",
    "RENDERERS",
    "Shell",
    "Table",
    "parse_code",
    "parse_document",
    "parse_heading",
    "parse_image",
    "parse_input",
    "parse_list",
    "parse_shell",
    "parse_table",
    "render_code_latex",
    "render_document_latex",
    "render_heading_latex",
    "render_image_latex",
    "render_list_latex",
    "render_paragraph_latex",
    "render_shell_latex",
    "render_table_latex",
]
