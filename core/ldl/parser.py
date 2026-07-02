from .model import Image, Table


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
