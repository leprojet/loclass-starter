"""Compatibility imports for the extracted LDL parser.

New code should import directly from ``loclass_ldl``.
"""

from loclass_ldl.parser import (
    parse_code,
    parse_document,
    parse_heading,
    parse_image,
    parse_input,
    parse_list,
    parse_shell,
    parse_table,
)

__all__ = [
    "parse_code",
    "parse_document",
    "parse_heading",
    "parse_image",
    "parse_input",
    "parse_list",
    "parse_shell",
    "parse_table",
]
