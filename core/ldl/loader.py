"""Compatibility imports for the extracted LDL loader.

New code should import directly from ``loclass_ldl``.
"""

from loclass_ldl.loader import LdlInputError, load_document

__all__ = [
    "LdlInputError",
    "load_document",
]
