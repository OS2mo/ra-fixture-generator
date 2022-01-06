# --------------------------------------------------------------------------------------
# SPDX-FileCopyrightText: 2021 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
# --------------------------------------------------------------------------------------
from typing import List

import more_itertools
from mimesis import Person
from mimesis.builtins import DenmarkSpecProvider
from mimesis.enums import Gender
from ramodels.mo import Employee
from ramodels.mo import OrganisationUnit

from .base import BaseGenerator


class EmployeeGenerator(BaseGenerator):
    def __init__(self, seed: str = None) -> None:
        super().__init__(seed)
        self.person_gen = Person("da", seed=seed)
        self.danish_gen = DenmarkSpecProvider(seed=seed)

    def generate(
        self, org_layers: List[List[OrganisationUnit]], employees_per_org: int = 10
    ) -> List[Employee]:
        num_orgs = more_itertools.ilen(more_itertools.flatten(org_layers))

        print("Number of organisation units:", num_orgs)
        print("Number of employees:", num_orgs * employees_per_org)

        def generate_employee(_: int) -> Employee:
            def even(x: int) -> bool:
                return (x % 2) == 0

            cpr = self.danish_gen.cpr()
            gender = Gender.MALE if even(int(cpr[-1])) else Gender.FEMALE

            return Employee(
                uuid=self.generate_uuid(cpr),
                givenname=self.person_gen.name(gender=gender),
                surname=self.person_gen.surname(gender=gender),
                cpr_no=cpr,
            )

        return list(map(generate_employee, range(employees_per_org * num_orgs)))
