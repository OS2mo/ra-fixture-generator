# --------------------------------------------------------------------------------------
# SPDX-FileCopyrightText: 2021 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
# --------------------------------------------------------------------------------------
import random
from uuid import UUID

import more_itertools
from ramodels.mo import Employee
from ramodels.mo import OrganisationUnit
from ramodels.mo import Validity
from ramodels.mo._shared import OrgUnitRef
from ramodels.mo._shared import PersonRef
from ramodels.mo._shared import RoleType
from ramodels.mo.details import Role

from .base import BaseGenerator


class RoleGenerator(BaseGenerator):
    def generate(
        self,
        org_layers: list[list[OrganisationUnit]],
        employees: list[Employee],
        employees_per_org: int,
        role_types: dict[str, UUID],
    ) -> list[list[Role]]:
        role_type_uuids = list(role_types.values())
        employee_iter = iter(employees)

        def construct_role(org_unit: OrganisationUnit) -> Role:
            org_employees = more_itertools.take(employees_per_org, employee_iter)
            assert len(org_employees) == employees_per_org

            employee = random.choice(org_employees)
            return Role(
                role_type=RoleType(uuid=random.choice(role_type_uuids)),
                person=PersonRef(uuid=employee.uuid),
                org_unit=OrgUnitRef(uuid=org_unit.uuid),
                validity=Validity(
                    from_date="1930-01-01",
                    to_date=None,
                ),
            )

        return_value = list(list(map(construct_role, layer)) for layer in org_layers)
        # Ensure all employees were consumed
        assert more_itertools.ilen(employee_iter) == 0
        return return_value
