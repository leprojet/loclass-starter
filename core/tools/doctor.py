#!/usr/bin/env python3

from __future__ import annotations

import importlib
import shutil
from dataclasses import dataclass
from pathlib import Path

from core.tools.project_config import load_project_config


PROJECT_ROOT = Path(__file__).resolve().parents[2]
CONFIG_PATH = PROJECT_ROOT / "pyproject.toml"


@dataclass(frozen=True)
class Check:
    name: str
    ok: bool
    detail: str


def _display_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(PROJECT_ROOT).as_posix()
    except ValueError:
        return path.resolve().as_posix()


def _command_check(command: str) -> Check:
    executable = shutil.which(command)

    if executable is None:
        return Check(
            name=command,
            ok=False,
            detail="not found",
        )

    return Check(
        name=command,
        ok=True,
        detail=executable,
    )


def _file_check(name: str, path: Path) -> Check:
    return Check(
        name=name,
        ok=path.is_file(),
        detail=_display_path(path),
    )


def _directory_check(name: str, path: Path) -> Check:
    if path.exists() and not path.is_dir():
        return Check(
            name=name,
            ok=False,
            detail=f"{_display_path(path)} is not a directory",
        )

    detail = _display_path(path)

    if not path.exists():
        detail += " (will be created)"

    return Check(
        name=name,
        ok=True,
        detail=detail,
    )


def _python_package_check(package: str) -> Check:
    try:
        module = importlib.import_module(package)
    except ImportError as exc:
        return Check(
            name=f"Python package {package}",
            ok=False,
            detail=str(exc),
        )

    module_file = getattr(module, "__file__", None)

    if module_file is None:
        return Check(
            name=f"Python package {package}",
            ok=False,
            detail="imported without a module location",
        )

    location = Path(module_file).resolve()

    return Check(
        name=f"Python package {package}",
        ok=location.is_file(),
        detail=location.as_posix(),
    )


def run_doctor() -> int:
    checks: list[Check] = []

    try:
        config = load_project_config(CONFIG_PATH)
    except (OSError, ValueError) as exc:
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
                    detail=_display_path(CONFIG_PATH),
                ),
                _file_check(
                    "main TeX document",
                    PROJECT_ROOT / config.tex_main,
                ),
                _directory_check(
                    "build directory",
                    PROJECT_ROOT / config.build_dir,
                ),
                Check(
                    name="generated PDF",
                    ok=True,
                    detail=_display_path(PROJECT_ROOT / config.pdf_path),
                ),
            ]
        )

    checks.extend(
        [
            _python_package_check("loclass"),
            _python_package_check("loclass_ldl"),
            _file_check(
                "starter frontend",
                PROJECT_ROOT / "loclass",
            ),
            _file_check(
                "loclass class",
                PROJECT_ROOT / "core/loclass.cls",
            ),
            _file_check(
                "latexmk configuration",
                PROJECT_ROOT / "latexmkrc",
            ),
            _file_check(
                "LDL PDF builder",
                PROJECT_ROOT / "core/tools/build_ldl_pdf.py",
            ),
            _file_check(
                "input generator",
                PROJECT_ROOT / "core/tools/generate_inputs.pl",
            ),
            _command_check("uv"),
            _command_check("loclass"),
            _command_check("perl"),
            _command_check("latexmk"),
            _command_check("pdflatex"),
        ]
    )

    print("loclass starter doctor")
    print()

    for check in checks:
        status = "ok" if check.ok else "error"
        print(f"[{status:5}] {check.name:<26} {check.detail}")

    failures = sum(not check.ok for check in checks)

    print()

    if failures:
        print(f"{failures} check(s) failed.")
        return 1

    print("All checks passed.")
    return 0


def main() -> int:
    return run_doctor()


if __name__ == "__main__":
    raise SystemExit(main())
