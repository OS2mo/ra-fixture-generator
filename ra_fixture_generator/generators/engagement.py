# --------------------------------------------------------------------------------------
# SPDX-FileCopyrightText: 2021 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
# --------------------------------------------------------------------------------------
import random
from collections.abc import Iterator
from uuid import UUID

import more_itertools
from mimesis import Person
from ramodels.mo import Employee
from ramodels.mo import OrganisationUnit
from ramodels.mo._shared import EngagementType
from ramodels.mo._shared import JobFunction
from ramodels.mo.details import Engagement

from .base import BaseGenerator
from ..util import EmployeeValidity
from ..util import thawed


class EngagementGenerator(BaseGenerator):
    def __init__(
        self,
        job_functions: dict[str, UUID],
        engagement_types: dict[str, UUID],
        primary_types: dict[str, UUID],
    ) -> None:
        super().__init__()
        self.job_function_uuids = list(job_functions.values())
        self.engagement_type_uuids = list(engagement_types.values())
        self.primary_type_uuids = list(primary_types.values())
        self.person_gen = Person("da")

    def generate(
        self,
        employees: list[Employee],
        employees_per_org: int,
        org_layers: list[list[OrganisationUnit]],
    ) -> list[list[Engagement]]:
        def construct_engagement(
            employee: Employee, org_unit: OrganisationUnit
        ) -> Engagement:
            return Engagement.from_simplified_fields(
                org_unit_uuid=org_unit.uuid,
                person_uuid=employee.uuid,
                job_function_uuid=random.choice(self.job_function_uuids),
                engagement_type_uuid=random.choice(self.engagement_type_uuids),
                primary_uuid=random.choice(self.primary_type_uuids),
                user_key=self.person_gen.identifier(mask="@@@@@@@@0###"),
                **self.validity(org_unit.validity, EmployeeValidity).dict()
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

    def generate_modifications(
        self,
        engagement_layers: list[list[Engagement]],
        org_layers: list[list[OrganisationUnit]],
    ) -> list[Engagement]:
        org_unit_validities = {
            ou.uuid: ou.validity for ou in more_itertools.flatten(org_layers)
        }

        def construct_modification(engagement: Engagement) -> Iterator[Engagement]:
            while random.random() < 0.2:
                with thawed(engagement.copy()) as copy:
                    copy.user_key = self.person_gen.identifier(mask="@@@@@@@@0###")
                    copy.validity = self.validity(
                        org_unit_validities[copy.org_unit.uuid], EmployeeValidity
                    )
                    if random.random() < 0.75:
                        copy.job_function = JobFunction(
                            uuid=random.choice(self.job_function_uuids)
                        )
                    if random.random() < 0.45:
                        copy.engagement_type = EngagementType(
                            uuid=random.choice(self.engagement_type_uuids)
                        )
                yield copy

        return list(
            more_itertools.flatten(
                map(construct_modification, more_itertools.flatten(engagement_layers))
            )
        )
