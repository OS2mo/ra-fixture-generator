# --------------------------------------------------------------------------------------
# SPDX-FileCopyrightText: 2021 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
# --------------------------------------------------------------------------------------
import itertools
from operator import itemgetter
from typing import List
from typing import Tuple

from ramodels.mo import OrganisationUnit

from ..util import OrgTree
from ..util import tree_visitor
from .base import BaseGenerator


class OrgUnitGenerator(BaseGenerator):
    def generate(self, org_tree: OrgTree) -> List[List[OrganisationUnit]]:
        def construct_org_unit(
            name: str, level: int, prefix: str
        ) -> Tuple[int, OrganisationUnit]:
            parent_uuid = None
            if prefix:
                parent_uuid = self.generate_uuid("org_unit" + prefix)

            return level, OrganisationUnit.from_simplified_fields(
                uuid=self.generate_uuid("org_unit" + prefix + name),
                user_key=name,
                name=name,
                org_unit_type_uuid=self.generate_uuid("Afdeling"),
                org_unit_level_uuid=self.generate_uuid("N" + str(level)),
                parent_uuid=parent_uuid,
                from_date="1930-01-01",
            )

        model_tree = list(tree_visitor(org_tree, construct_org_unit))
        model_layers = itertools.groupby(
            sorted(model_tree, key=itemgetter(0)), itemgetter(0)
        )

        return [
            list(map(itemgetter(1), model_layer)) for level, model_layer in model_layers
        ]
