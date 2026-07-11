"""Compatibility import for the extracted LDL formatter.

New code should import directly from ``loclass_ldl``.
"""

from loclass_ldl.formatter import format_source

__all__ = [
    "format_source",
]
