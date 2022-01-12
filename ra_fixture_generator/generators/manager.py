# --------------------------------------------------------------------------------------
# SPDX-FileCopyrightText: 2021 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
# --------------------------------------------------------------------------------------
import random
from uuid import UUID

import more_itertools
from ramodels.mo import Employee
from ramodels.mo import OrganisationUnit
from ramodels.mo.details import Manager

from .base import BaseGenerator


class ManagerGenerator(BaseGenerator):
    def generate(
        self,
        org_layers: list[list[OrganisationUnit]],
        employees: list[Employee],
        employees_per_org: int,
        responsibilities: dict[str, UUID],
        manager_levels: dict[str, UUID],
        manager_types: dict[str, UUID],
    ) -> list[list[Manager]]:
        responsibility_uuids = list(responsibilities.values())
        manager_level_uuids = list(manager_levels.values())
        manager_type_uuids = list(manager_types.values())
        employee_iter = iter(employees)

        def construct_manager(org_unit: OrganisationUnit) -> Manager:
            org_employees = more_itertools.take(employees_per_org, employee_iter)
            assert len(org_employees) == employees_per_org

            employee = random.choice(org_employees)
            return Manager.from_simplified_fields(
                org_unit_uuid=org_unit.uuid,
                person_uuid=employee.uuid,
                responsibility_uuids=[random.choice(responsibility_uuids)],
                manager_level_uuid=random.choice(manager_level_uuids),
                manager_type_uuid=random.choice(manager_type_uuids),
                from_date="1930-01-01",
            )

        return_value = list(list(map(construct_manager, layer)) for layer in org_layers)
        # Ensure all employees were consumed
        assert more_itertools.ilen(employee_iter) == 0
        return return_value
