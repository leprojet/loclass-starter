#!/usr/bin/env python3

from __future__ import annotations

import shutil
from dataclasses import dataclass
from pathlib import Path

from core.tools.project_config import load_project_config


@dataclass(frozen=True)
class Check:
    name: str
    ok: bool
    detail: str


def _command_check(command: str) -> Check:
    path = shutil.which(command)

    if path:
        return Check(
            name=command,
            ok=True,
            detail=path,
        )

    return Check(
        name=command,
        ok=False,
        detail="not found",
    )


def _file_check(name: str, path: Path) -> Check:
    return Check(
        name=name,
        ok=path.is_file(),
        detail=str(path),
    )


def _directory_check(name: str, path: Path) -> Check:
    if path.exists() and not path.is_dir():
        return Check(
            name=name,
            ok=False,
            detail=f"{path} exists but is not a directory",
        )

    return Check(
        name=name,
        ok=True,
        detail=str(path),
    )


def run_doctor() -> int:
    checks: list[Check] = []

    try:
        config = load_project_config()
    except ValueError as exc:
        checks.append(
            Check(
                name="project configuration",
                ok=False,
                detail=str(exc),
            )
        )
    else:
        checks.extend(
            [
                Check(
                    name="project configuration",
                    ok=True,
                    detail="pyproject.toml",
                ),
                _file_check(
                    "main TeX document",
                    config.tex_main,
                ),
                _directory_check(
                    "build directory",
                    config.build_dir,
                ),
            ]
        )

    checks.extend(
        [
            _file_check(
                "loclass class",
                Path("core/loclass.cls"),
            ),
            _file_check(
                "latexmk configuration",
                Path("latexmkrc"),
            ),
            _command_check("uv"),
            _command_check("latexmk"),
            _command_check("pdflatex"),
        ]
    )

    print("loclass starter doctor")
    print()

    for check in checks:
        status = "ok" if check.ok else "error"
        print(f"[{status:5}] {check.name:<24} {check.detail}")

    errors = sum(not check.ok for check in checks)

    print()

    if errors:
        print(f"{errors} check(s) failed.")
        return 1

    print("All checks passed.")
    return 0


def main() -> int:
    return run_doctor()


if __name__ == "__main__":
    raise SystemExit(main())
