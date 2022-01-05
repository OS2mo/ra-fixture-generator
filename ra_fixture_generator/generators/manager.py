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
from ramodels.mo.details import Manager

from .base import BaseGenerator


class ManagerGenerator(BaseGenerator):
    def generate(
        self,
        org_layers: List[List[OrganisationUnit]],
        employees: List[Employee],
        responsibilities: List[Tuple[str, str, str]],
        manager_levels: List[Tuple[str, str, str]],
        manager_types: List[Tuple[str, str, str]],
        employees_per_org: int = 10,
    ) -> List[List[Manager]]:

        employee_iter = iter(employees)

        def construct_manager(org_unit: OrganisationUnit) -> Manager:
            org_employees = more_itertools.take(employees_per_org, employee_iter)
            assert len(org_employees) == employees_per_org

            employee = random.choice(org_employees)

            employee_uuid = employee.uuid
            org_unit_uuid = org_unit.uuid

            responsibility = random.choice(responsibilities)[0]
            responsibility_uuid = self.generate_uuid(responsibility)

            manager_level = random.choice(manager_levels)[0]
            manager_level_uuid = self.generate_uuid(manager_level)

            manager_type = random.choice(manager_types)[0]
            manager_type_uuid = self.generate_uuid(manager_type)

            uuid = self.generate_uuid(
                str(employee_uuid) + str(org_unit_uuid) + str(responsibility_uuid)
            )

            return Manager.from_simplified_fields(
                uuid=uuid,
                org_unit_uuid=org_unit_uuid,
                person_uuid=employee_uuid,
                responsibility_uuids=[responsibility_uuid],
                manager_level_uuid=manager_level_uuid,
                manager_type_uuid=manager_type_uuid,
                from_date="1930-01-01",
            )

        return_value = list(list(map(construct_manager, layer)) for layer in org_layers)
        # Ensure all employees were consumed
        assert more_itertools.ilen(employee_iter) == 0
        return return_value
