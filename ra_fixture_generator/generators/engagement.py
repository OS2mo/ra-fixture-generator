# --------------------------------------------------------------------------------------
# SPDX-FileCopyrightText: 2021 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
# --------------------------------------------------------------------------------------
import random
from uuid import UUID

import more_itertools
from mimesis import Person
from ramodels.mo import Employee
from ramodels.mo import OrganisationUnit
from ramodels.mo.details import Engagement

from .base import BaseGenerator


class EngagementGenerator(BaseGenerator):
    def __init__(self) -> None:
        super().__init__()
        self.person_gen = Person("da")

    def generate(
        self,
        employees: list[Employee],
        employees_per_org: int,
        org_layers: list[list[OrganisationUnit]],
        job_functions: dict[str, UUID],
        engagement_types: dict[str, UUID],
    ) -> list[list[Engagement]]:
        job_function_uuids = list(job_functions.values())
        engagement_type_uuids = list(engagement_types.values())

        def construct_engagement(
            employee: Employee, org_unit: OrganisationUnit
        ) -> Engagement:
            return Engagement.from_simplified_fields(
                org_unit_uuid=org_unit.uuid,
                employee_uuid=employee.uuid,
                job_function_uuid=random.choice(job_function_uuids),
                engagement_type_uuid=random.choice(engagement_type_uuids),
                from_date="1930-01-01",
                to_date=None,
                primary_uuid=self.generate_uuid("primary"),
                user_key=self.person_gen.identifier(mask="@@@@@@@@0###"),
            )

        employee_iter = iter(employees)

        def construct_engagements(org_unit: OrganisationUnit) -> list[Engagement]:
            org_employees = more_itertools.take(employees_per_org, employee_iter)
            assert len(org_employees) == employees_per_org
            return [
                construct_engagement(employee, org_unit) for employee in org_employees
            ]

        return_value = list(
            list(more_itertools.flatten(map(construct_engagements, layer)))
            for layer in org_layers
        )
        # Ensure all employees were consumed
        assert more_itertools.ilen(employee_iter) == 0
        return return_value
