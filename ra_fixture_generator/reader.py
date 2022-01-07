from uuid import UUID

from gql import gql
from pydantic import AnyHttpUrl
from raclients.graph.client import GraphQLClient


def get_classes(
    mo_url: AnyHttpUrl,
    client_id: str,
    client_secret: str,
    auth_server: AnyHttpUrl,
    auth_realm: str = "mo",
) -> dict[str, dict[str, UUID]]:
    client = GraphQLClient(
        url=f"{mo_url}/graphql",
        client_id=client_id,
        client_secret=client_secret,
        auth_realm=auth_realm,
        auth_server=auth_server,
        sync=True,
    )
    with client as session:
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
