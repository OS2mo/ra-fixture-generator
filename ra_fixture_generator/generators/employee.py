# --------------------------------------------------------------------------------------
# SPDX-FileCopyrightText: 2021 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
# --------------------------------------------------------------------------------------
import more_itertools
from mimesis import Person
from mimesis.builtins import DenmarkSpecProvider
from mimesis.enums import Gender
from ramodels.mo import Employee
from ramodels.mo import OrganisationUnit

from .base import BaseGenerator


class EmployeeGenerator(BaseGenerator):
    def __init__(self) -> None:
        super().__init__()
        self.person_gen = Person("da")
        self.danish_gen = DenmarkSpecProvider()

    def generate(
        self, org_layers: list[list[OrganisationUnit]], employees_per_org: int
    ) -> list[Employee]:
        num_orgs = more_itertools.ilen(more_itertools.flatten(org_layers))

        print("Number of organisation units:", num_orgs)
        print("Number of employees:", num_orgs * employees_per_org)

        def generate_employee(_: int) -> Employee:
            def even(x: int) -> bool:
                return (x % 2) == 0

            cpr = self.danish_gen.cpr()
            gender = Gender.MALE if even(int(cpr[-1])) else Gender.FEMALE

            return Employee(
                givenname=self.person_gen.name(gender=gender),
                surname=self.person_gen.surname(gender=gender),
                cpr_no=cpr,
            )

        return list(map(generate_employee, range(employees_per_org * num_orgs)))
