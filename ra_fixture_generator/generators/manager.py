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
from ..util import EmployeeValidity


class ManagerGenerator(BaseGenerator):
    def __init__(
        self,
        responsibilities: dict[str, UUID],
        manager_levels: dict[str, UUID],
        manager_types: dict[str, UUID],
    ) -> None:
        super().__init__()
        self.responsibility_uuids = list(responsibilities.values())
        self.manager_level_uuids = list(manager_levels.values())
        self.manager_type_uuids = list(manager_types.values())

    def generate(
        self,
        org_layers: list[list[OrganisationUnit]],
        employees: list[Employee],
        employees_per_org: int,
    ) -> list[list[Manager]]:
        employee_iter = iter(employees)

        def construct_manager(org_unit: OrganisationUnit) -> Manager:
            org_employees = more_itertools.take(employees_per_org, employee_iter)
            assert len(org_employees) == employees_per_org

            employee = random.choice(org_employees)
            return Manager.from_simplified_fields(
                org_unit_uuid=org_unit.uuid,
                person_uuid=employee.uuid,
                responsibility_uuids=[random.choice(self.responsibility_uuids)],
                manager_level_uuid=random.choice(self.manager_level_uuids),
                manager_type_uuid=random.choice(self.manager_type_uuids),
                **self.random_validity(org_unit.validity, EmployeeValidity).dict(),
            )

        return_value = list(list(map(construct_manager, layer)) for layer in org_layers)
        # Ensure all employees were consumed
        assert more_itertools.ilen(employee_iter) == 0
        return return_value
