#!/usr/bin/env python3

from argparse import ArgumentParser
from pathlib import Path
import sys

from core.ldl.formatter import format_source


def format_file(path: Path, check: bool, stdout: bool) -> int:
    source = path.read_text(encoding="utf-8")
    formatted = format_source(source)

    if check:
        if source == formatted:
            print(f"✓ {path} is already formatted.")
            return 0

        print(f"✗ {path} is not formatted.")
        return 1

    if stdout:
        print(formatted, end="")
        return 0

    if source != formatted:
        path.write_text(formatted, encoding="utf-8")
        print(f"✓ Formatted {path}")
    else:
        print(f"✓ {path} already formatted")

    return 0


def main() -> None:
    parser = ArgumentParser(description="Format LDL documents.")

    parser.add_argument(
        "file",
        type=Path,
        help="LDL file",
    )

    parser.add_argument(
        "--check",
        action="store_true",
        help="Do not modify the file.",
    )

    parser.add_argument(
        "--stdout",
        action="store_true",
        help="Write formatted document to stdout.",
    )

    args = parser.parse_args()

    sys.exit(
        format_file(
            args.file,
            check=args.check,
            stdout=args.stdout,
        )
    )


if __name__ == "__main__":
    main()
