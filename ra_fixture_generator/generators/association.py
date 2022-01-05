# --------------------------------------------------------------------------------------
# SPDX-FileCopyrightText: 2021 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
# --------------------------------------------------------------------------------------
import random
from typing import List
from typing import Tuple

import more_itertools
from ramodels.mo import Employee
from ramodels.mo import OrganisationUnit
from ramodels.mo.details import Association

from .base import BaseGenerator


class AssociationGenerator(BaseGenerator):
    def generate(
        self,
        org_layers: List[List[OrganisationUnit]],
        employees: List[Employee],
        association_types: List[Tuple[str, str, str]],
        employees_per_org: int = 10,
    ) -> List[List[Association]]:
        def construct_association(org_unit: OrganisationUnit) -> Association:
            employee = random.choice(employees)

            employee_uuid = employee.uuid
            org_unit_uuid = org_unit.uuid

            association_type = random.choice(association_types)[0]
            association_type_uuid = self.generate_uuid(association_type)

            uuid = self.generate_uuid(
                str(employee_uuid) + str(org_unit_uuid) + str(association_type_uuid)
            )

            return Association.from_simplified_fields(
                uuid=uuid,
                org_unit_uuid=org_unit_uuid,
                person_uuid=employee_uuid,
                association_type_uuid=association_type_uuid,
                from_date="1930-01-01",
                to_date=None,
            )

        def construct_associations(org_unit: OrganisationUnit) -> List[Association]:
            return [construct_association(org_unit) for _ in range(employees_per_org)]

        return list(
            list(more_itertools.flatten(map(construct_associations, layer)))
            for layer in org_layers
        )
