from .model import Code, Heading, Image, Table


def _normalize_lines(source: str) -> list[str]:
    return [line.rstrip() for line in source.splitlines() if line.strip()]


def _indent(line: str) -> int:
    return len(line) - len(line.lstrip(" "))


def _split_cells(line: str) -> list[str]:
    return [cell.strip() for cell in line.split("|")]


def _parse_param_line(line: str) -> tuple[str, str]:
    stripped = line.strip()

    if ":" not in stripped:
        raise ValueError(f"Invalid parameter line: {line}")

    key, value = stripped.split(":", 1)
    return key.strip(), value.strip()


def _parse_common_params(params: dict[str, str]) -> tuple[str | None, str | None]:
    label = params.get("label") or None
    caption = params.get("caption") or None
    return label, caption


def _parse_fenced_body(lines: list[str]) -> list[str]:
    if not lines or lines[0].strip() != "---":
        raise ValueError("Body block must start with '---'.")

    body: list[str] = []

    for line in lines[1:]:
        if line.strip() == "---":
            return body

        if line.startswith("    "):
            body.append(line[4:])
        else:
            body.append(line)

    raise ValueError("Body block must end with '---'.")


def parse_table(source: str) -> Table:
    lines = _normalize_lines(source)

    if not lines or lines[0].strip() != "table":
        raise ValueError("LDL table block must start with 'table'.")

    params: dict[str, str] = {}
    header: list[str] | None = None
    rows: list[list[str]] = []

    section: str | None = None

    for line in lines[1:]:
        stripped = line.strip()
        indent = _indent(line)

        if indent == 2 and stripped in {"params", "head", "body"}:
            section = stripped
            continue

        if section == "params":
            key, value = _parse_param_line(line)

            if key not in {"label", "caption"}:
                raise ValueError(f"Unknown table parameter: {key}")

            params[key] = value

        elif section == "head":
            header = _split_cells(stripped)

        elif section == "body":
            rows.append(_split_cells(stripped))

        else:
            raise ValueError(f"Line outside known table section: {line}")

    label, caption = _parse_common_params(params)

    if not caption:
        raise ValueError("Table requires a caption.")

    if not header:
        raise ValueError("Table requires a head section.")

    column_count = len(header)

    for row in rows:
        if len(row) != column_count:
            raise ValueError(
                f"Table row has {len(row)} cells, expected {column_count}: {row}"
            )

    return Table(
        label=label,
        caption=caption,
        header=header,
        rows=rows,
    )


def parse_image(source: str) -> Image:
    lines = _normalize_lines(source)

    if not lines or lines[0].strip() != "image":
        raise ValueError("LDL image block must start with 'image'.")

    params: dict[str, str] = {}
    file: str | None = None

    section: str | None = None

    for line in lines[1:]:
        stripped = line.strip()
        indent = _indent(line)

        if indent == 2 and stripped in {"params", "file"}:
            section = stripped
            continue

        if section == "params":
            key, value = _parse_param_line(line)

            if key not in {"label", "caption"}:
                raise ValueError(f"Unknown image parameter: {key}")

            params[key] = value

        elif section == "file":
            file = stripped

        else:
            raise ValueError(f"Line outside known image section: {line}")

    label, caption = _parse_common_params(params)

    if not caption:
        raise ValueError("Image requires a caption.")

    if not file:
        raise ValueError("Image requires a file.")

    return Image(
        label=label,
        caption=caption,
        file=file,
    )


def parse_code(source: str) -> Code:
    lines = [line.rstrip() for line in source.splitlines()]

    while lines and not lines[0].strip():
        lines.pop(0)

    if not lines or lines[0].strip() != "code":
        raise ValueError("LDL code block must start with 'code'.")

    params: dict[str, str] = {}
    body_lines: list[str] = []

    section: str | None = None

    for line in lines[1:]:
        stripped = line.strip()
        indent = _indent(line)

        if not stripped and section != "body":
            continue

        if indent == 2 and stripped in {"params", "body"}:
            section = stripped
            continue

        if section == "params":
            key, value = _parse_param_line(line)

            if key not in {"label", "caption", "language"}:
                raise ValueError(f"Unknown code parameter: {key}")

            params[key] = value

        elif section == "body":
            body_lines.append(line)

        else:
            raise ValueError(f"Line outside known code section: {line}")

    label, caption = _parse_common_params(params)
    language = params.get("language")
    body = _parse_fenced_body(body_lines)

    if not language:
        raise ValueError("Code requires a language.")

    if not body:
        raise ValueError("Code requires a body.")

    return Code(
        label=label,
        caption=caption,
        language=language,
        body=body,
    )


def parse_heading(source: str) -> Heading:
    lines = _normalize_lines(source)

    if not lines:
        raise ValueError("LDL heading block is empty.")

    level = lines[0].strip()

    if level not in {"chapter", "section", "subsection"}:
        raise ValueError(f"Unsupported heading level: {level}")

    if len(lines) < 2:
        raise ValueError("Heading requires a title.")

    title = lines[1].strip()

    if not title:
        raise ValueError("Heading requires a title.")

    return Heading(level=level, title=title)


def _directive_name(line: str) -> str:
    return line.strip()


def _split_blocks(source: str) -> list[str]:
    lines = [line.rstrip() for line in source.splitlines()]

    blocks: list[list[str]] = []
    current: list[str] = []

    for line in lines:
        stripped = line.strip()

        if not stripped:
            if current:
                current.append(line)
            continue

        if not line.startswith(" ") and stripped:
            if current:
                blocks.append(current)
            current = [line]
        else:
            current.append(line)

    if current:
        blocks.append(current)

    return ["\n".join(block).strip("\n") for block in blocks]


def parse_document(source: str) -> list[object]:
    from .registry import PARSERS

    elements: list[object] = []

    for block in _split_blocks(source):
        first_line = block.splitlines()[0]
        directive = _directive_name(first_line)

        if directive not in PARSERS:
            raise ValueError(f"Unsupported LDL directive: {directive}")

        elements.append(PARSERS[directive](block))

    return elements
