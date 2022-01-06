# --------------------------------------------------------------------------------------
# SPDX-FileCopyrightText: 2021 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
# --------------------------------------------------------------------------------------
from typing import TextIO

import click

from .generator import generate_data


@click.command(
    context_settings=dict(
        max_content_width=120,
    ),
)
@click.option(
    "--root-org-name",
    help="Name of the root organisation.",
    type=click.STRING,
    default="Magenta Aps",
    show_default=True,
    envvar="ROOT_ORG_NAME",
    show_envvar=True,
)
@click.option(
    "-s",
    "--size",
    help=(
        "Size of the generated dataset. "
        "The number of generated employees roughly scales in 50n * log₂n."
    ),
    type=click.INT,
    default=10,
    show_default=True,
    envvar="FIXTURE_SIZE",
    show_envvar=True,
)
@click.option(
    "-i",
    "--indent",
    help="Pass 'indent' to json serializer.",
    type=click.INT,
    default=None,
)
@click.option(
    "-o",
    "--output-file",
    help="Output OS2mo flatfile to FILENAME.",
    type=click.File("w"),
    default="-",
)
def generate(root_org_name: str, size: int, indent: int, output_file: TextIO) -> None:
    """Flatfile Fixture Generator.

    Used to generate flatfile fixture data (JSON) for OS2mo.
    """
    mo_flatfile = generate_data(root_org_name, size)
    output_file.write(mo_flatfile.json(indent=indent))
