# --------------------------------------------------------------------------------------
# SPDX-FileCopyrightText: 2021 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
# --------------------------------------------------------------------------------------
import random
from collections.abc import Iterator
from uuid import UUID

import more_itertools
from ramodels.mo import Employee
from ramodels.mo import OrganisationUnit
from ramodels.mo._shared import OrgUnitRef
from ramodels.mo._shared import PersonRef
from ramodels.mo._shared import RoleType
from ramodels.mo.details import Role

from .base import BaseGenerator
from ..util import EmployeeValidity
from ..util import thawed


class RoleGenerator(BaseGenerator):
    def __init__(self, role_types: dict[str, UUID]) -> None:
        super().__init__()
        self.role_type_uuids = list(role_types.values())

    def generate(
        self,
        org_layers: list[list[OrganisationUnit]],
        employees: list[Employee],
        employees_per_org: int,
    ) -> list[list[Role]]:
        print("Generating roles")

        employee_iter = iter(employees)

        def construct_role(org_unit: OrganisationUnit) -> Role:
            org_employees = more_itertools.take(employees_per_org, employee_iter)
            assert len(org_employees) == employees_per_org

            employee = random.choice(org_employees)
            return Role(
                role_type=RoleType(uuid=random.choice(self.role_type_uuids)),
                person=PersonRef(uuid=employee.uuid),
                org_unit=OrgUnitRef(uuid=org_unit.uuid),
                validity=self.random_validity(org_unit.validity, EmployeeValidity),
            )

        return_value = list(list(map(construct_role, layer)) for layer in org_layers)
        # Ensure all employees were consumed
        assert more_itertools.ilen(employee_iter) == 0
        return return_value

    def generate_modifications(
        self,
        role_layers: list[list[Role]],
        org_layers: list[list[OrganisationUnit]],
    ) -> list[Role]:
        org_unit_validities = {
            ou.uuid: ou.validity for ou in more_itertools.flatten(org_layers)
        }

        def construct_modification(role: Role) -> Iterator[Role]:
            while random.random() < 0.25:
                with thawed(role.copy()) as copy:
                    copy.role_type = RoleType(uuid=random.choice(self.role_type_uuids))
                    copy.validity = self.random_validity(
                        org_unit_validities[copy.org_unit.uuid], EmployeeValidity
                    )
                yield copy

        return list(
            more_itertools.flatten(
                map(construct_modification, more_itertools.flatten(role_layers))
            )
        )
