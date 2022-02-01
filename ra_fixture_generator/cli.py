# --------------------------------------------------------------------------------------
# SPDX-FileCopyrightText: 2021 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
# --------------------------------------------------------------------------------------
from typing import TextIO

import click
from pydantic import AnyHttpUrl

from .generator import generate_data
from .reader import get_classes
from .reader import get_clients
from .reader import get_it_systems
from .util import validate_url


@click.command(
    context_settings=dict(
        max_content_width=120,
    ),
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
    "--mo-url",
    help="OS2mo URL.",
    required=True,
    callback=validate_url,
    envvar="MO_URL",
    show_envvar=True,
)
@click.option(
    "--client-id",
    help="Client ID used to authenticate against OS2mo.",
    required=True,
    default="dipex",
    show_default=True,
    envvar="CLIENT_ID",
    show_envvar=True,
)
@click.option(
    "--client-secret",
    help="Client secret used to authenticate against OS2mo.",
    required=True,
    envvar="CLIENT_SECRET",
    show_envvar=True,
)
@click.option(
    "--auth-server",
    help="Keycloak authentication server.",
    required=True,
    callback=validate_url,
    envvar="AUTH_SERVER",
    show_envvar=True,
)
@click.option(
    "--auth-realm",
    help="Keycloak realm for OS2mo authentication.",
    default="mo",
    show_default=True,
    envvar="AUTH_REALM",
    show_envvar=True,
)
@click.option(
    "-o",
    "--output-file",
    help="Output OS2mo flatfile to FILENAME.",
    type=click.File("w"),
    default="mo.json",
    show_default=True,
)
@click.option(
    "-i",
    "--indent",
    help="Pass 'indent' to json serializer.",
    type=click.INT,
    default=None,
)
def generate(
    size: int,
    mo_url: AnyHttpUrl,
    client_id: str,
    client_secret: str,
    auth_server: AnyHttpUrl,
    auth_realm: str,
    output_file: TextIO,
    indent: int,
) -> None:
    """Flatfile Fixture Generator.

    Used to generate flatfile fixture data (JSON) for OS2mo.
    """
    client, graphql_client = get_clients(
        mo_url=mo_url,
        client_id=client_id,
        client_secret=client_secret,
        auth_server=auth_server,
        auth_realm=auth_realm,
    )
    classes = get_classes(graphql_client)
    it_systems = get_it_systems(client, graphql_client)
    mo_flatfile = generate_data(size=size, classes=classes, it_systems=it_systems)
    output_file.write(mo_flatfile.json(indent=indent))
