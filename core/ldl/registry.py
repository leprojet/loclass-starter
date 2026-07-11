"""Compatibility facade for LDL parsers and LaTeX renderers."""

from loclass_ldl import PARSERS

from core.backends.latex.registry import RENDERERS, Renderer

__all__ = [
    "PARSERS",
    "RENDERERS",
    "Renderer",
]
