#!/usr/bin/env python3

from __future__ import annotations

import argparse
import tomllib
from dataclasses import dataclass
from pathlib import Path


DEFAULT_CONFIG_PATH = Path("pyproject.toml")


@dataclass(frozen=True)
class ProjectConfig:
    tex_main: Path
    build_dir: Path

    @property
    def pdf_path(self) -> Path:
        return self.build_dir / f"{self.tex_main.stem}.pdf"


def _required_string(
    section: dict[str, object],
    key: str,
) -> str:
    value = section.get(key)

    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"Missing or invalid [tool.loclass.dev].{key}")

    return value


def load_project_config(
    path: Path = DEFAULT_CONFIG_PATH,
) -> ProjectConfig:
    try:
        data = tomllib.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ValueError(f"Project configuration not found: {path}") from exc

    try:
        section = data["tool"]["loclass"]["dev"]
    except KeyError as exc:
        raise ValueError("Missing [tool.loclass.dev] configuration") from exc

    if not isinstance(section, dict):
        raise ValueError("[tool.loclass.dev] must be a TOML table")

    return ProjectConfig(
        tex_main=Path(_required_string(section, "tex_main")),
        build_dir=Path(_required_string(section, "build_dir")),
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="project_config",
        description="Read loclass starter project configuration.",
    )
    parser.add_argument(
        "value",
        choices=(
            "tex-main",
            "build-dir",
            "pdf",
        ),
    )

    args = parser.parse_args()
    config = load_project_config()

    values = {
        "tex-main": config.tex_main,
        "build-dir": config.build_dir,
        "pdf": config.pdf_path,
    }

    print(values[args.value])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
