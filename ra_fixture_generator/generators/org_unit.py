# --------------------------------------------------------------------------------------
# SPDX-FileCopyrightText: 2021 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
# --------------------------------------------------------------------------------------
import itertools
from operator import itemgetter
from uuid import UUID

from ramodels.mo import OrganisationUnit

from .base import BaseGenerator
from ..util import OrgTree
from ..util import tree_visitor


class OrgUnitGenerator(BaseGenerator):
    def __init__(self, org_unit_levels: dict[str, UUID]) -> None:
        super().__init__()
        self.org_unit_levels = org_unit_levels

    def generate(
        self, org_tree: OrgTree, org_unit_type_uuid: UUID
    ) -> list[list[OrganisationUnit]]:
        levels = [
            uuid
            for user_key, uuid in sorted(
                self.org_unit_levels.items(), key=itemgetter(0)
            )
        ]
        org_unit_uuids = {}

        def construct_org_unit(
            name: str, level: int, prefix: str
        ) -> tuple[int, OrganisationUnit]:
            org_unit = OrganisationUnit.from_simplified_fields(
                user_key=name,
                name=name,
                org_unit_type_uuid=org_unit_type_uuid,
                org_unit_level_uuid=levels[level],
                parent_uuid=org_unit_uuids[prefix] if prefix else None,
                **self.validity(allow_open_from=False).dict(),
            )
            org_unit_uuids[prefix + name] = org_unit.uuid
            return level, org_unit

        model_tree = list(tree_visitor(org_tree, construct_org_unit))
        model_layers = itertools.groupby(
            sorted(model_tree, key=itemgetter(0)), itemgetter(0)
        )

        return [
            list(map(itemgetter(1), model_layer)) for level, model_layer in model_layers
        ]
