#!/usr/bin/env python3
# --------------------------------------------------------------------------------------
# SPDX-FileCopyrightText: 2021 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
# --------------------------------------------------------------------------------------
from importlib.metadata import version  # type: ignore

from ra_fixture_generator import __version__


def test_version():
    pyproject_version = version("ra-fixture-generator")
    assert __version__ == pyproject_version
