import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
ENTRYPOINT = PROJECT_ROOT / "loclass"


def test_starter_entrypoint_is_a_valid_executable_symlink() -> None:
    assert ENTRYPOINT.is_symlink()

    stored_target = ENTRYPOINT.readlink()
    assert not stored_target.is_absolute()

    target = ENTRYPOINT.parent / stored_target
    assert target.exists()
    assert not target.is_symlink()
    assert target.is_file()
    assert os.access(target, os.X_OK)
    assert target.resolve().is_relative_to(PROJECT_ROOT.resolve())
