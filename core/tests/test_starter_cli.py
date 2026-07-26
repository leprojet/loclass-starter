import subprocess
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[2]
ENTRYPOINT = PROJECT_ROOT / "loclass"
HELP_OUTPUT = """\
loclass document runner

Verwendung:
  ./loclass.lua build
  ./loclass.lua odt
  ./loclass.lua all
  ./loclass.lua clean
  ./loclass.lua doctor

"""


def run_entrypoint(action: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [ENTRYPOINT, action],
        cwd=PROJECT_ROOT,
        check=False,
        capture_output=True,
        text=True,
    )


@pytest.mark.parametrize("action", ["--help", "-h", "help"])
def test_help_actions_succeed(action: str) -> None:
    result = run_entrypoint(action)

    assert result.returncode == 0
    assert result.stdout == HELP_OUTPUT
    assert result.stderr == ""


def test_unknown_action_is_an_error() -> None:
    result = run_entrypoint("unknown-action")

    assert result.returncode == 2
    assert result.stdout == HELP_OUTPUT
    assert result.stderr == ""
