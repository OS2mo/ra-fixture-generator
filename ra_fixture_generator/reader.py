# --------------------------------------------------------------------------------------
# SPDX-FileCopyrightText: 2021 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
# --------------------------------------------------------------------------------------
from typing import Optional
from uuid import UUID

from gql import gql
from httpx import Client
from pydantic import AnyHttpUrl
from raclients.auth import AuthenticatedHTTPXClient
from raclients.graph.client import GraphQLClient


def get_clients(
    mo_url: AnyHttpUrl,
    client_id: str,
    client_secret: str,
    auth_server: AnyHttpUrl,
    auth_realm: str = "mo",
) -> tuple[AuthenticatedHTTPXClient, GraphQLClient]:
    auth_params = dict(
        client_id=client_id,
        client_secret=client_secret,
        auth_realm=auth_realm,
        auth_server=auth_server,
    )
    httpx_client = AuthenticatedHTTPXClient(base_url=mo_url, **auth_params)
    graphql_client = GraphQLClient(
        url=f"{mo_url}/graphql/v3",
        **auth_params,
        sync=True,
    )
    return httpx_client, graphql_client


def get_root_org(graphql_client: GraphQLClient) -> Optional[UUID]:
    with graphql_client as session:
        query = gql(
            """
            query RootOrgQuery {
                org {
                    uuid
                }
            }
            """
        )
        result = session.execute(query)
    return UUID(result["org"]["uuid"])


def get_classes(graphql_client: GraphQLClient) -> dict[str, dict[str, UUID]]:
    with graphql_client as session:
        query = gql(
            """
            query FacetMOQuery {
              facets {
                user_key
                classes {
                  uuid
                  user_key
                }
              }
            }
            """
        )
        result = session.execute(query)
    return {
        facet["user_key"]: {
            klass["user_key"]: UUID(klass["uuid"]) for klass in facet["classes"]
        }
        for facet in result["facets"]
    }


def get_it_systems(client: Client, graphql_client: GraphQLClient) -> dict[str, UUID]:
    root_org_uuid = get_root_org(graphql_client)
    r = client.get(f"/service/o/{root_org_uuid}/it/")
    it_systems = r.json()
    return {i["user_key"]: UUID(i["uuid"]) for i in it_systems}
