#!/usr/bin/env python3
# --------------------------------------------------------------------------------------
# SPDX-FileCopyrightText: 2021 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
# --------------------------------------------------------------------------------------
import click


@click.command()
def generate() -> None:
    """Flatfile Fixture Generator.

    Used to generate flatfile fixture data (JSON) for OS2mo/LoRa.
    """
    pass


if __name__ == "__main__":
    cli(auto_envvar_prefix="FIXTURE_GENERATOR")
