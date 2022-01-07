# --------------------------------------------------------------------------------------
# SPDX-FileCopyrightText: 2021 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
# --------------------------------------------------------------------------------------
import itertools
from operator import itemgetter
from uuid import UUID

from ramodels.mo import OrganisationUnit

from ..util import OrgTree
from ..util import tree_visitor
from .base import BaseGenerator


class OrgUnitGenerator(BaseGenerator):
    def generate(
        self,
        org_tree: OrgTree,
        org_unit_type_uuid: UUID,
        org_unit_levels: dict[str, UUID],
    ) -> list[list[OrganisationUnit]]:
        levels = [
            uuid
            for user_key, uuid in sorted(org_unit_levels.items(), key=itemgetter(0))
        ]

        def construct_org_unit(
            name: str, level: int, prefix: str
        ) -> tuple[int, OrganisationUnit]:
            return level, OrganisationUnit.from_simplified_fields(
                uuid=self.generate_uuid(prefix + name),
                user_key=name,
                name=name,
                org_unit_type_uuid=org_unit_type_uuid,
                org_unit_level_uuid=levels[level],
                parent_uuid=self.generate_uuid(prefix) if prefix else None,
                from_date="1930-01-01",
            )

        model_tree = list(tree_visitor(org_tree, construct_org_unit))
        model_layers = itertools.groupby(
            sorted(model_tree, key=itemgetter(0)), itemgetter(0)
        )

        return [
            list(map(itemgetter(1), model_layer)) for level, model_layer in model_layers
        ]
