from .model import Table


def _indent(line: str) -> int:
    return len(line) - len(line.lstrip(" "))


def _split_cells(line: str) -> list[str]:
    return [cell.strip() for cell in line.split("|")]


def parse_table(source: str) -> Table:
    lines = [line.rstrip() for line in source.splitlines() if line.strip()]

    if not lines or lines[0].strip() != "table":
        raise ValueError("LDL table block must start with 'table'.")

    label: str | None = None
    caption: str | None = None
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
            if ":" not in stripped:
                raise ValueError(f"Invalid parameter line: {line}")

            key, value = stripped.split(":", 1)
            key = key.strip()
            value = value.strip()

            if key == "label":
                label = value or None
            elif key == "caption":
                caption = value
            else:
                raise ValueError(f"Unknown table parameter: {key}")

        elif section == "head":
            header = _split_cells(stripped)

        elif section == "body":
            rows.append(_split_cells(stripped))

        else:
            raise ValueError(f"Line outside known table section: {line}")

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
