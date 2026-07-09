from pathlib import Path

from .model import Document, Element, Input
from .parser import parse_document


class LdlInputError(ValueError):
    pass


def load_document(path: str | Path) -> Document:
    source_path = Path(path).resolve()
    return _load_document(source_path, stack=[])


def _load_document(path: Path, stack: list[Path]) -> Document:
    if path in stack:
        chain = " -> ".join(str(item) for item in [*stack, path])
        raise LdlInputError(f"Circular LDL input detected: {chain}")

    if not path.exists():
        raise LdlInputError(f"LDL input file not found: {path}")

    source = path.read_text(encoding="utf-8")
    document = parse_document(source)

    resolved_elements: list[Element] = []

    for element in document.elements:
        if isinstance(element, Input):
            child_path = (path.parent / element.path).resolve()
            child_document = _load_document(child_path, [*stack, path])
            resolved_elements.extend(child_document.elements)
        else:
            resolved_elements.append(element)

    return Document(
        metadata=document.metadata,
        elements=resolved_elements,
    )
