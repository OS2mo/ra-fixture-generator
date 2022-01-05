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
from ramodels.mo.details import Engagement

from .base import BaseGenerator


class EngagementGenerator(BaseGenerator):
    def generate(
        self,
        employees: List[Employee],
        org_layers: List[List[OrganisationUnit]],
        job_functions: List[Tuple[str, str, str]],
        engagement_types: List[Tuple[str, str, str]],
        employees_per_org: int = 10,
    ) -> List[List[Engagement]]:
        def construct_engagement(
            employee: Employee, org_unit: OrganisationUnit
        ) -> Engagement:
            employee_uuid = employee.uuid
            org_unit_uuid = org_unit.uuid

            job_function = random.choice(job_functions)[0]
            job_function_uuid = self.generate_uuid(job_function)

            engagement_type = random.choice(engagement_types)[0]
            engagement_type_uuid = self.generate_uuid(engagement_type)

            uuid = self.generate_uuid(
                str(employee_uuid) + str(org_unit_uuid) + str(job_function_uuid)
            )

            return Engagement.from_simplified_fields(
                uuid=uuid,
                org_unit_uuid=org_unit_uuid,
                person_uuid=employee_uuid,
                job_function_uuid=job_function_uuid,
                engagement_type_uuid=engagement_type_uuid,
                from_date="1930-01-01",
                to_date=None,
                primary_uuid=self.generate_uuid("primary"),
                user_key=str(uuid)[:8],
            )

        employee_iter = iter(employees)

        def construct_engagements(org_unit: OrganisationUnit) -> List[Engagement]:
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
