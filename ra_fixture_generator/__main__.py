# --------------------------------------------------------------------------------------
# SPDX-FileCopyrightText: 2021 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
# --------------------------------------------------------------------------------------
from ra_fixture_generator.cli import generate

if __name__ == "__main__":
    generate(
        prog_name=__package__,  # prevents 'Usage: __main__.py [OPTIONS]'
        auto_envvar_prefix="FIXTURE_GENERATOR",
    )
