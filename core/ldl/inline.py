"""Compatibility facade for the LaTeX inline renderer.

Backend-neutral inline lexing lives in ``loclass_ldl``.
LaTeX-specific rendering lives in ``core.backends.latex.inline``.
"""

from core.backends.latex.inline import (
    INLINE_TOKEN_RENDERERS,
    latex_escape,
    lex_inline,
    render_inline,
)

__all__ = [
    "INLINE_TOKEN_RENDERERS",
    "latex_escape",
    "lex_inline",
    "render_inline",
]
