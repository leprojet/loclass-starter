from dataclasses import dataclass, field


@dataclass(frozen=True)
class Table:
    label: str | None
    caption: str
    header: list[str]
    rows: list[list[str]] = field(default_factory=list)


@dataclass(frozen=True)
class Image:
    label: str | None
    caption: str
    file: str
