# --------------------------------------------------------------------------------------
# SPDX-FileCopyrightText: 2021 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
# --------------------------------------------------------------------------------------
import random
from uuid import UUID

import more_itertools
from ramodels.mo import Employee
from ramodels.mo import OrganisationUnit
from ramodels.mo.details import Association

from .base import BaseGenerator


class AssociationGenerator(BaseGenerator):
    def generate(
        self,
        org_layers: list[list[OrganisationUnit]],
        employees: list[Employee],
        employees_per_org: int,
        association_types: dict[str, UUID],
    ) -> list[list[Association]]:
        association_type_uuids = list(association_types.values())

        def construct_association(org_unit: OrganisationUnit) -> Association:
            employee = random.choice(employees)
            return Association.from_simplified_fields(
                org_unit_uuid=org_unit.uuid,
                person_uuid=employee.uuid,
                association_type_uuid=random.choice(association_type_uuids),
                from_date="1930-01-01",
                to_date=None,
            )

        def construct_associations(org_unit: OrganisationUnit) -> list[Association]:
            return [construct_association(org_unit) for _ in range(employees_per_org)]

        return [
            list(more_itertools.flatten(map(construct_associations, layer)))
            for layer in org_layers
        ]
