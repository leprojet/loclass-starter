"""Compatibility facade for the LaTeX block renderer.

The implementation lives in ``core.backends.latex.renderer``.
"""

from core.backends.latex.renderer import (
    IMAGE_BASE_PATH,
    render_code_latex,
    render_document_latex,
    render_heading_latex,
    render_image_latex,
    render_input_latex,
    render_list_latex,
    render_paragraph_latex,
    render_shell_latex,
    render_table_latex,
)

__all__ = [
    "IMAGE_BASE_PATH",
    "render_code_latex",
    "render_document_latex",
    "render_heading_latex",
    "render_image_latex",
    "render_input_latex",
    "render_list_latex",
    "render_paragraph_latex",
    "render_shell_latex",
    "render_table_latex",
]
