from pathlib import Path

from loclass.contributions import PagePlacement
from loclass_ldl import parse_document

from core.tools.ldl_pdf import (
    build_package_plan,
    render_wrapper,
)


def test_manifest_package_reaches_latex_plan() -> None:
    document = parse_document(
        """---
packages:
  loclass.tlp:
    label: amber+strict
---
"""
    )

    plan = build_package_plan(document)

    assert plan.package_ids == (
        "loclass.tlp",
    )

    headers = plan.contributions_for(
        "latex",
        slot=PagePlacement.HEADER_RIGHT.value,
    )
    footers = plan.contributions_for(
        "latex",
        slot=PagePlacement.FOOTER_RIGHT.value,
    )

    assert len(headers) == 1
    assert len(footers) == 1
    assert headers[0].value.text == "TLP:AMBER+STRICT"
    assert footers[0].value.text == "TLP:AMBER+STRICT"


def test_wrapper_loads_packages_before_project_code() -> None:
    document = parse_document(
        """---
title: Sicherheitsbericht
packages:
  loclass.tlp:
    label: amber
---
"""
    )

    wrapper = render_wrapper(
        Path("build/ldl/document.tex"),
        document.metadata,
        build_package_plan(document),
    )

    package_position = wrapper.index(
        r"\renewcommand{\locHeaderRightAddon}"
    )
    macros_position = wrapper.index(
        r"\InputIfFileExists{project/macros.tex}"
    )
    environments_position = wrapper.index(
        r"\InputIfFileExists{project/environments.tex}"
    )

    assert package_position < macros_position
    assert package_position < environments_position


def test_wrapper_does_not_reload_core() -> None:
    document = parse_document("Ein Absatz.")

    wrapper = render_wrapper(
        Path("build/ldl/document.tex"),
        document.metadata,
        build_package_plan(document),
    )

    assert r"\input{core/index}" not in wrapper
    assert r"\input{core/commands/index}" not in wrapper
    assert wrapper.count(
        r"\documentclass{core/loclass}"
    ) == 1
