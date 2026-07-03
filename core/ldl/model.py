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


@dataclass(frozen=True)
class Code:
    label: str | None
    caption: str | None
    language: str
    body: list[str]


@dataclass(frozen=True)
class Heading:
    level: str
    title: str


@dataclass(frozen=True)
class Raw:
    text: str


@dataclass(frozen=True)
class List:
    type: str
    items: list[str]


@dataclass(frozen=True)
class Shell:
    style: str
    title: str | None
    body: list[str]
